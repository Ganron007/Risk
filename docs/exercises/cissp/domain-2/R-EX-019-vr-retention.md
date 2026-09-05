# R-EX-019 — Velociraptor artifact retention policy

**CISSP Reference:** Chapter 5, Sections "Data Retention", "Data Protection Methods", Pages 395–415; GDPR Article 5(1)(e) — Storage Limitation  
**Exam Objective:** 2.1.4 Manage data retention; 2.1.2 Establish information and asset handling requirements  
**Study Guide Key Terms:** Data retention, storage limitation, retention schedule, data minimization, legal hold, retention policy exception, crypto-shredding  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md), RISK-008, AST-032

---

## Scenario Context

Cadre Corp's Velociraptor server (AST-032, classified Restricted) stores forensic artifacts collected from client investigations: memory dumps, registry hives, prefetch files, event logs, and browser histories. The current collection contains artifacts from 85 closed cases spanning 4 years — approximately 18 TB of data.

The CISO recently discovered that:

1. **No retention policy exists.** Artifacts are kept indefinitely — "disk space is cheap." Some artifacts from 2022 cases contain GDPR-subject PII that should have been deleted per the client's contractual 2-year retention clause.

2. **Legal hold exceptions are undocumented.** Three cases are under active litigation, requiring evidence preservation beyond normal retention — but this isn't tracked anywhere. If an admin follows a blanket "delete everything older than 2 years" policy, they'll destroy evidence under legal hold.

3. **VR artifact access logging is incomplete.** The current logs show WHO accessed artifacts but not WHY — making it impossible to distinguish legitimate case work from unauthorized curiosity browsing during an audit.

GDPR Article 5(1)(e) (Storage Limitation) requires that personal data be "kept in a form which permits identification of data subjects for no longer than is necessary." Four years of PII from closed cases is arguably "longer than necessary."

---

## Multiple-Choice Questions

**Question 1:** GDPR's storage limitation principle requires that personal data be:

A. Stored forever for investigative purposes  
B. Kept no longer than necessary for the purposes for which it was collected — once the investigation is complete and contractual retention expires, data should be deleted or anonymized  
C. Stored for exactly 7 years regardless of purpose  
D. Deleted immediately after the investigation closes

**Question 2:** The three cases under active litigation require evidence preservation beyond normal retention. What is the correct mechanism?

A. Ignore the retention policy for all cases — keep everything "just in case"  
B. Apply a documented legal hold to those specific cases — the legal hold overrides the standard retention schedule and prevents deletion until formally released by legal counsel  
C. Delete the evidence and rely on the client's copy  
D. Move the evidence to a non-Restricted share for easier access during litigation

**Question 3:** VR artifact access logs that show WHO but not WHY create what compliance gap?

A. No gap — knowing who accessed data is sufficient for all frameworks  
B. The inability to distinguish legitimate case work from unauthorized access — during an audit, "Analyst X accessed Case Y artifacts" without a documented purpose could be either appropriate investigation or a privacy violation; the WHY provides the justification  
C. Access logging is not required for forensic tools  
D. Only the WHY matters; WHO is irrelevant

**Question 4:** What is the correct approach to implementing a retention schedule for Velociraptor artifacts?

A. Delete everything after 30 days — simplest approach  
B. Tiered retention based on case status: Active cases — retain while case open; Closed cases — retain per contractual period (typically 90 days to 2 years); Legal hold — retain until hold released; then crypto-shred with destruction verification  
C. Keep everything forever — storage is inexpensive  
D. Let each analyst decide when to delete their case artifacts

---

## Answer Explanations

**Answer 1: B**  
GDPR's storage limitation requires data to be **kept no longer than necessary**. For forensic evidence, "necessary" is defined by: (a) the investigation purpose (once the case is closed and findings delivered, the original purpose is fulfilled), (b) contractual retention (the client engagement may specify a retention period for QA or legal defense), (c) legal obligations. After the longest applicable period expires, data must be deleted or irreversibly anonymized.

**Answer 2: B**  
A **documented legal hold** is the correct mechanism. When litigation is reasonably anticipated, a legal hold: (a) suspends normal retention/deletion policies for specified data, (b) is documented with case reference, scope, and issuing authority (legal counsel), (c) is tracked, (d) is formally released when litigation concludes. Keep-everything (A) violates storage limitation for non-held cases.

**Answer 3: B**  
The **WHY provides purpose justification**. Proper access logging for Restricted forensic data should include: (a) who (analyst identity), (b) what (specific artifacts), (c) when (timestamp), (d) why (case reference, investigation task, or approval ticket). The WHY distinguishes legitimate investigation from unauthorized browsing — critical for SOC 2 and GDPR audits.

**Answer 4: B**  
**Tiered retention based on case status** is correct. Active cases need evidence available for ongoing analysis. Closed cases follow contractual retention. Legal hold cases are preserved until release. Crypto-shredding ensures irrecoverable deletion. This balances operational needs, contractual obligations, GDPR storage limitation, and litigation preservation requirements.

---

## Cadre Corp Application

1. **VR Retention Policy:** Document in `docs/control-register.md`: Active cases = retain while open + 90 days post-closure for QA; Closed cases = per contract (default 2 years max); Legal hold = retain until hold released; Beyond retention = crypto-shred + destruction verification. Automate enforcement via scheduled cleanup scripts with hold-check.

2. **Legal Hold Register:** Track: case ID, hold date, issuing authority, scope, and release date. Integrate with deletion process — scripts check the hold register before removing any artifact.

3. **Access Logging Enhancement:** Configure VR audit logging to capture analyst ID, case reference, artifact ID, timestamp, and purpose. Feed to Elastic for correlation and anomaly detection (alert on closed-case access without active hold or re-opened case).

---

## Interview Talking Points

1. **Storage Limitation Is Not Optional:** "You can't keep EU citizens' browser histories forever because 'disk space is cheap.' GDPR Article 5(1)(e) requires a documented retention schedule and actual deletion when retention expires. Every terabyte past retention is a terabyte of GDPR liability."

2. **Legal Hold Is the Exception, Not the Rule:** "Legal hold suspends deletion for specific cases under specific legal authority. It is NOT a blanket 'keep everything' policy. If all your cases are under legal hold, either you're in constant litigation or you're using it as an excuse to avoid retention obligations."

3. **Access Logs Without Purpose Are Half the Story:** "Knowing WHO accessed evidence tells you who to ask. Knowing WHY tells you whether it was legitimate. During an audit, 'Analyst X accessed Case Y' is a question. 'Analyst X accessed Case Y as part of assigned task Z-1234' is an answer."
