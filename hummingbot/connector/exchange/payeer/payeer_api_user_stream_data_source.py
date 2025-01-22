import asyncio
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from hummingbot.connector.exchange.payeer import payeer_constants as CONSTANTS
from hummingbot.connector.exchange.payeer.payeer_auth import PayeerAuth
from hummingbot.core.data_type.user_stream_tracker_data_source import UserStreamTrackerDataSource
from hummingbot.core.web_assistant.connections.data_types import RESTMethod
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory
from hummingbot.logger import HummingbotLogger

if TYPE_CHECKING:
    from hummingbot.connector.exchange.payeer.payeer_exchange import PayeerExchange


class PayeerAPIUserStreamDataSource(UserStreamTrackerDataSource):
    _logger: Optional[HummingbotLogger] = None

    def __init__(
        self,
        auth: PayeerAuth,
        trading_pairs: List[str],
        connector: "PayeerExchange",
        api_factory: WebAssistantsFactory,
    ):
        super().__init__()
        self._auth: PayeerAuth = auth
        self._api_factory = api_factory
        self._trading_pairs = trading_pairs or []
        self._connector = connector

    async def _fetch_user_stream_data(self):
        while True:
            try:
                await self._fetch_order_status()
                await self._fetch_balance()
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                raise
            except Exception:
                self.logger().exception("Unexpected error while fetching user stream data.")
                await asyncio.sleep(5)

    async def _fetch_order_status(self):
        for trading_pair in self._trading_pairs:
            symbol = await self._connector.exchange_symbol_associated_to_pair(trading_pair=trading_pair)
            params = {"symbol": symbol}
            rest_assistant = await self._api_factory.get_rest_assistant()
            order_status_data = await rest_assistant.execute_request(
                url=CONSTANTS.PRIVATE_REST_URL + CONSTANTS.ORDER_STATUS_PATH_URL,
                params=params,
                method=RESTMethod.GET,
                throttler_limit_id=CONSTANTS.ORDER_STATUS_PATH_URL,
                headers=self._auth.get_auth_headers(CONSTANTS.ORDER_STATUS_PATH_URL),
            )
            self._process_order_status(order_status_data)

    async def _fetch_balance(self):
        rest_assistant = await self._api_factory.get_rest_assistant()
        balance_data = await rest_assistant.execute_request(
            url=CONSTANTS.PRIVATE_REST_URL + CONSTANTS.BALANCE_PATH_URL,
            method=RESTMethod.GET,
            throttler_limit_id=CONSTANTS.BALANCE_PATH_URL,
            headers=self._auth.get_auth_headers(CONSTANTS.BALANCE_PATH_URL),
        )
        self._process_balance(balance_data)

    def _process_order_status(self, order_status_data: Dict[str, Any]):
        # Process order status data and update user stream accordingly
        pass

    def _process_balance(self, balance_data: Dict[str, Any]):
        # Process balance data and update user stream accordingly
        pass
