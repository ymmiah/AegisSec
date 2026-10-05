from __future__ import annotations

import re
from typing import Any

_CVE = re.compile(r"^CVE-\d{4}-\d{4,}$", re.I)
_GHSA = re.compile(r"^GHSA-[23456789cfghjmpqrvwx]{4}-[23456789cfghjmpqrvwx]{4}-[23456789cfghjmpqrvwx]{4}$", re.I)


def classify_identifier(value: str) -> str:
    value = value.upper()
    if _CVE.match(value):
        return "cve"
    if _GHSA.match(value):
        return "ghsa"
    if value.startswith("OSV-"):
        return "osv"
    return "other"


def identifiers_from_osv(vuln: dict[str, Any]) -> dict[str, list[str]]:
    result = {"cve": [], "ghsa": [], "osv": [], "other": []}
    for value in [vuln.get("id"), *(vuln.get("aliases") or [])]:
        if not value:
            continue
        value = str(value).upper()
        bucket = classify_identifier(value)
        if value not in result[bucket]:
            result[bucket].append(value)
    return result


def canonical_identifier(identifiers: dict[str, list[str]], fallback: str | None = None) -> str:
    for bucket in ("cve", "ghsa", "osv", "other"):
        if identifiers.get(bucket):
            return identifiers[bucket][0]
    return fallback or "UNKNOWN"


def fixed_versions_from_osv(vuln: dict[str, Any]) -> list[str]:
    versions: list[str] = []
    for affected in vuln.get("affected") or []:
        for rng in affected.get("ranges") or []:
            for event in rng.get("events") or []:
                fixed = event.get("fixed")
                if fixed and fixed not in versions:
                    versions.append(str(fixed))
    return versions


def severity_label_to_score(label: str | None) -> float | None:
    if not label:
        return None
    return {
        "LOW": 3.0,
        "MODERATE": 5.5,
        "MEDIUM": 5.5,
        "HIGH": 8.0,
        "CRITICAL": 9.8,
    }.get(str(label).upper())
