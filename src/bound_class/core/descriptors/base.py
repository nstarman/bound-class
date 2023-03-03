"""Descriptors on the instance, not the class."""

##############################################################################
# IMPORTS

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, NoReturn, TypeVar

# LOCAL
from bound_class.core.base import BndTo, BoundClass, BoundClassRef

if TYPE_CHECKING:
    # THIRD PARTY
    from typing_extensions import TypeAlias


__all__: list[str] = []


##############################################################################
# PARAMETERS

Self = TypeVar("Self")  # mypy not yet compatible with Self

CacheLoc: TypeAlias = Literal["__dict__", "__cache__", None]


##############################################################################
# CODE
##############################################################################


@dataclass
class BoundDescriptorBase(BoundClass[BndTo]):
    """Base class for instance-level descriptors.

    Attributes
    ----------
    enclosing : BndTo
        Returns the enclosing instance to which this one is bound.

    Notes
    -----
    Normally descriptors are bound to a class and are used on instances of that
    class according to the ``__get__`` method. While very useful for, e.g.
    performing validation, this essentially makes descriptors just fancy
    methods. Using |BoundClass| descriptors can now be easily bound to class
    instances, not the class.

    There are currently some limitations:

    1. The class must have a ``__dict__`` attribute. This doesn't preclude
       slots, but few slotted classes also have a ``__dict__``.
    2. The class must have a ``__name__`` attribute. Pretty much all classes do,
       so don't worry about this one.

    This is a base class and mostly exists because MyPy complains that
    :class:`bound_class.descriptors.BoundDescriptor` and
    :class:`bound_class.descriptors.InstanceDescriptor` do not have matching
    signatures for ``__get__``.
    """

    store_in: Literal["__dict__", "_attrs_"] | None = "__dict__"

    def __post_init__(self) -> None:
        self.__selfref__: BoundClassRef[BndTo] | None
        object.__setattr__(self, "__selfref__", None)

    # ===============================================================
    # Descriptor

    def __set_name__(self, _: Any, name: str) -> None:  # noqa: ANN401
        """Store the name of the attribute on the enclosing object."""
        # Store the name of the attribute on the enclosing object
        self._enclosing_attr: str
        object.__setattr__(self, "_enclosing_attr", name)

    # @abstractmethod
    # def __get__(
    #     self,
    #     enclosing: BndTo | None,
    #     enclosing_type: None | type[BndTo],
    # ):
    #     ...

    def __set__(self, _: str, __: object) -> NoReturn:
        """Raise an error when trying to set the value."""
        raise AttributeError  # TODO! useful error message

    # ===============================================================

    @property
    def enclosing(self) -> BndTo:
        """Return the enclosing instance to which this one is bound.

        Each access of this properety dereferences a `weakref.RefernceType`, so
        it is sometimes better to assign this property to a variable and work
        with that.

        .. code-block:: python

            obj = accessor.accessee obj...
        """
        return self.__self__
