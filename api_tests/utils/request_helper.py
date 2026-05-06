import logging
from typing import Dict, Optional

import requests

logger = logging.getLogger(__name__)


class RequestHelper:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        logger.info("→ %s %s", method.upper(), url)
        if kwargs.get("json"):
            logger.debug("  Body: %s", kwargs["json"])
        if kwargs.get("params"):
            logger.debug("  Params: %s", kwargs["params"])

    def _log_response(self, response: requests.Response) -> None:
        logger.info("← %s %s", response.status_code, response.url)
        try:
            logger.debug("  Response: %s", response.json())
        except Exception:
            logger.debug("  Response: %s", response.text[:200])

    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        url = self._build_url(endpoint)
        self._log_request("GET", url, params=params)
        response = self.session.get(url, params=params, timeout=self.timeout)
        self._log_response(response)
        return response

    def post(self, endpoint: str, payload: Optional[Dict] = None) -> requests.Response:
        url = self._build_url(endpoint)
        self._log_request("POST", url, json=payload)
        response = self.session.post(url, json=payload, timeout=self.timeout)
        self._log_response(response)
        return response

    def put(self, endpoint: str, payload: Optional[Dict] = None) -> requests.Response:
        url = self._build_url(endpoint)
        self._log_request("PUT", url, json=payload)
        response = self.session.put(url, json=payload, timeout=self.timeout)
        self._log_response(response)
        return response

    def delete(self, endpoint: str) -> requests.Response:
        url = self._build_url(endpoint)
        self._log_request("DELETE", url)
        response = self.session.delete(url, timeout=self.timeout)
        self._log_response(response)
        return response
