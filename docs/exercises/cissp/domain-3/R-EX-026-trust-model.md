# R-EX-026 — Forest trust risk and trust model analysis

**CISSP Reference:** Chapter 8, Sections "Security Models", "Trust Boundaries", Pages 565–590; Chapter 14, Section "Access Control in Distributed Systems"  
**Exam Objective:** 3.1.1 Understand security models and frameworks; 3.3.1 Apply secure design principles (trust boundaries)  
**Study Guide Key Terms:** Trust model, trust boundary, forest trust, SID filtering, selective authentication, transitive trust, blast radius, trust direction, Bell-LaPadula  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md), RISK-003, `01-core-ad.yml`

---

## Scenario Context

Cadre Corp's Active Directory estate spans two forests with a bidirectional trust: `cadre.local` (root) ↔ `range.local` (external forest, hosts SCCM/WSUS and separate research accounts). The trust was created with Server 2025 defaults, which means **SID filtering is DISABLED** and **selective authentication is NOT enforced**.

RISK-003 (Cross-forest trust abuse, score 6) documents the attack path: an attacker who compromises any account in `child.cadre.local` can forge SID history to inject `cadre.local\Enterprise Admins` into their Kerberos ticket, gaining full administrative access across the trust boundary. This is the Skipjack attack vector — PAC signature corruption exploits the SID filtering gap.

The CISO asks: "Why do we have a bidirectional trust with an external forest that runs SCCM? And if we need it, why aren't SID filtering and selective authentication enabled?" The Infra Lead responds: "Those were the defaults. We didn't change them."

You need to analyze the trust model, identify the security boundary violations, and recommend trust hardening measures.

---

## Multiple-Choice Questions

**Question 1:** In security architecture, a "trust boundary" is:

A. A legal agreement between two organizations  
B. The point where data or control passes between security domains with different trust levels — crossing a trust boundary requires authentication, authorization, and validation  
C. The physical perimeter of a data center  
D. A firewall between network segments

**Question 2:** The bidirectional forest trust between `cadre.local` and `range.local` expands the blast radius because:

A. It doubles the number of domain controllers to manage  
B. A compromise in either forest can propagate to the other — if `range.local` is compromised (lower security, hosts SCCM/WSUS), the attacker can pivot into `cadre.local` (higher security, hosts client evidence and identity plane)  
C. Bidirectional trusts require more firewall rules  
D. Forest trusts are inherently insecure and should never be used

**Question 3:** SID filtering, when enabled on a forest trust, prevents:

A. Any authentication across the trust  
B. SID history injection — it strips SIDs from the trusted forest's authentication that don't belong to that forest's domain SID namespace, preventing an attacker from adding the trusting forest's privileged SIDs to their token  
C. Password changes for trusted users  
D. DNS queries across the trust

**Question 4:** Selective authentication on a forest trust provides what security benefit over domain-wide authentication?

A. It allows all users in the trusted forest to access all resources in the trusting forest  
B. It requires explicit per-resource permission — even if a trust exists, users from the trusted forest can only access specific resources where they've been explicitly granted the "Allowed to Authenticate" right, rather than authenticating to any resource by default  
C. It disables the trust entirely during non-business hours  
D. It requires MFA for all cross-forest authentications

---

## Answer Explanations

**Answer 1: B**  
A **trust boundary** marks where security contexts change. In Cadre Corp's case, the forest trust is the boundary between `cadre.local` and `range.local` — authentication crossing this boundary must be validated, and the trust configuration (SID filtering, selective authentication, direction) determines what crosses. A firewall (D) is one type of trust boundary enforcement, but the concept is broader — it's about where you stop trusting and start verifying.

**Answer 2: B**  
Bidirectional trusts create **mutual blast radius expansion**. A compromise in the less-secure forest (`range.local` runs SCCM/WSUS — documented attack surfaces) becomes a pivot point into the more-secure forest (`cadre.local` holds client evidence and domain identity). The trust direction means risk flows both ways. In Cadre Corp's case, the trust was created for SCCM/WSUS functionality but with insecure defaults — making a functional convenience into a cross-forest attack highway.

**Answer 3: B**  
**SID filtering strips foreign SIDs** from authentication tokens crossing the trust. Without it, an attacker in `range.local` can add `cadre.local\Enterprise Admins` SID to their token — and `cadre.local` will honor it. With SID filtering enabled, `cadre.local` discards any SID that doesn't belong to `range.local`'s domain SID namespace, preventing the injection. This is a one-line PowerShell command (`Set-ADTrust -SIDFilteringQuarantined $true`) that closes the primary cross-forest escalation path.

**Answer 4: B**  
**Selective authentication** flips the default from "authenticate to anything" to "authenticate only where explicitly permitted." Without it, any user in `range.local` can authenticate to any resource in `cadre.local` (subject to that resource's ACL). With selective authentication, the user must also have the "Allowed to Authenticate" permission on the specific computer object in `cadre.local` — adding a second, explicit gate. This is the principle of least privilege applied to trust relationships.

---

## Cadre Corp Application

1. **Immediate Trust Hardening:** (a) Enable SID filtering: `Set-ADTrust -Identity "range.local" -SIDFilteringQuarantined $true`, (b) Enable selective authentication: `Set-ADTrust -Identity "range.local" -SelectiveAuthentication $true`, (c) Review trust direction — does it need to be bidirectional or can it be one-way? Document the business justification for each trust attribute.

2. **Trust Review Control:** Add `CTL-TRUST-REVIEW` to the control register: quarterly review of all forest/external trusts, verifying SID filtering (enabled), selective authentication (enabled), trust direction (justified), and monitoring coverage (inter-realm Kerberos events logged and alerted).

3. **Trust Monitoring:** Deploy detection rules for cross-forest escalation: (a) Event ID 4769 (TGS request) with inter-realm ticket, (b) anomalous SID history in Kerberos tickets, (c) authentication from `range.local` users to `cadre.local` Restricted assets. Feed to Elastic and correlate with campaign telemetry.

---

## Interview Talking Points

1. **Defaults Are Not Security Decisions:** "Server 2025 defaults to SID filtering OFF on forest trusts. That's not a security decision — it's an absence of one. Every trust you create needs explicit hardening: SID filtering ON, selective authentication ON, direction justified. 'We used the defaults' is how RISK-003 goes from theoretical to exploitable."

2. **Trust = Blast Radius Union:** "When you create a forest trust, you're not just connecting two domains — you're merging their blast radiuses. A compromise in the less-secure forest is now a compromise in the more-secure one. Trusts should be as narrow as functionality allows: one-way where possible, selective authentication always, SID filtering always."

3. **Trust Boundaries Need Monitoring:** "The trust boundary is where your detection rules should be most aggressive. Inter-realm Kerberos, anomalous SID history, authentication from one forest to another's Restricted assets — these are high-signal events that should never be 'informational.' If you're not alerting on cross-forest auth, you're not monitoring your trust boundaries."
