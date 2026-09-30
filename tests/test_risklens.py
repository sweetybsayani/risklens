import unittest
from risklens.model import Risk, rating
from risklens.register import Register


def mk(**kw):
    base = dict(id="R-X", title="t", asset="a", threat="th", csf_function="protect",
                cissp_domain="d", likelihood=4, impact=5, control_effectiveness=0.5,
                asset_value=100000, exposure_factor=0.5, aro=2, owner="o",
                treatment="mitigate", review_date="2099-01-01")
    base.update(kw)
    return Risk(**base)


class Tests(unittest.TestCase):
    def test_scores(self):
        r = mk()
        self.assertEqual(r.inherent, 20)
        self.assertEqual(r.residual, 10.0)
        self.assertEqual(r.sle, 50000)
        self.assertEqual(r.ale, 100000)
        self.assertEqual(r.residual_ale, 50000)

    def test_rating_bands(self):
        self.assertEqual([rating(x) for x in (2, 5, 10, 15)], ["Low", "Medium", "High", "Critical"])

    def test_validation(self):
        self.assertTrue(mk(likelihood=9).validate())
        self.assertTrue(mk(treatment="ignore").validate())
        self.assertFalse(mk().validate())

    def test_duplicates_and_overdue(self):
        reg = Register([mk(), mk(review_date="2000-01-01")])
        self.assertIn("R-X: duplicate ID", reg.validate())
        self.assertEqual(len(reg.overdue()), 1)

    def test_appetite(self):
        reg = Register([mk(treatment="accept", control_effectiveness=0.1)], appetite=10)
        self.assertEqual(len(reg.appetite_breaches()), 1)
        reg = Register([mk(treatment="mitigate", control_effectiveness=0.1)], appetite=10)
        self.assertEqual(len(reg.appetite_breaches()), 0)


if __name__ == "__main__":
    unittest.main()
