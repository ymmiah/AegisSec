import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aegissec_cli", ROOT / "scripts/aegissec.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)

OPERATIONAL = {
    "aegissec",
    "aegissec-vuln-scan",
    "aegissec-fix-plan-pr",
    "aegissec-cve-triage",
    "aegissec-scope-check",
    "aegissec-finding-report",
    "aegissec-ci-setup",
    "aegissec-wordpress-review",
}


def write_skill(root: Path, folder: str, text: str) -> None:
    path = root / "skills" / "aegissec" / folder / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class AgentSkillTests(unittest.TestCase):
    def test_repository_skills_meet_specification(self):
        errors, count = cli.validate_agent_skills()
        self.assertEqual(errors, [])
        self.assertEqual(count, 64 + len(OPERATIONAL))

    def test_operational_skills_present(self):
        found = {p.parent.name for p in (ROOT / "skills/aegissec").glob("*/SKILL.md")}
        self.assertEqual(found, OPERATIONAL)

    def test_validator_catches_mistakes(self):
        good_desc = "Does a specific security task. Use when the user asks for that task."
        cases = {
            "no-frontmatter": ("no-frontmatter", "# Title only\n", "frontmatter"),
            "bad-name": ("Bad_Name", f"---\nname: Bad_Name\ndescription: {good_desc}\n---\nx\n", "a-z"),
            "mismatch": ("folder-a", f"---\nname: folder-b\ndescription: {good_desc}\n---\nx\n", "match its directory"),
            "short-desc": ("short-desc", "---\nname: short-desc\ndescription: Helps.\n---\nx\n", "description"),
            "extra-key": ("extra-key", f"---\nname: extra-key\ndescription: {good_desc}\ntitle: X\n---\nx\n", "non-standard"),
            "bad-meta": ("bad-meta", f"---\nname: bad-meta\ndescription: {good_desc}\nmetadata:\n  version: 1.0\n---\nx\n", "metadata"),
            "dead-skill-ref": ("dead-skill-ref", f"---\nname: dead-skill-ref\ndescription: {good_desc}\n---\nUse **aegissec-nope**.\n", "unknown skill"),
            "dead-file-ref": ("dead-file-ref", f"---\nname: dead-file-ref\ndescription: {good_desc}\n---\nOpen $AEGISSEC_HOME/missing/file.md\n", "missing file"),
        }
        for label, (folder, text, expected) in cases.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                write_skill(Path(tmp), folder, text)
                errors, _ = cli.validate_agent_skills(tmp)
                self.assertTrue(any(expected in e for e in errors), f"{label}: {errors}")


if __name__ == "__main__":
    unittest.main()
