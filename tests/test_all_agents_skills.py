"""Smoke test: every agent loads and drives the governed loop, every skill
loads, and every harness tool runs. Offline-safe — network tools (scan,
enrich) only need to return a string, not reach the internet."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from aegissec_agent import Harness, StubProvider
from aegissec_agent import personas
from aegissec_agent.providers import AssistantTurn, ToolCall
from aegissec_agent.tools import ToolContext, build_tools

ROOT = Path(__file__).resolve().parents[1]


class EveryAgentTests(unittest.TestCase):
    def test_every_persona_loads_and_runs_the_loop(self):
        rows = personas.list_personas()
        self.assertGreaterEqual(len(rows), 18)
        for e in rows:
            with self.subTest(agent=e["slug"]):
                h = Harness(StubProvider([
                    AssistantTurn(tool_calls=[ToolCall("1", "list_skills", {})]),
                    AssistantTurn(text="done"),
                ]), agent=e["slug"])
                self.assertIn("AegisSec operating rules", h.system)
                self.assertIn(e["name"], h.system)
                self.assertIn("scan_dependencies", h.system)
                self.assertEqual(h.ask("what can you do"), "done")
                self.assertTrue(any(m["role"] == "tool" and not m["is_error"] for m in h.history))


class EverySkillTests(unittest.TestCase):
    def setUp(self):
        self.read_skill = {t.name: t for t in build_tools(ToolContext(workdir=ROOT))}["read_skill"].handler

    def test_operational_skills_load(self):
        names = [p.parent.name for p in (ROOT / "skills/aegissec").glob("*/SKILL.md")]
        self.assertEqual(len(names), 8)
        for name in names:
            with self.subTest(skill=name):
                content = self.read_skill({"name": name})
                self.assertFalse(content.startswith("No skill named"))
                self.assertGreater(len(content), 200)

    def test_native_security_skills_load(self):
        skills = yaml.safe_load((ROOT / "skills/index.yaml").read_text())["skills"]
        self.assertEqual(len(skills), 115)
        for s in skills:
            with self.subTest(skill=s["id"]):
                content = self.read_skill({"name": s["id"]})
                self.assertFalse(content.startswith("No skill named"))
                self.assertGreater(len(content), 100)

    def test_senior_skills_parse_with_description(self):
        files = list((ROOT / "skills/senior").glob("*/SKILL.md"))
        self.assertEqual(len(files), 64)
        for f in files:
            with self.subTest(skill=f.parent.name):
                fm = yaml.safe_load(f.read_text().split("---")[1])
                self.assertTrue(fm.get("name"))
                self.assertTrue(fm.get("description"))


class EveryToolTests(unittest.TestCase):
    def test_all_tools_execute(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "sample.py").write_text("print('hi')\n")
            scope = {"engagement": {"owner": "Acme", "authority_confirmed": True,
                     "start": "2020-01-01T00:00:00+00:00", "end": "2100-01-01T00:00:00+00:00"},
                     "scope": {"targets": [{"type": "web", "value": "https://staging.acme.test"}],
                               "permitted_testing": ["safe"], "prohibited_actions": ["dos"]},
                     "controls": {"emergency_stop_contact": "+44 20 7946 0000", "stop_conditions": ["x"]},
                     "data_handling": {"classification": "Confidential", "evidence_store": "vault"}}
            (Path(tmp) / "scope.yaml").write_text(yaml.safe_dump(scope))
            T = {t.name: t for t in build_tools(ToolContext(workdir=Path(tmp)))}
            cases = {
                "list_skills": {}, "read_skill": {"name": "aegissec-vuln-scan"},
                "list_files": {"glob": "**/*.py"}, "read_file": {"path": "sample.py"},
                "check_scope": {"path": "scope.yaml"},
                "scan_dependencies": {"name": "lodash", "version": "4.17.20", "ecosystem": "npm"},
                "enrich_vulnerability": {"id": "CVE-2021-44228"},
            }
            self.assertEqual(set(cases), {t.name for t in T.values()})
            # Keep the smoke test hermetic and fast: make the two network tools
            # fail immediately instead of waiting on real timeouts. They must
            # still return a graceful string, which is what "working" means here.
            def no_network(*a, **k):
                from aegissec_vuln.http import HttpError
                raise HttpError("offline (smoke test)")
            with mock.patch("aegissec_vuln.http.JsonHttpClient.request_json", side_effect=no_network):
                for name, args in cases.items():
                    with self.subTest(tool=name):
                        out = T[name].handler(args)
                        self.assertIsInstance(out, str)
                        self.assertTrue(out)
            self.assertIn("PASSED", T["check_scope"].handler({"path": "scope.yaml"}))
            with self.assertRaises(ValueError):
                T["read_file"].handler({"path": "../../../etc/passwd"})


if __name__ == "__main__":
    unittest.main()
