#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aegissec_vuln.actions import PRIORITY_ORDER, apply_actions, compare_baseline, evaluate_gate
from aegissec_vuln.engine import VulnerabilityIntelligenceEngine
from aegissec_vuln.models import AssetContext, Component
from aegissec_vuln.report import markdown_report
from aegissec_vuln.sarif import sarif_report
from aegissec_vuln.risk import RiskEngine
from aegissec_vuln.sbom import load_components
from aegissec_vuln.osv_scanner import run_source_scan


def load_yaml(path: Path):
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("Install requirements: python -m pip install -r requirements.txt") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_config(path: Path) -> dict:
    return load_yaml(path) or {}


def context_from_file(path: str | None) -> AssetContext | None:
    if not path:
        return None
    raw = load_yaml(Path(path)) or {}
    data = raw.get("asset", raw)
    allowed = {
        "asset_id", "environment", "asset_criticality", "internet_exposed", "reachable",
        "runtime_loaded", "privileged_component", "sensitive_data", "compensating_controls", "owner"
    }
    return AssetContext(**{k: v for k, v in data.items() if k in allowed})


def build_engine(config_path: Path) -> VulnerabilityIntelligenceEngine:
    cfg = load_config(config_path)
    source_enabled = {name: bool(item.get("enabled", True)) for name, item in (cfg.get("sources") or {}).items()}
    risk = RiskEngine(cfg.get("prioritisation") or {})
    return VulnerabilityIntelligenceEngine(risk=risk, source_enabled=source_enabled)


GATE_EXIT_CODE = 3


def render(result: dict, fmt: str, artifact_uri: str | None = None) -> str:
    if fmt == "markdown":
        return markdown_report(result)
    if fmt == "sarif":
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "1"
        return json.dumps(sarif_report(result, artifact_uri=artifact_uri, version=version), indent=2)
    return json.dumps(result, indent=2, sort_keys=False)


def output_result(result: dict, output: str | None, fmt: str, artifact_uri: str | None = None) -> None:
    rendered = render(result, fmt, artifact_uri)
    if output:
        Path(output).write_text(rendered, encoding="utf-8")
        print(f"Wrote {output}", file=sys.stderr)
    else:
        print(rendered)


def finalise(result: dict, args, context: AssetContext | None, artifact_uri: str | None = None) -> int:
    """Add the fix plan, deadlines, baseline diff and CI gate; write every requested output."""
    cfg = load_config(Path(args.config))
    if context:
        result["context"] = context.to_dict()
    apply_actions(result, owner=context.owner if context else None, sla_days=cfg.get("remediation_sla_days"))
    if getattr(args, "baseline", None):
        baseline_path = Path(args.baseline)
        if baseline_path.exists():
            compare_baseline(result, json.loads(baseline_path.read_text(encoding="utf-8")))
        else:
            result.setdefault("warnings", []).append(f"Baseline {args.baseline} not found; every finding treated as new")
    gate = evaluate_gate(result, getattr(args, "fail_on", None), new_only=getattr(args, "new_only", False))

    output_result(result, args.output, args.format, artifact_uri)
    for extra_fmt, path in (("json", getattr(args, "json_out", None)), ("markdown", getattr(args, "markdown_out", None)), ("sarif", getattr(args, "sarif_out", None))):
        if path:
            Path(path).write_text(render(result, extra_fmt, artifact_uri), encoding="utf-8")
            print(f"Wrote {path}", file=sys.stderr)

    if gate["breached"]:
        print(
            f"AegisSec gate: {gate['count']} finding(s) at {gate['fail_on']} or above"
            f"{' (new since baseline)' if gate.get('new_only') else ''} — failing (exit {GATE_EXIT_CODE})",
            file=sys.stderr,
        )
        return GATE_EXIT_CODE
    return 0


def cmd_scan(args) -> int:
    components = load_components(args.input)
    context = context_from_file(args.context)
    engine = build_engine(Path(args.config))
    result = engine.scan_components(components, context=context, enrich=not args.no_enrich, max_enrich=args.max_enrich)
    return finalise(result, args, context, artifact_uri=args.input)


def cmd_package(args) -> int:
    component = Component(name=args.name, version=args.version, ecosystem=args.ecosystem, purl=args.purl)
    context = context_from_file(args.context)
    engine = build_engine(Path(args.config))
    result = engine.scan_components([component], context=context, enrich=not args.no_enrich, max_enrich=args.max_enrich)
    return finalise(result, args, context)


def cmd_enrich(args) -> int:
    context = context_from_file(args.context)
    engine = build_engine(Path(args.config))
    result = engine.enrich_identifier(args.identifier, context=context)
    print(json.dumps(result, indent=2))
    return 0


def _relative_paths(result: dict, roots: list[str]) -> None:
    """Report lockfile paths relative to the repository so SARIF links resolve."""
    prefixes = sorted({str(Path(r).resolve()).rstrip("/") + "/" for r in roots if r}, key=len, reverse=True)
    for finding in result.get("findings") or []:
        component = finding.get("component") or {}
        path = component.get("path")
        for prefix in prefixes:
            if path and path.startswith(prefix):
                component["path"] = path[len(prefix):]
                break


def cmd_repo(args) -> int:
    context = context_from_file(args.context)
    engine = build_engine(Path(args.config))
    if args.from_osv_json:
        # Reuse output from an existing OSV-Scanner run (e.g. the official GitHub Action).
        data = json.loads(Path(args.from_osv_json).read_text(encoding="utf-8"))
    else:
        data = run_source_scan(args.path, binary=args.scanner_bin)
    result = engine.ingest_osv_scanner(data, context=context, enrich=not args.no_enrich, max_enrich=args.max_enrich)
    _relative_paths(result, [args.path, os.environ.get("GITHUB_WORKSPACE", ""), "/github/workspace"])
    return finalise(result, args, context)


def cmd_config(args) -> int:
    cfg = load_config(Path(args.config))
    print(json.dumps(cfg, indent=2))
    return 0


def add_report_options(p: argparse.ArgumentParser) -> None:
    p.add_argument("--context", help="Asset context YAML (enables prioritisation, deadlines and owner)")
    p.add_argument("--no-enrich", action="store_true")
    p.add_argument("--max-enrich", type=int, default=50)
    p.add_argument("--format", choices=["json", "markdown", "sarif"], default="json", help="Format for --output / stdout")
    p.add_argument("--output", help="Write the main report here instead of stdout")
    p.add_argument("--json-out", help="Also write the full JSON result (use it as the next --baseline)")
    p.add_argument("--markdown-out", help="Also write the Markdown report")
    p.add_argument("--sarif-out", help="Also write SARIF 2.1.0 for GitHub code scanning")
    p.add_argument("--baseline", help="Previous JSON result; marks findings new and lists resolved ones")
    p.add_argument("--fail-on", choices=PRIORITY_ORDER, help=f"Exit {GATE_EXIT_CODE} if any finding is at this priority or above")
    p.add_argument("--new-only", action="store_true", help="With --fail-on and --baseline: only new findings can fail the gate")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="aegissec-vuln",
        description="AegisSec vulnerability intelligence and prioritisation",
        epilog=f"Exit codes: 0 success · 2 error · {GATE_EXIT_CODE} --fail-on gate breached",
    )
    p.add_argument("--config", default=str(ROOT / "config/vulnerability-intelligence.yaml"))
    sub = p.add_subparsers(dest="cmd", required=True)

    scan = sub.add_parser("scan", help="Scan CycloneDX/SPDX/generic component JSON via OSV and enrich findings")
    scan.add_argument("input")
    add_report_options(scan)
    scan.set_defaults(func=cmd_scan)

    pkg = sub.add_parser("package", help="Query one package/version")
    pkg.add_argument("--name", required=True)
    pkg.add_argument("--version", required=True)
    pkg.add_argument("--ecosystem")
    pkg.add_argument("--purl")
    add_report_options(pkg)
    pkg.set_defaults(func=cmd_package)

    repo = sub.add_parser("repo", help="Run local OSV-Scanner v2 against a source repository, then enrich/prioritise")
    repo.add_argument("path", nargs="?", default=".")
    repo.add_argument("--scanner-bin", default="osv-scanner")
    repo.add_argument("--from-osv-json", help="Read an existing OSV-Scanner v2 JSON file instead of running the scanner")
    add_report_options(repo)
    repo.set_defaults(func=cmd_repo)

    enrich = sub.add_parser("enrich", help="Enrich a CVE/GHSA identifier with public intelligence")
    enrich.add_argument("identifier")
    enrich.add_argument("--context")
    enrich.set_defaults(func=cmd_enrich)

    cfg = sub.add_parser("show-config")
    cfg.set_defaults(func=cmd_config)
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"AegisSec vulnerability intelligence error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
