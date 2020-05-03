from enumecg import generate, generator
from enumecg.generators import CodeGenerator


def test_generator_function_should_return_code_generator():
    assert type(generator()) is CodeGenerator


def test_generate_should_return_code(status_definition):
    assert generate(status_definition, documentation="doxygen") == CodeGenerator(
        documentation="doxygen"
    ).generate_enum_definitions(status_definition)
