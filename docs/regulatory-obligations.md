# Cadre Corp — Regulatory & Contractual Obligations

> **Sprint 1:** R2-S1.3  
> **Related:** [`enterprise-context.md`](enterprise-context.md) · [`risk-appetite-statement.md`](risk-appetite-statement.md)

---

## Obligation register

| ID | Framework | Driver | Key obligations | Primary assets | Owner |
|----|-----------|--------|-----------------|----------------|-------|
| REG-001 | **SOC 2 Type II** | Client retainer contracts | Continuous monitoring, access control, change management, IR, evidence integrity | AST-010–012, AST-030–032 | CISO |
| REG-002 | **GDPR** | EU client forensic data | Lawful basis, minimization, 72h breach notification, DPIA where needed, transfer controls | AST-030, AST-032, cloud AST-020 | CISO / DPO role |
| REG-003 | **ISO 27001** | Internal certification goal | Risk assessment, SoA, ISMS, continual improvement | Estate-wide | CISO |
| REG-004 | **Attorney–client / engagement privilege** | DFIR engagement contracts | Chain-of-custody, least privilege to evidence, disclosure controls | AST-030, AST-032 | DFIR Lead |
| REG-005 | **Contractual SLAs** | Retainers | Detection/response timeboxes, reporting cadence | AST-010–011 | SOC / DFIR Lead |

---

## SOC 2 Trust Services (mapping sketch)

| TSC | Cadre Corp control examples |
|-----|----------------------------|
| **Security** | AD auth, Elastic Defend/Fleet telemetry, Zeek/Suricata, HITL finding approval |
| **Availability** | SIEM/VR capacity, DR thinking for AST-010 (see R-EX later) |
| **Confidentiality** | Classification, CoC, lab isolation (AST-035) |
| **Processing integrity** | DFIR-Nexus audit chain / examiner approval |
| **Privacy** | GDPR handling of EU evidence |

Use [`control-register.md`](control-register.md) for NIST CSF / ISO crosswalks.

---

## GDPR — DFIR-specific notes

- Forensic images may contain **special category / criminal** data → treat AST-030 as Restricted.
- Lab copies for RevAI/DarkAI training must be **anonymized or synthetic** — never raw client disks in AST-035.
- Breach affecting EU client evidence triggers **72-hour assessment clock** even in this lab fiction.

---

## ISO 27001 — current state (lab)

| Item | Status |
|------|--------|
| Risk assessment process | This project (CADRE-Risk Sprint 1) |
| Statement of Applicability | Partial via control register |
| ISMS policies | Draft via R-EX-007 (information security policy exercise) |
| Certification | Not claimed — learning goal only |

---

## Evidence for audits (portfolio)

| Artifact | Path |
|----------|------|
| Asset inventory | `config/asset-inventory.csv` |
| Risk register | `docs/risk-register-baseline.md` |
| Control register | `docs/control-register.md` |
| Board memo sample | `docs/examples/board-memo-sample.md` |

---

*R2-S1.3 — 2026-07-12*
