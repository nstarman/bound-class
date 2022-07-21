"""Descriptors on the instance, not the class."""

##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
import copy
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar

# LOCAL
from bound_class.base import BoundClass

__all__: list[str] = []


##############################################################################
# PARAMETERS

Self = TypeVar("Self")  # mypy not yet compatible with Self


class SupportsDictAndName(Protocol):
    @property
    def __dict__(self) -> dict[str, Any]:  # type: ignore
        ...

    @property
    def __name__(self) -> str:
        ...


BoundToType = TypeVar("BoundToType", bound=SupportsDictAndName)


##############################################################################
# CODE
##############################################################################


@dataclass
class InstanceDescriptorBase(BoundClass[BoundToType]):
    def __set_name__(self, _: Any, name: str) -> None:
        # Store the name of the attribute on the enclosing object
        self._enclosing_attr: str
        object.__setattr__(self, "_enclosing_attr", name)

    def _replace(self: Self) -> Self:
        """Make a copy of the descriptor."""
        descriptor = copy.copy(self)  # TODO? deepcopy
        return descriptor

    @property
    def enclosing(self) -> BoundToType:
        """Return the enclosing instance to which this one is bound."""
        return self.__self__
