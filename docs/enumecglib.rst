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
   ...             enumerator_value="initializing",
   ...         ),
   ...         EnumMemberDefinition(
   ...             enumerator_name="WAITING_FOR_INPUT",
   ...             enumerator_value_constant_name="WAITING_FOR_INPUT_VALUE",
   ...             enumerator_value="waitingForInput",
   ...         ),
   ...         EnumMemberDefinition(
   ...             enumerator_name="BUSY",
   ...             enumerator_value_constant_name="BUSY_VALUE",
   ...             enumerator_value="busy",
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

Code generation options
-----------------------

Various aspects of code generation can be controlled by passing
keyword arguments to the code generator functions.

Please note that when generating the code directly from
:class:`enumecg.definitions.EnumDefinition` object, the options have
no effect because the :class:`EnumDefinition` object is assumed to contain
all information required to generate the code already.

Type names
..........

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

Enumerator values
.................

In the examples above the enumerator values are strings, but they can
be an arbitrary combination of C++ string, scalar types, arrays and
tuples, or even user defined types consisting thereof. The only
restriction is that the enumerator values must be constructible at
compile time.

.. warning::

   WIP: Enumerator values are currently hardcoded as
   ``std::string_view``. Working to make it inferred from the Python
   values.

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
