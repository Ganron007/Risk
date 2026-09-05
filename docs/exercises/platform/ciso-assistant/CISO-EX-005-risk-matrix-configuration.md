# CISO-EX-005 — Risk matrix configuration

**Platform:** CISO Assistant Community Edition  
**Time:** 20 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 6 (Assessment & Testing)  
**Prerequisites:** CISO-EX-001 completed, 5x5 ISO-27005 library loaded

---

## Objective

Configure, customize, and validate the 5x5 ISO-27005 risk matrix in CISO Assistant. Understand how the matrix translates qualitative risk ratings into actionable scores, and verify that Cadre Corp's risk appetite thresholds are correctly reflected.

---

## Steps

### Step 1 — Review the loaded 5x5 ISO-27005 matrix
1. Navigate to **Risk** → **Risk Matrix**.
2. Observe the default 5x5 grid:
   - **Likelihood:** 1 (Very Low) to 5 (Very High)
   - **Impact:** 1 (Very Low) to 5 (Very High)
   - **Score:** Likelihood × Impact → 1–25

### Step 2 — Map Cadre Corp's 3×3 scale to the 5×5 matrix
Cadre Corp uses a 3×3 scale (1-3) in `docs/risk-register-baseline.md`. Map it:

| Cadre Corp 3×3 | ISO 27005 5×5 | Justification |
|----------------|---------------|---------------|
| Likelihood 1 (Low) | 1-2 | Rare or unlikely in current environment |
| Likelihood 2 (Medium) | 3 | Possible, documented attack path exists |
| Likelihood 3 (High) | 4-5 | Validated exploitable in campaign exercises |
| Impact 1 (Low) | 1-2 | Internal lab systems, no client data |
| Impact 2 (Medium) | 3 | Business ops, telemetry, member servers |
| Impact 3 (High) | 4-5 | Client evidence, identity plane, PKI |

### Step 3 — Define risk acceptance thresholds
Configure in the matrix:
- **Low (1-6):** Accept — within risk appetite for research labs and workstations
- **Medium (8-12):** Monitor — require documented justification and quarterly review
- **High (15-20):** Mitigate — active remediation plan required, board visibility
- **Critical (25):** Immediate escalation — CISO must be notified, board briefed within 7 days

Verify these thresholds against `docs/risk-appetite-statement.md`.

### Step 4 — Validate with Cadre Corp risks
Check that Cadre Corp's risk scores map correctly:
- RISK-001 (3×3, 3×3 = score 9) → mapped to 5×5: likelihood 5, impact 5 = 25 (Critical)
- RISK-007 (2×3 = 6) → mapped to 5×5: likelihood 3, impact 5 = 15 (High)
- RISK-016 (2×2 = 4) → mapped to 5×5: likelihood 3, impact 2 = 6 (Low/Medium)

### Step 5 — Document the matrix configuration for auditors
Screenshot the configured matrix. Save to `docs/img/ciso-risk-matrix.png`. The auditor will ask: "What risk methodology do you use?" The answer: "ISO 27005 5x5 qualitative matrix, mapped to our internal 3x3 scale, with acceptance thresholds aligned to our board-approved risk appetite statement."

---

## Verification Checklist

- [ ] 5x5 ISO-27005 matrix loaded and reviewed
- [ ] Cadre Corp 3×3 scale mapped to 5×5 with documented justification
- [ ] Risk acceptance thresholds defined: Low, Medium, High, Critical
- [ ] Cadre Corp risks validate correctly against thresholds
- [ ] Matrix screenshot saved for audit evidence

---

## CISSP Connection

**Domain 1:** The risk matrix is the quantitative tool behind qualitative risk analysis. CISSP tests the theory (likelihood × impact = risk score); this exercise demonstrates the operational implementation — configuring the actual matrix in a GRC tool and mapping the organization's risk appetite to specific score thresholds.

**Domain 6:** The matrix configuration is itself an assessment control design activity. Validating that Cadre Corp's risk scores produce appropriate treatment recommendations is a control effectiveness test.

---

## Interview Talking Points

1. **"The matrix isn't abstract — it drives decisions":** "When RISK-001 scores Critical (25), our policy REQUIRES board notification within 7 days. When RISK-016 scores Low (6), the policy allows acceptance without escalation. The matrix isn't a diagram — it's a decision engine programmed with our risk appetite."

2. **"I can map between scales":** "Cadre Corp uses a simplified 3×3 scale for internal communication, mapped to ISO 27005's 5×5 for external audit compliance. I can explain the mapping to both the board ('here's what High means to us') and the auditor ('here's how it maps to your framework')."
