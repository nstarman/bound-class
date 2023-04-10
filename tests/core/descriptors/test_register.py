import warnings
from dataclasses import dataclass
from math import sqrt

# THIRD PARTY
import pytest
from bound_class.core import register_descriptor
from bound_class.core.descriptors import BoundDescriptor
from bound_class.core.descriptors.register import DescriptorRegistrationWarning

# TODO! add registration tests to ``test_base.py`` so that it applies to both
# ``BoundDescriptor`` and ``InstanceDeescriptor``.


def test_DescriptorRegistrationWarning():
    """Simple test of ``DescriptorRegistrationWarning``."""
    with pytest.warns(DescriptorRegistrationWarning):
        warnings.warn("test", DescriptorRegistrationWarning, stacklevel=2)


def test_register_cls():
    @dataclass
    class Vector:
        x: float
        y: float

    # not yet registered
    assert not hasattr(Vector, "radial")

    @register_descriptor(Vector, "radial")
    class Radial(BoundDescriptor[Vector]):
        @property
        def r(self):
            return sqrt(self.enclosing.x**2 + self.enclosing.y**2)

    assert hasattr(Vector, "radial")
    assert isinstance(Vector.radial, Radial)

    # test that it works
    v = Vector(3.0, 4.0)
    r = v.radial
    assert r.r == 5.0
