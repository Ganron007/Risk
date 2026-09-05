# R-EX-062 — Authorization models (RBAC, ABAC, MAC, DAC)

**CISSP Reference:** Chapter 14, Sections "Access Control Models", "Controlling and Monitoring Access"  
**Exam Objective:** 5.2.1 Implement authorization mechanisms; 5.2.2 Compare access control models  
**Study Guide Key Terms:** DAC (Discretionary), MAC (Mandatory), RBAC (Role-Based), ABAC (Attribute-Based), Rule-Based AC, Bell-LaPadula, Biba  
**Inputs:** Cadre Corp AD group structure, `05-ad-attack-surface.yml`

---

## Scenario Context

Cadre Corp's Active Directory has organically grown to 187 groups across two forests, with no documented access control model. The SOC Lead recently discovered that:

1. A DFIR analyst in the `Domain Users` group could read the `ITAdmin` share containing service account passwords because of nested group membership inherited from a project group created three years ago.
2. Three former employees' accounts are still enabled with memberships in `Backup Operators` and `Server Operators` — teams that no current employee should belong to.
3. The summer intern was accidentally added to `Domain Admins` for "a temporary project" — six months later, they're still there.

The CISO has asked you to recommend an access control model and implement a review process.

---

## Multiple-Choice Questions

**Question 1:** In DAC (Discretionary Access Control), who decides access to an object?

A. The system administrator exclusively  
B. The object's owner — each file/folder has an owner who can grant or revoke access at their discretion  
C. A central policy server  
D. Access is decided by security labels only

**Question 2:** MAC (Mandatory Access Control) differs from DAC primarily because:

A. MAC uses passwords; DAC uses biometrics  
B. In MAC, access decisions are enforced by the system based on security labels and clearances — the object owner cannot override them; in DAC, the owner has discretion to grant access  
C. MAC is only used in Windows; DAC is only used in Linux  
D. MAC and DAC are the same model with different names

**Question 3:** Why is RBAC (Role-Based Access Control) the most practical model for Cadre Corp's 45-employee DFIR firm?

A. RBAC requires no maintenance after initial setup  
B. RBAC maps to job functions — "DFIR Analyst," "SOC Lead," "Infra Lead" — permissions are assigned to roles, not individuals; when an employee changes roles, you change their role assignment, not 50 individual permissions  
C. RBAC is the only model that supports cloud applications  
D. RBAC eliminates the need for access reviews

**Question 4:** ABAC (Attribute-Based Access Control) extends RBAC by:

A. Using only biometric attributes for access  
B. Making access decisions based on multiple attributes simultaneously — user role, clearance, location, device posture, time of day, data sensitivity — enabling dynamic, context-aware policies  
C. Eliminating roles entirely  
D. Requiring physical hardware tokens

---

## Answer Explanations

**Answer 1: B**  
In **DAC**, each object has an owner (typically the creator) who controls access at their discretion. This is how Windows NTFS permissions and Unix file permissions work by default. The flexibility is both DAC's strength (owners can collaborate freely) and weakness (owners can make poor decisions, and access is hard to audit centrally).

**Answer 2: B**  
**MAC** enforces system-wide policy based on labels (classifications and clearances) that individual users cannot override. Classic example: Bell-LaPadula model in military systems — a "Secret" user cannot read a "Top Secret" document regardless of what the document owner wants. SELinux and Windows Mandatory Integrity Control (MIC) are MAC implementations.

**Answer 3: B**  
**RBAC maps to organizational structure**. Instead of managing permissions per user (45 users × 50 resources = 2,250 permission assignments), you define roles (DFIR Analyst, SOC Lead, Infra Lead), assign permissions to roles, and assign users to roles. When a DFIR analyst becomes SOC Lead, you change one role assignment — not 50 individual permissions. RBAC still requires periodic access reviews (D is false).

**Answer 4: B**  
**ABAC evaluates multiple attributes** for each access decision: user attributes (role, department, clearance), resource attributes (classification, owner, type), action attributes (read, write, delete), and environmental attributes (time, location, device posture). This enables policies like "DFIR Analysts can read evidence files classified Restricted only from managed workstations during business hours." ABAC is more flexible but more complex to administer than RBAC.

---

## Cadre Corp Application

1. **RBAC Implementation:** Map all 187 AD groups to defined job roles. Security groups should represent roles, not projects. Use AGDLP (Account → Global → Domain Local → Permissions) nesting. This makes the group structure auditable.

2. **MAC for Evidence:** For Restricted evidence stores (AST-030), consider Windows Mandatory Integrity Control (MIC) with High integrity label — preventing lower-integrity processes (e.g., a compromised web browser) from writing to evidence directories.

3. **Quarterly Access Review:** Implement automated reports (via PowerShell + AD module) listing: users with privileged group membership, users with enabled accounts but no logon in 90 days, nested group membership paths to sensitive resources.

---

## Interview Talking Points

1. **DAC Is the Wild West:** "Every file owner can grant anyone access. That's how the intern's project folder ends up readable by everyone — someone clicked 'Share with Everyone' three years ago and forgot. DAC needs central oversight to prevent permission sprawl."

2. **RBAC = Auditable Structure:** "When the auditor asks 'who has access to client evidence?', RBAC lets me answer by role — 'DFIR Analysts and DFIR Lead' — instead of listing 15 individual user accounts with no explanation of why they have access."

3. **Nested Groups Are Hidden Permissions:** "The analyst who had access to ITAdmin passwords through nested project groups? Nobody intentionally granted that. It was an inheritance accident. RBAC with flat role groups and documented nesting prevents this."
