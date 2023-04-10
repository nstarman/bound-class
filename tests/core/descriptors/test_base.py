from abc import ABCMeta, abstractmethod
from dataclasses import replace

# THIRD PARTY
import pytest
from bound_class.core.descriptors.base import BoundDescriptorBase


class BoundDescriptorBase_Test(metaclass=ABCMeta):
    @pytest.fixture()
    @abstractmethod
    def descr_cls(self) -> type:
        return BoundDescriptorBase

    @pytest.fixture()
    def encl_attr(self) -> str:
        return "attr"

    @pytest.fixture()
    def encl_cls(self, descr_cls, encl_attr) -> type:
        return type("Enclosing", (object,), {encl_attr: descr_cls()})

    @pytest.fixture()
    def descr_on_cls(self, encl_cls, encl_attr) -> object:
        return vars(encl_cls)[encl_attr]

    @pytest.fixture()
    def enclosing(self, encl_cls) -> object:
        return encl_cls()

    @pytest.fixture()
    def descr_on_inst(self, enclosing, encl_attr) -> object:
        return getattr(enclosing, encl_attr)

    # ===============================================================

    def test_encl_attr_on_cls(self, descr_cls):
        with pytest.raises(AttributeError):
            descr_cls._enclosing_attr  # noqa: B018

    def test_encl_attr_on_inst(self, descr_on_inst, encl_attr):
        # This tests that __set_name__ was called on the new instance
        assert descr_on_inst._enclosing_attr == encl_attr

    # -------------------------------------------
    # Test __get__

    def test_descr_on_inst_diff_on_cls(descriptor_on_cls, descr_on_inst):
        # since it's a copy, it's not the same as the descriptor instance on the class
        assert descr_on_inst is not descriptor_on_cls

    def test___get__from_inst(self, descr_on_inst, enclosing, encl_attr):
        # When get, the first time it is None, so self is copied and added to the dict of the enclosing.
        assert encl_attr in enclosing.__dict__
        assert enclosing.__dict__[encl_attr] is descr_on_inst

    # -------------------------------------------

    def test_enclosing(self, descr_on_inst, enclosing):
        """Test property ``enclosing``."""
        assert descr_on_inst.enclosing is enclosing

    # -------------------------------------------

    def test_replace(self, descr_on_inst):
        """Test ``replace(descriptor)``."""
        newdescriptor = replace(descr_on_inst)

        assert newdescriptor is not descr_on_inst  # copy
        assert newdescriptor == descr_on_inst  # is equal

    # ===============================================================

    def can_test_membership(self, encl_cls, encl_attr):
        """Can test that a descriptor is on the class."""
        hasattr(encl_cls, encl_attr)
