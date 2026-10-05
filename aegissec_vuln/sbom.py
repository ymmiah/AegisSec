from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Component


_PURL_ECOSYSTEM = {
    "npm": "npm",
    "pypi": "PyPI",
    "maven": "Maven",
    "golang": "Go",
    "cargo": "crates.io",
    "nuget": "NuGet",
    "gem": "RubyGems",
    "composer": "Packagist",
    "hex": "Hex",
    "pub": "Pub",
    "swift": "SwiftURL",
}


def ecosystem_from_purl(purl: str | None) -> str | None:
    if not purl or not purl.startswith("pkg:"):
        return None
    kind = purl[4:].split("/", 1)[0].lower()
    return _PURL_ECOSYSTEM.get(kind)


def _component(name: str, version: str, *, purl: str | None = None, path: str | None = None, metadata=None) -> Component:
    return Component(
        name=name,
        version=version,
        purl=purl,
        ecosystem=ecosystem_from_purl(purl),
        path=path,
        metadata=metadata or {},
    )


def parse_cyclonedx(data: dict[str, Any]) -> list[Component]:
    components: list[Component] = []
    for item in data.get("components", []) or []:
        name = item.get("name")
        version = item.get("version")
        if not name or not version:
            continue
        components.append(_component(str(name), str(version), purl=item.get("purl"), metadata={"type": item.get("type"), "bom_ref": item.get("bom-ref")}))
    return components


def parse_spdx(data: dict[str, Any]) -> list[Component]:
    components: list[Component] = []
    for package in data.get("packages", []) or []:
        name = package.get("name")
        version = package.get("versionInfo")
        if not name or not version:
            continue
        purl = None
        for ref in package.get("externalRefs", []) or []:
            if str(ref.get("referenceType", "")).lower().endswith("purl"):
                purl = ref.get("referenceLocator")
                break
        components.append(_component(str(name), str(version), purl=purl, metadata={"spdx_id": package.get("SPDXID")}))
    return components


def parse_generic(data: Any) -> list[Component]:
    items = data.get("components", []) if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise ValueError("Generic component input must be a list or an object with components[]")
    result: list[Component] = []
    for item in items:
        if not isinstance(item, dict) or not item.get("name") or not item.get("version"):
            continue
        result.append(
            Component(
                name=str(item["name"]),
                version=str(item["version"]),
                ecosystem=item.get("ecosystem"),
                purl=item.get("purl"),
                path=item.get("path"),
                direct=item.get("direct"),
                metadata=item.get("metadata") or {},
            )
        )
    return result


def load_components(path: str | Path) -> list[Component]:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("bomFormat") == "CycloneDX":
        return parse_cyclonedx(data)
    if "spdxVersion" in data:
        return parse_spdx(data)
    return parse_generic(data)
