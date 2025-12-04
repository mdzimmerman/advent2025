import unittest
from aoc import Point

class AocPointTests(unittest.TestCase):
    def test_neighbors(self):
        p = Point(1, 2)
        ns = list(p.neighbors())

        self.assertEqual(len(ns), 8)
        self.assertIn(Point(0, 1), ns)
        self.assertIn(Point(0, 2), ns)
        self.assertIn(Point(0, 3), ns)
        self.assertIn(Point(1, 1), ns)
        self.assertIn(Point(1, 3), ns)
        self.assertIn(Point(2, 1), ns)
        self.assertIn(Point(2, 2), ns)
        self.assertIn(Point(2, 3), ns)
