from __future__ import annotations

from ._core import Range
from ._generators import Empty, Indices, Iota, Repeat, Single


def empty() -> Range[int]:
    """Create an empty integer range."""
    return Empty()


def single[T](value: T) -> Range[T]:
    """Create a range containing exactly ``value``."""
    return Single(value)


def iota(start: int, end: int) -> Range[int]:
    """Create integers from ``start`` up to, but excluding, ``end``."""
    return Iota(start, end)


def indices(count: int) -> Range[int]:
    """Create zero-based indices up to, but excluding, ``count``."""
    return Indices(count)


def repeat[T](value: T, count: int) -> Range[T]:
    """Create a range containing ``count`` copies of ``value``."""
    return Repeat(value, count)


__all__ = ["empty", "single", "iota", "indices", "repeat"]
