import copy
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aegissec_cli", ROOT / "scripts/aegissec.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)

NOW = datetime(2026, 10, 5, 12, 0, tzinfo=timezone.utc)

VALID = {
    "engagement": {
        "id": "ENG-2026-001",
        "owner": "Spark Pixel Ltd",
        "requester": "Security lead",
        "authority_confirmed": True,
        "start": "2026-10-05T09:00:00+01:00",
        "end": "2026-10-05T17:00:00+01:00",
    },
    "scope": {
        "targets": [{"type": "web", "value": "https://staging.client-site.test"}],
        "permitted_testing": ["safe configuration checks"],
        "prohibited_actions": ["denial of service"],
    },
    "controls": {"emergency_stop_contact": "+44 20 7946 0000 (on-call)", "stop_conditions": ["service instability"]},
    "data_handling": {"classification": "Confidential", "evidence_store": "Encrypted project share"},
}


def run(data, now=NOW):
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as fh:
        yaml.safe_dump(data, fh)
    out = io.StringIO()
    with redirect_stdout(out):
        code = cli.check_scope(fh.name, now=now)
    Path(fh.name).unlink()
    return code, out.getvalue()


class ScopeGateTests(unittest.TestCase):
    def test_complete_scope_passes(self):
        code, out = run(VALID)
        self.assertEqual(code, 0, out)

    def test_template_is_rejected(self):
        template = yaml.safe_load((ROOT / "templates/engagement-scope.yaml").read_text())
        code, out = run(template)
        self.assertEqual(code, 2)
        for expected in ("authority_confirmed", "placeholder", "emergency_stop_contact", "owner"):
            self.assertIn(expected, out)

    def test_window_is_enforced(self):
        self.assertIn("has ended", run(VALID, now=datetime(2026, 10, 6, tzinfo=timezone.utc))[1])
        self.assertIn("has not started", run(VALID, now=datetime(2026, 10, 4, tzinfo=timezone.utc))[1])
        bad = copy.deepcopy(VALID)
        bad["engagement"]["end"] = "2026-10-05T08:00:00+01:00"
        self.assertIn("must be after", run(bad)[1])

    def test_each_requirement_is_checked(self):
        cases = {
            ("engagement", "owner"): "owner",
            ("scope", "targets"): "explicit target",
            ("scope", "permitted_testing"): "permitted_testing",
            ("scope", "prohibited_actions"): "prohibited_actions",
            ("data_handling", "evidence_store"): "data_handling",
            ("controls", "emergency_stop_contact"): "emergency_stop_contact",
            ("controls", "stop_conditions"): "stop_conditions",
            ("engagement", "authority_confirmed"): "authority_confirmed",
        }
        for (section, key), message in cases.items():
            data = copy.deepcopy(VALID)
            data[section].pop(key)
            code, out = run(data)
            self.assertEqual(code, 2, f"missing {section}.{key} should fail")
            self.assertIn(message, out)


if __name__ == "__main__":
    unittest.main()
