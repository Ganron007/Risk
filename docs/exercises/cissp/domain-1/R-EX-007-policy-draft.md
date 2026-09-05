# R-EX-007 — Information security policy draft

**CISSP Reference:** Chapter 1, Section "Security Policy, Standards, Procedures, and Guidelines", Pages 126-129  
**Exam Objective:** 1.1.5 Develop and implement security policies, standards, procedures, and guidelines  
**Study Guide Key Terms:** Security policy, policy development, policy scope, roles and responsibilities, acceptable use, enforcement, exceptions  
**Inputs:** [`../risk-appetite-statement.md`](../risk-appetite-statement.md), [`../enterprise-context.md`](../enterprise-context.md), [`../regulatory-obligations.md`](../regulatory-obligations.md)

---

## Scenario Context

Cadre Corp is preparing for its first formal SOC 2 Type II audit and ISO 27001 certification. The auditors have requested a comprehensive Information Security Policy that documents the organization's security governance structure, acceptable use guidelines, and enforcement mechanisms.

The current state includes:
- Informal security practices based on tribal knowledge
- No formal policy document
- Ad-hoc lab access procedures
- Inconsistent evidence handling practices
- No documented exception process

The CISO has requested a one-page policy outline that addresses Cadre Corp's specific context:
- DFIR services firm handling sensitive client evidence
- Research labs (DarkAI, RevAI, Praxis) for security testing
- Mixed environment: on-premises AD estate + cloud resources (Entra ID, Azure)
- Regulatory requirements: SOC 2, GDPR, ISO 27001
- Risk appetite: Low for client evidence, moderate for research labs

The policy must be practical for DFIR operations while satisfying audit requirements.

---

## Multiple-Choice Questions

**Question 1:** Which of the following is the most appropriate purpose statement for Cadre Corp's Information Security Policy?

A. To ensure all employees follow security best practices  
B. To protect client trust and comply with SOC 2 Type II and GDPR requirements  
C. To prevent all security incidents from occurring  
D. To satisfy ISO 27001 certification requirements

**Question 2:** When defining the scope of the policy, which of the following should be included?

A. Only production systems, not research labs  
B. Only cloud resources, not on-premises systems  
C. All Cadre Corp staff, contractors, and CADRE lab environments  
D. Only DFIR analysts, not administrative staff

**Question 3:** For the "Acceptable use of labs" section, which of the following is the most appropriate guideline for DarkAI and RevAI?

A. Labs are open for any research purposes without restrictions  
B. Labs are isolated on separate networks, cannot access client evidence, and require CI for shared applications  
C. Labs can be used for personal projects with manager approval  
D. Labs are only accessible during business hours

**Question 4:** When documenting the exception process, which of the following is the most appropriate approach?

A. No exceptions allowed under any circumstances  
B. Exceptions are automatically approved by the requester's manager  
C. Exceptions are time-boxed, require CISO approval, and must be logged for audit purposes  
D. Exceptions are documented after they occur

---

## Answer Explanations

**Answer 1: B**  
"To protect client trust and comply with SOC 2 Type II and GDPR requirements" is the most appropriate purpose statement. It addresses the business rationale (protecting client trust) and the specific regulatory requirements (SOC 2, GDPR) that drive the policy. Option A is too generic and doesn't address Cadre Corp's specific context. Option C is unrealistic—no policy can prevent all incidents. Option D focuses only on ISO 27001, missing the broader business and regulatory context.

**Answer 2: C**  
All Cadre Corp staff, contractors, and CADRE lab environments should be included in the scope. The policy must cover all personnel who have access to systems and data, including contractors. The lab environments are part of the certified scope and must be included. Options A and B are incorrect because they exclude significant parts of the environment. Option D is incorrect because administrative staff also have access to systems and must follow security policies.

**Answer 3: B**  
"Labs are isolated on separate networks, cannot access client evidence, and require CI for shared applications" is the most appropriate guideline. This addresses the specific security requirements for Cadre Corp's research labs: network isolation (prevent lab breakout), no client evidence access (protect Restricted data), and CI/CD requirements for shared applications (prevent supply chain compromise). Option A is incorrect because unrestricted labs pose unacceptable risk. Option C is incorrect because personal projects are not appropriate for corporate labs. Option D is insufficient because time restrictions don't address the core security requirements.

**Answer 4: C**  
Exceptions are time-boxed, require CISO approval, and must be logged for audit purposes is the most appropriate approach. This provides a structured process for legitimate exceptions while maintaining security oversight and audit trail. Time-boxing ensures exceptions don't become permanent. CISO approval ensures appropriate risk assessment. Logging provides audit evidence. Option A is impractical—some exceptions are necessary for business operations. Option B is insufficient because manager approval doesn't provide security oversight. Option D is incorrect because exceptions must be approved before they occur, not documented after.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's policy development by:

1. **Policy Structure:** Learning the essential sections of an information security policy
2. **DFIR-Specific Requirements:** Addressing lab isolation, evidence handling, and AI-assisted findings
3. **Regulatory Alignment:** Ensuring the policy supports SOC 2, GDPR, and ISO 27001 requirements
4. **Practical Enforcement:** Designing enforcement mechanisms that work for DFIR operations

**Lab Connection:** After completing this exercise, you can:
- Review the risk appetite statement (`docs/risk-appetite-statement.md`) to inform policy requirements
- Examine the enterprise context (`docs/enterprise-context.md`) to understand the environment
- Consider how the policy could be implemented in the CADRE lab environment
- Evaluate how CISO Assistant could track policy compliance and exceptions

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Policy Purpose-Driven Development:** "I develop policies with clear business purpose, not just to satisfy audits. For Cadre Corp, the Information Security Policy purpose is to protect client trust and comply with SOC 2 and GDPR. This business focus ensures the policy is meaningful rather than administrative overhead."

2. **Comprehensive Scope Definition:** "I define policy scope broadly to cover all personnel and environments. For Cadre Corp, this includes all staff, contractors, and CADRE lab environments. Excluding labs from scope would create audit gaps and security blind spots."

3. **DFIR-Specific Guidelines:** "I tailor policy guidelines to the specific business context. For our research labs, the policy requires network isolation, no client evidence access, and CI for shared applications. These specific guidelines address our unique risk profile rather than generic security best practices."

4. **Structured Exception Process:** "I establish a structured exception process that balances operational flexibility with security oversight. Exceptions are time-boxed, require CISO approval, and are logged for audit purposes. This process allows legitimate business needs while maintaining security governance."

5. **Enforcement with Business Impact:** "I design enforcement mechanisms that consider business impact. For critical violations (e.g., client evidence compromise), the board is notified because it represents existential business risk. For minor violations, HR handles it through standard performance processes. This tiered approach ensures proportionate response."

---

## Task

Write a one-page policy outline with sections: Purpose, Scope, Roles, Acceptable use of labs, Evidence handling, Exceptions, Enforcement.

## Answer key (outline)

1. **Purpose:** Protect client trust and comply with SOC 2/GDPR.  
2. **Scope:** All Cadre Corp staff + CADRE labs.  
3. **Roles:** CISO owns policy; DFIR Lead owns CoC; R&D Lead owns lab isolation.  
4. **Labs:** DarkAI/RevAI isolated; no client evidence; Praxis CI required for shared apps.  
5. **Evidence:** Restricted; ticketed access; HITL for AI-assisted findings.  
6. **Exceptions:** Time-boxed, CISO-approved, logged.  
7. **Enforcement:** HR + access revocation; board notified for Critical violations.

**Deliverable for portfolio:** Keep your draft under `docs/examples/` if you expand it.
