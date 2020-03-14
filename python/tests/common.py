import enum

from enumecg.definitions import EnumDefinition, EnumMemberDefinition, EnumDocumentation


class Status(enum.Enum):
    """An example enumeration for testing

    This is a long description of the test enum."""

    INITIALIZING = "initializing"
    WAITING_FOR_INPUT = "waitingForInput"
    BUSY = "busy"


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

STATUS_DEFINITION_DICT = {
    "typename": "Status",
    "docstring": Status.__doc__,
    "members": {
        "INITIALIZING": "initializing",
        "WAITING_FOR_INPUT": "waitingForInput",
        "BUSY": "busy",
    },
}


NESTED_ENUM_DEFINITION_DICT = {
    "typename": "NestedEnum",
    "members": {"enumerator": (0, ("string", True))},
}


STATUS_DOCUMENTATION = EnumDocumentation(
    short_description="An example enumeration for testing",
    long_description="This is a long description of the test enum.",
)
