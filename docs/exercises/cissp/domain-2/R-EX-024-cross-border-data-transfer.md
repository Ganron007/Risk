# R-EX-024 — Cross-border data transfer compliance

**CISSP Reference:** Chapter 4, Section "Legal and Regulatory Issues", Pages 302–330; Chapter 5, Section "Data Protection Methods"  
**Exam Objective:** 2.2.1 Determine and maintain information and asset ownership; 1.4.2 Understand legal and regulatory issues  
**Study Guide Key Terms:** Cross-border data transfer, GDPR Chapter V, adequacy decision, Standard Contractual Clauses (SCCs), Binding Corporate Rules (BCRs), Schrems II, EU-US Data Privacy Framework  
**Inputs:** [`../regulatory-obligations.md`](../regulatory-obligations.md), [`../enterprise-context.md`](../enterprise-context.md)

---

## Scenario Context

Cadre Corp has a growing international DFIR practice. Three situations have arisen simultaneously:

1. **EuroMfg evidence on US servers:** Forensic images from the German EuroMfg engagement (see R-EX-023) are stored on Cadre Corp's on-premises servers in Chicago. The images contain EU employee PII and health data.

2. **India-based analyst team:** Cadre Corp is piloting a cost-saving measure where two junior DFIR analysts in Mumbai will remotely access forensic case files on Cadre Corp's US servers to perform initial triage and file carving. They will use a VPN into the lab network and have read access to evidence shares.

3. **Australian client request:** A Sydney-based law firm has asked Cadre Corp to send forensic reports (containing Australian citizen PII) to their e-discovery vendor in Singapore for review.

The CISO has asked you to evaluate the cross-border data transfer compliance requirements for all three scenarios under GDPR and other applicable privacy regulations. The company has no existing SCCs, BCRs, or transfer impact assessments in place.

---

## Multiple-Choice Questions

**Question 1:** Under GDPR, Cadre Corp's storage of EuroMfg employee PII on US servers requires:

A. Nothing — the US is an "adequate" country under GDPR  
B. A valid transfer mechanism such as Standard Contractual Clauses (SCCs) with a Transfer Impact Assessment (TIA)  
C. Explicit consent from each of the 15 EuroMfg employees  
D. Registration with the EU Data Protection Board (EDPB)

**Question 2:** The Mumbai analyst access scenario creates which additional cross-border transfer concern beyond the storage question?

A. None — India has an EU adequacy decision  
B. The transfer from US → India adds a second international transfer that needs its own lawful basis  
C. Remote access via VPN eliminates the transfer concern since data "stays" on US servers  
D. Only transfers FROM the EU matter; transfers between non-EU countries are unregulated

**Question 3:** The Schrems II decision (2020) is relevant to Cadre Corp because it:

A. Banned all data transfers from the EU to the United States permanently  
B. Invalidated the EU-US Privacy Shield and required supplementary measures for SCC-based transfers to the US  
C. Exempted DFIR firms from cross-border transfer requirements  
D. Required all EU data to be stored exclusively within the EU

**Question 4:** For the Australian client's request to send PII to Singapore, which regulatory framework primarily governs the transfer?

A. GDPR — because the data originated from an EU-affiliated matter  
B. Australia's Privacy Act 1988 and its cross-border disclosure principles  
C. Singapore's PDPA — because Singapore is the destination  
D. US law — because Cadre Corp is US-based

---

## Answer Explanations

**Answer 1: B**  
Under GDPR Chapter V, transfers to the US require a valid transfer mechanism. While the EU-US Data Privacy Framework (DPF) now provides an adequacy decision for certified US entities, Cadre Corp would need to either (a) be DPF-certified, or (b) use **Standard Contractual Clauses with a Transfer Impact Assessment (TIA)**. The US is not automatically "adequate" — only specific certified entities qualify. Consent (C) is possible but impractical at scale and revocable.

**Answer 2: B**  
The US → India transfer is a **second international transfer** requiring its own lawful basis. India does not have an EU adequacy decision, so Cadre Corp needs SCCs (or another mechanism) covering the India access as a sub-processor. VPN access (C) is technically incorrect — GDPR regulates "transfer" as access from a third country, not just physical storage location. If an analyst in Mumbai can read PII on screen, a transfer has occurred.

**Answer 3: B**  
The **Schrems II** decision (CJEU, July 2020) invalidated the EU-US Privacy Shield and ruled that SCC-based transfers require a case-by-case assessment of whether the destination country's laws provide "essentially equivalent" protection. If not, **supplementary measures** (e.g., encryption with keys held outside the destination country) must be added. This directly affects Cadre Corp's US-based storage of EU evidence.

**Answer 4: B**  
The **Australian Privacy Act 1988** (specifically APP 8 — cross-border disclosure of personal information) primarily governs this transfer. Australia regulates the outbound transfer from its jurisdiction. GDPR applies to EU data subjects, not Australian citizens' data (unless the Sydney firm's matter involves EU residents). Singapore's PDPA (C) governs data once in Singapore, but the Australian firm's obligation to ensure protection before transfer is the primary concern.

---

## Cadre Corp Application

1. **Transfer Impact Assessment:** Cadre Corp should create a TIA template (`CTL-TIA`) documenting: destination country, surveillance laws, SCC supplementary measures, and residual risk acceptance. Every international engagement triggers this.

2. **Processor Chain Mapping:** For the Mumbai scenario, the sub-processor relationship (Cadre Corp → India analysts) must be disclosed in the DPA with each EU client. GDPR Article 28 requires controller authorization for sub-processors.

3. **Technical Supplementary Measures:** For US storage of EU evidence, consider: (a) client-side encryption with keys held only in the EU, (b) tokenization of PII fields before storage, or (c) contractual commitments from US cloud providers with DPF certification.

4. **Regulatory Obligations Doc Update:** Add a "Cross-Border Transfer" section to `docs/regulatory-obligations.md` listing each country pair (EU→US, US→India, Australia→Singapore) with its transfer mechanism and TIA status.

---

## Interview Talking Points

1. **Transfer Isn't Just Storage:** "Cross-border transfer isn't just about where disks sit. If an analyst in India can view PII on their screen, a transfer has occurred. VPNs don't create legal firewalls."

2. **Schrems II Is Alive:** "The EU-US Data Privacy Framework helped, but Schrems II's core requirement — case-by-case transfer impact assessment — is still the standard. You can't just sign SCCs and call it done."

3. **Sub-Processor Awareness:** "Every person who touches client data across a border is a sub-processor. Your DPA with the client needs to list them, or you're in breach."

4. **Practical Risk Management:** "For a DFIR firm, perfect compliance with every cross-border regime is expensive. I'd prioritize: (1) SCCs + TIA for EU→US, (2) client transparency about any non-US/non-EU access, (3) technical measures where legal ones are insufficient."
