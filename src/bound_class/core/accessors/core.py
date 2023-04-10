"""Core functionality for accessors."""

from __future__ import annotations

from typing import Protocol, TypeVar

from bound_class.core.base import BndTo, BoundClass, BoundClassRef

__all__: list[str] = []


ABndTo = TypeVar("ABndTo", covariant=True)


# @runtime_checkable  # TODO! https://github.com/mypyc/mypyc/issues/909
class AccessorLike(Protocol[BndTo]):
    """Protocol for `Accessor`-like classes."""

    def __init__(self, accessee: BndTo) -> None:
        ...

    # from BoundClassLike (can't inherit b/c C)
    __selfref__: BoundClassRef[BndTo] | None
    __self__: BndTo


class Accessor(BoundClass[BndTo]):
    """A convenience base class for acceessors.

    This class ensures the accessee is stored as a `weakref.ReferenceType` and
    correctly cleaned up. Classes do NOT need to be subclasses of this class to
    work with the accessor machinery. The only requirement is that they are
    ``AccessorLike`` (a `~typing.Protocool`).

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
