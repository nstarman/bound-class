"""Descriptors only on the instance, not the class."""

##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import NoReturn, overload

# LOCAL
from .base import BndTo, BoundDescriptorBase

# from typing_extensions import Self  # TODO! use when mypy doesn't complain

__all__ = ["InstanceDescriptor"]


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
        ExampleInstanceDescriptor()

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
    def __get__(self, enclosing: None, enclosing_cls: type[BndTo]) -> NoReturn:
        ...

    def __get__(
        self: InstanceDescriptor[BndTo],
        enclosing: BndTo | None,
        enclosing_cls: type[BndTo] | None,
    ) -> InstanceDescriptor[BndTo] | NoReturn:
        # When called without an instance, return self to allow access
        # to descriptor attributes.
        if enclosing is None:
            msg = f"{self._enclosing_attr!r} can only be accessed from " + (
                "its enclosing object." if enclosing_cls is None else f"a {enclosing_cls.__name__!r} object"
            )
            raise AttributeError(msg)

        # accessed from an enclosing
        # TODO! support if enclosing has slots
        descriptor = enclosing.__dict__.get(self._enclosing_attr)  # get from enclosing
        if descriptor is None:  # hasn't been created on the enclosing
            descriptor = self._replace()
            # transfer any other information
            descriptor.__set_name__(descriptor, self._enclosing_attr)
            # store on enclosing instance
            enclosing.__dict__[self._enclosing_attr] = descriptor

        # We set `__self__` on every call, since if one makes copies of objs,
        # 'descriptor' will be copied as well, which will lose the reference.
        descriptor.__self__ = enclosing
        # TODO? is it faster to check the reference then always make a new one.

        return descriptor
