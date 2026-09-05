import unittest
from collections.abc import Iterable

import rangeslib
from rangeslib import Range, ranges, views
from rangeslib._adaptors import (
    Adjacent,
    AdjacentTransform,
    CartesianProduct,
    Chunk,
    ChunkBy,
    Concat,
    Counted,
    Drop,
    DropWhile,
    Elements,
    Enumerate,
    Filter,
    Join,
    JoinWith,
    Keys,
    Reverse,
    Pairwise,
    PairwiseTransform,
    Slide,
    Split,
    Stride,
    Take,
    TakeWhile,
    To,
    Transform,
    Values,
    Zip,
    ZipTransform,
)
from rangeslib._core import RangeAdaptor, RangeGenerator
from rangeslib._generators import Empty, Indices, Iota, Repeat, Single


def is_positive(value: int) -> bool:
    return value > 0


def is_even(value: int) -> bool:
    return value % 2 == 0


def is_less_than_three(value: int) -> bool:
    return value < 3


def is_greater_than_one(value: int) -> bool:
    return value > 1


def times_ten(value: int) -> int:
    return value * 10


def to_range(value: int) -> range:
    return range(value)


def add_values(left: int, right: int) -> int:
    return left + right


def are_consecutive(left: int, right: int) -> bool:
    return right - left == 1


def join_strings(iterable: Iterable[str]) -> str:
    return ":".join(iterable)


class RangeTests(unittest.TestCase):
    def test_range_construction_and_display(self) -> None:
        values = Range(1, "two", 3)

        self.assertEqual(list(values), [1, "two", 3])
        self.assertEqual(repr(values), "Range(1, 'two', 3)")
        self.assertEqual(str(values), "[1, two, 3]")
        self.assertEqual(len(values), 3)

    def test_empty_and_is_empty(self) -> None:
        values = Empty()

        self.assertIsInstance(values, Range)
        self.assertTrue(values.is_empty())
        self.assertEqual(len(values), 0)

        values.append(1)
        self.assertFalse(values.is_empty())

    def test_range_factories(self) -> None:
        self.assertEqual(list(Single(1)), [1])
        self.assertEqual(list(Iota(2, 6)), [2, 3, 4, 5])
        self.assertEqual(list(Iota(4, 2)), [])
        self.assertEqual(list(Indices(4)), [0, 1, 2, 3])
        self.assertEqual(list(Indices(0)), [])
        self.assertEqual(list(Repeat("x", 3)), ["x", "x", "x"])
        self.assertEqual(list(Repeat("x", 0)), [])

    def test_all_range_generators_share_the_base_type(self) -> None:
        generators: list[type[RangeGenerator]] = [Empty, Single, Iota, Indices, Repeat]

        for generator in generators:
            with self.subTest(generator=generator):
                self.assertIn(RangeGenerator, generator.__mro__)


class RangeAdaptorTests(unittest.TestCase):
    def test_all_adaptors_share_the_base_type(self) -> None:
        self.assertIsInstance(To(list), RangeAdaptor)
        self.assertIsInstance(Reverse[int](), RangeAdaptor)
        self.assertIsInstance(Filter(is_positive), RangeAdaptor)
        self.assertIsInstance(Transform(str), RangeAdaptor)
        self.assertIsInstance(Take[int](1), RangeAdaptor)
        self.assertIsInstance(TakeWhile(is_positive), RangeAdaptor)
        self.assertIsInstance(Drop[int](1), RangeAdaptor)
        self.assertIsInstance(DropWhile(is_positive), RangeAdaptor)
        self.assertIsInstance(Counted[int](1), RangeAdaptor)
        self.assertIsInstance(Elements[str](0), RangeAdaptor)
        self.assertIsInstance(Keys[str](), RangeAdaptor)
        self.assertIsInstance(Values[int](), RangeAdaptor)
        self.assertIsInstance(Enumerate[int](), RangeAdaptor)
        self.assertIsInstance(Concat[int](), RangeAdaptor)
        self.assertIsInstance(Zip[int]([1]), RangeAdaptor)
        self.assertIsInstance(ZipTransform[int](add_values, [1]), RangeAdaptor)
        self.assertIsInstance(Adjacent[int](), RangeAdaptor)
        self.assertIsInstance(Pairwise[int](), RangeAdaptor)
        self.assertIsInstance(AdjacentTransform[int, int](add_values), RangeAdaptor)
        self.assertIsInstance(PairwiseTransform[int, int](add_values), RangeAdaptor)
        self.assertIsInstance(Chunk[int](1), RangeAdaptor)
        self.assertIsInstance(Slide[int](1), RangeAdaptor)
        self.assertIsInstance(ChunkBy[int](are_consecutive), RangeAdaptor)
        self.assertIsInstance(Stride[int](1), RangeAdaptor)
        self.assertIsInstance(CartesianProduct[int]([1]), RangeAdaptor)
        self.assertIsInstance(Join[int](), RangeAdaptor)
        self.assertIsInstance(JoinWith[int]([0]), RangeAdaptor)
        self.assertIsInstance(Split[int]([0]), RangeAdaptor)

    def test_reverse_accepts_a_normal_iterable(self) -> None:
        result: Range[int] = Reverse[int]()((value for value in [1, 2, 3]))

        self.assertEqual(list(result), [3, 2, 1])
        self.assertIsInstance(result, Range)

    def test_normal_iterables_support_pipe_syntax(self) -> None:
        result = "abcd" | Filter[str](lambda value: value != "b") | Take[str](2)

        self.assertEqual(list(result), ["a", "c"])

        range_result = range(4) | Transform[int, int](times_ten)
        self.assertEqual(list(range_result), [0, 10, 20, 30])

    def test_filter_accepts_a_normal_iterable(self) -> None:
        result = Filter(is_even)([1, 2, 3, 4])

        self.assertEqual(list(result), [2, 4])

    def test_transform_changes_element_type(self) -> None:
        result = Transform(str)([1, 2, 3])

        self.assertEqual(list(result), ["1", "2", "3"])
        self.assertIsInstance(result, Range)

    def test_take_and_drop(self) -> None:
        values: list[int] = [1, 2, 3, 4]

        self.assertEqual(list(Take[int](2)(values)), [1, 2])
        self.assertEqual(list(Take[int](0)(values)), [])
        self.assertEqual(list(Take[int](-1)(values)), [1, 2, 3])
        self.assertEqual(list(Drop[int](2)(values)), [3, 4])
        self.assertEqual(list(Drop[int](0)(values)), values)
        self.assertEqual(list(Drop[int](-1)(values)), [4])

    def test_to_converts_to_the_requested_type(self) -> None:
        values = Range(1, 2, 2, 3)

        self.assertEqual(To(list)(values), [1, 2, 2, 3])
        self.assertEqual(To(tuple)(values), (1, 2, 2, 3))
        self.assertEqual(To(set)(values), {1, 2, 3})

    def test_take_while_and_drop_while_accept_normal_iterables(self) -> None:
        take_result: Range[int] = TakeWhile(is_less_than_three)([1, 2, 3, 2])
        drop_result: Range[int] = DropWhile(is_less_than_three)([1, 2, 3, 2])

        self.assertEqual(list(take_result), [1, 2])
        self.assertEqual(list(drop_result), [3, 2])

    def test_counted_takes_from_a_one_shot_iterable(self) -> None:
        result: Range[int] = Counted[int](2)(value for value in [1, 2, 3])

        self.assertEqual(list(result), [1, 2])
        with self.assertRaises(ValueError):
            Counted(-1)

    def test_elements_keys_and_values_project_pairs(self) -> None:
        pairs = [("a", 1), ("b", 2)]

        self.assertEqual(list(Elements[str](0)(pairs)), ["a", "b"])
        self.assertEqual(list(Keys[str]()(pairs)), ["a", "b"])
        self.assertEqual(list(Values[int]()(pairs)), [1, 2])

    def test_enumerate_supports_a_start_value(self) -> None:
        result: Range[tuple[int, str]] = Enumerate[str](5)(["a", "b"])

        self.assertEqual(list(result), [(5, "a"), (6, "b")])

    def test_concat_appends_iterables(self) -> None:
        result = Concat((3, 4), (value for value in [5, 6]))([1, 2])

        self.assertEqual(list(result), [1, 2, 3, 4, 5, 6])

    def test_zip_stops_at_the_shortest_iterable(self) -> None:
        result = Zip[int]([10, 20])([1, 2, 3])

        self.assertEqual(list(result), [(1, 10), (2, 20)])

    def test_zip_transform_applies_to_corresponding_values(self) -> None:
        result = ZipTransform[int](add_values, [10, 20, 30])([1, 2])

        self.assertEqual(list(result), [11, 22])

    def test_adjacent_and_pairwise_create_overlapping_windows(self) -> None:
        self.assertEqual(list(Adjacent[int](3)([1, 2, 3, 4])), [(1, 2, 3), (2, 3, 4)])
        self.assertEqual(list(Pairwise[int]()(range(3))), [(0, 1), (1, 2)])

    def test_adjacent_transform_and_pairwise_transform(self) -> None:
        self.assertEqual(
            list(AdjacentTransform[int, int](add_values)([1, 2, 3])), [3, 5]
        )
        self.assertEqual(
            list(PairwiseTransform[int, int](add_values)([1, 2, 3])), [3, 5]
        )

    def test_chunk_and_slide(self) -> None:
        self.assertEqual(
            [list(chunk) for chunk in Chunk[int](2)([1, 2, 3, 4, 5])],
            [[1, 2], [3, 4], [5]],
        )
        self.assertEqual(
            [list(window) for window in Slide[int](3)([1, 2, 3, 4])],
            [[1, 2, 3], [2, 3, 4]],
        )

    def test_chunk_by_and_stride(self) -> None:
        chunks = ChunkBy[int](are_consecutive)([1, 2, 4, 5, 8])

        self.assertEqual([list(chunk) for chunk in chunks], [[1, 2], [4, 5], [8]])
        self.assertEqual(list(Stride[int](2)(range(6))), [0, 2, 4])

    def test_cartesian_product(self) -> None:
        result = CartesianProduct[int]([10, 20])([1, 2])

        self.assertEqual(list(result), [(1, 10), (1, 20), (2, 10), (2, 20)])

    def test_join_accepts_an_iterable_of_iterables(self) -> None:
        nested_values: Iterable[Iterable[int]] = iter([[1, 2], (3,), range(4, 6)])

        self.assertEqual(list(Join[int]()(nested_values)), [1, 2, 3, 4, 5])

    def test_join_with_inserts_a_pattern_between_iterables(self) -> None:
        nested_values: Iterable[Iterable[int]] = iter([[1, 2], (3,), range(4, 6)])

        self.assertEqual(
            list(JoinWith[int]([0, 0])(nested_values)),
            [1, 2, 0, 0, 3, 0, 0, 4, 5],
        )

    def test_split_accepts_a_pattern_and_preserves_empty_chunks(self) -> None:
        result = Split([0, 0])([1, 2, 0, 0, 3, 0, 0])

        self.assertEqual([list(chunk) for chunk in result], [[1, 2], [3], []])

    def test_split_rejects_an_empty_pattern(self) -> None:
        with self.assertRaises(ValueError):
            Split([])([1, 2, 3])

    def test_join_works_in_a_pipeline(self) -> None:
        nested_values: Range[range] = Transform[int, range](to_range)(Iota(1, 4))
        result: Range[int] = Join[int]()(nested_values)

        self.assertEqual(list(result), [0, 0, 1, 0, 1, 2])

    def test_to_supports_a_custom_factory(self) -> None:
        result = To(join_strings)(["a", "b", "c"])

        self.assertEqual(result, "a:b:c")

    def test_pipeline_composes_adaptors(self) -> None:
        result: Range[int] = (
            Iota(1, 7)
            | Reverse()
            | Filter[int](is_even)
            | Transform[int, int](times_ten)
            | Take[int](2)
        )

        self.assertEqual(list(result), [60, 40])

    def test_pipeline_can_finish_with_to(self) -> None:
        result = Iota(1, 4) | Filter(is_greater_than_one) | To(tuple)

        self.assertEqual(result, (2, 3))
        self.assertIsInstance(result, tuple)


class PublicNamespaceTests(unittest.TestCase):
    def test_lowercase_facade_composes_without_generic_parameters(self) -> None:
        result = (
            ranges.iota(1, 6)
            | views.filter(is_even)
            | views.transform(times_ten)
            | views.take(2)
            | views.to(list)
        )

        self.assertEqual(result, [20, 40])
        self.assertEqual(list("abc" | views.take(2)), ["a", "b"])

    def test_package_exposes_only_the_clean_facade(self) -> None:
        self.assertEqual(
            set(vars(rangeslib)) & {"Ranges", "Filter", "Iota", "Take"}, set()
        )
        self.assertIs(ranges.iota(1, 3).__class__, Range)
        self.assertEqual(list(views.take(2)([1, 2, 3])), [1, 2])


if __name__ == "__main__":
    unittest.main()
