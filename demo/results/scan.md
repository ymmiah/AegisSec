$ python scripts/vuln_intel.py scan demo/shop-sbom.json --context demo/shop-context.yaml --format markdown
# AegisSec Vulnerability Intelligence Report

Generated: `2026-10-05T12:08:24.793275+00:00`  
Components assessed: **5**  
Findings: **37**

## Findings

### CVE-2021-44228 — org.apache.logging.log4j:log4j-core 2.14.1

- Priority: **P0**
- Context score: **92.5 / 100**
- Confidence: **high**
- CVSS: `10.0`
- EPSS: `0.99999`
- CISA KEV: `True`
- Fixed version(s): `2.15.0, 2.3.1, 2.12.2, 1.9.2, 1.10.8, 1.11.10, 2.0.11`
- Recommended upgrade: `2.15.0`

Remote code injection in Log4j

Why prioritised:
- CISA KEV: known exploited vulnerability
- High EPSS probability (100.0%)
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2021-45046 — org.apache.logging.log4j:log4j-core 2.14.1

- Priority: **P0**
- Context score: **92.1 / 100**
- Confidence: **high**
- CVSS: `9.8`
- EPSS: `0.99977`
- CISA KEV: `True`
- Fixed version(s): `2.16.0, 2.12.2, 1.9.2, 1.10.8, 1.11.11, 2.0.12, 2.3.1`
- Recommended upgrade: `2.16.0`

Incomplete fix for Apache Log4j vulnerability

Why prioritised:
- CISA KEV: known exploited vulnerability
- High EPSS probability (100.0%)
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2021-45105 — org.apache.logging.log4j:log4j-core 2.14.1

- Priority: **P1**
- Context score: **70.0 / 100**
- Confidence: **high**
- CVSS: `8.6`
- EPSS: `0.99999`
- CISA KEV: `False`
- Fixed version(s): `2.12.3, 2.17.0, 2.3.1, 1.9.2, 1.10.9, 1.11.12, 2.0.13`
- Recommended upgrade: `2.17.0`

Apache Log4j2 vulnerable to Improper Input Validation and Uncontrolled Recursion

Why prioritised:
- High EPSS probability (100.0%)
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2021-44832 — org.apache.logging.log4j:log4j-core 2.14.1

- Priority: **P1**
- Context score: **70.0 / 100**
- Confidence: **high**
- CVSS: `6.6`
- EPSS: `0.97906`
- CISA KEV: `False`
- Fixed version(s): `2.3.2, 2.12.4, 2.17.1, 1.9.2, 1.10.9, 1.11.13, 2.0.14`
- Recommended upgrade: `2.17.1`

Improper Input Validation and Injection in Apache Log4j2

Why prioritised:
- High EPSS probability (97.9%)
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2021-23337 — lodash 4.17.20

- Priority: **P2**
- Context score: **53.0 / 100**
- Confidence: **high**
- CVSS: `8.1`
- EPSS: `0.21333`
- CISA KEV: `False`
- Fixed version(s): `4.17.21, 4.18.0`
- Recommended upgrade: `4.17.21`

Command Injection in lodash

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2021-3749 — axios 0.21.1

- Priority: **P2**
- Context score: **50.2 / 100**
- Confidence: **high**
- CVSS: `8.0`
- EPSS: `0.08515`
- CISA KEV: `False`
- Fixed version(s): `0.21.2`
- Recommended upgrade: `0.21.2`

axios Inefficient Regular Expression Complexity vulnerability

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-44492 — axios 0.21.1

- Priority: **P3**
- Context score: **49.9 / 100**
- Confidence: **high**
- CVSS: `8.6`
- EPSS: `0.00783`
- CISA KEV: `False`
- Fixed version(s): `1.16.0, 0.32.0`
- Recommended upgrade: `0.32.0`

axios's shouldBypassProxy does not recognize IPv4-mapped IPv6 addresses, allowing NO_PROXY bypass (incomplete fix for CVE-2025-62718)

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-44487 — axios 0.21.1

- Priority: **P3**
- Context score: **49.1 / 100**
- Confidence: **high**
- CVSS: `8.2`
- EPSS: `0.0076`
- CISA KEV: `False`
- Fixed version(s): `1.16.0, 0.32.0`
- Recommended upgrade: `0.32.0`

Axios: Proxy-Authorization Credential Leak to Origin Server Across HTTP-to-HTTPS Redirect in Axios Node.js HTTP Adapter

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-25639 — axios 0.21.1

- Priority: **P3**
- Context score: **48.9 / 100**
- Confidence: **high**
- CVSS: `8.0`
- EPSS: `0.01804`
- CISA KEV: `False`
- Fixed version(s): `1.13.5, 0.30.3`
- Recommended upgrade: `0.30.3`

Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2022-23539 — jsonwebtoken 8.5.1

- Priority: **P3**
- Context score: **48.8 / 100**
- Confidence: **high**
- CVSS: `8.1`
- EPSS: `0.00501`
- CISA KEV: `False`
- Fixed version(s): `9.0.0`
- Recommended upgrade: `9.0.0`

jsonwebtoken unrestricted key type could lead to legacy keys usage

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-44496 — axios 0.21.1

- Priority: **P3**
- Context score: **48.7 / 100**
- Confidence: **high**
- CVSS: `8.0`
- EPSS: `0.00966`
- CISA KEV: `False`
- Fixed version(s): `1.16.0, 0.32.0`
- Recommended upgrade: `0.32.0`

Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-44495 — axios 0.21.1

- Priority: **P3**
- Context score: **48.7 / 100**
- Confidence: **high**
- CVSS: `8.0`
- EPSS: `0.01041`
- CISA KEV: `False`
- Fixed version(s): `1.15.2, 0.31.1`
- Recommended upgrade: `0.31.1`

axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-44486 — axios 0.21.1

- Priority: **P3**
- Context score: **48.7 / 100**
- Confidence: **high**
- CVSS: `8.0`
- EPSS: `0.0076`
- CISA KEV: `False`
- Fixed version(s): `1.16.0, 0.32.0`
- Recommended upgrade: `0.32.0`

Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42033 — axios 0.21.1

- Priority: **P3**
- Context score: **48.7 / 100**
- Confidence: **high**
- CVSS: `8.0`
- EPSS: `0.00924`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios: Prototype Pollution Gadgets - Response Tampering, Data Exfiltration, and Request Hijacking

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2025-27152 — axios 0.21.1

- Priority: **P3**
- Context score: **48.7 / 100**
- Confidence: **high**
- CVSS: `8.0`
- EPSS: `0.00792`
- CISA KEV: `False`
- Fixed version(s): `1.8.2, 0.30.0`
- Recommended upgrade: `0.30.0`

axios Requests Vulnerable To Possible SSRF and Credential Leakage via Absolute URL

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42043 — axios 0.21.1

- Priority: **P3**
- Context score: **48.6 / 100**
- Confidence: **high**
- CVSS: `8.0`
- EPSS: `0.00579`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios: Incomplete Fix for CVE-2025-62718 — NO_PROXY Protection Bypassed via RFC 1122 Loopback Subnet (127.0.0.0/8) in Axios 1.15.0

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42035 — axios 0.21.1

- Priority: **P3**
- Context score: **48.6 / 100**
- Confidence: **high**
- CVSS: `8.0`
- EPSS: `0.00381`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios: Header Injection via Prototype Pollution

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2025-13465 — lodash 4.17.20

- Priority: **P3**
- Context score: **46.7 / 100**
- Confidence: **high**
- CVSS: `6.9`
- EPSS: `0.0185`
- CISA KEV: `False`
- Fixed version(s): `4.17.23, 4.18.0`
- Recommended upgrade: `4.17.23`

lodash vulnerable to Prototype Pollution via array path bypass in `_.unset` and `_.omit`

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42039 — axios 0.21.1

- Priority: **P3**
- Context score: **46.5 / 100**
- Confidence: **high**
- CVSS: `6.9`
- EPSS: `0.00966`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios: unbounded recursion in toFormData causes DoS via deeply nested request data

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-34480 — org.apache.logging.log4j:log4j-core 2.14.1

- Priority: **P3**
- Context score: **46.5 / 100**
- Confidence: **high**
- CVSS: `6.9`
- EPSS: `0.01187`
- CISA KEV: `False`
- Fixed version(s): `2.25.4`
- Recommended upgrade: `2.25.4`

Apache Log4j Core: Silent log event loss in XmlLayout due to unescaped XML 1.0 forbidden characters

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42038 — axios 0.21.1

- Priority: **P3**
- Context score: **46.2 / 100**
- Confidence: **high**
- CVSS: `6.8`
- EPSS: `0.00381`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios: no_proxy bypass via IP alias allows SSRF

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2023-45857 — axios 0.21.1

- Priority: **P3**
- Context score: **45.6 / 100**
- Confidence: **high**
- CVSS: `6.5`
- EPSS: `0.00556`
- CISA KEV: `False`
- Fixed version(s): `1.6.0, 0.28.0`
- Recommended upgrade: `0.28.0`

Axios Cross-Site Request Forgery Vulnerability

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2022-23540 — jsonwebtoken 8.5.1

- Priority: **P3**
- Context score: **45.4 / 100**
- Confidence: **high**
- CVSS: `6.4`
- EPSS: `0.00546`
- CISA KEV: `False`
- Fixed version(s): `9.0.0`
- Recommended upgrade: `9.0.0`

jsonwebtoken vulnerable to signature validation bypass due to insecure default algorithm in jwt.verify()

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2025-68161 — org.apache.logging.log4j:log4j-core 2.14.1

- Priority: **P3**
- Context score: **45.3 / 100**
- Confidence: **high**
- CVSS: `6.3`
- EPSS: `0.00767`
- CISA KEV: `False`
- Fixed version(s): `2.25.3`
- Recommended upgrade: `2.25.3`

Apache Log4j does not verify the TLS hostname in its Socket Appender

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2025-62718 — axios 0.21.1

- Priority: **P3**
- Context score: **45.3 / 100**
- Confidence: **high**
- CVSS: `6.3`
- EPSS: `0.01186`
- CISA KEV: `False`
- Fixed version(s): `1.15.0, 0.31.0`
- Recommended upgrade: `0.31.0`

Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-67319 — axios 0.21.1

- Priority: **P3**
- Context score: **45.2 / 100**
- Confidence: **high**
- CVSS: `6.3`
- EPSS: `0.00318`
- CISA KEV: `False`
- Fixed version(s): `0.33.0, 1.18.0`
- Recommended upgrade: `0.33.0`

Axios: Nested axios option objects can consume polluted prototype values

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-67316 — axios 0.21.1

- Priority: **P3**
- Context score: **45.2 / 100**
- Confidence: **high**
- CVSS: `6.3`
- EPSS: `0.00424`
- CISA KEV: `False`
- Fixed version(s): `1.18.0, 0.33.0`
- Recommended upgrade: `0.33.0`

Axios: Prototype pollution gadgets can alter axios request construction

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-34477 — org.apache.logging.log4j:log4j-core 2.14.1

- Priority: **P3**
- Context score: **45.2 / 100**
- Confidence: **high**
- CVSS: `6.3`
- EPSS: `0.00502`
- CISA KEV: `False`
- Fixed version(s): `2.25.4`
- Recommended upgrade: `2.25.4`

Apache Log4j Core: `verifyHostName` attribute silently ignored in TLS configuration

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2020-28500 — lodash 4.17.20

- Priority: **P3**
- Context score: **45.0 / 100**
- Confidence: **high**
- CVSS: `5.5`
- EPSS: `0.07336`
- CISA KEV: `False`
- Fixed version(s): `4.17.21`
- Recommended upgrade: `4.17.21`

Regular Expression Denial of Service (ReDoS) in lodash

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-40175 — axios 0.21.1

- Priority: **P3**
- Context score: **43.8 / 100**
- Confidence: **high**
- CVSS: `5.5`
- EPSS: `0.01307`
- CISA KEV: `False`
- Fixed version(s): `1.15.0, 0.31.0`
- Recommended upgrade: `0.31.0`

Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42041 — axios 0.21.1

- Priority: **P3**
- Context score: **43.7 / 100**
- Confidence: **high**
- CVSS: `5.5`
- EPSS: `0.0081`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios: Authentication Bypass via Prototype Pollution Gadget in `validateStatus` Merge Strategy

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2022-23541 — jsonwebtoken 8.5.1

- Priority: **P3**
- Context score: **43.7 / 100**
- Confidence: **high**
- CVSS: `5.5`
- EPSS: `0.00774`
- CISA KEV: `False`
- Fixed version(s): `9.0.0`
- Recommended upgrade: `9.0.0`

jsonwebtoken's insecure implementation of key retrieval function could lead to Forgeable Public/Private Tokens from RSA to HMAC

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-44490 — axios 0.21.1

- Priority: **P3**
- Context score: **43.6 / 100**
- Confidence: **high**
- CVSS: `5.5`
- EPSS: `0.00403`
- CISA KEV: `False`
- Fixed version(s): `1.16.0, 0.32.0`
- Recommended upgrade: `0.32.0`

axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42042 — axios 0.21.1

- Priority: **P3**
- Context score: **43.6 / 100**
- Confidence: **high**
- CVSS: `5.5`
- EPSS: `0.00324`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios: XSRF Token Cross-Origin Leakage via Prototype Pollution Gadget in `withXSRFToken` Boolean Coercion

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42036 — axios 0.21.1

- Priority: **P3**
- Context score: **43.6 / 100**
- Confidence: **high**
- CVSS: `5.5`
- EPSS: `0.0048`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios: HTTP adapter streamed responses bypass maxContentLength

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42034 — axios 0.21.1

- Priority: **P3**
- Context score: **43.6 / 100**
- Confidence: **high**
- CVSS: `5.5`
- EPSS: `0.0048`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

### CVE-2026-42040 — axios 0.21.1

- Priority: **P3**
- Context score: **40.0 / 100**
- Confidence: **high**
- CVSS: `3.7`
- EPSS: `0.00264`
- CISA KEV: `False`
- Fixed version(s): `1.15.1, 0.31.1`
- Recommended upgrade: `0.31.1`

Axios: Null Byte Injection via Reverse-Encoding in AxiosURLSearchParams

Why prioritised:
- Asset is internet exposed
- Vulnerable component/path is reachable

[exit 0]
