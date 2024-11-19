import unittest
from unittest.mock import patch, MagicMock
from hummingbot.connector.exchange.payeer import payeer_web_utils
from hummingbot.core.web_assistant.connections.data_types import RESTRequest


class TestPayeerWebUtils(unittest.TestCase):

    def test_get_hb_id_headers(self):
        headers = payeer_web_utils.get_hb_id_headers()
        self.assertEqual(headers, {"request-source": "hummingbot-liq-mining"})

    def test_public_rest_url(self):
        url = payeer_web_utils.public_rest_url("test_path")
        self.assertEqual(url, "https://payeer.com/api/trade/test_path")

    def test_private_rest_url(self):
        url = payeer_web_utils.private_rest_url("test_path")
        self.assertEqual(url, "https://payeer.com/api/trade/test_path")

    @patch("hummingbot.connector.exchange.payeer.payeer_web_utils.PayeerRESTPreProcessor.pre_process")
    def test_payeer_rest_pre_processor(self, mock_pre_process):
        mock_request = MagicMock(spec=RESTRequest)
        mock_request.headers = None
        pre_processor = payeer_web_utils.PayeerRESTPreProcessor()
        pre_processor.pre_process(mock_request)
        self.assertTrue(mock_pre_process.called)

    @patch("hummingbot.connector.exchange.payeer.payeer_web_utils.create_throttler")
    @patch("hummingbot.connector.exchange.payeer.payeer_web_utils.WebAssistantsFactory")
    def test_build_api_factory(self, mock_factory, mock_create_throttler):
        mock_throttler = MagicMock()
        mock_create_throttler.return_value = mock_throttler
        mock_auth = MagicMock()
        factory = payeer_web_utils.build_api_factory(auth=mock_auth)
        self.assertTrue(mock_create_throttler.called)
        self.assertTrue(mock_factory.called)
        self.assertEqual(factory, mock_factory.return_value)

    @patch("hummingbot.connector.exchange.payeer.payeer_web_utils.time.time")
    def test_get_current_server_time(self, mock_time):
        mock_time.return_value = 1234567890.123
        server_time = payeer_web_utils.get_current_server_time()
        self.assertEqual(server_time, 1234567890123)


if __name__ == "__main__":
    unittest.main()
