from day3.main import run

import unittest


class Test(unittest.TestCase):
    def test_run(self):
        dist, _ = run("day3/example1.txt")
        self.assertEqual(6, dist)

        dist, path = run("day3/example2.txt")
        self.assertEqual(159, dist)
        self.assertEqual(610, path)

        dist, path = run("day3/example3.txt")
        self.assertEqual(135, dist)
        self.assertEqual(410, path)
