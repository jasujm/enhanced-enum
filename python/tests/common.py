from enumecg.definitions import EnumDefinition, EnumMemberDefinition

STATUS_DEFINITION = EnumDefinition(
    label_enum_typename="StatusLabel",
    enhanced_enum_typename="EnhancedStatus",
    details_namespace_name="StatusDetails",
    members=[
        EnumMemberDefinition(
            label_enumerator_name="INITIALIZING",
            enumerator_value_constant_name="INITIALIZING_VALUE",
            enumerator_value="initializing",
        ),
        EnumMemberDefinition(
            label_enumerator_name="WAITING_FOR_INPUT",
            enumerator_value_constant_name="WAITING_FOR_INPUT_VALUE",
            enumerator_value="waitingForInput",
        ),
        EnumMemberDefinition(
            label_enumerator_name="BUSY",
            enumerator_value_constant_name="BUSY_VALUE",
            enumerator_value="busy",
        ),
    ],
    value_type_typename="std::string_view",
    value_type_alias="ValueType",
)
