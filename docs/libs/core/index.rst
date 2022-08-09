.. _core:

*************************************
The Core Package (`bound_class.core`)
*************************************

Introduction
============

``...``

.. toctree::
    :maxdepth: 1

    libs/core/base
    libs/core/descriptors


Weak References
===============

Behind the scenes |BoundClass| uses :mod:`weakref` to ensure that classes do not
unexpectedly keep each other from being :external+python:ref:`garbage
collected`. For details of this implementation, see |BoundClass|, and in
particular, :class:`~bound_class.core.base.BoundClassRef`.

.. _core-api:

API
===

.. automodapi:: bound_class.core
