Unreleased
----------

Added
  - Command line interface

Changed
  - Migrate Python unit tests to pytest
  - Introduce tox to manage Python unit tests
  - More explicit call signatures in Python API (more type
    annotations, less catch-all keyword arguments)
  - Change the format of ``dict`` representation of enumerators to
    have more explicit ordering of members
  - Improvements to the documentation
  - Use Python enums to enumerate the possible primary types in EnumECG

Version 0.3
-----------

Date
   2020-03-15

Added
  - Docstring from the Python enum definition is now included in the
    generated Doxygen comments
  - Documentation about integrating EnumECG to a project

Changed
  - Restructured documentation slightly

Version 0.2
-----------

Date
   2020-01-10

Added
   - Add :cpp:func:`enhanced_enum::enum_base::ssize()`
   - Add :cpp:func:`enhanced_enum::enum_base::begin()` and
     :cpp:func:`enhanced_enum::enum_base::end()`
   - Add support for generating Doxygen comments

Changed
   - Implement :cpp:func:`enhanced_enum::enum_base::all()` in terms
     of custom range type (not array)

Fixed
   - Add include guards to the C++ headers

Version 0.1
-----------

Date
   2019-12-07

Initial revision
