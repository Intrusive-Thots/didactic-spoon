import unittest
import customtkinter as ctk
from unittest.mock import MagicMock

# Assuming we can mock out dependencies to just test UI instantiation
from ui.components.priority_grid import PriorityIconGrid
from ui.components.factory import make_input

class TestUIKwargs(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.config_mock = MagicMock()
        self.config_mock.get.return_value = {}
        self.assets_mock = MagicMock()

    def test_priority_grid_instantiation(self):
        """Test that PriorityIconGrid instantiates without ValueError from unsupported kwargs."""
        try:
            grid = PriorityIconGrid(self.root, self.config_mock, self.assets_mock)
            self.assertIsNotNone(grid)
        except ValueError as e:
            self.fail(f"PriorityIconGrid instantiation failed with ValueError: {e}")

    def test_factory_make_input(self):
        """Test that factory.make_input instantiates without ValueError."""
        try:
            entry = make_input(self.root, placeholder="Test")
            self.assertIsNotNone(entry)
        except ValueError as e:
            self.fail(f"make_input instantiation failed with ValueError: {e}")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
