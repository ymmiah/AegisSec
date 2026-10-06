# AegisSec Runtime Harness

A governed security agent you can run as a chatbot or embed in your own app. It wraps any LLM in the AegisSec operating rules, the security skills and tools, and a specialist persona — and **enforces the scope and approval gates in code**, not just in the prompt.

It is `aegissec_agent/`, a pure-standard-library Python package (no third-party dependencies beyond the PyYAML already in `requirements.txt`).

## What it is

```
your prompt ─▶ Harness
                 ├─ system = AegisSec rules (AGENTS.md) + persona + tools + session facts
                 ├─ LLM provider (Anthropic · OpenAI-compatible · stub)
                 └─ tool loop:  model asks for a tool
                                   └▶ PolicyGate.check(action)      ← tools/action-risk.yaml
                                        allow / need scope / need approval / deny
                                   └▶ run tool, return result   ─▶ back to the model
```

The model can only affect the world through tools, and every tool call clears the policy gate first. The shipped tools are read-only or public-intelligence, so the harness advises and analyses; it never changes a live system on its own.

## Run it as a chatbot (CLI)

```bash
# Anthropic
export ANTHROPIC_API_KEY=sk-...
python scripts/aegissec_agent.py --agent security-appsec-engineer

# OpenAI or any OpenAI-compatible endpoint (local model, gateway…)
export OPENAI_API_KEY=sk-...
python scripts/aegissec_agent.py --provider openai --model gpt-4o \
  --base-url https://api.openai.com/v1

# one-shot
python scripts/aegissec_agent.py --once "Scan ./sbom.cdx.json and give me the fix plan"

# offline, no key needed
python scripts/aegissec_agent.py --list-agents
python scripts/aegissec_agent.py --list-skills
```

Useful flags: `--agent` (persona), `--workdir` (sandbox root for file tools), `--scope` (engagement YAML to unlock gated active testing), `--context` (asset context for scans), `--approve deny|prompt|auto`, `--verbose`.

## Embed it in your own chatbot

```python
from aegissec_agent import Harness
from aegissec_agent.providers import build_provider

harness = Harness(
    build_provider("anthropic", model="claude-opus-5-5"),
    agent="security-appsec-engineer",
    workdir="/path/to/repo",
    approval_mode="prompt",
    approver=lambda tool, summary: ask_your_user(tool, summary),  # your UI
)
answer = harness.ask("Review the auth code for authorization flaws")
```

`Harness` keeps conversation state across `ask()` calls; `reset()` clears it. Pass `on_event=...` to stream tool calls and policy decisions into your UI. Register extra tools with `extra_tools=[Tool(...)]`; a higher-risk tool is governed automatically by the `action` it declares.

### Use your own LLM client

Implement one method:

```python
from aegissec_agent.providers import LLMProvider, AssistantTurn, ToolCall

class MyProvider(LLMProvider):
    name = "mine"
    def complete(self, system, messages, tools) -> AssistantTurn:
        ...  # call your model, return text and any tool calls
```

## The policy gate

Each tool declares an `action` from [`tools/action-risk.yaml`](../tools/action-risk.yaml). Before a tool runs, the gate reads that action's risk tier and default and decides:

| Default contains | Gate requires |
| --- | --- |
| `allow` | runs (low-risk: read-only, public vulnerability intelligence) |
| `scope` | a loaded engagement scope that passes `check_scope`, else refused |
| `human_approval`, `change_control`, `owner`, `authority` | the approver callback (or `--approve auto` for non-critical), else refused |
| `deny` | never runs |

An action not in the policy fails closed. This is why active testing, production changes and destructive actions cannot happen "by accident": there is no shipped tool for them, and if you add one, the gate blocks it until scope and approval are in place.

## Tools the model has

| Tool | Action (risk) | Does |
| --- | --- | --- |
| `list_skills` | read_local_artifacts (low) | List AegisSec operational and native security skills |
| `read_skill` | read_local_artifacts (low) | Read one skill in full, then follow it |
| `list_files` | read_local_artifacts (low) | List files in the sandboxed working directory |
| `read_file` | read_local_artifacts (low) | Read a file inside the working directory (traversal refused) |
| `scan_dependencies` | query_public_vulnerability_intelligence (low) | Scan an SBOM/component JSON or a package → prioritised fix plan |
| `enrich_vulnerability` | query_public_vulnerability_intelligence (low) | Live CVSS, EPSS, CISA KEV, fixed versions, priority for a CVE/GHSA |
| `check_scope` | read_local_artifacts (low) | Validate an engagement scope before active testing |

## Personas

`python scripts/aegissec_agent.py --list-agents` lists them. `aegissec-operator` is the default. The rest are the **security** and **DevSecOps/SRE** specialists imported from [agency-agents](https://github.com/msitarzewski/agency-agents) (MIT), recorded in [`upstream/agency-agents.lock.json`](../upstream/agency-agents.lock.json). A persona changes expertise and voice; it never changes the rules — the harness always places `AGENTS.md` above it and keeps the gates in force.

## Providers and keys

- **Anthropic** — `ANTHROPIC_API_KEY`; default model `claude-opus-5-5`; `anthropic-version` defaults to `2023-06-01` (override with `ANTHROPIC_VERSION`).
- **OpenAI-compatible** — `OPENAI_API_KEY` (or `--api-key-env`); set `--base-url` for gateways or local servers that speak the chat-completions API.

Keys are read from the environment and never written to disk or into memory. Defaults live in [`config/agent.yaml`](../config/agent.yaml).

## Limits

- The shipped harness is advisory and read-only by design. Giving it write or execute power means adding tools and wiring real approvals — do that deliberately.
- A passed scope check is structural, not legal authority; that remains yours.
- Scanning needs network access to the public vulnerability sources (see [`docs/vulnerability-intelligence.md`](vulnerability-intelligence.md)).
