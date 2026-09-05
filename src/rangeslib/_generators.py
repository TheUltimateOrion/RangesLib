from __future__ import annotations

from ._core import Range, RangeGenerator


class Empty(RangeGenerator):
    """Create an empty integer ``Range``."""

    def __new__(cls) -> Range[int]:
        return Range()


class Single(RangeGenerator):
    """Create a ``Range`` containing one integer value."""

    def __new__(cls, value: int) -> Range[int]:
        return Range(value)


class Iota(RangeGenerator):
    """Create integers from ``start`` up to, but excluding, ``end``."""

    def __new__(cls, start: int, end: int) -> Range[int]:
        return Range(*range(start, end))


class Indices(RangeGenerator):
    """Create zero-based indices from ``0`` up to, but excluding, ``n``."""

    def __new__(cls, n: int) -> Range[int]:
        return Iota(0, n)


class Repeat(RangeGenerator):
    """Create a ``Range`` containing ``n`` copies of a value."""

    def __new__[T](cls, value: T, n: int) -> Range[T]:
        return Range(*[value] * n)
