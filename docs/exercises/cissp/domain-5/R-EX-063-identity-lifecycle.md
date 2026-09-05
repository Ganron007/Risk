# R-EX-063 — Identity lifecycle management

**CISSP Reference:** Chapter 13, Sections "Identity and Access Provisioning Life Cycle", "Managing Identity"  
**Exam Objective:** 5.1.1 Control physical and logical access; 5.1.3 Implement identity lifecycle  
**Study Guide Key Terms:** Provisioning, deprovisioning, identity lifecycle, joiner-mover-leaver, access certification, dormant accounts, privilege creep  

---

## Scenario Context

Cadre Corp has 45 employees but 62 enabled AD user accounts — 17 belong to former employees, contractors whose engagements ended, and test accounts created during lab setup. Three former employees' accounts still have `Backup Operators` and `Server Operators` membership. No deprovisioning process exists: when someone leaves, their manager might tell IT "when they get around to it." One contractor's account was used to access the lab network 14 months after their contract ended — the SOC team assumes it was a former employee "checking on old projects" but can't confirm.

---

## Multiple-Choice Questions

**Question 1:** The "joiner-mover-leaver" identity lifecycle refers to:

A. A physical security process for building access  
B. Provisioning access when someone joins, modifying access when their role changes (mover), and promptly revoking access when they leave (leaver)  
C. A backup rotation schedule  
D. An encryption key rotation process

**Question 2:** The 17 dormant accounts from former employees represent what PRIMARY risk?

A. Wasted software license costs  
B. Valid credentials available for unauthorized access — these accounts have authenticated access to the domain, may retain privileged group memberships, and are not monitored for suspicious activity  
C. Slower domain controller performance  
D. Email storage quota exceeded

**Question 3:** What is "privilege creep" in identity lifecycle management?

A. Privileges that are especially difficult to revoke  
B. The gradual accumulation of unnecessary permissions as an employee changes roles — each new role adds permissions, but old role permissions are rarely removed  
C. A type of malware that escalates privileges  
D. Privileges that creep across the network to other systems

---

## Answer Explanations

**Answer 1: B**  
The **joiner-mover-leaver** process covers: **Joiner** (new employee → create accounts, assign appropriate access based on role), **Mover** (role change → add new access, remove old access), **Leaver** (departure → disable accounts immediately, review for data ownership transfer, delete after grace period). This is the foundational identity governance process.

**Answer 2: B**  
Dormant accounts are **valid, unmonitored credentials**. They have all the access of their last known role, nobody reviews their activity, and they're perfect for attackers — no user will report "my account was compromised" because nobody uses that account anymore. The 14-month post-employment access is a textbook example.

**Answer 3: B**  
**Privilege creep** is the accumulation of permissions over time. An employee moves from DFIR Analyst → SOC Analyst → SOC Lead → DFIR Lead. At each move, new permissions are added, but the old SOC permissions are rarely removed. After 5 years, the employee has permissions spanning three roles — far more than needed for their current job. The mitigation: access recertification at each role change.

---

## Cadre Corp Application

1. **Immediate Cleanup:** Run `Search-ADAccount -AccountInactive -TimeSpan 90` on all domains. Disable all accounts with no logon in 90+ days. Move to a "Disabled Accounts" OU (Group Policy denies all logon rights). Delete after 180 days.

2. **Automated Deprovisioning:** Integrate with HR system (even a simple CSV export of active employees). Weekly reconciliation: accounts not in HR export → flag for manager review → disable within 7 days of departure confirmation.

3. **Access Recertification:** Quarterly campaign: every manager reviews their direct reports' group memberships. Remove any that don't match current job function.

---

## Interview Talking Points

1. **Deprovisioning Is the Most Important Security Process Nobody Does:** "Creating accounts is easy. Deleting them when people leave is the hard part — and the part that creates the most risk. A former employee's enabled account with Backup Operator privileges is a breach waiting to happen."

2. **Privilege Creep Is Invisible Until It's Exploited:** "Nobody notices privilege creep until an attacker moves laterally through 6 roles' worth of accumulated permissions on one compromised account. Access recertification at role change is the cure."
