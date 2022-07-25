# see LICENSE.rst

"""Bound Classes."""

from __future__ import annotations

# LOCAL
from . import base, descriptors  # noqa: F401, TC002
from .descriptors import InstanceDescriptor, register_descriptor
from .setup_package import __version__  # noqa: F401, TC002

__all__ = [
    "InstanceDescriptor",
    "register_descriptor",
]
