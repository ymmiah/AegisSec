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
        query: dict[str, Any] = {"version": self.version}
        if self.purl:
            query["package"] = {"purl": self.purl}
        elif self.ecosystem:
            query["package"] = {"name": self.name, "ecosystem": self.ecosystem}
        else:
            raise ValueError(f"Component {self.name!r} needs either purl or ecosystem")
        return query

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


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
