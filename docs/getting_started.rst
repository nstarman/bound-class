.. _boundclass-getting-started:

***************
Getting Started
***************

Welcome to the ``bound-class`` documentation!

For practical reasons, this documentation generally assumes that you are
familiar with the Python programming language. If you need a refresher on Python
programming, we recommend starting with the `official Python tutorial
<https://docs.python.org/3/tutorial/>`_, but many other good resources are
available on the internet.

On this introductory page, we will demonstrate a few common use cases for
``bound-class`` and give an overview of the package functionality.


What does 'bound' mean?
=======================

Methods on classes are unbound:

.. code-block:: python

    >>> class Example:
    ...     def method(self):
    ...         pass
    >>> Example.method
    <function Example.method at ...>

When the class is instantiated the method becomes bound:

.. code-block:: python

    >>> ex = Example()
    >>> ex.method
    <bound method Example.method of <__main__.Example object at ...>>

|BoundClass| allows this to be extended this so that a class can be ``bound`` to
another class. Remember that |BoundClass| is a baseclass, so the specific
implementation is determined by which subclass is used. As a quick example:

.. code-block:: python

    >>> from bound_class.descriptors import InstanceDescriptor
    >>> class Example2:
    ...     attribute = InstanceDescriptor()
    >>> ex2 = Example2()
    >>> ex2.attribute
    InstanceDescriptor(store_in='__dict__')
    >>> ex2.attribute.__self__ is ex2
    True


Making your first bound class
=============================

Documentation coming soon. This project is intended to be the base of a set of packages, to which this one will refer.


What else can ``bound-class`` do?
=================================

This page is meant to demonstrate a few initial things you may want to do with
``bound-class``. There is much more functionality that you can discover either
through the :ref:`tutorials <boundclass-tutorials>` or by perusing the
:ref:`user guide <boundclass-user-guide>`. Some other commonly-used
functionality includes:

.. TODO! when add descriptors

* Coming soon!


Where to go from here
=====================

The two places to learn more are the tutorials and the user guide:

* The :ref:`boundclass-tutorials` are narrative demonstrations of functionality
  that walk through simplified, real-world use cases for the tools available in
  ``bound-class``.
* The :ref:`boundclass-user-guide` contains more exhaustive descriptions of all
  of the functions and classes available in ``bound-class``, and should be
  treated more like reference material.
