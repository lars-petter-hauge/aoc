from day3.main import run

import unittest

class Test(unittest.TestCase):
    def test_run(self):
        self.assertEqual(6, run("day3/example1.txt"))
        self.assertEqual(159, run("day3/example2.txt"))
        self.assertEqual(135, run("day3/example3.txt"))

