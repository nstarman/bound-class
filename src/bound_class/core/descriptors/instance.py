"""Descriptors only on the instance, not the class."""

##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from dataclasses import dataclass, replace
from typing import Any, MutableMapping, NoReturn, overload

# LOCAL
from bound_class.core.base import BndTo
from bound_class.core.descriptors.base import BoundDescriptorBase

__all__: list[str] = []


##############################################################################
# CODE
##############################################################################


@dataclass
class InstanceDescriptor(BoundDescriptorBase[BndTo]):
    """Descriptor stored on and accessess its enclosing instance.

    Examples
    --------
    Descriptors are constructed within an enclosing class.

        >>> class ExampleInstanceDescriptor(InstanceDescriptor):
        ...     def print_info(self):
        ...         print(f"this is attached to {self.enclosing.name!r}")

        >>> class Example:
        ...     attribute = ExampleInstanceDescriptor()
        ...     def __init__(self, name):
        ...         self.name = name

    `InstanceDescriptor` will work (only) on instances of that class.

        >>> ex = Example("ex_instance")
        >>> ex.attribute
        ExampleInstanceDescriptor(store_in='__dict__')

    What's special about |BoundClass|-derived descriptors is that their
    instances are bound to the instance of the enclosing class, not the class
    itself.

        >>> ex.attribute is vars(Example)["attribute"]
        False

    Consquently :class:`bound_class.descriptors.InstanceDescriptor` can access the
    enclosing instance.

        >>> ex.attribute.enclosing is ex
        True

        >>> ex.attribute.print_info()
        this is attached to 'ex_instance'

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

    This is a data descriptor (see
    https://docs.python.org/3/howto/descriptor.html#descriptor-protocol). When
    ``__get__`` is first called it will make a copy of this descriptor instance
    and place it in the enclosing object's ``__dict__``. Thereafter attribute
    access will return the instance in ``__dict__``, first passing through this
    descriptor to make sure references are kept up-to-date.
    """

    @overload
    def __get__(self: InstanceDescriptor[BndTo], enclosing: BndTo, enclosing_cls: None) -> InstanceDescriptor[BndTo]:
        ...

    @overload
    def __get__(self: InstanceDescriptor[BndTo], enclosing: None, enclosing_cls: type[BndTo]) -> NoReturn:
        ...

    def __get__(
        self: InstanceDescriptor[BndTo],
        enclosing: BndTo | None,
        enclosing_cls: type[BndTo] | None,
    ) -> InstanceDescriptor[BndTo] | NoReturn:
        """Return a copy of this descriptor bound to the enclosing object.

        Parameters
        ----------
        enclosing : BndTo | None
            The object this descriptor is being accessed from. If ``None`` then
            this is being accessed from the class, not an instance.
        enclosing_cls : type[BndTo] | None
            The class this descriptor is being accessed from. If ``None`` then
            this is being accessed from an instance, not the class.

        Returns
        -------
        InstanceDescriptor[BndTo]
            A copy of this descriptor bound to the enclosing object.

        Raises
        ------
        AttributeError
            If ``enclosing`` is ``None``.
        TypeError
            If the descriptor stored on the enclosing object is not of the same
            type as this descriptor.
        """
        # When called without an instance, return self to allow access
        # to descriptor attributes.
        if enclosing is None:
            msg = f"{self._enclosing_attr!r} can only be accessed from " + (
                "its enclosing object." if enclosing_cls is None else f"a {enclosing_cls.__name__!r} object"
            )
            raise AttributeError(msg)

        # accessed from an enclosing
        if self.store_in is None:
            dsc = replace(self)
        else:  # try to get from cache
            cache: MutableMapping[str, Any] = getattr(enclosing, self.store_in)
            obj = cache.get(self._enclosing_attr)  # get from enclosing.

            if obj is None:  # hasn't been created on the enclosing
                dsc = replace(self)
                # transfer any other information
                dsc.__set_name__(dsc, self._enclosing_attr)
                # store on enclosing instance
                cache[self._enclosing_attr] = dsc
            elif not isinstance(obj, type(self)):
                msg = f"descriptor must be type <{type(self)}> not <{type(obj)}>"
                raise TypeError(msg)
            else:  # noqa: RET506
                dsc = obj

        # We set `__self__` on every call, since if one makes copies of objs,
        # 'dsc' will be copied as well, which will lose the reference.
        dsc._set__self__(enclosing)
        # TODO? is it faster to check the reference then always make a new one.

        return dsc
