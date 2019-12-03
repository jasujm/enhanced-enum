"""
Code generator
..............

The module contains the code generator consuming enum definitions and
outputting C++ code.
"""

import collections.abc as cabc
import jinja2


def _make_initializer_list(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, cabc.Iterable):
        value_initializer_list = ", ".join(_make_initializer_list(v) for v in value)
        return f"{{ {value_initializer_list} }}"
    raise ValueError("Argument not str or an iterable: {value!r}")


def _make_initializer_list_ensure_outer_braces(value):
    if isinstance(value, str):
        value = [value]
    return _make_initializer_list(value)


def _create_jinja_env():
    env = jinja2.Environment(loader=jinja2.PackageLoader(__name__))
    env.filters["initializer_list"] = _make_initializer_list_ensure_outer_braces
    return env


class CodeGenerator:
    """Code generator for an enhanced enum type

    Used to generate the necessary C++ definitions to make an enum type
    compatible with the Enhanced Enum library.

    The recommended way to create an instance is by using the
    :func:`enumecg.generator()` function.
    """

    _JINJA_ENV = _create_jinja_env()

    def __init__(self, enum_definition: "definitions.EnumDefinition"):
        """
        Parameters:
            enum_definition: The definition used to generate the C++ code
        """
        self.enum_definition = enum_definition
        self._enum_definitions_template = self._JINJA_ENV.get_template(
            "enum_definitions.hh.in"
        )

    def generate_enum_definitions(self):
        """Generate the C++ definitions needed for an enhanced enum

        Returns:
            The generated code
        """
        return self._enum_definitions_template.render(d=self.enum_definition)
