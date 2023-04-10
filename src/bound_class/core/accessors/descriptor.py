"""Descriptor for accessors."""

from __future__ import annotations

# STDLIB
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal, MutableMapping, NoReturn, overload

# LOCAL
from bound_class.core.base import BndTo
from bound_class.core.descriptors.base import BoundDescriptorBase

if TYPE_CHECKING:
    # LOCAL
    from bound_class.core.accessors.core import AccessorLike

__all__: list[str] = []


@dataclass
class AccessorProperty(BoundDescriptorBase[BndTo]):
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

    # See https://github.com/pandas-dev/pandas/blob/main/pandas/_libs/properties.pyx for a CPython implementation

    accessor_cls: type[AccessorLike[BndTo]] | None = None
    store_in: Literal["__dict__", "_attrs_"] | None = field(default="__dict__", repr=False)

    # TODO! not need this in py3.9 when have improved dataclass
    def __init__(
        self,
        accessor_cls: type[AccessorLike[BndTo]],
        store_in: Literal["__dict__", "_attrs_"] | None = "__dict__",
    ) -> None:
        object.__setattr__(self, "accessor_cls", accessor_cls)
        object.__setattr__(self, "store_in", store_in)

    def __post_init__(self) -> None:
        # TODO! remove when py3.10+
        # see https://docs.python.org/3/library/dataclasses.html#re-ordering-of-keyword-only-parameters-in-init
        if self.accessor_cls is None:
            raise TypeError

        # Set the docstring
        object.__setattr__(self, "__doc__", getattr(self.accessor_cls, "__doc__", None))
        # TODO! getattr b/c https://github.com/mypyc/mypyc/issues/909

    # ===============================================================
    # Descriptor

    @overload
    def __get__(self, enclosing: None, _: type[BndTo]) -> type[AccessorLike[BndTo]]:
        ...

    @overload
    def __get__(self, enclosing: BndTo, _: None) -> AccessorLike[BndTo]:
        ...

    def __get__(
        self,
        enclosing: BndTo | None,
        _: None | type[BndTo],
    ) -> AccessorLike[BndTo] | type[AccessorLike[BndTo]]:
        assert self.accessor_cls is not None  # TODO! rm py3.10+  # noqa: S101

        # Opt 1) accessed from the class, so return the accessor class.
        if enclosing is None:
            return self.accessor_cls

        # Opt 2) accessed from the instance, so return accesssor instance.
        if self.store_in is None:
            accessor = self.accessor_cls(enclosing)

        else:  # try to get from cache
            cache: MutableMapping[str, Any] = getattr(enclosing, self.store_in)
            obj = cache.get(self._enclosing_attr)  # get from enclosing.

            if obj is None:  # hasn't been created on the enclosing
                accesssor = self.accessor_cls(enclosing)
                # store on enclosing instance
                cache[self._enclosing_attr] = accesssor
            elif not isinstance(obj, self.accessor_cls):
                msg = f"accessor must be type <{type(self)}> not <{type(obj)}>"
                raise TypeError(msg)
            else:
                accesssor = obj

        return accessor

    def __set__(self, _: str, __: object) -> NoReturn:
        raise AttributeError  # TODO! useful error message
