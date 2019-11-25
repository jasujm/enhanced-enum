Enhanced Enum library
=====================

Motivation
----------

The native C++ enums are a good choice for types labeling choices from
a limited set. They are

- Type safe: It's hard for a programmer to deliberately create an enum
  object holding a value not in the predetermined set.

- Lightweight: Under the hood enum is just an integer

They also have restrictions which sometimes makes them tedious to work
with:

- Enum is just an integer. The concept an enum is modeling may well
  have a more natural representation, but with a native C++ enum that
  mapping is not implemented in the enum type itself.

- They lack reflection support. Even iterating over (or should I say
  *enumerating*) the members of an enum type requires writing
  boilerplate and duplicating enumerator definitions.

This library attempts to solve those problems by helping creating
*enhanced enum* types that are just as lightweight and type safe as
native enums, but support the convenient features users of higher
level languages have learned to expect from their enums.

The design goals are:

- **Standard compliant:** The library doesn't use compiler specific
  features to enable reflection capabilities.

- **IDE friendly:** The library doesn't use macros to generate the
  unavoidable boilerplate. The generated code is explicit and
  available for human and tool inspection.

- **Supporting modern C++ idioms:** The library is ``constexpr``
  correct, includes utilities for template programming and type
  checks, etc.

- **Zero-cost:** Ideally code manipulating enhanced enums should compile
  down to the same instructions as code manipulating native enums.

To give the enum types their capabilities without resorting to
compiler hacks, it's necessary to write some boilerplate accompanying
the enum definitions. To aid with that the project includes
:ref:`enumecg-library` that can be used to generate the necessary C++
code from Python enum definitions.

The library currently targets C++17, but will include C++20 goodies
later.

Overview of an enum definition
------------------------------

Generating boilerplate to support the enum definition is a necessary evil at
best. The library tries to keep the generated boilerplate minimal, clean, and
part of API. This means that the user of the generated enum type, and not just
the library machinery, is free to use the types, constants and functions that
the. Because the generated definitions are also public API of the type, backward
incompatible changes are not made lightly.

Let's take a closer look at the enumeration from :ref:`introduction`:

  >>> import enum
  >>> class Status(enum.Enum):
  ...     INITIALIZING = "initializing"
  ...     WAITING_FOR_INPUT = "waitingForInput"
  ...     BUSY = "busy"
  >>> import enumecg
  >>> enumecg.generate(Status)

This will generate the following C++ code:

.. code-block:: c++

   // TODO: Autogenerate definition from the above Python


Library reference
-----------------

.. doxygennamespace:: enhanced_enum
  :members:
