.. include:: references.txt

.. _boundclass-install:

************
Installation
************

With ``pip`` (recommended)
==========================

To install the latest stable version using ``pip``, use

.. code-block:: bash

    python -m pip install bound_class.core

This is the recommended way to install ``bound-class``.

To install the development version

.. code-block:: bash

    python -m pip install git+https://github.com/nstarman/bound-class


With ``conda``
==============

Conda is not yet supported.


From Source: Cloning, Building, Installing
==========================================

The latest development version of bound-class can be cloned from `GitHub
<https://github.com/>`_ using ``git``

.. code-block:: bash

    git clone git://github.com/nstarman/bound-class.git

To build and install the project (from the root of the source tree, e.g., inside
the cloned ``bound-class`` directory)

.. code-block:: bash

    python -m pip install [-e] .


Python Dependencies
===================

This packages has the following dependencies:

* `Python`_ >= 3.8

Explicit version requirements are specified in the project `pyproject.toml
<https://github.com/nstarman/bound-class/blob/main/pyproject.toml>`_. ``pip``
and ``conda`` should install and enforce these versions automatically.
