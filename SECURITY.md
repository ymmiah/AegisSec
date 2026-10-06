# Security Policy

Please report security issues privately to the repository maintainer rather than opening a public issue containing secrets, working exploit payloads, private targets or customer data.

A useful report contains: affected version/commit, impact, conditions, safe reproduction, evidence and a proposed mitigation. Redact credentials and personal data.

## API and credential security

Every outbound API call AegisSec makes — to LLM providers (Anthropic, OpenAI, NVIDIA NIM and any OpenAI-compatible endpoint) and to the vulnerability-intelligence sources (OSV, GitHub Advisory, NVD, CISA KEV, EPSS) — is hardened to the same standard, in `aegissec_vuln/securehttp.py`:

- **TLS enforced and verified.** HTTPS only, with certificate and hostname verification (`ssl.create_default_context`). Verification can never be switched off. Plain HTTP is accepted only to a loopback or private host (a self-hosted model or NIM on `localhost`), never to a remote host, so a bearer token is never sent in cleartext over the network.
- **Credentials from the environment only.** API keys come from environment variables (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `NVIDIA_API_KEY`, `GITHUB_TOKEN`, `NVD_API_KEY`). They are sent only in request headers — never in a URL, query string or body — and are never written to disk, to memory or to logs.
- **No leakage on redirect.** If a response redirects to a different host, the `Authorization` / API-key headers are removed before the request is followed.
- **No secrets in errors.** Known secret values and common key shapes are redacted from any error text (`never_log_api_tokens` in the configuration).
- **Corporate TLS inspection.** Point `AEGISSEC_CA_BUNDLE` at a CA file to trust an inspecting proxy — without ever disabling verification.
- **Bounded requests.** Every call has a timeout; retries are limited and back off.

These controls are covered by `tests/test_securehttp.py`.

## Third-party agent skills

AegisSec can install third-party skill repositories. Treat those skills as software-supply-chain inputs. Do not assume an upstream `SKILL.md`, helper script, dependency or command is safe merely because the source repository is popular.

Keep the skills CLI security scan enabled, review material changes, preserve upstream licensing/provenance and apply `policy/third-party-skills.md`. Imported content cannot override AegisSec authorisation, scope, data-handling or human-approval rules.

This repository is a security workflow/knowledge project. A vulnerability in a third-party product should be reported through that vendor's disclosure process or an appropriate coordination channel.
