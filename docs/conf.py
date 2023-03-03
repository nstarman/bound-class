"""Sphinx configuration file for the bound_class package."""

import pathlib
import sys
from importlib import import_module

# THIRD PARTY
import tomli


def get_authors(*pkg_names: str) -> set[str]:
    """Get author information from ``pyproject.toml``s.

    Returns
    -------
    set[str]
        The authors.
    """
    authors: set[str] = set()
    libs = pathlib.Path(__file__).parent.parent / "libs"

    for pkg_name in pkg_names:
        cfg = libs / pkg_name / "pyproject.toml"
        with cfg.open() as f:
            toml = tomli.load(f)
        project = dict(toml["project"])
        authors.update({d["name"] for d in project["authors"]})

    return authors


# -- General configuration ----------------------------------------------------

# By default, highlight as Python 3.
highlight_language = "python3"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "**.ipynb_checkpoints"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ".rst"

# Sphinx extensions
extensions = [
    "sphinx_automodapi.automodapi",
    "pytest_doctestplus.sphinx.doctestplus",
]

autosummary_generate = True

automodapi_toctreedirnm = "api"

# The reST default role (used for this markup: `text`) to use for all
# documents. Set to the "smart" one.
default_role = "obj"

# Class documentation should contain *both* the class docstring and
# the __init__ docstring
autoclass_content = "both"

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.
rst_epilog = """
.. |BoundClass| replace:: :class:`~bound_class.core.base.BoundClass`
"""

# intersphinx
intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3/",
        (None, "http://data.astropy.org/intersphinx/python3.inv"),
    ),
}

# Show / hide TODO blocks
todo_include_todos = True


# -- NumpyDoc Configuration ------------------------

# Don't show summaries of the members in each class along with the
# class' docstring
numpydoc_show_class_members = True

# Whether to create cross-references for the parameter types in the
# Parameters, Other Parameters, Returns and Yields sections of the docstring.
numpydoc_xref_param_type = True

# Words not to cross-reference. Most likely, these are common words used in
# parameter type descriptions that may be confused for classes of the same
# name. This can be overwritten or modified in packages and is provided here for
# convenience.
numpydoc_xref_ignore = {
    "or",
    "of",
    "thereof",
    "default",
    "optional",
    "keyword-only",
    "instance",
    "type",
    "class",
    "subclass",
    "method",
}

# Mappings to fully qualified paths (or correct ReST references) for the
# aliases/shortcuts used when specifying the types of parameters.
# Numpy provides some defaults
# https://github.com/numpy/numpydoc/blob/b352cd7635f2ea7748722f410a31f937d92545cc/numpydoc/xref.py#L62-L94
numpydoc_xref_aliases = {
    # Python terms
    "function": ":term:`python:function`",
    "iterator": ":term:`python:iterator`",
    "mapping": ":term:`python:mapping`",
}

# -- Project information ------------------------------------------------------

# This does not *have* to match the package name, but typically does
project = "bound_class"
author = ", ".join(
    get_authors(
        "core",
    ),
)
copyright = f"2022, {author}"  # noqa: A001

import_module(project)
package = sys.modules[project]

# The short X.Y version.
version = package.__version__.split("-", 1)[0]
# The full version, including alpha/beta/rc tags.
release = package.__version__


# -- Options for HTML output ---------------------------------------------------

html_theme = "pydata_sphinx_theme"


#     "icon_links": [
#         },
#     ],

# Custom sidebar templates, maps document names to template names.
html_sidebars = {"**": ["search-field.html", "sidebar-nav-bs.html"]}

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "bound_class.[X]"

# Output file base name for HTML help builder.
htmlhelp_basename = project + "doc"

# Static files to copy after template files
html_static_path = ["_static"]
html_css_files = ["bound-class.css"]
