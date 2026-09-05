# VW-EX-008 — AI risk mitigation tracking

**Platform:** VerifyWise | **Time:** 15 min | **CISSP:** 1, 7

---

## Objective

Track mitigation progress for RevAI's three AI risks (from VW-EX-005) in VerifyWise. Update mitigation status, link to evidence, and demonstrate risk treatment lifecycle management.

---

## Steps

### Step 1 — Update mitigation status for each risk
1. **Prompt injection risk:** Mitigation = HITL gate active. Status = **Implemented** — DFIR-Nexus E.0 Constellation HITL workflow deployed.
2. **Model supply chain risk:** Mitigation = Model version tracking + output monitoring. Status = **Partially Implemented** — version tracking active, output consistency monitoring in development.
3. **Data poisoning risk:** Mitigation = Provider data usage verification. Status = **Implemented** — DeepSeek TOS confirms no training on API inputs.

### Step 2 — Link evidence to mitigations
For each mitigation, attach evidence: HITL workflow documentation, model version history screenshot, provider TOS excerpt.

### Step 3 — Schedule review
Set each risk to **Review: Quarterly**. VerifyWise should flag risks due for review.

---

## Interview Talking Points

1. **"Mitigation tracking proves controls aren't just documented — they're active":** "Each AI risk has a mitigation, a status, evidence attached, and a review date. The auditor doesn't ask 'do you have controls?' — they ask 'prove they're working.' The mitigation tracker with dated evidence provides that proof."