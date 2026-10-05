from __future__ import annotations

import os
from typing import Any

from ..http import JsonHttpClient


class GitHubAdvisoryConnector:
    name = "github_advisory"
    endpoint = "https://api.github.com/advisories"

    def __init__(self, http: JsonHttpClient | None = None, token: str | None = None):
        self.http = http or JsonHttpClient()
        self.token = token if token is not None else os.getenv("GITHUB_TOKEN")

    def by_cve(self, cve_id: str) -> list[dict[str, Any]]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        data = self.http.request_json("GET", self.endpoint, params={"cve_id": cve_id}, headers=headers)
        return data if isinstance(data, list) else []
