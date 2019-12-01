from enumecg.definitions import EnumDefinition, EnumMemberDefinition

STATUS_DEFINITION = EnumDefinition(
    label_enum_typename="StatusLabel",
    enhanced_enum_typename="EnhancedStatus",
    value_type_typename="std::string_view",
    members=[
        EnumMemberDefinition(
            enumerator_name="INITIALIZING",
            enumerator_value_constant_name="INITIALIZING_VALUE",
            enumerator_value="initializing",
        ),
        EnumMemberDefinition(
            enumerator_name="WAITING_FOR_INPUT",
            enumerator_value_constant_name="WAITING_FOR_INPUT_VALUE",
            enumerator_value="waitingForInput",
        ),
        EnumMemberDefinition(
            enumerator_name="BUSY",
            enumerator_value_constant_name="BUSY_VALUE",
            enumerator_value="busy",
        ),
    ],
    associate_namespace_name="Statuses",
)
