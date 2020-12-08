import unittest


from day1 import main, calc_fuel_amount, calc_fuel_amount_recursive


class TestDay1(unittest.TestCase):
    def test_main(self):
        pass

    def test_fuel_amount(self):
        self.assertEqual(2, calc_fuel_amount(12))
        self.assertEqual(2, calc_fuel_amount(14))
        self.assertEqual(654, calc_fuel_amount(1969))
        self.assertEqual(33583, calc_fuel_amount(100756))

    def test_fuel_amount_recursive(self):
        self.assertEqual(2, calc_fuel_amount_recursive(14))
        self.assertEqual(966, calc_fuel_amount_recursive(1969))
        self.assertEqual(50346, calc_fuel_amount_recursive(100756))


if __name__ == "__main__":
    unittest.main()
