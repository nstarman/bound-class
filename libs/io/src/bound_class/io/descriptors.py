# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import annotations

# STDLIB
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Any, Literal, NoReturn, overload

# LOCAL
from .accessor import UnifiedIO
from .registry.core import RegistryManager, make_manager_for
from bound_class.core.accessors.descriptor import (
    AccessorClassPropertyBase,
    AccessorInstPropertyBase,
    AccessorPropertyBase,
    _get_accessor_instance,
)
from bound_class.core.base import BndTo

if TYPE_CHECKING:
    # LOCAL
    from bound_class.core.accessors.core import AccessorLike

__all__: list[str] = []


###############################################################################
# CODE
###############################################################################


class IOError(Exception):
    """Base error for I/O."""


class InputError(IOError):
    """Base error for I/O."""


class OutputError(IOError):
    """Base error for I/O."""


###############################################################################


class _NullUnifiedIO(UnifiedIO[Any]):
    """Protocol for `Accessor`-like classes.

    # TODO! remove when py3.10+
    # see https://docs.python.org/3/library/dataclasses.html#re-ordering-of-keyword-only-parameters-in-init
    """

    def __init__(self, accessee: Any, attr: Any) -> None:
        raise NotImplementedError(
            "this is a non-operable placeholder class until py3.10+. "
            "See https://docs.python.org/3/library/dataclasses.html#re-ordering-of-keyword-only-parameters-in-init"
        )

    accessee: Any = None


# @dataclass
# class IOMethodBase(AccessorPropertyBase[BndTo]):

#     accessor_cls: type[UnifiedIO[BndTo]] | type[UnifiedIO[type[BndTo]]] = _NullUnifiedIO
#     registry: RegistryManager[Any] = field(default_factory=make_manager_for)  # TODO? not Any type


###############################################################################


@dataclass
class InputMethod(AccessorClassPropertyBase[BndTo]):
    """Descriptor class for adding I/O methods in unified I/O.

    ::

      read = UnifiedReadWriteMethod(TableRead)
      write = UnifiedReadWriteMethod(TableWrite)

    Parameters
    ----------
    func : `~astropy.io.registry.UnifiedReadWrite` subclass
        Class that defines read or write functionality

    """

    accessor_cls: type[UnifiedIO[type[BndTo]]] = _NullUnifiedIO
    store_in: Literal["__dict__", "_attrs_", None] = field(default=None, init=False)
    # This is for class access, so there's no storage.
    # it will fail if overriden to __dict__ or __attrs_
    registry: RegistryManager[Any] = field(default_factory=make_manager_for)  # TODO? not Any type

    def __post_init__(self) -> None:
        super().__post_init__()

        # Set `store_in`, which was turned off
        object.__setattr__(self, "store_in", None)

    # ===============================================================
    # Descriptor

    @overload
    def __get__(self, enclosing: None, enclosing_cls: type[BndTo]) -> AccessorLike[BndTo]:
        ...

    @overload
    def __get__(self, enclosing: Any, enclosing_cls: None) -> NoReturn:
        ...

    def __get__(self, enclosing: None | Any, enclosing_cls: type[BndTo] | None) -> AccessorLike[BndTo]:
        assert self.accessor_cls is not None  # TODO! rm py3.10+

        # 1) Accessed from an instance
        if enclosing is not None or enclosing_cls is None:
            raise ValueError

        # 2) Accessed from a class
        dscr = replace(self)
        dscr.__self__ = enclosing_cls
        accessor = self.accessor_cls(dscr)

        return accessor


@dataclass
class OutputMethod(AccessorInstPropertyBase[BndTo]):
    """Descriptor class for adding I/O methods in unified I/O.

    ::

      read = UnifiedReadWriteMethod(TableRead)
      write = UnifiedReadWriteMethod(TableWrite)

    Parameters
    ----------
    func : `~astropy.io.registry.UnifiedReadWrite` subclass
        Class that defines read or write functionality
    """

    accessor_cls: type[UnifiedIO[BndTo]] = _NullUnifiedIO
    registry: RegistryManager[Any] = field(default_factory=make_manager_for)  # TODO? not Any type

    # ===============================================================
    # Descriptor

    @overload
    def __get__(self, enclosing: None, _: type[BndTo]) -> NoReturn:
        ...

    @overload
    def __get__(self, enclosing: BndTo, _: None) -> AccessorLike[BndTo]:
        ...

    # TODO! use Self
    def __get__(self, enclosing: None | BndTo, _: type[BndTo] | None) -> NoReturn | AccessorLike[BndTo]:
        assert self.accessor_cls is not None  # TODO! rm py3.10+

        # Opt 1) accessed from the class
        if enclosing is None:
            raise OutputError

        # Opt 2) accessed from the instance, so return accessor instance.
        accessor = _get_accessor_instance(self, enclosing)

        return accessor


###############################################################################


@dataclass
class UnifiedIOMethod(AccessorPropertyBase[BndTo]):

    accessor_cls: type[UnifiedIO[BndTo]] = _NullUnifiedIO
    store_in: Literal["__dict__", "_attrs_", None] = field(default=None, init=False)
    # This is for class access, so there's no storage.
    # it will fail if overriden to __dict__ or __attrs_
    registry: RegistryManager[Any] = field(default_factory=make_manager_for)  # TODO? not Any type

    def __post_init__(self) -> None:
        super().__post_init__()

        # Set `store_in`, which was turned off
        object.__setattr__(self, "store_in", None)

    # ===============================================================
    # Descriptor

    @overload
    def __get__(self, enclosing: None, enclosing_cls: type[BndTo]) -> AccessorLike[BndTo]:
        ...

    @overload
    def __get__(self, enclosing: BndTo, enclosing_cls: None) -> AccessorLike[BndTo]:
        ...

    # TODO! use Self
    def __get__(self, enclosing: None | BndTo, enclosing_cls: type[BndTo] | None) -> AccessorLike[BndTo]:
        assert self.accessor_cls is not None  # TODO! rm py3.10+

        if enclosing is None and enclosing_cls is None:
            raise ValueError

        dscr = replace(self)
        dscr.__self__ = enclosing if enclosing is not None else enclosing_cls
        accessor = self.accessor_cls(dscr)

        return accessor
