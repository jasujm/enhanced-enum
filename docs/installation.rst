Building and installing from sources
====================================

The project uses CMake as its build system. To build everything:

.. code-block:: console

   $ cd /path/to/build/dir
   $ cmake                                      \
   >   -D ENHANCEDENUM_BUILD_DOCS:BOOL=ON       \
   >   -D ENHANCEDENUM_BUILD_PYTHON:BOOL=ON     \
   >   -D ENHANCEDENUM_BUILD_TESTS:BOOL=ON      \
   >   /path/to/repository

The Enhanced Enum library specific CMake variables are:

- ``ENHANCEDENUM_BUILD_DOCS``: Build ``sphinx`` docs

- ``ENHANCEDENUM_BUILD_PYTHON``: Build and install the :mod:`enumecg`
  package

  Installing the package in this way is limited. Essentially it's
  equivalent of running the following in the ``python/`` directory:

  .. code-block:: console

     $ python setup.py build
     $ python setup.py install

  ...but does some extra bootstrapping to build out-of-source. The
  package is thus installed in the current site-packages. You can also
  do normal in-source build for greater control.

- ``ENHANCEDENUM_BUILD_TESTS``: Build tests for the C++ and/or Python
  packages

The C++ headers under the ``cxx/include/`` directory will always be
installed, along with CMake config files needed to find the package in
other projects. When installed this way, the project is exposed as
imported target ``EnhancedEnum::EnhancedEnum``:

.. code-block:: cmake

   find_package(EnhancedEnum)
   target_link_libraries(my-target EnhancedEnum::EnhancedEnum)

Docs, EnumECG and unit tests *all* require Python when being built. A
build environment can be bootstrapped using the ``Pipfile`` under
the ``python/`` directory:

.. code-block:: console

  $ cd /path/to/repository/python
  $ pipenv install --dev
  $ pipenv shell
