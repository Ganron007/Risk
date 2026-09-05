# R-EX-075 — Test environment isolation and safety

**CISSP Reference:** Chapter 15, Section "Training and Exercises"; Chapter 9, Section "Security Architecture Vulnerabilities"  
**Exam Objective:** 6.1.4 Conduct security testing safely; 6.3.1 Manage test environments  
**Study Guide Key Terms:** Test environment isolation, production safety, snapshot/rollback, scope boundaries, rules of engagement, accidental impact  

---

## Scenario Context

During Cadre Corp's internal red team exercise, a tester running Kerberoast against `range.local` accidentally targeted the production domain controller (`dc01.cadre.local`) instead of the intended test domain. The aggressive Kerberoast request rate triggered account lockouts for 12 production user accounts, including the CISO — who couldn't log in for 30 minutes during an incident.

In a separate incident, a junior analyst testing ransomware simulation in the DarkAI lab accidentally encrypted a shared folder that was also mounted on the production evidence server — 2 TB of client forensic data became inaccessible for 4 hours while restoring from backup.

The CISO demands: "How do we test safely without breaking production?"

---

## Multiple-Choice Questions

**Question 1:** What is the PRIMARY control to prevent test activities from impacting production systems?

A. Stronger passwords on production systems  
B. Clear environment separation — production and test environments must be logically or physically isolated with explicit scope boundaries, separate credentials, and distinct network identifiers  
C. Testing only during business hours when staff can respond  
D. Informing all users before testing begins

**Question 2:** The Kerberoast accident (targeting production instead of test) could have been prevented by:

A. Running Kerberoast faster to finish before lockouts triggered  
B. Using separate, visually distinct credentials for test vs production — e.g., `TEST\testuser` vs `CADRE\realuser` — and configuring tools with explicit target lists that exclude production DCs  
C. Not running Kerberoast at all  
D. Running the test from a different subnet

**Question 3:** For the ransomware simulation that affected production evidence, what is the appropriate isolation mechanism?

A. Running simulations on the same server as production to maximize realism  
B. Network-level isolation — the DarkAI lab network (172.20.0.0/24) must have NO routes, mounts, or shared storage with the production evidence network (192.168.77.0/24) — plus explicit "blast radius" verification before any destructive test  
C. Informing the DFIR team that a simulation is running  
D. Running simulations only when the evidence server is offline

---

## Answer Explanations

**Answer 1: B**  
**Clear environment separation** is the foundational control. Production and test must be distinct — different subnets, different credentials, different hostnames, preferably different hypervisors or at minimum different resource pools. Scope boundaries must be EXPLICIT (documented, reviewed before testing), not implicit ("I think this is the test DC"). The CISO's lockout happened because the tester could reach production with test credentials — that path shouldn't exist.

**Answer 2: B**  
**Distinct credentials and explicit target lists** prevent scope confusion. Use separate domains or separate accounts with naming conventions that make the environment obvious (`testlab\admin` vs `cadre\admin`). Pre-define target lists in tool configuration, not ad-hoc command lines. The tester should never have been able to type `dc01.cadre.local` as a target — the tool config should have rejected it.

**Answer 3: B**  
**Network-level isolation** with zero shared resources is the minimum for destructive testing. The DarkAI lab already had a separate Docker network (172.20.0.0/24) — the failure was a shared mount that bridged the isolation. Before any destructive test (ransomware sim, wiper, exploit with crash risk): (a) verify network isolation, (b) verify no shared storage, (c) take snapshots, (d) define and review blast radius, (e) have rollback procedure tested and ready.

---

## Cadre Corp Application

1. **Lab vs Production Separation:** The CADRE lab IS the test environment — it's already isolated on `vmnet2` with no route to production networks. However, WITHIN the lab, "production-like" services (DCs, evidence stores) must be separated from "test/destructive" services (DarkAI, campaign attack VMs).

2. **Pre-Flight Checklist for Destructive Tests:** Before any test that could crash systems or encrypt data: (a) VMware snapshot all target VMs, (b) verify network isolation from Restricted assets, (c) verify no shared storage/mounts, (d) confirm rollback procedure, (e) notify team of test window.

3. **Credentials Hygiene:** Campaign test accounts use `child.cadre.local` domain with distinct naming (`intern_blue`, `svc_mssql`). Production admin accounts should NEVER be used for testing. Separate credentials, separate domain context.

---

## Interview Talking Points

1. **"It Was Supposed to Be Test" Is Not a Defense:** "When a tester locks out the CISO's production account, 'I thought it was the test DC' doesn't help. Environment separation must be enforced technically — different credentials, different networks, explicit target lists — not left to human memory."

2. **Blast Radius Review Before Every Destructive Test:** "Before you push enter on a ransomware simulation, ask: 'What exactly can this reach? What mounts are shared? What happens if containment fails?' If you can't answer those questions definitively, don't run the test."
