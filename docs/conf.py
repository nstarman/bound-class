# Load all of the global Astropy configuration
# STDLIB
import datetime
import pathlib
import sys
from importlib import import_module

# THIRD PARTY
import tomlkit

# Get configuration information from pyproject.toml
docs_root = pathlib.Path(__file__).parent.parent / "pyproject.toml"
with docs_root.open() as f:
    toml = tomlkit.load(f)
setup_cfg = dict(toml["project"])  # type: ignore


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
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# Don't show summaries of the members in each class along with the
# class' docstring
numpydoc_show_class_members = True

# Whether to create cross-references for the parameter types in the
# Parameters, Other Parameters, Returns and Yields sections of the docstring.
numpydoc_xref_param_type = True

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
.. |BoundClass| replace:: :class:`~bound_class.base.BoundClass`
"""

# intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

# Show / hide TODO blocks
todo_include_todos = True

# -- Project information ------------------------------------------------------

# This does not *have* to match the package name, but typically does
project = str(setup_cfg["name"])
author = ", ".join(d["name"] for d in setup_cfg["authors"])  # type: ignore
copyright = f"{datetime.datetime.now().year}, {author}"

import_module(project)
package = sys.modules[project]

# The short X.Y version.
version = package.__version__.split("-", 1)[0]
# The full version, including alpha/beta/rc tags.
release = package.__version__

# -- Options for HTML output ---------------------------------------------------

html_theme = "pydata_sphinx_theme"

# html_logo = '_static/<X>.png'

# html_theme_options = {
#     "logo_link": "index",
#     "icon_links": [
#         {
#             "name": "GitHub",
#             "url": "",
#             "icon": "fab fa-github-square",
#         },
#     ],
# }

# Custom sidebar templates, maps document names to template names.
html_sidebars = {"**": ["search-field.html", "sidebar-nav-bs.html"]}

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = ''

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = str(docs_root / '_static' / 'X.ico')

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = ''

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = f"{project} v{release}"

# Output file base name for HTML help builder.
htmlhelp_basename = project + "doc"

# Static files to copy after template files
html_static_path = ["_static"]
html_css_files = ["bound-class.css"]