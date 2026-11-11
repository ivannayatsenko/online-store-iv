import unittest

from validation import calculate_discount, is_valid_quantity


class TestQuantityValidation(unittest.TestCase):
    def test_typical_valid_value(self):
        self.assertTrue(is_valid_quantity(50))

    def test_lower_boundary_is_valid(self):
        self.assertTrue(is_valid_quantity(1))

    def test_upper_boundary_is_valid(self):
        self.assertTrue(is_valid_quantity(100))

    def test_value_below_minimum_is_invalid(self):
        self.assertFalse(is_valid_quantity(0))

    def test_value_above_maximum_is_invalid(self):
        self.assertFalse(is_valid_quantity(101))

    def test_float_is_invalid(self):
        self.assertFalse(is_valid_quantity(10.5))

    def test_text_is_invalid(self):
        self.assertFalse(is_valid_quantity("abc"))

    def test_none_is_invalid(self):
        self.assertFalse(is_valid_quantity(None))

    def test_quantity_boundaries(self):
        cases = [
            (0, False),
            (1, True),
            (2, True),
            (99, True),
            (100, True),
            (101, False),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(is_valid_quantity(value), expected)


class TestDiscountCalculation(unittest.TestCase):
    def test_student_gets_discount(self):
        self.assertEqual(calculate_discount(1000, "student"), 900)

    def test_teacher_gets_discount(self):
        self.assertEqual(calculate_discount(1000, "teacher"), 900)

    def test_guest_has_no_discount(self):
        self.assertEqual(calculate_discount(1000, "guest"), 1000)


if __name__ == "__main__":
    unittest.main()
