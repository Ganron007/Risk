# Cadre Corp — Risk Appetite Statement

> **Sprint 1:** R2-S1.2  
> **Status:** Board-approved (lab fiction) — use in Domain 1 treatment decisions  
> **Owner:** CISO (draft) / CEO (acceptance)

---

## Statement

Cadre Corp operates a DFIR services business where **client trust is existential**.

1. We have **low risk appetite** for any event that compromises:
   - Client forensic evidence or PII/legal data (AST-030)
   - Evidence chain-of-custody integrity
   - Detection and monitoring capabilities that protect client environments under retainer (AST-010, AST-012)

2. We have **moderate appetite** for controlled research-lab risk (DarkAI AST-035, RevAI analysis pipelines) **provided**:
   - Research networks remain isolated from client evidence stores
   - No production secrets or client case data enter research labs
   - Findings are treated as risk inputs, not as free pass for unsafe experiments

3. We have **zero tolerance** for:
   - Willful regulatory non-compliance (SOC 2 Type II contractual obligations, GDPR breach-notification duties)
   - Silent approval of AI-generated forensic findings without human examiner gates (where DFIR-Nexus / HITL is the control)

4. Residual risk above appetite requires **documented treatment** (mitigate / transfer / avoid) or **CEO-level acceptance** with expiry and compensating controls.

---

## Appetite by category (quick matrix)

| Category | Appetite | Typical treatment |
|----------|----------|-------------------|
| Client evidence / CoC | Low | Remediate / mitigate immediately |
| AD identity takeover (DCSync, Golden Ticket, ADCS ESC) | Low | Mitigate; track to closure |
| SOC detection gaps | Low–Moderate | Mitigate; time-boxed exceptions |
| Isolated AI/malware research labs | Moderate | Accept with isolation controls |
| Non-production lab convenience (weak passwords in AD attack surface) | Moderate (lab only) | Document as intentional training risk — never mirror to client estates |

---

## KRIs (indicative)

| KRI | Threshold (illustrative) | Escalation |
|-----|--------------------------|------------|
| Open Critical risks on Restricted assets | > 0 for > 14 days | CISO → CEO |
| Client evidence access without ticket | Any | DFIR Lead + CISO |
| SIEM / NSM outage | > 4 hours | SOC Lead |
| GDPR-relevant incident without 72h assessment | Any | CISO / DPO role |

---

## Review cadence

- Quarterly board risk memo (see `src/board_report.py` / Domain 1 R-EX-010)
- After any Sev-1 incident affecting AST-030 / AST-032
- On material change to trust topology or cloud sync

---

*R2-S1.2 — 2026-07-12*
