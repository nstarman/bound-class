from __future__ import annotations

# STDLIB
import warnings
from typing import TYPE_CHECKING, Callable, Literal

# LOCAL
from .descriptor import AccessorProperty
from bound_class.descriptors.register import DescriptorRegistrationWarning

if TYPE_CHECKING:
    # LOCAL
    from .core import AccessorLike
    from bound_class.base import BndTo

__all__: list[str] = []


class AccessorRegistrationWarning(DescriptorRegistrationWarning):
    """Warning for conflicts in accessor registration."""


def register_accessor(
    cls: type[BndTo], name: str, *, store_in: Literal["__dict__", "_attrs_"] | None = "__dict__"
) -> Callable[[type[AccessorLike[BndTo]]], type[AccessorLike[BndTo]]]:
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
