# CISO-EX-011 — SOC 2 Type II audit preparation workflow

**Platform:** CISO Assistant | **Time:** 20 min | **CISSP:** 1, 6

---

## Objective

Use CISO Assistant to prepare for a SOC 2 Type II audit. Map controls to Trust Services Criteria, collect evidence, and generate an audit readiness report.

---

## Steps

### Step 1 — Map controls to SOC 2 TSCs
Navigate to the SOC 2 framework instance. Map Cadre Corp controls:

| TSC Category | Cadre Corp Control | Evidence |
|-------------|-------------------|----------|
| CC5.2 (Control Activities) | CTL-HITL | DFIR-Nexus approval logs |
| CC6.1 (Logical Access) | CTL-EVIDENCE-ACCESS | Access review reports |
| CC6.3 (Physical/Logical Access) | CTL-COC | Chain of custody records |
| CC7.1 (Detection) | CTL-SIEM-IDENTITY | Elastic detection rule validation |
| CC7.3 (Response) | IR playbooks (R-EX-037) | Tabletop exercise results |

### Step 2 — Assess operating effectiveness
For each control, verify you have evidence covering the full audit period (6-12 months). Flag controls with <6 months of evidence. Mark controls with evidence gaps as "Partially Effective."

### Step 3 — Generate audit readiness report
Export the SOC 2 mapping with evidence status. The report should identify: controls ready for audit (green), controls with evidence gaps (yellow), controls not yet implemented (red).

---

## Interview Talking Points

1. **"SOC 2 readiness is measurable, not aspirational":** "I don't guess whether we're audit-ready — I run the readiness report. Green controls = auditor-ready. Yellow = evidence gaps to close. Red = not yet implemented. The report drives the pre-audit sprint, not panic."