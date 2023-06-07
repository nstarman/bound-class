"""Common utilities for the bound-class package."""

from __future__ import annotations

__all__: list[str] = []


# TODO: move this to a better file
class DescriptorRegistrationWarning(Warning):
    """Warning for conflicts in descriptor registration."""
