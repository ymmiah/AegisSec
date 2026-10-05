#!/usr/bin/env python3
"""Helpers for installing and inspecting third-party agent skills.

This script never disables the skills CLI security scan. Imported skills remain
subordinate to AegisSec's canonical safety and engagement rules.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "mukul975/Anthropic-Cybersecurity-Skills"

COMMON_ROOTS = (
    ".skills",
    ".agents/skills",
    ".claude/skills",
    ".codex/skills",
    ".cursor/skills",
    ".gemini/skills",
    ".github/skills",
)


def _run(args: list[str]) -> int:
    print("+", " ".join(args))
    try:
        return subprocess.run(args, cwd=ROOT, check=False).returncode
    except FileNotFoundError:
        print("Node.js/npx was not found. Install Node.js, then retry.", file=sys.stderr)
        return 127


def install() -> int:
    # `--all -y` is supported by the open skills CLI. We deliberately do not
    # use --skip-check because third-party skill content is a supply-chain input.
    rc = _run(["npx", "skills", "add", SOURCE, "--all", "-y"])
    if rc == 0:
        _run(["npx", "skills", "generate-lock"])
    return rc


def update() -> int:
    rc = _run(["npx", "skills", "check"])
    if rc != 0:
        return rc
    rc = _run(["npx", "skills", "update"])
    if rc == 0:
        _run(["npx", "skills", "generate-lock"])
    return rc


def status() -> int:
    found: dict[str, int] = {}
    unique = set()
    for rel in COMMON_ROOTS:
        base = ROOT / rel
        if not base.exists():
            continue
        paths = list(base.rglob("SKILL.md"))
        if paths:
            found[rel] = len(paths)
            for p in paths:
                try:
                    unique.add(p.resolve())
                except OSError:
                    unique.add(p.absolute())
    lock = json.loads((ROOT / "upstream/source.lock.json").read_text(encoding="utf-8"))
    print(f"Upstream source: {lock['source']['repository']}")
    print(f"Reviewed commit: {lock['source']['audited_commit']}")
    print(f"Upstream reported skills at review: {lock['source']['reported_skills']}")
    if not found:
        print("No project-level third-party SKILL.md files detected.")
        print(f"Install with: npx skills add {SOURCE} --all -y")
        return 1
    for root, count in sorted(found.items()):
        print(f"{root}: {count} SKILL.md files")
    print(f"Unique resolved SKILL.md files: {len(unique)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("install")
    sub.add_parser("update")
    sub.add_parser("status")
    args = ap.parse_args()
    if args.cmd == "install":
        return install()
    if args.cmd == "update":
        return update()
    return status()


if __name__ == "__main__":
    raise SystemExit(main())
