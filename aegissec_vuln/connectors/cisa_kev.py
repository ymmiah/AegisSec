from __future__ import annotations

from typing import Any

from ..http import JsonHttpClient


class CisaKevConnector:
    name = "cisa_kev"
    feed_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

    def __init__(self, http: JsonHttpClient | None = None):
        self.http = http or JsonHttpClient(timeout=30)
        self._catalog: dict[str, dict[str, Any]] | None = None

    def catalog(self) -> dict[str, dict[str, Any]]:
        if self._catalog is None:
            data = self.http.request_json("GET", self.feed_url) or {}
            self._catalog = {
                str(item.get("cveID", "")).upper(): item
                for item in data.get("vulnerabilities", [])
                if item.get("cveID")
            }
        return self._catalog

    def by_cve(self, cve_id: str) -> dict[str, Any] | None:
        return self.catalog().get(cve_id.upper())
