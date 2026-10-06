"""Hardened HTTP primitives shared by the vulnerability connectors and the
agent providers.

Industry-standard controls for every outbound API call:

- **TLS enforced and verified** — HTTPS only, with certificate and hostname
  verification (``ssl.create_default_context``). Plain HTTP is allowed only to
  loopback/private hosts (a self-hosted model or NIM on localhost), never to a
  remote host, so a bearer token is never sent in cleartext over the network.
- **No credential leakage on redirect** — if a response redirects to a
  different host, the Authorization / API-key headers are stripped before the
  request is followed.
- **No secrets in logs or errors** — known secret values are redacted from any
  error text, and auth headers are never logged.
- **Corporate TLS inspection** — set ``AEGISSEC_CA_BUNDLE`` to a CA file to
  trust an inspecting proxy without ever disabling verification.

Nothing here can be configured to skip verification; that is deliberate.
"""

from __future__ import annotations

import ipaddress
import os
import re
import ssl
import urllib.request
from functools import lru_cache
from urllib.parse import urlsplit

SENSITIVE_HEADERS = {"authorization", "x-api-key", "apikey", "api-key", "proxy-authorization"}
# Shapes of common provider keys, redacted even if the exact value is unknown.
_KEY_PATTERNS = [
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]+", re.I),
    re.compile(r"\b(?:sk|nvapi|xai|gsk|ghp|github_pat)[-_][A-Za-z0-9._\-]{6,}"),
]


def validate_endpoint(url: str) -> None:
    """Allow HTTPS anywhere; allow HTTP only to a loopback/private host."""
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    if scheme == "https":
        return
    if scheme != "http":
        raise ValueError(f"unsupported URL scheme '{parts.scheme}' (use https)")
    host = parts.hostname or ""
    if host in ("localhost", "localhost.localdomain") or host.endswith(".local"):
        return
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        raise ValueError(f"refusing plain HTTP to remote host '{host}': use https so credentials are not sent in cleartext") from None
    if ip.is_loopback or ip.is_private:
        return
    raise ValueError(f"refusing plain HTTP to non-local address '{host}': use https so credentials are not sent in cleartext")


@lru_cache(maxsize=1)
def ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context(cafile=os.getenv("AEGISSEC_CA_BUNDLE") or None)
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    return ctx


class _StripAuthOnRedirect(urllib.request.HTTPRedirectHandler):
    """Drop Authorization / API-key headers when a redirect changes host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and urlsplit(newurl).hostname != urlsplit(req.full_url).hostname:
            for name in list(new.headers):
                if name.lower().replace("_", "-") in SENSITIVE_HEADERS:
                    del new.headers[name]
            for name in list(getattr(new, "unredirected_hdrs", {})):
                if name.lower().replace("_", "-") in SENSITIVE_HEADERS:
                    del new.unredirected_hdrs[name]
        return new


@lru_cache(maxsize=1)
def opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(
        urllib.request.ProxyHandler(),  # honours *_PROXY env; no credentials stored here
        urllib.request.HTTPSHandler(context=ssl_context()),
        _StripAuthOnRedirect(),
    )


def redact(text: str, secrets=()) -> str:
    out = text
    for secret in secrets:
        if secret and len(str(secret)) >= 6:
            out = out.replace(str(secret), "***")
    for pat in _KEY_PATTERNS:
        out = pat.sub("***", out)
    return out
