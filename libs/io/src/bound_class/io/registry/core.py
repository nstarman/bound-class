from __future__ import annotations

# STDLIB
import contextlib
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Iterator,
    KeysView,
    Mapping,
    Sequence,
    TypeVar,
    cast,
)
from weakref import WeakSet

# LOCAL
from .base import IORegistryBase
from .input import InputRegistry
from .output import OutputRegistry

if TYPE_CHECKING:
    # LOCAL
    from .identify import IdentifierRegistry

T = TypeVar("T")


class RegistryManager(Generic[T]):
    def __init__(self, **registries: IORegistryBase[T]) -> None:

        self._registries: dict[str, IdentifierRegistry | IORegistryBase[T]] = {}
        self._registries.update(registries)

        # If multiple formats are added to one class the update of the docs is quite
        # expensive. Classes for which the doc update is temporarly delayed are added
        # to this set.
        self._delayed_docs_classes: WeakSet[type] = WeakSet()

    # =========================================================================

    @property
    def available_registries(self) -> KeysView[str]:
        """Available registries.

        Returns
        -------
        ``dict_keys``
        """
        return self._registries.keys()

    @contextlib.contextmanager
    def delay_doc_updates(self, cls: type) -> Iterator[Any]:
        """Contextmanager to disable documentation updates when registering
        reader and writer. The documentation is only built once when the
        contextmanager exits.

        .. versionadded:: 1.3

        Parameters
        ----------
        cls : class
            Class for which the documentation updates should be delayed.

        Notes
        -----
        Registering multiple readers and writers can cause significant overhead
        because the documentation of the corresponding ``read`` and ``write``
        methods are build every time.

        Examples
        --------
        see for example the source code of ``astropy.table.__init__``.
        """
        self._delayed_docs_classes.add(cls)

        yield

        self._delayed_docs_classes.discard(cls)
        for method in self._registries.keys() - {"identify"}:
            self._update__doc__(method, cls)

    def _update__doc__(self, which: str, data_class: type) -> None:
        # TODO!
        # raise NotImplementedError("TODO!")
        return

    def get_formats(self, data_class: type | None = None, filter_on: str | None = None) -> Any:
        """
        Get the list of registered formats as a table.
        """
        # if which not in self._registries:
        #     raise ValueError

        # reg = self._registries[which]
        # return reg.get_formats(data_class=data_class, filter_on=filter_on)
        raise NotImplementedError("TODO!")

    # =========================================================================

    def register(self, which: str, *args: Any, **kwargs: Any) -> None:
        """Register a format on a sub-registry.

        Parameters
        ----------
        which : str
            On which sub-registry to register.
        """
        if which not in self._registries:
            raise ValueError

        reg = self._registries[which]
        reg.register(*args, **kwargs)

        if isinstance(reg, IORegistryBase):  # skips e.g. IdentifierRegistry
            if args[1] not in self._delayed_docs_classes:
                self._update__doc__(reg.name, args[1])

    def unregister(self, which: str, data_format: str, data_class: type) -> None:
        """
        Unregister a reader function

        Parameters
        ----------
        data_format : str
            The data format identifier.
        data_class : class
            The class of the object that the reader produces.
        """
        if which not in self._registries:
            raise ValueError

        reg = self._registries[which]
        assert hasattr(reg, "unregister")
        assert callable(reg.unregister)
        reg.unregister(data_format, data_class)

        if data_class not in self._delayed_docs_classes:
            self._update__doc__(reg.name, data_class)

    def get_registered(self, which: str, data_format: str, data_class: type) -> Callable[..., Any]:
        if which not in self._registries:
            raise ValueError

        reg = self._registries[which]
        out = getattr(reg, "get_registered")(data_format, data_class)
        return cast(Callable[..., Any], out)

    def __call__(
        self, which: str, /, args: Sequence[Any] | None = None, kwargs: Mapping[str, Any] | None = None
    ) -> Any:
        if which not in self._registries:
            raise ValueError

        reg = self._registries[which]
        return cast(Callable[..., Any], reg)(*(args or ()), **(kwargs or {}))


# ===================================================================

# Convenience functions


def make_manager_for(
    inputs: tuple[str, ...] = ("read", "from_format"),
    outputs: tuple[str, ...] = ("write", "to_format"),
) -> RegistryManager[Any]:
    registries: dict[str, IORegistryBase[Any]] = {}

    for n in inputs:
        registries[n] = InputRegistry(data=None, name=n)

    for n in outputs:
        registries[n] = OutputRegistry(data=None, name=n)

    rm = RegistryManager[Any](**registries)

    return rm
