import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure the root directory is in the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.path_utils import resource_path, get_data_dir

class TestPathUtils(unittest.TestCase):

    @patch('sys._MEIPASS', '/tmp/_MEI12345', create=True)
    def test_resource_path_with_meipass(self):
        """Test resource_path when sys._MEIPASS is set (PyInstaller executable)"""
        expected_path = os.path.join('/tmp/_MEI12345', 'assets', 'icon.png')
        self.assertEqual(resource_path(os.path.join('assets', 'icon.png')), expected_path)

    def test_resource_path_without_meipass(self):
        """Test resource_path when sys._MEIPASS is not set (running as script)"""
        # Ensure _MEIPASS is not set for this test
        if hasattr(sys, '_MEIPASS'):
            del sys._MEIPASS

        expected_path = os.path.join(os.path.abspath("."), 'assets', 'icon.png')
        self.assertEqual(resource_path(os.path.join('assets', 'icon.png')), expected_path)

    @patch('sys.frozen', True, create=True)
    @patch.dict(os.environ, {'LOCALAPPDATA': '/home/user/.local/share'}, clear=True)
    def test_get_data_dir_frozen_with_localappdata(self):
        """Test get_data_dir when frozen and LOCALAPPDATA is set"""
        expected_path = os.path.join('/home/user/.local/share', 'DidacticSpoon')
        self.assertEqual(get_data_dir(), expected_path)

    @patch('sys.frozen', True, create=True)
    @patch.dict(os.environ, clear=True)
    @patch('os.path.expanduser', return_value='/home/user')
    def test_get_data_dir_frozen_without_localappdata(self, mock_expanduser):
        """Test get_data_dir when frozen but LOCALAPPDATA is not set (fallback to ~)"""
        expected_path = os.path.join('/home/user', 'DidacticSpoon')
        self.assertEqual(get_data_dir(), expected_path)
        mock_expanduser.assert_called_once_with('~')

    @patch('sys.frozen', False, create=True)
    def test_get_data_dir_not_frozen(self):
        """Test get_data_dir when not frozen (running as script)"""
        expected_path = os.path.abspath(".")
        self.assertEqual(get_data_dir(), expected_path)

if __name__ == '__main__':
    unittest.main()
