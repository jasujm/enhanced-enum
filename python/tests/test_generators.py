import unittest

from enumecg.generators import CodeGenerator

from .common import STATUS_DEFINITION


def _generate_enum_definitions(**options):
    return CodeGenerator(**options).generate_enum_definitions(STATUS_DEFINITION)


class CodeGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.enum_definition = _generate_enum_definitions()

    def test_enum_definitions_should_contain_label_enum(self):
        self.assertIn("enum class StatusLabel", self.enum_definition)

    def test_enum_definitions_should_contain_enhanced_enum(self):
        self.assertIn("struct EnhancedStatus", self.enum_definition)

    def test_enum_definitions_should_contain_enhance_function(self):
        self.assertRegex(
            self.enum_definition, r"EnhancedStatus enhance\(StatusLabel \w+\)",
        )

    def test_enum_definitions_should_contain_value_type(self):
        self.assertIn(STATUS_DEFINITION.value_type_typename, self.enum_definition)

    def test_enum_definitions_should_contain_enumerators(self):
        snippet = self.enum_definition
        for member in STATUS_DEFINITION.members:
            self.assertIn(member.enumerator_name, snippet)

    def test_enum_definitions_should_contain_value_constants(self):
        snippet = self.enum_definition
        for member in STATUS_DEFINITION.members:
            self.assertIn(member.enumerator_value_constant_name, snippet)
            self.assertIn(member.enumerator_value_initializers, snippet)

    def test_enum_definitions_should_contain_associate_namespace(self):
        self.assertIn("namespace Statuses", self.enum_definition)


class CodeGeneratorDocumentationTest(unittest.TestCase):
    def test_enum_definitions_should_not_contain_documentation_if_not_requested(self):
        self.assertNotIn("/**", _generate_enum_definitions(documentation=None))

    def test_enum_definitions_should_contain_documentation_if_requested(self):
        self.assertIn("/**", _generate_enum_definitions(documentation="doxygen"))

    def test_unsupported_documentation_style(self):
        self.assertRaises(ValueError, CodeGenerator, documentation="invalid")
