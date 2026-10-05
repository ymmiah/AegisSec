"""SARIF 2.1.0 export so findings appear in GitHub code scanning (Security tab)."""

from __future__ import annotations

import hashlib
from typing import Any

LEVEL_BY_PRIORITY = {"P0": "error", "P1": "error", "P2": "warning", "P3": "note", "P4": "note"}


def _rule(finding: dict[str, Any]) -> dict[str, Any]:
    intel = finding.get("intelligence") or {}
    ids = finding.get("identifiers") or {}
    osv_id = (intel.get("sources") or {}).get("osv", {}).get("id") or finding.get("id")
    summary = (finding.get("summary") or finding.get("id") or "Vulnerability").strip().splitlines()[0][:200]
    tags = ["security", "vulnerability", "dependency"]
    if intel.get("cisa_kev"):
        tags.append("known-exploited")
    rule: dict[str, Any] = {
        "id": finding["id"],
        "name": finding["id"].replace("-", ""),
        "shortDescription": {"text": summary},
        "fullDescription": {"text": summary},
        "helpUri": f"https://osv.dev/vulnerability/{osv_id}",
        "help": {
            "text": "Aliases: " + ", ".join(sorted({*ids.get("cve", []), *ids.get("ghsa", []), *ids.get("osv", [])})),
        },
        "properties": {"tags": tags, "precision": "high"},
    }
    if intel.get("cvss_score") is not None:
        rule["properties"]["security-severity"] = f"{float(intel['cvss_score']):.1f}"
    return rule


def sarif_report(result: dict[str, Any], *, artifact_uri: str | None = None, version: str = "1.0.0") -> dict[str, Any]:
    rules: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []
    for finding in result.get("findings") or []:
        rules.setdefault(finding["id"], _rule(finding))
        component = finding.get("component") or {}
        assessment = finding.get("assessment") or {}
        remediation = finding.get("remediation") or {}
        priority = assessment.get("priority")
        uri = component.get("path") or artifact_uri or "sbom.json"
        upgrade = remediation.get("recommended_version")
        text = (
            f"{component.get('name')} {component.get('version')} is affected by {finding['id']}"
            + (f" ({priority}, score {assessment.get('score')})" if priority else "")
            + (f". Upgrade to {upgrade} or later." if upgrade else ". No fixed version is published yet.")
        )
        fingerprint = hashlib.sha256(f"{component.get('name')}|{finding['id']}".encode()).hexdigest()
        results.append(
            {
                "ruleId": finding["id"],
                "level": LEVEL_BY_PRIORITY.get(priority, "warning"),
                "message": {"text": text},
                "locations": [{"physicalLocation": {"artifactLocation": {"uri": uri}, "region": {"startLine": 1}}}],
                "partialFingerprints": {"aegissecComponentVuln/v1": fingerprint},
                "properties": {
                    "priority": priority,
                    "score": assessment.get("score"),
                    "component": component.get("name"),
                    "installed_version": component.get("version"),
                    "recommended_version": upgrade,
                    "due_by": remediation.get("due_by"),
                    "cisa_kev": bool((finding.get("intelligence") or {}).get("cisa_kev")),
                },
            }
        )
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "AegisSec Vulnerability Intelligence",
                        "informationUri": "https://github.com/ymmiah/AegisSec",
                        "version": version,
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }
