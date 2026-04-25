import unittest
from unittest.mock import MagicMock, patch, mock_open
import os

from services.asset_manager import AssetManager

class TestAssetManager(unittest.TestCase):
    def setUp(self):
        self.assets = AssetManager()

    def test_init(self):
        self.assertEqual(self.assets.champ_data, {})
        self.assertEqual(self.assets.id_to_key, {})
        self.assertEqual(self.assets.name_to_id, {})

    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.Session.get')
    def test_load_champion_data_cache_miss(self, mock_get, mock_open_file, mock_exists, mock_makedirs):
        mock_exists.return_value = False

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "Aatrox": {"id": "Aatrox", "key": "266", "name": "Aatrox"},
                "Ahri": {"id": "Ahri", "key": "103", "name": "Ahri"}
            }
        }
        mock_get.return_value = mock_response

        # We need to mock json.load because mock_open read() returns magic mock when accessed by json.load
        with patch('json.load') as mock_json_load:
            mock_json_load.return_value = {
                "data": {
                    "Aatrox": {"id": "Aatrox", "key": "266", "name": "Aatrox"},
                    "Ahri": {"id": "Ahri", "key": "103", "name": "Ahri"}
                }
            }
            self.assets.ddragon_ver = "14.4.1"
            self.assets._load_champion_data()

        self.assertIn("Aatrox", self.assets.champ_data)
        self.assertEqual(self.assets.id_to_key[266], "Aatrox")
        self.assertEqual(self.assets.name_to_id["aatrox"], 266)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_champion_data_cache_hit(self, mock_open_file, mock_exists):
        mock_exists.return_value = True

        with patch('json.load') as mock_json_load:
            mock_json_load.return_value = {
                "data": {
                    "Aatrox": {"id": "Aatrox", "key": "266", "name": "Aatrox"},
                    "Ahri": {"id": "Ahri", "key": "103", "name": "Ahri"}
                }
            }
            self.assets.ddragon_ver = "14.4.1"
            self.assets._load_champion_data()

        self.assertIn("Aatrox", self.assets.champ_data)
        self.assertEqual(self.assets.id_to_key[266], "Aatrox")
        self.assertEqual(self.assets.name_to_id["aatrox"], 266)

if __name__ == '__main__':
    unittest.main()
