from __future__ import annotations

# STDLIB
from typing import Any, Callable, Generic, TypeVar
from weakref import ProxyType, ReferenceType

# THIRD PARTY
from typing_extensions import Self

BoundToType = TypeVar("BoundToType")

class BoundClassRef(Generic[BoundToType]):

    _bound_ref: ReferenceType[BoundClass[BoundToType]]
    def __new__(
        cls: type[Self],
        ob: BoundToType,
        callback: Callable[[ReferenceType[BoundToType]], Any] | None = ...,
        *,
        bound: BoundClass[BoundToType],
    ) -> Self: ...
    def __init__(
        self,
        ob: BoundToType,
        callback: Callable[[ReferenceType[BoundToType]], Any] | None = ...,
        *,
        bound: BoundClass[BoundToType],
    ) -> None: ...
    def _finalizer_callback(self) -> None: ...

class BoundClass(Generic[BoundToType]):
    _self_: BoundClassRef[BoundToType] | None
    @property
    def __self__(self) -> ProxyType[BoundToType]: ...
    @__self__.setter
    def __self__(self, value: BoundToType) -> None: ...
    @__self__.deleter
    def __self__(self) -> None: ...
