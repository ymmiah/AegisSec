from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import AssetContext


DEFAULT_WEIGHTS = {
    "cvss": 0.20,
    "epss": 0.20,
    "kev": 0.20,
    "reachability": 0.15,
    "exposure": 0.10,
    "asset_criticality": 0.10,
    "privilege": 0.05,
}

CRITICALITY = {"low": 0.25, "medium": 0.50, "high": 0.75, "critical": 1.0}


class RiskEngine:
    def __init__(self, config: dict[str, Any] | None = None):
        config = config or {}
        self.weights = {**DEFAULT_WEIGHTS, **(config.get("weights") or {})}
        total = sum(float(v) for v in self.weights.values())
        if total <= 0:
            raise ValueError("Risk weights must sum to a positive value")
        self.weights = {k: float(v) / total for k, v in self.weights.items()}
        self.thresholds = config.get("thresholds") or {"P0": 85, "P1": 70, "P2": 50, "P3": 25, "P4": 0}

    def assess(self, finding: dict[str, Any], context: AssetContext) -> dict[str, Any]:
        intel = finding.get("intelligence", {})
        cvss = _clamp(float(intel.get("cvss_score") or 0.0) / 10.0)
        epss = _clamp(float(intel.get("epss") or 0.0))
        kev = 1.0 if intel.get("cisa_kev") else 0.0
        reachability = 1.0 if context.reachable else (0.6 if context.runtime_loaded else 0.0)
        exposure = 1.0 if context.internet_exposed else 0.0
        criticality = CRITICALITY.get(context.asset_criticality.lower(), 0.5)
        privilege = 1.0 if context.privileged_component else 0.0
        factors = {
            "cvss": cvss,
            "epss": epss,
            "kev": kev,
            "reachability": reachability,
            "exposure": exposure,
            "asset_criticality": criticality,
            "privilege": privilege,
        }
        raw = sum(factors[k] * self.weights.get(k, 0.0) for k in factors)
        score = round(raw * 100.0, 1)

        # Safety/urgency floors: observed exploitation plus realistic exposure/reachability
        # should not be hidden by a weighted average.
        floor = 0.0
        if kev and context.internet_exposed and (context.reachable or context.runtime_loaded):
            floor = 85.0
        elif kev:
            floor = 70.0
        elif epss >= 0.90 and context.internet_exposed:
            floor = 70.0
        score = max(score, floor)
        priority = self._priority(score)

        confidence_inputs = [intel.get("osv"), intel.get("github_advisory"), intel.get("nvd"), intel.get("epss") is not None]
        confidence_count = sum(bool(x) for x in confidence_inputs)
        confidence = "high" if confidence_count >= 3 else "medium" if confidence_count >= 2 else "low"

        reasons = []
        if kev:
            reasons.append("CISA KEV: known exploited vulnerability")
        if epss >= 0.50:
            reasons.append(f"High EPSS probability ({epss:.1%})")
        if context.internet_exposed:
            reasons.append("Asset is internet exposed")
        if context.reachable:
            reasons.append("Vulnerable component/path is reachable")
        if context.asset_criticality.lower() == "critical":
            reasons.append("Critical business asset")
        if context.privileged_component:
            reasons.append("Privileged component")
        if context.compensating_controls:
            reasons.append("Compensating controls recorded; analyst validation required")

        return {
            "score": score,
            "priority": priority,
            "confidence": confidence,
            "factors": factors,
            "weights": self.weights,
            "reasons": reasons,
            "context": asdict(context),
        }

    def _priority(self, score: float) -> str:
        ordered = sorted(((float(v), k) for k, v in self.thresholds.items()), reverse=True)
        for threshold, priority in ordered:
            if score >= threshold:
                return priority
        return "P4"


def _clamp(value: float) -> float:
    return min(1.0, max(0.0, value))
