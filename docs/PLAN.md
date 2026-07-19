# CADRE-Risk — Master Implementation Plan (v1 — REFERENCE ONLY)

> **SUPERSEDED for execution:** use [`../plan_v2.md`](../plan_v2.md) + [`../CHECKLIST.md`](../CHECKLIST.md).  
> **This file (v1)** remains the reference dump for Cadre Corp fiction, full exercise ID catalog (R-EX-*), and R-IMP-* history.  
> Do **not** start new work from the phase checkboxes below — follow plan_v2 sprints instead.  
> **2026-07-13:** Eramba was **removed** from CADRE-Risk (did not work for the lab). Ignore Eramba mentions below; GRC sinks are **CISO Assistant** + **VerifyWise** only.

> **Created:** 2026-07-12  
> **Goal:** Build a hands-on GRC lab where CISSP risk management concepts are practiced against the real Cadre Corp DFIR infrastructure — not a pipeline, but a **simulated enterprise risk program**.  
> **Tracking (legacy):** `R-IMP-NNN` / `R-EX-*` IDs below are still valid *names* for exercises; status lives in `CHECKLIST.md` under plan_v2.

---

## 1. The concept — "something no one did"

Most CISSP study is passive: read the book, take practice tests. Nobody builds a **hands-on GRC lab** where you actually *do* the risk management work against a real infrastructure with real findings.

**CADRE-Risk is that lab.** The "game board" is **Cadre Corp** — your actual DFIR service company infrastructure (the CADRE AD estate, cloud tenant, SOC stack, and workstation). The "findings" are real artifacts produced by your security tools (DarkAI audit logs, Praxis SARIF, Elastic detections, Velociraptor incidents). The "skill" is the full CISSP risk lifecycle: identify → classify → score → treat → report → monitor.

What makes it unique: **you're not scoring abstract risk.** You're scoring "a prompt-injection attack on Cadre Corp's customer-facing chatbot leaked 3 API keys — what's the business impact on our DFIR contract pipeline? What controls failed? How do you brief the board?"

### Three layers

| Layer | What it is | CISSP domains |
|-------|-----------|---------------|
| **Layer 1 — Enterprise context** | Cadre Corp asset inventory, business context, regulatory obligations, risk appetite | 1, 2 |
| **Layer 2 — CISSP exercises** | 60-80 hands-on risk exercises mapped to domains, each using a real finding | 1, 2, 3, 4, 6, 7, 8 |
| **Layer 3 — Tooling pipeline** | Python pipeline: ingest findings → score → push to Eramba → generate board reports | 7, 8 |

---

## 2. Cadre Corp — the enterprise context

### Company profile

| Attribute | Value |
|-----------|-------|
| **Name** | Cadre Corp |
| **Industry** | Digital Forensics & Incident Response (DFIR) services |
| **Revenue** | $12M ARR (mid-size) |
| **Employees** | 45 (15 DFIR analysts, 10 SOC, 5 R&D, 10 GRC/audit, 5 leadership) |
| **Customers** | 120 enterprise clients under DFIR retainers |
| **Regulatory** | SOC 2 Type II (required by client contracts), GDPR (EU client data), ISO 27001 (in progress) |
| **Risk appetite** | Low — any breach of client forensic data is existential to the business |
| **Forest** | `cadre.local` (forest root) + `child.cadre.local` + `range.local` trust |

### Asset inventory (from architecture.md + win11-workstation.md)

All assets are on `192.168.77.0/24` (vmnet2 host-only).

#### Windows infrastructure (7 VMs)

| Asset ID | Hostname | IP | OS | Classification | Owner | CISSP domain |
|----------|----------|----|----|---------------|-------|-------------|
| AST-001 | dc01 | .10 | Server 2025 | Restricted | Infrastructure lead | 3 (SE) |
| AST-002 | dc02 | .11 | Server 2025 | Restricted | Infrastructure lead | 3 (SE) |
| AST-003 | dc03 | .12 | Server 2025 | Restricted | Infrastructure lead | 3 (SE) |
| AST-004 | mbr01 | .22 | Server 2025 | Confidential | App team | 3 (SE) |
| AST-005 | mbr02 | .23 | Server 2025 | Confidential | App team | 3 (SE) |
| AST-006 | linux01 | .40 | Ubuntu 24.04 | Confidential | App team | 3 (SE) |
| AST-007 | ws01 | .62 | Win11 Ent 23H2 | Internal | SOC manager | 3 (SE) |

#### SOC & monitoring stack (4 VMs)

| Asset ID | Hostname | IP | OS | Classification | Owner | Role |
|----------|----------|----|----|---------------|-------|------|
| AST-010 | elk | .50 | Ubuntu 24.04 | Restricted | SOC lead | SIEM (Elastic + Kibana + Fleet) |
| AST-011 | vr | .51 | Ubuntu 24.04 | Confidential | DFIR lead | Velociraptor (DFIR + MCP) |
| AST-012 | monitor | .55 | Ubuntu 24.04 | Confidential | SOC lead | Zeek/Suricata/Arkime |
| AST-013 | provisioning | .60 | Ubuntu 24.04 | Internal | Infra lead | Ansible runner |

#### Cloud plane (Microsoft tenant)

| Asset ID | Component | Classification | Owner |
|----------|-----------|---------------|-------|
| AST-020 | Entra ID (M365 dev tenant) | Restricted | Cloud security lead |
| AST-021 | Azure subscription (RBAC/PIM) | Restricted | Cloud security lead |
| AST-022 | Cloud Sync agent (on dc01) | Restricted | Infra lead |
| AST-023 | Azure Arc (→ dc01) | Confidential | Cloud security lead |

#### Data & applications

| Asset ID | Component | Classification | Data type | Owner |
|----------|-----------|---------------|-----------|-------|
| AST-030 | Client forensic evidence (DFIR cases) | **Restricted** | PII + legal | DFIR lead |
| AST-031 | Elastic indices (SIEM logs) | Confidential | Telemetry | SOC lead |
| AST-032 | Velociraptor collected artifacts | **Restricted** | Forensic data | DFIR lead |
| AST-033 | MSSQL databases (mbr01/mbr02/linux01) | Confidential | Business data | App team |
| AST-034 | ADCS certificate authority (dc01) | **Restricted** | PKI keys | Infra lead |
| AST-035 | DarkAI lab (docker, 172.20.0.0/24) | Internal | Research | R&D |

#### People (business roles for risk ownership)

| Role | Unit | Risk responsibility |
|------|------|---------------------|
| CEO | Leadership | Final risk acceptance (board-level) |
| CISO | GRC/Audit | Risk register owner, treatment decisions |
| DFIR Lead | Operations | Client forensic data risk, incident response |
| SOC Lead | Operations | Detection gaps, monitoring coverage |
| Infra Lead | Infrastructure | AD/PKI/cloud infrastructure risk |
| R&D Lead | Engineering | Lab/research environment risk (DarkAI, Praxis) |

### Regulatory & contractual obligations

| Framework | Driver | Key obligations |
|-----------|--------|----------------|
| **SOC 2 Type II** | Client contracts (120 enterprises) | Continuous monitoring, access controls, incident response, evidence integrity |
| **GDPR** | EU client forensic data | Data minimization, breach notification (72h), DPO, cross-border transfer controls |
| **ISO 27001** | Internal certification goal | Risk assessment, statement of applicability, ISMS |
| **Attorney-client privilege** | DFIR engagement contracts | Evidence chain-of-custody, access restrictions, privileged data handling |

### Risk appetite statement (from the "board")

> Cadre Corp operates a DFIR services business where client trust is existential. We have **low risk appetite** for any event that compromises client forensic data, evidence chain-of-custody, or our detection/monitoring capabilities. We have **moderate appetite** for controlled research lab risk (DarkAI, RevAI) provided it remains isolated from client data. We have **zero tolerance** for regulatory non-compliance (SOC 2, GDPR).

---

## 3. CISSP domain exercise mapping

Each exercise uses a real finding from the CADRE ecosystem and requires a hands-on risk decision.

### Domain 1 — Security and Risk Management (~15 exercises)

| ID | Exercise | Source finding | CISSP skill |
|----|----------|---------------|-------------|
| R-EX-001 | Risk register setup — seed 20 baseline risks from the asset inventory | architecture.md | Risk identification |
| R-EX-002 | Risk assessment — score the DCSync attack surface on dc01 | CADRE attack surface summary | Qualitative risk analysis |
| R-EX-003 | BIA — Business Impact Analysis for the Elastic SIEM (AST-010) | architecture.md | BIA, criticality |
| R-EX-004 | ALE calculation — annualized loss expectancy for a client data breach | GDPR penalties + DFIR revenue | Quantitative risk |
| R-EX-005 | Risk treatment — accept vs mitigate vs transfer for the DarkAI lab | DarkAI isolation rules | Treatment decision |
| R-EX-006 | Framework mapping — map CADRE controls to NIST CSF + ISO 27001 | architecture.md detection coverage | Framework alignment |
| R-EX-007 | Policy drafting — write the Cadre Corp information security policy | Risk appetite statement | Policy development |
| R-EX-008 | Third-party risk — assess the Azure dev tenant exposure | Cloud plane architecture | Vendor risk |
| R-EX-009 | Risk monitoring — define KRIs and KPIs for the SOC | SOC stack assets | Metrics |
| R-EX-010 | Board reporting — write a quarterly risk memo from the top 5 risks | Register output | Executive communication |
| R-EX-011-015 | (5 more: exception management, risk culture, training, insurance, due diligence) | various | various |

### Domain 2 — Asset Security (~10 exercises)

| ID | Exercise | Source finding | CISSP skill |
|----|----------|---------------|-------------|
| R-EX-016 | Asset classification — classify all 30+ assets using the CADRE inventory | architecture.md | Classification |
| R-EX-017 | Data lifecycle — map the lifecycle of client forensic evidence | DFIR case workflow | Data handling |
| R-EX-018 | Privacy assessment — GDPR data flow for EU client evidence | Cloud plane | Privacy |
| R-EX-019 | Asset retention — define retention for Velociraptor artifacts | AST-032 | Retention/destruction |
| R-EX-020 | Data remanence — secure disposal procedure for decommissioned VMs | VM lifecycle | Media sanitation |
| R-EX-021-025 | (5 more: custody chain, SCIF, labeling, roles, inventory audit) | various | various |

### Domain 3 — Security Architecture & Engineering (~8 exercises)

| ID | Exercise | Source finding | CISSP skill |
|----|----------|---------------|-------------|
| R-EX-026 | Trust model — assess the `range.local` cross-forest trust | Trust topology | Security models |
| R-EX-027 | Cryptography — evaluate Kerberos AES vs RC4 in the estate | CADRE Kerberos config | Crypto evaluation |
| R-EX-028 | Secure design — review ADCS ESC1-15 attack surface as a design flaw | ADCS architecture | Design weakness |
| R-EX-029 | Vulnerability assessment — score the SCCM misconfig on mbr02 | SCCM site CAD | Vuln assessment |
| R-EX-030 | Cloud architecture — Azure Arc + PIM risk evaluation | Cloud plane | Cloud security |

### Domain 6 — Security Assessment & Testing (~8 exercises)

| ID | Exercise | Source finding | CISSP skill |
|----|----------|---------------|-------------|
| R-EX-031 | Pentest scoping — define scope for a CADRE red-team engagement | CADRE attack surfaces | Pentest management |
| R-EX-032 | SARIF interpretation — review a Praxis scan report | Praxis output | Finding assessment |
| R-EX-033 | Log audit — review the Windows telemetry baseline for gaps | architecture.md telemetry | Control testing |
| R-EX-034 | SOC 2 audit prep — map controls to SOC 2 trust principles | Regulatory obligations | Audit readiness |
| R-EX-035 | Pen test remediation — track DCSync/Kerberoast findings to closure | CADRE cert coverage | Remediation tracking |

### Domain 7 — Security Operations (~10 exercises)

| ID | Exercise | Source finding | CISSP skill |
|----|----------|---------------|-------------|
| R-EX-036 | Incident classification — classify a DarkAI prompt-injection event | DarkAI audit JSONL | Incident handling |
| R-EX-037 | IR playbook — write a playbook for a Velociraptor detection | VR artifacts | IR procedures |
| R-EX-038 | Detection gap — identify what the SOC missed during a simulated breach | Elastic detection coverage | Gap analysis |
| R-EX-039 | Evidence handling — chain-of-custody for a DFIR case | AST-030, AST-032 | Forensics |
| R-EX-040 | Disaster recovery — BCP/DRP for the SIEM (AST-010) failure | architecture.md | BCP/DR |
| R-EX-041-045 | (5 more: SOC metrics, threat intel, CSIRT, comms, post-incident) | various | various |

### Domain 8 — Software Development Security (~5 exercises)

| ID | Exercise | Source finding | CISSP skill |
|----|----------|---------------|-------------|
| R-EX-046 | Secure SDLC — assess the DarkAI lab's `.praxis.policy.json` as SSDLC | Praxis integration | SDLC |
| R-EX-047 | CI/CD risk — evaluate the Ansible pipeline security | provisioning VM | Pipeline risk |
| R-EX-048 | API security — assess the Velociraptor MCP endpoint | AST-011 | API security |
| R-EX-049 | Supply chain — Praxis threat intel assessment of dependencies | Praxis intel module | Supply chain |
| R-EX-050 | Malware analysis risk — assess RevAI findings as risk inputs | RevAI output | Malware risk |

**Total: ~55-65 exercises across 6 CISSP domains.**

---

## 4. Tooling pipeline (Layer 3)

### Architecture

```
CADRE-DarkAI audit JSONL ──┐
Praxis SARIF ──────────────┤
Elastic detection alerts ──┼──► ingest.py ──► risk_engine.py ──► eramba_client.py ──► Eramba GRC
Velociraptor artifacts ────┤                       │
RevAI malware reports ─────┘                       ▼
                                            board_report.py ──► Markdown board memo
```

### Components

| Component | Purpose | CISSP domain |
|-----------|---------|-------------|
| `src/ingest.py` | Read findings from CADRE projects (normalizes JSONL/SARIF/artifacts) | 7 |
| `src/risk_engine.py` | Score risks (qualitative matrix + ALE), map to assets/controls | 1 |
| `src/eramba_client.py` | Push risks/controls/assets to Eramba via REST API | 1, 7 |
| `src/board_report.py` | Generate Markdown board memo from top-N risks | 1 |
| `config/risk-mapping.yml` | Asset → owner → classification → control mappings | 1, 2 |
| `samples/` | Example findings from each CADRE source | all |

### Finding schema (unified)

```json
{
  "id": "cadre-finding-001",
  "source": "darkai",
  "severity": "high",
  "title": "Prompt injection leaked DARKAI-SECRET-42 via /chat",
  "description": "STUB_INJECTABLE mode allowed direct override of system prompt.",
  "asset_id": "AST-035",
  "discovered_at": "2026-07-12T14:30:00Z",
  "evidence": "artifacts/logs/prompt-audit.jsonl:42",
  "raw": { /* original JSONL line */ }
}
```

### Risk scoring (enhanced from README)

| Likelihood | Impact | Score | ALE range | Treatment |
|------------|--------|-------|-----------|-----------|
| Low (1) | Low (1) | Low (1) | < $10K | Accept/monitor |
| Low (1) | Medium (2) | Low (2) | $10K-$50K | Accept/monitor |
| Low (1) | High (3) | Medium (3) | $50K-$100K | Mitigate |
| Medium (2) | Low (1) | Medium (2) | $10K-$50K | Accept/monitor |
| Medium (2) | Medium (2) | Medium (4) | $50K-$200K | Mitigate |
| Medium (2) | High (3) | High (6) | $200K-$500K | Mitigate/transfer |
| High (3) | Low (1) | Medium (3) | $50K-$100K | Mitigate |
| High (3) | Medium (2) | High (6) | $200K-$500K | Mitigate/transfer |
| High (3) | High (3) | Critical (9) | > $500K | Remediate immediately |

---

## 5. Implementation phases

### Phase 0 — Enterprise context setup (do first)
- [ ] R-IMP-001: Create `docs/enterprise-context.md` (Cadre Corp profile + asset inventory + risk appetite) from the data in this plan
- [ ] R-IMP-002: Create `config/asset-inventory.csv` (machine-readable, importable to Eramba)
- [ ] R-IMP-003: Create `config/risk-mapping.yml` (asset → owner → classification → control)
- [ ] R-IMP-004: Create `docs/risk-appetite-statement.md` (the board's risk tolerance, approved)
- [ ] R-IMP-005: Create `docs/regulatory-obligations.md` (SOC 2, GDPR, ISO 27001 obligation register)

### Phase 1 — Risk register baseline (Layer 2 start)
- [ ] R-IMP-006: Create `samples/findings/` with 5 example findings from each CADRE source (DarkAI, Praxis, Elastic, VR, RevAI)
- [ ] R-IMP-007: Write R-EX-001 through R-EX-010 (Domain 1 exercises) in `docs/exercises/`
- [ ] R-IMP-008: Create `docs/risk-register-baseline.md` (20 seeded risks from the asset inventory)
- [ ] R-IMP-009: Create `docs/control-register.md` (existing CADRE controls mapped to NIST CSF + ISO 27001)

### Phase 2 — Tooling pipeline (Layer 3)
- [ ] R-IMP-010: Build `src/ingest.py` — read DarkAI JSONL + Praxis SARIF + example artifacts
- [ ] R-IMP-011: Build `src/risk_engine.py` — score findings using the matrix + ALE
- [ ] R-IMP-012: Build `src/eramba_client.py` — push risks/assets/controls to Eramba API
- [ ] R-IMP-013: Build `src/board_report.py` — generate Markdown board memo
- [ ] R-IMP-014: Create `tests/test_risk_engine.py` — verify scoring logic

### Phase 3 — CISSP exercise curriculum (Layer 2 complete)
- [ ] R-IMP-015: Write Domain 2 exercises (R-EX-016 → R-EX-025)
- [ ] R-IMP-016: Write Domain 3 exercises (R-EX-026 → R-EX-033)
- [ ] R-IMP-017: Write Domain 6 exercises (R-EX-031 → R-EX-035)
- [ ] R-IMP-018: Write Domain 7 exercises (R-EX-036 → R-EX-045)
- [ ] R-IMP-019: Write Domain 8 exercises (R-EX-046 → R-EX-050)

### Phase 4 — Eramba integration validation
- [ ] R-IMP-020: Confirm Eramba API endpoint + credentials in `docs/eramba-notes.md`
- [ ] R-IMP-021: End-to-end test: ingest 1 finding → score → push → verify in Eramba UI
- [ ] R-IMP-022: Import full asset inventory into Eramba
- [ ] R-IMP-023: Import baseline risk register into Eramba

---

## 6. Summary

| Area | `[ ]` TODO | Total |
|------|-----------|-------|
| Phase 0 — Enterprise context | 5 | 5 |
| Phase 1 — Risk register | 4 | 4 |
| Phase 2 — Tooling | 5 | 5 |
| Phase 3 — Exercises | 5 | 5 |
| Phase 4 — Eramba | 4 | 4 |
| **TOTAL** | **23** | **23** |

---

## 7. What makes this portfolio-grade

1. **It demonstrates the rare skill**: translating technical findings into business risk language.
2. **It's hands-on**: every exercise uses a real finding from a real tool against a real infrastructure.
3. **It's CISSP-aligned**: covers 6 of 8 domains with practical exercises, not flashcards.
4. **It produces real artifacts**: risk register, control register, board memos, BIA, ALE calculations — all portfolio-worthy.
5. **It integrates**: DarkAI, Praxis, CADRE, RevAI, and Eramba in one risk management lifecycle.

---

*End of PLAN.md. Start at Phase 0 — R-IMP-001.*
