Enhanced Enum is a library that gives C++ enums capabilities that they don't
normally have:

.. code-block:: c++

   struct StatusLabel {
       INITIALIZING,
       WAITING_FOR_INPUT,
       BUSY,
   };

   constexpr auto status = enhance(StatusLabel::INITIALIZING);

Their value is no longer restricted to integers:

.. code-block:: c++

   static_assert( status.value() == "initializing" );
   static_assert( status == Status::from("initializing") );

...all while taking remaining largely compatible with the fundamental enums:

.. code-block:: c++

   static_assert( sizeof(status) == sizeof(StatusLabel) );
   static_assert( status == StatusLabel::INITIALIZING );
   static_assert( status != StatusLabel::WAITING_FOR_INPUT );

Why yet another enum library for C++?
-------------------------------------

There are plethora of options available for application writers that
want similar capabilities than this library provides. Why write
another instead of picking one of them?

Short answer: Because it solved a problem for me, and I hope it will
solve similar problems for other people

Longer answer: There is a fundamental limitations to the capabilities
of native enums within the standard C++, and in order to cope with
them, enum library writers must choose from more or less
unsatisfactory options:

- Resort to compiler implementation details.  While this is a
  non-intrusive way to introduce reflection, it's not what I'm after.

- Use macros. By far the most common approach across the ecosystem is
  to use preprocessor macros to generate the type definitions. To me
  macros are just another form of code generation. The advantage is
  that this approach needs standard C++ compiler only. The drawback is
  the inflexibility of macro expansions.

Enhanced Enum utilizes a proper code generator to create the necessary
boilerplate for enum types. The generator is written in Python, and
unlocks all the power and nice syntax that Python provides. The
generated code is clean and IDE friendly. This approach enables the
enums created using the library to have arbitrary values, not just
strings derived from the enumerator names. The drawback is the need to
include another library in the build toolchain.

Getting started
---------------

The C++ library is header only. Just copy the contents of the
``cxx/include/`` directory in the repository to your include path. If
you prefer, you can create and install the CMake targets for the
library:

.. code-block:: console

   $ cmake /path/to/repository
   $ make && make install

In your project:

.. code-block:: cmake

   find_package(EnhancedEnum)
   target_link_libraries(my-target EnhancedEnum::EnhancedEnum)

The enum definitions are created with the EnumECG library written in
Python. It can be installed using ``pip``:

.. code-block:: console

   $ pip install EnumECG

The library and code generation API are documented in the user guide
hosted at `Read the Docs <https://enhanced-enum.readthedocs.io/>`_.

Contact
-------

The author of the library is Jaakko Moisio. For feedback and
suggestions, please contact jaakko@moisio.fi.
