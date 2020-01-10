"""
EnumECG package
...............

The top level module provides the high level code generation API for the
Enhanced Enum library.
"""

__version__ = "0.2"
__author__ = "Jaakko Moisio"

from . import generators


def generator(**options) -> generators.CodeGenerator:
    """Create code generator for an enhanced enum type

    Creates an instance of :class:`generators.CodeGenerator` created
    with the given ``options``.

    Parameters:
        options: The code generation options

    Returns:
        The :class:`generators.CodeGenerator` instance.

    """
    return generators.CodeGenerator(**options)


def generate(enum, **options) -> str:
    """Generate code for an enhanced enum

    This function is a shorthand for creating and invoking a code
    generator in one call. It first calls :func:`generator()` with
    ``options`` as the argument, followed by code
    generation. ``options`` may contain `both` options targeted for
    initializing the code generator and the options targeted for
    generating the enum definitions. The two kinds of options do not
    share names so there is no risk of ambiguity.

    The enum definition may be:

    - An instance of :class:`definitions.EnumDefinition`

    - A ``dict`` containing "typename" and "members" keys, "members"
      itself being a ``dict`` containing enumerator name to value
      mapping.

    - A native Python :class:`enum.Enum` class. The typename is
      derived from the name of the enum class, and the enumerator
      definitions are derived from its members.

    The exact way that the ``enum`` parameter is converted to an enum
    definition in the C++ code is covered in
    :ref:`enumecg-code-generation`.

    Parameters:
       enum: The description of the enum
       options: The code generation and enum definition generation options

    Returns:
       The enhanced enum definition created from the ``enum`` description.

    """
    return str(generator(**options).generate_enum_definitions(enum, **options))
