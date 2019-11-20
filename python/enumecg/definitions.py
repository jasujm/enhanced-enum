"""
Enum definitions
----------------

Contains the classes that the code generator uses as its representation of an
enum definition.
"""

import collections.abc as cabs
import dataclasses
import typing

from . import utils


@dataclasses.dataclass
class EnumMemberDefinition:
    """Enum member definition"""

    underlying_enumerator_name: str
    enumerator_value_constant_name: str
    enumerator_value: typing.Any


@dataclasses.dataclass
class EnumDefinition:
    """Enum definition"""

    underlying_enum_typename: str
    enhanced_enum_typename: str
    details_namespace_name: str
    members: typing.Sequence[EnumMemberDefinition]
    value_type_typename: str
    value_type_alias: str = "ValueType"


def _make_member_definition(member):
    name, value = member
    name_parts, joiner = utils.split_name(name)
    return EnumMemberDefinition(
        underlying_enumerator_name=name,
        enumerator_value_constant_name=joiner(name_parts + ["value"]),
        enumerator_value = value,
    )


def _make_definition_from_dict(enum_dict):
    typename = enum_dict["typename"]
    members = enum_dict["members"]
    typename_parts, joiner = utils.split_name(typename)
    return EnumDefinition(
        underlying_enum_typename=joiner(["underlying"] + typename_parts),
        enhanced_enum_typename=joiner(["enhanced"] + typename_parts),
        details_namespace_name=joiner(typename_parts + ["details"]),
        members=[_make_member_definition(member) for member in members.items()],
        value_type_typename="std::string_view" # TODO: infer from values
    )


def make_definition(enum) -> EnumDefinition:
    """Make :class:`EnumDefinition` instance from various types

    This function is used to convert various kinds of enum descriptions
    (standard Python :class:`enum.Enum` types, :class:`dict` instances etc.)
    into an :class:`EnumDefinition` instance usable by the code generator. It
    allows for an user to provide a simple enum description, and having the
    details filled in automatically.

    This function is mainly meant to be used by the high level functions in the
    top level :mod:`enumecg` module, but can also be invoked directly for
    greater control over the code generation process.
    """
    if isinstance(enum, EnumDefinition):
        return enum
    elif isinstance(enum, cabs.Mapping):
        return _make_definition_from_dict(enum)
    else:
        raise TypeError(
            f"Could not convert {enum!r} of type {type(enum)} into EnumDefinition"
        )
