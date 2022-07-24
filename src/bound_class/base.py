"""Bound classes."""

##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
import sys
import weakref
from typing import Any, Callable, Generic, TypeVar

__all__ = ["BoundClass"]

##############################################################################
# PARAMETERS

BoundToType = TypeVar("BoundToType")

Self = TypeVar("Self")
# TODO ``from typing_extensions import Self`` when supported


##############################################################################
# CODE
##############################################################################


if sys.version_info >= (3, 9):

    class ReferenceTypeShim(weakref.ReferenceType[BoundToType]):
        pass

else:  # TODO! remove when py3.9+

    class ReferenceTypeShim(weakref.ReferenceType):
        def __class_getitem__(cls, item):
            return cls


class BoundClassRef(ReferenceTypeShim[BoundToType]):
    """`weakref.ref` keeping a `BoundClass` connected to its referant.

    Notes
    -----
    `weakref.ProxyType` autodetects and cleans up deletion of the referent,
    which is great. However, unlike a dereferenced `weakref.ReferenceType`,
    `~weakref.ProxyType` fails ``is`` and ``issubclass`` checks. To emulate the
    auto-cleanup of `weakref.ProxyType`, this class adds a custom finalizer to
    `~weakref.ReferenceType` that will clean up deletion of the referent on the
    bound instance. It is therefore also necessary to store a weak reference
    (using the base `weakref.ref`) to the bound object in the attribute
    ``_bound_ref``.::

        bound object  --> BoundClassRef  --> referent
            ^------- ref <-----|
    """

    __slots__ = ("_bound_ref",)

    # `__new__` is needed for type hint tracing because the superclass defines `__new__` without `bound`.
    def __new__(
        cls: type[Self],
        ob: BoundToType,
        callback: Callable[[weakref.ReferenceType[BoundToType]], Any] | None = None,
        *,
        bound: BoundClass[BoundToType],
    ) -> Self:
        ref: Self = super().__new__(cls, ob, callback)  # type: ignore
        return ref

    def __init__(
        self,
        ob: BoundToType,
        callback: Callable[[weakref.ReferenceType[BoundToType]], Any] | None = None,
        *,
        bound: BoundClass[BoundToType],
    ) -> None:
        # Add a reference to the BoundClass object (it holds ``ob``)
        self._bound_ref = weakref.ref(bound)
        # Create a finalizer that will be called when the referant is deleted,
        # setting ``bound._self_ = None``.
        weakref.finalize(ob, self._finalizer_callback)

    def _finalizer_callback(self) -> None:
        """Callback for finalizer that sets ``bound._self_ = None``."""
        bound = self._bound_ref()
        if bound is not None:  # check that reference to bound is alive.
            del bound.__self__


class BoundClass(Generic[BoundToType]):
    """Base class for a class bound to an instance of another class.

    Attributes
    ----------
    __self__ : object
        The instance of a class to which this class is bound.

    Notes
    -----
    This class is modeled after methods on classes which have a ``__self__``
    attribute when they are on an instance. Assigning ``self.__self__ = <X>`` is
    left to subclasses.

    Examples
    --------
    Methods on classes are unbound:

        >>> class Example:
        ...     def method(self):
        ...         pass
        >>> Example.method
        <function Example.method at ...>

    When the class is instantiated the method becomes bound:

        >>> ex = Example()
        >>> ex.method
        <bound method Example.method of <bound_class.base.Example object at ...>>

    ``BoundClass`` allows this to be extended this so that a class can be
    ``bound`` to another class. Remember that ``BoundClass`` is a baseclass, so
    the specific implementation is determined by which subclass is used. As a
    quick example:

        >>> class Example2:
        ...     @property
        ...     def attribute(self):
        ...         bcb = BoundClass()
        ...         bcb.__self__ = self
        ...         return bcb
        >>> ex2 = Example2()
        >>> ex2.attribute
        <bound_class.base.BoundClass object at ...>
        >>> ex2.attribute.__self__ is ex2
        True

    Behind the scenes ``BoundClass`` uses :mod:`weakref` to ensure that classes
    do not unexpectedly keep each other from being garbage collected. For
    details of this implementation, see `bound_class.base.BoundClassRef`.

        >>> attribute = ex2.attribute  # survives deletion
        >>> del ex2
        >>> try: attribute.__self__
        ... except ReferenceError: print("ex2 has been deleted")
        ex2 has been deleted
    """

    @property
    def __self__(self) -> BoundToType:
        """Return object to which this one is bound.

        Returns
        -------
        object

        Raises
        ------
        `weakref.ReferenceError`
            If no referant was assigned, if it was deleted, or if it was
            de-refenced (e.g. by ``del self.__self__``).
        """
        if hasattr(self, "_self_") and isinstance(self._self_, BoundClassRef):
            boundto = self._self_()  # dereference
            if boundto is not None:
                return boundto

            raise ReferenceError("weakly-referenced object no longer exists")

        raise ReferenceError("no weakly-referenced object")

    @__self__.setter
    def __self__(self, value: BoundToType) -> None:
        # Set the reference.
        self._self_: BoundClassRef[BoundToType] | None
        self._self_ = BoundClassRef(value, bound=self)
        # Note: we use ReferenceType over ProxyType b/c the latter fails ``is``
        # and ``issubclass`` checks. ProxyType autodetects and cleans up
        # deletion of the referent, which ReferenceType does not, so we need a
        # custom BoundClassRef to emulate this behavior.

    @__self__.deleter
    def __self__(self) -> None:
        # Romove reference without deleting the attribute.
        self._self_ = None
