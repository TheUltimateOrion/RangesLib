from __future__ import annotations

from ._core import Range, RangeGenerator


class Empty(RangeGenerator):
    def __new__(cls) -> Range[int]:
        return Range()


class Single(RangeGenerator):
    def __new__(cls, value: int) -> Range[int]:
        return Range(value)


class Iota(RangeGenerator):
    def __new__(cls, start: int, end: int) -> Range[int]:
        return Range(*range(start, end))


class Indices(RangeGenerator):
    def __new__(cls, n: int) -> Range[int]:
        return Iota(0, n)


class Repeat(RangeGenerator):
    def __new__[T](cls, value: T, n: int) -> Range[T]:
        return Range(*[value] * n)
