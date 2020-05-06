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

from . import utils


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


def _make_definition_from_dict(enum_dict, *, primary_type, value_type):
    typename = enum_dict["typename"]
    members = enum_dict["members"]
    formatter = utils.NameFormatter(typename)
    member_formatter = utils.NameFormatter(*(member["name"] for member in members))
    label_enum_typename = (
        formatter.join(formatter.parts[0] + ["label"])
        if primary_type != "label"
        else typename
    )
    enhanced_enum_typename = (
        formatter.join(["enhanced"] + formatter.parts[0])
        if primary_type != "enhanced"
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
        label_enum_documentation=documentation if primary_type == "label" else None,
        enhanced_enum_documentation=documentation
        if primary_type == "enhanced"
        else None,
    )


def _extract_python_enum_attrs(enum):
    return {
        "typename": enum.__name__,
        "members": [{"name": member.name, "value": member.value} for member in enum],
        "docstring": enum.__doc__,
    }


def make_definition(
    enum,
    *,
    primary_type: typing.Optional[str] = None,
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
        primary_type: See :ref:`enumecg-primary-enum`.
        value_type: See :ref:`enumerator-value-type`.
    """
    if isinstance(enum, EnumDefinition):
        return enum
    elif isinstance(enum, cabc.Mapping):
        return _make_definition_from_dict(
            enum, primary_type=primary_type, value_type=value_type
        )
    elif isinstance(enum, py_enum.EnumMeta):
        return _make_definition_from_dict(
            _extract_python_enum_attrs(enum),
            primary_type=primary_type,
            value_type=value_type,
        )
    else:
        raise TypeError(
            f"Could not convert {enum!r} of type {type(enum)} into EnumDefinition"
        )
