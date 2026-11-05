import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    # ------------------------------------------------------------------
    # Standard service (existing behaviour preserved)
    # ------------------------------------------------------------------
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_standard_explicit_keyword(self):
        self.assertEqual(shipping_quote(2, "local", service="standard"), 8.0)

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local")

    # ------------------------------------------------------------------
    # Express service
    # ------------------------------------------------------------------
    def test_express_local(self):
        # 5.0 (base) + 1.5*2 (weight) + 7.0 (express) = 15.0
        self.assertEqual(shipping_quote(2, "local", service="express"), 15.0)

    def test_express_regional(self):
        # 8.0 (base) + 1.5*2 (weight) + 7.0 (express) = 18.0
        self.assertEqual(shipping_quote(2, "regional", service="express"), 18.0)

    def test_express_fractional_weight(self):
        # 5.0 + 1.5*1.5 + 7.0 = 14.25
        self.assertAlmostEqual(
            shipping_quote(1.5, "local", service="express"), 14.25
        )

    def test_express_costs_more_than_standard(self):
        for zone in ("local", "regional"):
            std = shipping_quote(3, zone, service="standard")
            exp = shipping_quote(3, zone, service="express")
            self.assertAlmostEqual(exp - std, 7.0)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def test_invalid_service(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "local", service="overnight")

    def test_invalid_zone(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "intergalactic")
