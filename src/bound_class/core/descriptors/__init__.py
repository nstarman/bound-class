"""Descriptors."""

from bound_class.core.descriptors.bound import BoundDescriptor
from bound_class.core.descriptors.instance import InstanceDescriptor
from bound_class.core.descriptors.register import register_descriptor

__all__ = ["BoundDescriptor", "InstanceDescriptor", "register_descriptor"]
