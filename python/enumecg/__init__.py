"""
EnumECG package
...............

The top level module provides the high level code generation API for the
Enhanced Enum library.
"""

from . import definitions
from . import generators


def generator(enum) -> generators.CodeGenerator:
    """Create code generator for an enhanced enum type

    Creates an instance of :class:`generators.CodeGenerator` created from the
    given enum description. Unlike using the constructor directly that always
    excepts its argument to be :class:`definitions.EnumDefinition`. the ``enum``
    parameter can be:

    - An instance of :class:`definitions.EnumDefinition`

    - A ``dict`` containing "typename" and "members" keys, "members" itself
      being a ``dict`` containing enumerator name to value mapping.

    - A native Python :class:`enum.Enum` class. The typename is derived from the
      name of the enum class, and the enumerator definitions are derived from
      its members.

    Parameters:
        enum: The description of the enum

    Returns:
        The :class:`generators.CodeGenerator` instance created from the ``enum``
        description.

    """
    return generators.CodeGenerator(definitions.make_definition(enum))


def generate(enum) -> str:
    """Generate code for an enhanced enum

    This function is a shorthand for creating and invoking a code generator in
    one call. It first calls :func:`generator()` using ``enum`` as the argument,
    and immediately returns the generated code.

    Parameters:
       enum: The description of the enum

    Returns:
       The enhanced enum definition created from the ``enum`` description.
    """
    return str(generator(enum).generate_enum_definitions())
