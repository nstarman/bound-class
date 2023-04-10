# THIRD PARTY
import pytest
from bound_class.core.descriptors import InstanceDescriptor

from .test_base import BoundDescriptorBase_Test


class Test_InstanceDescriptor(BoundDescriptorBase_Test):
    @pytest.fixture()
    def descr_cls(self) -> type:
        return InstanceDescriptor

    # ===============================================================

    def test___self___on_cls(self, descr_on_cls):
        with pytest.raises(ReferenceError, match="no weakly-referenced object"):
            descr_on_cls.__self__  # noqa: B018

    # -------------------------------------------

    def test___get__from_cls(self, encl_cls, encl_attr):
        msg = f"{encl_attr!r} can only be accessed from a {encl_cls.__name__!r} object"
        with pytest.raises(AttributeError, match=msg):
            getattr(encl_cls, encl_attr)

    # ===============================================================
    # Usage Tests

    def test_inst_decoupled_from_cls(self, descr_on_inst, encl_cls, encl_attr, enclosing):
        # Setting an attribute on the instance does not effect the class.
        descr_on_inst.from_inst = 2
        assert not hasattr(vars(encl_cls)[encl_attr], "from_inst")

        # And vice versa
        vars(encl_cls)[encl_attr].from_cls = 2
        assert not hasattr(getattr(enclosing, encl_attr), "from_cls")
