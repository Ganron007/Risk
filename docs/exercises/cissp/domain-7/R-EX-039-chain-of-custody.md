# R-EX-039 — Chain of custody for forensic evidence

**CISSP Reference:** Chapter 19, Sections "Investigations", "Evidence Collection and Preservation", "Chain of Custody"  
**Exam Objective:** 7.5.1 Conduct forensic investigations; 7.5.2 Preserve evidence integrity and chain of custody  
**Study Guide Key Terms:** Chain of custody, evidence integrity, cryptographic hashing, evidence handling, HITL approval, evidence lifecycle, admissibility  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), RISK-007, AST-030, DFIR-Nexus workflow

---

## Scenario Context

Cadre Corp is a DFIR firm — chain of custody (CoC) is not optional; it's the product. If evidence integrity cannot be proven, findings are inadmissible, clients lose cases, and Cadre Corp loses its SOC 2 attestation and its reputation.

A new DFIR analyst received a client hard drive for a corporate espionage investigation. The analyst:

1. Signed for the package at reception and took it to their desk.
2. Plugged the drive directly into their workstation USB port (no write blocker).
3. Imaged the drive using `dd` but didn't record the command, timestamp, or acquisition hash.
4. Copied the image to the evidence share and emailed the client: "Got the drive, starting analysis."
5. Began analysis 30 minutes later. No second person witnessed any step.

The DFIR Lead reviewed this workflow and immediately escalated to the CISO: this evidence is potentially inadmissible and the client must be notified. The CISO asks: "What did we miss, and how do we ensure this never happens again?"

---

## Multiple-Choice Questions

**Question 1:** What is the minimum set of fields a chain of custody record must capture?

A. Only the evidence description  
B. Evidence identifier (case ID, exhibit number), description, custodian (who has it), date/time of custody transfer, reason for transfer, hash value at each transfer, and signature/authentication of both the transferring and receiving custodians  
C. Only the date and time of collection  
D. Only the name of the person who collected the evidence

**Question 2:** The analyst's failure to use a write blocker means:

A. The evidence is still forensically sound — write blockers are optional  
B. The original evidence drive was potentially modified by the analyst's workstation — Windows mounts drives automatically, updating last-accessed timestamps, creating System Volume Information folders, and potentially triggering antivirus scans; these modifications break the chain of custody because the evidence is no longer identical to its original state  
C. The imaging process was faster without a write blocker  
D. Write blockers are only needed for SSD drives

**Question 3:** A cryptographic hash (SHA-256) taken at acquisition serves what specific CoC function?

A. It catalogs the evidence for inventory purposes  
B. It establishes a verifiable integrity baseline — at any future point (during analysis, before court, years later), the hash can be recalculated and compared to the acquisition hash; a match proves the evidence hasn't been modified since the moment of acquisition  
C. It compresses the evidence to save storage  
D. It identifies the type of file system on the evidence drive

**Question 4:** Why is dual-verification (a second analyst witnessing key steps) important for chain of custody?

A. It's a bureaucratic requirement with no practical value  
B. It provides independent corroboration — the second analyst can testify that they witnessed the acquisition, verified the hash, and confirm the evidence wasn't tampered with; this strengthens admissibility and provides defense against accusations of evidence manipulation  
C. It speeds up the acquisition process  
D. It's only required for criminal cases, not civil litigation

---

## Answer Explanations

**Answer 1: B**  
A CoC record must document the **complete custody journey**: (a) What — evidence identifier and description, (b) Who — custodian at each point, (c) When — date/time of every transfer, (d) Why — reason for transfer, (e) Integrity proof — hash value verified at each transfer, (f) Authentication — signature or digital approval of both parties. Without any of these, the chain is broken and evidence admissibility is challenged. The analyst's email ("Got the drive, starting analysis") satisfies none of these requirements.

**Answer 2: B**  
Without a write blocker, the analyst's workstation **modified the original evidence**. Windows automatically: mounts the file system, updates last-accessed timestamps on files, writes System Volume Information, may create thumbs.db files, and antivirus may scan and quarantine files. These modifications — even if unintentional and benign — mean the evidence is no longer a bit-for-bit copy of its original state. The hash taken AFTER these modifications doesn't prove the evidence matches the original — it proves it matches the already-modified version. This is a foundational CoC failure.

**Answer 3: B**  
The acquisition hash is the **integrity anchor** for the entire evidence lifecycle. It proves: "This evidence, as captured at this moment by this custodian, has this cryptographic fingerprint." Every subsequent handler verifies the hash hasn't changed. If the hash ever doesn't match, the evidence has been modified — and the CoC pinpoints which custodian was responsible. Without the acquisition hash, there is no objective integrity proof — only trust in human processes.

**Answer 4: B**  
**Dual verification provides independent witness testimony**. If the evidence is challenged in court, the second analyst can testify: "I witnessed the acquisition. I verified the hash independently. The evidence presented today is the same evidence we collected." This eliminates the accusation that a single analyst could have tampered with evidence. For a DFIR firm whose findings may be used in litigation, dual verification is not bureaucratic — it's professional liability protection.

---

## Cadre Corp Application

1. **CoC Minimum Standard:** Every evidence transfer must record: case ID, evidence ID, description, transferring custodian, receiving custodian, date/time, reason, hash (SHA-256 verified by both parties), and digital signature/approval. DFIR-Nexus provides this workflow with cryptographic audit trail — use it for ALL evidence, not just "important" cases.

2. **Write Blocker Policy:** Hardware write blocker required for ALL physical disk acquisitions. No exceptions. If a write blocker is unavailable, the acquisition is delayed — never performed without one. Software write blocking (Linux `blockdev --setro`) is acceptable for logical acquisitions with documented justification.

3. **Analyst Training + Audit:** The analyst who plugged the client drive directly into their workstation requires immediate retraining on CoC procedures. All their prior cases should be audited for CoC compliance. One analyst's bad practice can invalidate months of forensic work — and create liability for every client whose evidence they handled.

---

## Interview Talking Points

1. **Chain of Custody Is the Product:** "We don't sell forensic analysis. We sell provable truth. Chain of custody is the proof. If the chain is broken — no write blocker, no hash, no witness — the analysis is worthless regardless of how brilliant it is. The client can't use it in court, and we can't defend it under cross-examination."

2. **A Hash Is a Testimony You Can Prove:** "When I testify that evidence hasn't been modified, the hash is my proof. SHA-256 doesn't lie, doesn't forget, and doesn't get confused under cross-examination. Every piece of evidence gets a hash at acquisition. Every transfer verifies it. That's not process — that's the foundation of forensic science."

3. **One Bad Analyst, One Hundred Compromised Cases:** "The analyst who skipped the write blocker didn't just compromise one case — they potentially compromised every case they've ever handled. CoC failures are retroactive. Every client whose evidence that analyst touched now has potentially inadmissible evidence. That's why CoC discipline is non-negotiable."
