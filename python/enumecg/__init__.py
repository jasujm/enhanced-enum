"""
EnumECG package
...............

The top level module provides the high level code generation API for the
Enhanced Enum library.
"""

__version__ = "0.3"
__author__ = "Jaakko Moisio"

from . import generators
from .utils import call_with_supported_options


def generator(**options) -> generators.CodeGenerator:
    """Create code generator for an enhanced enum type

    Creates an instance of :class:`generators.CodeGenerator` created
    with the given ``options``.

    Parameters:
        options: The options to initialize the code generator. The unknown
                 options are silently ignored.

    Returns:
        The :class:`generators.CodeGenerator` instance.

    """
    return call_with_supported_options(generators.CodeGenerator, **options)


def generate(enum, **options) -> str:
    """Generate code for an enhanced enum

    This function is a shorthand for creating and invoking a code
    generator in one call. It first calls :func:`generator()` with
    ``options`` as the argument, followed by code
    generation.

    The enum definition may be:

    - An instance of :class:`definitions.EnumDefinition`

    - A ``dict`` object containing the enum definition. The required
      and optional keys are discussed in
      :ref:`enumecg-definition-from-dict`.

    - A native Python :class:`enum.Enum` class. The typename is
      derived from the name of the enum class, and the enumerator
      definitions are derived from its members.

    The exact way that the ``enum`` parameter is converted to an enum
    definition in the C++ code is covered in
    :ref:`enumecg-code-generation`.

    Parameters:
       enum: The enum definition
       options: The code generation and enum definition generation options. Please
                see :ref:`enumecg-code-generation` for the full list. The unknown
                options are silently ignored.

    Returns:
       The enhanced enum definition created from the ``enum`` description.

    """
    return str(generator(**options).generate_enum_definitions(enum, **options))
