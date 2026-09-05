# R-EX-041 — Key management lifecycle

**CISSP Reference:** Chapter 6, Section "Cryptographic Life Cycle", Pages 470–480; Chapter 7, Sections "Asymmetric Key Management" and "PKI"  
**Exam Objective:** 3.5.3 Understand public key infrastructure; 3.5.4 Manage cryptographic keys  
**Study Guide Key Terms:** Key generation, key storage, key distribution, key rotation, key revocation, key destruction, HSM, key escrow, certificate lifecycle  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md)

---

## Scenario Context

Cadre Corp's cryptographic key management is ad-hoc and distributed:

1. **ADCS CA private key (AST-034):** The root CA key for `cadre.local` is stored on DC01's local disk with no HSM protection. If DC01 is compromised (RISK-001), the attacker gets the CA private key and can issue arbitrary certificates.

2. **Ansible vault password:** The password that encrypts all lab secrets (`ansible/files/cadre_passwords.txt`, service account credentials, Ansible vault) is stored in a plaintext file on the provisioning server (AST-013). Anyone with access to provisioning can decrypt all lab secrets.

3. **Client PGP keys for evidence delivery:** When Cadre Corp receives a client's PGP public key for encrypted evidence delivery, the key is saved to the DFIR Lead's Downloads folder with no expiration tracking. Three clients' keys from 2024 have since expired or been revoked, but Cadre Corp still has the old keys and no process to verify current validity.

4. **TLS certificates for internal services:** Elastic, Velociraptor, and Arkime web UIs use self-signed certificates generated at install time — no tracking of expiration dates, no automated renewal. Two services had expired certificates for 45 days before anyone noticed.

The CISO has asked you to design a key management lifecycle that covers generation, storage, distribution, rotation, revocation, and destruction for all cryptographic material in the Cadre Corp estate.

---

## Multiple-Choice Questions

**Question 1:** The ADCS CA private key stored on DC01's local disk without HSM protection violates which key management principle?

A. Key distribution — the key hasn't been distributed to all DCs  
B. Key storage security — private keys for certificate authorities should be stored in hardware security modules (HSMs) or at minimum with strong access controls and encryption  
C. Key generation — the key was generated with insufficient entropy  
D. Key destruction — the key should be deleted after each use

**Question 2:** When a client notifies Cadre Corp that their PGP key has been revoked, what is the CORRECT key lifecycle action?

A. Delete the old key from the Downloads folder immediately  
B. Continue using the old key — revocation only matters for signing, not encryption  
C. Verify the revocation through the key server or client's published CRL, remove the old key, obtain the new key through an authenticated channel, and update the evidence delivery workflow  
D. Ignore the notification — key management is the client's responsibility

**Question 3:** Self-signed TLS certificates on internal services that expired 45 days ago represent a failure in which key lifecycle phase?

A. Key generation — the certificates were generated incorrectly  
B. Key renewal and monitoring — there was no process to track expiration dates or automatically renew before expiry  
C. Key distribution — the certificates weren't distributed to clients  
D. Key destruction — the expired certificates should have been destroyed

**Question 4:** What is the appropriate key destruction procedure for a decommissioned ADCS CA private key?

A. Delete the file from the filesystem — standard deletion is sufficient  
B. Cryptographic erasure: overwrite the key material multiple times (or use HSM secure delete), document the destruction with witness verification, revoke all certificates issued by that CA, and update the CRL  
C. Format the entire disk containing the key  
D. Keep the key indefinitely for forensic purposes — never destroy CA keys

---

## Answer Explanations

**Answer 1: B**  
The issue is **key storage security**. CA private keys are the most sensitive cryptographic material in a PKI — their compromise means arbitrary certificate issuance. Best practice is HSM storage (FIPS 140-2 Level 3) with multiparty controls for key access. At minimum, the key should be encrypted at rest with strong access controls, not stored as a plaintext file on a domain controller's disk where any Domain Admin can access it.

**Answer 2: C**  
The correct action is full **key lifecycle management**: verify the revocation (don't trust an unauthenticated email), remove the compromised/expired key, obtain the replacement through an authenticated channel (not the same email thread), and update the workflow. Using a revoked key (B) for encryption is dangerous — the corresponding private key may be compromised. Simply deleting (A) without obtaining the replacement breaks the evidence delivery workflow. Ignoring (D) is negligence — Cadre Corp is responsible for using valid keys to protect client data.

**Answer 3: B**  
This is a **key renewal and monitoring failure**. Self-signed certificates have expiration dates; a proper key lifecycle includes monitoring (automated alerts 30/14/7 days before expiry) and renewal (automated or documented manual process). Generation (A) was fine — the certificates worked when created. Distribution (C) isn't relevant for server-side TLS. Destruction (D) applies after decommissioning, not expiry — expired certificates should be replaced, not just destroyed.

**Answer 4: B**  
Proper key destruction for a CA private key requires: **cryptographic erasure** (not just filesystem delete — data remains recoverable), **documentation** (witness verification of destruction), and **certificate revocation** (all certificates issued by that CA must be revoked and the CRL published). This prevents any future use of the key and ensures relying parties know those certificates are no longer valid. Filesystem delete (A) is insufficient — forensic tools can recover deleted files. Full disk format (C) is excessive if only the key needs destruction. Keeping indefinitely (D) violates the principle of key lifecycle management — old keys are attack surface.

---

## Cadre Corp Application

1. **ADCS CA Key Protection:** The DC01 CA private key is a critical risk. Mitigation options: (a) migrate CA to a dedicated, hardened VM with BitLocker + restricted admin access, (b) use Windows Server 2025's TPM-backed key storage for the CA key, (c) document key access procedures in `CTL-KEY-MGMT` control.

2. **Ansible Vault Password Rotation:** Move the vault password to a secrets manager (Azure Key Vault or HashiCorp Vault). At minimum, encrypt the password file with the provisioning server's TPM and restrict read access to the Ansible service account only.

3. **Client Key Lifecycle Tracking:** Maintain a key registry (can be a simple CSV or the existing `config/asset-inventory.csv` extended with a `keys` sheet) tracking: client name, key ID, algorithm, creation date, expiration date, last verified date. Automated alerts 30 days before expiry.

4. **Internal TLS Certificate Automation:** Use ADCS to issue internal TLS certificates for Elastic, Velociraptor, and Arkime instead of self-signed. ADCS supports auto-enrollment and renewal via Group Policy — the infrastructure already exists.

---

## Interview Talking Points

1. **HSM Isn't Optional for CAs:** "If your CA private key is a file on a domain controller's C: drive, you don't have a PKI — you have a single point of cryptographic failure. HSMs exist for exactly this reason."

2. **Key Lifecycle Isn't Just Generation:** "Everyone focuses on key generation — 'use AES-256!' — but generation is 10% of the problem. Storage, distribution, rotation, revocation, destruction — the other 90% is where real-world compromises happen."

3. **Expired Certificates Are Broken Windows:** "If your internal services have had expired TLS certificates for 45 days, your team has learned to click through browser warnings. That's not a certificate problem — that's a security culture problem. Automated renewal is the fix; the cultural damage takes longer."

4. **Client Keys Are Our Responsibility:** "When a client's PGP key expires and we keep using it, we're encrypting their data with a key that might be compromised. 'The client didn't tell us' isn't a defense. Key lifecycle tracking is part of due care."
