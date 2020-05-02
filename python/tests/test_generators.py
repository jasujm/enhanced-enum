import copy
import pytest
import re

from enumecg.generators import CodeGenerator

from .common import STATUS_DEFINITION, STATUS_DOCUMENTATION


def _generate_enum_definitions(definition=STATUS_DEFINITION, **options):
    return CodeGenerator(**options).generate_enum_definitions(definition)


@pytest.fixture
def enum_definition():
    return _generate_enum_definitions(STATUS_DEFINITION)


def test_enum_definitions_should_contain_label_enum(enum_definition):
    assert "enum class StatusLabel" in enum_definition


def test_enum_definitions_should_contain_enhanced_enum(enum_definition):
    assert "struct EnhancedStatus" in enum_definition


def test_enum_definitions_should_contain_enhance_function(enum_definition):
    assert re.search(r"EnhancedStatus enhance\(StatusLabel \w+\)", enum_definition)


def test_enum_definitions_should_contain_value_type(enum_definition):
    assert STATUS_DEFINITION.value_type_typename in enum_definition


@pytest.mark.parametrize("member", STATUS_DEFINITION.members)
def test_enum_definitions_should_contain_enumerators(enum_definition, member):
    assert member.enumerator_name in enum_definition


@pytest.mark.parametrize("member", STATUS_DEFINITION.members)
def test_enum_definitions_should_contain_value_constants(enum_definition, member):
    assert member.enumerator_value_constant_name in enum_definition


@pytest.mark.parametrize("member", STATUS_DEFINITION.members)
def test_enum_definitions_should_contain_value_initializers(enum_definition, member):
    assert member.enumerator_value_initializers in enum_definition


def test_enum_definitions_should_contain_associate_namespace(enum_definition):
    assert "namespace Statuses" in enum_definition


def test_enum_definitions_should_not_contain_documentation_if_not_requested():
    assert "/**" not in _generate_enum_definitions(documentation=None)


def test_enum_definitions_should_contain_documentation_if_requested():
    assert "/**" in _generate_enum_definitions(documentation="doxygen")


def test_label_enum_documentation_should_contain_short_description():
    definition = copy.copy(STATUS_DEFINITION)
    definition.label_enum_documentation = STATUS_DOCUMENTATION
    assert STATUS_DOCUMENTATION.short_description in _generate_enum_definitions(
        definition, documentation="doxygen"
    )


def test_label_enum_documentation_should_contain_long_description():
    definition = copy.copy(STATUS_DEFINITION)
    definition.label_enum_documentation = STATUS_DOCUMENTATION
    assert STATUS_DOCUMENTATION.long_description in _generate_enum_definitions(
        definition, documentation="doxygen"
    )


def test_enhanced_enum_documentation_should_contain_short_description():
    definition = copy.copy(STATUS_DEFINITION)
    definition.enhanced_enum_documentation = STATUS_DOCUMENTATION
    assert STATUS_DOCUMENTATION.short_description in _generate_enum_definitions(
        definition, documentation="doxygen"
    )


def test_enhanced_enum_documentation_should_contain_long_description():
    definition = copy.copy(STATUS_DEFINITION)
    definition.enhanced_enum_documentation = STATUS_DOCUMENTATION
    assert STATUS_DOCUMENTATION.long_description in _generate_enum_definitions(
        definition, documentation="doxygen"
    )


def test_unsupported_documentation_style():
    with pytest.raises(ValueError):
        CodeGenerator(documentation="invalid")
