# R-EX-081 — Forensic evidence collection and preservation

**CISSP Reference:** Chapter 19, Sections "Investigations", "Evidence Collection"  
**Exam Objective:** 7.5.1 Conduct forensic investigations; 7.5.2 Preserve evidence integrity  
**Study Guide Key Terms:** Chain of custody, order of volatility, evidence preservation, forensic imaging, write blocker, hash verification, admissible evidence  

---

## Scenario Context

Cadre Corp IS a DFIR firm — forensic evidence handling is its core business. Yet during a recent internal review, the CISO discovered that evidence handling practices vary wildly between analysts:

1. Analyst A images disks using a hardware write blocker, generates SHA-256 hashes before and after, and logs every transfer in the chain-of-custody system.
2. Analyst B plugs client drives directly into their workstation USB port (no write blocker), drags files to their desktop, and records transfers in a text file named `evidence-log.txt`.
3. Analyst C uses `dd` over the network to image a live system but doesn't record the exact command, timestamp, or hash — "I'll document it later" (never does).

The CISO asks: "If Analyst B's evidence were challenged in court, would it be admissible? And if not, what's the liability to our clients?"

---

## Multiple-Choice Questions

**Question 1:** The "order of volatility" in forensic evidence collection refers to:

A. The alphabetical order of evidence types  
B. Collecting the most volatile evidence first — CPU registers/cache → RAM → network state → running processes → disk — because volatile data disappears quickly and cannot be recovered later  
C. Collecting disk evidence before memory evidence  
D. The order in which evidence is presented in court

**Question 2:** A hardware write blocker is used during forensic imaging to:

A. Speed up the imaging process  
B. Prevent any write commands from reaching the evidence drive — ensuring the original evidence is not modified (even accidentally) during the imaging process, preserving its integrity for legal admissibility  
C. Encrypt the forensic image  
D. Compress the image to save storage space

**Question 3:** For forensic evidence to be admissible in court, it must generally demonstrate:

A. That it was collected quickly  
B. A documented, unbroken chain of custody; verifiable integrity (cryptographic hashes); collection by qualified personnel following accepted procedures; and no evidence of tampering or alteration  
C. That the suspect confessed  
D. That the evidence was collected by law enforcement

---

## Answer Explanations

**Answer 1: B**  
**Order of volatility** prioritizes evidence by how quickly it disappears. CPU registers and cache vanish in nanoseconds; RAM contents disappear when power is lost; network connections time out; running processes terminate; disk data persists for years. Collecting volatile evidence first ensures you capture what will be gone if you start with the disk image. This is a fundamental forensic principle.

**Answer 2: B**  
A **write blocker** physically or logically prevents any write command from reaching the evidence drive. This ensures the original evidence remains pristine — even accidental writes (Windows mounting the drive and updating last-accessed timestamps, antivirus scanning) are blocked. The forensic image's hash is compared to the original; if they match, the copy is forensically sound. Analyst B's direct USB connection likely modified the evidence drive's metadata.

**Answer 3: B**  
Courts require: **unbroken chain of custody** (who had the evidence, when, where, why — documented from collection to courtroom), **verifiable integrity** (cryptographic hashes proving the evidence hasn't changed), **qualified collection** (trained personnel using accepted tools and procedures), and **no evidence of tampering**. Analyst B's `evidence-log.txt` with no hashes, no write blocker, and informal handling would likely fail admissibility challenges.

---

## Cadre Corp Application

1. **Standardized Evidence Handling SOP:** Mandate: (a) hardware write blocker for all disk imaging, (b) SHA-256 hash before and after imaging, (c) documented chain of custody in the DFIR-Nexus system (or equivalent) — not text files, (d) order of volatility for live system collection, (e) dual-verification for critical evidence.

2. **Analyst B Remediation:** Analyst B's methods are a RISK-007 (client evidence breach / CoC failure) trigger. Immediate retraining, audit of all evidence handled by Analyst B for potential integrity issues, and client notification if evidence integrity cannot be verified.

3. **Court-Ready by Default:** All forensic evidence should be collected as if it will be challenged in court — even if litigation isn't anticipated. The cost of proper collection is negligible compared to the cost of inadmissible evidence in a client's legal case.

---

## Interview Talking Points

1. **"I'll Document It Later" = Evidence Integrity Failure:** "Forensic evidence documentation isn't paperwork — it's the foundation of legal admissibility. If you didn't document it at the time, it didn't happen. Every transfer, every hash, every access must be contemporaneously recorded."

2. **Write Blocker or Wrong:** "Plugging a client's evidence drive directly into your workstation is professional negligence for a DFIR firm. You've modified the evidence, broken chain of custody, and potentially made it inadmissible. That's not just a process failure — that's a client liability."
