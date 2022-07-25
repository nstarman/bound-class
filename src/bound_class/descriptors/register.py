# TODO! rename this file

from __future__ import annotations

# STDLIB
import inspect
import warnings
from dataclasses import replace
from typing import Any, Callable

# LOCAL
from .base import BndTo, BoundDescriptorBase
from bound_class.common import DescriptorRegistrationWarning

__all__ = ["register_descriptor"]


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
    First we import

        >>> from dataclasses import dataclass
        >>> import numpy as np
        >>> from bound_class.descriptors import InstanceDescriptor, register_descriptor

    The primary class.

        >>> @dataclass
        ... class Vector:
        ...     x: float
        ...     y: float
        ...     z: float

    Add a descriptor.

        >>> @register_descriptor(Vector, "spherical")
        ... class Spherical(InstanceDescriptor):
        ...
        ...     @property
        ...     def r(self):
        ...         return np.sqrt(self.enclosing.x**2 + self.enclosing.y**2 + self.enclosing.z**2)

        >>> v = Vector(1.0, 2.0, 3.0)
        >>> v.spherical.r
        5.0
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
