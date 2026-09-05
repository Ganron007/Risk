# R-EX-029 — Symmetric vs asymmetric encryption use cases

**CISSP Reference:** Chapter 6, Sections "Symmetric Cryptography" and "Asymmetric Cryptography", Pages 425–480  
**Exam Objective:** 3.5.1 Understand cryptographic concepts; 3.5.2 Apply cryptography to protect information  
**Study Guide Key Terms:** Symmetric encryption, asymmetric encryption, AES, RSA, ECC, key exchange, hybrid cryptography, TLS handshake  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`config/asset-inventory.csv`](../../config/asset-inventory.csv)

---

## Scenario Context

Cadre Corp's infrastructure team is designing a new secure file transfer system for delivering forensic reports to clients. The system must:

1. Encrypt reports (50–500 MB disk images and memory dumps) in transit and at rest.
2. Allow clients to decrypt using credentials they already have (their Entra ID / Azure AD identity).
3. Support automated nightly batch transfers of SIEM telemetry to clients' SIEM instances.
4. Ensure that a compromised Cadre Corp server cannot decrypt reports already delivered to clients.

The junior infrastructure engineer proposed: "Let's just use AES-256 for everything — it's the strongest and fastest." The senior architect countered: "You can't just AES everything — key distribution will kill us at scale." The CISO has asked you to evaluate the appropriate use of symmetric vs asymmetric encryption for each component of this system.

---

## Multiple-Choice Questions

**Question 1:** For encrypting a 500 MB forensic disk image for a single client recipient, which encryption approach is most appropriate?

A. Encrypt the entire file with RSA-4096  
B. Encrypt the file with AES-256 (symmetric), then encrypt the AES key with the client's RSA public key (hybrid)  
C. Encrypt the file with AES-256 and email the passphrase to the client  
D. Use ECC for the file encryption — it's faster than AES for bulk data

**Question 2:** The automated nightly SIEM telemetry transfer to 120 client SIEMs poses a key management challenge. Which approach best addresses this at scale?

A. Generate a unique AES-256 key per client, store all keys in a central database encrypted with a master key  
B. Use a single shared AES-256 key for all 120 clients to simplify operations  
C. Use asymmetric encryption — each client provides their public key, Cadre Corp encrypts telemetry with it, no shared symmetric key needed  
D. Use TLS 1.3 for transport only, store data unencrypted at rest on the client side

**Question 3:** What is the PRIMARY reason AES-256 alone is insufficient for the forensic report delivery system?

A. AES-256 is too slow for 500 MB files  
B. AES-256 has known vulnerabilities in certain implementations  
C. AES-256 cannot solve the key distribution problem — both parties need the same secret key  
D. AES-256 is not approved for forensic evidence under NIST standards

**Question 4:** ECC (Elliptic Curve Cryptography) would be preferred over RSA for the client key pair because:

A. ECC provides stronger encryption than RSA for equivalent key sizes  
B. ECC keys are significantly smaller (256-bit ECC ≈ 3072-bit RSA security) with faster operations  
C. ECC is quantum-resistant while RSA is not  
D. ECC is required by GDPR for personal data encryption

---

## Answer Explanations

**Answer 1: B**  
The **hybrid approach** is the correct answer. AES-256 encrypts the bulk data efficiently (symmetric encryption is orders of magnitude faster for large data). The AES key (just 256 bits) is then encrypted with the client's RSA (or ECC) public key. This gives you: (a) AES speed for bulk data, (b) asymmetric key distribution (only the client with the private key can decrypt the AES key), and (c) forward secrecy if keys are rotated. RSA-4096 directly on 500 MB (A) would be impractically slow. Emailing the passphrase (C) is a key distribution anti-pattern. ECC for bulk data (D) is wrong — asymmetric ciphers are not used for bulk encryption.

**Answer 2: C**  
**Per-client asymmetric encryption** is the correct approach at scale. Each client generates a key pair, provides Cadre Corp their public key, and Cadre Corp encrypts their specific telemetry with that public key. Only the client with the corresponding private key can decrypt. No shared symmetric key management, no central key database to compromise. Option A (central key DB) creates a single point of key compromise. Option B (shared key) means one client breach exposes all 120 clients' telemetry. Option D (TLS only, no at-rest encryption) fails the at-rest encryption requirement.

**Answer 3: C**  
AES-256's fundamental limitation is the **key distribution problem**: both sender and receiver need the same secret key, and securely sharing that key at scale (120 clients) is the hard part. This is why TLS, PGP, and virtually all modern cryptosystems use asymmetric cryptography for key exchange and symmetric for bulk data. AES is fast (A is false), has no known practical vulnerabilities when properly implemented (B is false), and is NIST-approved (D is false).

**Answer 4: B**  
ECC provides equivalent security to RSA with **much smaller keys**: a 256-bit ECC key provides security comparable to a 3072-bit RSA key. This means faster key generation, faster operations, and lower bandwidth for certificate transmission. ECC is NOT quantum-resistant (C is false — Shor's algorithm breaks both RSA and ECC equally). ECC is not specifically required by GDPR (D is false). ECC doesn't provide "stronger" encryption (A is misleading — it provides comparable security at smaller key sizes).

---

## Cadre Corp Application

1. **Hybrid Encryption for Evidence Delivery:** Cadre Corp's forensic report delivery should use: (a) per-file AES-256-GCM for bulk encryption, (b) per-client ECC (Curve25519) public key for AES key wrapping, (c) TLS 1.3 for transport. This provides confidentiality, integrity (GCM authentication tag), and forward secrecy.

2. **Key Management in Ansible:** The Ansible vault that stores lab secrets (`ansible/files/cadre_passwords.txt`) is a symmetric encryption use case — one organization, one secret. But if Cadre Corp needed to share lab configurations with an external auditor, this becomes a key distribution problem requiring asymmetric encryption.

3. **PKI Context:** Cadre Corp's ADCS deployment (AST-034) is the on-prem PKI infrastructure. Understanding asymmetric cryptography is essential for evaluating RISK-002 (ADCS ESC abuse) — certificate templates, key archival, and enrollment agents all depend on asymmetric key management.

4. **Cloud Key Management:** For Azure-based evidence stores (R-EX-025), Azure Key Vault provides HSM-backed key management for both symmetric (AES) and asymmetric (RSA/ECC) keys. The shared responsibility model means Cadre Corp manages key access policies; Microsoft manages HSM physical security.

---

## Interview Talking Points

1. **Hybrid Is How the Internet Works:** "Nobody encrypts bulk data with RSA. TLS, PGP, S/MIME — they all use symmetric for data and asymmetric for key exchange. Understanding WHY is the difference between someone who's read about crypto and someone who can design with it."

2. **Key Distribution Is the Hard Part:** "AES-256 is fast and secure. The problem isn't the cipher — it's getting the key to the right person without exposing it. Asymmetric crypto solves key distribution. Symmetric crypto solves bulk encryption. Use each for what it's good at."

3. **ECC > RSA for Modern Systems:** "At comparable security levels, ECC keys are a fraction the size of RSA keys. For a DFIR firm sending reports to clients' mobile devices or low-bandwidth environments, that matters. RSA isn't wrong — ECC is just more efficient."

4. **Scale Changes Everything:** "One symmetric key for 120 clients? That's not a key — that's a liability. At scale, per-client asymmetric encryption is the only architecture that doesn't create a single point of key compromise."
