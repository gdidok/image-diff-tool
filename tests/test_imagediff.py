import unittest
import sys
from src.imagediff import roundToTwoDecimal

class ImageDiff(unittest.TestCase):
    def setUp(self):
        self.a = sys.argv[1]
    def test_rounding_number(self):
        value = roundToTwoDecimal(72.3123)
        self.assertEqual(value, 0.72)
    def test_zero_to_int(self):
        value = roundToTwoDecimal(0.0)
        self.assertEqual(value, 0)
    # test cases for compareImages, main, etc

if __name__ == '__main__':
    unittest.main()