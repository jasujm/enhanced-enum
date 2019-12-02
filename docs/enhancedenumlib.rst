.. _enhancedenum-library:

Enhanced Enum -- The C++ library
================================

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

.. _enhancedenum-overview:

Overview of an enum definition
------------------------------

.. warning::

   The generated definitions should not be edited, or the behavior of
   instantiating and using a class deriving from enum_base is
   undefined. The library makes assumptions about the types and
   functions used with the library. Those assumptions include but are
   not limited to:

   - The values of the label enumerators are zero-based integer
     sequence that can be used as indices in the ``values`` array.

   - The enhanced enum instantiates enum_base with correct template
     arguments, and has no non-static data members or non-empty
     bases.

Generating boilerplate to support the enum definition is a necessary evil at
best. The library tries to keep the generated boilerplate minimal, clean, and
part of API. This means that the user of the generated enum type, and not just
the library machinery, is free to use the types, constants and functions that
the. Because the generated definitions are also public API of the type, backward
incompatible changes are not made lightly.

Let's create ``Status`` type that enumerates the different states of
an imaginary process:

.. doctest::

   >>> import enum
   >>> class Status(enum.Enum):
   ...     INITIALIZING = "initializing"
   ...     WAITING_FOR_INPUT = "waitingForInput"
   ...     BUSY = "busy"
   >>> import enumecg
   >>> enumecg.generate(Status)
   '...'

The above command will generate the following C++ code:

.. literalinclude:: examples/status.hh
   :language: c++
   :linenos:

The code starts with definition of ``enum class StatusLabel`` at
line 1. This is the underlying *label enum* type. The `label
enumerators` be thought as a names for the enumerators in the enhanced
enum type.

The next block is the definition of ``struct EnhancedStatus`` at
line 7. This is the actual enhance enum type. It derives from
:cpp:class:`enum_base` implemented in the Enhanced Enum library
header. The base class has three template arguments:

1. ``EnhancedStatus`` to employ the curiously recurring template pattern.
2. ``StatusLabel``, the label enum type
3. ``std::string_view``, the value type of the enumerators. They are
   discussed in more detail in :ref:`enumecg-enumerator-values`.

The class also defines static data members mapping the enumerators to
their values.

The library needs a way to map a label enumerators to the
corresponding enhanced enumerators without knowing the name of the
enhanced enum type. That is done with the ``enhance()`` method,
defined at line 16. It needs to be defined in the same namespace as
``StatusLabel`` itself to support argument-dependent lookup. Because
the library needs to reserve an identifier in the user namespace,
there is a risk for name collision. The name ``enhance`` was chosen
because, although short, it is a verb not otherwise often used in
computer programming. Due to its shortness it makes the code using the
function cleaner.

Finally the enumerators and their values are defined as constants in
the ``namespace Statuses``, defined at line 21. This is not necessary
for the library itself, but defined for the application use.

Controlling output
..................

The above command generated names of the types, enumerators and the
helper namespace from the names in the Python definition. The defaults
may not be what you want. Especially you might want to control if the
label enum or the enhanced enum is the *primary type* and simply
called ``Status``.

For the details about controlling output see
:ref:`enumecg-code-generation`.

Using the generated enum in a project
-------------------------------------

The generated enum definitions may appear in a namespace scope (global
or any other namespace) in the user's C++ files. In addition the file
must include the ``enhanced_enum.hh`` header file, and any headers
needed to define the value type of the enumerator. Here is an example:


.. code-block:: c++

   #include <enhanced_enum/enhanced_enum.hh>

   #include <string_view>

   namespace myapp {

   // The above enum definitions appear here

   }

   static_assert(myapp::Statuses::INITIALIZING.value() == "initializing");

Library reference
-----------------

.. doxygennamespace:: enhanced_enum
  :members:
