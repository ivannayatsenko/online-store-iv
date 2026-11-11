import contextlib
import io
import unittest

from quality_sample import calculate_order_total

ITEMS = [{"price": 500, "qty": 2}, {"price": 200, "qty": 1}]


class TestQualitySample(unittest.TestCase):
    def test_student_gets_discount(self):
        self.assertAlmostEqual(calculate_order_total(ITEMS, "student"), 1080.0)

    def test_teacher_gets_discount(self):
        self.assertAlmostEqual(calculate_order_total(ITEMS, "teacher"), 1080.0)

    def test_guest_has_no_discount(self):
        self.assertEqual(calculate_order_total(ITEMS, "guest"), 1200)

    def test_debug_flag_prints_total(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            calculate_order_total(ITEMS, "student", True)
        self.assertEqual(buffer.getvalue().strip(), "Calculated total: 1080.0")

    def test_vip_has_no_unconfirmed_discount(self):
        self.assertEqual(calculate_order_total(ITEMS, "vip"), 1200)


if __name__ == "__main__":
    unittest.main()
