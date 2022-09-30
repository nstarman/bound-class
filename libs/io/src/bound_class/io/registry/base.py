# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import annotations

# STDLIB
from dataclasses import dataclass, field
from math import inf
from operator import itemgetter
from typing import IO, TYPE_CHECKING, Any, AnyStr, Protocol, TypeVar

# LOCAL
from .common import IORegistryError, RegistryBase
from .identify import IdentifierRegistry

if TYPE_CHECKING:
    # STDLIB
    from os import PathLike

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


@dataclass(frozen=True)
class IORegistryBase(RegistryBase[tuple[IOCallable[T], float]]):

    identifier: IdentifierRegistry = field(default_factory=IdentifierRegistry)

    # ===============================================================

    def register(
        self, data_format: str, data_class: type, function: IOCallable[T], force: bool = False, priority: float = 0
    ) -> None:
        """
        Register an I/O function.

        Parameters
        ----------
        data_format : str
            The data format identifier. This is the string that will be used to
            specify the data type when doing I/O.
        data_class : class
            The class of the object that the I/O function produces.
        function : function
            The function to I/O a data object.
        force : bool, optional
            Whether to override any existing function if already present.
            Default is `False`.
        priority : int, optional
            The priority of the I/O function, used to compare possible formats
            when trying to determine the best I/O function to use. Higher
            priorities are preferred over lower priorities, with the default
            priority being 0 (negative numbers are allowed though).
        """
        if (data_format, data_class) in self and not force:
            raise IORegistryError(
                f"I/O function for format {data_format!r} and class {data_class.__name__!r} is already defined"
            )

        self._data[(data_format, data_class)] = (function, priority)

    def get_registered(self, data_format: str, data_class: type[T]) -> IOCallable[T]:
        """Get function for ``data_format``.

        Parameters
        ----------
        data_format : str
            The data format identifier. This is the string that is used to
            specify the data type when doing I/O.
        data_class : class
            The class of the object that can be I/Oed.

        Returns
        -------
        function : callable
            The registered function for this format and class.
        """
        ios = [(fmt, cls) for fmt, cls in self.keys() if fmt == data_format]

        for fmt, kls in ios:
            if self._is_best_match(data_class, kls, ios):
                return self[(fmt, kls)][0]
        else:
            # TODO!
            # format_table_str = self._get_format_table_str(data_class, 'Read')
            format_table_str = tuple(fmt for fmt, _ in self.keys())
            raise IORegistryError(
                f"No I/O function defined for format {data_format!r} and class {data_class.__name__!r}."
                f"\n\nThe available formats are:\n\n{format_table_str}"
            )

    # ===============================================================
    # Working with `identifier`

    def _identify_highest_priority_format(self, cls: type, valid_formats: list[str]) -> str:

        best_formats: list[str] = []
        current_priority: float = -inf
        for fmt in valid_formats:
            try:
                _, priority = self[(fmt, cls)]
            except KeyError:
                # We could throw an exception here, but get_reader/get_writer handle
                # this case better, instead maximally deprioritise the format.
                priority = -inf

            if priority == current_priority:
                best_formats.append(fmt)
            elif priority > current_priority:
                best_formats = [fmt]
                current_priority = priority

        if len(best_formats) > 1:
            raise IORegistryError(
                "Format is ambiguous - options are: {}".format(", ".join(sorted(valid_formats, key=itemgetter(0))))
            )
        return best_formats[0]

    def identify_format(
        self, which: str, cls: type, path: PathLike[AnyStr], fileobj: IO[AnyStr], options: dict[str, Any]
    ) -> str:
        valid_formats = self.identifier(data_class_required=cls, path=path, fileobj=fileobj, options=options)

        if not valid_formats:
            raise IORegistryError(
                "Format could not be identified based on the arguments, please provide a 'format' argument.\n"
                f"The available formats are:\n{self.get_formats()}."
            )
        elif len(valid_formats) > 1:
            fmt = self._identify_highest_priority_format(cls, valid_formats)
        else:
            fmt = valid_formats[0]

        return fmt
