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

  ...but does some extra bootstrapping to build out-of-source.

- ``ENHANCEDENUM_BUILD_TESTS``: Build tests for the C++ and/or Python
  packages

The C++ headers under the ``cxx/include/`` directory will always be
installed, along with CMake config files needed to find the package in
other projects. When installed this way, the project is exposed as
imported target ``EnhancedEnum::EnhancedEnum``:

.. code-block:: cmake

   find_package(EnhancedEnum)
   target_link_libraries(my-target EnhancedEnum::EnhancedEnum)

Python environment
------------------

Docs, EnumECG and unit tests *all* require Python when being built. To
use the CMake targets, a suggested approach is to create a build
directory under the sources where the project ``Pipfile`` is
available.

.. code-block:: console

   $ mkdir /path/to/repository/build
   $ cd /path/to/repository/build
   $ pipenv install --dev
   $ pipenv run cmake                           \
   >   -D ENHANCEDENUM_BUILD_DOCS:BOOL=ON       \
   >   -D ENHANCEDENUM_BUILD_TESTS:BOOL=ON      \
   >   ..
   $ make && make test

However, ``make install`` target may not make much sense with this
workflow, as it will only install :mod:`enumecg` to the current
virtualenv. If want to install development version of the EnumECG
library via CMake, you should use an external virtualenv:

.. code-block:: console

   (venv) $ cd /path/to/build/dir
   (venv) $ cmake -D ENHANCEDENUM_BUILD_PYTHON:BOOL=ON /path/to/repository
   (venv) $ make && make install

It is of course possible to build and install EnumECG by invoking a
more typical in-source build.
