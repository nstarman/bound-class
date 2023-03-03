from weakref import ReferenceType

# THIRD PARTY
import pytest

# LOCAL
from bound_class.core.base import BoundClass, BoundClassRef

#####################################################################


@pytest.fixture()
def bound_cls() -> type:
    return BoundClass


@pytest.fixture()
def boundto_cls() -> type:
    return type("Enclosing", (object,), {})


@pytest.fixture()
def boundto(boundto_cls) -> object:
    return boundto_cls()


@pytest.fixture()
def unbound(bound_cls) -> object:
    return bound_cls()


@pytest.fixture()
def bound(bound_cls, boundto) -> object:
    bound = bound_cls()  # TODO? necessary
    bound._set__self__(boundto)
    return bound


#####################################################################
# Test_BoundClass:


def test_boundto_connection(unbound):
    """Test connection from ``bound`` to ``boundto``.

    B/c this is the base, bound is not yet connected to boundto.
    """
    assert not hasattr(unbound, "__selfref__")

    with pytest.raises(ReferenceError, match="no weakly-referenced object"):
        unbound.__self__


def test_set_connection(unbound, boundto):
    # test no current connection
    with pytest.raises(ReferenceError, match="no weakly-referenced object"):
        unbound.__self__

    # Set connection
    unbound._set__self__(boundto)

    # Test new connection
    assert unbound.__self__ is boundto
    assert isinstance(unbound.__selfref__, BoundClassRef)
    assert isinstance(unbound.__selfref__._bound_ref, ReferenceType)
    assert unbound.__selfref__._bound_ref() is unbound


def test_delete_connection(unbound, boundto):
    # Make bond
    unbound._set__self__(boundto)
    assert unbound.__self__ is boundto  # ensure connected

    # Delete and test
    unbound._del__self__()

    with pytest.raises(ReferenceError, match="no weakly-referenced object"):
        unbound.__self__

    assert unbound.__selfref__ is None


def test_boundto_deleted(unbound, boundto_cls):
    # need to make here for proper garbage collection
    boundto = boundto_cls()

    # Make bond
    unbound._set__self__(boundto)
    assert unbound.__self__ is boundto  # ensure connected

    # Delete and test
    del boundto

    with pytest.raises(ReferenceError, match="no weakly-referenced object"):
        unbound.__self__

    assert unbound.__selfref__ is None


def test_bound_not_alive_from_reference(bound_cls, boundto):
    """
    A bound-class holds a reference to the referent. The reference itself holds
    a reference to the bound-class so that if the referent is deleted, the
    attribution on the bound class is cleaned up. This tests that the cleanup
    works as.
    """
    # need to make here for proper garbage collection
    bound = bound_cls()
    bound._set__self__(boundto)

    boundref = bound.__selfref__  # stays alive
    assert isinstance(boundref, BoundClassRef)
    assert isinstance(boundref._bound_ref, ReferenceType)
    assert boundref._bound_ref() is bound

    del bound

    with pytest.raises(UnboundLocalError):  # garbage collected
        bound

    assert boundref._bound_ref() is None
