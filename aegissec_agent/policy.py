"""Policy gate for the AegisSec runtime harness.

Every tool declares an ``action`` from ``tools/action-risk.yaml``. Before a tool
runs, the gate reads that action's risk tier and default disposition and decides:

- **allow** — run it (low-risk, read-only or public-intelligence work);
- **require scope** — run only if a validated engagement scope is loaded;
- **require human approval** — ask the approval callback; refuse if it says no;
- **deny** — never run.

This is AegisSec policy enforced in code, not merely described to the model.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]

# How each action-risk default maps onto what the gate must check.
NEEDS_SCOPE = "scope"
NEEDS_APPROVAL = "approval"


def _requirements(default: str) -> set[str]:
    needs = set()
    d = default.lower()
    if "deny" in d:
        needs.add("deny")
    if "scope" in d:
        needs.add(NEEDS_SCOPE)
    if "human_approval" in d or "human_controlled" in d:
        needs.add(NEEDS_APPROVAL)
    if "change_control" in d or "owner" in d or "incident_authority" in d or "authority" in d:
        # These require a human decision the harness cannot make on its own.
        needs.add(NEEDS_APPROVAL)
    return needs


@dataclass
class Decision:
    allowed: bool
    reason: str


class PolicyGate:
    """Decides whether a tool may run, from AegisSec's action-risk policy."""

    def __init__(
        self,
        action_risk: dict,
        *,
        approval_mode: str = "deny",
        approver: Callable[[str, str], bool] | None = None,
        scope_ok: bool = False,
        scope_label: str | None = None,
    ):
        self.actions = (action_risk or {}).get("actions", {})
        self.approval_mode = approval_mode  # "prompt" | "auto" | "deny"
        self.approver = approver
        self.scope_ok = scope_ok
        self.scope_label = scope_label

    def risk_of(self, action: str) -> str:
        return (self.actions.get(action) or {}).get("risk", "unknown")

    def check(self, tool_name: str, action: str, summary: str) -> Decision:
        entry = self.actions.get(action)
        if entry is None:
            # Unknown action: fail closed. A tool must map to a known risk.
            return Decision(False, f"'{action}' is not in the AegisSec action-risk policy; refusing by default")
        risk = entry.get("risk", "unknown")
        default = entry.get("default", "deny")
        needs = _requirements(default)

        if "deny" in needs:
            return Decision(False, f"{tool_name} is a {risk}-risk action ({action}); AegisSec policy forbids it on real targets")

        if NEEDS_SCOPE in needs and not self.scope_ok:
            return Decision(
                False,
                f"{tool_name} ({action}, {risk} risk) needs a validated engagement scope. "
                "Load one with a passing scope check before active testing.",
            )

        if NEEDS_APPROVAL in needs:
            if self.approval_mode == "deny":
                return Decision(False, f"{tool_name} ({action}, {risk} risk) needs human approval, which is unavailable in this session")
            if self.approval_mode == "auto":
                return Decision(True, f"{tool_name} auto-approved ({risk} risk); recorded for audit")
            approved = bool(self.approver and self.approver(tool_name, f"{summary}\nAction: {action} ({risk} risk)"))
            return Decision(approved, "approved by human" if approved else "declined by human")

        return Decision(True, f"allowed ({risk} risk, {action})")
