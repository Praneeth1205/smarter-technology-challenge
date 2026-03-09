"""
Robotic Arm Package Dispatcher
Smarter Technology – Technical Screen
"""


import unittest


def sort(width: float, height: float, length: float, mass: float) -> str:
    """
    Dispatches a package to the correct stack based on its dimensions and mass.

    Args:
        width   (float): Width in centimeters
        height  (float): Height in centimeters
        length  (float): Length in centimeters
        mass    (float): Mass in kilograms

    Returns:
        str: "STANDARD" | "SPECIAL" | "REJECTED"

    Raises:
        ValueError: If any dimension or mass is negative
    """
    if any(v < 0 for v in (width, height, length, mass)):
        raise ValueError("Dimensions and mass must be non-negative.")

    volume = width * height * length
    is_bulky = volume >= 1_000_000 or max(width, height, length) >= 150
    is_heavy = mass >= 20

    if is_bulky and is_heavy:
        return "REJECTED"
    if is_bulky or is_heavy:
        return "SPECIAL"
    return "STANDARD"


# ──────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────


class TestSort(unittest.TestCase):

    # ── STANDARD ──────────────────────────────
    def test_standard_normal_package(self):
        self.assertEqual(sort(10, 10, 10, 5), "STANDARD")

    def test_standard_zero_mass(self):
        self.assertEqual(sort(5, 5, 5, 0), "STANDARD")

    def test_standard_boundary_below_volume(self):
        # volume = 999_999 → not bulky; mass 19 → not heavy
        self.assertEqual(sort(99.9999, 10, 10, 19), "STANDARD")

    # ── SPECIAL (bulky only) ───────────────────
    def test_special_volume_exactly_1m(self):
        # 100 x 100 x 100 = 1_000_000
        self.assertEqual(sort(100, 100, 100, 5), "SPECIAL")

    def test_special_volume_over_1m(self):
        self.assertEqual(sort(200, 50, 100, 10), "SPECIAL")

    def test_special_single_dimension_exactly_150(self):
        self.assertEqual(sort(150, 10, 10, 5), "SPECIAL")

    def test_special_single_dimension_over_150(self):
        self.assertEqual(sort(200, 5, 5, 1), "SPECIAL")

    # ── SPECIAL (heavy only) ──────────────────
    def test_special_heavy_exactly_20kg(self):
        self.assertEqual(sort(10, 10, 10, 20), "SPECIAL")

    def test_special_heavy_over_20kg(self):
        self.assertEqual(sort(10, 10, 10, 50), "SPECIAL")

    # ── REJECTED (bulky + heavy) ───────────────
    def test_rejected_bulky_and_heavy(self):
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")

    def test_rejected_large_dimension_and_heavy(self):
        self.assertEqual(sort(150, 10, 10, 25), "REJECTED")

    def test_rejected_all_extreme(self):
        self.assertEqual(sort(500, 500, 500, 100), "REJECTED")

    # ── Edge cases ────────────────────────────
    def test_zero_dimensions(self):
        self.assertEqual(sort(0, 0, 0, 0), "STANDARD")

    def test_negative_dimension_raises(self):
        with self.assertRaises(ValueError):
            sort(-1, 10, 10, 5)

    def test_negative_mass_raises(self):
        with self.assertRaises(ValueError):
            sort(10, 10, 10, -5)

    def test_float_dimensions(self):
        # 150.0001 triggers bulky by dimension
        self.assertEqual(sort(150.0001, 5, 5, 1), "SPECIAL")

    def test_exactly_boundary_mass_not_heavy(self):
        # 19.9999 kg → not heavy
        self.assertEqual(sort(10, 10, 10, 19.9999), "STANDARD")


if __name__ == "__main__":
    unittest.main(verbosity=2)
