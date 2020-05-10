import pytest
import re

from enumecg.generators import CodeGenerator, DocumentationStyle
from enumecg.exceptions import Error

from .conftest import STATUS_DEFINITION


def _generate_enum_definitions(definition, documentation=None):
    return CodeGenerator(documentation=documentation).generate_enum_definitions(
        definition
    )


@pytest.fixture
def enum_code(status_definition):
    """Return generated enum definition (C++ code) from the :func:`status_definition()` fixture"""
    return _generate_enum_definitions(status_definition)


def test_enum_definitions_should_contain_label_enum(enum_code):
    assert "enum class StatusLabel" in enum_code


def test_enum_definitions_should_contain_enhanced_enum(enum_code):
    assert "struct EnhancedStatus" in enum_code


def test_enum_definitions_should_contain_enhance_function(enum_code):
    assert re.search(r"EnhancedStatus enhance\(StatusLabel \w+\)", enum_code)


def test_enum_definitions_should_contain_value_type(status_definition, enum_code):
    assert status_definition.value_type_typename in enum_code


@pytest.mark.parametrize("member", STATUS_DEFINITION.members)
def test_enum_definitions_should_contain_enumerators(enum_code, member):
    assert member.enumerator_name in enum_code


@pytest.mark.parametrize("member", STATUS_DEFINITION.members)
def test_enum_definitions_should_contain_value_constants(enum_code, member):
    assert member.enumerator_value_constant_name in enum_code


@pytest.mark.parametrize("member", STATUS_DEFINITION.members)
def test_enum_definitions_should_contain_value_initializers(enum_code, member):
    assert member.enumerator_value_initializers in enum_code


def test_enum_definitions_should_contain_associate_namespace(enum_code):
    assert "namespace Statuses" in enum_code


def test_enum_definitions_should_not_contain_documentation_if_not_requested(
    status_definition,
):
    assert "/**" not in _generate_enum_definitions(
        status_definition, documentation=None
    )


def test_enum_definitions_should_contain_documentation_if_requested(status_definition):
    assert "/**" in _generate_enum_definitions(
        status_definition, documentation=DocumentationStyle.doxygen
    )


def test_label_enum_documentation_should_contain_short_description(
    status_definition, status_documentation
):
    status_definition.label_enum_documentation = status_documentation
    assert status_documentation.short_description in _generate_enum_definitions(
        status_definition, documentation=DocumentationStyle.doxygen
    )


def test_label_enum_documentation_should_contain_long_description(
    status_definition, status_documentation
):
    status_definition.label_enum_documentation = status_documentation
    assert status_documentation.long_description in _generate_enum_definitions(
        status_definition, documentation=DocumentationStyle.doxygen
    )


def test_enhanced_enum_documentation_should_contain_short_description(
    status_definition, status_documentation
):
    status_definition.enhanced_enum_documentation = status_documentation
    assert status_documentation.short_description in _generate_enum_definitions(
        status_definition, documentation=DocumentationStyle.doxygen
    )


def test_enhanced_enum_documentation_should_contain_long_description(
    status_definition, status_documentation
):
    status_definition.enhanced_enum_documentation = status_documentation
    assert status_documentation.long_description in _generate_enum_definitions(
        status_definition, documentation=DocumentationStyle.doxygen
    )


def test_code_generation_should_fail_if_enum_definition_is_invalid(status_definition):
    status_definition.members[0].enumerator_value_initializers = object()
    with pytest.raises(Error):
        _generate_enum_definitions(status_definition)
