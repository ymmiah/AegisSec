from __future__ import annotations

from typing import Any, Iterable
from urllib.parse import quote

from ..http import JsonHttpClient
from ..models import Component


class OSVConnector:
    name = "osv"
    base_url = "https://api.osv.dev/v1"

    def __init__(self, http: JsonHttpClient | None = None):
        self.http = http or JsonHttpClient()
        self._vuln_cache: dict[str, dict[str, Any]] = {}

    def get_vuln(self, vuln_id: str) -> dict[str, Any]:
        """Fetch the full OSV record (aliases, severity, affected ranges, references)."""
        if vuln_id not in self._vuln_cache:
            self._vuln_cache[vuln_id] = self.http.request_json("GET", f"{self.base_url}/vulns/{quote(vuln_id, safe='')}") or {}
        return self._vuln_cache[vuln_id]

    def _hydrate(self, vuln: dict[str, Any]) -> dict[str, Any]:
        # /querybatch returns only {"id", "modified"} per vulnerability. Without the
        # full record there are no CVE aliases, severity or fixed versions, so EPSS,
        # CISA KEV and NVD enrichment can never run and every finding scores low.
        vuln_id = vuln.get("id")
        if not vuln_id or "aliases" in vuln or "affected" in vuln:
            return vuln
        try:
            full = self.get_vuln(vuln_id)
        except Exception:
            return vuln
        return full or vuln

    def query_component(self, component: Component) -> list[dict[str, Any]]:
        data = self.http.request_json("POST", f"{self.base_url}/query", body=component.osv_query()) or {}
        return data.get("vulns", [])

    def query_batch(self, components: Iterable[Component], chunk_size: int = 100) -> list[list[dict[str, Any]]]:
        items = list(components)
        all_results: list[list[dict[str, Any]]] = []
        for start in range(0, len(items), chunk_size):
            chunk = items[start : start + chunk_size]
            body = {"queries": [component.osv_query() for component in chunk]}
            data = self.http.request_json("POST", f"{self.base_url}/querybatch", body=body) or {}
            results = data.get("results", [])
            if len(results) != len(chunk):
                raise RuntimeError("OSV querybatch returned an unexpected result count")
            all_results.extend([[self._hydrate(v) for v in entry.get("vulns", []) or []] for entry in results])
        return all_results
