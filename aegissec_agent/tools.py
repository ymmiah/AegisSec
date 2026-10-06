"""Tools the AegisSec harness exposes to the model.

Every tool declares an ``action`` from ``tools/action-risk.yaml`` so the policy
gate can govern it. The shipped tools are all low-risk and read-only or public
intelligence: the harness advises and analyses, it does not change live systems.
A host embedding the harness can register further tools; higher-risk ones are
automatically gated by their declared action.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
MAX_READ = 60_000


@dataclass
class Tool:
    name: str
    description: str
    action: str
    input_schema: dict
    handler: Callable[[dict], str]


@dataclass
class ToolContext:
    workdir: Path
    config_path: Path = ROOT / "config/vulnerability-intelligence.yaml"
    scope_file: Path | None = None
    extra: dict = field(default_factory=dict)


# --- helpers -----------------------------------------------------------------

def _safe_path(ctx: ToolContext, rel: str) -> Path:
    """Resolve ``rel`` inside the workdir; refuse anything outside it."""
    base = ctx.workdir.resolve()
    target = (base / rel).resolve()
    if base != target and base not in target.parents:
        raise ValueError(f"path '{rel}' is outside the working directory")
    return target


def _aegissec_cli():
    spec = importlib.util.spec_from_file_location("aegissec_cli", ROOT / "scripts/aegissec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _vuln_markdown(result: dict, context) -> str:
    from aegissec_vuln.actions import apply_actions
    from aegissec_vuln.report import markdown_report
    if context:
        result["context"] = context.to_dict()
    apply_actions(result, owner=getattr(context, "owner", None) if context else None)
    return markdown_report(result)


# --- tool handlers -----------------------------------------------------------

def _list_skills(_: dict) -> str:
    import yaml
    out = ["AegisSec operational skills (skills/aegissec/):"]
    for p in sorted((ROOT / "skills/aegissec").glob("*/SKILL.md")):
        m = p.read_text(encoding="utf-8").split("---")
        meta = yaml.safe_load(m[1]) if len(m) > 2 else {}
        out.append(f"- {meta.get('name', p.parent.name)}: {meta.get('description','').split('. ')[0]}.")
    native = yaml.safe_load((ROOT / "skills/index.yaml").read_text(encoding="utf-8"))
    out.append("\nAegisSec native security skills (skills/index.yaml) — read one with read_skill by id:")
    out += [f"- {s['id']} ({s['domain']}, {s['mode']})" for s in native.get("skills", [])[:60]]
    return "\n".join(out)


def _read_skill(args: dict) -> str:
    name = str(args.get("name", "")).strip()
    candidates = [
        ROOT / "skills/aegissec" / name / "SKILL.md",
        *(ROOT / "skills").glob(f"*/{name}.md"),
        *(ROOT / "skills").glob(f"{name}/SKILL.md"),
    ]
    import yaml
    native = {s["id"]: s["file"] for s in yaml.safe_load((ROOT / "skills/index.yaml").read_text()).get("skills", [])}
    if name in native:
        candidates.insert(0, ROOT / native[name])
    for c in candidates:
        if c.exists():
            return c.read_text(encoding="utf-8")[:MAX_READ]
    return f"No skill named '{name}'. Use list_skills to see what is available."


def _make_check_scope(ctx: ToolContext):
    def handler(args: dict) -> str:
        rel = args.get("path") or (str(ctx.scope_file) if ctx.scope_file else "")
        if not rel:
            return "No scope file given. Provide 'path' to an engagement YAML."
        path = _safe_path(ctx, rel) if not Path(rel).is_absolute() else Path(rel)
        if not path.exists():
            return f"Scope file not found: {rel}"
        cli = _aegissec_cli()
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli.check_scope(str(path))
        return f"{buf.getvalue()}\n(scope {'PASSED' if code == 0 else 'NOT ready'})"
    return handler


def _make_read_file(ctx: ToolContext):
    def handler(args: dict) -> str:
        path = _safe_path(ctx, str(args.get("path", "")))
        if not path.exists() or not path.is_file():
            return f"No such file: {args.get('path')}"
        data = path.read_bytes()[: MAX_READ + 1]
        if b"\x00" in data:
            return f"{args.get('path')} looks binary; not shown."
        text = data.decode("utf-8", errors="replace")
        note = "\n…(truncated)" if len(text) > MAX_READ else ""
        return text[:MAX_READ] + note
    return handler


def _make_list_files(ctx: ToolContext):
    def handler(args: dict) -> str:
        base = ctx.workdir.resolve()
        pattern = str(args.get("glob", "**/*"))
        skip = {".git", "node_modules", "__pycache__", ".venv", "dist", "build", "vendor"}
        files = []
        for p in sorted(base.glob(pattern)):
            if p.is_file() and not (skip & set(p.relative_to(base).parts)):
                files.append(str(p.relative_to(base)))
            if len(files) >= 400:
                files.append("…(more omitted)")
                break
        return "\n".join(files) or "(no files matched)"
    return handler


def _load_vuln_cli():
    import importlib.util as il
    spec = il.spec_from_file_location("vuln_cli", ROOT / "scripts/vuln_intel.py")
    mod = il.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _make_scan(ctx: ToolContext):
    def handler(args: dict) -> str:
        vcli = _load_vuln_cli()
        from aegissec_vuln.models import Component
        ctx_file = args.get("context") or ctx.extra.get("context_file")
        context = vcli.context_from_file(ctx_file) if ctx_file else None
        engine = vcli.build_engine(ctx.config_path)
        try:
            if args.get("sbom"):
                comps = vcli.load_components(str(_safe_path(ctx, args["sbom"])))
                result = engine.scan_components(comps, context=context)
            elif args.get("name") and args.get("version"):
                comp = Component(name=args["name"], version=args["version"],
                                 ecosystem=args.get("ecosystem"), purl=args.get("purl"))
                result = engine.scan_components([comp], context=context)
            else:
                return "Provide either 'sbom' (path to a CycloneDX/SPDX/component JSON) or 'name'+'version'+'ecosystem'."
        except Exception as exc:  # network or parse failure
            return f"Scan could not complete: {exc}"
        return _vuln_markdown(result, context)
    return handler


def _make_enrich(ctx: ToolContext):
    def handler(args: dict) -> str:
        vcli = _load_vuln_cli()
        ident = str(args.get("id", "")).strip()
        if not ident:
            return "Provide a CVE, GHSA or OSV id."
        ctx_file = args.get("context") or ctx.extra.get("context_file")
        context = vcli.context_from_file(ctx_file) if ctx_file else None
        engine = vcli.build_engine(ctx.config_path)
        try:
            return json.dumps(engine.enrich_identifier(ident, context=context), indent=2)[:MAX_READ]
        except Exception as exc:
            return f"Enrichment could not complete: {exc}"
    return handler


# --- registry ----------------------------------------------------------------

def build_tools(ctx: ToolContext) -> list[Tool]:
    return [
        Tool("list_skills", "List the AegisSec skills you can load (operational and native security skills).",
             "read_local_artifacts", {"type": "object", "properties": {}}, _list_skills),
        Tool("read_skill", "Read one AegisSec skill in full by its name or id, then follow it.",
             "read_local_artifacts",
             {"type": "object", "properties": {"name": {"type": "string", "description": "Skill name or id, e.g. aegissec-vuln-scan or secure-code-review"}}, "required": ["name"]},
             _read_skill),
        Tool("list_files", "List files in the working directory (for code or config review). Optional glob.",
             "read_local_artifacts",
             {"type": "object", "properties": {"glob": {"type": "string", "description": "Glob like **/*.php (default **/*)"}}},
             _make_list_files(ctx)),
        Tool("read_file", "Read a file inside the working directory. Read-only and sandboxed to the workdir.",
             "read_local_artifacts",
             {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
             _make_read_file(ctx)),
        Tool("scan_dependencies", "Scan an SBOM/component JSON or one package for known vulnerabilities and get a prioritised fix plan.",
             "query_public_vulnerability_intelligence",
             {"type": "object", "properties": {
                 "sbom": {"type": "string", "description": "Path (in the workdir) to a CycloneDX/SPDX/component JSON"},
                 "name": {"type": "string"}, "version": {"type": "string"},
                 "ecosystem": {"type": "string", "description": "npm, PyPI, Maven, Packagist, Go…"},
                 "purl": {"type": "string"}, "context": {"type": "string", "description": "Path to an asset-context YAML"}}},
             _make_scan(ctx)),
        Tool("enrich_vulnerability", "Pull live CVSS, EPSS, CISA KEV, fixed versions and priority for one CVE/GHSA/OSV id.",
             "query_public_vulnerability_intelligence",
             {"type": "object", "properties": {"id": {"type": "string"}, "context": {"type": "string"}}, "required": ["id"]},
             _make_enrich(ctx)),
        Tool("check_scope", "Validate an engagement scope file against all eight AegisSec requirements before any active testing.",
             "read_local_artifacts",
             {"type": "object", "properties": {"path": {"type": "string"}}},
             _make_check_scope(ctx)),
    ]
