# R-EX-018 — GDPR data flow for EU client evidence

**CISSP Reference:** Chapter 4, Sections "Privacy and Data Protection", "GDPR", Pages 302–330; Chapter 5, Section "Data Protection Methods"  
**Exam Objective:** 2.2.1 Determine and maintain information and asset ownership; 1.4.2 Understand legal and regulatory issues (GDPR)  
**Study Guide Key Terms:** GDPR, data controller, data processor, data flow mapping, Article 30 (Records of Processing), Article 33 (Breach Notification), 72-hour notification, cross-border transfer, SCCs  
**Inputs:** [`../regulatory-obligations.md`](../regulatory-obligations.md), [`../enterprise-context.md`](../enterprise-context.md), RISK-017

---

## Scenario Context

Cadre Corp handles forensic evidence from EU-based clients, making it a **data processor** under GDPR for personal data contained in client disk images, memory dumps, and network captures. Under GDPR Article 30, processors must maintain Records of Processing Activities (RoPA) documenting: purposes of processing, categories of data subjects and personal data, recipients, cross-border transfers, and retention periods.

The current Cadre Corp processing flow for a EuroMfg GmbH insider threat case:

1. **Collection:** Disk image received via encrypted courier from Munich → imaged on mbr01 in Chicago.
2. **Processing:** Image analyzed by DFIR analysts in Chicago; personal data (employee HR records, health data — see R-EX-023) extracted as evidence.
3. **Storage:** Evidence stored on AST-030 (on-prem Restricted share) and backed up to a US-based cloud provider (AST-023).
4. **Sharing:** Findings shared with EuroMfg's legal team via the client portal; metadata (file names, user accounts) visible in Elastic SIEM dashboards accessible to 10 SOC analysts.

The CISO asks: "If this evidence were breached, when does our 72-hour notification clock start? And are our cross-border transfers compliant?"

---

## Multiple-Choice Questions

**Question 1:** Under GDPR Article 33, the 72-hour breach notification clock starts when:

A. The breach actually occurred  
B. Cadre Corp becomes AWARE of the breach — awareness triggers the clock; "awareness" means a reasonable degree of certainty that a breach involving personal data has occurred  
C. The client notifies Cadre Corp of the breach  
D. 72 hours after the end of the investigation

**Question 2:** Cadre Corp stores EU client evidence on US servers and backs up to a US cloud provider. Under GDPR Chapter V, what is required for these cross-border transfers?

A. Nothing — the US has a full GDPR adequacy decision for all companies  
B. A valid transfer mechanism — such as Standard Contractual Clauses (SCCs) with a Transfer Impact Assessment (TIA) — and the client (controller) must be informed of and authorize the transfer locations  
C. Only the cloud provider needs to be GDPR-compliant; Cadre Corp has no obligations as a processor  
D. EU evidence can never leave the EU under any circumstances

**Question 3:** Ten SOC analysts can see EU client metadata in Elastic dashboards. Under GDPR's data minimization and access control principles, this is problematic because:

A. SOC analysts are not EU citizens  
B. Access to personal data (even metadata like usernames and file paths) should be limited to those with a legitimate need — all 10 SOC analysts may not need access to every EU client's case metadata; role-based access controls should restrict visibility to the assigned case team  
C. Elasticsearch cannot store EU personal data  
D. Metadata is never considered personal data under GDPR

**Question 4:** As a data processor, Cadre Corp's GDPR Article 30 obligation requires maintaining:

A. A list of all software licenses used in the lab  
B. Records of Processing Activities (RoPA) documenting: the controller (client), purposes of processing, categories of data subjects and personal data, recipients of the data, cross-border transfers and safeguards, and retention periods  
C. A list of all employees who have ever accessed any data  
D. An annual report filed with the EU Commission

---

## Answer Explanations

**Answer 1: B**  
The 72-hour clock starts at **awareness**, not at the time of the breach itself. If a breach occurred on Monday but wasn't discovered until Friday, the clock starts Friday. "Awareness" means Cadre Corp has a reasonable degree of certainty that a breach involving personal data has occurred — not just a suspicion. This is critical operationally: detection time directly impacts notification compliance. If your MTTD is 73 days, you've been in breach of the notification requirement for 72 days and 21 hours.

**Answer 2: B**  
Cross-border transfers to the US require a **valid transfer mechanism** — typically SCCs with a Transfer Impact Assessment (TIA) evaluating whether US surveillance laws provide "essentially equivalent" protection (per Schrems II). The EU-US Data Privacy Framework provides adequacy for certified entities only, not blanket adequacy. Cadre Corp must either be DPF-certified or use SCCs + TIA. The client (controller) must be informed of and authorize all transfer destinations, including sub-processors like the cloud backup provider.

**Answer 3: B**  
Access to personal data (including metadata — usernames, hostnames, file paths that identify individuals) must follow the **principle of least privilege** and data minimization. If only 3 analysts are assigned to the EuroMfg case, the other 7 SOC analysts have no legitimate need to see that case's metadata in dashboards. Role-based access controls, case-level data segregation, and need-to-know access grants are required. Metadata IS personal data under GDPR if it can identify an individual (username = direct identifier, file path containing employee name = indirect identifier).

**Answer 4: B**  
Article 30 requires processors to maintain **Records of Processing Activities (RoPA)**. This is a specific, structured document — not just a policy statement. It must include: controller identity, processing purposes, data subject categories, personal data categories, recipient categories, cross-border transfers with safeguards, and retention periods. It must be provided to supervisory authorities on request. This is a mandatory compliance document, not optional.

---

## Cadre Corp Application

1. **RoPA Creation:** Create a Records of Processing Activities document for the EuroMfg engagement template, covering: (a) controller = EuroMfg GmbH, (b) purpose = insider threat forensic investigation, (c) data subjects = EuroMfg employees, (d) data categories = HR records, system logs, email, file metadata, (e) recipients = assigned DFIR analysts, EuroMfg legal team, (f) transfers = US (Cadre Corp servers) + US cloud backup (sub-processor), safeguards = SCCs + TIA + encryption, (g) retention = per engagement contract + 90 days post-case-closure for QA.

2. **Breach Notification Procedure:** Document the 72-hour workflow: (a) detection → (b) assess whether personal data is involved → (c) if yes, clock starts → (d) notify controller (EuroMfg) "without undue delay" → (e) controller notifies supervisory authority within 72 hours → (f) if high risk to data subjects, controller notifies affected individuals. Cadre Corp as processor must assist the controller.

3. **Elastic Dashboard Access Control:** Implement role-based access in Elastic: case-level index permissions so only the assigned case team sees that case's data. SOC analysts without case assignment see aggregated metrics only, not per-case metadata.

---

## Interview Talking Points

1. **Awareness Starts the Clock:** "The 72-hour GDPR notification clock doesn't start when the breach happens — it starts when you KNOW about it. If your detection is slow, you're already in violation before you begin. This is why dwell time isn't just a security metric — it's a compliance metric."

2. **Processor ≠ No Obligations:** "Being a data processor doesn't mean the controller handles everything. We have independent obligations: RoPA, breach notification assistance, cross-border transfer safeguards, and sub-processor disclosure. The client can't comply without our cooperation — and regulators will come after both of us."

3. **Metadata Is Personal Data:** "Usernames, hostnames, file paths containing employee names — all of it is personal data if it can identify a living person. Access to Elastic dashboards showing EU client metadata is access to personal data. Treat it accordingly."
