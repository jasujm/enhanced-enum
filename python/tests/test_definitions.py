import enum
import unittest

from .common import STATUS_DEFINITION

from enumecg.definitions import EnumDefinition, EnumMemberDefinition, make_definition


class EnumDefinitionTest(unittest.TestCase):
    def test_make_definition_should_return_native_definition_as_is(self):
        self.assertIs(make_definition(STATUS_DEFINITION), STATUS_DEFINITION)

    def test_make_definition_should_make_definition_from_dict(self):
        definition_dict = {
            "typename": "Status",
            "members": {
                "INITIALIZING": "initializing",
                "WAITING_FOR_INPUT": "waitingForInput",
                "BUSY": "busy",
            },
        }
        self.assertEqual(make_definition(definition_dict), STATUS_DEFINITION)

    def test_make_definition_should_make_definition_from_python_enum(self):
        class Status(enum.Enum):
            INITIALIZING = "initializing"
            WAITING_FOR_INPUT = "waitingForInput"
            BUSY = "busy"

        self.assertEqual(make_definition(Status), STATUS_DEFINITION)

    def test_make_definition_should_raise_error_on_unknown_type(self):
        self.assertRaises(TypeError, make_definition, "this doesn't make sense")
