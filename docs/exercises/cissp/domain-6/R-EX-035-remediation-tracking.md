# R-EX-035 — Remediation tracking and Definition of Done

**CISSP Reference:** Chapter 15, Section "Collecting Security Process Data"; Chapter 16, Section "Patch Management and Vulnerability Reduction"  
**Exam Objective:** 6.2.3 Track remediation; 7.1.3 Manage vulnerability remediation  
**Study Guide Key Terms:** Remediation tracking, Definition of Done (DoD), vulnerability lifecycle, risk acceptance, residual risk, compensating control, SLAs by severity  
**Inputs:** [`../risk-register-baseline.md`](../risk-register-baseline.md), RISK-001, `samples/findings/`

---

## Scenario Context

Cadre Corp's risk register documents RISK-001 (Domain Admin compromise via DCSync) as score 9 (Critical). A recent campaign exercise confirmed the attack path is exploitable: the attacker used Kerberoast → DCSync → extracted KRBTGT hash in under 4 hours.

The CISO has directed remediation. The Infra Lead proposed three actions:

1. Deploy a SIEM detection rule for Event ID 4662 with DRSUAPI GUID (completed — rule `cadre-002` now fires on DCSync).
2. Implement AD tiered administration (Tier 0 for DCs, Tier 1 for servers, Tier 2 for workstations) — partially completed: Tier 0 accounts created, but no privileged access workstations deployed.
3. Enable `Protected Users` group membership for all Domain Admins — proposed but not yet started.

The CISO asks: "Is RISK-001 closed?" The Infra Lead says: "We did the detection rule." The CISO counters: "The attacker can still DCSync. Detection is not remediation." You need to define the Definition of Done for closing RISK-001.

---

## Multiple-Choice Questions

**Question 1:** What is the correct Definition of Done (DoD) for closing a critical risk like RISK-001?

A. At least one mitigating action has been implemented — even if the attack path still exists  
B. The risk has been reduced to an acceptable residual level per the risk appetite statement — for a score 9 risk with low appetite (client evidence at stake), this means the attack path is demonstrably CLOSED or reduced to a level where the residual risk is acceptable with documented compensating controls  
C. The detection rule fires correctly  
D. The risk register entry has been updated with any status

**Question 2:** The SIEM detection rule for DCSync (`cadre-002`) is:

A. Remediation — the risk is now closed  
B. A detective control — it tells you when DCSync happens but does NOT prevent it; the attack path remains open; detection reduces dwell time but does not reduce likelihood or impact  
C. Irrelevant to risk management  
D. A preventative control that blocks DCSync

**Question 3:** When remediation is partially complete (Tier 0 accounts created, but privileged access workstations not deployed), the appropriate risk register status is:

A. Closed — partial remediation is sufficient  
B. In Progress — with documented residual risk: "Tier 0 accounts reduce credential exposure, but without PAWs, Domain Admins still log into Tier 2 workstations (where they can be credential-dumped). Residual risk: High. Target closure: [date]."  
C. Open — partial work doesn't count as any progress  
D. Transferred — the risk is now the infra team's problem

**Question 4:** If RISK-001 cannot be fully remediated within the target timeframe (e.g., PAW deployment delayed by budget), what is the appropriate risk management action?

A. Close the risk anyway — you tried  
B. Document a formal risk acceptance for the residual risk: "RISK-001 partially mitigated: detection rule deployed (reduces dwell time), Tier 0 accounts created (reduces exposure). Residual risk: DA credentials still cacheable on Tier 2 workstations. Acceptance rationale: PAW deployment delayed to Q2 2027 per budget. Acceptance expires: [date]. Accepted by: CISO."  
C. Escalate to the board immediately without documenting the partial mitigation  
D. Remove the risk from the register since it can't be fully fixed

---

## Answer Explanations

**Answer 1: B**  
The DoD for risk closure is **residual risk reduced to acceptable level per risk appetite**. For RISK-001 (score 9, low appetite), "acceptable" means the attack path is closed or sufficiently obstructed that the residual risk is manageable. Detection alone (C) doesn't close the risk — the attacker can still DCSync, you just know about it faster. The DoD must be defined BEFORE remediation begins — agreed between risk owner and CISO — so everyone knows what "done" looks like.

**Answer 2: B**  
The detection rule is a **detective control** — it improves MTTD (Mean Time to Detect) but does not reduce likelihood (the attack still works) or impact (the attacker still gets all hashes). Detective controls are valuable — they reduce dwell time — but they don't remediate the vulnerability. RISK-001 requires preventative controls (AD tiering, Protected Users, PAWs) to reduce likelihood, not just faster detection.

**Answer 3: B**  
**In Progress with documented residual risk** is the honest and useful status. "Tier 0 accounts created" is real progress — it reduces the attack surface. But "without PAWs, DAs still log into compromisable workstations" is the honest residual risk assessment. This status: (a) acknowledges progress, (b) identifies what's still exposed, (c) sets a target closure date, (d) enables the CISO to make informed decisions about resource allocation. Closing prematurely (A) hides risk. "Doesn't count" (C) demotivates the team and hides real risk reduction.

**Answer 4: B**  
**Formal risk acceptance with expiration** is the correct approach when remediation is delayed by legitimate constraints. The acceptance documents: (a) what's been done (partial mitigation — detection + Tier 0), (b) what's still exposed (DA credential caching on workstations), (c) why full remediation is delayed (budget, not neglect), (d) when acceptance expires (forces re-evaluation, prevents "temporary" becoming "permanent"), (e) who accepted it (accountability). Close anyway (A) is dishonest. Escalate immediately (C) may be disproportionate if the CISO agrees with the acceptance. Remove from register (D) hides the risk.

---

## Cadre Corp Application

1. **DoD Template:** For every risk in the register, define DoD at creation time: (a) what conditions must be true for the risk to be considered "Closed"? (b) what's the minimum acceptable reduction in score? (c) what evidence demonstrates closure? Example for RISK-001: "DoD = (a) AD tiered administration fully deployed, (b) Protected Users group contains all Tier 0 accounts, (c) PAWs deployed for all Tier 0 admin activities, (d) detection rule validated (confirming preventative controls work), (e) campaign re-test confirms DCSync blocked or detected within 5 minutes."

2. **Remediation Tracking Board:** Add a remediation tracking view (spreadsheet or dashboard) showing: risk ID, current score, target score, remediation actions (with % complete), residual risk description, next milestone date, and owner. Review weekly at the security standup.

3. **Partial Credit Is Real Risk Reduction:** Don't mark risks as "Open — no progress" when partial work has been done. "Tier 0 accounts created" reduces the attack surface — it's not complete, but it's not zero. Document the reduced residual risk so leadership sees progress, not stagnation.

---

## Interview Talking Points

1. **Detection Is Not Remediation:** "A SIEM rule that tells you DCSync happened is not the same as preventing DCSync. Detection reduces dwell time; remediation reduces likelihood. You need both. Don't close a risk because you can detect the attack — close it when the attack can't succeed."

2. **Define Done Before You Start:** "Every risk needs a Definition of Done written at creation — not discovered during the 'is it done yet?' argument. The DoD is the contract between the risk owner and the CISO: 'When X, Y, and Z are true, this risk is closed.' Without it, risks drift in 'In Progress' purgatory forever."

3. **Acceptance Is a Valid Outcome — With an Expiration Date:** "Not every risk can be fully remediated on the ideal timeline. A formal risk acceptance with: (a) documented residual risk, (b) compensating controls, (c) expiration date, and (d) named approver — that's professional risk management. Pretending the risk is closed because you can't fix it is professional negligence."
