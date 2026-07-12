# Cadre Corp — Baseline Risk Register

> **Sprint 1:** R2-S1.6  
> **Count:** 18 risks  
> **Scoring:** Likelihood × Impact (1–3) → score 1–9 (Critical ≥ 9, High ≥ 6, Medium ≥ 3, Low &lt; 3)  
> **Appetite:** [`risk-appetite-statement.md`](risk-appetite-statement.md)

| Risk ID | Title | Asset | L | I | Score | Treatment | Owner | Status |
|---------|-------|-------|---|---|-------|-----------|-------|--------|
| RISK-001 | Domain Admin compromise via DCSync / secretsdump | AST-001 | 3 | 3 | 9 | Mitigate | Infra Lead | Open |
| RISK-002 | ADCS ESC abuse → authentication as privileged user | AST-034 | 3 | 3 | 9 | Mitigate | Infra Lead | Open |
| RISK-003 | Cross-forest trust abuse / SID history attacks | AST-003 | 2 | 3 | 6 | Mitigate | Infra Lead | Open |
| RISK-004 | Unconstrained delegation on mbr01 → credential theft | AST-004 | 3 | 3 | 9 | Mitigate | App team | Open |
| RISK-005 | SCCM / WSUS misconfig → lateral & supply-chain style abuse | AST-005 | 2 | 3 | 6 | Mitigate | App team | Open |
| RISK-006 | Kerberoast / AS-REP roast of service & weak accounts | AST-001 | 3 | 2 | 6 | Mitigate | Infra Lead | Open |
| RISK-007 | Client forensic evidence breach / CoC failure | AST-030 | 2 | 3 | 6 | Mitigate | DFIR Lead | Open |
| RISK-008 | Velociraptor artifact store unauthorized access | AST-032 | 2 | 3 | 6 | Mitigate | DFIR Lead | Open |
| RISK-009 | SIEM (Elastic) prolonged outage → detection blindness | AST-010 | 2 | 3 | 6 | Mitigate | SOC Lead | Open |
| RISK-010 | NSM gap (Zeek/Suricata) during campaign-scale attack | AST-012 | 2 | 2 | 4 | Mitigate | SOC Lead | Open |
| RISK-011 | Entra / Cloud Sync compromise pivots to hybrid identity | AST-020 | 2 | 3 | 6 | Mitigate | Cloud security lead | Open |
| RISK-012 | DarkAI lab breakout / data mix with client evidence | AST-035 | 2 | 3 | 6 | Mitigate | R&D Lead | Open |
| RISK-013 | Prompt-injection / LLM abuse leaks lab secrets | AST-035 | 3 | 2 | 6 | Mitigate | R&D Lead | Open |
| RISK-014 | Malware sample mishandling on RevAI analysis path | AST-035 | 2 | 2 | 4 | Accept* | R&D Lead | Open |
| RISK-015 | Ansible / provisioning credential misuse | AST-013 | 2 | 3 | 6 | Mitigate | Infra Lead | Open |
| RISK-016 | Analyst workstation (ws01) compromise → beachhead | AST-007 | 2 | 2 | 4 | Mitigate | SOC manager | Open |
| RISK-017 | GDPR breach-notification failure on EU evidence | AST-030 | 1 | 3 | 3 | Mitigate | CISO | Open |
| RISK-018 | AI-generated forensic finding accepted without HITL | AST-030 | 2 | 3 | 6 | Mitigate | DFIR Lead | Open |

\*Accept only with isolation controls (`CTL-LAB-ISOLATION`) and no client data — per appetite.

---

## Detail notes (selected)

### RISK-001 — DCSync / DA compromise
- **Threat:** Authenticated replication abuse after privilege escalation.
- **Impact:** Full domain takeover; client environments under retainer may share patterns.
- **Controls:** CTL-SIEM-IDENTITY, CTL-AD-BASELINE, detection rules for 4662 / DRSUAPI.
- **Sample finding link:** Campaign / Elastic-shaped sample `samples/findings/elastic-dcsync-alert.json`.

### RISK-007 — Client evidence breach
- **Threat:** Unauthorized copy, ransomware on evidence share, lost CoC.
- **Impact:** Contractual + GDPR + privilege loss — existential per appetite.
- **Controls:** CTL-COC, CTL-EVIDENCE-ACCESS, CTL-HITL.

### RISK-012 / RISK-013 — Research lab
- **Threat:** Isolation failure or prompt injection exposing secrets.
- **Controls:** CTL-LAB-ISOLATION, CTL-PRAXIS-SCAN.
- **Sample:** `samples/findings/darkai-prompt-inject.json`.

### RISK-018 — HITL bypass
- **Threat:** LLM invents findings without audit_id / examiner password.
- **Control:** DFIR-Nexus DRAFT → approve gate (`CTL-HITL`).

---

## Review

- Update status when campaign detection or hardening closes a risk.
- Board memo uses top scores from this register + live sample scoring.

---

*R2-S1.6 — 2026-07-12*
