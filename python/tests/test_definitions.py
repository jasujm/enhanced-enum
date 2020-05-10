import pytest

from enumecg.definitions import (
    EnumDefinition,
    EnumMemberDefinition,
    make_definition,
    PrimaryType,
)
from enumecg.exceptions import Error

from .conftest import Status


def test_make_definition_should_return_native_definition_as_is(status_definition):
    assert make_definition(status_definition) is status_definition


def test_make_definition_should_make_definition_from_dict(
    status_definition, status_definition_dict
):
    assert make_definition(status_definition_dict) == status_definition


def test_make_definition_should_make_definition_from_python_enum(status_definition):
    assert make_definition(Status) == status_definition


def test_make_definition_should_raise_error_on_unknown_type():
    with pytest.raises(Error):
        make_definition("this doesn't make sense")


def test_invalid_definition_dict_should_raise_error(status_definition_dict):
    del status_definition_dict["members"][0]["name"]
    with pytest.raises(Error):
        make_definition(status_definition_dict)


def test_make_definition_with_label_type_as_primary(
    status_definition, status_definition_dict, status_documentation
):
    status_definition.label_enum_typename = "Status"
    status_definition.label_enum_documentation = status_documentation
    assert (
        make_definition(status_definition_dict, primary_type=PrimaryType.label)
        == status_definition
    )


def test_make_definition_with_enhanced_type_as_primary(
    status_definition, status_definition_dict, status_documentation
):
    status_definition.enhanced_enum_typename = "Status"
    status_definition.enhanced_enum_documentation = status_documentation
    make_definition(
        status_definition_dict, primary_type=PrimaryType.enhanced
    ) == status_definition


def test_make_definition_type_deduction(nested_enum_definition_dict):
    nested_enum_definition = make_definition(nested_enum_definition_dict)
    assert (
        nested_enum_definition.value_type_typename
        == "std::tuple<long, std::tuple<std::string_view, bool>>"
    )


def test_make_definition_enumerator_value_initializers(nested_enum_definition_dict):
    nested_enum_definition = make_definition(nested_enum_definition_dict)
    assert nested_enum_definition.members[0].enumerator_value_initializers == [
        "0",
        ['"string"', "true"],
    ]
