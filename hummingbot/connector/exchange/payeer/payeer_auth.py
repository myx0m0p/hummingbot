import hashlib
import hmac
import time
from typing import Any, Dict, Optional

from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTRequest, WSRequest


class PayeerAuth(AuthBase):
    """
    Auth class required by Payeer API
    """

    def __init__(self, api_key: str, secret_key: str, time_provider: TimeSynchronizer):
        self.api_key: str = api_key
        self.secret_key: str = secret_key
        self.time_provider: TimeSynchronizer = time_provider

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        """
        Adds the server time and the signature to the request, required for authenticated interactions. It also adds
        the required parameter in the request header.
        :param request: the request to be configured for authenticated interaction
        """
        headers = {}
        if request.headers is not None:
            headers.update(request.headers)
        headers.update(self.get_auth_headers(request=request))
        request.headers = headers

        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        This method is intended to configure a websocket request to be authenticated. Payeer does not use this
        functionality
        """
        return request  # pass-through

    def get_auth_headers(self, request: RESTRequest) -> Dict[str, Any]:
        """
        Generates authentication signature and return it in a dictionary along with other inputs
        :param path_url: URL of the auth API endpoint
        :param data: data to be included in the headers
        :return: a dictionary of request info including the request signature
        """

        path_url = f"{request.url.split('/api/trade/')[-1]}"
        return {
            "API-ID": self.api_key,
            "API-SIGN": self._generate_signature(path_url, request.data),
        }

    def _generate_signature(self, action: str, body: Optional[str] = None) -> str:
        unsigned_signature = action
        if body is not None:
            unsigned_signature += body

        signature = hmac.new(
            self.secret_key.encode("utf-8"), unsigned_signature.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return signature

    def _time(self) -> float:
        return time.time()
