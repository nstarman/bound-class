# STDLIB
import warnings

# THIRD PARTY
import pytest

# LOCAL
from bound_class.common import DescriptorRegistrationWarning


def test_DescriptorRegistrationWarning():
    """Simple test of ``DescriptorRegistrationWarning``."""
    with pytest.warns(DescriptorRegistrationWarning):
        warnings.warn("test", DescriptorRegistrationWarning)
