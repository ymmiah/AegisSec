from __future__ import annotations

import os
import time
from typing import Any

from ..http import HttpError, JsonHttpClient


class NVDConnector:
    name = "nvd"
    endpoint = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    # NVD public limits: 5 requests per rolling 30 s without a key, 50 with one.
    interval_without_key = 6.5
    interval_with_key = 0.7
    rate_limit_backoff = 35.0

    def __init__(self, http: JsonHttpClient | None = None, api_key: str | None = None, sleep=time.sleep, clock=time.monotonic):
        self.http = http or JsonHttpClient()
        self.api_key = api_key if api_key is not None else os.getenv("NVD_API_KEY")
        self._sleep = sleep
        self._clock = clock
        self._last_call: float | None = None

    def _throttle(self) -> None:
        interval = self.interval_with_key if self.api_key else self.interval_without_key
        if self._last_call is not None:
            wait = interval - (self._clock() - self._last_call)
            if wait > 0:
                self._sleep(wait)
        self._last_call = self._clock()

    def by_cve(self, cve_id: str) -> dict[str, Any] | None:
        headers = {"apiKey": self.api_key} if self.api_key else {}
        try:
            self._throttle()
            data = self.http.request_json("GET", self.endpoint, params={"cveId": cve_id}, headers=headers) or {}
        except HttpError as exc:
            if "HTTP 429" not in str(exc):
                raise
            # Rolling-window limit hit (e.g. shared IP): wait for the window to clear once.
            self._sleep(self.rate_limit_backoff)
            self._last_call = self._clock()
            data = self.http.request_json("GET", self.endpoint, params={"cveId": cve_id}, headers=headers) or {}
        vulnerabilities = data.get("vulnerabilities") or []
        if not vulnerabilities:
            return None
        return vulnerabilities[0].get("cve")
