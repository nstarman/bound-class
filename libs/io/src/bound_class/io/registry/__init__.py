# LOCAL
from .core import RegistryManager, make_manager_for
from .identify import IdentifierRegistry
from .input import InputRegistry
from .output import OutputRegistry

__all__ = [
    "RegistryManager",
    "make_manager_for",
    "IdentifierRegistry",
    "InputRegistry",
    "OutputRegistry",
]
