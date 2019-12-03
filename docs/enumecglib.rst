.. _enumecg-library:

EnumECG -- The Python library
=============================

Overview
--------

EnumECG (almost acronym for Enhanced Enum Code Generator) is a Python
library accompanying the Enhanced Enum library. It is used to generate
C++ boilerplate for the enhanced enum types. Please see
:ref:`enhancedenum-library` for more information about the design of
the library.

There are multiple ways to map a Python object to the C++ enum
type. The following code examples all produce the same C++
definitions. For further discussion see :ref:`enhancedenum-overview`.

.. literalinclude:: examples/status.hh
   :language: c++
   :linenos:

Creating C++ enum from Python enum
..................................

The most idiomatic way to create an enum definition in pure Python is
to give the generator a Python enum type.

.. doctest::

   >>> import enum
   >>> class Status(enum.Enum):
   ...     INITIALIZING = "initializing"
   ...     WAITING_FOR_INPUT = "waitingForInput"
   ...     BUSY = "busy"
   >>> import enumecg
   >>> enumecg.generate(Status)
   '...'

The mapping between the name of the enum type, and the names and
values of the enum members are obvious in this style.

Creating C++ enum from a dict
.............................

This is a convenient method if the enum definitions are loaded from a
file using general purpose serialization format like JSON or YAML.

.. doctest::

   >>> status = {
   ...     "typename": "Status",
   ...     "members": {
   ...         "INITIALIZING": "initializing",
   ...         "WAITING_FOR_INPUT": "waitingForInput",
   ...         "BUSY": "busy",
   ...     }
   ... }
   >>> import enumecg
   >>> enumecg.generate(status)
   '...'

The supported keys are:

- ``typename``: The enum typename.

- ``members``: Mapping between enumerator names and values. The
  enumerators appear in the same order as they appear in the
  definition. Note that in CPython ``dict`` type is ordered by
  default, but to be more explicit, :class:`collections.OrderedDict` might
  be preferred.

Native representation
.....................

The code generator uses :class:`enumecg.definitions.EnumDefinition` as
its datatype holding the native representation of enum
definition. They can be used with the generator directly if a very
fine control of the generated code is required.
%
.. doctest::

   >>> from enumecg.definitions import EnumDefinition, EnumMemberDefinition
   >>> status = EnumDefinition(
   ...     label_enum_typename="StatusLabel",
   ...     enhanced_enum_typename="EnhancedStatus",
   ...     value_type_typename="std::string_view",
   ...     members=[
   ...         EnumMemberDefinition(
   ...             enumerator_name="INITIALIZING",
   ...             enumerator_value_constant_name="INITIALIZING_VALUE",
   ...             enumerator_value_initializers="initializing",
   ...         ),
   ...         EnumMemberDefinition(
   ...             enumerator_name="WAITING_FOR_INPUT",
   ...             enumerator_value_constant_name="WAITING_FOR_INPUT_VALUE",
   ...             enumerator_value_initializers="waitingForInput",
   ...         ),
   ...         EnumMemberDefinition(
   ...             enumerator_name="BUSY",
   ...             enumerator_value_constant_name="BUSY_VALUE",
   ...             enumerator_value_initializers="busy",
   ...         ),
   ...     ],
   ...     associate_namespace_name="Statuses",
   ... )
   >>> import enumecg
   >>> enumecg.generate(status)
   '...'

Note that in this style all names used in the C++ template are
explicit fields of the definition object.

.. _enumecg-code-generation:

Enum definitions in detail
--------------------------

Various aspects of code generation can be controlled by passing
keyword arguments to the code generator functions.

Please note that when generating the code directly from
:class:`enumecg.definitions.EnumDefinition` object, the options have
no effect because the :class:`EnumDefinition` object is assumed to contain
all information required to generate the code already.

.. _enumecg-identifiers:

Identifiers
...........

In the example above the type names follow CamelCase while the
enumerator names are UPPER_SNAKE_CASE. The code generator tries to
deduce the case style for the different kinds of identifiers and uses
it to format the names of others.

- The case style of the enum type name is used to format the names of
  the C++ enums and the associate namespace.

- The case style of the enumerator names are used to format the names
  of the the C++ enumerators and value constants.

The following case styles are recognized:

- Snake case with all lowercase letters: ``lower_snake_case``

- Snake case with all uppercase letters: ``UPPER_SNAKE_CASE``

- Camel case with every word capitalized: ``CamelCase``

- Camel case with the first word starting with a lowercase letter:
  ``mixedCase``. A single lower case word is recognized as snake_case
  instead of mixedCase.

Only ASCII alphanumeric characters are supported. Numbers may appear
in any other position except at the start of a subword. All
enumerators must follow the same case style. The following leads to an
error:

.. doctest::

   >>> class BadExample(enum.Enum):
   ...     mixedCaseValue = "value1"
   ...     snake_case_value = "value2"
   >>> enumecg.generate(BadExample)
   Traceback (most recent call last):
     ...
   ValueError: Could not find common case

Primary enum type
.................

By default the label enum for ``Status`` has the name ``StatusLabel``
and the enhanced enum has the name ``EnhancedStatus``. Almost
certainly the user will want to call one of those types simply
``Status`` depending on the view whether the label enum or the
enhanced enum is considered the *primary enum type*.

To make the label enum the primary type, set ``primary_type`` option
to "label" when invoking the code generation:

.. doctest::

   >>> enumecg.generate(Status, primary_type="label")
   '...enum class Status {...'

Similarly, passing option "enhanced" will make the enhanced enum the
primary type:

.. doctest::

   >>> enumecg.generate(Status, primary_type="enhanced")
   '...struct Status : ::enhanced_enum::enum_base<...'

.. _enumecg-enumerator-values:

Enumerator types and values
...........................

Python has dynamic typing, but in C++ all enumerators within an enum
type must have the same type known in advance. There are two ways to
define the enumerator type:

- Have the code generator deduce a C++ type automatically from the
  Python enumerator values

- Specify it manually

Enumerator type deduction
`````````````````````````

In the examples above the enumerator values are strings, but the
enumerator type can be any type that can be constexpr constructible
from arbitrarily nested initializer lists of string, integer, float
and bool literals.

For example:

.. doctest::

   >>> class MathConstants(enum.Enum):
   ...     PI = 3.14
   ...     NEPER = 2.71
   >>> enumecg.generate(MathConstants)
   '...enum_base<..., double>...'

Or even:

   >>> class NestedExample(enum.Enum):
   ...     EXPLICIT_VALUE = 0, 1.2, ("string", True)
   ...     DEFAULT_VALUE = ()
   >>> enumecg.generate(NestedExample)
   '...enum_base<..., std::tuple<long, double, std::tuple<std::string_view, bool>>>...'

The Python types are mapped to C++ types in the following way:

- Integral types are mapped to ``long``

- Other real numbers (like floats) are mapped to ``double``

- ``str`` and ``bytes`` are mapped to ``std::string_view``

- ``bool`` is mapped to ``bool``

- Sequences are mapped to ``std::tuple`` whose template arguments are
  (recursively) the mapped types of the elements of the sequence.

All enumerator values must have a compatible types for the type
deduction to work. When deducing the type from multiple sequences, the
longest sequence determines the template arguments of the resulting
``std::tuple``, and all prefixes of values must have types compatible
with the longest sequence. For example the following works:

.. doctest::

   >>> class GoodExample(enum.Enum):
   ...     VALUE1 = 1, 2
   ...     VALUE2 = 3,
   >>> enumecg.generate(GoodExample)
   '...enum_base<..., std::tuple<long, long>>...'

But the following doesn't:

.. doctest::

   >>> class BadExample(enum.Enum):
   ...     VALUE1 = 1, 2
   ...     VALUE2 = "string",
   >>> enumecg.generate(BadExample)
   Traceback (most recent call last):
     ...
   ValueError: Could not deduce compatible type

Specifying enumerator type manually
```````````````````````````````````

WIP

C++ enumerator value initializers
`````````````````````````````````

WIP

Overriding arbitrary fields in the definition
.............................................

It is also possible to start with an
:class:`enumecg.definitions.EnumDefinition` object generated from any
of the above representations, and modifying it before actually using
it to generate the C++
code. :func:`enumecg.definitions.make_definition()` can first be used
to get an :class:`EnumDefinition` object, which can further be used
with the :func:`enumecg.generate()` function.

Note that, although the :func:`generate()` function will ignore any
options when an :class:`EnumDefinition` object is used as argument,
:func:`make_definition()` accepts all the same options, that will be
applied when creating the enum definition.

.. _enumecg-high-level-api:

High level API
--------------

Most of the time the high level API is all you need to get started
with code generation.

.. automodule:: enumecg
   :members:

Module reference
----------------

The package contains lower level modules. These are used to implement
the :ref:`enumecg-high-level-api`, but can also be utilized directly
to give greater control over the generated code.

.. automodule:: enumecg.definitions
   :members:

.. automodule:: enumecg.generators
   :members:

.. automodule:: enumecg.utils
   :members:
