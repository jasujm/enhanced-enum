"""
Code generator
..............

The module contains the code generator consuming enum definitions and
outputting C++ code.
"""

import jinja2


class CodeGenerator:
    """Code generator for an enhanced enum type

    Used to generate the necessary C++ definitions to make an enum type
    compatible with the Enhanced Enum library.

    The recommended way to create an instance is by using the
    :func:`enumecg.generator()` function.
    """

    _JINJA_ENV = jinja2.Environment(loader=jinja2.PackageLoader(__name__))

    def __init__(self, enum_definition: "definitions.EnumDefinition"):
        """
        Parameters:
            enum_definition: The definition used to generate the C++ code
        """
        self.enum_definition = enum_definition
        self._enum_definitions_template = self._JINJA_ENV.get_template(
            "enum_definitions.hh.in"
        )

    @staticmethod
    def _as_cxx_initializer(value):
        return f'"{value}"'

    def generate_enum_definitions(self):
        """Generate the C++ definitions needed for an enhanced enum

        Returns:
            The generated code
        """
        return self._enum_definitions_template.render(
            d=self.enum_definition, initializer=self._as_cxx_initializer
        )
