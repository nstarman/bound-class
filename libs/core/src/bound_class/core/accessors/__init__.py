# LOCAL
from bound_class.core.accessors.core import Accessor, AccessorLike
from bound_class.core.accessors.descriptor import AccessorProperty
from bound_class.core.accessors.register import register_accessor

__all__ = [
    "AccessorLike",
    "Accessor",
    "AccessorProperty",
    "register_accessor",
]
