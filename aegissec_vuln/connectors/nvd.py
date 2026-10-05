from __future__ import annotations

import os
from typing import Any

from ..http import JsonHttpClient


class NVDConnector:
    name = "nvd"
    endpoint = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def __init__(self, http: JsonHttpClient | None = None, api_key: str | None = None):
        self.http = http or JsonHttpClient()
        self.api_key = api_key if api_key is not None else os.getenv("NVD_API_KEY")

    def by_cve(self, cve_id: str) -> dict[str, Any] | None:
        headers = {"apiKey": self.api_key} if self.api_key else {}
        data = self.http.request_json("GET", self.endpoint, params={"cveId": cve_id}, headers=headers) or {}
        vulnerabilities = data.get("vulnerabilities") or []
        if not vulnerabilities:
            return None
        return vulnerabilities[0].get("cve")
