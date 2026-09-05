# R-EX-006 — Framework mapping

**CISSP Reference:** Chapter 1, Section "Evaluate and Apply Security Governance Principles", Pages 106-109  
**Exam Objective:** 1.1.4 Map security controls to multiple frameworks  
**Study Guide Key Terms:** Framework alignment, NIST CSF, ISO 27001, Statement of Applicability (SoA), control mapping, residual risk  
**Inputs:** [`../control-register.md`](../control-register.md), [`../regulatory-obligations.md`](../regulatory-obligations.md)

---

## Scenario Context

Cadre Corp is pursuing ISO 27001 certification while also demonstrating alignment with NIST CSF for US-based clients. The company has documented its security controls in the control register (`docs/control-register.md`), which maps CADRE capabilities to both frameworks.

The control register includes:
- CTL-HITL: Human-in-the-loop approval for critical operations
- CTL-COC: Chain-of-custody documentation for evidence handling
- CTL-SIEM-IDENTITY: SIEM detection rules for identity attacks (DCSync, Kerberoasting)
- CTL-LAB-ISOLATION: Network isolation for research labs (DarkAI, RevAI, Praxis)

The ISO 27001 certification process requires a Statement of Applicability (SoA) that documents which controls from Annex A are implemented, which are partially implemented, and which are not applicable. Cadre Corp faces a unique challenge: the lab environment intentionally contains vulnerabilities (e.g., DCSync, ADCS ESC) for training purposes, which must be properly scoped in the SoA.

As the Risk Manager, you need to map these controls to NIST CSF functions and ISO 27001 Annex A controls, and explain how intentional lab vulnerabilities should be documented in the SoA.

---

## Multiple-Choice Questions

**Question 1:** Which of the following NIST CSF functions best describes CTL-HITL (Human-in-the-loop approval for critical operations)?

A. Detect (DE)  
B. Respond (RS)  
C. Protect (PR)  
D. Recover (RC)

**Question 2:** CTL-SIEM-IDENTITY (SIEM detection rules for identity attacks) maps to which NIST CSF function and sub-category?

A. Protect - Access Control (PR.AC)  
B. Detect - Anomalous Activity (DE.AE)  
C. Respond - Mitigation (RS.MI)  
D. Identify - Risk Assessment (ID.RA)

**Question 3:** When mapping CTL-LAB-ISOLATION to ISO 27001 Annex A, which control area is most appropriate?

A. A.5 (Information security policies)  
B. A.8 (Asset management)  
C. A.12 (Operations security)  
D. A.14 (System acquisition)

**Question 4:** In the ISO 27001 Statement of Applicability (SoA), how should intentional AD vulnerabilities in the lab environment be documented?

A. Marked as "not applicable" because they're in the lab  
B. Marked as "implemented" because they're part of the training environment  
C. Marked as "accepted residual risk for training" with clear scoping from production  
D. Omitted entirely from the SoA

---

## Answer Explanations

**Answer 1: C**  
Protect (PR) is the correct NIST CSF function for CTL-HITL. Human-in-the-loop approval is a preventive control that protects against unauthorized or incorrect actions by requiring human verification before critical operations execute. The Protect function focuses on developing and implementing appropriate safeguards to ensure delivery of critical services. Detect (A) is for identifying anomalies, Respond (B) is for incident response, and Recover (D) is for restoration activities.

**Answer 2: B**  
Detect - Anomalous Activity (DE.AE) is the correct mapping for CTL-SIEM-IDENTITY. SIEM detection rules for identity attacks are designed to detect anomalous activity (DCSync, Kerberoasting) that may indicate compromise. The Detect function focuses on identifying the occurrence of a cybersecurity event. Protect (A) would be for preventive controls like access restrictions. Respond (C) is for taking action after detection. Identify (D) is for understanding the business context and risk assessment.

**Answer 3: C**  
A.12 (Operations security) is the most appropriate ISO 27001 control area for CTL-LAB-ISOLATION. Network isolation for labs falls under operations security, specifically A.12.6 (Technical vulnerability management) or related controls on segregation of duties and network security. A.5 (A) is for policies, not technical controls. A.8 (B) is for asset classification and handling. A.14 (D) is for system development and acquisition.

**Answer 4: C**  
Marked as "accepted residual risk for training" with clear scoping from production is the correct approach. The SoA should document that production-equivalent controls are implemented for client-facing systems, while lab attack surfaces are accepted residual risk specifically scoped for training purposes. This transparency is required for ISO 27001 certification. Marking as "not applicable" (A) is incorrect because the lab is part of the certified scope. Marking as "implemented" (B) is misleading because the vulnerabilities are intentional. Omitting entirely (D) would violate ISO 27001 documentation requirements.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's compliance efforts by:

1. **Framework Mapping:** Understanding how to map technical controls to NIST CSF and ISO 27001
2. **SoA Documentation:** Learning how to properly document intentional vulnerabilities in certification scope
3. **Lab vs. Production Scoping:** Distinguishing between training environments and production systems
4. **Control Categorization:** Understanding the difference between Detect and Protect functions

**Lab Connection:** After completing this exercise, you can:
- Review the control register (`docs/control-register.md`) to see how CADRE capabilities map to frameworks
- Examine the regulatory obligations document (`docs/regulatory-obligations.md`) for ISO 27001 requirements
- Consider how CISO Assistant could track control implementation across multiple frameworks
- Evaluate the lab isolation architecture in the CADRE environment

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Framework Mapping Strategy:** "I map technical controls to multiple frameworks to support diverse client requirements. For Cadre Corp, I map our controls to both NIST CSF for US clients and ISO 27001 for global certification. This dual mapping demonstrates comprehensive security governance while avoiding redundant documentation."

2. **Detect vs. Protect Distinction:** "I clearly distinguish between Detect and Protect functions when mapping controls. SIEM detection rules for identity attacks are Detect (DE.AE) because they identify anomalous activity, while human-in-the-loop approval is Protect (PR.IP) because it prevents unauthorized actions. This distinction is critical for accurate framework alignment."

3. **SoA Transparency:** "In the ISO 27001 Statement of Applicability, I document intentional lab vulnerabilities as 'accepted residual risk for training' with clear scoping from production. This transparency is required for certification and demonstrates that we understand and accept the risk for legitimate business purposes."

4. **Lab vs. Production Scoping:** "I maintain clear separation between training environments and production systems in compliance documentation. Lab vulnerabilities are scoped as training tools with compensating controls (network isolation), while production systems have full control implementation. This scoping is essential for audit readiness."

5. **Control Register Value:** "The control register serves as the single source of truth for framework mapping. By documenting each control once and mapping it to multiple frameworks, we reduce documentation burden while ensuring consistency across NIST CSF, ISO 27001, and SOC 2 requirements."

---

## Task

1. Map CTL-HITL, CTL-COC, CTL-SIEM-IDENTITY, CTL-LAB-ISOLATION to NIST CSF functions.
2. Pick one ISO 27001 control for each.
3. Explain how intentional AD vulnerabilities in the lab should appear in an SoA.

## Answer key

1. HITL→PR.IP; COC→PR.IP; SIEM-IDENTITY→DE.AE; LAB-ISOLATION→PR.PT (or PR.AC).
2. Examples: A.5.37, A.5.33, A.8.15, A.8.22 (approx — memorize concepts not exact clause numbers for CISSP).
3. SoA should mark production-equivalent controls as **implemented**; lab attack surfaces as **accepted residual risk for training**, scoped out of production client estates.

**Pass criteria:** You can explain Detect vs Protect without conflating them.
