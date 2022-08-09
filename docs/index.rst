.. module:: bound_class

***********
Bound-Class
***********

``bound-class`` provides tools for creating classes that are bound to another
class' instances. In `Python`_, methods on a class are just functions, until an
instance of the class is made and those 'unbound' methods are bound.
``bound-class`` offers similar functionality for classes.

TL;DR this means you can bundle related functionality and not overburden the
namespace -- e.g. all plot methods can be grouped.

.. code-block:: python

   from bound_class.core.descriptors import InstanceDescriptor

   class BoundPlotter(InstanceDescriptor):
       def histogram(self, ...):
           ...


   @dataclass
   class DataClass:
       data: DataFrame

       plot = BoundPlotter()  # bound to instances of DataClass


   mydata = DataClass(...)

   # plot can now contain many different plotting functions.
   mydata.plot.histogram(...)


This package is being actively developed in `a public repository on GitHub
<https://github.com/nstarman/bound-class>`_, and we are always looking for new
contributors! No contribution is too small, so if you have any trouble with this
code, find a typo, or have requests for new content (tutorials or features),
please `open an issue on GitHub
<https://github.com/nstarman/bound-class/issues>`_.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   install
   getting_started
   tutorials
   user_guide
   contributing


Contributors
============

.. include:: ../AUTHORS.rst
