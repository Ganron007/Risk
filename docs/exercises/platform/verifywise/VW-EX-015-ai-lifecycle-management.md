# VW-EX-015 — AI system lifecycle management

**Platform:** VerifyWise | **Time:** 15 min | **CISSP:** 1, 8

---

## Objective

Track an AI system through its full lifecycle in VerifyWise: design → deploy → monitor → decommission. Demonstrate end-to-end AI governance.

---

## Steps

### Step 1 — Lifecycle stages in VerifyWise
For each AI project, document the current lifecycle stage:

| Stage | DarkAI | RevAI | Praxis |
|-------|--------|-------|--------|
| **Design** | ✅ Complete | ✅ Complete | ✅ Complete |
| **Development** | ✅ Active (ongoing research) | ✅ Complete (v2.0) | ✅ Active (continuous) |
| **Deployment** | ✅ Lab deployment | ✅ Operational (v2.0) | ✅ CI/CD integrated |
| **Monitoring** | ⚠️ Partial (manual review) | ✅ Active (HITL + drift monitoring) | ⚠️ Partial (SARIF-based) |
| **Decommission** | N/A | N/A | N/A |

### Step 2 — Identify lifecycle gaps
- DarkAI monitoring: from manual → automated prompt injection detection
- Praxis monitoring: from SARIF-only → runtime AI behavior monitoring
- No decommissioning procedure defined for any AI system

### Step 3 — Create decommissioning procedure
When an AI system is retired: (a) revoke API keys, (b) archive model outputs, (c) update VerifyWise status to "Decommissioned" with date, (d) notify stakeholders, (e) retain decommissioning record for audit.

---

## Interview Talking Points

1. **"AI systems have lifecycles, not just deployments":** "Every AI system needs a documented path from design to decommissioning. Currently, Cadre Corp lacks formal decommissioning procedures — that's a lifecycle gap I've identified and prioritized for the next governance sprint."