# R-EX-017 — Client evidence lifecycle

**CISSP Reference:** Chapter 5, Sections "Data Protection Methods", "Data Lifecycle", Pages 395–415  
**Exam Objective:** 2.1.2 Establish information and asset handling requirements; 2.1.3 Manage data lifecycle  
**Study Guide Key Terms:** Data lifecycle, create, store, use, share, archive, destroy, chain of custody, data retention, crypto-shredding  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md), RISK-007, RISK-017

---

## Scenario Context

Cadre Corp's DFIR practice handles client forensic evidence through a defined lifecycle: **Create** (forensic imaging), **Store** (evidence repositories), **Use** (analysis), **Share** (client deliverables), **Archive** (long-term retention), and **Destroy** (end-of-retention disposal). Each stage requires specific controls to maintain chain of custody (CoC) and prevent evidence compromise (RISK-007).

Recently, three lifecycle failures were discovered:

1. **Create failure:** An analyst imaged a client laptop without a write blocker and didn't record the acquisition hash. The evidence cannot be cryptographically verified as identical to the original — potentially inadmissible.

2. **Archive failure:** A 2022 case was archived to an external hard drive and stored in a desk drawer. The drive was discovered during an office move — unencrypted, unlabeled, and containing PII from 45 EU citizens (potential GDPR breach notification requirement).

3. **Destroy failure:** When a client requested evidence destruction per their data retention policy, the DFIR Lead deleted the files from the evidence share but forgot about the backup copies on the cloud backup provider and the analyst's local working copy. The client's data still exists in three locations.

The CISO asks you to design controls for each lifecycle stage that would prevent these failures.

---

## Multiple-Choice Questions

**Question 1:** At the Create stage, a forensic acquisition hash (SHA-256) serves what PRIMARY purpose?

A. It compresses the forensic image to save storage space  
B. It provides a cryptographic fingerprint of the evidence at the moment of acquisition — enabling verification at any future point that the evidence has not been modified since collection  
C. It encrypts the evidence for secure storage  
D. It catalogs the evidence for inventory purposes

**Question 2:** The 2022 archived drive (unencrypted, unlabeled, in a desk drawer) violates which combination of data lifecycle controls?

A. Only the destroy stage — the data should have been destroyed by now  
B. Both store and archive controls — storage media must be encrypted, labeled with classification and retention date, and stored in access-controlled facilities; a desk drawer is none of these  
C. Only the create stage — the acquisition was flawed  
D. The share stage — the drive was shared inappropriately

**Question 3:** The destruction failure (data still exists in three locations after "deletion") demonstrates why data destruction requires:

A. A single delete command issued by the data owner  
B. A documented destruction process that accounts for ALL copies — primary storage, backups, cloud replicas, analyst working copies, and offline archives — with verification that each copy is irrecoverably destroyed  
C. Simply waiting for the backups to expire naturally  
D. Destruction is only required for Restricted data, not all evidence

**Question 4:** What control at the Share stage ensures client deliverables don't create uncontrolled data copies?

A. Emailing forensic reports as unencrypted PDF attachments  
B. Delivering reports through an authenticated, encrypted client portal with access logging and automatic expiration of shared links — preventing email forwarding, unauthorized downloads, and perpetual access  
C. Printing reports and mailing physical copies  
D. Posting reports to a public-facing website behind a password

---

## Answer Explanations

**Answer 1: B**  
The acquisition hash provides a **cryptographic integrity baseline**. At any point in the evidence lifecycle — during analysis, before sharing with the client, or years later in archive — the hash can be recalculated and compared to the original. A match proves the evidence hasn't been altered. This is the foundation of forensic admissibility and chain of custody. It does not compress (A), encrypt (C), or merely catalog (D) the evidence.

**Answer 2: B**  
The 2022 archive violates **storage and archival controls**: (a) no encryption — anyone with physical access to the desk drawer can read the data, (b) no labeling — the drive wasn't identified as containing Restricted client evidence with PII, (c) no access control — a desk drawer is not a secured storage facility, (d) no retention tracking — nobody knew what was on the drive or when it should be destroyed. This is a cascading failure of the Archive stage.

**Answer 3: B**  
Data destruction requires **comprehensive copy accounting**. Deleting the primary copy is not destruction if copies exist in: cloud backups (retained per provider policy), analyst working directories (forgotten local copies), offline archives (the desk drawer drive), and backup snapshots. A proper destruction process: (a) inventory all copies, (b) crypto-shred (encrypt then destroy keys) or physical destruction for each, (c) verify destruction, (d) issue destruction certificate to the client. Waiting for backups to expire (C) may violate the client's retention policy and GDPR's "right to erasure."

**Answer 4: B**  
An **authenticated, encrypted client portal** with access controls prevents uncontrolled proliferation. Email attachments (A) can be forwarded, downloaded to personal devices, and persist in inboxes indefinitely. Physical mail (C) creates uncontrolled physical copies. Password-protected public websites (D) are trivial to brute-force or share. The portal provides: authentication (only authorized recipients), encryption (TLS in transit + at rest), access logging (audit trail), and expiration (automatic revocation of access per retention policy).

---

## Cadre Corp Application

1. **Lifecycle Control Matrix:** For each evidence lifecycle stage, document: (a) required controls, (b) responsible role, (c) verification step, (d) failure mode and response. Example — Create: acquisition hash (control) → DFIR Analyst (role) → hash verified by second analyst (verification) → if missing, evidence flagged as non-forensic and client notified (response).

2. **Archive Hygiene:** All archived evidence must be: encrypted (AES-256), labeled (case ID, classification, retention date, destruction date), stored in access-controlled facilities (not desk drawers), and inventoried in a searchable catalog. The 2022 desk-drawer drive is a RISK-007 trigger event — immediate remediation required.

3. **Destruction Certificate Process:** When a client requests evidence destruction: (a) identify all copies (primary, backup, cloud, analyst local, offline archive), (b) crypto-shred or physically destroy each, (c) verify destruction, (d) issue a signed destruction certificate with dates and methods, (e) retain the certificate (not the data) for audit purposes.

---

## Interview Talking Points

1. **Deletion Is Not Destruction:** "Deleting a file from the evidence share is not destruction — it's hiding. True destruction means you can prove, with certificates, that every copy across every system has been irrecoverably destroyed. If you can't prove it, you haven't done it."

2. **Every Lifecycle Stage Has a Failure Mode:** "The desk drawer drive wasn't a one-off mistake — it was a systemic Archive stage failure. No encryption, no labeling, no inventory, no access control. When you design lifecycle controls, design for the failure mode at each stage, not just the happy path."

3. **The Hash Is the Foundation:** "Everything in forensic evidence handling builds on the acquisition hash. Without it, you can't prove integrity at any subsequent stage. It's the first control you apply and the last control you verify. If the hash is missing, the evidence is forensically unsound."
