# INT-EX-001 — Classic GRC + AI governance sync

**Platforms:** CISO Assistant + VerifyWise | **Time:** 20 min | **CISSP:** 1, 3

---

## Objective

Synchronize risk data between CISO Assistant (classic GRC) and VerifyWise (AI governance). Map AI-specific risks to the overarching enterprise risk register, ensuring unified risk visibility.

---

## Steps

### Step 1 — Map AI risks to enterprise risks
| VerifyWise AI Risk | CISO Assistant Enterprise Risk |
|-------------------|-------------------------------|
| RevAI prompt injection → malicious YARA rules | RISK-013 (Prompt injection / LLM abuse leaks lab secrets) |
| Model supply chain compromise | RISK-013 (broader supply chain risk) |
| AI finding accepted without HITL | RISK-018 (AI-generated forensic finding accepted without HITL) |

### Step 2 — Verify consistency
Check that the AI risks in VerifyWise and their enterprise counterparts in CISO Assistant have consistent:
- Severity scores (High in VerifyWise = score 6-9 in CISO Assistant)
- Risk owners (same person owns both views)
- Treatment status (mitigation status consistent across platforms)

### Step 3 — Document the mapping
Create a cross-reference document: `docs/grc-cross-reference.md` mapping every VerifyWise risk to its CISO Assistant counterpart. This is the Rosetta Stone for unified risk visibility.

---

## Interview Talking Points

1. **"AI risk IS enterprise risk":** "I don't manage AI risk in a separate universe. Every AI risk maps to an enterprise risk in CISO Assistant. The board sees a unified risk view. The AI governance platform is a specialized lens on the same risk landscape."