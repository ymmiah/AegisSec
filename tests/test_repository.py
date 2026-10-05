import json
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

class RepositoryTests(unittest.TestCase):
    def test_skill_index_is_consistent(self):
        idx = yaml.safe_load((ROOT / "skills/index.yaml").read_text())
        skills = idx["skills"]
        ids = [s["id"] for s in skills]
        self.assertEqual(len(ids), len(set(ids)))
        for skill in skills:
            self.assertTrue((ROOT / skill["file"]).is_file(), skill["file"])
            self.assertIn(skill["mode"], {"DEFENSIVE", "ASSESSMENT", "LAB", "PROHIBITED"})
            self.assertIn(skill["risk"], {"low", "medium", "high", "critical"})

    def test_manifest_count_matches_index(self):
        idx = yaml.safe_load((ROOT / "skills/index.yaml").read_text())
        manifest = json.loads((ROOT / "agent/manifest.json").read_text())
        self.assertEqual(manifest["curated_skill_count"], len(idx["skills"]))


    def test_all_in_one_senior_skills(self):
        index = json.loads((ROOT / "skills/skills-index.json").read_text())
        router = json.loads((ROOT / "skills/router.json").read_text())
        self.assertEqual(index["count"], 64)
        self.assertEqual(len(index["skills"]), 64)
        ids = {s["id"] for s in index["skills"]}
        self.assertEqual(len(ids), 64)
        for skill in index["skills"]:
            self.assertTrue((ROOT / skill["path"]).is_file(), skill["path"])
            self.assertTrue(skill["source_refs"])
        self.assertEqual({r["skill"] for r in router["routes"]}, ids)
        self.assertEqual(len(router["routes"]), 64)

    def test_framework_sources_use_https(self):
        data = json.loads((ROOT / "docs/frameworks.lock.json").read_text())
        for framework in data["frameworks"]:
            self.assertTrue(framework["url"].startswith("https://"), framework["name"])

    def test_policy_precedence_files_exist(self):
        for rel in [
            "AGENTS.md", "policy/policy-precedence.md", "policy/runtime-control.md",
            "policy/production-change.md", "policy/evidence-integrity.md",
            "tools/action-risk.yaml", "tools/capability-matrix.yaml"
        ]:
            self.assertTrue((ROOT / rel).is_file(), rel)

if __name__ == "__main__":
    unittest.main()
