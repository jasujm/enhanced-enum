import pytest

from enumecg import generate, generator
from enumecg.generators import CodeGenerator, DocumentationStyle
from enumecg.definitions import PrimaryType
from enumecg.exceptions import Error


def test_generator_function_should_return_code_generator():
    assert type(generator()) is CodeGenerator


def test_generate_should_return_code(status_definition):
    assert generate(status_definition, documentation="doxygen") == CodeGenerator(
        documentation=DocumentationStyle.doxygen
    ).generate_enum_definitions(status_definition)


@pytest.mark.parametrize("primary_type", PrimaryType)
def test_generate_should_accept_primary_type_as_string(
    status_definition_dict, primary_type
):
    assert generate(
        status_definition_dict, primary_type=primary_type.value
    ) == generate(status_definition_dict, primary_type=primary_type)


@pytest.mark.parametrize("documentation", DocumentationStyle)
def test_generate_should_accept_documentation_as_string(
    status_definition_dict, documentation
):
    assert generate(
        status_definition_dict, documentation=documentation.value
    ) == generate(status_definition_dict, documentation=documentation)


def test_invalid_primary_type_should_raise_error(status_definition):
    with pytest.raises(Error):
        generate(status_definition, primary_type="invalid")


def test_invalid_documentation_should_raise_error(status_definition):
    with pytest.raises(Error):
        generate(status_definition, documentation="invalid")
