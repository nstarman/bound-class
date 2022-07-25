# STDLIB

# THIRD PARTY
import pytest

# LOCAL
from .test_base import BoundDescriptorBase_Test
from bound_class.descriptors import BoundDescriptor


class Test_BoundDescriptor(BoundDescriptorBase_Test):
    @pytest.fixture
    def descr_cls(self) -> type:
        return BoundDescriptor

    # ===============================================================

    def test___self___on_cls(self, descr_on_cls):
        with pytest.raises(ReferenceError, match="no weakly-referenced object"):
            descr_on_cls.__self__

    # -------------------------------------------

    def test___get__from_cls(self, encl_cls, encl_attr, descr_on_cls):
        assert getattr(encl_cls, encl_attr) is descr_on_cls

    # ===============================================================
    # Usage Tests

    def test_inst_decoupled_from_cls(self, descr_on_inst, encl_cls, encl_attr, enclosing):
        # Setting an attribute on the instance does not effect the class.
        descr_on_inst.from_inst = 2
        assert not hasattr(getattr(encl_cls, encl_attr), "from_inst")

        # And vice versa
        getattr(encl_cls, encl_attr).from_cls = 2
        assert not hasattr(getattr(enclosing, encl_attr), "from_cls")
