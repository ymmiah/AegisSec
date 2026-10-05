from __future__ import annotations

from typing import Any


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        "# AegisSec Vulnerability Intelligence Report",
        "",
        f"Generated: `{result.get('generated_at', 'unknown')}`  ",
        f"Components assessed: **{result.get('component_count', 0)}**  ",
        f"Findings: **{result.get('finding_count', 0)}**",
        "",
    ]
    warnings = result.get("warnings") or []
    if warnings:
        lines.extend(["## Warnings", ""] + [f"- {w}" for w in warnings] + [""])
    lines.extend(["## Findings", ""])
    for finding in result.get("findings", []):
        assessment = finding.get("assessment") or {}
        component = finding.get("component") or {}
        intel = finding.get("intelligence") or {}
        lines.extend(
            [
                f"### {finding.get('id')} — {component.get('name', 'unknown')} {component.get('version', '')}",
                "",
                f"- Priority: **{assessment.get('priority', 'unassessed')}**",
                f"- Context score: **{assessment.get('score', 'n/a')} / 100**",
                f"- Confidence: **{assessment.get('confidence', 'n/a')}**",
                f"- CVSS: `{intel.get('cvss_score', 'n/a')}`",
                f"- EPSS: `{intel.get('epss', 'n/a')}`",
                f"- CISA KEV: `{bool(intel.get('cisa_kev'))}`",
                f"- Fixed version(s): `{', '.join(finding.get('fixed_versions', [])) or 'not confirmed'}`",
                f"- Recommended upgrade: `{(finding.get('remediation') or {}).get('recommended_version') or 'not confirmed'}`",
                "",
                (finding.get("summary") or "No summary available.").strip(),
                "",
            ]
        )
        if assessment.get("reasons"):
            lines.append("Why prioritised:")
            lines.extend([f"- {r}" for r in assessment["reasons"]])
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
