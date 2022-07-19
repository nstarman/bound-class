.. module:: bound-class

***********
Bound-Class
***********

``bound-class`` provides tools for creating classes that are bound to the instance of another class: like bound methods but as customizable as a class; like nested classes but better.
What does this mean? It means it's not too hard to do

.. code-block:: python

   class BoundPlotter(...):
      def histogram(self):
         ...


   @dataclass
   class DataClass:
      data: DataFrame

      plot = BoundPlotter()  # knows about DataClass


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
