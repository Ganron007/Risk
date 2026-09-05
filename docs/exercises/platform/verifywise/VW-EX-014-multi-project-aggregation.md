# VW-EX-014 — Multi-project AI risk aggregation

**Platform:** VerifyWise | **Time:** 15 min | **CISSP:** 1, 2

---

## Objective

Aggregate AI risks across all three Cadre Corp projects into an enterprise AI risk view. Identify cross-project patterns and systemic AI risks.

---

## Steps

### Step 1 — Aggregate risks across projects
Query VerifyWise for all AI risks across DarkAI, RevAI, and Praxis. Common patterns:
- **Prompt injection risk:** Present in all 3 projects (any LLM-integrated system)
- **API key exposure:** DarkAI + Praxis (both call external LLM APIs)
- **Output integrity:** RevAI + Praxis (both generate operational outputs)

### Step 2 — Identify systemic risks
Systemic = a risk that exists across multiple projects due to shared architecture or dependencies:
- **Shared LLM provider dependency:** 2 of 3 projects use Anthropic API — provider outage or compromise affects multiple systems
- **Shared HITL dependency:** All 3 projects rely on the same DFIR-Nexus HITL workflow — if Nexus is down, all AI HITL gates are unavailable

### Step 3 — Create enterprise AI risk register
Document systemic risks in VerifyWise at the organization level (not project-specific). These risks require enterprise-level mitigations: multi-provider LLM strategy, HITL high-availability deployment.

---

## Interview Talking Points

1. **"Systemic AI risks transcend individual projects":** "Prompt injection isn't just a RevAI problem — it affects every LLM-integrated system we run. The enterprise AI risk view identifies these cross-cutting risks and drives organization-wide mitigations, not project-by-project band-aids."