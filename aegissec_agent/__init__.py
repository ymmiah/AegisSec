"""AegisSec runtime harness — a governed security agent around any LLM.

Public API:
    from aegissec_agent import Harness
    from aegissec_agent.providers import build_provider, StubProvider
"""

from .harness import Event, Harness
from .policy import Decision, PolicyGate
from .providers import (
    AnthropicProvider, AssistantTurn, LLMProvider, NvidiaProvider,
    OpenAIProvider, StubProvider, ToolCall, build_provider,
)
from .tools import Tool, ToolContext

__all__ = [
    "Harness", "Event", "PolicyGate", "Decision",
    "LLMProvider", "AnthropicProvider", "OpenAIProvider", "NvidiaProvider",
    "StubProvider", "AssistantTurn", "ToolCall", "build_provider",
    "Tool", "ToolContext",
]
__version__ = "1.0.0"
