"""Core functionality for accessors."""

from __future__ import annotations

# STDLIB
from typing import Protocol, TypeVar, runtime_checkable

# LOCAL
from bound_class.core.base import BndTo, BoundClass, BoundClassLike

__all__: list[str] = []


ABndTo = TypeVar("ABndTo", covariant=True)


@runtime_checkable
class AccessorLike(BoundClassLike[BndTo], Protocol):
    """Protocol for `Accessor`-like classes."""

    __doc__: str | None  # noqa: A003

    def __init__(self, accessee: BndTo) -> None:
        ...

    # from BoundClassLike


class Accessor(BoundClass[BndTo]):
    """A convenience base class for acceessors.

    This class ensures the accessee is stored as a `weakref.ReferenceType` and
    correctly cleaned up. Classes do NOT need to be subclasses of this class to
    work with the accessor machinery. The only requirement is that they are
    `AccessorLike` (a run-time-checkable `~typing.Protocool`).

    Parameters
    ----------
    accessee : object
        The object to which this object is the accessor.
    """

    def __init__(self, accessee: BndTo) -> None:
        self._set__self__(accessee)

    @property
    def accessee(self) -> BndTo:
        """Return the instance that this one is an accessor for.

        Each access of this properety dereferences a `weakref.RefernceType`, so
        it is sometimes better to assign this property to a variable and work
        with that.

        .. code-block:: python

            obj = accessor.accessee obj...
        """
        return self.__self__
