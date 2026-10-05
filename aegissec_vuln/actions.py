"""Turn prioritised findings into actions people can work through.

The engine produces one finding per vulnerability. Teams fix packages, not
CVEs, so this module adds:

- ``fix_plan``: one upgrade action per affected component, with the version
  that clears every fixable finding on it;
- ``due_by`` / ``owner`` on each finding and plan item, from the remediation
  SLA in the configuration and the asset context;
- ``summary``: the counts a reader needs first;
- ``baseline``: what is new and what has been resolved since a previous scan;
- ``gate``: whether the result breaches a ``--fail-on`` priority for CI.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
from typing import Any

PRIORITY_ORDER = ["P0", "P1", "P2", "P3", "P4"]

# Defaults used when the configuration has no ``remediation_sla_days`` block.
# They are starting points, not a standard: set your own in
# config/vulnerability-intelligence.yaml.
DEFAULT_SLA_DAYS = {"P0": 2, "P1": 7, "P2": 30, "P3": 90, "P4": 180}


def priority_rank(priority: str | None) -> int:
    return PRIORITY_ORDER.index(priority) if priority in PRIORITY_ORDER else len(PRIORITY_ORDER)


def version_key(version: str | None) -> tuple[int, ...] | None:
    if not version:
        return None
    parts = [p for p in re.split(r"[^0-9]+", version.split("+", 1)[0]) if p]
    return tuple(int(p) for p in parts) if parts else None


def is_major_upgrade(current: str | None, target: str | None) -> bool:
    """True when moving current -> target is likely to include breaking changes.

    Follows semantic versioning: a change in the first non-zero component
    (major for >=1.0.0, minor for 0.x) is treated as breaking.
    """
    cur, tgt = version_key(current), version_key(target)
    if not cur or not tgt:
        return False
    cur, tgt = cur + (0, 0), tgt + (0, 0)
    if cur[0] != tgt[0]:
        return True
    return cur[0] == 0 and cur[1] != tgt[1]


def _scan_date(result: dict[str, Any]) -> date:
    raw = result.get("generated_at")
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).date()
    except (TypeError, ValueError):
        return datetime.now(timezone.utc).date()


def apply_actions(
    result: dict[str, Any],
    *,
    owner: str | None = None,
    sla_days: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Annotate findings with due dates and owner, then add fix_plan and summary."""
    sla = {**DEFAULT_SLA_DAYS, **(sla_days or {})}
    scanned = _scan_date(result)
    findings = result.get("findings") or []

    for finding in findings:
        priority = (finding.get("assessment") or {}).get("priority")
        days = sla.get(priority) if priority else None
        remediation = finding.setdefault("remediation", {})
        remediation["owner"] = owner
        remediation["sla_days"] = days
        remediation["due_by"] = (scanned + timedelta(days=int(days))).isoformat() if days is not None else None

    result["fix_plan"] = build_fix_plan(findings)
    result["remediation_sla_days"] = sla
    result["summary"] = summarise(result)
    return result


def build_fix_plan(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for finding in findings:
        component = finding.get("component") or {}
        key = (str(component.get("name")), str(component.get("version")), str(component.get("path") or ""))
        groups.setdefault(key, []).append(finding)

    plan: list[dict[str, Any]] = []
    for (name, version, path), items in groups.items():
        component = items[0].get("component") or {}
        fixable = [f for f in items if (f.get("remediation") or {}).get("recommended_version")]
        unresolved = [f for f in items if f not in fixable]
        targets = [(f.get("remediation") or {})["recommended_version"] for f in fixable]
        comparable = [t for t in targets if version_key(t) is not None]
        upgrade_to = max(comparable, key=version_key) if comparable else (targets[0] if targets else None)
        priorities = [(f.get("assessment") or {}).get("priority") for f in items]
        highest = min(priorities, key=priority_rank) if priorities else None
        due_dates = [d for f in items if (d := (f.get("remediation") or {}).get("due_by"))]
        owners = {o for f in items if (o := (f.get("remediation") or {}).get("owner"))}
        kev = [f["id"] for f in items if (f.get("intelligence") or {}).get("cisa_kev")]
        major = is_major_upgrade(version, upgrade_to)

        if upgrade_to:
            action = f"Upgrade {name} from {version} to {upgrade_to} or later"
        else:
            action = f"No fixed version of {name} {version} is published yet; apply vendor mitigations and monitor"
        notes = []
        if major:
            notes.append("Major-version change: review the changelog and run regression tests before release")
        if unresolved and upgrade_to:
            notes.append(f"{len(unresolved)} finding(s) have no published fix and stay open after the upgrade")
        if kev:
            notes.append("Includes known exploited vulnerabilities (CISA KEV)")
        if component.get("direct") is False:
            notes.append("Indirect dependency: upgrade the package that pulls it in, or pin it with your package manager's override")

        plan.append(
            {
                "component": name,
                "ecosystem": component.get("ecosystem"),
                "path": path or None,
                "current_version": version,
                "upgrade_to": upgrade_to,
                "major_upgrade": major,
                "action": action,
                "notes": notes,
                "highest_priority": highest,
                "max_score": max(((f.get("assessment") or {}).get("score") or 0) for f in items),
                "due_by": min(due_dates) if due_dates else None,
                "owner": ", ".join(sorted(owners)) if owners else None,
                "clears": [f["id"] for f in fixable],
                "clears_count": len(fixable),
                "unresolved": [f["id"] for f in unresolved],
                "known_exploited": kev,
                "finding_count": len(items),
            }
        )

    plan.sort(key=lambda p: (priority_rank(p["highest_priority"]), -p["max_score"], p["component"]))
    for step, item in enumerate(plan, start=1):
        item["step"] = step
    # Link each finding back to the plan step that fixes it.
    steps = {(p["component"], p["current_version"], p["path"] or ""): p for p in plan}
    for finding in findings:
        component = finding.get("component") or {}
        item = steps.get((str(component.get("name")), str(component.get("version")), str(component.get("path") or "")))
        if item:
            remediation = finding.setdefault("remediation", {})
            remediation["plan_step"] = item["step"]
            remediation["plan_upgrade_to"] = item["upgrade_to"]
    return plan


def summarise(result: dict[str, Any]) -> dict[str, Any]:
    findings = result.get("findings") or []
    by_priority = {p: 0 for p in PRIORITY_ORDER}
    unassessed = 0
    for finding in findings:
        priority = (finding.get("assessment") or {}).get("priority")
        if priority in by_priority:
            by_priority[priority] += 1
        else:
            unassessed += 1
    plan = result.get("fix_plan") or []
    summary = {
        "components_affected": len(plan),
        "actions": len(plan),
        "findings": len(findings),
        "by_priority": by_priority,
        "unassessed": unassessed,
        "known_exploited": sum(1 for f in findings if (f.get("intelligence") or {}).get("cisa_kev")),
        "fixable": sum(p["clears_count"] for p in plan),
        "no_fix_available": sum(len(p["unresolved"]) for p in plan),
        "next_due": min((p["due_by"] for p in plan if p.get("due_by")), default=None),
    }
    if result.get("baseline"):
        summary["new"] = result["baseline"]["new_count"]
        summary["resolved"] = result["baseline"]["resolved_count"]
    return summary


def _finding_key(finding: dict[str, Any]) -> tuple[str, str]:
    component = finding.get("component") or {}
    return (str(component.get("name")), str(finding.get("id")))


def compare_baseline(result: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    """Mark findings new/existing and list findings resolved since ``baseline``.

    Findings are matched on component name + finding ID, so upgrading a
    package (version change) correctly counts the old finding as resolved.
    """
    previous = {_finding_key(f): f for f in baseline.get("findings") or []}
    current_keys = set()
    new = 0
    for finding in result.get("findings") or []:
        key = _finding_key(finding)
        current_keys.add(key)
        finding["status"] = "existing" if key in previous else "new"
        new += finding["status"] == "new"
    resolved = [
        {
            "id": f.get("id"),
            "component": (f.get("component") or {}).get("name"),
            "previous_version": (f.get("component") or {}).get("version"),
            "previous_priority": (f.get("assessment") or {}).get("priority"),
        }
        for key, f in previous.items()
        if key not in current_keys
    ]
    result["baseline"] = {
        "compared_with": baseline.get("generated_at"),
        "new_count": new,
        "existing_count": len(current_keys) - new,
        "resolved_count": len(resolved),
        "resolved": resolved,
    }
    if result.get("summary") is not None:
        result["summary"]["new"] = new
        result["summary"]["resolved"] = len(resolved)
    return result


def evaluate_gate(result: dict[str, Any], fail_on: str | None, *, new_only: bool = False) -> dict[str, Any]:
    """Decide whether CI should fail: any finding at or above ``fail_on``."""
    if not fail_on:
        return {"fail_on": None, "breached": False, "count": 0, "findings": []}
    threshold = priority_rank(fail_on)
    hits = [
        f["id"]
        for f in result.get("findings") or []
        if priority_rank((f.get("assessment") or {}).get("priority")) <= threshold
        and (not new_only or f.get("status", "new") == "new")
    ]
    gate = {"fail_on": fail_on, "new_only": new_only, "breached": bool(hits), "count": len(hits), "findings": hits}
    result["gate"] = gate
    return gate
