import unittest

from rangeslib import (
    Drop,
    DropWhile,
    Empty,
    Filter,
    Iota,
    Indices,
    Join,
    JoinWith,
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
)


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
        self.assertEqual(list(Single("value")), ["value"])
        self.assertEqual(list(Iota(2, 6)), [2, 3, 4, 5])
        self.assertEqual(list(Iota(4, 2)), [])
        self.assertEqual(list(Indices(4)), [0, 1, 2, 3])
        self.assertEqual(list(Indices(0)), [])
        self.assertEqual(list(Repeat("x", 3)), ["x", "x", "x"])
        self.assertEqual(list(Repeat("x", 0)), [])

    def test_all_range_generators_share_the_base_type(self) -> None:
        generators = [Empty, Single, Iota, Indices, Repeat]

        for generator in generators:
            with self.subTest(generator=generator):
                self.assertTrue(issubclass(generator, RangeGenerator))


class RangeAdaptorTests(unittest.TestCase):
    def test_all_adaptors_share_the_base_type(self) -> None:
        adaptors = [To(list), Reverse(), Filter(lambda value: value > 0), Transform(str), Take(1), TakeWhile(lambda value: value > 0), Drop(1), DropWhile(lambda value: value > 0), Join(), JoinWith([0]), Split([0])]

        for adaptor in adaptors:
            with self.subTest(adaptor=adaptor):
                self.assertIsInstance(adaptor, RangeAdaptor)

    def test_reverse_accepts_a_normal_iterable(self) -> None:
        result = Reverse()((value for value in [1, 2, 3]))

        self.assertEqual(list(result), [3, 2, 1])
        self.assertIsInstance(result, Range)

    def test_filter_accepts_a_normal_iterable(self) -> None:
        result = Filter(lambda value: value % 2 == 0)([1, 2, 3, 4])

        self.assertEqual(list(result), [2, 4])

    def test_transform_changes_element_type(self) -> None:
        result = Transform(str)([1, 2, 3])

        self.assertEqual(list(result), ["1", "2", "3"])
        self.assertIsInstance(result, Range)

    def test_take_and_drop(self) -> None:
        values = [1, 2, 3, 4]

        self.assertEqual(list(Take(2)(values)), [1, 2])
        self.assertEqual(list(Take(0)(values)), [])
        self.assertEqual(list(Take(-1)(values)), [1, 2, 3])
        self.assertEqual(list(Drop(2)(values)), [3, 4])
        self.assertEqual(list(Drop(0)(values)), values)
        self.assertEqual(list(Drop(-1)(values)), [4])

    def test_to_converts_to_the_requested_type(self) -> None:
        values = Range(1, 2, 2, 3)

        self.assertEqual(To(list)(values), [1, 2, 2, 3])
        self.assertEqual(To(tuple)(values), (1, 2, 2, 3))
        self.assertEqual(To(set)(values), {1, 2, 3})

    def test_take_while_and_drop_while_accept_normal_iterables(self) -> None:
        self.assertEqual(list(TakeWhile(lambda value: value < 3)([1, 2, 3, 2])), [1, 2])
        self.assertEqual(list(DropWhile(lambda value: value < 3)([1, 2, 3, 2])), [3, 2])

    def test_join_accepts_an_iterable_of_iterables(self) -> None:
        nested_values = (values for values in [[1, 2], (3,), range(4, 6)])

        self.assertEqual(list(Join()(nested_values)), [1, 2, 3, 4, 5])

    def test_join_with_inserts_a_pattern_between_iterables(self) -> None:
        nested_values = (values for values in [[1, 2], (3,), range(4, 6)])

        self.assertEqual(list(JoinWith([0, 0])(nested_values)), [1, 2, 0, 0, 3, 0, 0, 4, 5])

    def test_split_accepts_a_pattern_and_preserves_empty_chunks(self) -> None:
        result = Split([0, 0])([1, 2, 0, 0, 3, 0, 0])

        self.assertEqual([list(chunk) for chunk in result], [[1, 2], [3], []])

    def test_split_rejects_an_empty_pattern(self) -> None:
        with self.assertRaises(ValueError):
            Split([])([1, 2, 3])

    def test_join_works_in_a_pipeline(self) -> None:
        result = Iota(1, 4) | Transform(lambda value: range(value)) | Join()

        self.assertEqual(list(result), [0, 0, 1, 0, 1, 2])

    def test_to_supports_a_custom_factory(self) -> None:
        result = To(lambda iterable: ":".join(iterable))(["a", "b", "c"])

        self.assertEqual(result, "a:b:c")

    def test_pipeline_composes_adaptors(self) -> None:
        result = (
            Iota(1, 7)
            | Reverse()
            | Filter(lambda value: value % 2 == 0)
            | Transform(lambda value: value * 10)
            | Take(2)
        )

        self.assertEqual(list(result), [60, 40])

    def test_pipeline_can_finish_with_to(self) -> None:
        result = Iota(1, 4) | Filter(lambda value: value > 1) | To(tuple)

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
            "Join",
            "JoinWith",
            "Single",
            "Split",
            "Empty",
            "Iota",
            "Indices",
            "Repeat",
            "Transform",
        }

        self.assertEqual(set(vars(Ranges)), expected_names)
        self.assertIs(Ranges.Range, Range)
        self.assertIs(Ranges.To, To)
        self.assertIsInstance(Ranges.Reverse, Reverse)


if __name__ == "__main__":
    unittest.main()
