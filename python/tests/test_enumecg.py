from enumecg import generate, generator
from enumecg.generators import CodeGenerator

from .common import STATUS_DEFINITION


def test_generator_function_should_return_code_generator():
    assert type(generator()) is CodeGenerator


def test_generate_should_return_code():
    assert generate(STATUS_DEFINITION, documentation="doxygen") == CodeGenerator(
        documentation="doxygen"
    ).generate_enum_definitions(STATUS_DEFINITION)
