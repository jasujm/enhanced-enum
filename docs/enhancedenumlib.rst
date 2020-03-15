.. _enhancedenum-library:

Enhanced Enum -- The guide
==========================

.. _enhancedenum-motivation:

Motivation
----------

The native C++ enums are a good choice for types labeling choices from
a limited set. They are

- Type safe: It's hard for a programmer to accidentally create an enum
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
``EnumECG`` library that can be used to generate the necessary C++
code from Python enum definitions. See :ref:`enumecg-library` for more
details.

The library currently targets C++17, but will include C++20 goodies
later.

.. _enhancedenum-creating:

Creating the enumeration
------------------------

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

As discussed if :ref:`enhancedenum-motivation`, some boilerplate is
needed to define an enhanced enum type. The library tries to keep the
generated boilerplate minimal, clean, and part of API. This means that
the user of the generated enum type, and not just the library
machinery, is free to use the types, constants and functions that
the. Because the generated definitions are also public API of the
type, backward incompatible changes are not made lightly.

Let's create ``Status`` type that enumerates the different states of
an imaginary process. The boilerplate can be generated with the
EnumECG library, described in detail in :ref:`enumecg-library`.

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

The generated enum definitions may appear in a namespace scope (global
or any other namespace) in the user's C++ files. In addition the file
must include the ``enhanced_enum.hh`` header file.

Overview of the generated definitions
.....................................

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
the ``namespace Statuses``, defined at line 21. This *associate
namespace* is not necessary for the library itself, but the
application may use the constants from this namespace.

Controlling the output
......................

The above command generated names of the types, enumerators and the
helper namespace from the names in the Python definition. The defaults
may not be what you want. Especially you might want to control if the
label enum or the enhanced enum is the *primary type* and simply
called ``Status``.

For the details about controlling output see
:ref:`enumecg-code-generation`.

Integrating to a project
........................

The Enhanced Enum library does not provide integration between the
``EnumECG`` and the development environment out of box. It is
recommended to use template based code generator tooling to include
the bits generated by ``EnumECG`` to your C++ header files.

Here is an example using the awesome `cog
<https://github.com/nedbat/cog>`_ library. Write a header file like
the following:

.. code-block:: c++

   #include <enhanced_enum/enhanced_enum.hh>

   #include <string_view>

   namespace myapp {

   /*[[[cog
   import cog
   import enumecg
   import enum
   class Status(enum.Enum):
       INITIALIZING = "initializing"
       WAITING_FOR_INPUT = "waitingForInput"
       BUSY = "busy"
   cog.out(enumecg.generate(Status))
   ]]]*/
   //[[[end]]]

   }

Then, assuming you have ``cog`` installed in your environment, just
invoke the command line utility and the enum definitions will appear
where the template is located in the source file:

.. code-block:: console

   $ cog -r status.hh

``cog`` supports both in-place code generation and writing the output
to a file. There are advantages and disadvantages in both
approaches. In-place code generation is IDE friendly and allows users
that don't have ``cog`` or ``EnumECG`` installed still compile your
code, but care must be taken that the definitions are not changed
manually. See the ``cog`` documentation for more details.

Using the enumeration
---------------------

This section introduces how to use an enhanced enum definition in your
code, and the basic properties of an enhanced enum type. It is assumed
that the code is the one generated in the previous section
(:ref:`enhancedenum-creating`).

- Label type called ``StatusLabel``

- Enhanced enum type called ``EnhancedStatus``

- Function ``enhance()`` that can be used to promote a label enum into
  enhanced enum

- Associate namespace ``Statuses`` containing enums and their values
  as constants

Basic properties
................

Enhanced enums, like the build-in C++ enums, are `regular
<https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c11-make-concrete-types-regular>`_.
They can be constructed and assigned from enhanced and label enums:

.. code-block:: c++

   auto status = enhance(StatusLabel::INITIALIZING);
   assert( status.get() == StatusLabel::INITIALIZING );
   status = StatusLabel::BUSY;
   assert( status.get() == StatusLabel::BUSY );

They have all comparison operators defined, and working transparently
with both enhanced and label enum operands. Both the enhanced enums
and label enums are totally ordered by the order the labels are
declared in the code.

.. code-block:: c++

   static_assert( Statuses::INITIALIZING == StatusLabel::INITIALIZING );
   static_assert( StatusLabel::INITIALIZING < Statuses::BUSY );
   // etc...

Enumerator values and labels
............................

Enhanced enumerators have values. They can be accessed using the
:cpp:func:`value()` function

.. code-block:: c++

   static_assert( Statuses::INITIALIZING.value() == "initializing" );

Enumerators can be constructed from value using the static
:cpp:func:`from()` method:

.. code-block:: c++

   static_assert( EnhancedStatus::from("initializing") == Statuses::INITIALIZING );

The underlying label enum can be accessed either with the
:cpp:func:`get()` method or explicit cast. Note that although label
enum is implicitly convertible to enhanced enum, the converse is
deliberately explicit.


.. code-block:: c++

   static_assert( Statuses::INITIALIZING.get() == StatusLabel::INITIALIZING )
   static_assert( static_cast<StatusLabel>(Statuses::INITIALIZING) == StatusLabel::INITIALIZING );

Enumerator ranges
.................

The number of enumerators in an enhanced enum type can be queries by
using the :cpp:func:`size()` and :cpp:func:`ssize()`, for unsigned and
signed sizes, respectively.

A range containing all enumerators of a given enum type can be
constructed with the static :cpp:func:`all()` method:

.. code-block:: c++

   for (const auto status : EnhancedStatus::all()) {
       // use status
   }

The returned range can be used in compile time and has all the
enumerators in the same order as they are declared in the type.

For interfaces consuming iterator pairs, using :cpp:func:`begin()` and
:cpp:func:`end()` may be more convenient:

.. code-block:: c++

   std::for_each(
       EnhancedStatus::begin(), EnhancedStatus::end(),
       [](const auto status) { /* use status */ });

.. note::

   The user should not assume an underlying type returned by the
   :cpp:func:`all()`, :cpp:func:`begin()` and :cpp:func:`end()`
   functions, except that the iterators supports random access.

   The iterators model the C++17 random access iterator concepts. The
   range returned by :cpp:func:`all()` *doesn't* model STL
   container. The intention is to remain forward-compatible with the
   view concepts from the `Ranges TS
   <http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0896r3.pdf>`_. Unlike
   STL containers, views don't define type aliases etc. The other
   functions in the view interface should be implemented later.

Library reference
-----------------

.. doxygennamespace:: enhanced_enum
   :members:
