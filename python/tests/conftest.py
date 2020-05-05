import copy
import enum
import pytest

from enumecg.definitions import EnumDefinition, EnumMemberDefinition, EnumDocumentation


class Status(enum.Enum):
    """An example enumeration for testing

    This is a long description of the test enum."""

    INITIALIZING = "initializing"
    WAITING_FOR_INPUT = "waitingForInput"
    BUSY = "busy"


"""The :class:`definitions.EnumDefinition` expected to be generated from :class:`Status`

This is global constant. For copy that can be modified, please use the
:func:`status_definition()` fixture.
"""
STATUS_DEFINITION = EnumDefinition(
    label_enum_typename="StatusLabel",
    enhanced_enum_typename="EnhancedStatus",
    value_type_typename="std::string_view",
    members=[
        EnumMemberDefinition(
            enumerator_name="INITIALIZING",
            enumerator_value_constant_name="INITIALIZING_VALUE",
            enumerator_value_initializers='"initializing"',
        ),
        EnumMemberDefinition(
            enumerator_name="WAITING_FOR_INPUT",
            enumerator_value_constant_name="WAITING_FOR_INPUT_VALUE",
            enumerator_value_initializers='"waitingForInput"',
        ),
        EnumMemberDefinition(
            enumerator_name="BUSY",
            enumerator_value_constant_name="BUSY_VALUE",
            enumerator_value_initializers='"busy"',
        ),
    ],
    associate_namespace_name="Statuses",
)

""":class:`dict` representation of :const:`STATUS_DEFINITION`

This is global constant. For copy that can be modified, please use the
:func:`status_definition_dict()` fixture.
"""
STATUS_DEFINITION_DICT = {
    "typename": "Status",
    "docstring": Status.__doc__,
    "members": [
        {"name": "INITIALIZING", "value": "initializing",},
        {"name": "WAITING_FOR_INPUT", "value": "waitingForInput",},
        {"name": "BUSY", "value": "busy",},
    ],
}


"""Sample nested enum definition

This is global constant. For copy that can be modified, please use the
:func:`nested_enum_definition_dict()` fixture.
"""
NESTED_ENUM_DEFINITION_DICT = {
    "typename": "NestedEnum",
    "members": [{"name": "enumerator", "value": (0, ("string", True))}],
}


@pytest.fixture
def status_definition():
    """Return deep copy of :const:`STATUS_DEFINITION`

    This definition is expected to be generated from
    :class:`Status`. Can be modified by a test case because this is a
    copy.
    """
    return copy.deepcopy(STATUS_DEFINITION)


@pytest.fixture
def status_definition_dict():
    """Return deep copy of :const:`STATUS_DEFINITION_DICT`

    This definition is expected to be generated from
    :class:`Status`. Can be modified by a test case because this is a
    copy.
    """
    return copy.deepcopy(STATUS_DEFINITION_DICT)


@pytest.fixture
def nested_enum_definition_dict():
    """Return deep copy of :const:`NESTED_ENUM_DEFINITION_DICT`

    This definition is expected to be generated from
    :class:`Status`. Can be modified by a test case because this is a
    copy.
    """
    return copy.deepcopy(NESTED_ENUM_DEFINITION_DICT)


@pytest.fixture
def status_documentation():
    """Return :class:`definitions.EnumDocumentation` expected to be generated from :class:`Status`"""
    return EnumDocumentation(
        short_description="An example enumeration for testing",
        long_description="This is a long description of the test enum.",
    )
