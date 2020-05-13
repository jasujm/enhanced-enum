Building and installing from sources
====================================

The project uses CMake as its build system. To build everything:

.. code-block:: console

   $ cd /path/to/build
   $ cmake                                      \
   >   -D ENHANCEDENUM_BUILD_DOCS:BOOL=ON       \
   >   -D ENHANCEDENUM_BUILD_PYTHON:BOOL=ON     \
   >   -D ENHANCEDENUM_BUILD_TESTS:BOOL=ON      \
   >   /path/to/repository

The Enhanced Enum library specific CMake variables are:

- ``ENHANCEDENUM_BUILD_DOCS``: Build ``sphinx`` docs

- ``ENHANCEDENUM_BUILD_PYTHON``: Build the :mod:`enumecg` package
  (see caveats below)

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

Docs, EnumECG and unit tests *all* require Python when being
built. This would be a typical way to bootstrap a virtual environment,
and build and test the C++ code and documentations with CMake:

.. code-block:: console

   $ mkdir /path/to/build
   $ cd /path/to/build
   $ source /path/to/venv/bin/activate
   $ pip install -r requirements.txt -r requirements-dev.txt
   $ cmake                                      \
   >   -D ENHANCEDENUM_BUILD_DOCS:BOOL=ON       \
   >   -D ENHANCEDENUM_BUILD_TESTS:BOOL=ON      \
   >   /path/to/repository
   $ make && make test && make install

Installing EnumECG from sources
-------------------------------

EnumECG uses `Flit <https://flit.readthedocs.io/en/latest/>`_ for
building. By default CMake will not build the EnumECG library. If you
want to install :mod:`enumecg` from sources using CMake, you can do
that:

.. code-block:: console

   $ cd /path/to/build
   $ cmake -D ENHANCEDENUM_BUILD_PYTHON:BOOL=ON /path/to/repository
   $ make && make install

Installing the package in this way is limited. Essentially it's
equivalent of running the following in the ``python/`` directory:

.. code-block:: console

   $ flit build
   $ flit install

Note that the build will happen in-source.
