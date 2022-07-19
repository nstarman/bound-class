# see LICENSE.rst

"""Bound Classes."""

from __future__ import annotations

# STDLIB
import pathlib
from importlib.metadata import version as get_version

__version__ = get_version(str(pathlib.Path(__file__).parent.name))
