"""
EnumECG package
...............

The top level module provides the high level code generation API for
the Enhanced Enum library.
"""

__version__ = "0.3"
__author__ = "Jaakko Moisio"

import typing

from . import definitions, generators


def generator(
    *, documentation: typing.Union[generators.DocumentationStyle, str, None] = None
) -> generators.CodeGenerator:
    """Create code generator for an enhanced enum type

    Creates an instance of :class:`generators.CodeGenerator`.

    Parameters:
        documentation: A string or an enumerator indicating the documentation
                       style. See :ref:`enumecg-documentation-generation`.

    Returns:
        The :class:`generators.CodeGenerator` instance.
    """
    if documentation is not None:
        documentation = generators.DocumentationStyle(documentation)
    return generators.CodeGenerator(documentation=documentation)


def generate(
    enum,
    *,
    documentation: typing.Union[generators.DocumentationStyle, str, None] = None,
    primary_type: typing.Union[definitions.PrimaryType, str, None] = None,
    value_type: typing.Optional[str] = None
) -> str:
    """Generate code for an enhanced enum

    This function is a shorthand for creating and invoking a code
    generator in one call.

    The enum definition may be:

    - An instance of :class:`definitions.EnumDefinition`

    - A :class:`dict` object containing the enum definition. The
      required and optional keys are discussed in
      :ref:`enumecg-definition-from-dict`.

    - A native Python :class:`enum.Enum` class. The typename is
      derived from the name of the enum class, and the enumerator
      definitions are derived from its members.

    The exact way that the ``enum`` parameter is converted to an enum
    definition in the C++ code is covered in
    :ref:`enumecg-code-generation`.

    Parameters:
        enum: The enum definition
        documentation: A string or an enumerator indicating the documentation
                       style. See :ref:`enumecg-documentation-generation`.
        primary_type: A string or an enumerator indicating the
                      primary type. See :ref:`enumecg-primary-enum`.
        value_type: See :ref:`enumerator-value-type`.

    Returns:
        The enhanced enum definition created from the ``enum`` description.

    """
    if primary_type is not None:
        primary_type = definitions.PrimaryType(primary_type)
    return str(
        generator(documentation=documentation).generate_enum_definitions(
            enum, primary_type=primary_type, value_type=value_type
        )
    )
