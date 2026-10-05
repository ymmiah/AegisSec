from __future__ import annotations

from typing import Any

DETAILED = {"P0", "P1", "P2"}
LABEL = {"P0": "P0 · act now", "P1": "P1 · urgent", "P2": "P2 · planned", "P3": "P3 · routine", "P4": "P4 · backlog"}


def _cell(value: Any) -> str:
    text = "—" if value in (None, "", []) else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _short(text: str | None, limit: int = 220) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def markdown_report(result: dict[str, Any]) -> str:
    context = result.get("context") or {}
    summary = result.get("summary") or {}
    plan = result.get("fix_plan") or []
    findings = result.get("findings") or []
    asset = context.get("asset_id")

    lines = [f"# AegisSec Vulnerability Report{f' — {asset}' if asset else ''}", ""]
    meta = [f"Generated `{result.get('generated_at', 'unknown')}`"]
    if context:
        exposure = "internet-exposed" if context.get("internet_exposed") else "internal"
        meta.append(f"{context.get('environment', 'unknown')} · {exposure} · criticality {context.get('asset_criticality', 'n/a')}")
        if context.get("owner"):
            meta.append(f"owner **{context['owner']}**")
    lines += [" · ".join(meta), ""]

    # 1. Summary — the one screen a reader needs first.
    lines += ["## Summary", ""]
    if not findings:
        lines += [f"No known vulnerabilities in **{result.get('component_count', 0)}** components.", ""]
    else:
        by = summary.get("by_priority") or {}
        counts = " · ".join(f"**{by[p]}** {p}" for p in ("P0", "P1", "P2", "P3", "P4") if by.get(p))
        lines += [
            f"- **{len(plan)} action(s)** resolve **{summary.get('fixable', 0)} of {len(findings)}** findings "
            f"in {len(plan)} affected component(s) ({result.get('component_count', 0)} scanned).",
        ]
        if counts:
            lines.append(f"- By priority: {counts}")
        if summary.get("unassessed"):
            lines.append(f"- {summary['unassessed']} finding(s) unassessed — pass `--context` to prioritise them")
        if summary.get("known_exploited"):
            lines.append(f"- **{summary['known_exploited']} known exploited** (CISA KEV)")
        if summary.get("no_fix_available"):
            lines.append(f"- {summary['no_fix_available']} finding(s) have no published fix yet")
        if summary.get("next_due"):
            lines.append(f"- Next deadline: **{summary['next_due']}**")
        if "new" in summary:
            lines.append(f"- Since last scan: **{summary['new']} new**, **{summary['resolved']} resolved**")
        gate = result.get("gate") or {}
        if gate.get("fail_on"):
            verdict = f"**FAILED** — {gate['count']} finding(s) at {gate['fail_on']} or above" if gate["breached"] else "passed"
            lines.append(f"- CI gate (`--fail-on {gate['fail_on']}`{' new only' if gate.get('new_only') else ''}): {verdict}")
        lines.append("")

    # 2. Fix plan — one action per package, in order.
    if plan:
        lines += [
            "## Fix plan",
            "",
            "Work top to bottom. Each step clears every listed finding that has a published fix.",
            "",
            "| # | Action | Clears | Priority | Fix by | Notes |",
            "| ---: | --- | ---: | --- | --- | --- |",
        ]
        for item in plan:
            lines.append(
                f"| {item['step']} | {_cell(item['action'])} | {item['clears_count']}/{item['finding_count']} "
                f"| {_cell(item['highest_priority'])} | {_cell(item['due_by'])} | {_cell('; '.join(item['notes']))} |"
            )
        lines.append("")

    baseline = result.get("baseline") or {}
    if baseline.get("resolved"):
        lines += ["## Resolved since last scan", ""]
        lines += [f"- ~~{r['id']}~~ — {r['component']} {r['previous_version']} (was {r.get('previous_priority') or 'unassessed'})" for r in baseline["resolved"]]
        lines.append("")

    # 3. Detail for what needs attention; a compact table for the rest.
    urgent = [f for f in findings if (f.get("assessment") or {}).get("priority") in DETAILED]
    rest = [f for f in findings if f not in urgent]
    if urgent:
        lines += ["## Findings that need attention", ""]
        for finding in urgent:
            lines += _detail(finding)
    if rest:
        title = "Other findings" if urgent else "Findings"
        lines += [
            f"## {title}",
            "",
            "| Finding | Package | Priority | Score | CVSS | Upgrade to | Fix by |",
            "| --- | --- | --- | ---: | ---: | --- | --- |",
        ]
        for finding in rest:
            component = finding.get("component") or {}
            assessment = finding.get("assessment") or {}
            remediation = finding.get("remediation") or {}
            new = " 🆕" if finding.get("status") == "new" and baseline else ""
            lines.append(
                f"| {finding['id']}{new} | {_cell(component.get('name'))} {_cell(component.get('version'))} "
                f"| {_cell(assessment.get('priority'))} | {_cell(assessment.get('score'))} "
                f"| {_cell((finding.get('intelligence') or {}).get('cvss_score'))} "
                f"| {_cell(remediation.get('recommended_version'))} | {_cell(remediation.get('due_by'))} |"
            )
        lines.append("")

    warnings = result.get("warnings") or []
    if warnings:
        lines += [f"## Warnings ({len(warnings)})", ""] + [f"- {_short(w)}" for w in warnings] + [""]
    return "\n".join(lines).rstrip() + "\n"


def _detail(finding: dict[str, Any]) -> list[str]:
    assessment = finding.get("assessment") or {}
    component = finding.get("component") or {}
    intel = finding.get("intelligence") or {}
    remediation = finding.get("remediation") or {}
    epss = intel.get("epss")
    new = " · 🆕 new" if finding.get("status") == "new" else ""
    out = [
        f"### {finding.get('id')} — {component.get('name', 'unknown')} {component.get('version', '')}",
        "",
        f"**{LABEL.get(assessment.get('priority'), assessment.get('priority', 'unassessed'))}** · "
        f"score {assessment.get('score', 'n/a')}/100 · confidence {assessment.get('confidence', 'n/a')}{new}",
        "",
        _do_line(remediation),
        f"- **Fix by:** {remediation.get('due_by') or 'not set'}" + (f" · owner {remediation['owner']}" if remediation.get("owner") else ""),
        f"- CVSS `{intel.get('cvss_score', 'n/a')}` · EPSS `{f'{epss:.1%}' if isinstance(epss, (int, float)) else 'n/a'}` · "
        f"CISA KEV `{'yes' if intel.get('cisa_kev') else 'no'}`",
    ]
    if remediation.get("production_change_control_required"):
        out.append("- Production change: follow `playbooks/production-security-change.md` (approval, rollback, verification)")
    out += ["", _short(finding.get("summary") or "No summary available.", 400), ""]
    if assessment.get("reasons"):
        out += ["Why prioritised: " + "; ".join(assessment["reasons"]) + ".", ""]
    return out


def _do_line(remediation: dict[str, Any]) -> str:
    own, step, target = remediation.get("recommended_version"), remediation.get("plan_step"), remediation.get("plan_upgrade_to")
    if not own:
        return "- **Do:** no fixed version yet — apply vendor mitigations and monitor"
    if step and target and target != own:
        return f"- **Do:** fix plan step {step} — upgrade to `{target}` (this issue alone is fixed from `{own}`)"
    return f"- **Do:** {'fix plan step ' + str(step) + ' — ' if step else ''}upgrade to `{own}` or later"
