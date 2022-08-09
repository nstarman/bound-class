# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar

# LOCAL
from .base import IORegistryBase

__all__ = ["InputRegistry"]


##############################################################################
# TYPING

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


class InputCallable(Protocol[T_co]):
    def __call__(self, *args: Any, **kwds: Any) -> T_co:
        ...


##############################################################################
# CODE
##############################################################################


@dataclass(frozen=True)
class InputRegistry(IORegistryBase[T]):

    # ===============================================================

    def register(
        self, data_format: str, data_class: type, function: InputCallable[T], force: bool = False, priority: float = 0
    ) -> None:
        return super().register(
            data_format=data_format, data_class=data_class, function=function, force=force, priority=priority
        )

    def get_registered(self, data_format: str, data_class: type[T]) -> InputCallable[T]:
        return super().get_registered(data_format=data_format, data_class=data_class)

    def __call__(self, cls: type, *args: Any, format: str | None = None, cache: bool = False, **kwargs: Any) -> Any:
        """
        Read in data.

        Parameters
        ----------
        cls : class
        *args
            The arguments passed to this method depend on the format.
        format : str or None
        cache : bool
            Whether to cache the results of reading in the data.
        **kwargs
            The arguments passed to this method depend on the format.

        Returns
        -------
        object or None
            The output of the registered reader.
        """
        raise NotImplementedError("TODO!")
        # ctx = None
        # try:
        #     # Expand a tilde-prefixed path if present in args[0]
        #     args = _expand_user_in_args(args)

        #     if format is None:
        #         path = None
        #         fileobj = None

        #         if len(args):
        #             if isinstance(args[0], PATH_TYPES) and not os.path.isdir(args[0]):
        #                 from astropy.utils.data import get_readable_fileobj

        #                 # path might be a os.PathLike object
        #                 if isinstance(args[0], os.PathLike):
        #                     args = (os.fspath(args[0]),) + args[1:]
        #                 path = args[0]
        #                 try:
        #                     ctx = get_readable_fileobj(args[0], encoding='binary', cache=cache)
        #                     fileobj = ctx.__enter__()
        #                 except OSError:
        #                     raise
        #                 except Exception:
        #                     fileobj = None
        #                 else:
        #                     args = [fileobj] + list(args[1:])
        #             elif hasattr(args[0], 'read'):
        #                 path = None
        #                 fileobj = args[0]

        #         format = self._get_valid_format(
        #             'read', cls, path, fileobj, args, kwargs)

        #     reader = self.get_reader(format, cls)
        #     data = reader(*args, **kwargs)

        #     if not isinstance(data, cls):
        #         # User has read with a subclass where only the parent class is
        #         # registered.  This returns the parent class, so try coercing
        #         # to desired subclass.
        #         try:
        #             data = cls(data)
        #         except Exception:
        #             raise TypeError('could not convert reader output to {} '
        #                             'class.'.format(cls.__name__))
        # finally:
        #     if ctx is not None:
        #         ctx.__exit__(*sys.exc_info())

        # return data
