import unittest
from unittest.mock import patch
from hummingbot.connector.exchange.payeer import payeer_utils


class TestPayeerUtils(unittest.TestCase):

    @patch("hummingbot.connector.exchange.payeer.payeer_utils._time")
    def test_get_ms_timestamp(self, mock_time):
        mock_time.return_value = 1234567890.123
        timestamp = payeer_utils.get_ms_timestamp()
        self.assertEqual(timestamp, 1234567890123)

    def test_is_pair_information_valid(self):
        valid_pair_info = {"statusCode": "Normal"}
        invalid_pair_info = {"statusCode": "Disabled"}
        self.assertTrue(payeer_utils.is_pair_information_valid(valid_pair_info))
        self.assertFalse(payeer_utils.is_pair_information_valid(invalid_pair_info))


if __name__ == "__main__":
    unittest.main()
