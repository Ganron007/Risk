# CISO-EX-002 — Risk scenario creation workflow

**Platform:** CISO Assistant Community Edition  
**Time:** 25 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 6 (Assessment & Testing)  
**Prerequisites:** CISO-EX-001 completed, PAT available, Cadre Corp domain created

---

## Objective

Create risk scenarios in CISO Assistant for three of Cadre Corp's top risks (RISK-001 DCSync, RISK-002 ADCS ESC, RISK-007 Client evidence breach), apply the 5x5 ISO-27005 matrix, and assign treatment plans. This demonstrates the core GRC workflow: identify → assess → treat → monitor.

---

## Steps

### Step 1 — Create RISK-001: Domain Admin compromise via DCSync
1. Navigate to **Risk** → **Create Risk Scenario**.
2. Fill in:
   - **Name:** `RISK-001 — Domain Admin compromise via DCSync`
   - **Description:** Authenticated replication abuse after privilege escalation. DCSync allows attacker to harvest password hashes for all domain accounts including KRBTGT, enabling Golden Ticket forgery and full domain takeover.
   - **Domain:** Cadre Corp
   - **Risk Matrix:** 5x5 ISO-27005
   - **Likelihood:** 3 (High — documented in campaign exercises, multiple tools available)
   - **Impact:** 3 (Critical — full domain compromise, client evidence at risk)
   - **Treatment:** Mitigate
   - **Owner:** Infra Lead
3. Save.

### Step 2 — Create RISK-002: ADCS ESC abuse
1. **Name:** `RISK-002 — ADCS ESC abuse → authentication as privileged user`
2. **Description:** ESC1 (enrollee supplies subject) allows low-privilege users to request certificates for privileged accounts. Combined with ESC8 (NTLM relay to ADCS web enrollment), multiple paths to certificate-based domain privilege escalation exist.
3. **Likelihood:** 3 | **Impact:** 3 | **Treatment:** Mitigate | **Owner:** Infra Lead

### Step 3 — Create RISK-007: Client evidence breach
1. **Name:** `RISK-007 — Client forensic evidence breach / CoC failure`
2. **Description:** Unauthorized access to or tampering with client forensic evidence. Could result from: compromised analyst workstation, insider threat, ransomware on evidence share, or chain-of-custody documentation failure. Breach is existential per risk appetite.
3. **Likelihood:** 2 (Medium — multiple controls in place) | **Impact:** 3 (Critical) | **Treatment:** Mitigate | **Owner:** DFIR Lead

### Step 4 — Seed the remaining baseline risks via REST API
```powershell
.\scripts\ciso-seed-baseline.ps1 -Token "<your-pat>"
```
This script creates the remaining 15 risks (RISK-003 through RISK-018) from `docs/risk-register-baseline.md` via the REST API. Verify the count: you should now have 18 risk scenarios.

### Step 5 — Verify in UI
1. Navigate to **Risk** → **Risk Scenarios**.
2. Confirm all 18 risks are listed with correct likelihood, impact, and treatment.
3. Filter by treatment "Mitigate" — you should see 16 risks.
4. Filter by score (9 = Critical) — you should see RISK-001, RISK-002, RISK-004.

---

## Verification Checklist

- [ ] RISK-001, 002, 007 manually created with correct scores and treatments
- [ ] `ciso-seed-baseline.ps1` executed successfully — 18 total risks
- [ ] Risk matrix correctly calculates score from likelihood × impact
- [ ] Filtering and sorting work in the UI

---

## CISSP Connection

**Domain 1:** This is the practical implementation of qualitative risk analysis (likelihood × impact matrix). The CISSP exam tests your understanding of the matrix; this exercise proves you can operationalize it in a GRC tool.

**Domain 6:** Risk assessment is an ongoing assessment activity. The baseline risks from the campaign exercises demonstrate that security testing findings flow into the risk register — closing the loop between detection and governance.

---

## Interview Talking Points

1. **"I don't just list risks — I operationalize them":** "Cadre Corp's risk register lives in CISO Assistant with a 5x5 ISO-27005 matrix. Every risk has an owner, a treatment, and a score. The register isn't a static document — it's a living system that ingests findings from our security tools via REST API."

2. **"The matrix is traceable to real attacks":** "RISK-001 (DCSync) isn't theoretical. We validated it in our campaign exercises — the attack path works. The risk score of 9 reflects that validated exploitability, not a guess."