# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import annotations

# STDLIB
import inspect
import os
import pydoc
import re
import sys
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Mapping,
    Protocol,
    Sequence,
    TextIO,
    overload,
    runtime_checkable,
)

# LOCAL
from .registry.common import IORegistryError
from bound_class.core.accessors.core import Accessor
from bound_class.core.base import BndTo, BoundClassLike

if TYPE_CHECKING:
    # LOCAL
    from .registry.core import RegistryManager

__all__ = ["UnifiedIO"]


@runtime_checkable
class IOMethodBaseLike(BoundClassLike[BndTo], Protocol[BndTo]):

    registry: RegistryManager[Any]
    store_in: Literal["__dict__", "_attrs_"] | None
    accessor_cls: type[UnifiedIO[BndTo]]


# -----------------------------------------------------------------------------


@dataclass(frozen=True)
class UnifiedIO(Accessor[BndTo]):
    """Base class for the worker object used in unified I/O methods."""

    def __init__(self, bound: IOMethodBaseLike[BndTo], /) -> None:
        self.__wrapped__: IOMethodBaseLike[BndTo]  # set in super
        super().__init__(bound)

    # ======================================================

    @property
    def registry(self) -> RegistryManager[Any]:
        return self.__wrapped__.registry

    def __call__(
        self, which: str, /, args: Sequence[Any] | None = None, kwargs: Mapping[str, Any] | None = None
    ) -> Any:
        return self.registry(which, args=args, kwargs=kwargs)

    def help(self, which: str, format: str | None = None, out: TextIO | None = None) -> None:
        """Output help documentation for the specified unified I/O ``format``.

        By default the help output is printed to the console via ``pydoc.pager``.
        Instead one can supplied a file handle object as ``out`` and the output
        will be written to that handle.

        Parameters
        ----------
        format : str
            Unified I/O format name, e.g. 'fits' or 'ascii.ecsv'
        out : None or path-like
            Output destination (default is stdout via a pager)
        """
        # Get reader or writer function associated with the registry
        # get_func = self._registry.get_thing
        enclosing = self.__wrapped__.__self__
        data_cls = enclosing if inspect.isclass(enclosing) else type(enclosing)
        method_name = self.__wrapped__._enclosing_attr

        try:
            if format:
                iofunc = self.registry.get_registered(which, data_format=format, data_class=data_cls)
        except IORegistryError as err:
            reader_doc = "ERROR: " + str(err)
        else:
            if format:
                # Format-specific
                header = f"{data_cls.__name__}.{method_name}(format='{format}') documentation\n"
                doc = iofunc.__doc__

            else:
                # General docs
                header = f"{data_cls.__name__}.{method_name} general documentation\n"
                doc = getattr(data_cls, method_name).__doc__

            reader_doc = re.sub(".", "=", header)
            reader_doc += header
            reader_doc += re.sub(".", "=", header)
            reader_doc += os.linesep
            if doc is not None:
                reader_doc += inspect.cleandoc(doc)

        if out is None:
            pydoc.pager(reader_doc)
        else:
            out.write(reader_doc)

    # -----------------------------------------------------

    @overload
    def list_formats(self, out: None) -> None:
        ...

    @overload
    def list_formats(self, out: TextIO) -> TextIO:
        ...

    def list_formats(self, out: TextIO | None = None) -> TextIO | None:
        """Print a list of available formats to console (or ``out`` filehandle)

        out : None or file handle object
            Output destination (default is stdout via a pager)
        """
        tbl = self.__wrapped__.registry.get_formats(self.accessee.__class__, self.__wrapped__._enclosing_attr)

        if out is None:
            out = sys.stdout
            # out.write('\n'.join(tbl.pformat(max_lines=-1, max_width=-1)))
        out.write(tbl)

        return out
