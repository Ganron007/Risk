# R-EX-066 — Active Directory security (domain trusts, delegation)

**CISSP Reference:** Chapter 14, Section "Access Control Attacks"; Chapter 13, Section "Identity and Access Provisioning"  
**Exam Objective:** 5.2.1 Implement authorization mechanisms; 5.2.3 Manage access control in distributed systems  
**Study Guide Key Terms:** Domain trusts, Kerberos delegation, SID filtering, selective authentication, unconstrained delegation, constrained delegation, forest trust, PAC validation  

---

## Scenario Context

Cadre Corp's Active Directory estate spans two forests (`cadre.local` ↔ `range.local`) with a bidirectional forest trust and SID filtering DISABLED (the Server 2025 default). The campaign exercise revealed that:

1. RISK-003 (Cross-forest trust abuse) is rated 6 — an attacker who compromises `child.cadre.local` can forge SID history to gain Enterprise Admin in `cadre.local`.
2. `mbr01` has **unconstrained delegation** enabled (RISK-004, score 9) — any service running on mbr01 can impersonate any user who authenticates to it. During the campaign, this was exploited to capture a Domain Admin's TGT.
3. The `svc_mssql` service account has an SPN (Service Principal Name) and a weak password — making it vulnerable to Kerberoasting (RISK-006).

---

## Multiple-Choice Questions

**Question 1:** SID filtering on a forest trust prevents what specific attack?

A. Password spraying across the trust  
B. SID history injection — an attacker in the trusted forest cannot add forged SIDs (like Enterprise Admins) to their Kerberos ticket to gain elevated privileges in the trusting forest  
C. DNS cache poisoning between forests  
D. Man-in-the-middle attacks on LDAP

**Question 2:** Unconstrained Kerberos delegation on mbr01 allows:

A. The server to delegate any user's credentials to any service — if a Domain Admin authenticates to mbr01 (even just browsing a file share), mbr01 can request a TGS for any service AS that Domain Admin  
B. The server to enforce password policies  
C. Only HTTP service delegation  
D. Delegation that is automatically disabled after 24 hours

**Question 3:** Why are service accounts with SPNs vulnerable to Kerberoasting?

A. SPNs expose the service account's password hash through the Kerberos protocol  
B. Any authenticated domain user can request a TGS for any service with an SPN — the TGS is encrypted with the service account's password hash, enabling offline cracking  
C. SPN accounts have weaker encryption by default  
D. Kerberoasting only works on domain controllers

---

## Answer Explanations

**Answer 1: B**  
**SID filtering** strips SIDs from the trusted forest's authentication that don't belong to that forest's domain SID namespace. Without it, an attacker who compromises any user in the trusted forest can inject the trusting forest's Enterprise Admins SID into their Kerberos ticket — granting full administrative access across the trust boundary. Cadre Corp's SID filtering is OFF (verified per `01-core-ad.yml`), making RISK-003 a live vulnerability.

**Answer 2: A**  
**Unconstrained delegation** means the service can impersonate ANY user who authenticates to it, to ANY service. The server receives the user's TGT and can request service tickets on their behalf. This is the most dangerous delegation type — it's why RISK-004 is scored 9 (Critical). The mitigation: use constrained delegation (specifying which services) or resource-based constrained delegation (RBCD) instead.

**Answer 3: B**  
**Kerberoasting** exploits the fact that any authenticated domain user can request a TGS for any SPN. The TGS contains a portion encrypted with the service account's NTLM hash. The attacker extracts this and cracks it offline. Service accounts with weak passwords are trivially cracked. Mitigation: (a) 30+ character random passwords for service accounts, (b) use Group Managed Service Accounts (gMSA) where supported, (c) monitor for RC4 Kerberoast requests (Event ID 4769 with Ticket Encryption Type 0x17).

---

## Cadre Corp Application

1. **Enable SID Filtering:** On the `cadre.local` ↔ `range.local` trust, enable SID filtering via `Set-ADTrust -SIDFilteringQuarantined $true`. This directly closes RISK-003 and the Skipjack cross-forest attack.

2. **Replace Unconstrained Delegation:** On mbr01, remove unconstrained delegation. For IIS services, configure constrained delegation to specific SPNs. For SQL Server, use gMSA with managed passwords.

3. **Service Account Hardening:** Convert `svc_mssql` and other SPN-bearing accounts to gMSA. For accounts that can't use gMSA, set 30+ character random passwords with automated rotation.

---

## Interview Talking Points

1. **SID Filtering OFF = Forest Is a Gateway:** "A forest trust without SID filtering means compromising ANY user in one forest can lead to Enterprise Admin in the other. This is the Server 2025 default — you must explicitly enable it. That's a board-level conversation I've already had."

2. **Unconstrained Delegation = "I Trust This Server With Everything":** "When you enable unconstrained delegation, you're saying: any service on this server can impersonate any user. Including Domain Admins. Including the KRBTGT account. This is the most dangerous checkbox in Active Directory."
