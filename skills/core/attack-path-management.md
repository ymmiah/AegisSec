# Attack Path Management

**Skill ID:** `attack-path-management`  
**Domain:** `core`  
**Default mode:** `DEFENSIVE`  
**Operational risk:** `medium`  
**Frameworks:** MITRE-ATT&CK, MITRE-D3FEND, NIST-CSF

Model how combinations of identity, network, cloud and application weaknesses could produce meaningful compromise.

## Outcomes
- Identify high-value attack paths without needing to exploit them.
- Rank control points that break the greatest number of paths.

## Method
1. Identify crown-jewel assets and privileged identities.
2. Map identity, network, trust, service, cloud and deployment relationships.
3. Add verified exposures and misconfigurations as graph edges.
4. Calculate plausible paths from reachable entry points to critical assets.
5. Validate assumptions using passive evidence and safe configuration review first.
6. Recommend choke-point controls and verify path removal.

## Guardrails
Do not turn path modelling into unscope-controlled exploitation. Real active validation remains an ASSESSMENT and requires scope.

## Output
Return: `entry → intermediate trust edges → target → confidence → control gaps → break points`.
