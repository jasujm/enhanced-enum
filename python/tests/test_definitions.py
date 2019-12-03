import copy
import unittest

from .common import (
    STATUS_DEFINITION,
    Status,
    STATUS_DEFINITION_DICT,
    NESTED_ENUM_DEFINITION_DICT,
)

from enumecg.definitions import EnumDefinition, EnumMemberDefinition, make_definition


class EnumDefinitionTest(unittest.TestCase):
    def test_make_definition_should_return_native_definition_as_is(self):
        self.assertIs(make_definition(STATUS_DEFINITION), STATUS_DEFINITION)

    def test_make_definition_should_make_definition_from_dict(self):
        self.assertEqual(make_definition(STATUS_DEFINITION_DICT), STATUS_DEFINITION)

    def test_make_definition_should_make_definition_from_python_enum(self):
        self.assertEqual(make_definition(Status), STATUS_DEFINITION)

    def test_make_definition_should_raise_error_on_unknown_type(self):
        self.assertRaises(TypeError, make_definition, "this doesn't make sense")

    def test_make_definition_with_label_type_as_primary(self):
        definition = copy.copy(STATUS_DEFINITION)
        definition.label_enum_typename = "Status"
        self.assertEqual(
            make_definition(STATUS_DEFINITION_DICT, primary_type="label"), definition
        )

    def test_make_definition_with_enhanced_type_as_primary(self):
        definition = copy.copy(STATUS_DEFINITION)
        definition.enhanced_enum_typename = "Status"
        self.assertEqual(
            make_definition(STATUS_DEFINITION_DICT, primary_type="enhanced"), definition
        )

    def test_make_definition_type_deduction(self):
        nested_enum_definition = make_definition(NESTED_ENUM_DEFINITION_DICT)
        self.assertEqual(
            nested_enum_definition.value_type_typename,
            "std::tuple<long, std::tuple<std::string_view, bool>>",
        )

    def test_make_definition_enumerator_value_initializers(self):
        nested_enum_definition = make_definition(NESTED_ENUM_DEFINITION_DICT)
        self.assertSequenceEqual(
            nested_enum_definition.members[0].enumerator_value_initializers,
            ["0", ['"string"', "true"]],
        )
