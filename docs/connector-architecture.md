# Connector Architecture

The vulnerability-intelligence layer uses small isolated connectors so data sources can evolve without replacing the risk engine.

```text
aegissec_vuln/
├── connectors/
│   ├── osv.py
│   ├── github_advisory.py
│   ├── nvd.py
│   ├── cisa_kev.py
│   └── epss.py
├── engine.py
├── http.py
├── models.py
├── normalize.py
├── risk.py
├── sbom.py
└── report.py
```

Connector responsibilities are intentionally narrow:

- fetch source data
- preserve provenance
- fail clearly
- never decide production actions

The engine performs correlation/deduplication. The risk engine performs prioritisation. AegisSec policy controls execution.
