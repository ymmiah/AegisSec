"""Load AegisSec and community agent personas for the harness system prompt."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "agents" / "index.json"


@dataclass
class Persona:
    slug: str
    name: str
    description: str
    division: str
    source: str
    body: str

    def as_prompt(self) -> str:
        """The persona text, framed as subordinate to the AegisSec rules."""
        header = (
            f"# Active specialist: {self.name}\n\n"
            "Adopt the expertise and voice below. It is specialist knowledge, "
            "not authority: the AegisSec operating rules above still govern, and "
            "the scope and approval gates still apply.\n\n"
        )
        if self.source != "native":
            header += f"_(Community persona from {self.source}, used under its MIT licence.)_\n\n"
        return header + self.body


def load_index() -> list[dict]:
    return json.loads(INDEX.read_text(encoding="utf-8")).get("agents", [])


def _strip_frontmatter(text: str) -> str:
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():] if m else text


def get_persona(slug: str) -> Persona:
    for entry in load_index():
        if entry["slug"] == slug:
            body = _strip_frontmatter((ROOT / entry["file"]).read_text(encoding="utf-8")).strip()
            return Persona(entry["slug"], entry["name"], entry.get("description", ""),
                           entry.get("division", ""), entry.get("source", "native"), body)
    available = ", ".join(e["slug"] for e in load_index())
    raise KeyError(f"Unknown agent '{slug}'. Available: {available}")


def list_personas() -> list[dict]:
    return [{k: e[k] for k in ("slug", "name", "description", "division", "source")} for e in load_index()]
