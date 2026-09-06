from collections.abc import Iterable
from typing import assert_type

from rangeslib import Range, ranges, views


def stringify(value: int) -> str:
    return str(value)


def as_tuple(values: Iterable[int]) -> tuple[int, ...]:
    return tuple(values)


numbers = ranges.iota(1, 5)
nested = Range(numbers)

assert_type(numbers, Range[int])
assert_type(ranges.single("x"), Range[str])
assert_type(ranges.repeat("x", 2), Range[str])
assert_type([1, 2, 3] | views.all(), Range[int])
assert_type("abc" | views.all(), Range[str])

assert_type(numbers | views.reverse(), Range[int])
assert_type(numbers | views.take(2), Range[int])
assert_type(numbers | views.counted(2), Range[int])
assert_type(numbers | views.enumerate(), Range[tuple[int, int]])
assert_type(numbers | views.adjacent(2), Range[tuple[int, ...]])
assert_type(numbers | views.pairwise(), Range[tuple[int, int]])
assert_type(numbers | views.chunk(2), Range[Range[int]])
assert_type(nested | views.join(), Range[int])
assert_type(numbers | views.transform(stringify), Range[str])
assert_type(numbers | views.to(as_tuple), tuple[int, ...])
assert_type(["a", "b"] | views.to(str), str)
assert_type(numbers | views.zip(["a", "b"]), Range[tuple[int, str]])
assert_type(numbers | views.cartesian_product(["a", "b"]), Range[tuple[int, str]])
assert_type([("a", 1), ("b", 2)] | views.keys(), Range[str])
assert_type([("a", 1), ("b", 2)] | views.values(), Range[int])
