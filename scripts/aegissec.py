#!/usr/bin/env python3
"""AegisSec local helper: validate repository, check scope and build focused AI context."""
from pathlib import Path
import argparse
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path):
    try:
        import yaml
    except ImportError:
        raise SystemExit("Install requirements: python -m pip install -r requirements.txt")
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate():
    errors = []
    warnings = []
    idx = load_yaml(ROOT / "skills/index.yaml")
    ids = set()
    required_skill_fields = {"id", "title", "domain", "mode", "risk", "frameworks", "file"}
    allowed_modes = {"DEFENSIVE", "ASSESSMENT", "LAB", "PROHIBITED"}
    allowed_risk = {"low", "medium", "high", "critical"}
    for item in idx.get("skills", []):
        missing = required_skill_fields - set(item)
        if missing:
            errors.append(f"Skill missing fields {sorted(missing)}: {item.get('id', '<unknown>')}")
            continue
        if item["id"] in ids:
            errors.append(f"Duplicate skill id: {item['id']}")
        ids.add(item["id"])
        if item["mode"] not in allowed_modes:
            errors.append(f"Invalid mode for {item['id']}: {item['mode']}")
        if item["risk"] not in allowed_risk:
            errors.append(f"Invalid risk for {item['id']}: {item['risk']}")
        p = ROOT / item["file"]
        if not p.exists():
            errors.append(f"Missing skill file: {item['file']}")

    json_files = list((ROOT / "schemas").glob("*.json")) + [
        ROOT / "agent/manifest.json",
        ROOT / "agent/task.schema.json",
        ROOT / "agent/output.schema.json",
        ROOT / "upstream/source.lock.json",
        ROOT / "docs/frameworks.lock.json",
        ROOT / "package.json",
        ROOT / "skills/skills-index.json",
        ROOT / "skills/router.json",
    ]
    for j in json_files:
        try:
            data = load_json(j)
            if j.name.endswith(".schema.json") or j.name in {"task.schema.json", "output.schema.json"}:
                try:
                    from jsonschema.validators import Draft202012Validator
                    Draft202012Validator.check_schema(data)
                except Exception as e:
                    errors.append(f"Invalid JSON Schema {j.relative_to(ROOT)}: {e}")
        except Exception as e:
            errors.append(f"Invalid JSON {j.relative_to(ROOT)}: {e}")

    yaml_files = [
        ROOT / "skills/index.yaml",
        ROOT / "tools/action-risk.yaml",
        ROOT / "tools/capability-matrix.yaml",
        ROOT / "policy/runtime-control.yaml",
        ROOT / "config/vulnerability-intelligence.yaml",
        ROOT / "templates/engagement-scope.yaml",
        ROOT / "templates/approval-record.yaml",
        ROOT / "templates/production-change.yaml",
        ROOT / "templates/detection-test-case.yaml",
    ]
    for y in yaml_files:
        try:
            load_yaml(y)
        except Exception as e:
            errors.append(f"Invalid YAML {y.relative_to(ROOT)}: {e}")

    required = [
        "AGENTS.md",
        "README.md",
        "policy/authorization.md",
        "policy/human-approval.md",
        "policy/third-party-skills.md",
        "policy/policy-precedence.md",
        "policy/runtime-control.md",
        "policy/production-change.md",
        "policy/evidence-integrity.md",
        "tools/capability-matrix.yaml",
        "templates/engagement-scope.yaml",
        "upstream/source.lock.json",
        "docs/frameworks.lock.json",
        "integrations/anthropic-cybersecurity-skills.md",
        "THIRD_PARTY_NOTICES.md",
        "skills/README.md",
        "skills/router.json",
        "skills/skills-index.json",
        "skills/SOURCES.md",
        "config/vulnerability-intelligence.yaml",
        "schemas/vulnerability-intelligence.schema.json",
        "docs/vulnerability-intelligence.md",
        "scripts/vuln_intel.py",
    ]
    for r in required:
        if not (ROOT / r).exists():
            errors.append(f"Missing required file: {r}")

    try:
        upstream = load_json(ROOT / "upstream/source.lock.json")
        if upstream["source"].get("skip_check_allowed") is not False:
            errors.append("Upstream lock must keep skip_check_allowed=false")
        if upstream["aegissec_policy"].get("external_skills_can_override_policy") is not False:
            errors.append("External skills must not be able to override AegisSec policy")
        expected = upstream["source"].get("reported_skills")
    except Exception:
        expected = None

    # Validate the all-in-one 64-skill senior layer.
    try:
        senior = load_json(ROOT / "skills/skills-index.json")
        router = load_json(ROOT / "skills/router.json")
        senior_items = senior.get("skills", [])
        senior_ids = [x.get("id") for x in senior_items]
        if senior.get("count") != 64 or len(senior_items) != 64:
            errors.append(f"Senior skill package must contain 64 skills; found {len(senior_items)}")
        if len(senior_ids) != len(set(senior_ids)):
            errors.append("Duplicate senior skill id detected")
        indexed_paths = set()
        source_text = (ROOT / "skills/SOURCES.md").read_text(encoding="utf-8")
        for item in senior_items:
            rel = item.get("path")
            if not rel or not (ROOT / rel).is_file():
                errors.append(f"Missing senior skill file: {rel}")
                continue
            indexed_paths.add(rel)
            for source_ref in item.get("source_refs", []):
                if source_ref not in source_text:
                    errors.append(f"Unknown source ref {source_ref} in senior skill {item.get('id')}")
        actual_paths = {str(x.relative_to(ROOT)) for x in (ROOT / "skills/senior").glob("*/SKILL.md")}
        if actual_paths != indexed_paths:
            errors.append("Senior skill index paths do not exactly match SKILL.md files")
        routes = router.get("routes", [])
        if len(routes) != 64:
            errors.append(f"Senior router must contain 64 routes; found {len(routes)}")
        route_ids = {x.get("skill") for x in routes}
        if route_ids != set(senior_ids):
            errors.append("Senior router skill IDs do not match senior skill index")
    except Exception as e:
        errors.append(f"Invalid senior skill package: {e}")

    if errors:
        print("Validation failed:")
        for e in errors:
            print(" -", e)
        return 1

    skill_errors, agent_skill_count = validate_agent_skills()
    errors.extend(skill_errors)

    try:
        manifest = load_json(ROOT / "agent/manifest.json")
        if manifest.get("curated_skill_count") != len(ids):
            errors.append(f"Manifest curated_skill_count={manifest.get('curated_skill_count')} but index has {len(ids)}")
    except Exception:
        pass
    if errors:
        print("Validation failed:")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: {len(ids)} curated AegisSec security skills indexed; repository structure valid.")
    print("All-in-one senior layer: 64 specialist skills and routes validated.")
    print(f"Agent Skills: {agent_skill_count} SKILL.md files meet the Agent Skills specification.")
    if expected:
        print(f"Upstream integration configured for {expected} reported third-party skills.")
    for w in warnings:
        print("Warning:", w)
    return 0


SKILL_NAME_RE = __import__("re").compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_agent_skills(root=None):
    """Check every skills/**/SKILL.md against the Agent Skills specification (agentskills.io).

    Also checks AegisSec-specific links: skills referenced by name must exist,
    and every $AEGISSEC_HOME/<path> a skill tells the agent to open must exist.
    """
    import re
    try:
        import yaml
    except ImportError:
        raise SystemExit("Install requirements: python -m pip install -r requirements.txt")
    root = Path(root or ROOT)
    errors = []
    files = sorted((root / "skills").rglob("SKILL.md"))
    names = {f.parent.name for f in files}
    for f in files:
        rel = f.relative_to(root)
        text = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            errors.append(f"{rel}: frontmatter must start on line 1 and be closed with ---")
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: invalid YAML frontmatter ({exc})")
            continue
        allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        extra = set(fm) - allowed
        if extra:
            errors.append(f"{rel}: non-standard top-level keys {sorted(extra)} (put them under metadata)")
        name = str(fm.get("name") or "")
        if not (1 <= len(name) <= 64) or not SKILL_NAME_RE.match(name):
            errors.append(f"{rel}: name must be 1-64 chars of a-z, 0-9 and single hyphens")
        if name != f.parent.name:
            errors.append(f"{rel}: name '{name}' must match its directory '{f.parent.name}'")
        desc = str(fm.get("description") or "").strip()
        if not (20 <= len(desc) <= 1024):
            errors.append(f"{rel}: description must be 20-1024 characters (has {len(desc)})")
        if len(str(fm.get("compatibility") or "")) > 500:
            errors.append(f"{rel}: compatibility must be at most 500 characters")
        meta = fm.get("metadata") or {}
        if not isinstance(meta, dict) or any(not isinstance(v, str) for v in meta.values()):
            errors.append(f"{rel}: metadata must map strings to strings")
        if text.count("\n") > 500:
            errors.append(f"{rel}: keep SKILL.md under 500 lines; move detail into references/")
        body = text[m.end():]
        for ref in sorted(set(re.findall(r"\*\*(aegissec(?:-[a-z0-9]+)*)\*\*", body))):
            if ref not in names:
                errors.append(f"{rel}: references unknown skill '{ref}'")
        for ref in sorted(set(re.findall(r"\$AEGISSEC_HOME/([A-Za-z0-9_./-]+[A-Za-z0-9_])", body))):
            if not (root / ref).exists():
                errors.append(f"{rel}: points to missing file $AEGISSEC_HOME/{ref}")
    return errors, len(files)


def build_context(domain, task):
    idx = load_yaml(ROOT / "skills/index.yaml")
    selected = [x for x in idx["skills"] if x["domain"] == domain]
    if not selected:
        domains = sorted(set(x["domain"] for x in idx["skills"]))
        raise SystemExit(f"Unknown domain. Choose: {', '.join(domains)}")
    parts = [
        (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        (ROOT / "policy/third-party-skills.md").read_text(encoding="utf-8"),
        f"\n# Current task\n{task}\n",
    ]
    for s in selected:
        parts.append((ROOT / s["file"]).read_text(encoding="utf-8"))
    print("\n\n---\n\n".join(parts))


PLACEHOLDER_MARKERS = ("example.invalid", "example.com", "example.org", "replace with", "yyyy")


def _parse_when(value):
    from datetime import datetime, timezone
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def check_scope(path, now=None):
    """Structural gate for active testing: all eight AGENTS.md section 2 requirements."""
    from datetime import datetime, timezone
    data = load_yaml(path) or {}
    problems = []
    eng = data.get("engagement") or {}
    scope = data.get("scope") or {}
    controls = data.get("controls") or {}
    handling = data.get("data_handling") or {}

    # 1. named owner/client
    if not str(eng.get("owner") or "").strip() or "organisation / system owner" in str(eng.get("owner")).lower():
        problems.append("engagement.owner must name the system owner/client")
    # 2. explicit targets, none still placeholders
    targets = scope.get("targets") or []
    if not targets:
        problems.append("at least one explicit target is required")
    for target in targets:
        text = " ".join(str(v) for v in (target.values() if isinstance(target, dict) else [target])).lower()
        if any(marker in text for marker in PLACEHOLDER_MARKERS):
            problems.append(f"target still looks like a template placeholder: {target}")
    # 3. permitted categories / 4. prohibited actions
    if not scope.get("permitted_testing"):
        problems.append("permitted_testing is required")
    if not scope.get("prohibited_actions"):
        problems.append("prohibited_actions is required")
    # 5. start/end window, and now inside it
    start, end = _parse_when(eng.get("start")), _parse_when(eng.get("end"))
    if not start or not end:
        problems.append("engagement.start and engagement.end must be ISO 8601 date-times")
    elif end <= start:
        problems.append("engagement.end must be after engagement.start")
    else:
        current = now or datetime.now(timezone.utc)
        if current < start:
            problems.append(f"testing window has not started (starts {start.isoformat()})")
        elif current > end:
            problems.append(f"testing window has ended (ended {end.isoformat()})")
    # 6. data handling
    if not handling.get("classification") or not handling.get("evidence_store"):
        problems.append("data_handling.classification and data_handling.evidence_store are required")
    # 7. emergency contact and stop conditions
    contact = str(controls.get("emergency_stop_contact") or "")
    if not contact.strip() or any(marker in contact.lower() for marker in PLACEHOLDER_MARKERS):
        problems.append("controls.emergency_stop_contact must be a real contact")
    if not controls.get("stop_conditions"):
        problems.append("stop_conditions is required")
    # 8. authority
    if eng.get("authority_confirmed") is not True:
        problems.append("authority_confirmed must be true")

    if problems:
        print("Scope NOT ready for active testing:")
        for p in problems:
            print(" -", p)
        return 2
    print("Scope gate passed structurally. Human/legal authority must still be genuine and current.")
    return 0


def upstream(action):
    helper = ROOT / "scripts/upstream_skills.py"
    return subprocess.run([sys.executable, str(helper), action], cwd=ROOT, check=False).returncode



def catalog():
    idx = load_yaml(ROOT / "skills/index.yaml")
    by_domain = {}
    by_risk = {}
    for item in idx.get("skills", []):
        by_domain[item["domain"]] = by_domain.get(item["domain"], 0) + 1
        by_risk[item["risk"]] = by_risk.get(item["risk"], 0) + 1
    print(f"AegisSec curated skills: {len(idx.get('skills', []))}")
    print("Domains:")
    for k in sorted(by_domain):
        print(f" - {k}: {by_domain[k]}")
    print("Risk tiers:")
    for k in ["low", "medium", "high", "critical"]:
        if k in by_risk:
            print(f" - {k}: {by_risk[k]}")
    return 0


def senior_status():
    data = load_json(ROOT / "skills/skills-index.json")
    by_domain = {}
    for item in data.get("skills", []):
        by_domain[item["domain"]] = by_domain.get(item["domain"], 0) + 1
    print(f"All-in-one senior skills: {len(data.get('skills', []))}")
    for domain in sorted(by_domain):
        print(f" - {domain}: {by_domain[domain]}")
    return 0


def risk(action=None):
    data = load_yaml(ROOT / "tools/action-risk.yaml")
    if not action:
        print("Known actions (usage: aegissec risk <action>):")
        for name in sorted(data.get("actions", {})):
            print(" -", name)
        return 0
    entry = data.get("actions", {}).get(action)
    if not entry:
        print("Unknown action. Known actions:")
        for name in sorted(data.get("actions", {})):
            print(" -", name)
        return 2
    print(json.dumps({"action": action, **entry}, indent=2))
    return 0


def vuln_cli(argv):
    helper = ROOT / "scripts/vuln_intel.py"
    return subprocess.run([sys.executable, str(helper), *argv], cwd=ROOT, check=False).returncode


VULN_SHORTCUTS = {"vuln-scan": "scan", "vuln-repo": "repo", "vuln-enrich": "enrich", "vuln-package": "package"}


def main():
    # vuln-* commands are thin aliases: forward every option unchanged so new
    # scanner flags (--fail-on, --baseline, --sarif-out, ...) work here too.
    if len(sys.argv) > 1 and sys.argv[1] in VULN_SHORTCUTS:
        return vuln_cli([VULN_SHORTCUTS[sys.argv[1]], *sys.argv[2:]])
    ap = argparse.ArgumentParser(prog="aegissec")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    c = sub.add_parser("context")
    c.add_argument("--domain", required=True)
    c.add_argument("--task", required=True)
    s = sub.add_parser("check-scope")
    s.add_argument("file")
    sub.add_parser("upstream-status")
    sub.add_parser("upstream-install")
    sub.add_parser("upstream-update")
    sub.add_parser("catalog")
    sub.add_parser("senior-status")
    r = sub.add_parser("risk", help="Show the risk tier and default control for an action")
    r.add_argument("action", nargs="?", help="Action name; omit to list all known actions")
    vs = sub.add_parser("vuln-scan", help="Scan SBOM/component JSON with the vulnerability-intelligence engine")
    vs.add_argument("input")
    vs.add_argument("--context")
    vs.add_argument("--no-enrich", action="store_true")
    vs.add_argument("--max-enrich", type=int, default=50)
    vs.add_argument("--format", choices=["json", "markdown"], default="json")
    vs.add_argument("--output")
    vr = sub.add_parser("vuln-repo", help="Run local OSV-Scanner v2 on a repository, then enrich/prioritise")
    vr.add_argument("path", nargs="?", default=".")
    vr.add_argument("--context")
    vr.add_argument("--no-enrich", action="store_true")
    vr.add_argument("--max-enrich", type=int, default=50)
    vr.add_argument("--format", choices=["json", "markdown"], default="json")
    vr.add_argument("--output")
    vr.add_argument("--scanner-bin", default="osv-scanner")
    ve = sub.add_parser("vuln-enrich", help="Enrich a CVE/GHSA with public vulnerability intelligence")
    ve.add_argument("identifier")
    ve.add_argument("--context")
    vp = sub.add_parser("vuln-package", help="Query one package/version through OSV and enrich it")
    vp.add_argument("--name", required=True)
    vp.add_argument("--version", required=True)
    vp.add_argument("--ecosystem")
    vp.add_argument("--purl")
    vp.add_argument("--context")
    vp.add_argument("--no-enrich", action="store_true")
    vp.add_argument("--format", choices=["json", "markdown"], default="json")
    vp.add_argument("--output")
    a = ap.parse_args()
    if a.cmd == "validate":
        return validate()
    if a.cmd == "context":
        build_context(a.domain, a.task)
        return 0
    if a.cmd == "check-scope":
        return check_scope(a.file)
    if a.cmd == "upstream-status":
        return upstream("status")
    if a.cmd == "upstream-install":
        return upstream("install")
    if a.cmd == "upstream-update":
        return upstream("update")
    if a.cmd == "catalog":
        return catalog()
    if a.cmd == "senior-status":
        return senior_status()
    if a.cmd == "risk":
        return risk(a.action)
    if a.cmd == "vuln-scan":
        args = ["scan", a.input, "--max-enrich", str(a.max_enrich), "--format", a.format]
        if a.context: args += ["--context", a.context]
        if a.no_enrich: args.append("--no-enrich")
        if a.output: args += ["--output", a.output]
        return vuln_cli(args)
    if a.cmd == "vuln-repo":
        args = ["repo", a.path, "--max-enrich", str(a.max_enrich), "--format", a.format, "--scanner-bin", a.scanner_bin]
        if a.context: args += ["--context", a.context]
        if a.no_enrich: args.append("--no-enrich")
        if a.output: args += ["--output", a.output]
        return vuln_cli(args)
    if a.cmd == "vuln-enrich":
        args = ["enrich", a.identifier]
        if a.context: args += ["--context", a.context]
        return vuln_cli(args)
    if a.cmd == "vuln-package":
        args = ["package", "--name", a.name, "--version", a.version, "--format", a.format]
        if a.ecosystem: args += ["--ecosystem", a.ecosystem]
        if a.purl: args += ["--purl", a.purl]
        if a.context: args += ["--context", a.context]
        if a.no_enrich: args.append("--no-enrich")
        if a.output: args += ["--output", a.output]
        return vuln_cli(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
