# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import annotations

# STDLIB
from dataclasses import InitVar, dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Iterator,
    Mapping,
    MutableMapping,
    Protocol,
    TypeVar,
)

if TYPE_CHECKING:
    # THIRD PARTY
    from typing_extensions import TypeAlias

__all__: list[str] = []


##############################################################################
# TYPING


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
K: TypeAlias = tuple[str, type]
V = TypeVar("V")


class IOCallable(Protocol[T_co]):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...


##############################################################################
# CODE
##############################################################################


class IORegistryError(Exception):
    """Custom error for registry clashes."""


# TODO!  dataclass doesn't support abc
@dataclass(frozen=True)  # metaclass=ABCMeta
class RegistryBase(Mapping[K, V]):
    """Abstract base class for registries.

    Parameters
    ----------
    name : str data : `~collections.abc.MutableMapping`

    Notes
    -----
    The only requirement for the ``data`` argument is that it is a mutable
    mapping. In particular, this means that an external database system, e.g. an
    SQL database, could be used (though it might need to be wrapped as a mutable
    mapping).
    """

    # _: KW_ONLY
    name: str
    data: InitVar[MutableMapping[K, V] | None] = None  # TODO! when py3.10+

    def __post_init__(self, data: MutableMapping[K, V] | None) -> None:
        self._data: MutableMapping[K, V]
        object.__setattr__(self, "_data", data if data is not None else {})

    # ===============================================================
    # Mapping

    def __getitem__(self, key: K) -> V:
        return self._data[key]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    def __repr__(self) -> str:
        return repr(self._data)  # TODO! include name

    # ===============================================================

    def get_formats(self, data_class: type | None = None, filter_on: str | None = None) -> tuple[str, ...]:
        """Get the list of registered formats."""
        return tuple(s for s, _ in self.keys())

    # ===============================================================

    # @abstractmethod  # dataclass doesn't support abc
    def register(
        self, data_format: str, data_class: type, function: Any, force: bool = False, priority: int = 0
    ) -> None:
        raise NotImplementedError

    def unregister(self, data_format: str, data_class: type) -> None:
        """
        Unregister a function.

        Parameters
        ----------
        data_format : str
            The data format identifier.
        data_class : class
            The class of the object that the I/O produces.
        """
        if (data_format, data_class) not in self:
            raise IORegistryError(
                f"Nothing in registry {self.name!r} for format {data_format!r} and class {data_class.__name__!r}"
            )

        self._data.pop((data_format, data_class))

    # @abstractmethod  # TODO!
    # def get_registered(self, data_format: str, data_class: type[T]) -> V:
    #     raise NotImplementedError

    # @abstractmethod  # TODO!
    # def __call__(self, *args: Any, **kwds: Any) -> Any:
    #     raise NotImplementedError

    def _is_best_match(self, class1: type, class2: type, format_classes: Collection[K]) -> bool:
        """
        Determine if class2 is the "best" match for class1 in the list
        of classes.  It is assumed that (class2 in classes) is True.
        class2 is the the best match if:

        - ``class1`` is a subclass of ``class2`` AND
        - ``class2`` is the nearest ancestor of ``class1`` that is in classes
          (which includes the case that ``class1 is class2``)
        """
        out: bool = False
        if not issubclass(class1, class2):
            return out

        classes = {cls for _, cls in format_classes}
        for parent in class1.__mro__:
            if parent is class2:  # class2 is closest registered ancestor
                out = True
                break
            if parent in classes:  # class2 was superceded
                break

        return out
