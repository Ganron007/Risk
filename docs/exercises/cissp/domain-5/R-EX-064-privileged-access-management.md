# R-EX-064 — Privileged access management (PAM)

**CISSP Reference:** Chapter 14, Section "Access Control Attacks"; Chapter 13, Section "AAA Model"  
**Exam Objective:** 5.2.1 Implement authorization mechanisms; 5.1.2 Implement authentication mechanisms  
**Study Guide Key Terms:** PAM, just-in-time (JIT) access, privileged account management, session recording, password vaulting, least privilege, break-glass accounts  

---

## Scenario Context

Cadre Corp's domain admin credentials are used daily for routine tasks: the Infra Lead logs in as `Administrator@cadre.local` to check event logs, restart services, and install Windows Updates. The `Administrator` password is shared among three team members and stored in a Teams chat called "Admin Crew." There's no session recording, no justification workflow, and no time-limited access — a Domain Admin session runs indefinitely on the admin's workstation.

During a campaign exercise, the attacker compromised the Infra Lead's workstation (running a DA session) and extracted the DA credentials from LSASS memory — achieving full domain compromise without needing to escalate.

---

## Multiple-Choice Questions

**Question 1:** A Privileged Access Management (PAM) solution primarily addresses which problem demonstrated in the scenario?

A. Slow server performance during administrative tasks  
B. Standing privilege — Domain Admin accounts that are always active, shared among multiple users, and used for routine tasks that don't require DA-level access  
C. Password complexity requirements  
D. Network bandwidth consumption

**Question 2:** Just-in-Time (JIT) access in PAM means:

A. Privileged access is available at any time without restrictions  
B. Privileged access is granted only when needed, for a specific task, for a limited time window, and automatically revoked afterward — no standing privileges  
C. Access is granted based on the time of day only  
D. Access is "just in time" for the quarterly audit

**Question 3:** Why is a shared `Administrator` password (known to 3 team members) problematic from an auditing perspective?

A. It's too complex to type quickly  
B. Non-repudiation is impossible — any action performed under the shared account cannot be attributed to a specific individual; "who deleted that OU?" has no answer  
C. Shared passwords are always weaker than individual passwords  
D. It violates password length requirements

---

## Answer Explanations

**Answer 1: B**  
The core PAM problem is **standing privilege**: highly privileged accounts that are permanently active, shared, and used for tasks that don't require that privilege level. PAM solutions provide: (a) credential vaulting (passwords are stored securely, not in Teams chats), (b) session brokering (admin connects through PAM, not directly with the password), (c) JIT elevation (privilege granted temporarily, not permanently).

**Answer 2: B**  
**JIT access** means zero standing privileges. When an admin needs DA access to perform a specific task, they request it with a justification. PAM grants the access for a limited time (e.g., 2 hours). After expiration, the privilege is automatically revoked. If the admin needs it again, they submit a new request. This reduces the attack window from "always" to "2 hours."

**Answer 3: B**  
Shared accounts destroy **non-repudiation**. If Administrator deletes an OU, modifies a GPO, or resets a password, the audit log shows "Administrator" — not which of the three team members performed the action. This is unacceptable for forensic investigation and regulatory compliance. Individual named accounts with delegated privileges solve this.

---

## Cadre Corp Application

1. **Immediate: Eliminate Shared DA Usage.** Each admin gets a separate named admin account (e.g., `admin-john@cadre.local`). The built-in `Administrator` account is reserved as a break-glass account with a password stored in a physical safe — not in Teams.

2. **PAM Lite with AD Capabilities:** Use AD's built-in capabilities temporarily: (a) `Protected Users` group prevents credential caching for DA accounts (no LSASS extraction), (b) Authentication Policy Silos restrict DA accounts to specific hosts, (c) Time-based group membership via scheduled tasks.

3. **Tiered Admin Model:** Implement AD tiered administration: Tier 0 (forest/domain admins) → Tier 1 (server admins) → Tier 2 (workstation admins). No account from a lower tier can log on to a higher tier's systems.

---

## Interview Talking Points

1. **Standing Privilege = Standing Risk:** "A Domain Admin session that's always active on a workstation is a gift to attackers. Every minute of DA uptime is a minute an attacker can extract those credentials from memory. JIT access shrinks the attack window from 24/7 to a few hours."

2. **Shared Admin Accounts = Zero Accountability:** "If three people share 'Administrator' and something breaks, you can't ask who did it. Named privileged accounts with individual accountability are table stakes for any mature security program."
