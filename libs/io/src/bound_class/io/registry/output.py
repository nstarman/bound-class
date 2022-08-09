# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar

# LOCAL
from .base import IORegistryBase

__all__ = ["OutputRegistry"]


##############################################################################
# TYPING

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


class OutputCallable(Protocol[T_co]):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...


##############################################################################
# CODE
##############################################################################


@dataclass(frozen=True)
class OutputRegistry(IORegistryBase[T]):

    # ===============================================================

    def register(
        self, data_format: str, data_class: type, function: OutputCallable[T], force: bool = False, priority: float = 0
    ) -> None:
        return super().register(
            data_format=data_format, data_class=data_class, function=function, force=force, priority=priority
        )

    def get_registered(self, data_format: str, data_class: type[T]) -> OutputCallable[T]:
        return super().get_registered(data_format=data_format, data_class=data_class)

    def __call__(self, data: object, *args: Any, format: str | None = None, **kwargs: Any) -> Any:
        """Read in data.

        Parameters
        ----------
        data : object
            The data to write.
        *args
            The arguments passed to this method depend on the format.
        format : str or None
        **kwargs
            The arguments passed to this method depend on the format.

        Returns
        -------
        object or None
            The output of the registered outputter.
        """
        raise NotImplementedError("TODO!")

        # # Expand a tilde-prefixed path if present in args[0]
        # args = _expand_user_in_args(args)

        # if format is None:
        #     path = None
        #     fileobj = None
        #     if len(args):
        #         if isinstance(args[0], PATH_TYPES):
        #             # path might be a os.PathLike object
        #             if isinstance(args[0], os.PathLike):
        #                 args = (os.fspath(args[0]),) + args[1:]
        #             path = args[0]
        #             fileobj = None
        #         elif hasattr(args[0], 'read'):
        #             path = None
        #             fileobj = args[0]

        #     format = self._get_valid_format(
        #         'write', data.__class__, path, fileobj, args, kwargs)

        # writer = self.get_writer(format, data.__class__)
        # return writer(data, *args, **kwargs)
