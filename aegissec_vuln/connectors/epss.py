from __future__ import annotations

from typing import Any, Iterable

from ..http import JsonHttpClient


class EPSSConnector:
    name = "epss"
    endpoint = "https://api.first.org/data/v1/epss"

    def __init__(self, http: JsonHttpClient | None = None):
        self.http = http or JsonHttpClient()

    def by_cves(self, cves: Iterable[str]) -> dict[str, dict[str, Any]]:
        unique = sorted({str(c).upper() for c in cves if c})
        if not unique:
            return {}
        results: dict[str, dict[str, Any]] = {}
        # FIRST accepts comma-separated CVEs; keep URLs comfortably bounded.
        for start in range(0, len(unique), 80):
            batch = unique[start : start + 80]
            data = self.http.request_json("GET", self.endpoint, params={"cve": ",".join(batch)}) or {}
            for item in data.get("data", []) or []:
                cve = str(item.get("cve", "")).upper()
                if cve:
                    results[cve] = item
        return results
