# R-EX-021 — Data owner vs data custodian roles

**CISSP Reference:** Chapter 5, Section "Understanding Data Roles", Pages 390–394  
**Exam Objective:** 2.1.1 Identify and classify information and assets  
**Study Guide Key Terms:** Data owner, data custodian, data controller, data processor, accountability, responsibility  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`config/asset-inventory.csv`](../../config/asset-inventory.csv), [`../risk-register-baseline.md`](../risk-register-baseline.md)

---

## Scenario Context

Cadre Corp's DFIR analysts handle client forensic evidence daily — disk images, memory dumps, and privileged logs from 120 enterprise clients. A recent internal audit revealed confusion around data ownership: the DFIR Lead believes they "own" the evidence since they collect it, the SOC Lead claims ownership because it traverses their SIEM, and the CISO insists ultimate accountability rests with them as the most senior security officer.

To complicate matters, Cadre Corp uses a third-party cloud backup provider for disaster recovery of forensic case files. The contract designates the provider as a "data processor," but the provider's sales engineer told the DFIR Lead they "treat all customer data as their own."

You have been asked to clarify the data roles for Cadre Corp's forensic evidence chain and resolve the ownership confusion before the upcoming SOC 2 audit, where auditors will specifically examine role definitions and access control accountability.

---

## Multiple-Choice Questions

**Question 1:** In the context of Cadre Corp's client forensic evidence (AST-030), who is the **data owner**?

A. The DFIR Lead, because they collect and manage the evidence  
B. The client who contracted Cadre Corp for DFIR services  
C. The CISO, because they are accountable for all security decisions  
D. The SOC Lead, because evidence traverses their SIEM infrastructure

**Question 2:** The third-party cloud backup provider's claim that they "treat customer data as their own" is problematic because:

A. It violates the principle of least privilege  
B. It conflates the role of data custodian with data owner  
C. It exceeds the provider's processing capacity  
D. It creates an audit trail gap for SOC 2

**Question 3:** Which of the following best describes the Cadre Corp CISO's role with respect to AST-030?

A. Data owner — the CISO is ultimately accountable for all data  
B. Data custodian — the CISO implements technical controls  
C. Senior management — the CISO ensures data governance policies exist and are enforced  
D. Data processor — the CISO processes risk decisions about data

**Question 4:** A DFIR analyst at Cadre Corp copies a client's forensic disk image to their personal external drive for "offline analysis convenience." Under the data roles framework, this is a violation by the:

A. Data owner — they should not have allowed the copy  
B. Data custodian — they failed to implement proper technical controls  
C. Data processor — the analyst was processing data outside authorized systems  
D. Both B and C — the analyst (as custodian/processor) violated handling procedures, and the custodian controls failed to prevent it

---

## Answer Explanations

**Answer 1: B**  
The **client** is the data owner. Cadre Corp is a service provider — the client owns the evidence, determines its classification, and grants Cadre Corp permission to process it. The DFIR Lead and SOC Lead are custodians; the CISO is senior management. This is a classic CISSP distinction: the data owner is the entity with ultimate organizational authority over the data, which in a DFIR services context is the client, not the service provider.

**Answer 2: B**  
The provider's statement conflates **data custodian** (implementing technical controls on behalf of the owner) with **data owner** (ultimate authority and accountability). A processor/custodian cannot unilaterally claim ownership — ownership stays with the client (or Cadre Corp as the contracted service provider to the client). This distinction is critical for SOC 2 Trust Services Criteria and GDPR Article 28 processor requirements.

**Answer 3: C**  
The CISO is **senior management** responsible for ensuring data governance policies exist and are enforced. The CISO does not own client data (the client does) and is not a hands-on custodian. In CISSP terminology, senior management bears ultimate organizational accountability for security, including ensuring data roles are defined, not for owning every dataset.

**Answer 4: D**  
This is a dual failure: the analyst (acting as a data custodian/processor) violated handling procedures by copying Restricted data to an unauthorized device, AND the custodian controls (DLP, USB restrictions, endpoint monitoring) failed to prevent it. The client (data owner) is not responsible for Cadre Corp's internal control failures — they entrusted Cadre Corp to handle data properly.

---

## Cadre Corp Application

This exercise directly applies to the Cadre Corp lab environment by:

1. **Role Assignment:** Using the asset inventory, each AST-* entry has an `owner` field — but this is the *organizational* owner, not the CISSP *data owner*. For AST-030 (client evidence), the data owner is always the client.

2. **SOC 2 Audit Readiness:** Auditors will ask "who owns this data?" and expect clear role delineation. The control register's `CTL-EVIDENCE-ACCESS` control requires documented data ownership for all Restricted assets.

3. **Third-Party Risk:** The cloud backup scenario (R-EX-008 covered vendor risk management) extends here into data role clarity — every third-party contract must specify whether the vendor is a custodian or processor.

4. **Lab Verification:** Review `config/asset-inventory.csv` — verify every Restricted asset has a clear data owner (client vs Cadre Corp), custodian (team responsible for controls), and processor designation where applicable.

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Ownership ≠ Possession:** "Just because we hold the data doesn't mean we own it. For a DFIR firm, the client is always the data owner. We're custodians and processors. Confusing these roles is how you fail a SOC 2 audit."

2. **Contractual Clarity:** "Every third-party contract must specify data roles. When a vendor says 'we treat your data as our own,' that's a red flag — they're claiming ownership, not custodianship. That's a liability for us and our clients."

3. **Accountability Chain:** "The CISO doesn't own every dataset, but they own the governance framework that ensures every dataset HAS a designated owner. That's the distinction between operational ownership and governance accountability."

4. **Audit Trail:** "When auditors ask 'who owns this data?', having a clear answer backed by documented role assignments is the difference between a finding and a clean opinion."

5. **Custodian Controls:** "Data custodians are measured by the controls they implement, not their job title. If a DFIR analyst can copy Restricted evidence to a personal drive, the custodian controls have failed regardless of who 'owns' the data."
