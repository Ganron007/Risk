# INT-EX-002 — Multi-framework control mapping

**Platforms:** CISO Assistant + VerifyWise | **Time:** 20 min | **CISSP:** 1, 6

---

## Objective

Create a master control mapping that spans all five frameworks across both platforms: ISO 27001, SOC 2, NIST CSF, GDPR (CISO Assistant) + EU AI Act, ISO 42001, NIST AI RMF (VerifyWise). Demonstrate unified compliance visibility.

---

## Steps

### Step 1 — Create the master mapping
Pick CTL-HITL (Human-in-the-loop approval). Map it to ALL applicable frameworks:

| Framework | Control Reference | Platform |
|-----------|------------------|----------|
| ISO 27001 | A.9.4.2 (Secure log-on procedures) | CISO Assistant |
| SOC 2 | CC5.2 (Control Activities) | CISO Assistant |
| NIST CSF | PR.AC (Identity Management) | CISO Assistant |
| GDPR | Art. 32 (Security of processing) | CISO Assistant |
| EU AI Act | Art. 14 (Human oversight — High Risk AI) | VerifyWise |
| ISO 42001 | 8.2 (Human oversight of AI systems) | VerifyWise |
| NIST AI RMF | Govern 3.2 (Human oversight) | VerifyWise |

### Step 2 — Document the evidence chain
One control (CTL-HITL) → one implementation (DFIR-Nexus DRAFT → approve) → one evidence set (approval logs) → satisfies 7 framework requirements across 2 platforms.

### Step 3 — Calculate compliance leverage
"CTL-HITL costs one implementation but satisfies 7 framework requirements — a 7:1 compliance leverage ratio." This metric justifies GRC investment to the board.

---

## Interview Talking Points

1. **"One control, seven frameworks":** "I don't implement HITL seven different ways for seven different frameworks. I implement it once, document the evidence once, and map it to all seven. The auditor for each framework sees the same control, the same evidence, the same implementation. That's GRC efficiency."