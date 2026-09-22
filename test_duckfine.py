import unittest

from duckfine import DuckFine


class TestDuckFineInit(unittest.TestCase):
    def test_init_sets_member_id(self):
        fine = DuckFine("member-1")
        self.assertEqual(fine.member_id, "member-1")

    def test_init_sets_total_owed_to_zero(self):
        fine = DuckFine("member-1")
        self.assertEqual(fine.total_owed, 0.0)


class TestDuckFineChargeValidation(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine("member-1")

    def test_negative_days_late_raises(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)

    def test_negative_days_late_does_not_change_total_owed(self):
        try:
            self.fine.charge(-1)
        except ValueError:
            pass
        self.assertEqual(self.fine.total_owed, 0.0)


class TestDuckFineGracePeriod(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine("member-1")

    def test_zero_days_late_has_no_fee(self):
        self.assertEqual(self.fine.charge(0), 0.0)

    def test_days_late_within_grace_has_no_fee(self):
        self.assertEqual(self.fine.charge(2), 0.0)

    def test_day_after_grace_period_incurs_fee(self):
        self.assertEqual(self.fine.charge(3), 0.5)


class TestDuckFineFeeCalculation(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine("member-1")

    def test_standard_fee_for_days_past_grace(self):
        self.assertEqual(self.fine.charge(5), 1.5)

    def test_deluxe_doubles_the_fee(self):
        self.assertEqual(self.fine.charge(5, deluxe=True), 3.0)

    def test_fee_is_capped_at_max_fee(self):
        self.assertEqual(self.fine.charge(100), 5.00)

    def test_deluxe_fee_is_capped_at_max_fee(self):
        self.assertEqual(self.fine.charge(20, deluxe=True), 5.00)


class TestDuckFineTotalOwed(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine("member-1")

    def test_charge_returns_the_fee_amount(self):
        result = self.fine.charge(5)
        self.assertEqual(result, 1.5)

    def test_charge_adds_fee_to_total_owed(self):
        self.fine.charge(5)
        self.assertEqual(self.fine.total_owed, 1.5)

    def test_total_owed_accumulates_across_multiple_charges(self):
        self.fine.charge(5)
        self.fine.charge(3)
        self.assertEqual(self.fine.total_owed, 2.0)


if __name__ == "__main__":
    unittest.main()
