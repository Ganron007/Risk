# VW-EX-006 — ISO 42001 framework mapping

**Platform:** VerifyWise  
**Time:** 20 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 6 (Assessment & Testing)

---

## Objective

Map Cadre Corp's AI governance controls to the ISO 42001 AI Management System framework in VerifyWise. Demonstrate how AI-specific controls satisfy the standard's requirements for AI system governance.

---

## Steps

### Step 1 — Understand ISO 42001 structure
ISO 42001 defines requirements for an AI Management System (AIMS):
- **Context:** Understanding the organization and its AI context
- **Leadership:** AI policy, roles, responsibilities
- **Planning:** AI risk assessment, AI impact assessment
- **Support:** Resources, competence, awareness, documentation
- **Operation:** AI system lifecycle management, AI risk treatment
- **Performance Evaluation:** Monitoring, internal audit, management review
- **Improvement:** Nonconformity, corrective action, continual improvement

### Step 2 — Map Cadre Corp's AI controls
Navigate to the ISO 42001 framework in VerifyWise. Map:

| ISO 42001 Clause | Cadre Corp Control |
|-----------------|-------------------|
| AI Policy (5.2) | `docs/enterprise-context.md` §AI governance + risk appetite statement |
| AI Risk Assessment (6.1) | VW-EX-005 risk assessments for RevAI, DarkAI, Praxis |
| AI System Inventory (8.1) | VW-EX-002 project registry + VW-EX-003 model inventory |
| AI Impact Assessment (6.1.2) | VW-EX-004 EU AI Act classification |
| Human Oversight (8.2) | CTL-HITL (DFIR-Nexus DRAFT → approve gate for RevAI outputs) |
| Monitoring & Measurement (9.1) | Model output monitoring, prompt injection detection, classification drift tracking |
| Internal Audit (9.2) | Quarterly AI risk review, annual model inventory audit |

### Step 3 — Identify gaps
Which ISO 42001 clauses have no Cadre Corp controls mapped? Document as the AI governance gap list:
- **Competence (7.2):** No formal AI ethics training program for developers
- **Documented Information (7.5):** AI policies not yet centralized in a single AIMS manual

### Step 4 — Generate ISO 42001 readiness report
Export the mapping as a readiness report. This demonstrates the gap between current state and ISO 42001 certification readiness.

---

## Verification Checklist

- [ ] ISO 42001 clauses mapped to Cadre Corp AI controls
- [ ] Gap list documented with 2+ identified gaps
- [ ] Readiness report exported

---

## Interview Talking Points

1. **"ISO 42001 is ISO 27001 for AI":** "The structure is the same Plan-Do-Check-Act cycle. If you understand ISO 27001, ISO 42001 is a domain-specific adaptation for AI systems. I've mapped our AI controls to it and identified the gaps — same methodology, different asset class."