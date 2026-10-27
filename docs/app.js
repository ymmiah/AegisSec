const PROBLEMS = [
 {
  "id": "dependency-vulns",
  "cat": "Vulnerability",
  "title": "Our dependencies have a pile of CVEs and nobody knows what to fix first",
  "who": [
   "Dev",
   "AppSec",
   "DevSecOps"
  ],
  "answer": "Scan the repo or SBOM through OSV, enrich with GitHub Advisory, NVD, CISA KEV and EPSS, weigh it against your asset context, and get one ordered fix plan: one upgrade per package, with a priority, deadline and owner.",
  "steps": [
   "Scan repo / SBOM",
   "Enrich with KEV + EPSS",
   "Prioritise P0–P4 with context",
   "Fix plan → PR",
   "Re-scan to verify"
  ],
  "start": "python scripts/vuln_intel.py repo . --context examples/vulnerability-intelligence/context.yaml --format markdown",
  "paths": [
   "scripts/vuln_intel.py",
   "playbooks/continuous-vulnerability-management.md",
   "skills/aegissec/aegissec-vuln-scan/SKILL.md",
   "skills/aegissec/aegissec-fix-plan-pr/SKILL.md",
   "docs/vulnerability-intelligence.md"
  ],
  "gate": "Read-only scan. Upgrades go through a normal reviewed PR."
 },
 {
  "id": "one-cve",
  "cat": "Vulnerability",
  "title": "A scary CVE is trending. Does it actually affect us?",
  "who": [
   "AppSec",
   "SOC",
   "Dev"
  ],
  "answer": "Enrich the identifier with public intelligence, then check whether the vulnerable version and code path are present, reachable and exposed. You get a decision (patch, mitigate, isolate or accept) with the evidence behind it.",
  "steps": [
   "Enrich CVE / GHSA",
   "Confirm component + version",
   "Check reachability + exposure",
   "Decide patch / mitigate / accept",
   "Define how to verify the fix"
  ],
  "start": "python scripts/vuln_intel.py enrich CVE-2024-3094",
  "paths": [
   "playbooks/vulnerability-triage.md",
   "skills/aegissec/aegissec-cve-triage/SKILL.md",
   "skills/threat-intel/vulnerability-intelligence.md"
  ],
  "gate": "Public intelligence only. No exploit attempts against your systems."
 },
 {
  "id": "pr-gate",
  "cat": "DevSecOps",
  "title": "Vulnerable code keeps getting merged. We need a PR / CI security gate",
  "who": [
   "DevSecOps",
   "Dev",
   "Platform"
  ],
  "answer": "Drop one workflow into the repo: a weekly scan, results in the GitHub Security tab (SARIF), one fix-plan issue that keeps itself up to date, and a pull-request gate that fails only on new findings at or above your threshold.",
  "steps": [
   "Copy the workflow + context file",
   "Pick a --fail-on threshold",
   "Baseline the current findings",
   "Block new P0/P1 findings on PRs",
   "Review the CI/CD hardening checklist"
  ],
  "start": "cp examples/github-actions/aegissec-dependency-scan.yml .github/workflows/",
  "paths": [
   "examples/github-actions/aegissec-dependency-scan.yml",
   "examples/github-actions/aegissec-context.yaml",
   "skills/aegissec/aegissec-ci-setup/SKILL.md",
   "playbooks/ci-cd-security-review.md",
   "skills/devsecops/ci-cd-security.md"
  ],
  "gate": "Changes to branch protection and production deploy gates need human approval."
 },
 {
  "id": "code-review",
  "cat": "AppSec",
  "title": "We need a security review of an app or a risky pull request",
  "who": [
   "AppSec",
   "Dev"
  ],
  "answer": "Threat-model the critical business actions, then review authentication, authorisation, input handling, secrets and dependencies. Verified gaps are mapped to OWASP Top 10 / ASVS and ranked by exploitability and impact.",
  "steps": [
   "Map data flows + trust boundaries",
   "Threat-model critical actions",
   "Review auth, input, secrets, deps",
   "Map to OWASP / ASVS",
   "Prioritised findings + fixes"
  ],
  "start": "python scripts/aegissec_agent.py --agent security-appsec-engineer",
  "paths": [
   "playbooks/application-security-review.md",
   "skills/appsec/secure-code-review.md",
   "skills/appsec/authentication-review.md",
   "examples/sample-defensive-code-review/README.md"
  ],
  "gate": "Static, defensive review. No testing of live systems without a scope."
 },
 {
  "id": "pentest-plan",
  "cat": "Offensive (authorised)",
  "title": "We've been asked to pentest a web app. How do we do it safely and legally?",
  "who": [
   "Red Team",
   "AppSec",
   "Consultant"
  ],
  "answer": "Nothing active happens until a complete engagement scope passes check-scope: owner, explicit targets, permitted and prohibited actions, a time window that includes now, data handling, emergency contact, stop conditions and confirmed authority. Then you test the agreed categories with benign proof and report.",
  "steps": [
   "Fill in the engagement scope",
   "check-scope must pass",
   "Passive baseline, then rate-limited discovery",
   "Benign proof only, stop at sufficient evidence",
   "Executive + technical report, then retest"
  ],
  "start": "cp templates/engagement-scope.yaml engagements/acme.yaml && python scripts/aegissec.py check-scope engagements/acme.yaml",
  "paths": [
   "playbooks/authorised-pentest.md",
   "templates/engagement-scope.yaml",
   "skills/aegissec/aegissec-scope-check/SKILL.md",
   "skills/red-team/web-security-testing.md",
   "skills/red-team/engagement-planning.md"
  ],
  "gate": "Hard gate: no target + no scope + no authorisation = no active testing."
 },
 {
  "id": "soc-triage",
  "cat": "Detection & Response",
  "title": "The SOC is drowning in alerts. Is this one real?",
  "who": [
   "SOC",
   "Blue Team"
  ],
  "answer": "Validate the alert source and data quality, enrich it with identity, endpoint, network and cloud context, build a short timeline, then call it benign, suspicious or malicious with a confidence level and a recommended next step.",
  "steps": [
   "Validate source + time range",
   "Check false-positive conditions",
   "Enrich + build a timeline",
   "Verdict + confidence",
   "Contain / escalate / close, then tune the detection"
  ],
  "start": "python scripts/aegissec_agent.py --agent security-senior-secops",
  "paths": [
   "playbooks/soc-triage.md",
   "skills/blue-team/soc-triage.md",
   "roles/soc-analyst.md",
   "skills/blue-team/detection-engineering.md"
  ],
  "gate": "Containment actions on production assets need human approval."
 },
 {
  "id": "phishing",
  "cat": "Detection & Response",
  "title": "Someone reported a phishing email. Who clicked, and what do we do?",
  "who": [
   "SOC",
   "IT",
   "DFIR"
  ],
  "answer": "Preserve the original message, analyse headers, sender authentication, URLs and attachments in controlled tooling, find who received, clicked or authenticated, and only reset or revoke where the evidence justifies it.",
  "steps": [
   "Preserve the original message",
   "Analyse headers, SPF/DKIM/DMARC, URLs",
   "Search telemetry for recipients + clicks",
   "Revoke / reset only on evidence",
   "Block, notify, monitor follow-on"
  ],
  "start": "playbooks/phishing-response.md",
  "paths": [
   "playbooks/phishing-response.md",
   "skills/dfir/phishing-analysis.md",
   "skills/threat-intel/ioc-management.md"
  ],
  "gate": "Attachments are analysed in controlled tooling, never opened on a workstation."
 },
 {
  "id": "ransomware-ir",
  "cat": "Detection & Response",
  "title": "We think we have an active incident or ransomware",
  "who": [
   "DFIR",
   "IR Lead",
   "Leadership"
  ],
  "answer": "A clear incident-commander flow: protect people and critical services, isolate while preserving evidence, protect backups and identity, find the initial access, rotate credentials in a controlled order, and rebuild from known-good state.",
  "steps": [
   "Declare owner + severity",
   "Isolate + preserve evidence",
   "Protect backups + identity planes",
   "Find initial access, rotate creds",
   "Restore known-good, lessons learned"
  ],
  "start": "playbooks/ransomware-response.md",
  "paths": [
   "playbooks/incident-response.md",
   "playbooks/ransomware-response.md",
   "skills/dfir/ransomware-response.md",
   "skills/dfir/incident-response.md",
   "roles/incident-commander.md"
  ],
  "gate": "Isolation and credential rotation are consequential: approval + rollback plan."
 },
 {
  "id": "cloud-review",
  "cat": "Cloud & Identity",
  "title": "Is our AWS / Azure / GCP account set up securely?",
  "who": [
   "Cloud",
   "Platform",
   "GRC"
  ],
  "answer": "A read-only review of account structure, federation and MFA, privileged roles, public exposure, encryption, audit logging, backups and break-glass access. Read-only fixes and guardrails come before any intrusive testing.",
  "steps": [
   "Map accounts + critical workloads",
   "Review identities + privileged roles",
   "Find public exposure + trust paths",
   "Check logging, keys, backups",
   "Guardrails first, then fixes"
  ],
  "start": "python scripts/aegissec_agent.py --agent security-cloud-security-architect",
  "paths": [
   "playbooks/cloud-security-review.md",
   "skills/cloud/aws-security.md",
   "skills/cloud/azure-security.md",
   "skills/cloud/gcp-security.md",
   "roles/cloud-security.md"
  ],
  "gate": "Read-only by default. Any configuration change goes through production change control."
 },
 {
  "id": "iam-review",
  "cat": "Cloud & Identity",
  "title": "Too many admins, stale accounts and unknown service principals",
  "who": [
   "Identity",
   "IT",
   "GRC"
  ],
  "answer": "Inventory human, privileged, service and workload identities. Review Conditional Access, legacy protocols, PAM/PIM, app consent and dormant accounts, then fix the attack-path choke points first.",
  "steps": [
   "Inventory all identity types",
   "Review auth, federation, Conditional Access",
   "Review privilege, PAM/PIM, consent",
   "Find dormant + machine credentials",
   "Change-controlled fixes, then retest"
  ],
  "start": "python scripts/aegissec_agent.py --agent engineering-identity-access-engineer",
  "paths": [
   "playbooks/identity-security-review.md",
   "skills/identity-security/entra-id-security.md",
   "skills/identity-security/active-directory-hardening.md",
   "skills/identity-security/pam-pim-security.md",
   "skills/identity-security/workload-machine-identity.md"
  ],
  "gate": "Disabling accounts or roles is a production change: approval + rollback."
 },
 {
  "id": "wordpress",
  "cat": "AppSec",
  "title": "Our WordPress site / plugin needs hardening before it gets hacked",
  "who": [
   "Dev",
   "Agency",
   "SMB"
  ],
  "answer": "Inventory core, plugins and themes, then review custom PHP for nonce, capability, sanitisation and escaping flaws. Also review REST/AJAX endpoints, uploads, secrets, headers, backups, and admin users and MFA.",
  "steps": [
   "Inventory core / plugins / themes",
   "Review admins, roles, MFA",
   "Review PHP: nonce, caps, escaping, SQL",
   "Review REST/AJAX, uploads, secrets",
   "Remove abandoned components"
  ],
  "start": "npx skills add ymmiah/AegisSec -s aegissec -s aegissec-wordpress-review",
  "paths": [
   "playbooks/wordpress-security-review.md",
   "skills/aegissec/aegissec-wordpress-review/SKILL.md",
   "skills/platform/wordpress-security.md",
   "skills/senior/wordpress-engineer/SKILL.md"
  ],
  "gate": "Code review is static. Scanning a live site requires a scope."
 },
 {
  "id": "ai-agent",
  "cat": "AI Security",
  "title": "We're shipping an AI agent / MCP server. What can go wrong?",
  "who": [
   "AI Eng",
   "AppSec",
   "Platform"
  ],
  "answer": "Map models, prompts, memory, RAG, tools, MCP servers and identities. Mark every untrusted-input path, treat each tool call as a privileged API call, keep high-impact actions behind approval, and add replayable tool-call audit trails.",
  "steps": [
   "Map models, tools, MCP, memory, RAG",
   "Mark prompt-injection boundaries",
   "Least privilege + per-action policy",
   "Keep secrets out of model context",
   "Telemetry + synthetic-data leakage tests"
  ],
  "start": "playbooks/ai-agent-security-review.md",
  "paths": [
   "playbooks/ai-agent-security-review.md",
   "skills/ai-security/tool-mcp-security.md",
   "skills/ai-security/secure-mcp-server-development.md",
   "skills/ai-security/rag-security.md",
   "playbooks/genai-incident-response.md"
  ],
  "gate": "Leakage tests use synthetic data only."
 },
 {
  "id": "third-party-skills",
  "cat": "AI Security",
  "title": "Can we trust this third-party agent skill / prompt pack?",
  "who": [
   "AI Eng",
   "AppSec",
   "GRC"
  ],
  "answer": "Pin the source, licence and commit. Inspect high-risk skills first (shell, credentials, exploitation, network), test them in LAB mode with synthetic secrets, and verify they cannot override scope, approval or data-handling controls.",
  "steps": [
   "Pin source, licence, commit",
   "Inspect without --skip-check",
   "Review high-risk skills + helper scripts",
   "Test in LAB with fake secrets",
   "Record the accepted revision"
  ],
  "start": "python scripts/aegissec.py upstream-status",
  "paths": [
   "playbooks/third-party-agent-skill-review.md",
   "policy/third-party-skills.md",
   "skills/ai-security/agent-skill-security.md",
   "upstream/source.lock.json"
  ],
  "gate": "Third-party skills are knowledge, not permission."
 },
 {
  "id": "purple-team",
  "cat": "Purple Team",
  "title": "Would our detections actually catch a real attacker?",
  "who": [
   "Purple Team",
   "Detection Eng",
   "SOC"
  ],
  "answer": "Plan an authorised, ATT&CK-mapped emulation where every step names the detection it should trigger, then map detections, findings and controls to ATT&CK and report the coverage gaps.",
  "steps": [
   "Pick a threat profile",
   "ATT&CK-mapped emulation plan",
   "Expected detection per step",
   "Run in scope, record hits / misses",
   "Coverage gap report + new detections"
  ],
  "start": "npx skills add ymmiah/AegisSec -s aegissec -s aegissec-adversary-emulation-plan -s aegissec-attack-technique-coverage",
  "paths": [
   "skills/aegissec/aegissec-adversary-emulation-plan/SKILL.md",
   "skills/aegissec/aegissec-attack-technique-coverage/SKILL.md",
   "skills/purple-team/detection-validation.md",
   "roles/purple-team.md"
  ],
  "gate": "Emulation runs only in a scoped, approved window."
 },
 {
  "id": "threat-hunt",
  "cat": "Detection & Response",
  "title": "We suspect something is in the network that no alert has caught",
  "who": [
   "Threat Hunter",
   "SOC",
   "CTI"
  ],
  "answer": "Start from a falsifiable hypothesis, map the telemetry you need (and the gaps), query a defined time range, pivot only on evidence, and turn useful hunt logic into maintained detections.",
  "steps": [
   "State a falsifiable hypothesis",
   "Map telemetry + gaps",
   "Query a defined range + population",
   "Pivot on evidence only",
   "Escalate to IR, ship a detection"
  ],
  "start": "playbooks/threat-hunting.md",
  "paths": [
   "playbooks/threat-hunting.md",
   "skills/blue-team/threat-hunting.md",
   "skills/threat-intel/cti-analysis.md",
   "skills/senior/threat-hunter/SKILL.md"
  ],
  "gate": "Hunting is read-only over your own telemetry."
 },
 {
  "id": "exposure",
  "cat": "Exposure",
  "title": "Thousands of findings across tools, and no idea which ones lead to the crown jewels",
  "who": [
   "Security Lead",
   "Vuln Mgmt",
   "Cloud"
  ],
  "answer": "Establish asset and ownership truth, correlate vulnerability, identity, configuration and internet exposure, build attack paths to critical assets, and fix the choke points that break the most paths.",
  "steps": [
   "Asset + owner truth",
   "Correlate vuln, identity, config, exposure",
   "De-duplicate + validate",
   "Build attack paths",
   "Fix choke points, measure reduction"
  ],
  "start": "playbooks/exposure-management.md",
  "paths": [
   "playbooks/exposure-management.md",
   "skills/red-team/attack-surface-discovery.md",
   "docs/risk-prioritisation.md"
  ],
  "gate": "External discovery of assets you don't own is out of scope."
 },
 {
  "id": "prod-change",
  "cat": "Governance",
  "title": "We need to push a security fix to production without breaking things",
  "who": [
   "SRE",
   "Platform",
   "Change Mgr"
  ],
  "answer": "Plan the exact change, assess the blast radius, get approval, have backup and rollback ready, run a bounded change, verify service and security telemetry, then revoke any temporary access.",
  "steps": [
   "Plan the exact change",
   "Assess blast radius",
   "Approval + rollback ready",
   "Execute a bounded change",
   "Verify telemetry, revoke temp access"
  ],
  "start": "playbooks/production-security-change.md",
  "paths": [
   "playbooks/production-security-change.md",
   "policy/production-change.md",
   "policy/human-approval.md"
  ],
  "gate": "If reality differs from the approved plan: stop and re-plan."
 },
 {
  "id": "reporting",
  "cat": "Governance",
  "title": "Findings are scattered. We need a report leadership and engineers will both read",
  "who": [
   "Consultant",
   "GRC",
   "Security Lead"
  ],
  "answer": "Evidence-based findings in one template (impact, evidence, fix, residual risk), with an executive summary on top and retest validation to close each item.",
  "steps": [
   "Collect evidence per finding",
   "Write in the finding template",
   "Executive summary on top",
   "Remediation + owner",
   "Retest and close"
  ],
  "start": "templates/finding.md",
  "paths": [
   "skills/aegissec/aegissec-finding-report/SKILL.md",
   "templates/finding.md",
   "skills/reporting/executive-reporting.md",
   "skills/reporting/retest-validation.md"
  ],
  "gate": "Report only what the evidence supports."
 }
];

(() => {
  // Mobile menu
  const btn = document.querySelector('.menu-button');
  const menu = document.querySelector('#site-menu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    }));
  }

  // Problem registry
  const REPO = 'https://github.com/ymmiah/AegisSec/blob/main/';
  const grid = document.getElementById('registry');
  const q = document.getElementById('q');
  const filters = document.getElementById('filters');
  const count = document.getElementById('count');
  if (!grid) return;

  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const GROUPS = {
    'All': () => true,
    'Dev & AppSec': p => p.who.some(w => /Dev|AppSec|Agency|SMB/.test(w)),
    'SOC & IR': p => p.who.some(w => /SOC|DFIR|IR Lead|Hunter|Blue|CTI/.test(w)),
    'Cloud & Identity': p => p.cat === 'Cloud & Identity',
    'AI Security': p => p.cat === 'AI Security',
    'Offensive / Purple': p => /Offensive|Purple/.test(p.cat),
    'GRC & Leadership': p => p.who.some(w => /GRC|Leader|Lead$|Change|Consultant/.test(w)),
  };
  let active = 'All';

  Object.keys(GROUPS).forEach(name => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'chip'; b.textContent = name;
    b.setAttribute('aria-pressed', String(name === active));
    b.addEventListener('click', () => {
      active = name;
      filters.querySelectorAll('.chip').forEach(c => c.setAttribute('aria-pressed', String(c.textContent === active)));
      render();
    });
    filters.appendChild(b);
  });

  const isFile = s => !/\s/.test(s) && s.includes('/');
  const card = (p, i) => `
    <article class="problem" id="p-${esc(p.id)}">
      <div class="problem-top"><span class="num">#${String(i + 1).padStart(2, '0')}</span><span class="cat">${esc(p.cat)}</span></div>
      <h3>${esc(p.title)}</h3>
      <div class="who" aria-label="Who it hurts">${p.who.map(w => `<span>${esc(w)}</span>`).join('')}</div>
      <p class="answer">${esc(p.answer)}</p>
      <ol class="steps" aria-label="Workflow">${p.steps.map(s => `<li>${esc(s)}</li>`).join('')}</ol>
      <p class="guard">${esc(p.gate)}</p>
      <details class="problem-more"><summary>Files in the repo (${p.paths.length})</summary>
        <div class="files">${p.paths.map(f => `<a href="${REPO}${esc(f)}" rel="noopener">${esc(f)}</a>`).join('')}</div>
      </details>
      <div class="start">
        <div class="start-label"><span>Start with</span><button class="copy" type="button" data-copy="${esc(p.start)}">Copy</button></div>
        <pre>${isFile(p.start) ? `<a href="${REPO}${esc(p.start)}" rel="noopener">${esc(p.start)}</a>` : esc(p.start)}</pre>
      </div>
    </article>`;

  function render() {
    const term = (q.value || '').trim().toLowerCase();
    const list = PROBLEMS.map((p, i) => [p, i]).filter(([p]) => GROUPS[active](p) &&
      (!term || [p.title, p.answer, p.cat, p.who.join(' '), p.steps.join(' '), p.paths.join(' '), p.start].join(' ').toLowerCase().includes(term)));
    grid.innerHTML = list.length ? list.map(([p, i]) => card(p, i)).join('') :
      `<div class="empty">No problem matches yet. Try "CVE", "phishing", "MCP" or "IAM", or <a href="https://github.com/ymmiah/AegisSec/issues">suggest one</a>.</div>`;
    count.textContent = `${list.length} of ${PROBLEMS.length} problems`;
  }
  q.addEventListener('input', render);
  grid.addEventListener('click', e => {
    const b = e.target.closest('.copy');
    if (!b) return;
    navigator.clipboard?.writeText(b.dataset.copy).then(() => { b.textContent = 'Copied'; setTimeout(() => (b.textContent = 'Copy'), 1400); });
  });
  if (location.hash.startsWith('#p-')) setTimeout(() => document.querySelector(location.hash)?.scrollIntoView(), 50);
  render();
})();
