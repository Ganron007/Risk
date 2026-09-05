# R-EX-023 — Privacy impact assessment (DPIA)

**CISSP Reference:** Chapter 4, Section "Privacy and Data Protection", Pages 314–322; Chapter 5, Section "Data Protection Methods"  
**Exam Objective:** 2.2.1 Determine and maintain information and asset ownership; 1.4.2 Understand legal and regulatory issues  
**Study Guide Key Terms:** DPIA, GDPR Article 35, PII, data protection by design, privacy risk, processing activities  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../regulatory-obligations.md`](../regulatory-obligations.md), [`../risk-register-baseline.md`](../risk-register-baseline.md)

---

## Scenario Context

Cadre Corp has just signed a new retainer with a German manufacturing client ("EuroMfg GmbH") that requires forensic collection and analysis of 15 employee laptops following a suspected insider threat incident. The laptops contain:

- Employee HR records (performance reviews, disciplinary notes, salary data)
- Personal emails and browser histories mixed with corporate data
- Biometric authentication logs (Windows Hello facial recognition data)
- Health insurance claim documents that employees submitted for reimbursement

Under GDPR Article 35, processing that is "likely to result in high risk to the rights and freedoms of natural persons" requires a Data Protection Impact Assessment (DPIA) BEFORE processing begins. The DFIR Lead wants to start imaging immediately — "the client said it's urgent." The CISO has asked you to determine whether a DPIA is required and, if so, to outline its key components before any forensic work begins.

---

## Multiple-Choice Questions

**Question 1:** Does Cadre Corp's planned forensic collection for EuroMfg GmbH trigger the GDPR Article 35 DPIA requirement?

A. No — Cadre Corp is a data processor, and the DPIA obligation falls on EuroMfg (the data controller)  
B. No — forensic investigations are exempt from DPIA under the "law enforcement exemption"  
C. Yes — the processing involves special categories of data (health, biometrics) at scale and is likely high-risk  
D. Yes — any processing of EU citizen data automatically requires a DPIA regardless of risk level

**Question 2:** Which of the following data types in the EuroMfg laptops constitutes "special category data" under GDPR Article 9?

A. Employee salary data  
B. Windows Hello biometric authentication logs  
C. Personal email messages  
D. Corporate documents marked "Confidential"

**Question 3:** If Cadre Corp proceeds with forensic imaging before completing the DPIA, which of the following is the most significant consequence?

A. The forensic evidence will be inadmissible in court  
B. Cadre Corp may face GDPR administrative fines of up to €10M or 2% of annual turnover  
C. The client will immediately terminate the retainer  
D. The SOC 2 auditor will issue an automatic qualified opinion

**Question 4:** Which of the following is NOT a required component of a GDPR-compliant DPIA?

A. A systematic description of the processing operations  
B. An assessment of the necessity and proportionality of the processing  
C. A cost-benefit analysis of the forensic engagement  
D. The measures to mitigate risks to data subjects' rights

---

## Answer Explanations

**Answer 1: C**  
Yes, a DPIA is required. The processing involves special category data (health records, biometric data) under Article 9, is conducted at scale (15 employees), and involves systematic evaluation of personal aspects (insider threat investigation). While EuroMfg as the data controller also bears DPIA responsibility, Cadre Corp as the processor must assist and cannot simply claim exemption. The "law enforcement exemption" (B) applies to public authorities, not private DFIR firms.

**Answer 2: B**  
Windows Hello biometric authentication logs constitute **special category data** under GDPR Article 9 (biometric data for the purpose of uniquely identifying a natural person). Health insurance documents also qualify (data concerning health). Salary data (A), emails (C), and corporate documents (D) are personal data but not special category data — they receive standard GDPR protections without Article 9's heightened requirements.

**Answer 3: B**  
The maximum fine for DPIA non-compliance under GDPR Article 83(4) is **€10M or 2% of annual worldwide turnover**, whichever is higher. While evidence admissibility (A) and client relationship damage (C) are real concerns, the regulatory financial penalty is the most significant quantified risk. SOC 2 (D) is a separate framework; GDPR violations don't automatically trigger SOC 2 findings.

**Answer 4: C**  
A **cost-benefit analysis** of the engagement is NOT a required DPIA component. The GDPR Article 35(7) requires: (a) description of processing, (b) necessity/proportionality assessment, (c) risk assessment, and (d) mitigation measures. While cost-benefit analysis is good business practice, it's not a legal requirement for DPIA compliance.

---

## Cadre Corp Application

1. **DPIA Template:** Cadre Corp should maintain a DPIA template as part of its control register (`CTL-DPIA`), pre-populated with the company's standard forensic processing activities, so that new engagements don't start from scratch.

2. **Processor vs Controller:** Under GDPR, Cadre Corp is typically a **data processor** (client = controller), but processor obligations under Article 28 include assisting the controller with DPIAs. Cadre Corp cannot simply defer — it must actively support.

3. **Risk Register Link:** RISK-017 (GDPR breach-notification failure) should be extended to include DPIA non-compliance as a trigger condition. The control `CTL-DPIA` should be linked to this risk.

4. **Lab Application:** When processing MTA malware samples in CADRE-RevEng, consider whether any sample contains EU personal data. If so, a mini-DPIA should document the processing purpose, scope, and safeguards.

---

## Interview Talking Points

1. **DPIA as a Gate, Not a Hurdle:** "A DPIA isn't paperwork for paperwork's sake — it's a structured risk assessment that protects both the data subjects AND our firm. I'd rather spend two hours on a DPIA than two years fighting a GDPR fine."

2. **Processor Liability:** "Being a data processor doesn't mean we're off the hook. GDPR Article 28 requires processors to assist controllers with DPIAs. If we image laptops containing health data without one, we share the liability."

3. **Special Category Data Recognition:** "You need to recognize special category data BEFORE processing starts. Biometrics, health data, political opinions — these trigger heightened requirements. A DFIR firm that can't spot these in a scope document is a liability."

4. **Risk-Based Approach:** "Not every engagement needs a full DPIA. The trigger is 'likely to result in high risk.' For a simple ransomware triage with no PII, a lightweight assessment suffices. For insider threat investigations with employee HR data, you go full DPIA."
