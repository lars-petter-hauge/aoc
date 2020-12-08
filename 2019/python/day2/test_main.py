import unittest

from day2.main import run


class Test(unittest.TestCase):
    def test_run(self):
        data = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
        expected = [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
        self.assertEqual(expected, run(data))

        data = [1, 0, 0, 0, 99]
        expected = [2, 0, 0, 0, 99]
        self.assertEqual(expected, run(data))

        data = [2, 3, 0, 3, 99]
        expected = [2, 3, 0, 6, 99]
        self.assertEqual(expected, run(data))

        data = [2, 4, 4, 5, 99, 0]
        expected = [2, 4, 4, 5, 99, 9801]
        self.assertEqual(expected, run(data))

        data = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        expected = [30, 1, 1, 4, 2, 5, 6, 0, 99]
        self.assertEqual(expected, run(data))
