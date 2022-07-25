# LOCAL
from .core import Accessor, AccessorLike
from .descriptor import AccessorProperty
from .register import register_accessor

__all__ = [
    "AccessorLike",
    "Accessor",
    "AccessorProperty",
    "register_accessor",
]
