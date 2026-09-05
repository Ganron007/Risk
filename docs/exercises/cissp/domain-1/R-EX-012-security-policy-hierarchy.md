# R-EX-012 — Security policy hierarchy and development

**CISSP Reference:** Chapter 1, Section "Security Policy, Standards, Procedures, and Guidelines", Pages 126-129  
**Exam Objective:** 1.1.5 Develop and implement security policies, standards, procedures, and guidelines  
**Study Guide Key Terms:** Security policy, standards, procedures, guidelines, policy hierarchy, policy development lifecycle  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-appetite-statement.md`](../risk-appetite-statement.md), [`../control-register.md`](../control-register.md)

---

## Scenario Context

Cadre Corp has grown rapidly from a small DFIR consultancy to a mid-size firm with 45 employees and 120 enterprise clients. The company's security practices have evolved organically through tribal knowledge and individual analyst decisions rather than through formal documentation. As the company prepares for SOC 2 Type II audit and ISO 27001 certification, the lack of formal security policies has become a critical gap.

The CISO has been tasked with developing a comprehensive security policy hierarchy that will:
- Establish clear expectations for employee behavior
- Provide auditable evidence of security governance
- Support ISO 27001 Annex A control requirements
- Enable consistent security practices across the organization
- Scale as the company continues to grow

The current state includes:
- Ad-hoc password rules enforced by Active Directory
- Informal evidence handling procedures passed between DFIR analysts
- No formal incident response documentation
- Inconsistent access request processes
- No documented security roles and responsibilities

You need to design a policy hierarchy that addresses Cadre Corp's specific risks (client evidence compromise, identity plane attacks, research lab isolation) while remaining practical for a DFIR environment that requires operational agility.

---

## Multiple-Choice Questions

**Question 1:** In the context of Cadre Corp's ISO 27001 certification efforts, which of the following represents the correct hierarchy of security documentation from highest to lowest level of detail?

A. Guidelines → Standards → Procedures → Policies  
B. Policies → Standards → Procedures → Guidelines  
C. Procedures → Standards → Policies → Guidelines  
D. Standards → Policies → Guidelines → Procedures

**Question 2:** Cadre Corp needs to develop a policy specifically addressing client evidence handling. Which of the following would be the most appropriate title and classification for this document?

A. "Evidence Handling Guidelines" - Guideline document  
B. "Client Evidence Protection Policy" - Policy document  
C. "Forensic Evidence Procedures" - Procedure document  
D. "Chain of Custody Standard" - Standard document

**Question 3:** The CISO is concerned that overly prescriptive policies will hinder DFIR operational agility. Which of the following approaches best balances control requirements with operational flexibility?

A. Develop detailed procedures for every possible scenario  
B. Use policy for high-level requirements and guidelines for implementation flexibility  
C. Avoid formal policies and rely on analyst judgment  
D. Adopt industry-standard policies without customization

**Question 4:** When developing the incident response policy, which of the following elements must be included to satisfy ISO 27001 Annex A control A.16.1 (Management of information security incidents)?

A. Detailed technical containment procedures for every attack type  
B. Incident classification categories and reporting requirements  
C. List of all possible incident scenarios  
D. Contact information for every law enforcement agency globally

---

## Answer Explanations

**Answer 1: B**  
The correct hierarchy is Policies → Standards → Procedures → Guidelines. Policies are high-level statements of management intent and requirements. Standards provide specific technical requirements or configurations. Procedures provide step-by-step instructions for implementing standards. Guidelines offer recommended best practices and implementation suggestions. This hierarchy ensures clear governance while allowing implementation flexibility.

**Answer 2: B**  
"Client Evidence Protection Policy" as a Policy document is the most appropriate classification. A policy document sets the high-level requirement for protecting client evidence, establishes the business rationale (existential risk to Cadre Corp), and defines roles and responsibilities. Procedures would provide the step-by-step evidence handling steps, standards would specify technical requirements (e.g., encryption standards), and guidelines would offer best practices for evidence handling.

**Answer 3: B**  
Using policy for high-level requirements and guidelines for implementation flexibility best balances control and agility. Policies establish the "what" and "why" (e.g., "Client evidence must be protected with encryption at rest"), while guidelines provide the "how" with implementation options (e.g., "AES-256 encryption is recommended for evidence storage"). This approach satisfies audit requirements while allowing DFIR analysts to adapt to specific incident scenarios without policy violations.

**Answer 4: B**  
Incident classification categories and reporting requirements must be included to satisfy ISO 27001 A.16.1. The control requires a documented incident management process that includes incident classification, reporting procedures, and responsibility assignment. Detailed technical containment procedures (A) are too granular for a policy and belong in procedures. Lists of all possible scenarios (C) are impractical and not required. Contact information for every law enforcement agency (D) is unnecessary and should be in procedures or contact databases.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's policy development needs by:

1. **Policy Hierarchy Design:** Creating a structured approach to documentation that supports ISO 27001 certification and SOC 2 audit requirements
2. **Risk-Based Policies:** Developing policies that address Cadre Corp's specific risks (client evidence, identity plane, research labs)
3. **Operational Balance:** Designing policies that provide governance without hindering DFIR operational agility
4. **Audit Evidence:** Creating documentation that serves as auditable evidence for ISO 27001 and SOC 2

**Lab Connection:** After completing this exercise, you can:
- Review the existing risk appetite statement (`docs/risk-appetite-statement.md`) to inform policy requirements
- Examine the control register (`docs/control-register.md`) to identify which controls require policy support
- Consider how CISO Assistant could be used to track policy compliance and control implementation
- Map policies to ISO 27001 Annex A controls for certification preparation

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Policy Hierarchy Strategy:** "I design policy hierarchies that provide clear governance while allowing operational flexibility. Policies establish the 'what' and 'why,' standards define technical requirements, procedures provide step-by-step instructions, and guidelines offer implementation best practices."

2. **Risk-Based Policy Development:** "I prioritize policy development based on risk impact. For Cadre Corp, client evidence handling and identity security policies come first because these represent existential risks to the business. Research lab policies are secondary because the business impact is lower."

3. **Audit Alignment:** "I develop policies with audit requirements in mind. Each policy maps to specific ISO 27001 Annex A controls and SOC 2 Trust Services Criteria, ensuring our documentation serves as evidence of compliance rather than just administrative overhead."

4. **Operational Agility:** "In DFIR environments, overly prescriptive policies can hinder incident response. I use policies for high-level requirements and guidelines for implementation flexibility, allowing analysts to adapt to unique incident scenarios without violating policy."

5. **Policy Lifecycle:** "Policy development is not a one-time project. I establish a policy lifecycle that includes annual reviews, change management, and employee training. This ensures policies remain relevant as the business evolves and new threats emerge."

---

## Task

1. Design a policy hierarchy for Cadre Corp addressing the top 5 priority areas.
2. Draft a high-level policy statement for client evidence protection.
3. Explain how the policy hierarchy supports ISO 27001 Annex A controls.
4. Describe the policy development and maintenance lifecycle.

## Answer key

1. **Policy hierarchy for Cadre Corp (priority order):**
   - **Policy Level:**
     - Information Security Policy (overall governance)
     - Client Evidence Protection Policy (existential risk)
     - Identity and Access Management Policy (identity plane risk)
     - Incident Response Policy (operational continuity)
     - Acceptable Use Policy (employee behavior)
   
   - **Standard Level:**
     - Encryption Standards (evidence storage, transmission)
     - Access Control Standards (AD, cloud, lab isolation)
     - Authentication Standards (MFA, password complexity)
   
   - **Procedure Level:**
     - Evidence Handling Procedures (chain of custody, transfer)
     - Access Request Procedures (provisioning, deprovisioning)
     - Incident Response Procedures (classification, containment, reporting)
   
   - **Guideline Level:**
     - Evidence Encryption Guidelines (implementation options)
     - Secure Configuration Guidelines (endpoint hardening)
     - Remote Access Guidelines (VPN, secure connectivity)

2. **Client Evidence Protection Policy statement:**
   - "Cadre Corp shall protect all client forensic evidence from unauthorized access, modification, or destruction throughout its lifecycle. Evidence must be classified as Restricted, stored with encryption at rest using AES-256 or equivalent, transmitted using encrypted channels, and accessed only by authorized personnel with documented business need. All evidence handling must maintain chain of custody documentation to support legal proceedings and client requirements."

3. **ISO 27001 Annex A mapping:**
   - Information Security Policy → A.5.1 (Policies for information security)
   - Client Evidence Protection Policy → A.8 (Asset management), A.10 (Cryptography)
   - Identity and Access Management Policy → A.9 (Access control)
   - Incident Response Policy → A.16 (Information security incident management)
   - Acceptable Use Policy → A.7 (Human resources security)

4. **Policy lifecycle:**
   - **Development:** Risk assessment → stakeholder review → legal/compliance review → management approval
   - **Implementation:** Employee training → system configuration updates → compliance monitoring
   - **Maintenance:** Annual review → incident-driven updates → regulatory change updates
   - **Retirement:** Obsolescence assessment → replacement policy development → archival

**Pass criteria:** You can design a policy hierarchy that balances governance requirements with operational agility while supporting audit and certification objectives.
