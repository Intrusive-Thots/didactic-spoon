import sys
import unittest
from unittest.mock import patch, MagicMock

# Mock dependencies before importing the module under test
patch.dict(sys.modules, {
    'customtkinter': MagicMock(),
    'tkinter': MagicMock(),
    'PIL': MagicMock(),
    'PIL.Image': MagicMock(),
    'PIL.ImageTk': MagicMock()
}).start()

from ui.components.color_utils import hex_to_rgb, interpolate_color
from utils.logger import Logger

class TestColorUtils(unittest.TestCase):
    def test_hex_to_rgb_6_char(self):
        """Test with standard 6-character hex string with leading #"""
        self.assertEqual(hex_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#FF0000"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("#00FF00"), (0, 255, 0))
        self.assertEqual(hex_to_rgb("#0000FF"), (0, 0, 255))
        self.assertEqual(hex_to_rgb("#1A2B3C"), (26, 43, 60))

    def test_hex_to_rgb_6_char_no_hash(self):
        """Test with 6-character hex string without leading #"""
        self.assertEqual(hex_to_rgb("FFFFFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("1A2B3C"), (26, 43, 60))

    def test_hex_to_rgb_3_char(self):
        """Test with 3-character hex string with leading #"""
        self.assertEqual(hex_to_rgb("#FFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#F00"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("#123"), (17, 34, 51))

    def test_hex_to_rgb_3_char_no_hash(self):
        """Test with 3-character hex string without leading #"""
        self.assertEqual(hex_to_rgb("FFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("123"), (17, 34, 51))

    def test_hex_to_rgb_invalid_length(self):
        """Test with invalid hex string lengths"""
        with self.assertRaises(ValueError):
            hex_to_rgb("#FF") # Length 2
        with self.assertRaises(ValueError):
            hex_to_rgb("#FFFF") # Length 4
        with self.assertRaises(ValueError):
            hex_to_rgb("FFFFF") # Length 5
        with self.assertRaises(ValueError):
            hex_to_rgb("#FFFFFFF") # Length 7

    def test_hex_to_rgb_invalid_chars(self):
        """Test with invalid characters in hex string"""
        with self.assertRaises(ValueError):
            hex_to_rgb("#ZZZZZZ")
        with self.assertRaises(ValueError):
            hex_to_rgb("GHIJKL")


    def test_interpolate_color_transparent(self):
        """Test interpolation with 'transparent' color"""
        self.assertEqual(interpolate_color("transparent", "#FFFFFF", 0.5), "transparent")
        self.assertEqual(interpolate_color("#FFFFFF", "transparent", 0.5), "#FFFFFF")
        self.assertEqual(interpolate_color("transparent", "transparent", 0.5), "transparent")

    def test_interpolate_color_factor_0(self):
        """Test interpolation with factor 0 (returns color1)"""
        self.assertEqual(interpolate_color("#000000", "#FFFFFF", 0), "#000000")
        self.assertEqual(interpolate_color("#FF0000", "#00FF00", 0), "#ff0000") # Lowercase hex returned

    def test_interpolate_color_factor_1(self):
        """Test interpolation with factor 1 (returns color2)"""
        self.assertEqual(interpolate_color("#000000", "#FFFFFF", 1), "#ffffff")
        self.assertEqual(interpolate_color("#FF0000", "#00FF00", 1), "#00ff00")

    def test_interpolate_color_factor_midpoint(self):
        """Test interpolation with factor 0.5"""
        # Midpoint of black and white is gray
        self.assertEqual(interpolate_color("#000000", "#FFFFFF", 0.5), "#7f7f7f") # int(255*0.5) = 127 = 7f

        # Midpoint of Red and Blue is Purple
        self.assertEqual(interpolate_color("#FF0000", "#0000FF", 0.5), "#7f007f")

    @patch('utils.logger.Logger.error')
    def test_interpolate_color_error_handling(self, mock_logger_error):
        """Test that invalid inputs trigger the broad exception block, log the error, and return color1"""
        # Invalid color2 format triggers ValueError in list comprehension
        result = interpolate_color("#FFFFFF", "invalid_hex", 0.5)

        # Should return color1
        self.assertEqual(result, "#FFFFFF")

        # Logger should have been called
        mock_logger_error.assert_called_once()
        args, kwargs = mock_logger_error.call_args
        self.assertEqual(args[0], "color_utils.py")
        self.assertTrue(args[1].startswith("Handled exception:"))

if __name__ == '__main__':
    unittest.main()
