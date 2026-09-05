# R-EX-030 — Hash functions and digital signatures

**CISSP Reference:** Chapter 6, Sections "Hash Functions" and "Digital Signatures", Pages 450–470; Chapter 7, Sections "Digital Signatures" and "PKI"  
**Exam Objective:** 3.5.2 Apply cryptography to protect information; 3.5.3 Understand public key infrastructure  
**Study Guide Key Terms:** Hash functions, SHA-256, SHA-3, collision resistance, digital signatures, non-repudiation, HMAC, message authentication  
**Inputs:** [`../risk-register-baseline.md`](../risk-register-baseline.md), [`../enterprise-context.md`](../enterprise-context.md)

---

## Scenario Context

Cadre Corp's DFIR evidence handling chain relies on cryptographic integrity verification at three critical points:

1. **Evidence intake:** When a client ships a disk for forensic imaging, Cadre Corp must prove the disk image is an exact copy — no tampering, no corruption. Currently, the lab technician runs `sha256sum` and emails the hash to the client. The client has no way to verify the email wasn't tampered with.

2. **Chain of custody (CoC):** Each evidence transfer between analysts must be logged with a cryptographic verification that the evidence hasn't changed since the last handler. The current process uses MD5 hashes (chosen "because it's fast"), and logs are stored in a shared Excel file anyone can edit.

3. **Forensic report signing:** Final reports delivered to clients must be provably from Cadre Corp and provably unmodified. Currently, the DFIR Lead prints the report, signs it with a pen, and scans it back to PDF — the digital PDF has no cryptographic signature.

The SOC 2 auditor has flagged all three as material weaknesses in evidence integrity controls. You have been asked to redesign the cryptographic integrity chain using proper hash functions and digital signatures.

---

## Multiple-Choice Questions

**Question 1:** Cadre Corp's use of MD5 for chain-of-custody hashing is problematic because:

A. MD5 is too slow for forensic-sized files  
B. MD5 is cryptographically broken — collisions can be generated, allowing evidence tampering without hash change  
C. MD5 produces hashes that are too long for CoC logs  
D. MD5 is proprietary and requires licensing fees

**Question 2:** When the lab technician emails a SHA-256 hash to the client for evidence verification, what security property is MISSING?

A. Confidentiality — the hash is sent in cleartext  
B. Integrity and authenticity — the email itself could be tampered with; the client has no way to verify the hash came from Cadre Corp  
C. Availability — email is not a guaranteed delivery mechanism  
D. The SHA-256 algorithm is insufficient for forensic evidence

**Question 3:** A digital signature on a forensic report provides which two security properties that a hand-signed scanned PDF does NOT?

A. Confidentiality and availability  
B. Integrity (proof the report hasn't been modified) and non-repudiation (proof Cadre Corp signed it)  
C. Speed and efficiency of signing  
D. Compression and archival compatibility

**Question 4:** Which of the following best describes the relationship between a hash function and a digital signature?

A. The digital signature IS the hash of the document  
B. The document is hashed, and the hash is encrypted with the signer's private key — the resulting ciphertext is the signature  
C. The hash and signature are independent — you can have one without the other  
D. The signature replaces the hash — you don't need both

---

## Answer Explanations

**Answer 1: B**  
MD5 is **cryptographically broken**. Since 2004, researchers have demonstrated practical collision attacks — two different files can produce the same MD5 hash. For chain of custody, this means an attacker could replace evidence with a tampered version that produces the identical MD5 hash, defeating the integrity check. SHA-256 (or SHA-3) should be used instead. MD5 is fast (A is false) but broken. Hash length (C) and licensing (D) are not issues.

**Answer 2: B**  
The email provides no **integrity or authenticity** for the hash itself. An attacker who can intercept or spoof the email can replace both the evidence AND the hash value, making the verification meaningless. The solution: sign the hash with Cadre Corp's private key (digital signature) or publish it via an authenticated channel (client portal with TLS + authentication). The hash being cleartext (A) is fine — hashes don't need confidentiality. SHA-256 is appropriate for forensic use (D is false).

**Answer 3: B**  
A digital signature provides **integrity** (any modification to the report invalidates the signature — mathematically provable) and **non-repudiation** (Cadre Corp cannot deny signing because only they possess the private key). A scanned pen signature provides neither — the PDF can be modified after scanning, and a pen signature can be copied/forged. Confidentiality (A) is not a property of digital signatures. Speed (C) isn't the primary benefit.

**Answer 4: B**  
The correct process: (1) hash the document with SHA-256, (2) encrypt the hash with the signer's private key, (3) the encrypted hash IS the digital signature. Verification: (1) decrypt the signature with the signer's public key to get the original hash, (2) independently hash the document, (3) compare — if they match, the document is intact and authentically signed. This is how TLS, S/MIME, code signing, and PKI all work.

---

## Cadre Corp Application

1. **Evidence Hash Publishing:** Instead of emailing hashes, publish evidence hashes to the client portal (authenticated, TLS-encrypted) or sign them with a Cadre Corp code-signing certificate from the ADCS CA (AST-034). The client can verify the signature independently.

2. **CoC Hash Upgrade:** Replace MD5 with SHA-256 (or BLAKE3 for performance on large forensic images). Store hashes in an append-only, cryptographically verifiable log — the DFIR-Nexus audit chain (`HMAC-SHA256` with `prev_hash` linking) is an existing implementation that could be adapted.

3. **Report Signing with ADCS:** Cadre Corp's ADCS deployment can issue code-signing or document-signing certificates. Tools like `gpg --sign` or S/MIME in Outlook can produce cryptographically signed PDFs using these certificates. This directly leverages the existing PKI investment.

4. **Hash Function Selection:** For forensic use, SHA-256 is the minimum. SHA-512 for long-term archival. Avoid SHA-1 (deprecated) and MD5 (broken). The control `CTL-COC` in `docs/control-register.md` should specify the approved hash algorithms.

---

## Interview Talking Points

1. **MD5 Is Negligence in 2026:** "If I see MD5 in a chain-of-custody log, I know nobody's reviewed the crypto controls in 20 years. MD5 has been broken since 2004. Using it for forensic evidence integrity is professional negligence."

2. **Hash + Signature, Not Hash OR Signature:** "A hash proves the file hasn't changed. A signature proves who vouched for the hash. You need both. An unsigned hash is just a number anyone could have written down."

3. **Non-Repudiation Is the Killer Feature:** "A pen signature on a scanned PDF doesn't prove I signed THAT version of the report — I can always claim the PDF was modified after scanning. A digital signature is mathematically tied to the exact bytes. That's non-repudiation."

4. **Our ADCS PKI Already Supports This:** "We invested in a certificate authority. Document-signing certificates are a standard template. The infrastructure exists — we just need to use it for evidence integrity instead of just domain authentication."
