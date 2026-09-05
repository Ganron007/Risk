# R-EX-043 — Data minimization principles

**CISSP Reference:** Chapter 5, Section "Data Protection Methods", Pages 395–410; GDPR Article 5(1)(c)  
**Exam Objective:** 2.1.2 Establish information and asset handling requirements; 1.4.2 Understand legal and regulatory issues  
**Study Guide Key Terms:** Data minimization, collection limitation, purpose limitation, GDPR Article 5, data retention, need-to-know, proportionality  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../regulatory-obligations.md`](../regulatory-obligations.md), [`config/asset-inventory.csv`](../../config/asset-inventory.csv)

---

## Scenario Context

Cadre Corp's DFIR analysts have a habit of "collect everything, just in case." When imaging a client laptop for an insider threat investigation, the standard practice is:

1. Full disk image (500 GB) — including the employee's personal photos, tax returns, and family videos mixed with corporate data.
2. Memory dump (32 GB) — capturing browser sessions with personal banking URLs and saved passwords.
3. Network packet capture (50 GB) — covering 72 hours of the employee's home network traffic, including their smart TV streaming and kids' gaming sessions.

Only about 15% of the collected data is relevant to the investigation. The other 85% is the employee's personal life — unnecessarily collected, stored on Cadre Corp's evidence servers, and accessible to the DFIR team.

A GDPR-subject client (EuroMfg GmbH, see R-EX-023) has challenged Cadre Corp's collection scope: "Why did you image my employee's entire personal life for a corporate insider threat investigation? Under GDPR Article 5(1)(c), you must limit collection to what is adequate, relevant, and limited to what is necessary."

---

## Multiple-Choice Questions

**Question 1:** GDPR Article 5(1)(c) establishes the principle of data minimization. Which of the following BEST describes this principle?

A. Data should be encrypted using the minimum acceptable algorithm strength  
B. Personal data must be adequate, relevant, and limited to what is necessary in relation to the purposes for which they are processed  
C. Data should be stored for the minimum time required by law  
D. Only the minimum number of employees should have access to personal data

**Question 2:** Cadre Corp's "collect everything, just in case" forensic imaging practice violates data minimization because:

A. Forensic imaging is always a GDPR violation  
B. The collection scope is not limited to what is necessary for the stated purpose (insider threat investigation) — 85% of the collected data (personal photos, family videos, banking sessions) is irrelevant to the investigation and constitutes excessive collection  
C. Disk imaging is slower than targeted file collection  
D. Full disk images cannot be encrypted

**Question 3:** Which technical control would BEST enable Cadre Corp to comply with data minimization during forensic collection?

A. Faster imaging hardware to reduce collection time  
B. Targeted forensic collection — use pre-imaging triage (file system metadata analysis, keyword search, timeline filtering) to identify and collect only data relevant to the investigation scope, rather than blindly imaging the entire disk  
C. Encrypting the full disk image after collection  
D. Deleting all collected data after 30 days regardless of relevance

**Question 4:** How does data minimization relate to the broader principle of purpose limitation under GDPR?

A. They are unrelated principles  
B. Purpose limitation defines WHY you collect data (specified, explicit, legitimate purposes); data minimization defines HOW MUCH you collect (limited to what's necessary for that purpose) — you cannot minimize without first defining the purpose  
C. Purpose limitation is optional; data minimization is mandatory  
D. Purpose limitation only applies to marketing data

---

## Answer Explanations

**Answer 1: B**  
GDPR Article 5(1)(c) requires that personal data be **"adequate, relevant, and limited to what is necessary in relation to the purposes for which they are processed."** This is the data minimization principle. It's not about encryption (A), storage duration (C — that's storage limitation, Article 5(1)(e)), or access control (D — that's integrity and confidentiality, Article 5(1)(f)). It's about not collecting more than you need.

**Answer 2: B**  
The violation is **disproportionate collection**. For an insider threat investigation, relevant data includes: corporate documents accessed by the employee, email communications about sensitive projects, USB device connection history, and recently executed files. It does NOT include: the employee's family vacation photos, personal tax returns, children's gaming traffic, or smart TV streaming logs. Collecting 85% irrelevant personal data is the textbook definition of failing data minimization. Forensic imaging is not always a violation (A — it's about scope, not technique).

**Answer 3: B**  
**Targeted forensic collection** is the correct technical control. Modern forensic tools support: (a) file system metadata analysis before imaging — identify relevant file types, date ranges, and paths, (b) keyword indexing of the live disk to scope collection, (c) logical acquisition (collecting specific files/folders) vs. physical acquisition (full disk image), (d) automated filtering during collection to exclude known irrelevant data types (e.g., `*.jpg` in `Pictures/` folders unless specifically in scope). Encryption after collection (C) doesn't address over-collection. Deleting everything after 30 days (D) compounds the problem — you collected excessively AND destroyed potentially relevant evidence.

**Answer 4: B**  
**Purpose limitation and data minimization are complementary, sequential principles.** First, define the purpose: "investigate whether Employee X exfiltrated Project Y files to a competitor between March 1–15, 2026." Then, minimize collection to what's necessary for THAT purpose: (a) files modified in that date range, (b) email attachments sent externally, (c) USB device connection history, (d) cloud storage sync logs. Without a clear purpose, you can't determine what's "necessary" — and without minimization, you collect everything, which is the current Cadre Corp practice.

---

## Cadre Corp Application

1. **Collection Scope Documentation:** Before every forensic collection, document: (a) the specific investigation purpose (who, what, when), (b) the data categories needed to answer the investigation questions, (c) the data categories explicitly OUT of scope (personal photos, personal communications unrelated to work, etc.). This document becomes part of the chain of custody and demonstrates GDPR compliance.

2. **Targeted Collection Tools:** Add to the DFIR toolkit: (a) `fdump.py` or similar for pre-imaging file system metadata analysis, (b) keyword-based triage collection scripts, (c) automated PII/personal file detection during imaging (flag and exclude family photos, tax documents, etc., with examiner review).

3. **Proportionality Review:** Add a "proportionality check" to the evidence intake workflow: before imaging begins, a second analyst reviews the collection scope and confirms it's proportional to the investigation purpose. This provides four-eyes validation and an audit trail.

4. **Client Communication:** When clients push for "image everything," educate them on GDPR risk: excessive collection creates liability for BOTH the client (controller) and Cadre Corp (processor). A documented, minimized collection scope protects both parties.

---

## Interview Talking Points

1. **'Collect Everything' Is a Liability, Not a Strategy:** "The instinct to image everything 'just in case' creates more legal risk than it solves. Every gigabyte of irrelevant personal data we collect is a gigabyte we're liable for protecting, a gigabyte that could be subpoenaed, and a gigabyte that violates GDPR's data minimization principle. Targeted collection isn't lazy — it's legally required."

2. **Purpose First, Collection Second:** "You can't minimize what you haven't scoped. Define the investigation purpose with precision — who, what, when, which systems — THEN collect only what serves that purpose. 'We're investigating an insider threat' is not a purpose. 'We're determining whether Employee X exfiltrated Project Y files between March 1–15 via USB or email' is a purpose you can minimize against."

3. **Proportionality Is a Four-Eyes Check:** "Before any forensic image is taken, a second analyst reviews the scope and asks: is this proportional? Are we imaging an entire 500 GB disk when 20 GB of relevant files would answer the question? That conversation takes 10 minutes and prevents months of legal exposure."
