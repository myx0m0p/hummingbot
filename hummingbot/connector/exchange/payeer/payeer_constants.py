from hummingbot.core.api_throttler.data_types import LinkedLimitWeightPair, RateLimit
from hummingbot.core.data_type.in_flight_order import OrderState

MAX_ORDER_ID_LEN = 32

PING_TIMEOUT = 15.0
DEFAULT_DOMAIN = ""
HBOT_ORDER_ID_PREFIX = "HMBot"

EXCHANGE_NAME = "payeer"
PUBLIC_REST_URL = "https://payeer.com/api/trade/"
PRIVATE_REST_URL = "https://payeer.com/api/trade/"
WS_URL = "wss://payeer.com/api/trade/ws"
PRIVATE_WS_URL = "wss://payeer.com/api/trade/ws"

# REST API ENDPOINTS
ORDER_PATH_URL = "order_create"
ORDER_CANCEL_PATH_URL = "order_cancel"
ORDER_STATUS_PATH_URL = "order_status"
BALANCE_PATH_URL = "account"
TICKER_PATH_URL = "ticker"
PRODUCTS_PATH_URL = "info"
TRADES_PATH_URL = "trades"
DEPTH_PATH_URL = "depth"
INFO_PATH_URL = "info"
STREAM_PATH_URL = "stream"

SERVER_LIMIT_INFO = "risk-limit-info"

# WS API ENDPOINTS
SUB_ENDPOINT_NAME = "sub"
PONG_ENDPOINT_NAME = "pong"
TRADE_TOPIC_ID = "trades"
DIFF_TOPIC_ID = "depth"
PING_TOPIC_ID = "ping"
ACCOUNT_TYPE = "CASH"
BALANCE_EVENT_TYPE = "balance"
ORDER_CHANGE_EVENT_TYPE = "order"

# OrderStates

ORDER_STATE = {
    "PendingNew": OrderState.PENDING_CREATE,
    "New": OrderState.OPEN,
    "Filled": OrderState.FILLED,
    "PartiallyFilled": OrderState.PARTIALLY_FILLED,
    "Canceled": OrderState.CANCELED,
    "Rejected": OrderState.FAILED,
}

# Payeer has multiple pools for API request limits
# Any call increases call rate in ALL pool, so e.g. a order_create call will contribute to both ALL and order_create pools.
ALL_ENDPOINTS_LIMIT = "All"
RATE_LIMITS = [
    RateLimit(limit_id=ALL_ENDPOINTS_LIMIT, limit=100, time_interval=1),
    RateLimit(
        limit_id=ORDER_PATH_URL, limit=50, time_interval=1, linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)]
    ),
    RateLimit(
        limit_id=ORDER_CANCEL_PATH_URL,
        limit=50,
        time_interval=1,
        linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)],
    ),
    RateLimit(
        limit_id=ORDER_STATUS_PATH_URL,
        limit=50,
        time_interval=1,
        linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)],
    ),
    RateLimit(
        limit_id=BALANCE_PATH_URL,
        limit=100,
        time_interval=1,
        linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)],
    ),
    RateLimit(
        limit_id=TICKER_PATH_URL, limit=100, time_interval=1, linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)]
    ),
    RateLimit(
        limit_id=PRODUCTS_PATH_URL,
        limit=100,
        time_interval=1,
        linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)],
    ),
    RateLimit(
        limit_id=TRADES_PATH_URL, limit=100, time_interval=1, linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)]
    ),
    RateLimit(
        limit_id=DEPTH_PATH_URL, limit=100, time_interval=1, linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)]
    ),
    RateLimit(
        limit_id=INFO_PATH_URL, limit=100, time_interval=1, linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)]
    ),
    RateLimit(
        limit_id=SUB_ENDPOINT_NAME,
        limit=100,
        time_interval=1,
        linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)],
    ),
    RateLimit(
        limit_id=PONG_ENDPOINT_NAME,
        limit=100,
        time_interval=1,
        linked_limits=[LinkedLimitWeightPair(ALL_ENDPOINTS_LIMIT)],
    ),
]
