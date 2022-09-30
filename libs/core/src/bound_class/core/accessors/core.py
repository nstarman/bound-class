from __future__ import annotations

# STDLIB
from typing import Protocol, runtime_checkable

# LOCAL
from bound_class.core.base import BndTo, BoundClassLike

__all__: list[str] = []


class AccesorPropertyBaseLike(Protocol[BndTo]):
    accessor_cls: type[AccessorLike[BndTo]] | type[AccessorLike[type[BndTo]]]


@runtime_checkable
class AccessorLike(Protocol[BndTo]):
    """Protocol for `Accessor`-like classes."""

    # __doc__: str | None

    def __init__(self, bound: BoundClassLike[BndTo], /) -> None:
        ...

    __wrapped__: BoundClassLike[BndTo]
    # TODO! not sure if __wrapped__ is the right name

    @property
    def accessee(self) -> BndTo:
        ...


class Accessor(AccessorLike[BndTo]):
    """A convenience base class for accessors.



    # This class ensures the accessee is stored as a `weakref.ReferenceType` and
    # correctly cleaned up. Classes do NOT need to be subclasses of this class to
    # work with the accessor machinery. The only requirement is that they are
    # `AccessorLike` (a run-time-checkable `~typing.Protocool`).

    Parameters
    ----------
    wrapper : object, positional-only
        The object to which this object is the accessor.
    """

    def __init__(self, bound: BoundClassLike[BndTo], /) -> None:
        self.__wrapped__ = bound

    @property
    def accessee(self) -> BndTo:
        """Return the instance that this one is an accessor for.

        Each access of this properety dereferences a `weakref.RefernceType`, so
        it is sometimes better to assign this property to a variable and work
        with that.

        .. code-block:: python

            obj = accessor.accessee obj...
        """
        return self.__wrapped__.__self__
