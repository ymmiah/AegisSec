#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aegissec_vuln.engine import VulnerabilityIntelligenceEngine
from aegissec_vuln.models import AssetContext, Component
from aegissec_vuln.report import markdown_report
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


def output_result(result: dict, output: str | None, fmt: str) -> None:
    rendered = markdown_report(result) if fmt == "markdown" else json.dumps(result, indent=2, sort_keys=False)
    if output:
        Path(output).write_text(rendered, encoding="utf-8")
        print(f"Wrote {output}")
    else:
        print(rendered)


def cmd_scan(args) -> int:
    components = load_components(args.input)
    context = context_from_file(args.context)
    engine = build_engine(Path(args.config))
    result = engine.scan_components(components, context=context, enrich=not args.no_enrich, max_enrich=args.max_enrich)
    output_result(result, args.output, args.format)
    return 0


def cmd_package(args) -> int:
    component = Component(name=args.name, version=args.version, ecosystem=args.ecosystem, purl=args.purl)
    context = context_from_file(args.context)
    engine = build_engine(Path(args.config))
    result = engine.scan_components([component], context=context, enrich=not args.no_enrich, max_enrich=args.max_enrich)
    output_result(result, args.output, args.format)
    return 0


def cmd_enrich(args) -> int:
    context = context_from_file(args.context)
    engine = build_engine(Path(args.config))
    result = engine.enrich_identifier(args.identifier, context=context)
    print(json.dumps(result, indent=2))
    return 0


def cmd_repo(args) -> int:
    context = context_from_file(args.context)
    engine = build_engine(Path(args.config))
    data = run_source_scan(args.path, binary=args.scanner_bin)
    result = engine.ingest_osv_scanner(data, context=context, enrich=not args.no_enrich, max_enrich=args.max_enrich)
    output_result(result, args.output, args.format)
    return 0


def cmd_config(args) -> int:
    cfg = load_config(Path(args.config))
    print(json.dumps(cfg, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="aegissec-vuln", description="AegisSec vulnerability intelligence and prioritisation")
    p.add_argument("--config", default=str(ROOT / "config/vulnerability-intelligence.yaml"))
    sub = p.add_subparsers(dest="cmd", required=True)

    scan = sub.add_parser("scan", help="Scan CycloneDX/SPDX/generic component JSON via OSV and enrich findings")
    scan.add_argument("input")
    scan.add_argument("--context", help="Asset context YAML")
    scan.add_argument("--no-enrich", action="store_true")
    scan.add_argument("--max-enrich", type=int, default=50)
    scan.add_argument("--format", choices=["json", "markdown"], default="json")
    scan.add_argument("--output")
    scan.set_defaults(func=cmd_scan)

    pkg = sub.add_parser("package", help="Query one package/version")
    pkg.add_argument("--name", required=True)
    pkg.add_argument("--version", required=True)
    pkg.add_argument("--ecosystem")
    pkg.add_argument("--purl")
    pkg.add_argument("--context")
    pkg.add_argument("--no-enrich", action="store_true")
    pkg.add_argument("--max-enrich", type=int, default=50)
    pkg.add_argument("--format", choices=["json", "markdown"], default="json")
    pkg.add_argument("--output")
    pkg.set_defaults(func=cmd_package)

    repo = sub.add_parser("repo", help="Run local OSV-Scanner v2 against a source repository, then enrich/prioritise")
    repo.add_argument("path", nargs="?", default=".")
    repo.add_argument("--scanner-bin", default="osv-scanner")
    repo.add_argument("--context")
    repo.add_argument("--no-enrich", action="store_true")
    repo.add_argument("--max-enrich", type=int, default=50)
    repo.add_argument("--format", choices=["json", "markdown"], default="json")
    repo.add_argument("--output")
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
