"""Register an accessor class on a class."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Callable, Literal

from bound_class.core.accessors.descriptor import AccessorProperty
from bound_class.core.descriptors.register import DescriptorRegistrationWarning

if TYPE_CHECKING:
    from bound_class.core.accessors.core import AccessorLike
    from bound_class.core.base import BndTo

__all__: list[str] = []


class AccessorRegistrationWarning(DescriptorRegistrationWarning):
    """Warning for conflicts in accessor registration."""


def register_accessor(
    cls: type[BndTo],
    name: str,
    *,
    store_in: Literal["__dict__", "_attrs_"] | None = "__dict__",
) -> Callable[[type[AccessorLike[BndTo]]], type[AccessorLike[BndTo]]]:
    """Decorator to register an accessor class.

    Parameters
    ----------
    cls : type[BndTo]
        The class to which to add the accessor.
    name : str
        The name of the accessor on `cls`.
    store_in : Literal["__dict__", "_attrs_"] | None, optional
        The attribute of the class to which to store the accessor instance. By
        default, this is ``"__dict__"``.

    Returns
    -------
    Callable[[type[AccessorLike[BndTo]]], type[AccessorLike[BndTo]]]
        The decorator.
    """

    def decorator(accessor_cls: type[AccessorLike[BndTo]]) -> type[AccessorLike[BndTo]]:
        # TODO! validation that ``accessor_cls``

        if hasattr(cls, name):
            warnings.warn(
                f"registration of accessor {accessor_cls!r} under name {name!r} for "
                f"type {cls!r} is overriding an attribute of the same name.",
                AccessorRegistrationWarning,
                stacklevel=2,
            )

        descriptor = AccessorProperty(accessor_cls, store_in=store_in)
        descriptor.__set_name__(descriptor, name)
        setattr(cls, name, descriptor)

        return accessor_cls

    return decorator
