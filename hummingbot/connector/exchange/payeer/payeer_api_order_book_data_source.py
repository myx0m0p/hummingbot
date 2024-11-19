import asyncio
from decimal import Decimal
from typing import Any, Dict, List, Optional

from hummingbot.connector.exchange.payeer import payeer_constants as CONSTANTS, payeer_web_utils as web_utils
from hummingbot.core.data_type.order_book_message import OrderBookMessage, OrderBookMessageType
from hummingbot.core.data_type.order_book_tracker_data_source import OrderBookTrackerDataSource
from hummingbot.core.web_assistant.connections.data_types import RESTMethod
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory
from hummingbot.logger import HummingbotLogger


class PayeerAPIOrderBookDataSource(OrderBookTrackerDataSource):
    _logger: Optional[HummingbotLogger] = None

    def __init__(
        self,
        trading_pairs: List[str],
        connector: "PayeerExchange",
        api_factory: Optional[WebAssistantsFactory] = None,
    ):
        super().__init__(trading_pairs)
        self._connector = connector
        self._api_factory = api_factory

    async def get_last_traded_prices(self, trading_pairs: List[str]) -> Dict[str, float]:
        return await self._connector.get_last_traded_prices(trading_pairs=trading_pairs)

    async def _request_order_book_snapshot(self, trading_pair: str) -> Dict[str, Any]:
        """
        Retrieves a copy of the full order book from the exchange, for a particular trading pair.

        :param trading_pair: the trading pair for which the order book will be retrieved

        :return: the response from the exchange (JSON dictionary)
        """
        params = {"pair": await self._connector.exchange_symbol_associated_to_pair(trading_pair=trading_pair)}

        rest_assistant = await self._api_factory.get_rest_assistant()
        data = await rest_assistant.execute_request(
            url=web_utils.public_rest_url(path_url=CONSTANTS.DEPTH_PATH_URL),
            params=params,
            method=RESTMethod.GET,
            throttler_limit_id=CONSTANTS.DEPTH_PATH_URL,
        )

        return data

    async def _order_book_snapshot(self, trading_pair: str) -> OrderBookMessage:
        snapshot_response: Dict[str, Any] = await self._request_order_book_snapshot(trading_pair)
        snapshot_timestamp = float(snapshot_response["timestamp"]) / 1000

        order_book_message_content = {
            "trading_pair": trading_pair,
            "update_id": snapshot_timestamp,
            "bids": snapshot_response["bids"],
            "asks": snapshot_response["asks"],
        }
        snapshot_msg: OrderBookMessage = OrderBookMessage(
            OrderBookMessageType.SNAPSHOT, order_book_message_content, snapshot_timestamp
        )

        return snapshot_msg

    async def _parse_trade_message(self, raw_message: Dict[str, Any], message_queue: asyncio.Queue):
        trading_pair = await self._connector.trading_pair_associated_to_exchange_symbol(symbol=raw_message["pair"])
        for trade_data in raw_message["trades"]:
            timestamp: float = trade_data["timestamp"] / 1000
            message_content = {
                "trade_id": timestamp,  # trade id isn't provided so using timestamp instead
                "trading_pair": trading_pair,
                "trade_type": float(trade_data["type"]),
                "amount": Decimal(trade_data["amount"]),
                "price": Decimal(trade_data["price"]),
            }
            trade_message: Optional[OrderBookMessage] = OrderBookMessage(
                message_type=OrderBookMessageType.TRADE, content=message_content, timestamp=timestamp
            )

            message_queue.put_nowait(trade_message)

    async def _parse_order_book_diff_message(self, raw_message: Dict[str, Any], message_queue: asyncio.Queue):
        diff_data: Dict[str, Any] = raw_message
        timestamp: float = diff_data["timestamp"] / 1000

        trading_pair = await self._connector.trading_pair_associated_to_exchange_symbol(symbol=raw_message["pair"])

        message_content = {
            "trading_pair": trading_pair,
            "update_id": timestamp,
            "bids": diff_data["bids"],
            "asks": diff_data["asks"],
        }
        diff_message: OrderBookMessage = OrderBookMessage(OrderBookMessageType.DIFF, message_content, timestamp)

        message_queue.put_nowait(diff_message)

    async def _fetch_order_book_data(self):
        while True:
            try:
                for trading_pair in self._trading_pairs:
                    snapshot_msg = await self._order_book_snapshot(trading_pair)
                    self._message_queue[self._snapshot_messages_queue_key].put_nowait(snapshot_msg)
            except asyncio.CancelledError:
                raise
            except Exception:
                self.logger().exception("Unexpected error occurred fetching order book data...")
                await asyncio.sleep(5.0)
            await asyncio.sleep(1.0)

    async def start(self):
        self._fetch_order_book_data_task = asyncio.create_task(self._fetch_order_book_data())
        await super().start()

    async def stop(self):
        self._fetch_order_book_data_task.cancel()
        await super().stop()
