"""Descriptors on the instance, not the class."""

##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import Any, Literal, NoReturn, Protocol, TypeVar

# LOCAL
from bound_class.base import BoundClass

__all__: list[str] = []


##############################################################################
# PARAMETERS

Self = TypeVar("Self")  # mypy not yet compatible with Self


class SupportsDictAndName(Protocol):
    __dict__: dict[str, Any]

    @property
    def __name__(self) -> str:
        ...


BndTo = TypeVar("BndTo", bound=SupportsDictAndName)


##############################################################################
# CODE
##############################################################################


@dataclass
class BoundDescriptorBase(BoundClass[BndTo]):
    """Base class for instance-level descriptors.

    Attributes
    ----------
    enclosing : BndTo
        Returns the enclosing instance to which this one is bound.

    Notes
    -----
    Normally descriptors are bound to a class and are used on instances of that
    class according to the ``__get__`` method. While very useful for, e.g.
    performing validation, this essentially makes descriptors just fancy
    methods. Using |BoundClass| descriptors can now be easily bound to class
    instances, not the class.

    There are currently some limitations:

    1. The class must have a ``__dict__`` attribute. This doesn't preclude
       slots, but few slotted classes also have a ``__dict__``.
    2. The class must have a ``__name__`` attribute. Pretty much all classes do,
       so don't worry about this one.

    This is a base class and mostly exists because MyPy complains that
    :class:`bound_class.descriptors.BoundDescriptor` and
    :class:`bound_class.descriptors.InstanceDescriptor` do not have matching
    signatures for ``__get__``.
    """

    cache_loc: Literal["__dict__", "__cache__", None] = "__dict__"

    # ===============================================================
    # Descriptor

    def __set_name__(self, _: Any, name: str) -> None:
        # Store the name of the attribute on the enclosing object
        self._enclosing_attr: str
        object.__setattr__(self, "_enclosing_attr", name)

    # @abstractmethod
    # def __get__(
    #     self,
    #     enclosing: BndTo | None,
    #     enclosing_type: None | type[BndTo],
    # ):
    #     ...

    def __set__(self, _: str, __: Any) -> NoReturn:
        raise AttributeError  # TODO! useful error message

    # ===============================================================

    @property
    def enclosing(self) -> BndTo:
        """Return the enclosing instance to which this one is bound."""
        return self.__self__
