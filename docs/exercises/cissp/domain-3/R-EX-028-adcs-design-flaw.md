# R-EX-028 — ADCS as an architectural design weakness

**CISSP Reference:** Chapter 7, Sections "Public Key Infrastructure", "Certificate Authorities", Pages 490–530; Chapter 8, Section "Security Vulnerabilities, Threats, and Countermeasures"; Chapter 9, Section "Common Security Architecture Flaws"  
**Exam Objective:** 3.3.1 Apply secure design principles; 3.5.3 Understand public key infrastructure; 3.6.1 Identify security architecture vulnerabilities  
**Study Guide Key Terms:** PKI architecture, certificate templates, ESC1-15, design weakness vs implementation bug, compensating controls, defense-in-depth for PKI  
**Inputs:** [`../risk-register-baseline.md`](../risk-register-baseline.md), RISK-002, AST-034, `08-adcs-deploy.yml`

---

## Scenario Context

Cadre Corp deployed Active Directory Certificate Services (ADCS) on DC01 as part of the default enterprise PKI setup. The deployment used default certificate templates, including the "Web Server" template configured with `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` — meaning any domain user can request a certificate for ANY subject name, including "DomainController.cadre.local" or "Administrator@cadre.local."

RISK-002 rates ADCS ESC abuse as score 9 (Critical) because:

- **ESC1 (Enrollee Supplies Subject):** A low-privilege user can request a certificate for a Domain Admin account, then use that certificate for Kerberos authentication (PKINIT) — obtaining a TGT as that Domain Admin.
- **ESC4 (WriteDacl on Template):** If an attacker gains write permissions on a certificate template, they can modify it to add dangerous EKUs or remove manager approval requirements.
- **ESC8 (NTLM Relay to ADCS):** The CA's web enrollment endpoint accepts NTLM authentication — enabling relay attacks from coerced machine accounts.

The CISO asks: "Is this a patch issue or a design issue?" The answer: it's primarily a DESIGN issue. The templates were configured insecurely by architecture choice, not by software bug. Patching doesn't fix ESC1 — you have to change the template design.

---

## Multiple-Choice Questions

**Question 1:** Why is ESC1 (enrollee supplies subject) classified as a design weakness rather than an implementation bug?

A. It's caused by a coding error in Microsoft's certificate enrollment code  
B. The certificate template was CONFIGURED to allow enrollees to specify the subject name — this was an architectural choice made during PKI design, not a software vulnerability; the fix is to change the template configuration, not apply a patch  
C. It only affects older versions of Windows Server  
D. It requires physical access to the CA server

**Question 2:** In PKI architecture, the `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` flag on a certificate template:

A. Enables automatic certificate renewal for all users  
B. Allows the certificate requester to specify WHO the certificate is for (the Subject) — without this flag, the CA uses the requester's identity from Active Directory; with it, the requester can request a certificate for ANY identity, which is the architectural flaw  
C. Enables certificate revocation checking  
D. Encrypts the certificate's private key during issuance

**Question 3:** Which of the following is a compensating control for ESC1 that addresses the DESIGN issue at the architecture level?

A. Installing the latest Windows security patches  
B. Removing the `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` flag from templates where it's not required, requiring CA certificate manager approval for high-value templates, and deploying SIEM detection rules for anomalous certificate requests (Event ID 4886/4887)  
C. Disabling the entire ADCS CA  
D. Running antivirus on the CA server

**Question 4:** Why is ADCS deployed on a Domain Controller (DC01) an architectural concern, separate from the template configuration issues?

A. There's no concern — ADCS on a DC is Microsoft's recommended best practice  
B. A DC already holds the most sensitive data in the domain (KRBTGT hash, NTDS.dit) — adding the CA private key to the same server concentrates multiple crown jewels on a single host; compromise of DC01 yields both domain dominance AND the ability to issue arbitrary certificates, eliminating any remaining trust in the PKI  
C. ADCS requires more RAM than a DC typically has  
D. ADCS on a DC improves certificate enrollment performance

---

## Answer Explanations

**Answer 1: B**  
ESC1 is a **configuration-level design weakness**, not a code vulnerability. The `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` flag was intentionally designed by Microsoft to support use cases where the certificate subject differs from the requester (e.g., a helpdesk requesting a certificate for a user). The vulnerability arises when this powerful flag is left enabled on templates available to low-privilege users. The fix is architectural: review every template, remove the flag where not explicitly required, and require manager approval for remaining cases. No patch fixes bad PKI design.

**Answer 2: B**  
`CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` allows the requester to specify **any subject name**, regardless of their own identity. Combined with an EKU that enables domain authentication (like `Client Authentication` or `Smart Card Logon`), this means User A can request a certificate identifying them as DomainAdmin — and the CA will issue it. This is the architectural heart of ESC1. The flag exists for legitimate delegation scenarios but is dangerous when broadly available.

**Answer 3: B**  
The compensating controls address the design issue at multiple architectural layers: (a) **template hardening** — remove the dangerous flag where not needed (fixing the root cause), (b) **CA certificate manager approval** — adding a human gate for high-value certificates (defense-in-depth), (c) **SIEM detection** — monitoring for anomalous certificate requests as a detective control in case the preventative controls fail. Patching (A) doesn't fix template configuration. Disabling ADCS (C) is avoidance, not compensation. Antivirus (D) doesn't address certificate issuance logic.

**Answer 4: B**  
Deploying ADCS on a DC creates a **crown jewel concentration risk**. The DC holds: NTDS.dit (all password hashes), KRBTGT hash (Golden Ticket forging), and all domain replication data. Adding the CA private key means DC01 compromise yields: (a) domain dominance via DCSync/Golden Ticket, AND (b) the ability to issue certificates for any identity — including certificates that persist even after KRBTGT rotation (certificates are valid until revoked, not until password change). Best practice is to deploy the CA on a dedicated, hardened server — not on a DC.

---

## Cadre Corp Application

1. **ADCS Template Audit:** Run `certipy find -vulnerable` or review all published certificate templates. For each template with `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`, document the business justification. Remove the flag from any template where it's not explicitly required. Add CA certificate manager approval for remaining cases.

2. **ADCS Separation:** Plan migration of the CA role from DC01 to a dedicated, hardened member server. The CA private key should be stored with TPM protection or HSM. This separates the identity plane (DC) from the PKI plane (CA), reducing crown jewel concentration.

3. **ADCS Monitoring:** Deploy detection rules: (a) Event ID 4886 (certificate issued) with anomalous subject name (e.g., a low-privilege user requesting a certificate for a privileged account), (b) Event ID 4887 (certificate request denied — may indicate an attacker probing templates), (c) template modification events. Feed to Elastic with cadre-* rules.

---

## Interview Talking Points

1. **Bad PKI Design Is Not a Patch Problem:** "ESC1 isn't a vulnerability Microsoft will fix in next month's Patch Tuesday. It's a design choice we made when we configured certificate templates. The fix is architectural: review every template, remove dangerous flags, add approval gates. You can't patch bad architecture."

2. **Don't Put Your CA on Your DC:** "A domain controller already holds the keys to the kingdom. Adding the CA private key to the same server is like putting your house keys and your safe combination in the same pocket. Separate them. Dedicated CA server, TPM-backed key storage, restricted admin access."

3. **Certificate Abuse Survives Password Changes:** "When you reset KRBTGT after a breach, Golden Tickets stop working. But certificates issued by a compromised CA are valid until revoked — potentially years. That's why CA compromise is worse than DCSync. It creates persistent, hard-to-detect access that survives standard incident response."
