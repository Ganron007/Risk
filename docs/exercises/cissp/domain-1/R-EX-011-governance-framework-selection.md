# R-EX-011 — Security governance framework selection

**CISSP Reference:** Chapter 1, Section "Evaluate and Apply Security Governance Principles", Pages 106-109  
**Exam Objective:** 1.1.3 Evaluate and apply security governance principles  
**Study Guide Key Terms:** Security governance, risk management framework, NIST CSF, ISO 27001, COBIT, governance framework selection  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../regulatory-obligations.md`](../regulatory-obligations.md), [`../control-register.md`](../control-register.md)

---

## Scenario Context

Cadre Corp is preparing for its first formal SOC 2 Type II audit and has initiated an ISO 27001 certification process. The CISO has been asked by the board to recommend a primary security governance framework to guide the organization's risk management and control implementation. The company currently has ad-hoc security practices but needs a structured approach to satisfy multiple compliance requirements while maintaining operational efficiency.

The board has expressed concerns about:
- The complexity of implementing multiple frameworks simultaneously
- The cost of framework certification and maintenance
- The need to demonstrate due diligence to clients and auditors
- Balancing security requirements with the agility needed for DFIR operations

You have been tasked with evaluating the major governance frameworks (NIST CSF, ISO 27001, COBIT) and recommending the most appropriate primary framework for Cadre Corp, considering the company's regulatory obligations (SOC 2, GDPR, ISO 27001) and business model as a DFIR services provider.

---

## Multiple-Choice Questions

**Question 1:** Which of the following governance frameworks would be most appropriate as Cadre Corp's primary framework given its need to satisfy SOC 2 Type II and ISO 27001 requirements simultaneously?

A. COBIT 2019  
B. NIST Cybersecurity Framework (CSF)  
C. ISO/IEC 27001  
D. CIS Controls

**Question 2:** If Cadre Corp selects ISO 27001 as its primary framework, which of the following best describes the relationship between ISO 27001 and SOC 2 Type II compliance?

A. ISO 27001 certification automatically satisfies all SOC 2 requirements  
B. SOC 2 and ISO 27001 are completely independent and cannot be mapped  
C. ISO 27001 controls can be mapped to SOC 2 Trust Services Criteria with some gaps  
D. SOC 2 is a subset of ISO 27001 and requires no additional work

**Question 3:** The CISO is considering using NIST CSF as an overlay framework to ISO 27001. What is the primary benefit of this approach for Cadre Corp?

A. NIST CSF provides certification that ISO 27001 lacks  
B. NIST CSF offers a more flexible, risk-based approach that complements ISO 27001's prescriptive controls  
C. NIST CSF is required by GDPR for EU client data  
D. NIST CSF is less expensive to implement than ISO 27001

**Question 4:** When presenting the framework recommendation to the board, which of the following arguments would be most compelling for selecting ISO 27001 as the primary framework?

A. "ISO 27001 is the most widely recognized framework globally and will enhance our market credibility"  
B. "ISO 27001 will automatically make us compliant with all regulations including GDPR and HIPAA"  
C. "ISO 27001 requires no ongoing maintenance costs after initial certification"  
D. "ISO 27001 is only relevant for European companies and won't impact our US clients"

---

## Answer Explanations

**Answer 1: C**  
ISO/IEC 27001 is the most appropriate primary framework because Cadre Corp has already initiated an ISO 27001 certification process and ISO 27001 can be effectively mapped to SOC 2 Type II requirements. ISO 27001 provides a comprehensive Information Security Management System (ISMS) that includes risk management, controls, and continual improvement—elements that support both SOC 2 and GDPR compliance. NIST CSF is excellent as a complementary framework but is not certifiable in the same way as ISO 27001.

**Answer 2: C**  
ISO 27001 controls can be mapped to SOC 2 Trust Services Criteria with some gaps. Both frameworks address similar security domains but use different terminology and structures. ISO 27001's Annex A controls can be mapped to SOC 2's Trust Services Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy), but organizations typically need to demonstrate additional evidence for SOC 2-specific requirements. ISO 27001 certification does not automatically satisfy SOC 2, but it significantly reduces the compliance burden.

**Answer 3: B**  
NIST CSF offers a more flexible, risk-based approach that complements ISO 27001's prescriptive controls. While ISO 27001 provides specific controls (Annex A), NIST CSF organizes security into five functions (Identify, Protect, Detect, Respond, Recover) that emphasize risk management and continuous improvement. Using NIST CSF as an overlay allows Cadre Corp to maintain ISO 27001 certification while adopting a more agile, risk-based approach to security governance that aligns with DFIR operational needs.

**Answer 4: A**  
"ISO 27001 is the most widely recognized framework globally and will enhance our market credibility" is the most compelling argument because it addresses the board's business concerns. ISO 27001 certification is a globally recognized standard that demonstrates due diligence to clients and can be a competitive differentiator in the DFIR market. The other options are incorrect: ISO 27001 does not automatically ensure compliance with all regulations (B), requires ongoing maintenance costs (C), and is relevant globally, not just for European companies (D).

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's compliance journey by:

1. **Framework Alignment:** Understanding how ISO 27001 (already initiated) maps to SOC 2 Type II (contractual requirement) and GDPR (EU client data requirement)
2. **Control Mapping:** Using the existing control register (`docs/control-register.md`) to see how CADRE capabilities map to ISO 27001 Annex A controls
3. **Regulatory Strategy:** Developing a coherent compliance strategy that satisfies multiple obligations without redundant effort
4. **Business Case:** Building a board presentation that justifies framework selection based on business value, not just technical compliance

**Lab Connection:** After completing this exercise, you can:
- Review `docs/regulatory-obligations.md` to understand Cadre Corp's compliance drivers
- Examine `docs/control-register.md` to see how current capabilities map to NIST CSF and ISO 27001
- Consider how CISO Assistant (classic GRC) could be used to manage ISO 27001 compliance
- Evaluate how VerifyWise (AI governance) could support ISO 42001 for AI systems

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Framework Selection Criteria:** "When selecting a governance framework, I consider regulatory requirements, industry recognition, implementation cost, and operational fit. For Cadre Corp, ISO 27001 was the right choice because it aligns with our certification goals, maps well to SOC 2, and enhances our market credibility."

2. **Multi-Framework Strategy:** "Rather than implementing frameworks in isolation, I use a primary framework (ISO 27001) and overlay complementary frameworks (NIST CSF) to address specific needs. This approach reduces redundancy while ensuring comprehensive coverage."

3. **Business Value Focus:** "Governance frameworks aren't just compliance checkboxes—they're business enablers. ISO 27001 certification helps us win client contracts, demonstrate due diligence, and operationalize our risk management process."

4. **Gap Management:** "I map controls across frameworks to identify gaps and overlaps. For example, ISO 27001 Annex A controls map well to SOC 2 Trust Services Criteria, but we need additional evidence for SOC 2-specific requirements like continuous monitoring."

5. **Continuous Improvement:** "Framework adoption is not a one-time project. I establish continual improvement processes that align with ISO 27001's Plan-Do-Check-Act cycle, ensuring our security governance evolves with the business and threat landscape."

---

## Task

1. Compare NIST CSF, ISO 27001, and COBIT as primary frameworks for Cadre Corp.
2. Map ISO 27001 Annex A controls to SOC 2 Trust Services Criteria.
3. Recommend a primary framework with justification for the board.
4. Identify how the selected framework supports GDPR compliance for EU client data.

## Answer key

1. **Comparison:**
   - **NIST CSF:** Flexible, risk-based, five functions (Identify, Protect, Detect, Respond, Recover), not certifiable, excellent for risk management
   - **ISO 27001:** Prescriptive controls (Annex A), certifiable ISMS, globally recognized, aligns with SOC 2 and GDPR
   - **COBIT:** Process-focused, IT governance oriented, broader than security, more complex implementation

2. **ISO 27001 to SOC 2 mapping:**
   - ISO 27001 A.5 (Information security policies) → SOC 2 CC1.1 (Communication and responsibility)
   - ISO 27001 A.6 (Organization of information security) → SOC 2 CC1.2 (Governance structure)
   - ISO 27001 A.8 (Asset management) → SOC 2 CC6.1 (Logical and physical access)
   - ISO 27001 A.12 (Operations security) → SOC 2 CC7.2 (System operations)
   - Gaps exist in SOC 2-specific areas like continuous monitoring and vendor risk management

3. **Recommendation:** ISO 27001 as primary framework because:
   - Already initiated certification process
   - Maps effectively to SOC 2 Type II requirements
   - Supports GDPR compliance through risk management and controls
   - Globally recognized, enhances market credibility
   - Provides certifiable ISMS structure

4. **GDPR support:** ISO 27001 supports GDPR through:
   - Risk management process (Article 32)
   - Access controls (Article 25)
   - Incident management (Article 33)
   - Business continuity (Article 32)
   - Documentation and evidence (Articles 24, 30)

**Pass criteria:** You can justify framework selection based on Cadre Corp's specific regulatory obligations, business model, and operational needs.
