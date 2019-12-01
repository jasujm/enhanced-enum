"""
Enum definitions
................

Contains the classes that the code generator uses as its representation of an
enum definition.
"""

import collections
import collections.abc as cabs
import enum as py_enum
import dataclasses
import typing

from . import utils


@dataclasses.dataclass
class EnumMemberDefinition:
    """Enum member definition"""

    enumerator_name: str
    enumerator_value_constant_name: str
    enumerator_value: typing.Any


@dataclasses.dataclass
class EnumDefinition:
    """Enum definition"""

    label_enum_typename: str
    enhanced_enum_typename: str
    value_type_typename: str
    members: typing.Sequence[EnumMemberDefinition]
    associate_namespace_name: str


def _make_definition_from_dict(enum_dict, **options):
    typename = enum_dict["typename"]
    members = enum_dict["members"]
    formatter = utils.NameFormatter(typename)
    member_formatter = utils.NameFormatter(*members.keys())
    primary_type = options.get("primary_type")
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
    return EnumDefinition(
        label_enum_typename=label_enum_typename,
        enhanced_enum_typename=enhanced_enum_typename,
        value_type_typename="std::string_view",  # TODO: infer from values
        members=[
            EnumMemberDefinition(
                enumerator_name=member_name,
                enumerator_value_constant_name=member_formatter.join(
                    member_formatter.parts[n] + ["value"]
                ),
                enumerator_value=member_value,
            )
            for (n, (member_name, member_value)) in enumerate(members.items())
        ],
        associate_namespace_name=formatter.join(formatter.parts[0], pluralize=True),
    )


def _extract_python_enum_attrs(enum):
    return {
        "typename": enum.__name__,
        "members": collections.OrderedDict(
            (member.name, member.value) for member in enum
        ),
    }


def make_definition(enum, **options) -> EnumDefinition:
    """Make :class:`EnumDefinition` instance from various types

    This function is used to convert various kinds of enum descriptions
    (standard Python :class:`enum.Enum` types, :class:`dict` instances etc.)
    into an :class:`EnumDefinition` instance usable by the code generator. It
    allows for an user to provide a simple enum description, and having the
    details filled in automatically.

    This function is mainly meant to be used by the high level functions in the
    top level :mod:`enumecg` module, but can also be invoked directly for
    greater control over the code generation process.

    Parameters:
        enum: The convertible enum description
        options: The conversion options
    """
    if isinstance(enum, EnumDefinition):
        return enum
    elif isinstance(enum, cabs.Mapping):
        return _make_definition_from_dict(enum, **options)
    elif isinstance(enum, py_enum.EnumMeta):
        return _make_definition_from_dict(_extract_python_enum_attrs(enum), **options)
    else:
        raise TypeError(
            f"Could not convert {enum!r} of type {type(enum)} into EnumDefinition"
        )
