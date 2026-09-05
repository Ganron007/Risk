# R-EX-034 — SOC 2 Type II audit preparation

**CISSP Reference:** Chapter 15, Sections "Security Management Processes", "Audit Readiness"; Chapter 1, Section "Security Governance"  
**Exam Objective:** 6.2.1 Conduct security audits; 6.2.2 Prepare for external assessment  
**Study Guide Key Terms:** SOC 2 Type II, Trust Services Criteria (TSC), audit evidence, control mapping, management assertion, qualified opinion, audit readiness  
**Inputs:** [`../control-register.md`](../control-register.md), [`../risk-register-baseline.md`](../risk-register-baseline.md), [`../enterprise-context.md`](../enterprise-context.md)

---

## Scenario Context

Cadre Corp's SOC 2 Type II audit is 30 days away. The audit scope covers the Trust Services Criteria most relevant to a DFIR services firm: **Security** (mandatory), **Confidentiality** (client evidence protection), and **Availability** (SOC monitoring uptime). The auditor will test controls for DESIGN (do they exist?) and OPERATING EFFECTIVENESS (have they worked consistently over the audit period — typically 6-12 months?).

The CISO is preparing the management assertion — the formal statement that Cadre Corp's controls meet the criteria. However, during a pre-audit readiness review, three issues emerged:

1. **Control CTL-SIEM-IDENTITY** (SIEM detection for identity attacks) has great documentation but only 3 months of operational evidence — the Elastic rules were deployed 3 months ago, not 6. This may not meet the Type II operating effectiveness period.

2. **Control CTL-EVIDENCE-ACCESS** (evidence access controls) has strong design documentation but inconsistent operating evidence — some months have access review logs, others are missing. The DFIR Lead says "we did the reviews, we just forgot to save the evidence."

3. **Control CTL-HITL** (human-in-the-loop approval) has excellent evidence — DFIR-Nexus cryptographic approval logs for every finding — but only for the DFIR-Nexus tool. Manual forensic findings outside Nexus have no HITL evidence.

---

## Multiple-Choice Questions

**Question 1:** What is the PRIMARY difference between SOC 2 Type I and Type II reports?

A. Type I is for security; Type II is for confidentiality  
B. Type I assesses control DESIGN at a point in time; Type II assesses design AND OPERATING EFFECTIVENESS over a period (typically 6-12 months)  
C. Type I requires more evidence than Type II  
D. Type II does not require on-site auditor visits

**Question 2:** CTL-SIEM-IDENTITY only has 3 months of operating evidence for a 6-month audit period. What is the appropriate response?

A. Claim 6 months anyway — the auditor won't check  
B. Document the control as "in place for 3 of 6 months" — the auditor will note this as a control gap (shorter operating period than required) but it's not a complete failure; the finding will be that the control operated effectively for the period it was in place, with a recommendation to extend the evidence period for the next audit  
C. Remove the control from scope entirely  
D. Backdate the evidence to cover 6 months

**Question 3:** CTL-EVIDENCE-ACCESS has inconsistent evidence ("we did the reviews, forgot to save evidence"). Under SOC 2, this is:

A. Acceptable — verbal confirmation is sufficient evidence  
B. A control operating effectiveness failure — if you can't PROVE the control operated (with dated, documented evidence), it didn't operate as far as the auditor is concerned; "we did it but forgot to save evidence" is indistinguishable from "we didn't do it"  
C. A minor documentation issue with no impact on the audit opinion  
D. Only relevant for Type I, not Type II

**Question 4:** What is the correct approach for CTL-HITL evidence that exists for DFIR-Nexus but not for manual forensic findings?

A. Claim HITL applies to all findings — the auditor won't check manual processes  
B. Scope the control honestly: "CTL-HITL is implemented for DFIR-Nexus automated findings (100% coverage). Manual forensic findings use a peer review process (CTL-PEER-REVIEW) which is a separate compensating control." — be precise about what's covered and what's covered differently  
C. Stop using manual forensic processes entirely  
D. Remove HITL from the control register

---

## Answer Explanations

**Answer 1: B**  
**Type I = design at a point in time. Type II = design + operating effectiveness over time.** For Cadre Corp, the auditor will test: (a) is the control designed appropriately? (does the policy make sense?), AND (b) did the control actually work for the entire audit period? (is there evidence it was followed every month?). Type II is what clients and regulators rely upon. The "over time" requirement is why missing months of evidence matter.

**Answer 2: B**  
**Document the actual operating period honestly.** The auditor WILL check — claiming 6 months when evidence only covers 3 is misrepresentation. The correct approach: present the 3 months as "control implemented [date], operating effectively since implementation." The finding is that the control wasn't in place for the full audit period — a gap, but less severe than a control that was in place but FAILED to operate. For the next audit, the control will have 12+ months of evidence.

**Answer 3: B**  
**"We did it but can't prove it" = control failure in an audit context.** SOC 2 requires evidence — dated, documented, retrievable. If the access review happened but wasn't documented, the auditor cannot verify it. The auditor's standard: "I need to see evidence." The DFIR Lead's assurance is not evidence. This is a common failure mode: the control operated but the evidence process failed. Fix: automate evidence collection so it's generated as a byproduct of the control operation, not a separate "remember to save" step.

**Answer 4: B**  
**Scope precisely, not aspirationally.** Don't claim "HITL on all findings" if only Nexus findings are covered. Instead: describe what IS covered (Nexus automated findings — 100% HITL), what's covered DIFFERENTLY (manual findings — peer review), and note the gap (manual findings don't have cryptographic HITL but have a compensating control). Auditors respect precision and honesty. Over-claiming and being corrected is worse than accurate scoping with documented compensating controls.

---

## Cadre Corp Application

1. **Pre-Audit Evidence Review:** For each in-scope control: (a) verify evidence exists for EVERY month of the audit period, (b) verify evidence is dated, named, and retrievable, (c) identify gaps and document honestly, (d) prepare the management assertion with gap disclosures.

2. **Evidence Automation:** For CTL-EVIDENCE-ACCESS and similar controls, automate evidence generation: scheduled PowerShell scripts that dump access review results to a dated log file, or Elastic dashboards that capture monthly snapshots as PDF evidence. Evidence that generates itself can't be "forgotten."

3. **Control Scope Accuracy:** Review every control in `docs/control-register.md` and verify the scope description is accurate. If a control covers "some but not all" of what it claims, narrow the scope or broaden the implementation — but don't leave the scope statement aspirational.

---

## Interview Talking Points

1. **Evidence Is the Product, Not the Afterthought:** "In a SOC 2 audit, the control you can't prove operated is a control you didn't have. 'We did the monthly access review but forgot to save the evidence' is the same as 'we didn't do it' to an auditor. Evidence must be generated automatically as a byproduct of the control — not as a separate documentation task someone remembers."

2. **Three Months of Evidence Is Three Months, Not Six:** "Never over-claim your operating period. If a control has been running for 3 months, say 3 months. The auditor will find the truth. The finding will be 'shorter operating period than required' — not 'management misrepresented evidence.' The former is a maturity gap; the latter is an integrity finding."

3. **Scope Honestly:** "If HITL applies to Nexus findings but not manual ones, say so. Auditors respect accurate scoping with documented compensating controls more than aspirational scoping that collapses under testing. 'We do HITL for 80% of findings and peer review for 20%' is a defensible answer. 'We do HITL for everything' — when you don't — is not."
