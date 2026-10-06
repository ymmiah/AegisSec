"""LLM providers for the AegisSec harness.

Provider-agnostic by design (AegisSec is AI-agnostic). Each provider turns a
neutral message history and the AegisSec tool specs into its own wire format,
calls the API over the standard library (no third-party dependencies), and
returns a normalised assistant turn. A stub provider runs the whole loop
offline, which is how the tests exercise it.

Message history is a list of dicts:
  {"role": "user", "text": "..."}
  {"role": "assistant", "text": "...", "tool_calls": [{"id","name","input"}]}
  {"role": "tool", "id": "...", "name": "...", "output": "...", "is_error": bool}
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

from aegissec_vuln.securehttp import opener as _secure_opener
from aegissec_vuln.securehttp import redact as _redact
from aegissec_vuln.securehttp import validate_endpoint as _validate_endpoint


@dataclass
class ToolCall:
    id: str
    name: str
    input: dict


@dataclass
class AssistantTurn:
    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)


class ProviderError(RuntimeError):
    pass


def _check_endpoint(base_url: str) -> None:
    try:
        _validate_endpoint(base_url)
    except ValueError as exc:
        raise ProviderError(str(exc)) from None


def _post(url: str, headers: dict, body: dict, timeout: int = 120, secrets=()) -> dict:
    # TLS is enforced and verified; credentials ride only in headers, never in
    # the URL, and are redacted from any error text.
    try:
        _validate_endpoint(url)
    except ValueError as exc:
        raise ProviderError(str(exc)) from None
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={**headers, "content-type": "application/json"}, method="POST")
    try:
        with _secure_opener().open(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = _redact(exc.read().decode("utf-8", "replace")[:800], secrets)
        raise ProviderError(f"HTTP {exc.code} from {url}: {detail}") from None
    except urllib.error.URLError as exc:
        raise ProviderError(_redact(f"could not reach {url}: {exc.reason}", secrets)) from None


class LLMProvider:
    """Interface: turn system prompt + history + tools into one assistant turn."""

    name = "base"

    def complete(self, system: str, messages: list[dict], tools: list) -> AssistantTurn:
        raise NotImplementedError


class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, model="claude-opus-5-5", api_key=None, max_tokens=4096,
                 base_url="https://api.anthropic.com", version=None):
        self.model = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.max_tokens = max_tokens
        self.base_url = base_url.rstrip("/")
        self.version = version or os.getenv("ANTHROPIC_VERSION", "2023-06-01")
        if not self.api_key:
            raise ProviderError("ANTHROPIC_API_KEY is not set")
        _check_endpoint(self.base_url)

    def _messages(self, messages: list[dict]) -> list[dict]:
        out = []
        for m in messages:
            if m["role"] == "user":
                out.append({"role": "user", "content": m["text"]})
            elif m["role"] == "assistant":
                content = []
                if m.get("text"):
                    content.append({"type": "text", "text": m["text"]})
                for tc in m.get("tool_calls", []):
                    content.append({"type": "tool_use", "id": tc["id"], "name": tc["name"], "input": tc["input"]})
                out.append({"role": "assistant", "content": content})
            elif m["role"] == "tool":
                out.append({"role": "user", "content": [{
                    "type": "tool_result", "tool_use_id": m["id"],
                    "content": m["output"], "is_error": bool(m.get("is_error"))}]})
        return out

    def complete(self, system, messages, tools) -> AssistantTurn:
        body = {
            "model": self.model, "max_tokens": self.max_tokens, "system": system,
            "messages": self._messages(messages),
            "tools": [{"name": t.name, "description": t.description, "input_schema": t.input_schema} for t in tools],
        }
        resp = _post(f"{self.base_url}/v1/messages",
                     {"x-api-key": self.api_key, "anthropic-version": self.version}, body,
                     secrets=[self.api_key])
        turn = AssistantTurn()
        for block in resp.get("content", []):
            if block.get("type") == "text":
                turn.text += block["text"]
            elif block.get("type") == "tool_use":
                turn.tool_calls.append(ToolCall(block["id"], block["name"], block.get("input", {})))
        return turn


class OpenAIProvider(LLMProvider):
    """OpenAI and any OpenAI-compatible endpoint (local models, gateways, etc.)."""

    name = "openai"

    def __init__(self, model="gpt-4o", api_key=None, max_tokens=4096,
                 base_url="https://api.openai.com/v1", api_key_env="OPENAI_API_KEY"):
        self.model = model
        self.api_key = api_key or os.getenv(api_key_env)
        self.max_tokens = max_tokens
        self.base_url = base_url.rstrip("/")
        if not self.api_key:
            raise ProviderError(f"{api_key_env} is not set")
        _check_endpoint(self.base_url)

    def _messages(self, system: str, messages: list[dict]) -> list[dict]:
        out = [{"role": "system", "content": system}]
        for m in messages:
            if m["role"] == "user":
                out.append({"role": "user", "content": m["text"]})
            elif m["role"] == "assistant":
                msg = {"role": "assistant", "content": m.get("text") or None}
                if m.get("tool_calls"):
                    msg["tool_calls"] = [{"id": tc["id"], "type": "function",
                                          "function": {"name": tc["name"], "arguments": json.dumps(tc["input"])}}
                                         for tc in m["tool_calls"]]
                out.append(msg)
            elif m["role"] == "tool":
                out.append({"role": "tool", "tool_call_id": m["id"], "content": m["output"]})
        return out

    def complete(self, system, messages, tools) -> AssistantTurn:
        body = {
            "model": self.model, "max_tokens": self.max_tokens,
            "messages": self._messages(system, messages),
            "tools": [{"type": "function", "function": {
                "name": t.name, "description": t.description, "parameters": t.input_schema}} for t in tools],
        }
        resp = _post(f"{self.base_url}/chat/completions", {"authorization": f"Bearer {self.api_key}"}, body,
                     secrets=[self.api_key])
        msg = (resp.get("choices") or [{}])[0].get("message", {})
        turn = AssistantTurn(text=msg.get("content") or "")
        for tc in msg.get("tool_calls") or []:
            fn = tc.get("function", {})
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            turn.tool_calls.append(ToolCall(tc.get("id", fn.get("name", "call")), fn.get("name", ""), args))
        return turn


class NvidiaProvider(OpenAIProvider):
    """NVIDIA NIM — the NVIDIA API catalog or a self-hosted NIM container.

    Both speak the OpenAI chat-completions API, so this reuses OpenAIProvider
    and only changes the defaults. Point at a self-hosted NIM with base_url
    (or NVIDIA_API_BASE_URL), e.g. http://localhost:8000/v1. Pick a model that
    supports tool calling (the default does).
    """

    name = "nvidia"
    DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"

    def __init__(self, model="meta/llama-3.3-70b-instruct", api_key=None, max_tokens=4096,
                 base_url=None, api_key_env="NVIDIA_API_KEY"):
        base_url = base_url or os.getenv("NVIDIA_API_BASE_URL") or self.DEFAULT_BASE_URL
        super().__init__(model=model, api_key=api_key, max_tokens=max_tokens,
                         base_url=base_url, api_key_env=api_key_env)


class StubProvider(LLMProvider):
    """Deterministic provider for offline use and tests.

    ``script`` is a list of AssistantTurn, or callables (system, messages, tools)
    -> AssistantTurn, returned in order. Each call is recorded in ``calls``.
    """

    name = "stub"

    def __init__(self, script: list):
        self.script = list(script)
        self.calls: list[dict] = []

    def complete(self, system, messages, tools) -> AssistantTurn:
        self.calls.append({"system": system, "messages": [dict(m) for m in messages], "tools": [t.name for t in tools]})
        if not self.script:
            return AssistantTurn(text="(stub exhausted)")
        step = self.script.pop(0)
        return step(system, messages, tools) if callable(step) else step


def build_provider(name: str, **kwargs) -> LLMProvider:
    name = (name or "").lower()
    if name == "anthropic":
        return AnthropicProvider(**{k: v for k, v in kwargs.items() if v is not None})
    if name in ("openai", "openai-compatible"):
        return OpenAIProvider(**{k: v for k, v in kwargs.items() if v is not None})
    if name in ("nvidia", "nim", "nvidia-nim"):
        return NvidiaProvider(**{k: v for k, v in kwargs.items() if v is not None})
    raise ProviderError(f"unknown provider '{name}' (use anthropic, openai or nvidia, or pass a provider object)")
