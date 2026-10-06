import json
import tempfile
import unittest
from pathlib import Path

import yaml

from aegissec_agent import Harness, StubProvider, Tool
from aegissec_agent import providers as providers_mod
from aegissec_agent.providers import AnthropicProvider, AssistantTurn, OpenAIProvider, ToolCall
from aegissec_agent import personas

ROOT = Path(__file__).resolve().parents[1]


def one_call(tool, inp):
    return [AssistantTurn(tool_calls=[ToolCall("c1", tool, inp)]), AssistantTurn(text="done")]


VALID_SCOPE = {
    "engagement": {"owner": "Acme Ltd", "authority_confirmed": True,
                   "start": "2020-01-01T00:00:00+00:00", "end": "2100-01-01T00:00:00+00:00"},
    "scope": {"targets": [{"type": "web", "value": "https://staging.acme.test"}],
              "permitted_testing": ["safe"], "prohibited_actions": ["dos"]},
    "controls": {"emergency_stop_contact": "+44 20 7946 0000", "stop_conditions": ["instability"]},
    "data_handling": {"classification": "Confidential", "evidence_store": "vault"},
}


class LoopTests(unittest.TestCase):
    def test_tool_loop_runs_and_returns_final_text(self):
        h = Harness(StubProvider(one_call("list_skills", {})), agent="security-appsec-engineer")
        out = h.ask("what can you do")
        self.assertEqual(out, "done")
        roles = [m["role"] for m in h.history]
        self.assertEqual(roles, ["user", "assistant", "tool", "assistant"])
        tool_out = [m for m in h.history if m["role"] == "tool"][0]["output"]
        self.assertIn("aegissec", tool_out)

    def test_system_prompt_has_rules_persona_and_tools(self):
        h = Harness(StubProvider([AssistantTurn(text="hi")]), agent="security-appsec-engineer")
        self.assertIn("AegisSec operating rules", h.system)
        self.assertIn("Application Security Engineer", h.system)
        self.assertIn("scan_dependencies", h.system)
        self.assertIn("used under its MIT licence", h.system)  # community persona attribution

    def test_read_file_is_sandboxed(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.txt").write_text("inside")
            h = Harness(StubProvider(one_call("read_file", {"path": "../../../etc/passwd"})), workdir=tmp)
            h.ask("read it")
            out = [m for m in h.history if m["role"] == "tool"][0]
            self.assertTrue(out["is_error"])
            self.assertIn("outside the working directory", out["output"])

    def test_step_limit_is_enforced(self):
        # Provider always asks for a tool, never finishes.
        forever = [lambda s, m, t: AssistantTurn(tool_calls=[ToolCall("c", "list_skills", {})])] * 50
        h = Harness(StubProvider(forever), max_steps=3)
        out = h.ask("loop")
        self.assertIn("stopped after the step limit", out)
        self.assertEqual(sum(m["role"] == "assistant" for m in h.history), 3)


class PolicyTests(unittest.TestCase):
    def _run(self, tool, **hk):
        ran = []
        t = Tool(tool.name, tool.description, tool.action, tool.input_schema,
                 lambda a: ran.append(a) or "executed")
        h = Harness(StubProvider(one_call(tool.name, {})), extra_tools=[t], **hk)
        h.ask("go")
        result = [m for m in h.history if m["role"] == "tool"][0]
        return result, bool(ran)

    def test_low_risk_runs(self):
        t = Tool("peek", "read", "read_local_artifacts", {"type": "object", "properties": {}}, None)
        result, ran = self._run(t)
        self.assertFalse(result["is_error"])
        self.assertTrue(ran)

    def test_high_risk_denied_without_approval(self):
        t = Tool("rotate", "rotate prod key", "rotate_production_secret_or_key", {"type": "object", "properties": {}}, None)
        result, ran = self._run(t, approval_mode="deny")
        self.assertTrue(result["is_error"])
        self.assertFalse(ran)
        self.assertIn("approval", result["output"].lower())

    def test_approval_prompt_yes_and_no(self):
        t = Tool("deploy", "deploy rule", "deploy_detection_content", {"type": "object", "properties": {}}, None)
        self.assertTrue(self._run(t, approval_mode="prompt", approver=lambda n, s: True)[1])
        self.assertFalse(self._run(t, approval_mode="prompt", approver=lambda n, s: False)[1])

    def test_critical_denied_even_on_auto(self):
        t = Tool("dos", "load test", "load_or_dos_test", {"type": "object", "properties": {}}, None)
        result, ran = self._run(t, approval_mode="auto")
        self.assertTrue(result["is_error"])
        self.assertFalse(ran)

    def test_scope_gated_action(self):
        t = Tool("ascan", "active scan", "active_safe_scan", {"type": "object", "properties": {}}, None)
        self.assertFalse(self._run(t)[1])  # no scope -> refused
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as fh:
            yaml.safe_dump(VALID_SCOPE, fh)
        result, ran = self._run(t, scope_file=fh.name)
        self.assertTrue(ran, result["output"])

    def test_unknown_action_fails_closed(self):
        t = Tool("weird", "???", "not_a_real_action", {"type": "object", "properties": {}}, None)
        result, ran = self._run(t, approval_mode="auto")
        self.assertTrue(result["is_error"])
        self.assertFalse(ran)


class AnthropicWireTests(unittest.TestCase):
    def setUp(self):
        self.captured = {}

        def fake_post(url, headers, body, timeout=120):
            self.captured.update(url=url, headers=headers, body=body)
            return {"content": [{"type": "text", "text": "hi"},
                                {"type": "tool_use", "id": "toolu_1", "name": "list_skills", "input": {}}]}
        providers_mod._post = fake_post

    def test_request_and_parsing(self):
        p = AnthropicProvider(model="claude-opus-5-5", api_key="k")
        skill_tool = Harness(StubProvider([]), agent="aegissec-operator").tools[0]
        messages = [{"role": "user", "text": "hello"},
                    {"role": "assistant", "text": "", "tool_calls": [{"id": "toolu_0", "name": "list_skills", "input": {}}]},
                    {"role": "tool", "id": "toolu_0", "name": "list_skills", "output": "ok", "is_error": False}]
        turn = p.complete("SYS", messages, [skill_tool])
        self.assertEqual(self.captured["url"], "https://api.anthropic.com/v1/messages")
        self.assertEqual(self.captured["headers"]["x-api-key"], "k")
        self.assertEqual(self.captured["headers"]["anthropic-version"], "2023-06-01")
        body = self.captured["body"]
        self.assertEqual(body["system"], "SYS")
        self.assertIn("input_schema", body["tools"][0])
        # assistant tool_use and tool_result round-trip
        self.assertEqual(body["messages"][1]["content"][0]["type"], "tool_use")
        self.assertEqual(body["messages"][2]["content"][0]["type"], "tool_result")
        self.assertEqual(body["messages"][2]["content"][0]["tool_use_id"], "toolu_0")
        # parsed response
        self.assertEqual(turn.text, "hi")
        self.assertEqual(turn.tool_calls[0].name, "list_skills")


class OpenAIWireTests(unittest.TestCase):
    def setUp(self):
        self.captured = {}

        def fake_post(url, headers, body, timeout=120):
            self.captured.update(url=url, headers=headers, body=body)
            return {"choices": [{"message": {"content": "answer",
                    "tool_calls": [{"id": "call_1", "type": "function",
                                    "function": {"name": "enrich_vulnerability", "arguments": '{"id": "CVE-2021-44228"}'}}]}}]}
        providers_mod._post = fake_post

    def test_request_and_parsing(self):
        p = OpenAIProvider(model="gpt-4o", api_key="k", base_url="https://api.openai.com/v1")
        tool = Harness(StubProvider([]), agent="aegissec-operator").tools[0]
        messages = [{"role": "user", "text": "hello"},
                    {"role": "assistant", "text": "", "tool_calls": [{"id": "call_0", "name": "list_skills", "input": {"x": 1}}]},
                    {"role": "tool", "id": "call_0", "name": "list_skills", "output": "ok"}]
        turn = p.complete("SYS", messages, [tool])
        self.assertTrue(self.captured["url"].endswith("/chat/completions"))
        self.assertEqual(self.captured["headers"]["authorization"], "Bearer k")
        body = self.captured["body"]
        self.assertEqual(body["messages"][0], {"role": "system", "content": "SYS"})
        self.assertEqual(body["messages"][1], {"role": "user", "content": "hello"})
        self.assertEqual(body["tools"][0]["type"], "function")
        self.assertIn("parameters", body["tools"][0]["function"])
        # assistant tool_calls arguments is a JSON string; tool role carries result
        self.assertEqual(json.loads(body["messages"][2]["tool_calls"][0]["function"]["arguments"]), {"x": 1})
        self.assertEqual(body["messages"][3]["role"], "tool")
        self.assertEqual(turn.text, "answer")
        self.assertEqual(turn.tool_calls[0].input, {"id": "CVE-2021-44228"})

    def tearDown(self):
        import importlib
        importlib.reload(providers_mod)


class PersonaTests(unittest.TestCase):
    def test_index_matches_files_and_all_load(self):
        entries = personas.load_index()
        self.assertEqual(len(entries), 18)
        for e in entries:
            self.assertTrue((ROOT / e["file"]).exists(), e["file"])
            persona = personas.get_persona(e["slug"])
            self.assertTrue(persona.body)
            self.assertTrue(persona.description)


if __name__ == "__main__":
    unittest.main()
