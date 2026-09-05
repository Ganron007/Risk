# CISO-EX-013 — NIST CSF implementation tracking

**Platform:** CISO Assistant | **Time:** 15 min | **CISSP:** 1, 6

---

## Objective

Track Cadre Corp's NIST CSF implementation maturity using CISO Assistant. Map controls to CSF functions and categories, score implementation tiers, and identify improvement priorities.

---

## Steps

### Step 1 — Map controls to CSF functions
| CSF Function | Cadre Corp Controls |
|-------------|-------------------|
| **Identify** | Asset inventory, risk register, governance framework |
| **Protect** | CTL-EVIDENCE-ACCESS, CTL-LAB-ISOLATION, IAM controls |
| **Detect** | CTL-SIEM-IDENTITY, CTL-ADCS-MONITOR, Zeek/Suricata |
| **Respond** | IR playbooks (R-EX-037), CSIRT definition |
| **Recover** | SIEM DR plan (R-EX-040), backup strategy, BCP |

### Step 2 — Score implementation tiers
Use NIST's 4-tier model: Partial (Tier 1) → Risk-Informed (Tier 2) → Repeatable (Tier 3) → Adaptive (Tier 4). Score each function:
- Identify: Tier 3 (Repeatable — documented, regularly updated)
- Protect: Tier 2 (Risk-Informed — controls exist, not fully automated)
- Detect: Tier 3 (Repeatable — detection rules deployed, validated)
- Respond: Tier 2 (Risk-Informed — playbooks exist, not fully tested)
- Recover: Tier 1 (Partial — DR plan documented but never tested)

### Step 3 — Generate improvement roadmap
Recover (Tier 1 → Tier 2): Conduct first SIEM restoration test within 30 days.
Respond (Tier 2 → Tier 3): Run quarterly tabletop exercises.
Protect (Tier 2 → Tier 3): Automate evidence collection for access reviews.

---

## Interview Talking Points

1. **"NIST CSF tiers measure maturity, not just compliance":** "Tier 1 means 'we have a plan on paper.' Tier 4 means 'we adapt automatically based on threat intelligence.' I scored Cadre Corp honestly — Tier 1 for Recovery because we've never tested our DR plan. That's not a failure — it's a roadmap."