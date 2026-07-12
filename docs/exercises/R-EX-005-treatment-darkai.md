# R-EX-005 — Treatment: DarkAI lab risk

**CISSP skill:** Risk treatment  
**Inputs:** RISK-012/013, finding-darkai-001, appetite (moderate for research)

## Task

1. Choose Accept / Mitigate / Transfer / Avoid for finding-darkai-001.
2. List compensating controls required if Accept.
3. State the condition that would force Avoid (shut lab).

## Answer key

1. **Mitigate** (prompt injection + secret hygiene); residual research risk may be **Accept** only after fix.
2. CTL-LAB-ISOLATION, no AST-030 data, secret rotation, Praxis gate, disable STUB_INJECTABLE in shared demos.
3. Evidence of client data in `172.20.0.0/24` or bridge to `192.168.77.0/24` without capstone controls → **Avoid** until redesigned.

**Appetite:** Moderate for isolated research — not a blank check for secret leakage.
