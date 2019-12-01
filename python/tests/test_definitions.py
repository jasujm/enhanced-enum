import copy
import enum
import unittest

from .common import STATUS_DEFINITION

from enumecg.definitions import EnumDefinition, EnumMemberDefinition, make_definition


class Status(enum.Enum):
    INITIALIZING = "initializing"
    WAITING_FOR_INPUT = "waitingForInput"
    BUSY = "busy"


STATUS_DEFINITION_DICT = {
    "typename": "Status",
    "members": {
        "INITIALIZING": "initializing",
        "WAITING_FOR_INPUT": "waitingForInput",
        "BUSY": "busy",
    },
}


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
