from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Component:
    name: str
    version: str
    ecosystem: str | None = None
    purl: str | None = None
    path: str | None = None
    direct: bool | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def osv_query(self) -> dict[str, Any]:
        # OSV rejects a query that sets the version twice (HTTP 400), so only
        # send "version" separately when the purl does not already carry one.
        query: dict[str, Any] = {}
        if self.purl:
            query["package"] = {"purl": self.purl}
            if not _purl_has_version(self.purl) and self.version:
                query["version"] = self.version
        elif self.ecosystem:
            query["version"] = self.version
            query["package"] = {"name": self.name, "ecosystem": self.ecosystem}
        else:
            raise ValueError(f"Component {self.name!r} needs either purl or ecosystem")
        return query

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _purl_has_version(purl: str) -> bool:
    """True when a Package URL already pins a version (pkg:type/ns/name@version)."""
    core = purl.split("#", 1)[0].split("?", 1)[0]
    return "@" in core.rsplit("/", 1)[-1]


@dataclass(frozen=True)
class AssetContext:
    asset_id: str = "unknown"
    environment: str = "unknown"
    asset_criticality: str = "medium"
    internet_exposed: bool = False
    reachable: bool = False
    runtime_loaded: bool = False
    privileged_component: bool = False
    sensitive_data: bool = False
    compensating_controls: list[str] = field(default_factory=list)
    owner: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
