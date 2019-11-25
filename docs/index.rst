Enhanced Enum -- first class enums in C++
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _introduction:

Introduction
============

Enhanced Enum is a library that gives C++ enums capabilities that they don't
normally have:

.. code-block:: c++

   struct Status {
       INITIALIZING,
       WAITING_FOR_INPUT,
       BUSY,
   };

   constexpr auto status = enhance(Status::INITIALIZING);

Their value is no longer restricted to integers:

.. code-block:: c++

   static_assert( status.value() == "initializing" );

...all while taking remaining largely compatible with the fundamental enums:

.. code-block:: c++

   static_assert( sizeof(status) == sizeof(Status) );
   static_assert( status == Status::INITIALIZING );
   static_assert( status != Status::WAITING_FOR_INPUT );

C++ enums with superpowers
==========================

The Enhanced Enum C++ library is a header-only library used to implement
enhanced enumeration types.

.. toctree::
   :maxdepth: 2

   enhancedenumlib

Generating enum definitions
---------------------------

The :mod:`enumecg` package that is used to generate the necessary boilerplate
for C++ enum definitions.

.. toctree::
   :maxdepth: 2

   enumecglib
