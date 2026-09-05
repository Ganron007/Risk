# CISO-EX-004 — Framework selection and loading

**Platform:** CISO Assistant Community Edition  
**Time:** 20 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 6 (Assessment & Testing)  
**Prerequisites:** CISO-EX-001 completed

---

## Objective

Load and configure three compliance frameworks in CISO Assistant — ISO 27001, SOC 2, and NIST CSF — and demonstrate how Cadre Corp's controls map across all three. This is the practical implementation of multi-framework compliance, a core GRC competency.

---

## Steps

### Step 1 — Load framework libraries
1. Navigate to **Libraries** → **Load Library**.
2. Load each framework:
   - **ISO/IEC 27001:2022** — Annex A controls (93 controls across 4 themes)
   - **SOC 2 Trust Services Criteria** — Security, Availability, Confidentiality
   - **NIST Cybersecurity Framework v1.1** — Identify, Protect, Detect, Respond, Recover

### Step 2 — Create framework instances for Cadre Corp
1. Navigate to **Compliance** → **Frameworks**.
2. Create an assessment/implementation tracking instance for each framework:
   - **ISO 27001 Certification Program** — Target: achieve certification within 12 months
   - **SOC 2 Type II Audit (2026)** — Target: clean opinion within 6 months
   - **NIST CSF Implementation Profile** — Target: continuous improvement, no specific certification

### Step 3 — Map a control to all three frameworks
Select CTL-SIEM-IDENTITY (from CISO-EX-003). Map it to:
- **ISO 27001:** A.12.6.1 (Management of technical vulnerabilities) + A.12.4.1 (Event logging)
- **SOC 2:** CC7.1 (Detection and monitoring) + CC7.2 (Detection of anomalies)
- **NIST CSF:** DE.AE (Anomalies and Events) + DE.CM (Continuous Monitoring)

This demonstrates that a single Cadre Corp control satisfies requirements across all three frameworks — the "map once, comply many" principle.

### Step 4 — Generate framework coverage report
1. Navigate to the ISO 27001 instance.
2. Review the coverage dashboard: which Annex A controls are covered? Which have no Cadre Corp controls?
3. Note the uncovered controls as a gap list for the next control development sprint.

---

## Verification Checklist

- [ ] ISO 27001:2022, SOC 2, and NIST CSF frameworks loaded
- [ ] Framework instances created for Cadre Corp with target dates
- [ ] CTL-SIEM-IDENTITY mapped to all three frameworks
- [ ] Gap report shows uncovered controls requiring attention

---

## CISSP Connection

**Domain 1:** Multi-framework compliance — mapping one set of controls to satisfy ISO 27001, SOC 2, and NIST CSF simultaneously — is a key CISSP governance skill. It demonstrates understanding that frameworks overlap significantly and can be addressed with a unified control set.

**Domain 6:** Framework assessment is an ongoing assessment activity. The coverage gap report is a security assessment output feeding the control development backlog.

---

## Interview Talking Points

1. **"Map once, comply many":** "ISO 27001, SOC 2, and NIST CSF share 70%+ overlap. I don't build three separate control sets — I build one Cadre Corp control library and map it to all three frameworks. When an auditor asks about a specific control, I show the single implementation that satisfies all relevant framework requirements."

2. **"The gap report drives the roadmap":** "After mapping, I identify which framework controls have no Cadre Corp implementation. That gap list becomes the prioritized control development backlog. 'We're not compliant with Annex A.14.2.8' isn't a finding — it's a ticket with an owner and a due date."
