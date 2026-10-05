from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Iterable

from .connectors import CisaKevConnector, EPSSConnector, GitHubAdvisoryConnector, NVDConnector, OSVConnector
from .models import AssetContext, Component
from .normalize import affected_ranges_from_osv, canonical_identifier, fixed_versions_from_osv, identifiers_from_osv, severity_label_to_score
from .risk import RiskEngine


class VulnerabilityIntelligenceEngine:
    """Discover via OSV, enrich with public intelligence, then prioritise using asset context."""

    def __init__(
        self,
        *,
        osv: OSVConnector | None = None,
        github: GitHubAdvisoryConnector | None = None,
        nvd: NVDConnector | None = None,
        kev: CisaKevConnector | None = None,
        epss: EPSSConnector | None = None,
        risk: RiskEngine | None = None,
        source_enabled: dict[str, bool] | None = None,
    ):
        self.osv = osv or OSVConnector()
        self.github = github or GitHubAdvisoryConnector()
        self.nvd = nvd or NVDConnector()
        self.kev = kev or CisaKevConnector()
        self.epss = epss or EPSSConnector()
        self.risk = risk or RiskEngine()
        self.source_enabled = {
            "osv": True,
            "github_advisory": True,
            "nvd": True,
            "cisa_kev": True,
            "epss": True,
            **(source_enabled or {}),
        }

    def scan_components(
        self,
        components: Iterable[Component],
        *,
        context: AssetContext | None = None,
        enrich: bool = True,
        max_enrich: int = 50,
    ) -> dict[str, Any]:
        components = list(components)
        if not self.source_enabled.get("osv", True):
            raise ValueError("OSV discovery is disabled; component scan requires a discovery source")
        osv_results = self.osv.query_batch(components)
        findings: list[dict[str, Any]] = []
        for component, vulns in zip(components, osv_results):
            for vuln in vulns:
                findings.append(self._from_osv(component, vuln))
        findings = self._deduplicate(findings)
        warnings: list[str] = []
        if enrich and findings:
            self._enrich(findings[:max_enrich], warnings)
            if len(findings) > max_enrich:
                warnings.append(f"Enrichment limited to first {max_enrich} findings; {len(findings)-max_enrich} remain OSV-only")
        if context:
            for finding in findings:
                finding["assessment"] = self.risk.assess(finding, context)
                finding["routing"] = self._route(finding, context)
                finding["remediation"] = self._remediation(finding, context)
        else:
            for finding in findings:
                finding["routing"] = self._route(finding, None)
                finding["remediation"] = self._remediation(finding, None)
        findings.sort(key=lambda f: (f.get("assessment", {}).get("score", 0), f["id"]), reverse=True)
        return {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "engine": "AegisSec Vulnerability Intelligence",
            "component_count": len(components),
            "finding_count": len(findings),
            "sources": {k: v for k, v in self.source_enabled.items() if v},
            "warnings": warnings,
            "findings": findings,
        }

    def enrich_identifier(self, identifier: str, context: AssetContext | None = None) -> dict[str, Any]:
        finding = {
            "id": identifier.upper(),
            "identifiers": {"cve": [], "ghsa": [], "osv": [], "other": []},
            "component": None,
            "summary": None,
            "fixed_versions": [],
            "intelligence": {"sources": {}},
            "references": [],
        }
        bucket = "cve" if identifier.upper().startswith("CVE-") else "ghsa" if identifier.upper().startswith("GHSA-") else "other"
        finding["identifiers"][bucket].append(identifier.upper())
        warnings: list[str] = []
        self._enrich([finding], warnings)
        if context:
            finding["assessment"] = self.risk.assess(finding, context)
        finding["routing"] = self._route(finding, context)
        finding["remediation"] = self._remediation(finding, context)
        return {"finding": finding, "warnings": warnings}

    def ingest_osv_scanner(self, data: dict[str, Any], *, context: AssetContext | None = None, enrich: bool = True, max_enrich: int = 50) -> dict[str, Any]:
        from .osv_scanner import iter_packages

        findings: list[dict[str, Any]] = []
        component_keys: set[tuple[str, str, str]] = set()
        for source, package, vulns in iter_packages(data):
            component = Component(
                name=str(package.get("name")),
                version=str(package.get("version")),
                ecosystem=package.get("ecosystem"),
                purl=package.get("purl"),
                path=source.get("path"),
                metadata={"source_type": source.get("type")},
            )
            component_keys.add((component.name, component.version, component.path or ""))
            for vuln in vulns:
                findings.append(self._from_osv(component, vuln))
        findings = self._deduplicate(findings)
        warnings: list[str] = []
        scanner_meta = data.get("_aegissec") or {}
        if scanner_meta.get("scanner_stderr"):
            warnings.append("OSV-Scanner emitted diagnostic output; see scanner metadata in the result")
        if enrich and findings:
            self._enrich(findings[:max_enrich], warnings)
            if len(findings) > max_enrich:
                warnings.append(f"Enrichment limited to first {max_enrich} findings; {len(findings)-max_enrich} remain OSV-only")
        for finding in findings:
            if context:
                finding["assessment"] = self.risk.assess(finding, context)
            finding["routing"] = self._route(finding, context)
            finding["remediation"] = self._remediation(finding, context)
        findings.sort(key=lambda f: (f.get("assessment", {}).get("score", 0), f["id"]), reverse=True)
        return {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "engine": "AegisSec Vulnerability Intelligence",
            "discovery": "OSV-Scanner v2",
            "component_count": len(component_keys),
            "finding_count": len(findings),
            "sources": {k: v for k, v in self.source_enabled.items() if v},
            "warnings": warnings,
            "scanner": scanner_meta,
            "findings": findings,
        }

    def _from_osv(self, component: Component, vuln: dict[str, Any]) -> dict[str, Any]:
        identifiers = identifiers_from_osv(vuln)
        severity_label = (vuln.get("database_specific") or {}).get("severity")
        return {
            "id": canonical_identifier(identifiers, vuln.get("id")),
            "identifiers": identifiers,
            "component": component.to_dict(),
            "summary": vuln.get("summary") or vuln.get("details"),
            "published": vuln.get("published"),
            "modified": vuln.get("modified"),
            "fixed_versions": fixed_versions_from_osv(vuln, component.name),
            "affected_ranges": affected_ranges_from_osv(vuln, component.name),
            "references": [r.get("url") for r in vuln.get("references", []) or [] if r.get("url")],
            "intelligence": {
                "osv": True,
                "cvss_score": severity_label_to_score(severity_label),
                "severity_label": severity_label,
                "epss": None,
                "epss_percentile": None,
                "cisa_kev": False,
                "github_advisory": False,
                "nvd": False,
                "sources": {"osv": {"id": vuln.get("id"), "url": f"https://osv.dev/vulnerability/{vuln.get('id')}" if vuln.get("id") else None}},
            },
        }

    def _deduplicate(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
        for finding in findings:
            component = finding.get("component") or {}
            key = (str(component.get("name")), str(component.get("version")), finding["id"])
            if key not in grouped:
                grouped[key] = finding
                continue
            current = grouped[key]
            current["fixed_versions"] = sorted(set(current.get("fixed_versions", [])) | set(finding.get("fixed_versions", [])))
            # Keep every advisory's affected ranges: a fix for one advisory can
            # still sit inside another advisory's range for the same CVE.
            for rng in finding.get("affected_ranges", []):
                if rng not in current.setdefault("affected_ranges", []):
                    current["affected_ranges"].append(rng)
            current["references"] = sorted(set(current.get("references", [])) | set(finding.get("references", [])))
        return list(grouped.values())

    def _enrich(self, findings: list[dict[str, Any]], warnings: list[str]) -> None:
        cve_to_findings: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for finding in findings:
            for cve in finding.get("identifiers", {}).get("cve", []):
                cve_to_findings[cve.upper()].append(finding)

        if self.source_enabled.get("epss") and cve_to_findings:
            try:
                epss_map = self.epss.by_cves(cve_to_findings)
                for cve, item in epss_map.items():
                    for finding in cve_to_findings.get(cve, []):
                        intel = finding["intelligence"]
                        intel["epss"] = _to_float(item.get("epss"))
                        intel["epss_percentile"] = _to_float(item.get("percentile"))
                        intel["sources"]["epss"] = {"date": item.get("date"), "url": "https://api.first.org/data/v1/epss"}
            except Exception as exc:
                warnings.append(f"EPSS enrichment unavailable: {exc}")

        if self.source_enabled.get("cisa_kev") and cve_to_findings:
            try:
                catalog = self.kev.catalog()
                for cve, related in cve_to_findings.items():
                    item = catalog.get(cve)
                    if not item:
                        continue
                    for finding in related:
                        finding["intelligence"]["cisa_kev"] = True
                        finding["intelligence"]["sources"]["cisa_kev"] = {
                            "date_added": item.get("dateAdded"),
                            "due_date": item.get("dueDate"),
                            "known_ransomware_campaign_use": item.get("knownRansomwareCampaignUse"),
                            "required_action": item.get("requiredAction"),
                            "url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                        }
            except Exception as exc:
                warnings.append(f"CISA KEV enrichment unavailable: {exc}")

        for cve, related in cve_to_findings.items():
            if self.source_enabled.get("github_advisory"):
                try:
                    advisories = self.github.by_cve(cve)
                    if advisories:
                        self._merge_github(related, advisories[0])
                except Exception as exc:
                    warnings.append(f"GitHub Advisory enrichment unavailable for {cve}: {exc}")
            if self.source_enabled.get("nvd"):
                try:
                    cve_data = self.nvd.by_cve(cve)
                    if cve_data:
                        self._merge_nvd(related, cve_data)
                except Exception as exc:
                    warnings.append(f"NVD enrichment unavailable for {cve}: {exc}")

    def _merge_github(self, findings: list[dict[str, Any]], advisory: dict[str, Any]) -> None:
        ghsa_id = advisory.get("ghsa_id")
        score = _github_cvss_score(advisory)
        for finding in findings:
            intel = finding["intelligence"]
            intel["github_advisory"] = True
            if score is not None and (intel.get("cvss_score") is None or score > intel["cvss_score"]):
                intel["cvss_score"] = score
            intel["severity_label"] = advisory.get("severity") or intel.get("severity_label")
            if ghsa_id and ghsa_id not in finding["identifiers"]["ghsa"]:
                finding["identifiers"]["ghsa"].append(ghsa_id)
            for vuln in advisory.get("vulnerabilities", []) or []:
                # The REST API returns first_patched_version as a plain string; older
                # payloads used {"identifier": ...}. Accept both.
                patched = vuln.get("first_patched_version")
                if isinstance(patched, dict):
                    patched = patched.get("identifier")
                if patched and patched not in finding["fixed_versions"]:
                    finding["fixed_versions"].append(patched)
            intel["sources"]["github_advisory"] = {
                "ghsa_id": ghsa_id,
                "html_url": advisory.get("html_url"),
                "published_at": advisory.get("published_at"),
                "updated_at": advisory.get("updated_at"),
            }

    def _merge_nvd(self, findings: list[dict[str, Any]], cve_data: dict[str, Any]) -> None:
        score = _nvd_cvss_score(cve_data)
        for finding in findings:
            intel = finding["intelligence"]
            intel["nvd"] = True
            if score is not None and (intel.get("cvss_score") is None or score > intel["cvss_score"]):
                intel["cvss_score"] = score
            intel["sources"]["nvd"] = {
                "id": cve_data.get("id"),
                "published": cve_data.get("published"),
                "last_modified": cve_data.get("lastModified"),
                "vuln_status": cve_data.get("vulnStatus"),
                "url": f"https://nvd.nist.gov/vuln/detail/{cve_data.get('id')}" if cve_data.get("id") else None,
            }

    def _route(self, finding: dict[str, Any], context: AssetContext | None) -> dict[str, Any]:
        assessment = finding.get("assessment") or {}
        priority = assessment.get("priority")
        primary = "devsecops-security"
        supporting = ["threat-intelligence"]
        reason = "Software dependency/SBOM vulnerability remediation"
        if priority in {"P0", "P1"}:
            supporting.append("security-lead")
        if context and context.environment.lower() == "production":
            supporting.append("forward-deployed-security-engineer")
        return {
            "primary_role": primary,
            "supporting_roles": sorted(set(supporting)),
            "playbook": "playbooks/continuous-vulnerability-management.md",
            "reason": reason,
        }

    def _remediation(self, finding: dict[str, Any], context: AssetContext | None) -> dict[str, Any]:
        fixed = finding.get("fixed_versions") or []
        current = ((finding.get("component") or {}).get("version")) or ""
        targets = _upgrade_targets(current, fixed, finding.get("affected_ranges"))
        production = bool(context and context.environment.lower() == "production")
        return {
            "fix_available": bool(fixed),
            "recommended_version": targets[0] if targets else None,
            "target_versions": targets,
            "recommended_action": "Upgrade to a confirmed fixed version and re-scan" if fixed else "Review vendor/advisory mitigation and track a fixed version",
            "verification": "Repeat dependency/SBOM scan and confirm the vulnerable version is no longer present/reachable",
            "production_change_control_required": production,
        }


def _to_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _version_key(version: str) -> tuple[int, ...] | None:
    parts = [p for p in re.split(r"[^0-9]+", version.split("+", 1)[0]) if p]
    return tuple(int(p) for p in parts) if parts else None


def _is_affected(version: tuple[int, ...], ranges: list[dict[str, Any]]) -> bool:
    for rng in ranges:
        start = _version_key(str(rng.get("introduced") or "0")) or (0,)
        if version < start:
            continue
        fixed = _version_key(rng["fixed"]) if rng.get("fixed") else None
        last = _version_key(rng["last_affected"]) if rng.get("last_affected") else None
        if fixed is not None:
            if version < fixed:
                return True
        elif last is not None:
            if version <= last:
                return True
        elif not rng.get("fixed") and not rng.get("last_affected"):
            return True  # open-ended: everything from `introduced` onwards
    return False


def _upgrade_targets(current: str, fixed: list[str], ranges: list[dict[str, Any]] | None = None) -> list[str]:
    """Fixed versions that are real, safe upgrades from `current`, lowest first.

    - Older-branch fixes are dropped: OSV lists a fix per maintained branch
      (e.g. Log4j 2.3.1 and 2.12.2 alongside 2.15.0).
    - A candidate still inside any affected range is dropped: one CVE can have
      several advisories, and a version that fixes one can remain vulnerable to
      another (seen live with lodash 4.17.23 vs 4.18.0).
    Falls back to the full list when versions cannot be compared, and to the
    highest candidate when the range data leaves no version clear.
    """
    cur = _version_key(current) if current else None
    keyed = [(k, v) for v in fixed if (k := _version_key(v)) is not None]
    if cur is None or len(keyed) != len(fixed):
        return list(fixed)
    upgrades = [(k, v) for k, v in sorted(set(keyed)) if k > cur]
    if not ranges:
        return [v for _, v in upgrades]
    safe = [v for k, v in upgrades if not _is_affected(k, ranges)]
    return safe or [v for _, v in upgrades[-1:]]


def _github_cvss_score(advisory: dict[str, Any]) -> float | None:
    severities = advisory.get("cvss_severities") or {}
    for key in ("cvss_v4", "cvss_v3"):
        score = _to_float((severities.get(key) or {}).get("score"))
        if score:
            return score
    return _to_float((advisory.get("cvss") or {}).get("score")) or None


def _nvd_cvss_score(cve: dict[str, Any]) -> float | None:
    metrics = cve.get("metrics") or {}
    for key in ("cvssMetricV40", "cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        for metric in metrics.get(key, []) or []:
            score = _to_float((metric.get("cvssData") or {}).get("baseScore"))
            if score is not None:
                return score
    return None
