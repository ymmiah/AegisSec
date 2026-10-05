import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from aegissec_vuln.actions import apply_actions, compare_baseline, evaluate_gate, is_major_upgrade
from aegissec_vuln.report import markdown_report
from aegissec_vuln.sarif import sarif_report

ROOT = Path(__file__).resolve().parents[1]


def finding(fid, name, version, priority, score, own_fix, kev=False, cvss=7.5):
    return {
        "id": fid,
        "identifiers": {"cve": [fid] if fid.startswith("CVE") else [], "ghsa": [], "osv": [], "other": []},
        "component": {"name": name, "version": version, "ecosystem": "npm", "path": None},
        "summary": f"Issue {fid}",
        "fixed_versions": [own_fix] if own_fix else [],
        "intelligence": {"cvss_score": cvss, "epss": 0.97 if kev else 0.01, "cisa_kev": kev, "sources": {"osv": {"id": fid}}},
        "assessment": {"priority": priority, "score": score, "confidence": "high", "reasons": []},
        "remediation": {"recommended_version": own_fix, "production_change_control_required": True},
    }


def sample_result():
    return {
        "schema_version": "1.0",
        "generated_at": "2026-10-05T12:00:00+00:00",
        "component_count": 3,
        "finding_count": 5,
        "warnings": [],
        "findings": [
            finding("CVE-2021-44228", "log4j-core", "2.14.1", "P0", 92.5, "2.15.0", kev=True, cvss=10.0),
            finding("CVE-2021-44832", "log4j-core", "2.14.1", "P1", 70.0, "2.17.1"),
            finding("CVE-2021-23337", "lodash", "4.17.20", "P2", 53.0, "4.17.21"),
            finding("CVE-2022-23539", "jsonwebtoken", "8.5.1", "P3", 48.8, "9.0.0"),
            finding("GHSA-none-none-none", "jsonwebtoken", "8.5.1", "P3", 30.0, None),
        ],
    }


class ActionTests(unittest.TestCase):
    def test_fix_plan_groups_findings_per_package(self):
        result = apply_actions(sample_result(), owner="web-team")
        plan = result["fix_plan"]
        self.assertEqual([p["component"] for p in plan], ["log4j-core", "lodash", "jsonwebtoken"])
        log4j = plan[0]
        self.assertEqual(log4j["upgrade_to"], "2.17.1", "highest fix clears every finding on the package")
        self.assertEqual(log4j["clears_count"], 2)
        self.assertEqual(log4j["highest_priority"], "P0")
        self.assertEqual(log4j["known_exploited"], ["CVE-2021-44228"])
        jwt = plan[2]
        self.assertTrue(jwt["major_upgrade"])
        self.assertEqual(jwt["unresolved"], ["GHSA-none-none-none"])
        self.assertTrue(any("no published fix" in n for n in jwt["notes"]))

    def test_deadlines_and_owner_follow_sla(self):
        result = apply_actions(sample_result(), owner="web-team", sla_days={"P0": 1})
        p0 = result["findings"][0]["remediation"]
        self.assertEqual(p0["due_by"], "2026-10-06")
        self.assertEqual(p0["owner"], "web-team")
        self.assertEqual(result["findings"][2]["remediation"]["due_by"], "2026-11-04")  # default P2 = 30 days
        self.assertEqual(result["fix_plan"][0]["due_by"], "2026-10-06", "plan item takes its earliest deadline")
        self.assertEqual(result["summary"]["next_due"], "2026-10-06")
        self.assertEqual(result["findings"][1]["remediation"]["plan_step"], 1)

    def test_summary_counts(self):
        summary = apply_actions(sample_result())["summary"]
        self.assertEqual(summary["actions"], 3)
        self.assertEqual(summary["by_priority"]["P3"], 2)
        self.assertEqual(summary["known_exploited"], 1)
        self.assertEqual(summary["fixable"], 4)
        self.assertEqual(summary["no_fix_available"], 1)

    def test_baseline_marks_new_and_resolved(self):
        previous = apply_actions(sample_result())
        current = sample_result()
        current["findings"] = [f for f in current["findings"] if f["component"]["name"] != "log4j-core"]
        current["findings"].append(finding("CVE-2099-0001", "lodash", "4.17.20", "P1", 75.0, "4.17.22"))
        apply_actions(current)
        compare_baseline(current, previous)
        self.assertEqual(current["baseline"]["resolved_count"], 2)
        self.assertEqual(current["baseline"]["new_count"], 1)
        self.assertEqual(current["summary"]["resolved"], 2)
        statuses = {f["id"]: f["status"] for f in current["findings"]}
        self.assertEqual(statuses["CVE-2099-0001"], "new")
        self.assertEqual(statuses["CVE-2021-23337"], "existing")

    def test_gate(self):
        result = apply_actions(sample_result())
        self.assertTrue(evaluate_gate(copy.deepcopy(result), "P1")["breached"])
        self.assertEqual(evaluate_gate(copy.deepcopy(result), "P1")["count"], 2)
        self.assertFalse(evaluate_gate(copy.deepcopy(result), None)["breached"])
        compare_baseline(result, copy.deepcopy(result))
        self.assertFalse(evaluate_gate(result, "P0", new_only=True)["breached"], "nothing is new")

    def test_output_matches_schema(self):
        from jsonschema import Draft202012Validator

        schema = json.loads((ROOT / "schemas/vulnerability-intelligence.schema.json").read_text())
        result = apply_actions(sample_result(), owner="web-team")
        compare_baseline(result, copy.deepcopy(result))
        evaluate_gate(result, "P1")
        errors = [e.message for e in Draft202012Validator(schema).iter_errors(result)]
        self.assertEqual(errors, [])

    def test_major_upgrade_rules(self):
        self.assertTrue(is_major_upgrade("8.5.1", "9.0.0"))
        self.assertTrue(is_major_upgrade("0.21.1", "0.33.0"))
        self.assertFalse(is_major_upgrade("2.14.1", "2.17.1"))
        self.assertFalse(is_major_upgrade("4.17.20", "4.17.21"))

    def test_markdown_leads_with_summary_and_plan(self):
        result = apply_actions(sample_result(), owner="web-team")
        result["context"] = {"asset_id": "shop", "environment": "production", "internet_exposed": True, "asset_criticality": "high", "owner": "web-team"}
        evaluate_gate(result, "P0")
        md = markdown_report(result)
        self.assertLess(md.index("## Summary"), md.index("## Fix plan"))
        self.assertLess(md.index("## Fix plan"), md.index("## Findings that need attention"))
        self.assertIn("Upgrade log4j-core from 2.14.1 to 2.17.1 or later", md)
        self.assertIn("fix plan step 1 — upgrade to `2.17.1` (this issue alone is fixed from `2.15.0`)", md)
        self.assertIn("**FAILED**", md)
        self.assertIn("## Other findings", md)  # P3s collapse into a table

    def test_sarif_shape(self):
        sarif = sarif_report(apply_actions(sample_result()), artifact_uri="package-lock.json")
        run = sarif["runs"][0]
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertEqual(len(run["results"]), 5)
        self.assertEqual(len(run["tool"]["driver"]["rules"]), 5)
        first = run["results"][0]
        self.assertEqual(first["level"], "error")
        self.assertEqual(first["locations"][0]["physicalLocation"]["artifactLocation"]["uri"], "package-lock.json")
        self.assertEqual(run["tool"]["driver"]["rules"][0]["properties"]["security-severity"], "10.0")
        self.assertIn("Upgrade to 2.15.0", first["message"]["text"])

    def test_cli_gate_exit_code_and_outputs(self):
        # Drives scripts/vuln_intel.py end to end with stubbed network sources.
        script = f"""
import json, sys
sys.path.insert(0, {str(ROOT)!r})
sys.argv = ["vuln_intel.py", "scan", sys.argv[1], "--context", sys.argv[2], "--format", "markdown",
            "--json-out", sys.argv[3], "--sarif-out", sys.argv[4], "--fail-on", "P1"]
import scripts.vuln_intel as cli
from tests.test_vulnerability_intelligence import StubOSV, StubEPSS, StubKEV, StubGitHub, StubNVD
from aegissec_vuln.engine import VulnerabilityIntelligenceEngine
real = cli.build_engine
cli.build_engine = lambda path: VulnerabilityIntelligenceEngine(osv=StubOSV(), epss=StubEPSS(), kev=StubKEV(), github=StubGitHub(), nvd=StubNVD(), risk=real(path).risk)
raise SystemExit(cli.main())
"""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "sbom.json").write_text(json.dumps({"components": [{"name": "demo", "version": "1.0.0", "ecosystem": "npm"}]}))
            (tmp / "ctx.yaml").write_text("asset:\n  asset_id: shop\n  environment: production\n  internet_exposed: true\n  reachable: true\n  asset_criticality: high\n  owner: web-team\n")
            proc = subprocess.run(
                [sys.executable, "-c", script, str(tmp / "sbom.json"), str(tmp / "ctx.yaml"), str(tmp / "out.json"), str(tmp / "out.sarif")],
                capture_output=True, text=True, cwd=ROOT,
            )
            self.assertEqual(proc.returncode, 3, proc.stderr)
            self.assertIn("## Fix plan", proc.stdout)
            data = json.loads((tmp / "out.json").read_text())
            self.assertTrue(data["gate"]["breached"])
            self.assertEqual(data["fix_plan"][0]["owner"], "web-team")
            self.assertEqual(json.loads((tmp / "out.sarif").read_text())["version"], "2.1.0")


if __name__ == "__main__":
    unittest.main()
