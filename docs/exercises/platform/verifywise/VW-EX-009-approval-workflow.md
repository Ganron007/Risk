# VW-EX-009 — AI approval workflow management

**Platform:** VerifyWise | **Time:** 15 min | **CISSP:** 1, 5

---

## Objective

Configure and test VerifyWise's approval workflow for AI risk acceptances and project changes. Demonstrate governance oversight of AI system modifications.

---

## Steps

### Step 1 — Configure approval workflow
1. For the RevAI project, set approval requirements: any change to EU AI Act classification or risk acceptance requires **Risk Owner + CISO approval**.
2. Assign approvers: Risk Owner = DFIR Lead, Secondary Approver = CISO.

### Step 2 — Test the workflow
1. As org admin, attempt to change RevAI's classification from High Risk to Limited Risk.
2. The change should enter **Pending Approval** state.
3. Log in as DFIR Lead (Risk Owner) — approve.
4. The change should now require CISO approval.
5. The change is only applied after BOTH approvals.

### Step 3 — Document the governance trail
Each approval records: who approved, timestamp, and justification. This creates an auditable governance trail proving AI system changes were reviewed by appropriate authorities.

---

## Interview Talking Points

1. **"AI changes require human governance, not just automation":** "If someone tries to reclassify RevAI from High Risk to Limited Risk without justification, the approval workflow blocks it. The Risk Owner AND CISO must approve. This protects against both mistakes and misconduct — and provides an audit trail for regulators."