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

from ui.components.factory import get_color

class TestFactoryGetColor(unittest.TestCase):
    def setUp(self):
        # Clear lru_cache before each test to ensure deterministic behavior
        get_color.cache_clear()

    @patch('ui.components.factory.TOKENS.get')
    def test_get_color_valid_path(self, mock_get):
        mock_get.return_value = "#123456"
        result = get_color("colors.primary")
        self.assertEqual(result, "#123456")
        mock_get.assert_called_once_with("colors", "primary", default="#000000")

    @patch('ui.components.factory.TOKENS.get')
    def test_get_color_invalid_path_default(self, mock_get):
        # When get returns default, we mock it
        mock_get.return_value = "#000000"
        result = get_color("colors.invalid")
        self.assertEqual(result, "#000000")
        mock_get.assert_called_once_with("colors", "invalid", default="#000000")

    @patch('ui.components.factory.TOKENS.get')
    def test_get_color_custom_default(self, mock_get):
        mock_get.return_value = "#FFFFFF"
        result = get_color("colors.missing", default="#FFFFFF")
        self.assertEqual(result, "#FFFFFF")
        mock_get.assert_called_once_with("colors", "missing", default="#FFFFFF")

    @patch('ui.components.factory.TOKENS.get')
    def test_get_color_no_dots(self, mock_get):
        mock_get.return_value = "#111111"
        result = get_color("primary")
        self.assertEqual(result, "#111111")
        mock_get.assert_called_once_with("primary", default="#000000")

    @patch('ui.components.factory.TOKENS.get')
    def test_get_color_caching(self, mock_get):
        mock_get.return_value = "#222222"
        # First call
        result1 = get_color("colors.secondary")
        # Second call
        result2 = get_color("colors.secondary")

        self.assertEqual(result1, "#222222")
        self.assertEqual(result2, "#222222")
        # Ensure TOKENS.get was only called once due to caching
        mock_get.assert_called_once_with("colors", "secondary", default="#000000")

if __name__ == '__main__':
    unittest.main()
