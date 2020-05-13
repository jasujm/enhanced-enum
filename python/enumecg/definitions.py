"""
Enum definitions
................

Contains the classes that the code generator uses as its
representation of an enum definition.
"""

import collections.abc as cabc
import enum as py_enum
import dataclasses
import typing

import docstring_parser

from . import utils, exceptions


class PrimaryType(py_enum.Enum):
    """Possible primary types when generating enum definitions

    These are the accepted choices for the ``primary_type`` argument
    in :func:`make_definition()`.
    """

    label = "label"
    """Label enum is the primary type"""

    enhanced = "enhanced"
    """Enhanced enum is the primary type"""


@dataclasses.dataclass
class EnumDocumentation:
    """Documentation associated with an enum"""

    short_description: typing.Optional[str]
    long_description: typing.Optional[str]


@dataclasses.dataclass
class EnumMemberDefinition:
    """Enum member definition"""

    enumerator_name: str
    enumerator_value_constant_name: str
    enumerator_value_initializers: typing.Union[typing.Sequence, str]


@dataclasses.dataclass
class EnumDefinition:
    """Enum definition"""

    label_enum_typename: str
    enhanced_enum_typename: str
    value_type_typename: str
    members: typing.Sequence[EnumMemberDefinition]
    associate_namespace_name: str
    label_enum_documentation: typing.Optional[EnumDocumentation] = None
    enhanced_enum_documentation: typing.Optional[EnumDocumentation] = None


Enum = typing.Union[EnumDefinition, typing.Mapping, py_enum.EnumMeta]
"""Generic enum definition

Types accepted by :func:`make_definition()` and other functions that
are used to generate enhanced enum definition.
"""


def _make_definition_from_dict(enum_dict, *, primary_type, value_type):
    typename = enum_dict["typename"]
    members = enum_dict["members"]
    formatter = utils.NameFormatter(typename)
    member_formatter = utils.NameFormatter(*(member["name"] for member in members))
    label_enum_typename = (
        formatter.join(formatter.parts[0] + ["label"])
        if primary_type != PrimaryType.label
        else typename
    )
    enhanced_enum_typename = (
        formatter.join(["enhanced"] + formatter.parts[0])
        if primary_type != PrimaryType.enhanced
        else typename
    )
    type_deducer = utils.CppTypeDeducer(
        *(member["value"] for member in members), type_name=value_type
    )
    unparsed_docstring = enum_dict.get("docstring")
    if unparsed_docstring:
        parsed_docstring = docstring_parser.parse(unparsed_docstring)
        documentation = EnumDocumentation(
            short_description=parsed_docstring.short_description,
            long_description=parsed_docstring.long_description,
        )
    else:
        documentation = None
    return EnumDefinition(
        label_enum_typename=label_enum_typename,
        enhanced_enum_typename=enhanced_enum_typename,
        value_type_typename=type_deducer.type_name,
        members=[
            EnumMemberDefinition(
                enumerator_name=member["name"],
                enumerator_value_constant_name=member_formatter.join(
                    member_formatter.parts[n] + ["value"]
                ),
                enumerator_value_initializers=type_deducer.get_initializer(
                    member["value"]
                ),
            )
            for (n, member) in enumerate(members)
        ],
        associate_namespace_name=formatter.join(formatter.parts[0], pluralize=True),
        label_enum_documentation=documentation
        if primary_type == PrimaryType.label
        else None,
        enhanced_enum_documentation=documentation
        if primary_type == PrimaryType.enhanced
        else None,
    )


def _extract_python_enum_attrs(enum):
    return {
        "typename": enum.__name__,
        "members": [{"name": member.name, "value": member.value} for member in enum],
        "docstring": enum.__doc__,
    }


def make_definition(
    enum: Enum,
    *,
    primary_type: typing.Optional[PrimaryType] = None,
    value_type: typing.Optional[str] = None,
) -> EnumDefinition:
    """Make :class:`EnumDefinition` instance from various types

    This function is used to convert various kinds of enum definitions
    (standard Python :class:`enum.Enum` types, :class:`dict` instances
    etc.) into an :class:`EnumDefinition` instance usable by the code
    generator. It allows for an user to provide a simpler enum
    definition, and having the details filled in automatically.

    This function is mainly meant to be used by the high level
    functions in the top level :mod:`enumecg` module, but can also be
    invoked directly for greater control over the code generation
    process.

    Parameters:
        enum: The enum definition.
        primary_type: A :class:`PrimaryType` enumerator indicating the
                      primary type. See :ref:`enumecg-primary-enum`.
        value_type: See :ref:`enumerator-value-type`.

    Raises:
        :exc:`exceptions.Error`: If ``enum`` is invalid and cannot be
          converted to :class:`EnumDefinition`.
    """
    if isinstance(enum, EnumDefinition):
        return enum

    if isinstance(enum, py_enum.EnumMeta):
        enum = _extract_python_enum_attrs(enum)
    elif not isinstance(enum, cabc.Mapping):
        raise exceptions.Error(
            f"Could not convert {enum!r} of type {type(enum)} into EnumDefinition"
        )

    try:
        return _make_definition_from_dict(
            enum, primary_type=primary_type, value_type=value_type
        )
    except (KeyError, AttributeError, TypeError, ValueError) as ex:
        raise exceptions.Error(
            f"Failed to convert {enum!r} into an enum definition"
        ) from ex
