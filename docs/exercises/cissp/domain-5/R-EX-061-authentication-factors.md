# R-EX-061 — Authentication factors (MFA, biometrics, knowledge-based)

**CISSP Reference:** Chapter 13, Sections "Authentication Factors", "Controlling Access to Assets"  
**Exam Objective:** 5.1.1 Control physical and logical access; 5.1.2 Implement authentication mechanisms  
**Study Guide Key Terms:** Type 1 (knowledge), Type 2 (possession), Type 3 (biometric/inherence), MFA, 2FA, FRR/FAR, CER, passwordless authentication  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), Cadre Corp AD infrastructure

---

## Scenario Context

Cadre Corp currently authenticates all 45 employees using a single factor: domain password (Type 1 — something you know). The password policy requires 12 characters with complexity, changed every 90 days. However, three recent incidents have highlighted the inadequacy of single-factor auth:

1. A DFIR analyst's password (`Summer2025!`) was cracked from a Kerberoast hash during a campaign exercise — granting the attacker domain access with the analyst's privileges.

2. The CISO's executive assistant fell for a phishing email and entered their domain credentials on a fake login page. The attacker logged in within 90 seconds.

3. An intern wrote their password on a sticky note attached to their monitor — discovered during a routine walkthrough.

You have been asked to design a multi-factor authentication strategy appropriate for Cadre Corp's risk profile, considering the varying sensitivity of different access tiers.

---

## Multiple-Choice Questions

**Question 1:** Which of the following correctly classifies authentication factors by type?

A. Password = Type 1 (knowledge), Smart card = Type 2 (possession), Fingerprint = Type 3 (inherence/biometric)  
B. Password = Type 2, Smart card = Type 3, Fingerprint = Type 1  
C. All three are Type 1 — they all verify identity  
D. Passwords are Type 3 because they're "something you are"

**Question 2:** What is the PRIMARY reason that two factors of the SAME type (e.g., password + security question) do NOT constitute true MFA?

A. Security questions are less secure than passwords  
B. Both are Type 1 (knowledge) — an attacker who steals one knowledge factor can often steal the other (phishing captures both password AND security answers)  
C. Security questions are deprecated by NIST  
D. Password + security question is too slow for users

**Question 3:** For Cadre Corp's domain controllers and Restricted assets, which MFA combination provides the strongest protection?

A. Password + security question  
B. Password + SMS one-time code  
C. Smart card (Type 2) + PIN (Type 1) — or FIDO2 security key + biometric (Type 3) — providing true two-factor from different types with phishing resistance  
D. Password only, but longer and more complex

**Question 4:** What are FRR (False Rejection Rate) and FAR (False Acceptance Rate) in biometric authentication?

A. FRR = how fast the biometric scanner operates; FAR = how far the user must stand  
B. FRR = legitimate users incorrectly rejected; FAR = impostors incorrectly accepted — there's an inverse relationship; tuning one affects the other  
C. FRR is only for fingerprints; FAR is only for facial recognition  
D. FRR and FAR measure the same thing — biometric accuracy

---

## Answer Explanations

**Answer 1: A**  
The standard CISSP classification: **Type 1 = something you know** (password, PIN, security question), **Type 2 = something you have** (smart card, token, phone), **Type 3 = something you are** (fingerprint, iris, face, behavioral biometrics). True MFA requires factors from at least two different types.

**Answer 2: B**  
Two Type 1 factors don't constitute MFA because they share the same vulnerability profile. Phishing captures both passwords AND security question answers simultaneously. SMS intercept captures both a password (if keylogged) and the SMS code. True MFA requires factors from DIFFERENT types so that compromising one factor type doesn't automatically compromise the other.

**Answer 3: C**  
**Smart card + PIN** or **FIDO2 security key + biometric** provides true phishing-resistant MFA. Smart cards and FIDO2 keys use public-key cryptography bound to the origin (the browser verifies the site's identity before releasing credentials), making them immune to phishing. SMS codes (B) are vulnerable to SIM swapping and phishing. Password-only (D) is single factor.

**Answer 4: B**  
**FRR (False Rejection Rate)** = legitimate users incorrectly denied access (Type I error). **FAR (False Acceptance Rate)** = impostors incorrectly granted access (Type II error). They have an inverse relationship: making the system more sensitive (lower FAR) increases FRR (more legitimate users rejected). The crossover point (CER - Crossover Error Rate) is where FRR = FAR and indicates overall biometric accuracy.

---

## Cadre Corp Application

1. **Tiered MFA Strategy:**
   - **Restricted assets (DCs, evidence stores, ADCS):** FIDO2 security keys + PIN for all admin access. Phishing-resistant.
   - **Confidential assets (SOC tools, member servers):** Authenticator app (TOTP) + password. Stronger than SMS, deployable today.
   - **Internal assets (workstations, lab access):** Windows Hello for Business (biometric + TPM-bound key) for workstation login.

2. **Kerberoast Mitigation:** MFA doesn't prevent Kerberoast (it's an offline attack on service account hashes), but strong, unique service account passwords (30+ character random, managed in a PAM solution — see R-EX-064) reduce the impact.

3. **AD-Integrated MFA:** Windows Server 2025 + Entra ID supports hybrid MFA. For on-prem domain auth, consider AD FS with Azure MFA adapter, or third-party MFA providers that integrate with Windows logon.

---

## Interview Talking Points

1. **Two of the Same Type Is Not MFA:** "Password + security question is not MFA — it's one factor asked twice. Both are things you know, both can be phished, both can be shoulder-surfed. True MFA crosses factor types: something you know + something you have + something you are."

2. **SMS MFA Is Better Than Nothing, Barely:** "SIM swapping, SS7 attacks, and SMS phishing make SMS-based MFA the weakest form of true MFA. FIDO2 security keys are phishing-resistant — the browser cryptographically verifies the site before releasing credentials. That's the standard for protecting domain admin accounts."

3. **Biometrics Are Usernames, Not Passwords:** "Your fingerprint is a username — it identifies you, but you can't rotate it if compromised. Always pair biometrics with a second factor, and never rely on biometrics alone for high-security authentication."
