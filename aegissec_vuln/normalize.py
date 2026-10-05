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


def _norm_name(name: Any) -> str:
    return str(name or "").strip().lower().replace("_", "-")


def _affected_for(vuln: dict[str, Any], package_name: str | None) -> list[dict[str, Any]]:
    """The affected[] entries for this package (an advisory can cover several)."""
    entries = vuln.get("affected") or []
    if not package_name:
        return entries
    wanted = _norm_name(package_name)
    matched = [a for a in entries if _norm_name((a.get("package") or {}).get("name")) == wanted]
    return matched or entries


def affected_ranges_from_osv(vuln: dict[str, Any], package_name: str | None = None) -> list[dict[str, str | None]]:
    """Affected intervals for the package, as {introduced, fixed, last_affected}.

    OSV encodes each range as an ordered event list (introduced, fixed,
    introduced, fixed, ...). Git ranges are skipped: they hold commit hashes.
    """
    intervals: list[dict[str, str | None]] = []
    for affected in _affected_for(vuln, package_name):
        for rng in affected.get("ranges") or []:
            if str(rng.get("type", "")).upper() == "GIT":
                continue
            current: dict[str, str | None] | None = None
            for event in rng.get("events") or []:
                if "introduced" in event:
                    current = {"introduced": str(event["introduced"]), "fixed": None, "last_affected": None}
                    intervals.append(current)
                elif current is not None and "fixed" in event:
                    current["fixed"] = str(event["fixed"])
                    current = None
                elif current is not None and "last_affected" in event:
                    current["last_affected"] = str(event["last_affected"])
                    current = None
    return intervals


def fixed_versions_from_osv(vuln: dict[str, Any], package_name: str | None = None) -> list[str]:
    versions: list[str] = []
    for affected in _affected_for(vuln, package_name):
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
