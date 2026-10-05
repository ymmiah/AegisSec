from __future__ import annotations

from typing import Any, Iterable

from ..http import JsonHttpClient
from ..models import Component


class OSVConnector:
    name = "osv"
    base_url = "https://api.osv.dev/v1"

    def __init__(self, http: JsonHttpClient | None = None):
        self.http = http or JsonHttpClient()

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
            all_results.extend([entry.get("vulns", []) for entry in results])
        return all_results
