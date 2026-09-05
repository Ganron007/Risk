# R-EX-022 — Data classification handling procedures

**CISSP Reference:** Chapter 5, Section "Establishing Information and Asset Handling Requirements", Pages 395–402  
**Exam Objective:** 2.1.2 Establish information and asset handling requirements  
**Study Guide Key Terms:** Data classification, handling procedures, labeling, marking, downgrading, declassification, need-to-know  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`config/asset-inventory.csv`](../../config/asset-inventory.csv), [`../risk-register-baseline.md`](../risk-register-baseline.md)

---

## Scenario Context

Cadre Corp maintains a three-tier classification scheme (Restricted, Confidential, Internal) documented in the enterprise context. However, during a recent tabletop exercise, the following incidents were discovered:

1. A SOC analyst emailed a Restricted evidence summary as an unencrypted PDF attachment to their personal Gmail account to "work from home."
2. The R&D team stored DarkAI model training logs (Internal classification) on the same NAS share as client forensic evidence (Restricted).
3. An intern printed 40 pages of Confidential SIEM telemetry and left them on the breakroom printer overnight.
4. When asked to produce a data handling procedure document, the CISO's team couldn't find one — only the classification labels in `asset-inventory.csv`.

The SOC 2 auditor has given Cadre Corp 30 days to produce formal data handling procedures for each classification level, or risk a qualified opinion. You have been tasked with drafting the handling procedures and resolving the specific incidents.

---

## Multiple-Choice Questions

**Question 1:** For Restricted data like AST-030 (client forensic evidence), which of the following handling requirements is MOST critical?

A. Data must be encrypted at rest using AES-256  
B. Data must never leave authorized systems without documented approval and encryption  
C. Data must be backed up daily to a secure offsite location  
D. Data must be reviewed quarterly for classification accuracy

**Question 2:** The R&D team's co-location of Internal (DarkAI logs) and Restricted (client evidence) data on the same share violates which data handling principle?

A. Data minimization  
B. Need-to-know and segregation of duties  
C. Appropriate segregation by classification level  
D. Least privilege access control

**Question 3:** When drafting the handling procedure for Confidential data (e.g., SIEM telemetry), which of the following should be explicitly PROHIBITED?

A. Access by SOC analysts during incident response  
B. Storage on encrypted file servers within the SOC subnet  
C. Printing without a documented business need and secure disposal afterward  
D. Automated ingestion into Elasticsearch for analysis

**Question 4:** The intern who left printed SIEM data on the breakroom printer violated the principle of:

A. Clean desk policy  
B. Least privilege  
C. Separation of duties  
D. Job rotation

---

## Answer Explanations

**Answer 1: B**  
For Restricted data — where breach is existential to Cadre Corp — the most critical handling requirement is that data must **never leave authorized systems** without documented approval and encryption. Encryption at rest (A) is important but secondary to the authorization gate. The key control is preventing unauthorized exfiltration, which is what the SOC analyst violated by emailing to Gmail.

**Answer 2: C**  
Storing Internal and Restricted data on the same share violates **appropriate segregation by classification level**. Different classification levels require different handling procedures, access controls, and audit requirements. Mixing them means Restricted data inherits the weaker controls of Internal data, creating a classification downgrade by proximity.

**Answer 3: C**  
Printing Confidential data should be **prohibited without a documented business need and secure disposal afterward**. The intern's incident demonstrates why: printed materials create uncontrolled physical copies that bypass digital access controls and audit trails. SOC analysts accessing SIEM data (A) and automated ingestion (D) are legitimate operational needs. The prohibition is on uncontrolled physical reproduction.

**Answer 4: A**  
The intern violated the **clean desk policy** — a foundational physical security control that requires sensitive materials to be secured when unattended. While least privilege (B) might also apply if the intern shouldn't have had access to print SIEM data, the immediate violation is leaving sensitive printed material in an uncontrolled public area — the definition of a clean desk violation.

---

## Cadre Corp Application

1. **Classification Scheme Validation:** Cadre Corp's three-tier scheme (Restricted/Confidential/Internal) maps to standard CISSP models. Verify that every asset in `config/asset-inventory.csv` has a classification label and that the label drives actual handling behavior, not just documentation.

2. **Handling Procedure Gap:** The control register should include `CTL-DATA-HANDLING` with sub-controls for each classification level (storage, transmission, printing, disposal, declassification). The absence of this control is what the SOC 2 auditor flagged.

3. **Lab Verification:** In the CADRE lab, Restricted assets (DCs, client evidence, ADCS CA) sit on the same `192.168.77.0/24` subnet as Internal assets (ws01, provisioning). While this is a lab environment, the principle applies: in production, different classification levels warrant network segmentation.

4. **Print Governance:** For a DFIR firm, printed evidence summaries are a real risk. The procedure should mandate secure print release (PIN at printer) and immediate retrieval for any Restricted or Confidential output.

---

## Interview Talking Points

1. **Procedures Drive Behavior:** "Classification labels in a spreadsheet mean nothing without handling procedures that people actually follow. The SOC 2 auditor found our gap — labels without procedures. I closed it by drafting tiered handling requirements with concrete 'do this, don't do that' rules."

2. **Physical = Digital Risk:** "People forget that printing is a data exfiltration vector. A Restricted document on a breakroom printer is just as breached as one emailed to Gmail. Handling procedures must cover physical and digital equally."

3. **Segregation by Classification:** "Don't mix classification levels on the same storage. Internal data needs different controls than Restricted. If they coexist, the higher classification inherits the lower classification's weaker controls."

4. **Documentation as Control:** "The handling procedure document IS a control. Its existence demonstrates to auditors that we've thought through data lifecycle protection. Its absence is itself a finding."
