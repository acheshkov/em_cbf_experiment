import unittest
from line_range import Range


class TestLineRange(unittest.TestCase):

    def test_creation_1(self):
        rg = Range(3)
        self.assertEqual(rg.start, rg.end)

    def test_creation_2(self):
        rg = Range(3, 5)
        self.assertEqual(rg.start, 3)
        self.assertEqual(rg.end, 5)

    def test_creation_assert(self):
        with self.assertRaises(AssertionError):
            Range(5, 2)

    def test_equality(self):
        rg_1 = Range(2, 5)
        rg_2 = Range(2, 5)
        rg_3 = Range(3, 6)
        self.assertEqual(rg_1, rg_2)
        self.assertNotEqual(rg_1, rg_3)

    def test_make_from_str(self):
        self.assertEqual(Range.from_str("[4, 5]"), Range(4, 5))
        self.assertEqual(Range.from_str("(5, 6)"), Range(5, 6))

    def test_access_start_property(self):
        rg = Range(3, 5)
        self.assertEqual(rg.start, 3)
        self.assertEqual(rg.end, 5)

    def test_contains(self):
        self.assertTrue(Range(1, 5).contains(Range(1, 5)))
        self.assertTrue(Range(1, 5).contains(Range(2, 4)))
        self.assertFalse(Range(1, 5).contains(Range(1, 6)))
