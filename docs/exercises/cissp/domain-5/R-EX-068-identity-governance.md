# R-EX-068 — Identity governance and administration (IGA)

**CISSP Reference:** Chapter 13, Section "Identity Management Implementation"; Chapter 14, Section "Controlling and Monitoring Access"  
**Exam Objective:** 5.3.1 Implement identity governance; 5.3.2 Conduct access reviews  
**Study Guide Key Terms:** IGA, access certification, role mining, segregation of duties (SoD), entitlements management, access review campaigns  

---

## Scenario Context

Cadre Corp's IGA maturity is low: no formal access reviews, no segregation of duties enforcement, and no role definitions beyond Active Directory group memberships. The SOC 2 auditor has given a qualified opinion: "The organization cannot demonstrate that user access is reviewed and appropriate on a periodic basis."

Specific issues: (1) The same person who approves forensic reports (DFIR Lead) also administers the evidence store — they could theoretically modify evidence and approve their own modifications, (2) No process exists for managers to certify their team's access, (3) When asked "who has access to the client evidence share?", the answer takes 3 days of manual PowerShell queries.

---

## Multiple-Choice Questions

**Question 1:** Segregation of Duties (SoD) addresses which risk at Cadre Corp?

A. Password reuse across applications  
B. A single individual having conflicting responsibilities — like the DFIR Lead who both administers evidence AND approves evidence reports, enabling undetected tampering  
C. Slow VPN connection speeds  
D. Excessive software licensing costs

**Question 2:** An access certification (or "attestation") campaign is:

A. A training course for new employees about access policies  
B. A periodic review where managers confirm each of their direct reports still needs their assigned access — stale or inappropriate access is flagged for removal  
C. A penetration test focused on access controls  
D. A certification exam for IT administrators

**Question 3:** Role mining in IGA refers to:

A. Cryptocurrency mining using privileged accounts  
B. Analyzing existing user permissions across systems to identify common patterns and define formal roles — "what permissions do all DFIR Analysts actually have?" — as a foundation for RBAC  
C. Searching for hidden administrator accounts  
D. Mining role-based data for business intelligence

---

## Answer Explanations

**Answer 1: B**  
**SoD prevents conflict of interest** by separating duties that should not be held by the same person. Classic example: the person who writes checks shouldn't reconcile the bank statement. At Cadre Corp: the person who administers evidence storage shouldn't approve evidence reports — otherwise, they can modify evidence and self-approve the modification with no oversight. SoD is detected via access review and enforced via role design.

**Answer 2: B**  
**Access certification** is the formal, periodic process where managers review their team's access and attest: "These permissions are still appropriate for their current role." Any access that can't be justified is revoked. This is the primary detective control against privilege creep and is required by SOC 2, ISO 27001, and most compliance frameworks.

**Answer 3: B**  
**Role mining** is the analytical precursor to RBAC: instead of defining roles from scratch, analyze existing permissions to identify natural clusters ("these 12 users all have the same 8 AD groups — that's probably a 'DFIR Analyst' role"). This is a bottom-up approach that grounds role definitions in reality rather than assumptions.

---

## Cadre Corp Application

1. **Quarterly Access Certification:** Implement a lightweight certification using PowerShell: export all AD group memberships → send to managers → managers review and flag inappropriate access → revoke flagged access within 30 days. Document the campaign for SOC 2 evidence.

2. **SoD Rules:** Define critical SoD conflicts: (a) Evidence admin + Evidence report approver, (b) Code committer + Code reviewer (for Ansible playbooks), (c) Audit log admin + System administrator. Detect violations via automated analysis of group memberships.

3. **Role Definitions:** Mine the existing 187 AD groups to identify 8-12 job roles. Formalize each role's required and prohibited permissions. This becomes the RBAC foundation.

---

## Interview Talking Points

1. **You Can't Protect What You Can't See:** "When the auditor asked 'who has access to client evidence?' and it took 3 days to answer, that's an IGA failure. A mature IGA program answers that question in 30 seconds — and can prove the answer is current."

2. **Access Reviews Are Your Safety Net:** "Privilege creep happens silently. The quarterly access review is the moment you catch it — the manager who says 'wait, why does my intern still have Server Operator?' That conversation is the entire point of IGA."
