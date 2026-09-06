import itertools
import unittest
from collections.abc import Callable

import rangeslib
from rangeslib import Range, ranges, views


def is_even(value: int) -> bool:
    return value % 2 == 0


def is_less_than_three(value: int) -> bool:
    return value < 3


def add_values(left: int, right: int) -> int:
    return left + right


def multiply_values(left: int, right: int) -> int:
    return left * right


def are_consecutive(left: int, right: int) -> bool:
    return right - left == 1


def is_odd(value: int) -> bool:
    return value % 2 == 1


def times_ten(value: int) -> int:
    return value * 10


def is_small(value: int) -> bool:
    return value < 10


class PublicGeneratorTests(unittest.TestCase):
    def test_all_generators_are_available_through_ranges(self) -> None:
        self.assertEqual(list(ranges.empty()), [])
        self.assertEqual(list(ranges.single("value")), ["value"])
        self.assertEqual(list(ranges.iota(2, 5)), [2, 3, 4])
        self.assertEqual(list(ranges.indices(3)), [0, 1, 2])
        self.assertEqual(list(ranges.repeat("x", 3)), ["x", "x", "x"])

    def test_views_all_materializes_existing_iterables(self) -> None:
        self.assertEqual(list([1, 2, 3] | views.all()), [1, 2, 3])
        self.assertEqual(
            list("abcdefg" | views.all()), ["a", "b", "c", "d", "e", "f", "g"]
        )
        self.assertEqual(list(("a", "b") | views.all()), ["a", "b"])
        self.assertEqual(set({1, 2, 3} | views.all()), {1, 2, 3})
        source = iter([1, 2, 3])
        values = views.all()(source)

        self.assertEqual(list(values), [1, 2, 3])
        self.assertEqual(list(values), [1, 2, 3])
        with self.assertRaises(StopIteration):
            next(source)

    def test_adaptors_can_be_composed_and_reused(self) -> None:
        pipeline = views.filter(is_even) | views.take(3)

        self.assertEqual(list([1, 2, 3, 4, 5, 6, 8] | pipeline), [2, 4, 6])
        self.assertEqual(list([10, 11, 12, 14] | pipeline), [10, 12, 14])

    def test_composed_adaptor_reuses_captured_one_shot_iterables_once(self) -> None:
        suffix = iter([3, 4])
        pipeline = views.concat(suffix) | views.take(3)

        self.assertEqual(list([1, 2] | pipeline), [1, 2, 3])
        self.assertEqual(list([1, 2] | pipeline), [1, 2])

    def test_non_positive_generator_counts_follow_builtin_range_and_list_rules(
        self,
    ) -> None:
        self.assertEqual(list(ranges.indices(-2)), [])
        self.assertEqual(list(ranges.repeat("x", -2)), [])
        self.assertEqual(list(ranges.iota(5, 2)), [])


class PublicViewTests(unittest.TestCase):
    def test_value_processing_views(self) -> None:
        values = [1, 2, 3, 4]

        self.assertEqual(list(views.reverse()(values)), [4, 3, 2, 1])
        self.assertEqual(list(views.filter(is_even)(values)), [2, 4])
        self.assertEqual(list(views.transform(str)(values)), ["1", "2", "3", "4"])
        self.assertEqual(list(views.take(2)(values)), [1, 2])
        self.assertEqual(list(views.take(-1)(values)), [1, 2, 3])
        self.assertEqual(list(views.drop(2)(values)), [3, 4])
        self.assertEqual(list(views.drop(-1)(values)), [4])
        self.assertEqual(list(views.takewhile(is_less_than_three)(values)), [1, 2])
        self.assertEqual(list(views.take_while(is_less_than_three)(values)), [1, 2])
        self.assertEqual(list(views.dropwhile(is_less_than_three)(values)), [3, 4])
        self.assertEqual(list(views.drop_while(is_less_than_three)(values)), [3, 4])

    def test_bounded_take_and_counted_leave_a_one_shot_iterator_positioned(
        self,
    ) -> None:
        take_source = iter([1, 2, 3, 4])
        counted_source = iter([1, 2, 3, 4])

        self.assertEqual(list(views.take(2)(take_source)), [1, 2])
        self.assertEqual(next(take_source), 3)

        self.assertEqual(list(views.counted(2)(counted_source)), [1, 2])
        self.assertEqual(next(counted_source), 3)

    def test_positive_take_can_bound_an_infinite_iterable(self) -> None:
        result = views.take(4)(itertools.count(10))

        self.assertEqual(list(result), [10, 11, 12, 13])

    def test_negative_take_materializes_the_complete_input(self) -> None:
        source = iter([1, 2, 3, 4])

        self.assertEqual(list(views.take(-1)(source)), [1, 2, 3])
        with self.assertRaises(StopIteration):
            next(source)

    def test_projection_and_enumeration_views(self) -> None:
        pairs = [("a", 1), ("b", 2)]

        self.assertEqual(list(views.elements(0)(pairs)), ["a", "b"])
        self.assertEqual(list(views.keys()(pairs)), ["a", "b"])
        self.assertEqual(list(views.values()(pairs)), [1, 2])
        self.assertEqual(list(views.enumerate(5)(["a", "b"])), [(5, "a"), (6, "b")])

    def test_combination_views(self) -> None:
        self.assertEqual(list(views.concat([3], [4, 5])([1, 2])), [1, 2, 3, 4, 5])
        self.assertEqual(list(views.zip([10, 20])([1, 2, 3])), [(1, 10), (2, 20)])
        self.assertEqual(
            list(views.zip([10, 20], [True, False])([1, 2, 3])),
            [(1, 10, True), (2, 20, False)],
        )
        self.assertEqual(
            list(views.zip_transform(add_values, [10, 20])([1, 2, 3])),
            [11, 22],
        )
        self.assertEqual(
            list(views.cartesian_product([10, 20])([1, 2])),
            [(1, 10), (1, 20), (2, 10), (2, 20)],
        )
        self.assertEqual(
            list(views.cartesian_product([10, 20], ["a", "b"])([1, 2])),
            [
                (1, 10, "a"),
                (1, 10, "b"),
                (1, 20, "a"),
                (1, 20, "b"),
                (2, 10, "a"),
                (2, 10, "b"),
                (2, 20, "a"),
                (2, 20, "b"),
            ],
        )
        self.assertEqual(
            list([1, 2] | views.zip(["a", "b"])),
            [(1, "a"), (2, "b")],
        )
        self.assertEqual(
            list([1, 2] | views.cartesian_product(["a", "b"])),
            [(1, "a"), (1, "b"), (2, "a"), (2, "b")],
        )

    def test_uneven_zip_consumes_one_extra_from_longer_left_iterator(self) -> None:
        source = iter([1, 2, 3])

        self.assertEqual(list(source | views.zip(["a"])), [(1, "a")])
        self.assertEqual(next(source), 3)

    def test_window_and_grouping_views(self) -> None:
        self.assertEqual(list(views.adjacent(3)([1, 2, 3, 4])), [(1, 2, 3), (2, 3, 4)])
        self.assertEqual(list(views.pairwise()([1, 2, 3])), [(1, 2), (2, 3)])
        self.assertEqual(
            list(views.adjacent_transform(add_values, 2)([1, 2, 3])), [3, 5]
        )
        self.assertEqual(
            list(views.pairwise_transform(multiply_values)([1, 2, 3])),
            [2, 6],
        )
        self.assertEqual(
            [list(chunk) for chunk in views.chunk(2)([1, 2, 3, 4, 5])],
            [[1, 2], [3, 4], [5]],
        )
        self.assertEqual(
            [list(window) for window in views.slide(3)([1, 2, 3, 4])],
            [[1, 2, 3], [2, 3, 4]],
        )
        self.assertEqual(
            [list(chunk) for chunk in views.chunk_by(are_consecutive)([1, 2, 4, 5, 8])],
            [[1, 2], [4, 5], [8]],
        )
        empty_chunks: Range[Range[int]] = views.chunk_by(are_consecutive)([])
        self.assertEqual(list(empty_chunks), [])
        self.assertEqual(list(views.stride(2)(range(6))), [0, 2, 4])

    def test_join_split_and_conversion_views(self) -> None:
        nested: list[list[int]] = [[1, 2], [3], [4, 5]]

        self.assertEqual(list(views.join()(nested)), [1, 2, 3, 4, 5])
        self.assertEqual(list(views.join_with([0])(nested)), [1, 2, 0, 3, 0, 4, 5])
        self.assertEqual(list(views.join_with(0)(nested)), [1, 2, 0, 3, 0, 4, 5])

        string_nested: list[list[str]] = [["left"], ["right"]]
        self.assertEqual(
            list(views.join_with("::")(string_nested)), ["left", "::", "right"]
        )

        empty_separator: list[int] = []
        joined_without_separator = views.join_with(empty_separator)(nested)
        self.assertEqual(list(joined_without_separator), [1, 2, 3, 4, 5])

        self.assertEqual(
            [list(chunk) for chunk in views.split([0])([1, 0, 2, 0])],
            [[1], [2], []],
        )
        self.assertEqual(
            [list(chunk) for chunk in views.split(0)([1, 0, 2, 0])],
            [[1], [2], []],
        )
        self.assertEqual(
            [list(chunk) for chunk in views.split("::")(["left", "::", "right"])],
            [["left"], ["right"]],
        )
        self.assertEqual(
            [list(chunk) for chunk in views.split([1, 1])([1, 1, 1])],
            [[], [1]],
        )
        self.assertEqual(views.to(tuple)([1, 2, 3]), (1, 2, 3))
        self.assertEqual(views.to(str)(["a", "b", "c"]), "abc")

    def test_public_validation_contract(self) -> None:
        invalid_factories: list[Callable[[], object]] = [
            lambda: views.counted(-1),
            lambda: views.adjacent(0),
            lambda: views.adjacent_transform(sum, 0),
            lambda: views.chunk(0),
            lambda: views.slide(0),
            lambda: views.stride(0),
        ]

        for factory in invalid_factories:
            with self.subTest(factory=factory):
                with self.assertRaises(ValueError):
                    factory()

        with self.assertRaises(ValueError):
            views.split([])([1, 2, 3])

    def test_split_validates_before_consuming_input(self) -> None:
        source = iter([1, 2, 3])

        with self.assertRaises(ValueError):
            views.split([])(source)

        self.assertEqual(next(source), 1)

    def test_pipeline_uses_only_the_public_facade(self) -> None:
        result = (
            ranges.iota(1, 8)
            | views.filter(is_odd)
            | views.transform(times_ten)
            | views.take(3)
            | views.to(tuple)
        )

        self.assertEqual(result, (10, 30, 50))
        self.assertIsInstance(ranges.iota(1, 2), Range)

    def test_root_namespace_stays_small(self) -> None:
        self.assertEqual(rangeslib.__all__, ["Range", "ranges", "views"])
        self.assertFalse(hasattr(rangeslib, "Take"))
        self.assertFalse(hasattr(rangeslib, "Iota"))


if __name__ == "__main__":
    unittest.main()
