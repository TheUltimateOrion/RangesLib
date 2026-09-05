import itertools
import unittest

import rangeslib
from rangeslib import Range, ranges, views


class PublicGeneratorTests(unittest.TestCase):
    def test_all_generators_are_available_through_ranges(self) -> None:
        self.assertEqual(list(ranges.empty()), [])
        self.assertEqual(list(ranges.single("value")), ["value"])
        self.assertEqual(list(ranges.iota(2, 5)), [2, 3, 4])
        self.assertEqual(list(ranges.indices(3)), [0, 1, 2])
        self.assertEqual(list(ranges.repeat("x", 3)), ["x", "x", "x"])

    def test_non_positive_generator_counts_follow_builtin_range_and_list_rules(self) -> None:
        self.assertEqual(list(ranges.indices(-2)), [])
        self.assertEqual(list(ranges.repeat("x", -2)), [])
        self.assertEqual(list(ranges.iota(5, 2)), [])


class PublicViewTests(unittest.TestCase):
    def test_value_processing_views(self) -> None:
        values = [1, 2, 3, 4]

        self.assertEqual(list(views.reverse()(values)), [4, 3, 2, 1])
        self.assertEqual(list(views.filter(lambda x: x % 2 == 0)(values)), [2, 4])
        self.assertEqual(list(views.transform(str)(values)), ["1", "2", "3", "4"])
        self.assertEqual(list(views.take(2)(values)), [1, 2])
        self.assertEqual(list(views.take(-1)(values)), [1, 2, 3])
        self.assertEqual(list(views.drop(2)(values)), [3, 4])
        self.assertEqual(list(views.drop(-1)(values)), [4])
        self.assertEqual(list(views.takewhile(lambda x: x < 3)(values)), [1, 2])
        self.assertEqual(list(views.dropwhile(lambda x: x < 3)(values)), [3, 4])

    def test_bounded_take_and_counted_leave_a_one_shot_iterator_positioned(self) -> None:
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
            list(views.zip_transform(lambda a, b: a + b, [10, 20])([1, 2, 3])),
            [11, 22],
        )
        self.assertEqual(
            list(views.cartesian_product([10, 20])([1, 2])),
            [(1, 10), (1, 20), (2, 10), (2, 20)],
        )

    def test_window_and_grouping_views(self) -> None:
        self.assertEqual(list(views.adjacent(3)([1, 2, 3, 4])), [(1, 2, 3), (2, 3, 4)])
        self.assertEqual(list(views.pairwise()([1, 2, 3])), [(1, 2), (2, 3)])
        self.assertEqual(list(views.adjacent_transform(lambda a, b: a + b, 2)([1, 2, 3])), [3, 5])
        self.assertEqual(
            list(views.pairwise_transform(lambda a, b: a * b)([1, 2, 3])),
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
            [
                list(chunk)
                for chunk in views.chunk_by(lambda a, b: b - a == 1)(
                    [1, 2, 4, 5, 8]
                )
            ],
            [[1, 2], [4, 5], [8]],
        )
        self.assertEqual(list(views.chunk_by(lambda a, b: True)([])), [])
        self.assertEqual(list(views.stride(2)(range(6))), [0, 2, 4])

    def test_join_split_and_conversion_views(self) -> None:
        nested = [[1, 2], [3], [4, 5]]

        self.assertEqual(list(views.join()(nested)), [1, 2, 3, 4, 5])
        self.assertEqual(list(views.join_with([0])(nested)), [1, 2, 0, 3, 0, 4, 5])
        self.assertEqual(list(views.join_with([])(nested)), [1, 2, 3, 4, 5])
        self.assertEqual(
            [list(chunk) for chunk in views.split([0])([1, 0, 2, 0])],
            [[1], [2], []],
        )
        self.assertEqual(views.to(tuple)([1, 2, 3]), (1, 2, 3))

    def test_public_validation_contract(self) -> None:
        invalid_factories = [
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

    def test_pipeline_uses_only_the_public_facade(self) -> None:
        result = (
            ranges.iota(1, 8)
            | views.filter(lambda value: value % 2 == 1)
            | views.transform(lambda value: value * 10)
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
