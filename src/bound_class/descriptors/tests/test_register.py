# STDLIB
from dataclasses import dataclass
from math import sqrt

# LOCAL
from bound_class import register_descriptor
from bound_class.descriptors import BoundDescriptor

# TODO! add registration tests to ``test_base.py`` so that it applies to both
# ``BoundDescriptor`` and ``InstanceDeescriptor``.


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
    assert isinstance(getattr(Vector, "radial"), Radial)

    # test that it works
    v = Vector(3.0, 4.0)
    r = v.radial
    assert r.r == 5.0


def test_register_inst():
    @dataclass
    class Vector:
        x: float
        y: float

    # not yet registered
    assert not hasattr(Vector, "radial")

    class Radial(BoundDescriptor[Vector]):
        @property
        def r(self):
            return sqrt(self.enclosing.x**2 + self.enclosing.y**2)

    radial = Radial()
    register_descriptor(Vector, "radial")(radial)

    assert hasattr(Vector, "radial")
    assert isinstance(getattr(Vector, "radial"), Radial)

    # test that it works
    v = Vector(3.0, 4.0)
    r = v.radial
    assert r.r == 5.0
