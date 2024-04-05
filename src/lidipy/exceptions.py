"""Exceptions module for the Lidi framework.

Defines custom exceptions used within the Lidi framework.
"""


class BaseLidiException(Exception):  # noqa: N818
    """Base class for all Lidi exceptions."""

    ...


class BindingMissing(BaseLidiException):
    """Raise when binding is not found within Lidi container."""

    pass
