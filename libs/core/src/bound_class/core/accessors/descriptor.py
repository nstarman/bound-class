from __future__ import annotations

# STDLIB
from dataclasses import dataclass, replace
from typing import Any, MutableMapping, NoReturn, overload

# LOCAL
from bound_class.core.accessors.core import AccessorLike
from bound_class.core.base import BndTo
from bound_class.core.descriptors.base import BoundDescriptorBase

__all__: list[str] = []


class _NullAccessor(AccessorLike[Any]):
    """Protocol for `Accessor`-like classes.

    # TODO! remove when py3.10+
    # see https://docs.python.org/3/library/dataclasses.html#re-ordering-of-keyword-only-parameters-in-init
    """

    accessee: Any = None

    def __init__(self, bound: Any, /) -> None:
        self.__wrapped__ = bound
        raise NotImplementedError(
            "this is a non-operable placeholder class until py3.10+. "
            "See https://docs.python.org/3/library/dataclasses.html#re-ordering-of-keyword-only-parameters-in-init"
        )


@dataclass
class AccessorPropertyBase(BoundDescriptorBase[BndTo]):

    # See https://github.com/pandas-dev/pandas/blob/main/pandas/_libs/properties.pyx for a CPython implementation

    accessor_cls: type[AccessorLike[BndTo]] | type[AccessorLike[type[BndTo]]] = _NullAccessor
    # Either an accessor on the instance or class

    def __post_init__(self) -> None:
        super().__post_init__()  # for store_in

        # TODO! remove when py3.10+
        # see https://docs.python.org/3/library/dataclasses.html#re-ordering-of-keyword-only-parameters-in-init
        if self.accessor_cls is _NullAccessor:
            raise TypeError

        # Set the docstring
        object.__setattr__(self, "__doc__", self.accessor_cls.__doc__)

    def __set__(self, _: str, __: Any) -> NoReturn:
        raise AttributeError  # TODO! useful error message


@dataclass
class AccessorClassPropertyBase(AccessorPropertyBase[BndTo]):
    # included for type narrowing
    accessor_cls: type[AccessorLike[type[BndTo]]] = _NullAccessor


@dataclass
class AccessorInstPropertyBase(AccessorPropertyBase[BndTo]):
    # included for type narrowing
    accessor_cls: type[AccessorLike[BndTo]] = _NullAccessor


# ===================================================================


@dataclass
class AccessorProperty(AccessorInstPropertyBase[BndTo]):
    """Descriptor for accessors.

    Parameters
    ----------
    accessor_cls : type
        Must NOT be None. This may look like a valid option, but it is not.
        :mod:`dataclasses` in Python <= 3.10 does not support inheitance and
        keyword argument ordering.
    store_in : {"__dict__", "_attrs_"}
        Should be in ``__slots__`` of enclosing object.
    """

    accessor_cls: type[AccessorLike[BndTo]] = _NullAccessor
    # Accessor on the instance

    # ===============================================================
    # Descriptor

    @overload
    def __get__(self, enclosing: None, _: type[BndTo]) -> type[AccessorLike[BndTo]]:
        ...

    @overload
    def __get__(self, enclosing: BndTo, _: None) -> AccessorLike[BndTo]:
        ...

    def __get__(
        self, enclosing: None | BndTo, _: type[BndTo] | None
    ) -> AccessorLike[BndTo] | type[AccessorLike[BndTo]]:
        assert self.accessor_cls is not None  # TODO! rm py3.10+

        # Opt 1) accessed from the class, so return the accessor class.
        if enclosing is None:
            return self.accessor_cls

        # Opt 2) accessed from the instance, so return accessor instance.
        accessor = _get_accessor_instance(self, enclosing)

        return accessor


def _get_accessor_instance(self: AccessorInstPropertyBase[BndTo], enclosing: BndTo) -> AccessorLike[BndTo]:

    if self.store_in is None:
        dscr = replace(self)
        dscr.__self__ = enclosing
        accessor = self.accessor_cls(dscr)

    else:
        cache: MutableMapping[str, Any] = getattr(enclosing, self.store_in)
        obj = cache.get(self._enclosing_attr)  # get from enclosing.

        if obj is None:  # hasn't been created on the enclosing
            dscr = replace(self)
            dscr.__self__ = enclosing
            accessor = self.accessor_cls(dscr)
            # store on enclosing instance
            cache[self._enclosing_attr] = accessor
        elif not isinstance(obj, self.accessor_cls):
            raise TypeError(f"accessor must be type <{type(self)}> not <{type(obj)}>")
        else:
            accessor = obj
            accessor.__wrapped__.__self__ = enclosing

    return accessor
