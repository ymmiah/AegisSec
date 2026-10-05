from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


class OsvScannerError(RuntimeError):
    pass


def run_source_scan(path: str | Path, binary: str = "osv-scanner") -> dict[str, Any]:
    resolved = shutil.which(binary) if "/" not in binary else binary
    if not resolved:
        raise OsvScannerError(
            "osv-scanner is not installed. Install OSV-Scanner v2 or use `vuln-scan` with an SBOM/component inventory."
        )
    target = str(Path(path).resolve())
    cmd = [resolved, "scan", "source", "--format", "json", "--recursive", target]
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if not proc.stdout.strip():
        raise OsvScannerError(f"OSV-Scanner returned no JSON output (exit={proc.returncode}): {proc.stderr.strip()[:500]}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise OsvScannerError(f"Invalid JSON from OSV-Scanner: {exc}") from exc
    data.setdefault("_aegissec", {})["scanner_exit_code"] = proc.returncode
    if proc.stderr.strip():
        data["_aegissec"]["scanner_stderr"] = proc.stderr.strip()[-2000:]
    return data


def iter_packages(data: dict[str, Any]):
    """Yield (source, package, vulnerabilities) from OSV-Scanner v2 JSON."""
    for result in data.get("results", []) or []:
        source = result.get("source") or {}
        for entry in result.get("packages", []) or []:
            package = entry.get("package") or {}
            vulns = entry.get("vulnerabilities") or []
            if package.get("name") and package.get("version"):
                yield source, package, vulns
