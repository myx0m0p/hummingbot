import unittest
from decimal import Decimal
from unittest.mock import AsyncMock, patch

from hummingbot.connector.exchange.payeer.payeer_exchange import PayeerExchange
from hummingbot.core.data_type.common import OrderType, TradeType
from hummingbot.core.data_type.in_flight_order import InFlightOrder


class TestPayeerExchange(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.secret_key = "test_secret_key"
        self.trading_pair = "BTC-USDT"
        self.exchange = PayeerExchange(
            client_config_map=None,
            payeer_api_key=self.api_key,
            payeer_secret_key=self.secret_key,
            trading_pairs=[self.trading_pair],
        )

    @patch("hummingbot.connector.exchange.payeer.payeer_exchange.PayeerExchange._api_post")
    def test_place_order(self, mock_api_post):
        mock_api_post.return_value = {
            "code": 0,
            "data": {
                "info": {
                    "orderId": "test_order_id",
                    "timestamp": 1620000000,
                }
            }
        }

        order_id = "test_order_id"
        trading_pair = self.trading_pair
        amount = Decimal("0.01")
        trade_type = TradeType.BUY
        order_type = OrderType.LIMIT
        price = Decimal("50000.0")

        result = self.exchange._place_order(
            order_id=order_id,
            trading_pair=trading_pair,
            amount=amount,
            trade_type=trade_type,
            order_type=order_type,
            price=price,
        )

        self.assertEqual(result, ("test_order_id", 1620000000))

    @patch("hummingbot.connector.exchange.payeer.payeer_exchange.PayeerExchange._api_delete")
    def test_cancel_order(self, mock_api_delete):
        mock_api_delete.return_value = {
            "code": 0,
        }

        order_id = "test_order_id"
        tracked_order = InFlightOrder(
            client_order_id=order_id,
            exchange_order_id="test_exchange_order_id",
            trading_pair=self.trading_pair,
            order_type=OrderType.LIMIT,
            trade_type=TradeType.BUY,
            price=Decimal("50000.0"),
            amount=Decimal("0.01"),
        )

        result = self.exchange._place_cancel(order_id=order_id, tracked_order=tracked_order)

        self.assertTrue(result)

    @patch("hummingbot.connector.exchange.payeer.payeer_exchange.PayeerExchange._api_get")
    def test_fetch_order_status(self, mock_api_get):
        mock_api_get.return_value = {
            "code": 0,
            "data": {
                "orderId": "test_order_id",
                "status": "New",
            }
        }

        tracked_order = InFlightOrder(
            client_order_id="test_order_id",
            exchange_order_id="test_exchange_order_id",
            trading_pair=self.trading_pair,
            order_type=OrderType.LIMIT,
            trade_type=TradeType.BUY,
            price=Decimal("50000.0"),
            amount=Decimal("0.01"),
        )

        result = self.exchange._request_order_status(tracked_order=tracked_order)

        self.assertEqual(result.new_state, "New")

    @patch("hummingbot.connector.exchange.payeer.payeer_exchange.PayeerExchange._api_get")
    def test_fetch_trading_pairs(self, mock_api_get):
        mock_api_get.return_value = {
            "code": 0,
            "data": [
                {
                    "symbol": "BTC/USDT",
                    "statusCode": "Normal",
                }
            ]
        }

        result = self.exchange.trading_pairs

        self.assertEqual(result, ["BTC-USDT"])

    @patch("hummingbot.connector.exchange.payeer.payeer_exchange.PayeerExchange._api_get")
    def test_fetch_order_book_data(self, mock_api_get):
        mock_api_get.return_value = {
            "code": 0,
            "data": {
                "bids": [
                    ["50000.0", "0.01"]
                ],
                "asks": [
                    ["51000.0", "0.01"]
                ]
            }
        }

        result = self.exchange.get_all_pairs_prices()

        self.assertEqual(result["data"][0]["bids"], [["50000.0", "0.01"]])
        self.assertEqual(result["data"][0]["asks"], [["51000.0", "0.01"]])


if __name__ == "__main__":
    unittest.main()
