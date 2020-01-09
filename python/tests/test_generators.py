import unittest

from enumecg.generators import CodeGenerator

from .common import STATUS_DEFINITION


class CodeGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.gen = CodeGenerator(STATUS_DEFINITION)

    def test_enum_definitions_should_contain_label_enum(self):
        self.assertIn("enum class StatusLabel", self.gen.generate_enum_definitions())

    def test_enum_definitions_should_contain_enhanced_enum(self):
        self.assertIn("struct EnhancedStatus", self.gen.generate_enum_definitions())

    def test_enum_definitions_should_contain_enhance_function(self):
        self.assertRegex(
            self.gen.generate_enum_definitions(),
            r"EnhancedStatus enhance\(StatusLabel \w+\)",
        )

    def test_enum_definitions_should_contain_value_type(self):
        self.assertIn(
            STATUS_DEFINITION.value_type_typename, self.gen.generate_enum_definitions()
        )

    def test_enum_definitions_should_contain_enumerators(self):
        snippet = self.gen.generate_enum_definitions()
        for member in STATUS_DEFINITION.members:
            self.assertIn(member.enumerator_name, snippet)

    def test_enum_definitions_should_contain_value_constants(self):
        snippet = self.gen.generate_enum_definitions()
        for member in STATUS_DEFINITION.members:
            self.assertIn(member.enumerator_value_constant_name, snippet)
            self.assertIn(member.enumerator_value_initializers, snippet)

    def test_enum_definitions_should_contain_associate_namespace(self):
        self.assertIn("namespace Statuses", self.gen.generate_enum_definitions())

    def test_enum_definitions_should_not_contain_documentation_if_not_requested(self):
        self.assertNotIn("/**", self.gen.generate_enum_definitions(documentation=None))

    def test_enum_definitions_should_contain_documentation_if_requested(self):
        self.assertIn(
            "/**", self.gen.generate_enum_definitions(documentation="doxygen")
        )
        print(self.gen.generate_enum_definitions(documentation="doxygen"))

    def test_unsupported_documentation_style(self):
        self.assertRaises(
            ValueError, self.gen.generate_enum_definitions, documentation="invalid"
        )
