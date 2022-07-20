"""Descriptors on the instance, not the class."""

##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import overload

# LOCAL
from .base import BoundToType, InstanceDescriptorBase

# from typing_extensions import Self  # TODO! use when mypy doesn't complain


__all__ = ["InstanceDescriptor"]

##############################################################################
# CODE
##############################################################################


@dataclass
class InstanceDescriptor(InstanceDescriptorBase[BoundToType]):
    """Descriptor that is stored on and provides access to its enclosing instance.

    Notes
    -----
    This is a non-data descriptor (see
    https://docs.python.org/3/howto/descriptor.html#descriptor-protocol). When
    ``__get__`` is first called it will make a copy of this descriptor instance
    and place it in the enclosing object's ``__dict__``. Thereafter attribute
    access will return the instance in ``__dict__`` without calling this
    descriptor.
    """

    @overload
    def __get__(
        self: InstanceDescriptor[BoundToType], enclosing: BoundToType, _: None
    ) -> InstanceDescriptor[BoundToType]:
        ...

    @overload
    def __get__(
        self: InstanceDescriptor[BoundToType], enclosing: None, _: type[BoundToType]
    ) -> InstanceDescriptor[BoundToType]:
        ...

    def __get__(
        self: InstanceDescriptor[BoundToType], enclosing: BoundToType | None, _: type[BoundToType] | None
    ) -> InstanceDescriptor[BoundToType]:
        # When called without an instance, return self to allow access
        # to descriptor attributes.
        if enclosing is None:
            return self

        # accessed from an enclosing
        # TODO! support if enclosing is slotted
        descriptor = enclosing.__dict__.get(self._enclosing_attr)  # get from enclosing
        if descriptor is None:  # hasn't been created on the enclosing
            descriptor = self._replace()
            # store on enclosing instance
            enclosing.__dict__[self._enclosing_attr] = descriptor

        # We set `__self__` on every call, since if one makes copies of objs,
        # 'descriptor' will be copied as well, which will lose the reference.
        descriptor.__self__ = enclosing

        return descriptor
