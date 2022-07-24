# STDLIB
from abc import ABCMeta, abstractmethod

# THIRD PARTY
import pytest

# LOCAL
from bound_class.descriptors.base import BoundDescriptorBase


class BoundDescriptorBase_Test(metaclass=ABCMeta):
    @pytest.fixture
    @abstractmethod
    def descriptor_cls(self) -> type:
        return BoundDescriptorBase

    @pytest.fixture
    def enclosing_attr(self) -> str:
        return "attr"

    @pytest.fixture
    def enclosing_cls(self, descriptor_cls, enclosing_attr) -> type:
        Enclosing = type("Enclosing", (object,), {enclosing_attr: descriptor_cls()})

        return Enclosing

    @pytest.fixture
    def descriptor_on_cls(self, enclosing_cls, enclosing_attr) -> object:
        return vars(enclosing_cls)[enclosing_attr]

    @pytest.fixture
    def enclosing(self, enclosing_cls) -> object:
        return enclosing_cls()

    @pytest.fixture
    def descriptor_on_inst(self, enclosing, enclosing_attr) -> object:
        return getattr(enclosing, enclosing_attr)

    # ===============================================================

    def test_enclosing_attr_on_cls(self, descriptor_cls):
        with pytest.raises(AttributeError):
            descriptor_cls._enclosing_attr

    def test_enclosing_attr_on_inst(self, descriptor_on_inst, enclosing_attr):
        # This tests that __set_name__ was called
        assert descriptor_on_inst._enclosing_attr == enclosing_attr

    # -------------------------------------------

    def test_replace(self, descriptor_on_inst):
        newdescriptor = descriptor_on_inst._replace()

        assert newdescriptor is not descriptor_on_inst
        assert newdescriptor == descriptor_on_inst
