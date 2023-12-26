"""This module defines types to help with supporting omitted values in API types."""

import enum
import typing

__all__: typing.Sequence[str] = ("Undefined", "UndefinedType")


class UndefinedType(enum.Enum):
    """The type of Undefined. Meant for use with isinstance."""

    Undefined = enum.auto()
    """A sentinel value to designate that a field was omitted."""


Undefined: typing.Literal[UndefinedType.Undefined] = UndefinedType.Undefined
"""A sentinel value to designate that a field was omitted."""
