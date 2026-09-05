# R-EX-067 — Cloud identity (Azure AD, AWS IAM, GCP IAM)

**CISSP Reference:** Chapter 13, Section "Identity Management Implementation"; Chapter 9, Section "Shared Responsibility Models"  
**Exam Objective:** 5.1.1 Control access; 5.2.1 Implement authorization; 3.5.1 Shared responsibility  
**Study Guide Key Terms:** Entra ID (Azure AD), AWS IAM, GCP IAM, hybrid identity, Cloud Sync, PIM, conditional access, federation  

---

## Scenario Context

Cadre Corp operates a hybrid identity model: on-prem AD (`cadre.local`) syncs to Entra ID (Azure AD) via Cloud Sync agent running on DC01. The Entra ID tenant (AST-020) is classified Restricted because the Entra ID Global Administrator role can reset passwords for synced on-prem accounts, including Domain Admins — a cloud-to-on-prem escalation path.

The Cloud Security Lead recently discovered that three users have permanent Global Administrator assignment in Entra ID (no PIM/just-in-time), the Cloud Sync agent runs with a highly privileged service account, and there's no Conditional Access policy requiring MFA for cloud admin roles.

---

## Multiple-Choice Questions

**Question 1:** In Cadre Corp's hybrid identity model, why does Entra ID Global Administrator equate to on-prem Domain Admin?

A. It doesn't — cloud and on-prem are separate  
B. Password hash synchronization means an Entra ID Global Admin can reset the password of a synced on-prem account (including Domain Admins) through Entra ID, which syncs back to on-prem AD — creating a transitive escalation path  
C. Only if the same person holds both roles  
D. Global Administrator only affects Office 365, not AD

**Question 2:** What is Azure AD Privileged Identity Management (PIM)?

A. A tool that manages Azure subscription costs  
B. Just-in-Time privileged role activation — users are eligible for roles but must activate them with MFA, justification, and approval for a limited time window; no standing privileged assignments  
C. A password manager for cloud applications  
D. An identity threat detection tool

**Question 3:** Conditional Access in Entra ID enables what security capability?

A. Unrestricted access from any device and location  
B. Policy-based access control considering user, device, location, application, and risk signals — e.g., "require MFA when accessing from outside the corporate network" or "block access from non-compliant devices"  
C. Automatic user provisioning to all applications  
D. Passwordless authentication only

---

## Answer Explanations

**Answer 1: B**  
**Password hash synchronization creates a transitive trust path**: Entra ID Global Admin → reset synced user's password in Entra ID → password hash syncs back to on-prem AD → the admin now controls the on-prem account. If that account is a Domain Admin, cloud compromise = full on-prem domain compromise. This is why AST-020 is classified Restricted and why cloud identity roles must be protected at the same level as on-prem DA.

**Answer 2: B**  
**PIM provides JIT privileged access** — the same concept as PAM but for cloud roles. Instead of three users having permanent Global Admin, they are "eligible" and must activate the role when needed: provide MFA, a justification, optionally get approval, and the role auto-expires after a configured time. This eliminates standing cloud privileges.

**Answer 3: B**  
**Conditional Access evaluates access context** and enforces policy in real time. Example policies: (a) require MFA for all admin role access, (b) block access from countries Cadre Corp doesn't operate in, (c) require compliant (domain-joined, patched) devices for access to Restricted data, (d) require re-authentication for high-risk sign-ins detected by Identity Protection.

---

## Cadre Corp Application

1. **Immediate Entra ID Hardening:** (a) Remove permanent Global Admin assignments — migrate to PIM-eligible only, (b) Deploy Conditional Access: require MFA for all admin roles, block legacy authentication, require compliant devices for cloud access, (c) Enable Identity Protection risk-based policies.

2. **Cloud Sync Service Account:** Review the Cloud Sync agent's service account privileges. Follow least privilege — it needs password hash sync permissions, not Domain Admin. Create a dedicated gMSA with only the required delegated permissions.

3. **Cross-Cloud IAM Consistency:** If Cadre Corp expands to AWS or GCP, apply the same principles: JIT access (AWS IAM Access Analyzer + permission boundaries, GCP Privileged Access Manager), conditional/context-based policies, and consistent RBAC role design.

---

## Interview Talking Points

1. **Cloud Admin = Domain Admin in Hybrid:** "If password hash sync is enabled, the cloud Global Admin can reset on-prem Domain Admin passwords. That's not a bug — it's how the sync works. Protecting cloud identity is protecting on-prem identity. Same security bar."

2. **PIM + Conditional Access = Cloud PAM:** "No permanent Global Admins. Activate when needed, with MFA, with justification. Conditional Access ensures you're on a managed device from a trusted location. This is the cloud equivalent of the PAM controls we're applying on-prem."
