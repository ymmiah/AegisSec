from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from .securehttp import SENSITIVE_HEADERS, opener, redact, validate_endpoint


class HttpError(RuntimeError):
    pass


@dataclass
class JsonHttpClient:
    timeout: int = 20
    retries: int = 2
    user_agent: str = "AegisSec-AI/1 vulnerability-intelligence"

    def request_json(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | list[Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        if params:
            encoded = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            url = f"{url}{'&' if '?' in url else '?'}{encoded}"
        payload = None
        merged = {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        if headers:
            merged.update(headers)
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            merged.setdefault("Content-Type", "application/json")

        # TLS is enforced and verified; credentials ride in headers only and are
        # redacted from any error text (config sets never_log_api_tokens: true).
        try:
            validate_endpoint(url)
        except ValueError as exc:
            raise HttpError(str(exc)) from None
        secrets = [v for k, v in merged.items() if k.lower() in SENSITIVE_HEADERS]

        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            req = urllib.request.Request(url, data=payload, method=method.upper(), headers=merged)
            try:
                with opener().open(req, timeout=self.timeout) as response:
                    raw = response.read()
                    if not raw:
                        return None
                    return json.loads(raw.decode("utf-8"))
            except urllib.error.HTTPError as exc:
                detail = redact(exc.read().decode("utf-8", errors="replace")[:500], secrets)
                last_error = HttpError(f"HTTP {exc.code} from {url}: {detail}")
                # Do not retry most client errors. 429 is retryable.
                if 400 <= exc.code < 500 and exc.code != 429:
                    break
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = exc
            if attempt < self.retries:
                time.sleep(0.75 * (2**attempt))
        raise HttpError(redact(str(last_error), secrets) if last_error else f"Request failed: {url}")
