import copy
import pytest

from .common import (
    STATUS_DEFINITION,
    Status,
    STATUS_DEFINITION_DICT,
    NESTED_ENUM_DEFINITION_DICT,
    STATUS_DOCUMENTATION,
)

from enumecg.definitions import EnumDefinition, EnumMemberDefinition, make_definition


def test_make_definition_should_return_native_definition_as_is():
    assert make_definition(STATUS_DEFINITION) is STATUS_DEFINITION


def test_make_definition_should_make_definition_from_dict():
    assert make_definition(STATUS_DEFINITION_DICT) == STATUS_DEFINITION


def test_make_definition_should_make_definition_from_python_enum():
    assert make_definition(Status) == STATUS_DEFINITION


def test_make_definition_should_raise_error_on_unknown_type():
    with pytest.raises(TypeError):
        make_definition("this doesn't make sense")


def test_make_definition_with_label_type_as_primary():
    definition = copy.copy(STATUS_DEFINITION)
    definition.label_enum_typename = "Status"
    definition.label_enum_documentation = STATUS_DOCUMENTATION
    assert make_definition(STATUS_DEFINITION_DICT, primary_type="label") == definition


def test_make_definition_with_enhanced_type_as_primary():
    definition = copy.copy(STATUS_DEFINITION)
    definition.enhanced_enum_typename = "Status"
    definition.enhanced_enum_documentation = STATUS_DOCUMENTATION
    make_definition(STATUS_DEFINITION_DICT, primary_type="enhanced") == definition


def test_make_definition_type_deduction():
    nested_enum_definition = make_definition(NESTED_ENUM_DEFINITION_DICT)
    assert (
        nested_enum_definition.value_type_typename
        == "std::tuple<long, std::tuple<std::string_view, bool>>"
    )


def test_make_definition_enumerator_value_initializers():
    nested_enum_definition = make_definition(NESTED_ENUM_DEFINITION_DICT)
    assert nested_enum_definition.members[0].enumerator_value_initializers == [
        "0",
        ['"string"', "true"],
    ]
