# R-EX-003 — BIA for Elastic SIEM (AST-010)

**CISSP Reference:** Chapter 3, Section "Business Impact Analysis", Pages 275-285  
**Exam Objective:** 1.4.2 Conduct business impact analysis (BIA)  
**Study Guide Key Terms:** Business impact analysis (BIA), recovery time objective (RTO), recovery point objective (RPO), critical business functions, maximum tolerable downtime (MTD)  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md), RISK-009

---

## Scenario Context

Cadre Corp's Elastic SIEM (AST-010) is the central security monitoring platform that ingests logs from domain controllers, member servers, endpoints, and network sensors. The SIEM supports two critical business functions:

1. **Continuous monitoring for client retainers:** Cadre Corp has 120 enterprise clients under DFIR retainers that require 24/7 security monitoring with specific detection and response SLAs
2. **Detection engineering and campaign validation:** The SOC team uses SIEM telemetry to validate detection rules, test campaign scenarios, and improve security posture

The SIEM infrastructure includes:
- Elastic cluster with hot data retention (30 days) and warm storage (90 days)
- Fleet agents on all endpoints and servers
- Custom detection rules for DCSync, Kerberoasting, and other AD attacks
- Integration with Velociraptor (AST-011) for endpoint response

A recent risk assessment (RISK-009) identified SIEM availability as a critical concern. The CISO has requested a Business Impact Analysis (BIA) to determine appropriate RTO/RPO targets and continuity strategies for the SIEM.

---

## Multiple-Choice Questions

**Question 1:** Which of the following best describes the primary business impact if the SIEM is unavailable for 72 hours during an active client incident response?

A. Minor inconvenience—analysts can use alternative log sources  
B. Delayed incident containment leading to client SLA breach and potential evidence loss  
C. No impact—clients understand that systems occasionally fail  
D. Only internal detection engineering is affected, not client monitoring

**Question 2:** When determining the Recovery Time Objective (RTO) for the SIEM, which of the following factors should be the primary driver?

A. Technical feasibility of recovery  
B. Client contractual SLAs for detection and response times  
C. Cost of high-availability solutions  
D. IT team preference for recovery procedures

**Question 3:** For the SIEM's security event data, which of the following RPO targets would be most appropriate given Cadre Corp's DFIR business model?

A. 24 hours—acceptable to lose a day of security events  
B. 1 hour—minimal data loss acceptable  
C. Near-zero—no security event data loss acceptable  
D. 1 week—security events are not critical for DFIR

**Question 4:** In the context of the BIA, which of the following represents the Maximum Tolerable Downtime (MTD) for the SIEM based on client SLA requirements?

A. 1 hour—any downtime is unacceptable  
B. 4 hours—aligns with typical client SLA response times  
C. 72 hours—clients can tolerate extended outages  
D. 1 week—DFIR engagements are not time-sensitive

---

## Answer Explanations

**Answer 1: B**  
Delayed incident containment leading to client SLA breach and potential evidence loss is the primary business impact. During an active client IR, the SIEM provides critical telemetry for incident scoping, attacker identification, and containment. Without SIEM data, analysts cannot effectively respond, leading to delayed containment, extended attacker dwell time, and potential evidence destruction. This violates client SLAs and could result in contract penalties. Option A is incorrect because alternative log sources are insufficient for comprehensive monitoring. Option C is incorrect because clients expect reliable monitoring. Option D is incorrect because client monitoring is the primary function.

**Answer 2: B**  
Client contractual SLAs for detection and response times should be the primary driver for RTO. Cadre Corp's business model depends on meeting client SLAs, which typically specify detection and response timeframes (e.g., 4-hour initial response, 24-hour containment). The SIEM RTO must support these requirements. Technical feasibility (A) and cost (C) are constraints but not the primary driver. IT team preference (D) is not a valid business justification.

**Answer 3: C**  
Near-zero RPO (no security event data loss acceptable) is most appropriate for a DFIR business model. Security event data is critical for incident investigation, attacker attribution, and legal proceedings. Losing even 1 hour of event data could mean missing critical indicators of compromise, attack timeline gaps, or evidence destruction. In DFIR, event data loss directly impacts the ability to fulfill client engagements. Options A, B, and D are incorrect because any data loss compromises forensic investigations.

**Answer 4: B**  
4 hours aligns with typical client SLA response times and represents the Maximum Tolerable Downtime. Client SLAs typically specify 4-hour initial response times, so the SIEM must be available within this window to support incident response. MTD of 1 hour (A) may be technically challenging and expensive. 72 hours (C) and 1 week (D) would violate client SLAs and result in contract penalties.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's business continuity planning by:

1. **BIA Methodology:** Applying structured business impact analysis to critical security infrastructure
2. **SLA-Driven Requirements:** Using client contractual obligations to drive RTO/RPO targets
3. **DFIR-Specific Considerations:** Understanding the unique impact of SIEM unavailability on forensic investigations
4. **Continuity Strategy:** Informing the selection of appropriate continuity strategies (hot site vs. warm site)

**Lab Connection:** After completing this exercise, you can:
- Review RISK-009 in the risk register (`docs/risk-register-baseline.md`) to understand SIEM availability concerns
- Examine the SIEM architecture in the CADRE lab to evaluate high-availability options
- Consider how Elastic cluster replication could provide near-zero RPO
- Evaluate the business continuity strategy (R-EX-014) for SIEM-specific requirements

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **BIA-Driven Continuity Planning:** "I conduct Business Impact Analysis before implementing continuity solutions. For the SIEM, I identified that client SLAs drive RTO requirements (4 hours) and the DFIR business model drives RPO requirements (near-zero). This analysis ensures we invest in the right continuity strategies."

2. **SLA Alignment:** "In DFIR, client SLAs are the primary driver for system availability requirements. I map technical RTO/RPO targets to contractual obligations—4-hour RTO because that's the typical initial response SLA, near-zero RPO because event data loss compromises forensic investigations."

3. **DFIR-Specific Impact Analysis:** "Security infrastructure BIA differs from traditional IT BIA. For the SIEM, the impact isn't just operational—it's forensic. Losing SIEM data during an active IR means losing evidence, missing attacker TTPs, and potentially failing to fulfill client engagements. This justifies higher investment in continuity."

4. **Cost-Benefit Justification:** "When presenting continuity investment to the board, I translate technical requirements into business impact. 'Near-zero RPO for the SIEM prevents evidence loss that could violate attorney-client privilege and result in contract penalties.' This business-focused justification secures funding for high-availability solutions."

5. **MTD vs. RTO Distinction:** "I distinguish between Maximum Tolerable Downtime (MTD) and Recovery Time Objective (RTO). MTD is the point where business impact becomes unacceptable—4 hours for the SIEM based on client SLAs. RTO is our target recovery time, which should be less than MTD to provide buffer. This distinction ensures we don't set RTO equal to MTD."

---

## Task

1. Identify two business processes that depend on AST-010.
2. Estimate RTO/RPO (illustrative) for SOC retainer monitoring.
3. State the worst-case impact if SIEM is dark for 72 hours during an active client IR.

## Answer key

1. Continuous monitoring for retainers; detection engineering / campaign validation telemetry.
2. Example: RTO 4–8h (SOC Lead escalate), RPO near-zero for security events (prefer short ILM hot retention, not loss).
3. Missed DCSync/Kerberoast telemetry → delayed containment → contractual SLA breach + appetite violation on detection capability.

**Link:** RISK-009 treatment remains Mitigate (availability + access controls).
