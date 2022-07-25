from __future__ import annotations

# STDLIB
import inspect
import warnings
from dataclasses import replace
from typing import Any, Callable

# LOCAL
from .base import BndTo, BoundDescriptorBase
from bound_class.common import DescriptorRegistrationWarning

__all__: list[str] = []


def register_descriptor(
    cls: type[BndTo], name: str, **kwargs: Any
) -> Callable[
    [BoundDescriptorBase[BndTo] | type[BoundDescriptorBase[BndTo]]],
    BoundDescriptorBase[BndTo] | type[BoundDescriptorBase[BndTo]],
]:
    """Decorator to register a descriptor -- class or instance.

    Parameters
    ----------
    cls : type[BndTo]
        The class to which to add the descriptor.
    name : str
        The name of the descriptor on `cls`.
    **kwargs : Any
        Arguments passed to

    Examples
    --------
    First the basic imports:

        >>> from dataclasses import dataclass
        >>> from math import atan2, sqrt

    Descriptors are attached to a primary class. Here, we have a 2D vector in
    Cartesian coordinates.

        >>> @dataclass
        ... class Cartesian:
        ...     x: float
        ...     y: float

    With descriptors we can work with the vector in other coordinate systems:

        >>> from bound_class.descriptors import InstanceDescriptor, register_descriptor
        >>> @register_descriptor(Cartesian, "spherical")
        ... class SphericalDescriptor(InstanceDescriptor):
        ...
        ...     @property
        ...     def r(self):
        ...         return sqrt(self.enclosing.x**2 + self.enclosing.y**2)
        ...     @property
        ...     def theta(self):
        ...         return atan2(self.enclosing.y, self.enclosing.x)

        >>> v = Cartesian(3.0, 4.0)
        >>> v.spherical.r
        5.0
        >>> v.spherical.theta  # doctest: +FLOAT_CMP
        0.92729
    """

    def decorator(
        descriptor: BoundDescriptorBase[BndTo] | type[BoundDescriptorBase[BndTo]],
    ) -> BoundDescriptorBase[BndTo] | type[BoundDescriptorBase[BndTo]]:
        """Set the descriptor on the class.

        Parameters
        ----------
        descriptor : type[BoundClass[BndTo]]
            The descriptor to set on the class.

        Returns
        -------
        type[BoundClass[BndTo]]
            The descriptor object.

        Raises
        ------
        ValueError
            If the descriptor is not a `bound_class.descriptors.base.BoundDescriptorBase`
        """
        if hasattr(cls, name):
            warnings.warn(
                f"registration of descriptor {descriptor!r} under name {name!r} for "
                f"type {cls!r} is overriding an attribute of the same name.",
                DescriptorRegistrationWarning,
                stacklevel=2,
            )

        # Make the descriptor instance: instantiate class or make copy
        if inspect.isclass(descriptor):
            if not issubclass(descriptor, BoundDescriptorBase):
                raise ValueError  # TODO! error message

            # correctly parse args vs kwargs
            sig = inspect.signature(descriptor.__init__)
            ba = sig.bind_partial(None, **kwargs)  # None -> self in unbound __init__

            descr = descriptor(*ba.args[1:], **ba.kwargs)  # make instance (skip 'self=None')

        else:
            if not isinstance(descriptor, BoundDescriptorBase):
                raise ValueError  # TODO! error message

            descr = replace(descriptor, **kwargs)  # TODO! use ``_replace`` method

        # Set the descriptor on the class.
        descr.__set_name__(descr, name)  # descriptor callback
        setattr(cls, name, descr)  # attach to class

        return descriptor

    return decorator
