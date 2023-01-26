# see LICENSE.rst

"""Bound Classes."""

from __future__ import annotations

# LOCAL
from bound_class.core import base, descriptors  # noqa: F401
from bound_class.core.accessors import register_accessor
from bound_class.core.descriptors import InstanceDescriptor, register_descriptor
from bound_class.core.setup_package import __version__  # noqa: F401

__all__ = [
    "InstanceDescriptor",
    "register_descriptor",
    "register_accessor",
]
