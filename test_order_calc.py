import contextlib
import io
import unittest

from order_calc import (
    add_tax,
    apply_bonus_discount,
    apply_discount,
    calculate_order_total,
    calculate_subtotal,
    p,
)

STUDENT = {"type": "student", "active": True}
GUEST = {"type": "guest", "active": True}
ITEMS = [{"price": 500, "qty": 2}, {"price": 200, "qty": 1}]


class TestOrderCalculation(unittest.TestCase):
    def test_subtotal_sums_price_times_quantity(self):
        self.assertEqual(calculate_subtotal(ITEMS), 1200)

    def test_student_total_includes_discount_and_tax(self):
        result = calculate_order_total(STUDENT, ITEMS, 0)
        self.assertAlmostEqual(result, 1296.0)

    def test_guest_total_has_only_tax(self):
        result = calculate_order_total(GUEST, [{"price": 100, "qty": 3}], 1)
        self.assertAlmostEqual(result, 360.0)

    def test_unknown_user_type_has_no_discount(self):
        self.assertEqual(apply_discount(1000, "manager"), 1000)

    def test_inactive_user_does_not_get_bonus(self):
        self.assertEqual(apply_bonus_discount(2000, 1, False), 2000)

    def test_bonus_disabled_flag_does_not_give_bonus(self):
        self.assertEqual(apply_bonus_discount(2000, 0, True), 2000)

    def test_bonus_threshold_is_not_included(self):
        self.assertEqual(apply_bonus_discount(1000, 1, True), 1000)

    def test_value_above_threshold_gets_bonus(self):
        self.assertEqual(apply_bonus_discount(1001, 1, True), 951)

    def test_empty_order_has_zero_total(self):
        self.assertEqual(calculate_order_total(STUDENT, [], 1), 0)

    def test_add_tax_increases_amount_by_twenty_percent(self):
        self.assertAlmostEqual(add_tax(100), 120.0)

    def test_legacy_function_p_prints_and_returns_total(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = p(STUDENT, ITEMS, 1)
        self.assertAlmostEqual(result, 1236.0)
        self.assertEqual(buffer.getvalue().strip(), "Total: 1236.0")


if __name__ == "__main__":
    unittest.main()
