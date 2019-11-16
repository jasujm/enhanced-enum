"""
Enum definitions
----------------

Contains the classes that the code generator uses as its representation of an
enum definition.
"""

import dataclasses
import typing


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
    value_type_alias: str
