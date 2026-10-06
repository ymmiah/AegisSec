#!/usr/bin/env python3
"""AegisSec runtime harness — CLI.

Run AegisSec as a governed security chatbot over any LLM provider.

    # interactive, Anthropic
    ANTHROPIC_API_KEY=... python scripts/aegissec_agent.py --agent security-appsec-engineer

    # one-shot, OpenAI-compatible endpoint
    OPENAI_API_KEY=... python scripts/aegissec_agent.py --provider openai \\
        --once "Scan ./sbom.cdx.json for vulnerabilities and give me the fix plan"

    # offline: list what is available
    python scripts/aegissec_agent.py --list-agents
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aegissec_agent import Harness, personas  # noqa: E402
from aegissec_agent.providers import ProviderError, build_provider  # noqa: E402

DIM, BOLD, RESET = "\033[2m", "\033[1m", "\033[0m"


def _supports_colour() -> bool:
    return sys.stdout.isatty()


def _event_printer(verbose: bool):
    c = _supports_colour()
    d = (lambda s: f"{DIM}{s}{RESET}") if c else (lambda s: s)
    b = (lambda s: f"{BOLD}{s}{RESET}") if c else (lambda s: s)

    def printer(event):
        if event.type == "tool_call":
            print(d(f"  ⚙ {event.data['name']}({', '.join(f'{k}={v!r}' for k, v in event.data['input'].items())})"))
        elif event.type == "policy" and not event.data["allowed"]:
            print(d(f"  🔒 {event.data['reason']}"))
        elif event.type == "tool_result" and verbose:
            head = (event.data["output"].splitlines() or [""])[0]
            print(d(f"    → {head[:100]}"))
    return printer


def _approver(tool_name: str, summary: str) -> bool:
    print(f"\n{BOLD}AegisSec needs approval{RESET} to run {tool_name}:\n  {summary}")
    try:
        return input("Approve? [y/N] ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


def main() -> int:
    p = argparse.ArgumentParser(prog="aegissec-agent", description="AegisSec runtime harness (governed security chatbot)")
    p.add_argument("--provider", default="anthropic", help="anthropic or openai (default anthropic)")
    p.add_argument("--model", help="model id (provider default otherwise)")
    p.add_argument("--base-url", help="override API base URL (e.g. an OpenAI-compatible gateway)")
    p.add_argument("--api-key-env", help="env var holding the key (OpenAI providers; default OPENAI_API_KEY)")
    p.add_argument("--agent", default="aegissec-operator", help="persona slug (see --list-agents)")
    p.add_argument("--workdir", default=".", help="sandbox root for file tools (default: cwd)")
    p.add_argument("--scope", help="engagement scope YAML to load (enables gated active testing if it passes)")
    p.add_argument("--context", help="asset-context YAML for scans")
    p.add_argument("--approve", choices=["deny", "prompt", "auto"], help="how to handle gated actions (default: prompt on a TTY, else deny)")
    p.add_argument("--max-steps", type=int, default=12)
    p.add_argument("--once", help="run a single message and exit")
    p.add_argument("--verbose", action="store_true", help="print tool result heads")
    p.add_argument("--list-agents", action="store_true")
    p.add_argument("--list-skills", action="store_true")
    a = p.parse_args()

    if a.list_agents:
        for e in personas.list_personas():
            print(f"{e['slug']:<42} {e['division']:<10} {e['name']}")
        return 0
    if a.list_skills:
        for d in sorted((ROOT / "skills/aegissec").glob("*/SKILL.md")):
            print(d.parent.name)
        return 0

    approve = a.approve or ("prompt" if sys.stdin.isatty() else "deny")
    kwargs = {"model": a.model, "base_url": a.base_url}
    if a.api_key_env:
        kwargs["api_key_env"] = a.api_key_env
    try:
        provider = build_provider(a.provider, **kwargs)
    except ProviderError as exc:
        print(f"Provider error: {exc}", file=sys.stderr)
        return 2

    try:
        harness = Harness(
            provider, agent=a.agent, workdir=a.workdir, approval_mode=approve,
            approver=_approver, scope_file=a.scope, context_file=a.context,
            max_steps=a.max_steps, on_event=_event_printer(a.verbose),
        )
    except KeyError as exc:
        print(exc, file=sys.stderr)
        return 2

    print(f"{BOLD}AegisSec{RESET} · {harness.persona.name} · {provider.name} · approvals: {approve}"
          + ("  · scope loaded" if harness.gate.scope_ok else ""))

    def turn(msg: str):
        try:
            answer = harness.ask(msg)
        except ProviderError as exc:
            print(f"Provider error: {exc}", file=sys.stderr)
            return
        print(f"\n{answer}\n")

    if a.once:
        turn(a.once)
        return 0

    print("Type your request. Ctrl-D or 'exit' to quit.\n")
    while True:
        try:
            msg = input("you › ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if msg.lower() in ("exit", "quit"):
            return 0
        if msg:
            turn(msg)


if __name__ == "__main__":
    raise SystemExit(main())
