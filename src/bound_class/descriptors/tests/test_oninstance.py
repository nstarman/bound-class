# STDLIB

# THIRD PARTY
import pytest

# LOCAL
from .test_base import BoundDescriptorBase_Test
from bound_class.descriptors import BoundDescriptor


class Test_BoundDescriptor(BoundDescriptorBase_Test):
    @pytest.fixture
    def descriptor_cls(self) -> type:
        return BoundDescriptor

    # ===============================================================

    def test___self___on_cls(self, descriptor_on_cls):
        with pytest.raises(ReferenceError, match="no weakly-referenced object"):
            descriptor_on_cls.__self__

    # -------------------------------------------

    def test___get__from_cls(self, enclosing_cls, enclosing_attr, descriptor_on_cls):
        assert getattr(enclosing_cls, enclosing_attr) is descriptor_on_cls

    def test_descriptor_on_inst_diff_on_cls(descriptor_on_cls, descriptor_on_inst):
        # since it's a copy, it's not the same as the descriptor instance on the class
        assert descriptor_on_inst is not descriptor_on_cls

    def test___get__from_inst(self, descriptor_on_inst, enclosing, enclosing_attr):
        # When get, the first time it is None, so self is copied and added to the dict of the enclosing.
        assert enclosing_attr in enclosing.__dict__
        assert enclosing.__dict__[enclosing_attr] is descriptor_on_inst

    # ===============================================================
    # Usage Tests

    def test_inst_decoupled_from_cls(self, descriptor_on_inst, enclosing_cls, enclosing_attr, enclosing):
        # Setting an attribute on the instance does not effect the class.
        descriptor_on_inst.from_inst = 2
        assert not hasattr(getattr(enclosing_cls, enclosing_attr), "from_inst")

        # And vice versa
        getattr(enclosing_cls, enclosing_attr).from_cls = 2
        assert not hasattr(getattr(enclosing, enclosing_attr), "from_cls")