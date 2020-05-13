"""
Code generator
..............

The module contains the code generator consuming enum definitions and
outputting C++ code.
"""

import collections.abc as cabc
import enum as py_enum
import typing

import jinja2

from . import definitions, exceptions


class DocumentationStyle(py_enum.Enum):
    """Possible documentation styles

    These are the accepted choices for the ``documentation`` argument
    in :func:`CodeGenerator()`.
    """

    doxygen = "doxygen"
    """Doxygen documentation style"""


def _make_initializer_list(value):
    if isinstance(value, str):
        return value
    if isinstance(value, cabc.Iterable):
        value_initializer_list = ", ".join(_make_initializer_list(v) for v in value)
        return f"{{ {value_initializer_list} }}"
    raise exceptions.Error("Argument not str or an iterable: {value!r}")


def _make_initializer_list_ensure_outer_braces(value):
    if isinstance(value, str):
        value = [value]
    return _make_initializer_list(value)


def _doxygenize(value):
    return value.replace("\n", "\n * ")


def _create_jinja_env():
    env = jinja2.Environment(loader=jinja2.PackageLoader(__name__))
    env.filters["initializer_list"] = _make_initializer_list_ensure_outer_braces
    env.filters["doxygenize"] = _doxygenize
    return env


# pylint: disable=too-few-public-methods
class CodeGenerator:
    """Code generator for an enhanced enum type

    Used to generate the necessary C++ boilerplate to make an enum type
    compatible with the Enhanced Enum library.

    The recommended way to create an instance is by using the
    :func:`enumecg.generator()` function.
    """

    _JINJA_ENV = _create_jinja_env()

    def __init__(self, *, documentation: typing.Optional[DocumentationStyle] = None):
        """
        Parameters:
            documentation: A :class:`DocumentationStyle` enumerator indicating the
                           documentation style. See :ref:`enumecg-documentation-generation`.
        """
        self._documentation = documentation.value if documentation else None
        self._enum_definitions_template = self._JINJA_ENV.get_template(
            "enum_definitions.hh.in"
        )

    def generate_enum_definitions(self, enum, **options):
        """Generate the C++ definitions needed for an enhanced enum

        Parameters:
            enum: The enum definition
            options: The options passed to :func:`definitions.make_definition()`.

        Returns:
            The generated code

        Raises:
            :exc:`exceptions.Error`: If the code generation fails due
              to an invalid enum definition.
        """
        return self._enum_definitions_template.render(
            d=definitions.make_definition(enum, **options),
            documentation=self._documentation,
        )
