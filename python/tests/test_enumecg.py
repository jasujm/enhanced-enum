import unittest

from enumecg import generate, generator
from enumecg.generators import CodeGenerator

from .common import STATUS_DEFINITION


class EnumECGTest(unittest.TestCase):
    def test_generator_function_should_return_code_generator(self):
        self.assertIsInstance(generator(), CodeGenerator)

    def test_generate_should_return_code(self):
        self.assertEqual(
            generate(STATUS_DEFINITION, documentation="doxygen"),
            CodeGenerator(documentation="doxygen").generate_enum_definitions(
                STATUS_DEFINITION
            ),
        )
