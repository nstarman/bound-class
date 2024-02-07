"""Configure Test Suite.

This file is used to configure the behavior of pytest when using the Astropy
test infrastructure. It needs to live inside the package in order for it to
get picked up when running the tests inside an interpreter using
packagename.test

"""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from pytest_astropy_header.display import PYTEST_HEADER_MODULES, TESTED_VERSIONS

if TYPE_CHECKING:
    import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Configure Pytest with Astropy.

    Parameters
    ----------
    config : `pytest.Config`
        Pytest configuration.

    """
    config.option.astropy_header = True

    # Customize the following lines to add/remove entries from the list of
    # packages for which version numbers are displayed when running the
    # tests.
    PYTEST_HEADER_MODULES.pop("Pandas", None)

    from importlib.metadata import version

    packagename = pathlib.Path(__file__).parent.name
    TESTED_VERSIONS[packagename] = version("bound_class." + packagename)
