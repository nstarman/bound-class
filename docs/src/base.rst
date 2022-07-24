.. _base:

******************************
The Base  (`bound_class.base`)
******************************

Introduction
============

``...``


Weak References
===============

Behind the scenes |BoundClass| uses :mod:`weakref` to ensure that classes do not
unexpectedly keep each other from being :external+python:ref:`garbage
collected`. For details of this implementation, see |BoundClass|, and in
particular, :class:`~bound_class.base.BoundClassRef`.

.. _base-api:

API
===

.. automodapi:: bound_class.base
