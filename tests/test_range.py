import unittest
from collections.abc import Iterable

from rangeslib import (
    Concat,
    Counted,
    Drop,
    DropWhile,
    Elements,
    Enumerate,
    Empty,
    Filter,
    Iota,
    Indices,
    Join,
    JoinWith,
    Keys,
    Range,
    RangeAdaptor,
    RangeGenerator,
    Ranges,
    Repeat,
    Reverse,
    Single,
    Split,
    Take,
    TakeWhile,
    To,
    Transform,
    Values,
)


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
                self.assertIsSubclass(generator, RangeGenerator)


class RangeAdaptorTests(unittest.TestCase):
    def test_all_adaptors_share_the_base_type(self) -> None:
        adaptors: list[object] = [To(list), Reverse(), Filter(is_positive), Transform(str), Take(1), TakeWhile(is_positive), Drop(1), DropWhile(is_positive), Counted(1), Elements(0), Keys(), Values(), Enumerate(), Concat(), Join(), JoinWith([0]), Split([0])]

        for adaptor in adaptors:
            with self.subTest(adaptor=adaptor):
                self.assertIsInstance(adaptor, RangeAdaptor)

    def test_reverse_accepts_a_normal_iterable(self) -> None:
        result: Range[int] = Reverse[int]()((value for value in [1, 2, 3]))

        self.assertEqual(list(result), [3, 2, 1])
        self.assertIsInstance(result, Range)

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

        self.assertEqual(list(Elements(0)(pairs)), ["a", "b"])
        self.assertEqual(list(Keys()(pairs)), ["a", "b"])
        self.assertEqual(list(Values()(pairs)), [1, 2])

    def test_enumerate_supports_a_start_value(self) -> None:
        result: Range[tuple[int, str]] = Enumerate[str](5)(["a", "b"])

        self.assertEqual(list(result), [(5, "a"), (6, "b")])

    def test_concat_appends_iterables(self) -> None:
        result = Concat((3, 4), (value for value in [5, 6]))([1, 2])

        self.assertEqual(list(result), [1, 2, 3, 4, 5, 6])

    def test_join_accepts_an_iterable_of_iterables(self) -> None:
        nested_values: Iterable[Iterable[int]] = iter([[1, 2], (3,), range(4, 6)])

        self.assertEqual(list(Join[int]()(nested_values)), [1, 2, 3, 4, 5])

    def test_join_with_inserts_a_pattern_between_iterables(self) -> None:
        nested_values: Iterable[Iterable[int]] = iter([[1, 2], (3,), range(4, 6)])

        self.assertEqual(list(JoinWith[int]([0, 0])(nested_values)), [1, 2, 0, 0, 3, 0, 0, 4, 5])

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
    def test_ranges_exposes_public_api(self) -> None:
        expected_names = {
            "Range",
            "RangeAdaptor",
            "RangeGenerator",
            "To",
            "Reverse",
            "Filter",
            "Take",
            "TakeWhile",
            "Drop",
            "DropWhile",
            "Counted",
            "Elements",
            "Enumerate",
            "Join",
            "JoinWith",
            "Keys",
            "Single",
            "Split",
            "Empty",
            "Iota",
            "Indices",
            "Repeat",
            "Transform",
            "Values",
            "Concat",
        }

        self.assertEqual(set(vars(Ranges)), expected_names)
        self.assertIs(Ranges.Range, Range)
        self.assertIs(Ranges.To, To)
        self.assertIsInstance(Ranges.Reverse, Reverse)


if __name__ == "__main__":
    unittest.main()
