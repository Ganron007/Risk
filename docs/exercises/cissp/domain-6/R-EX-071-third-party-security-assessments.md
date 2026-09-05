# R-EX-071 — Third-party security assessments

**CISSP Reference:** Chapter 15, Section "Building a Security Assessment Program"; Chapter 1, Section "Supply Chain Risk Management"  
**Exam Objective:** 6.1.1 Design assessment strategy; 1.7.1 Manage third-party risk  
**Study Guide Key Terms:** Third-party assessment, vendor risk assessment, SOC 2 report, ISO 27001 certificate, SIG questionnaire, right-to-audit  

---

## Scenario Context

Cadre Corp relies on 8 critical third parties: cloud backup provider (client evidence), M365/Entra ID (identity), LLM API providers (DarkAI, Praxis), Managed SOC provider (after-hours alert monitoring), and the colocation facility (physical lab hosting). The CISO has asked for third-party security assessments — but only 3 of the 8 vendors provided SOC 2 reports. Two vendors (LLM API providers) claim "our security is proprietary" and won't share assessment results. The colocation facility sent a 200-page SOC 2 report that nobody has read.

---

## Multiple-Choice Questions

**Question 1:** When a vendor provides a SOC 2 Type II report, what information does it contain?

A. A penetration test of the vendor's systems  
B. An auditor's opinion on the design (Type I) AND operating effectiveness over time (Type II) of the vendor's controls against the Trust Services Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy)  
C. A list of all vulnerabilities in the vendor's software  
D. A guarantee that the vendor will never be breached

**Question 2:** How should Cadre Corp handle vendors that refuse to share security assessment results?

A. Accept the risk and continue using them — they're major providers  
B. Conduct an independent assessment (questionnaire, evidence review, or on-site audit if the contract includes right-to-audit), and if the vendor still won't provide assurance, evaluate alternative vendors  
C. Report them to regulatory authorities  
D. Assume they're secure because they're large companies

**Question 3:** What is the appropriate cadence for reassessing third-party vendors?

A. Once, at onboarding — never again  
B. Risk-based: critical vendors (holding client data, providing identity) reassessed annually; lower-risk vendors every 2-3 years; plus event-driven reassessment after a vendor breach or major change  
C. Every month for all vendors  
D. Only when the contract is up for renewal

---

## Answer Explanations

**Answer 1: B**  
A **SOC 2 Type II report** provides an independent auditor's opinion on controls' operating effectiveness over a period (typically 6-12 months). Type I = design only (point in time). Type II = design + operating effectiveness (over time). For Cadre Corp's cloud backup provider, a Type II report covering the Security and Confidentiality criteria is the minimum expectation.

**Answer 2: B**  
If a vendor won't provide assurance, Cadre Corp must either: (a) exercise contractual right-to-audit, (b) accept the risk with executive sign-off (documented, reviewed periodically), or (c) find an alternative vendor. "They're a major provider" is not a risk treatment — it's risk denial. For LLM API providers processing client code (Praxis scenario), Cadre Corp must assess what data leaves its control and whether the provider's data processing terms are acceptable.

**Answer 3: B**  
Third-party assessment is **continuous, not one-time**. Critical vendors (cloud backup, Entra ID, colocation) = annual reassessment. Medium-risk = every 2 years. Event-driven = if the vendor has a breach, changes ownership, or significantly changes their service. The 200-page colocation SOC 2 report should be reviewed at least annually by someone qualified to assess it.

---

## Cadre Corp Application

1. **Vendor Risk Register:** Add a "Third-Party Risk" section to the risk register. Each critical vendor gets a risk entry with: services provided, data accessed, assessment status, last assessment date, next assessment due.

2. **LLM API Provider Assessment:** For Anthropic/OpenAI (used by Praxis/DarkAI): review data processing agreements, assess whether client code submitted for analysis could be used for model training, document the residual risk acceptance.

3. **SOC 2 Report Review:** Assign the 200-page colocation SOC 2 report to a qualified reviewer (GRC team member or external auditor). Key focus areas: physical security controls, environmental controls, access management. Document the review and any findings.

---

## Interview Talking Points

1. **Your Vendor's Breach Is Your Breach:** "When the cloud backup provider gets breached and client evidence is exposed, our clients don't sue the provider — they sue us. Third-party risk IS first-party risk. Vendor assessments aren't paperwork — they're due diligence."

2. **'Proprietary Security' Is Not an Answer:** "When an LLM API vendor says 'our security is proprietary' and won't share assessment results, that's a risk indicator — not a reassurance. If they process our clients' code, we need to know how. No transparency = no trust."
