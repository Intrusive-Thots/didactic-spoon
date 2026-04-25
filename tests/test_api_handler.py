import unittest
from unittest.mock import MagicMock, patch
import os

from services.api_handler import LCUClient

class TestLCUClient(unittest.TestCase):
    def setUp(self):
        self.client = LCUClient()

    def test_init(self):
        self.assertFalse(self.client.is_connected)
        self.assertIsNone(self.client.port)
        self.assertIsNone(self.client.auth_token)

    @patch('psutil.process_iter')
    @patch('os.path.exists')
    @patch('builtins.open')
    @patch('requests.get')
    def test_connect_success(self, mock_get, mock_open, mock_exists, mock_process_iter):
        mock_proc = MagicMock()
        mock_proc.info = {'name': 'LeagueClientUx.exe'} # For the attrs=['name'] call
        mock_proc.cwd.return_value = "C:\\Riot Games\\League of Legends"
        mock_process_iter.return_value = [mock_proc]

        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = "LeagueClient:1234:54321:password:https"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Override cooldown
        self.client._last_scan_time = 0
        self.assertTrue(self.client.connect())
        self.assertTrue(self.client.is_connected)
        self.assertEqual(self.client.port, "54321")
        self.assertEqual(self.client.auth_token, "password")

    @patch('services.api_handler.requests.Session.request')
    def test_request_success(self, mock_request):
        self.client.is_connected = True
        self.client.port = "1234"
        self.client.base_url = "https://127.0.0.1:1234" # Need to set base_url
        self.client.headers = {"Authorization": "Basic xxx"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        result = self.client.request("GET", "/test")
        self.assertEqual(result, mock_response)

    def test_request_not_connected(self):
        self.client.is_connected = False
        result = self.client.request("GET", "/test")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
