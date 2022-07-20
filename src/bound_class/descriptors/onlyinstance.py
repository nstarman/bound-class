"""Descriptors on the instance, not the class."""

##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import Any, NoReturn, overload

# LOCAL
from .base import BoundToType, InstanceDescriptorBase

# from typing_extensions import Self  # TODO! use when mypy doesn't complain

__all__ = ["InstanceOnlyDescriptor"]


##############################################################################
# CODE
##############################################################################


@dataclass(init=False)
class InstanceOnlyDescriptor(InstanceDescriptorBase[BoundToType]):
    @overload
    def __get__(
        self: InstanceOnlyDescriptor[BoundToType], enclosing: BoundToType, enclosing_cls: None, **changes: Any
    ) -> InstanceOnlyDescriptor[BoundToType]:
        ...

    @overload
    def __get__(self, enclosing: None, enclosing_cls: type[BoundToType], **changes: Any) -> NoReturn:
        ...

    def __get__(
        self: InstanceOnlyDescriptor[BoundToType],
        enclosing: BoundToType | None,
        enclosing_cls: type[BoundToType] | None,
        **changes: Any,
    ) -> InstanceOnlyDescriptor[BoundToType] | NoReturn:
        # When called without an instance, return self to allow access
        # to descriptor attributes.
        if enclosing is None:
            msg = f"{self._enclosing_attr!r} can only be accessed from " + (
                "its enclosing object." if enclosing_cls is None else f"a {enclosing_cls.__name__!r} object"
            )
            raise AttributeError(msg)

        # accessed from an enclosing
        # TODO! support if enclosing has slots
        descriptor = enclosing.__dict__.get(self._enclosing_attr)  # get from enclosing
        if descriptor is None:  # hasn't been created on the enclosing
            descriptor = self._replace(**changes)
            # store on enclosing instance
            enclosing.__dict__[self._enclosing_attr] = descriptor

        # We set `__self__` on every call, since if one makes copies of objs,
        # 'descriptor' will be copied as well, which will lose the reference.
        descriptor.__self__ = enclosing

        return descriptor
