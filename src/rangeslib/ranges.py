from __future__ import annotations

from typing import TypeVar

from ._core import Range
from ._generators import Empty, Indices, Iota, Repeat, Single

T = TypeVar("T")


def empty() -> Range[int]:
    """Create an empty range."""
    return Empty()


def single(value: int) -> Range[int]:
    """Create a range containing one integer."""
    return Single(value)


def iota(start: int, end: int) -> Range[int]:
    """Create integers from ``start`` up to, excluding, ``end``."""
    return Iota(start, end)


def indices(count: int) -> Range[int]:
    """Create zero-based indices up to, excluding, ``count``."""
    return Indices(count)


def repeat(value: T, count: int) -> Range[T]:
    """Create a range containing ``count`` copies of ``value``."""
    return Repeat(value, count)


__all__ = ["empty", "single", "iota", "indices", "repeat"]
