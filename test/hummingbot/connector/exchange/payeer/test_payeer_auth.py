import unittest
from unittest.mock import patch, MagicMock
from hummingbot.connector.exchange.payeer.payeer_auth import PayeerAuth
from hummingbot.core.web_assistant.connections.data_types import RESTRequest


class TestPayeerAuth(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.secret_key = "test_secret_key"
        self.auth = PayeerAuth(self.api_key, self.secret_key)

    @patch("hummingbot.connector.exchange.payeer.payeer_auth.PayeerAuth._time")
    def test_get_auth_headers(self, mock_time):
        mock_time.return_value = 1234567890
        path_url = "/api/test"
        expected_headers = {
            "API-ID": self.api_key,
            "API-SIGN": "d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2",
            "API-TIMESTAMP": "1234567890000",
        }
        headers = self.auth.get_auth_headers(path_url)
        self.assertEqual(headers, expected_headers)

    @patch("hummingbot.connector.exchange.payeer.payeer_auth.PayeerAuth._time")
    def test_rest_authenticate(self, mock_time):
        mock_time.return_value = 1234567890
        request = RESTRequest(method="GET", url="https://payeer.com/api/test", headers={})
        authenticated_request = self.auth.rest_authenticate(request)
        self.assertIn("API-ID", authenticated_request.headers)
        self.assertIn("API-SIGN", authenticated_request.headers)
        self.assertIn("API-TIMESTAMP", authenticated_request.headers)


if __name__ == "__main__":
    unittest.main()
