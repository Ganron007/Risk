# CISO-EX-012 — ISO 27001 Statement of Applicability workflow

**Platform:** CISO Assistant | **Time:** 20 min | **CISSP:** 1, 6

---

## Objective

Generate an ISO 27001 Statement of Applicability (SoA) from CISO Assistant's control library. The SoA documents which Annex A controls are applicable, implemented, and the justification for exclusions.

---

## Steps

### Step 1 — Review Annex A coverage
Navigate to ISO 27001 framework → Annex A controls. For each of the 93 controls, mark status:
- **Applicable & Implemented:** Controls mapped to Cadre Corp controls (e.g., A.12.4.1 → CTL-SIEM-IDENTITY)
- **Applicable & Partially Implemented:** Controls with some evidence (e.g., A.12.4.2 → CTL-COC, but missing some evidence months)
- **Applicable & Not Implemented:** Controls on the gap list
- **Not Applicable:** Controls irrelevant to Cadre Corp's DFIR business model (e.g., A.15.1.3 — ICT supply chain for critical infrastructure — Cadre Corp is not critical infrastructure)

### Step 2 — Document justifications
For each "Not Applicable" control, write a brief justification. Example: "A.15.1.3: Not applicable — Cadre Corp is a DFIR services firm, not a critical national infrastructure operator under NIS2."

### Step 3 — Export the SoA
Generate the SoA document. This is the primary deliverable for ISO 27001 certification — the auditor will verify that: (a) applicable controls are identified, (b) implementations are evidenced, (c) exclusions are justified.

---

## Interview Talking Points

1. **"The SoA is the contract with the auditor":** "The Statement of Applicability says: 'Here are the 93 Annex A controls. These 78 apply to us. Here's how we implement them. These 15 don't apply — here's why.' The auditor tests what you declare, not what you hide. Honest, justified exclusions are better than claiming applicability without evidence."