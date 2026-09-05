# CISO-EX-015 — Multi-framework risk assessment

**Platform:** CISO Assistant | **Time:** 20 min | **CISSP:** 1, 6

---

## Objective

Conduct a single risk assessment that simultaneously satisfies ISO 27001, SOC 2, NIST CSF, and GDPR requirements. Demonstrate the "assess once, comply many" principle of multi-framework GRC.

---

## Steps

### Step 1 — Create a unified assessment
Create a risk assessment for RISK-001 (DCSync) that maps to all four frameworks:
- **ISO 27001:** A.12.6.1 (Technical vulnerability management) + A.12.4.1 (Event logging)
- **SOC 2:** CC7.1 (Detection and monitoring)
- **NIST CSF:** DE.AE (Anomalies and Events) + DE.CM (Continuous Monitoring)
- **GDPR:** Art. 32 (Security of processing — technical measures to protect personal data)

### Step 2 — Document the evidence once, reference everywhere
Evidence: Elastic detection rule `cadre-002` (4662/DRSUAPI). Attach once. Link to all four frameworks. When the evidence is updated (rule tuned, validated in campaign), all four framework assessments automatically reflect the update.

### Step 3 — Generate multi-framework compliance report
Export a report showing: RISK-001 → CTL-SIEM-IDENTITY → Evidence: cadre-002 validated → Satisfies: ISO A.12.4.1, SOC 2 CC7.1, NIST DE.AE, GDPR Art. 32. One control, one evidence set, four frameworks satisfied.

### Step 4 — Calculate framework overlap
Run the numbers: what percentage of Cadre Corp controls satisfy 2+ frameworks? 3+? 4? This metric demonstrates GRC efficiency — "83% of our controls satisfy at least two frameworks simultaneously."

---

## Interview Talking Points

1. **"Assess once, comply many":** "I don't run four separate assessments for ISO, SOC 2, NIST, and GDPR. I assess the risk once, map the control to all four frameworks, and attach the evidence once. When the auditor for Framework A asks about Control X, I show the same evidence the Framework B auditor saw — consistent, efficient, and provable."