# R-EX-008 — Third-party / cloud risk (Entra)

**CISSP Reference:** Chapter 1, Section "Supply Chain Risk Management", Pages 137-141  
**Exam Objective:** 1.1.6 Assess and manage third-party and cloud risks  
**Study Guide Key Terms:** Third-party risk management, cloud risk, vendor due diligence, hybrid identity, privileged identity management (PIM), conditional access  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md), AST-020–023, RISK-011

---

## Scenario Context

Cadre Corp uses Microsoft Entra ID (Azure AD) as a cloud identity provider to support hybrid identity scenarios between the on-premises Active Directory estate and cloud resources. The Entra tenant (AST-020) is used for:
- Hybrid identity synchronization with on-premises AD
- Cloud-based authentication for certain applications
- Lab environments testing cloud identity scenarios
- Potential future client identity management services

The cloud assets include:
- AST-020: Entra ID tenant (hybrid identity)
- AST-021: Azure resources (storage, compute)
- AST-022: Cloud-based SIEM components
- AST-023: Cloud-based backup services

RISK-011 in the risk register identifies cloud identity takeover as a critical concern. The CISO is evaluating whether to enable Cloud Sync to a more production-like tenant, which would increase the cloud identity plane's importance to Cadre Corp's operations.

As the Risk Manager, you need to identify the risks of using a Microsoft cloud tenant for hybrid identity labs, propose due diligence questions before enabling Cloud Sync, and determine the appropriate risk treatment.

---

## Multiple-Choice Questions

**Question 1:** Which of the following represents the most significant risk of using a Microsoft cloud tenant for hybrid identity labs?

A. Increased monthly subscription costs  
B. Token or admin compromise leading to cloud identity takeover  
C. Requirement for additional training for IT staff  
D. Limited customization options for lab environments

**Question 2:** When evaluating whether to enable Cloud Sync to a more production-like tenant, which of the following due diligence questions is most critical?

A. What is the monthly cost of the production tenant?  
B. Who holds Global Admin privileges and is PIM enforced?  
C. How many users will be synced to the cloud tenant?  
D. What is the uptime SLA for the cloud tenant?

**Question 3:** Which of the following control combinations would be most effective in mitigating RISK-011 (cloud identity takeover)?

A. Only implement password complexity requirements  
B. Deploy PIM, conditional access, cloud monitoring, and sync review processes  
C. Rely on Microsoft's default security settings  
D. Implement only network-level controls

**Question 4:** Given Cadre Corp's low risk appetite for hybrid identity takeover, which of the following is the appropriate risk treatment for RISK-011?

A. Accept the risk because cloud providers have strong security  
B. Transfer the risk through Microsoft's shared responsibility model  
C. Mitigate through PIM, conditional access, and monitoring controls  
D. Avoid the risk by eliminating cloud identity entirely

---

## Answer Explanations

**Answer 1: B**  
Token or admin compromise leading to cloud identity takeover is the most significant risk. In hybrid identity scenarios, compromise of cloud admin credentials or tokens can provide attackers with access to both cloud and on-premises resources through synchronization. This represents an existential risk to Cadre Corp's identity plane. Options A, C, and D are incorrect because they represent operational concerns rather than security risks.

**Answer 2: B**  
Who holds Global Admin privileges and is PIM enforced is the most critical due diligence question. Global Admin privileges provide complete control over the Entra tenant, and Privileged Identity Management (PIM) ensures these privileges are only granted when needed. This is the single most important security control for cloud identity. Options A, C, and D are operational or cost considerations, not security risks.

**Answer 3: B**  
Deploying PIM, conditional access, cloud monitoring, and sync review processes provides comprehensive mitigation for cloud identity takeover risk. PIM limits privileged access, conditional access adds context-based authentication requirements, monitoring provides visibility into suspicious activity, and sync review processes ensure synchronization doesn't introduce unintended access. Option A is insufficient for cloud identity. Option C is inadequate because default settings may not meet Cadre Corp's security requirements. Option D is insufficient because network controls don't address identity-specific risks.

**Answer 4: C**  
Mitigate through PIM, conditional access, and monitoring controls is the appropriate treatment given Cadre Corp's low risk appetite for hybrid identity takeover. Cloud identity represents a critical attack surface that requires active mitigation. Acceptance (A) contradicts the low risk appetite. Transfer (B) through Microsoft's shared responsibility model doesn't address Cadre Corp's specific security responsibilities. Avoidance (D) is impractical because cloud identity provides necessary functionality for hybrid scenarios.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's cloud risk management by:

1. **Third-Party Risk Assessment:** Evaluating risks associated with Microsoft cloud services
2. **Hybrid Identity Security:** Understanding the unique risks of cloud-on-premises identity synchronization
3. **Due Diligence Process:** Developing questions for evaluating cloud service configurations
4. **Control Implementation:** Selecting appropriate controls for cloud identity protection

**Lab Connection:** After completing this exercise, you can:
- Review RISK-011 in the risk register (`docs/risk-register-baseline.md`) for cloud identity takeover details
- Examine the Entra ID configuration (AST-020) in the CADRE environment
- Evaluate PIM and conditional access settings in the lab tenant
- Consider how CISO Assistant could track cloud identity risks

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Cloud Identity Risk Assessment:** "I assess cloud identity risks as part of third-party risk management. For Cadre Corp's Entra ID tenant, the primary risk is token or admin compromise leading to cloud identity takeover, which could provide attackers with access to both cloud and on-premises resources through synchronization."

2. **Due Diligence Critical Questions:** "When evaluating cloud identity configurations, I focus on privilege control: Who holds Global Admin privileges? Is PIM enforced? Are conditional access policies in place? These questions reveal the most significant security risks in cloud identity environments."

3. **Layered Cloud Controls:** "I implement layered controls for cloud identity risk mitigation. PIM limits privileged access, conditional access adds context-based authentication requirements, cloud monitoring provides visibility, and sync review processes ensure synchronization doesn't introduce unintended access. This layered approach addresses multiple attack vectors."

4. **Risk Appetite-Driven Treatment:** "Cadre Corp's low risk appetite for hybrid identity takeover drives a Mitigate treatment rather than Acceptance. Cloud identity is too critical to our operations to accept residual risk without appropriate controls. We invest in PIM, conditional access, and monitoring to reduce risk to acceptable levels."

5. **Shared Responsibility Understanding:** "I understand that cloud security follows a shared responsibility model. Microsoft secures the cloud infrastructure, but Cadre Corp is responsible for identity configuration, access policies, and monitoring. This distinction is critical for effective cloud risk management."

---

## Task

1. Identify three risks of using a Microsoft cloud tenant for hybrid identity labs.
2. Propose due-diligence questions before enabling Cloud Sync to a more production-like tenant.
3. Choose treatment for RISK-011.

## Answer key

1. Token/admin compromise; sync of privileged on-prem accounts; misconfigured PIM/RBAC.
2. Who holds GA? Is PIM enforced? Conditional Access? Separate lab tenant vs client tenant? Sync filtering?
3. **Mitigate** — CTL-ENTRA-PIM, CTL-CLOUD-MONITOR, CTL-CLOUD-SYNC-REVIEW; do not Accept without those.

**Link:** Cloud plane is Restricted — appetite is low for hybrid identity takeover.
