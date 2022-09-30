# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import IO, TYPE_CHECKING, Any, AnyStr, Mapping, Protocol, final

# LOCAL
from .common import IORegistryError, RegistryBase

if TYPE_CHECKING:
    # STDLIB
    from os import PathLike

__all__ = ["IdentifierRegistry"]


##############################################################################
# TYPING


class IdentifyCallable(Protocol):
    def __call__(self, path: PathLike[AnyStr], fileobj: IO[AnyStr], options: Mapping[str, Any]) -> bool:
        ...


##############################################################################


@final
@dataclass(frozen=True)
class IdentifierRegistry(RegistryBase[IdentifyCallable]):
    # registry of identifier functions

    name: str = "Auto-identify"

    # ===============================================================

    def register(
        self, data_format: str, data_class: type, function: IdentifyCallable, force: bool = False, priority: int = 0
    ) -> None:
        """
        Associate an identifier function with a specific data type.

        Parameters
        ----------
        data_format : str
            The data format identifier. This is the string that is used to
            specify the data type when reading/writing.
        data_class : class
            The class of the object that can be written.
        function : function
            A function that checks the argument specified to `read` or `write` to
            determine whether the input can be interpreted as a table of type
            ``data_format``. This function should take the following arguments:

               - ``which``: A string ``"read"`` or ``"write"`` identifying whether
                 the file is to be opened for reading or writing.
               - ``path``: The path to the file.
               - ``fileobj``: An open file object to read the file's contents, or
                 `None` if the file could not be opened.
               - ``options``: Keyword arguments for the `read` or `write`
                 function.

            One or both of ``path`` or ``fileobj`` may be `None`.  If they are
            both `None`, the identifier will need to work from ``args[0]``.

            The function should return True if the input can be identified
            as being of format ``data_format``, and False otherwise.
        force : bool, optional
            Whether to override any existing function if already present.
            Default is ``False``.
        priority : int, optional
            NOT USED. Included for compatility with base class.

        Examples
        --------
        To set the identifier based on extensions, for formats that take a
        filename as a first argument, you can do for example

        .. code-block:: python

            from astropy.io.registry import register_identifier
            from astropy.table import Table
            def my_identifier(*args, **kwargs):
                return isinstance(args[0], str) and args[0].endswith('.tbl')
            register_identifier('ipac', Table, my_identifier)
            unregister_identifier('ipac', Table)
        """
        if (data_format, data_class) in self and not force:
            raise IORegistryError(
                f"Identifier for format {data_format!r} and class {data_class.__name__!r} is already defined"
            )

        self._data[(data_format, data_class)] = function

    def get_registered(self, data_format: str, data_class: type) -> IdentifyCallable:
        return self[(data_format, data_class)]

    def __call__(
        self,
        data_class_required: type,
        path: PathLike[AnyStr],
        fileobj: IO[AnyStr],
        options: dict[str, Any],
    ) -> list[str]:
        valid_formats: list[str] = []

        for data_format, data_class in self.keys():
            if not self._is_best_match(data_class_required, data_class, self.keys()):
                continue

            if self[(data_format, data_class)](path, fileobj, options=options):
                valid_formats.append(data_format)

        return valid_formats
