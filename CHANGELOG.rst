Unreleased
----------

Added
  - Pylint (test target, configurations)

Fixed
  - Several pylint errors

Version 0.4
-----------

Date
  2020-05-13

Added
  - Command line interface

Changed
  - Migrate EnumECG build system to flit
  - Migrate EnumECG unit tests to pytest
  - Use tox to manage EnumECG unit tests
  - More explicit call signatures in Python API (more type
    annotations, less catch-all keyword arguments)
  - Change the format of ``dict`` representation of enumerators to
    have a more explicit ordering of members
  - Improvements to the documentation
  - Use Python enums to enumerate the possible primary types and documentation
    styles in the EnumECG library

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
