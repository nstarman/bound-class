# see LICENSE.rst

"""Bound Classes."""

from __future__ import annotations

from bound_class.core.accessors import register_accessor
from bound_class.core.base import BoundClass, BoundClassRef
from bound_class.core.descriptors import BoundDescriptor, InstanceDescriptor, register_descriptor
from bound_class.core.setup_package import __version__  # noqa: F401

__all__ = [
    "BoundClass",
    "BoundClassRef",
    "BoundDescriptor",
    "InstanceDescriptor",
    "register_descriptor",
    "register_accessor",
]
