import copy
import unittest

from rangeslib import Range


class RangeCollectionContractTests(unittest.TestCase):
    def test_slicing_returns_a_flat_range(self) -> None:
        values = Range(1, 2, 3, 4)

        result = values[1:3]

        self.assertIsInstance(result, Range)
        self.assertEqual(list(result), [2, 3])

    def test_slice_steps_preserve_range(self) -> None:
        values = Range(1, 2, 3, 4, 5)

        self.assertEqual(list(values[::2]), [1, 3, 5])
        self.assertEqual(list(values[::-1]), [5, 4, 3, 2, 1])

    def test_addition_preserves_range_and_order(self) -> None:
        values = Range(1, 2, 3)

        self.assertEqual(list(values + [4, 5]), [1, 2, 3, 4, 5])
        self.assertEqual(list([0] + values), [0, 1, 2, 3])
        self.assertEqual(list(values + Range(4, 5)), [1, 2, 3, 4, 5])
        self.assertIsInstance(values + [4], Range)

    def test_multiplication_preserves_range(self) -> None:
        values = Range(1, 2, 3)

        self.assertEqual(list(values * 2), [1, 2, 3, 1, 2, 3])
        self.assertEqual(list(2 * values), [1, 2, 3, 1, 2, 3])
        self.assertEqual(list(values * 0), [])
        self.assertIsInstance(values * 2, Range)

    def test_copy_is_shallow_independent_and_not_nested(self) -> None:
        inner: list[int] = [1]
        values = Range(inner, [2])

        copied = values.copy()
        copied_by_protocol = copy.copy(values)

        self.assertIsInstance(copied, Range)
        self.assertIsInstance(copied_by_protocol, Range)
        self.assertEqual(list(copied), [inner, [2]])
        self.assertEqual(list(copied_by_protocol), [inner, [2]])
        self.assertIs(copied[0], inner)
        self.assertIs(copied_by_protocol[0], inner)

        copied.append([3])
        self.assertEqual(len(values), 2)
        self.assertEqual(len(copied), 3)

    def test_positional_constructor_can_store_an_iterable_as_one_element(self) -> None:
        nested = [1, 2]

        values = Range(nested)

        self.assertEqual(len(values), 1)
        self.assertIs(values[0], nested)


if __name__ == "__main__":
    unittest.main()
