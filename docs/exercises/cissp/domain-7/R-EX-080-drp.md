# R-EX-080 — Disaster recovery planning (DRP)

**CISSP Reference:** Chapter 18, Sections "Recovery Strategies", "Recovery Plan Development", "Testing and Maintenance"  
**Exam Objective:** 7.4.2 Develop DRP; 7.4.3 Test disaster recovery  
**Study Guide Key Terms:** DRP, hot site, warm site, cold site, reciprocal agreement, failover, failback, tabletop exercise, simulation test  

---

## Scenario Context

Building on the BCP exercise (R-EX-079), Cadre Corp needs a formal disaster recovery plan for the lab infrastructure. The single VMware host is the single point of failure. The current "backup strategy" is: VMware snapshots taken "when someone remembers" (last snapshot: 47 days ago), stored on the same physical disk as the VMs (so a disk failure destroys both production AND backups), and never tested — nobody knows if they can actually restore from them.

---

## Multiple-Choice Questions

**Question 1:** What is the difference between BCP and DRP?

A. They're the same thing  
B. BCP covers business processes and operations continuity; DRP specifically covers IT system and data recovery — DRP is a subset of BCP focused on technology restoration  
C. BCP is for small incidents; DRP is for major disasters  
D. DRP replaces BCP for technology companies

**Question 2:** Cadre Corp's backup storage (same disk as production) violates what backup principle?

A. Backups should be encrypted  
B. The 3-2-1 rule: 3 copies of data, on 2 different media, with 1 copy off-site — storing backups on the same physical disk means a single hardware failure destroys everything  
C. Backups should be taken daily  
D. Backups should be compressed

**Question 3:** A DRP test that involves actually failing over to the recovery site and processing real work there is called:

A. Tabletop exercise  
B. Simulation test  
C. Full-interruption test — the most realistic and disruptive; it validates that recovery actually works but risks production impact if recovery fails  
D. Checklist review

---

## Answer Explanations

**Answer 1: B**  
**BCP is the umbrella; DRP is the IT subset**. BCP covers: who declares a disaster, where do people work, how do we communicate with clients, how do we continue critical business processes (not just IT). DRP covers: how do we restore servers, databases, networks, and applications to meet the RTO/RPO targets defined in the BIA. DRP answers "how do we get the technology back?" BCP answers "how do we keep the business running while we do it?"

**Answer 2: B**  
The **3-2-1 rule** is the foundational backup principle: **3 copies** of data, on **2 different media types**, with **1 copy off-site** (geographically separate). Cadre Corp's approach violates all three: snapshots + production = same disk = same media = same location. A fire, disk failure, or ransomware that hits the host destroys everything simultaneously.

**Answer 3: C**  
A **full-interruption test** actually fails over to the recovery site and processes real work. It's the only test that validates: (a) backups are restorable, (b) recovery procedures work end-to-end, (c) recovered systems can handle production load. It's also the riskiest — if recovery fails, production is down. Less disruptive tests (tabletop, simulation, parallel) should precede it.

---

## Cadre Corp Application

1. **3-2-1 Backup Implementation:** (a) Primary: VM running on host disk, (b) Copy 2: nightly backup to a separate NAS or external drive (different media), (c) Copy 3: weekly backup to Azure Blob Storage (off-site). Automate via script; monitor backup success with alerts on failure.

2. **Restore Testing:** Quarterly: restore one random VM from backup and verify it boots and services start. Document the result. A backup you haven't tested isn't a backup — it's a wish.

3. **DRP Document:** This exercise IS the start of the DRP document. Include: recovery team contacts, step-by-step restore procedures, VM priority order (DCs first, then SOC, then lab), and post-recovery validation tests.

---

## Interview Talking Points

1. **Untested Backups Are Wishes, Not Backups:** "If you've never restored from your backup, you don't have a backup — you have a hope. Test restores quarterly. The day you discover your backup script has been failing silently for 6 months is not the day of a real disaster."

2. **3-2-1 Isn't Optional:** "Backup on the same disk as production isn't a backup — it's a copy waiting to die with the original. Ransomware that encrypts the host encrypts your 'backup' too. Off-site, different media, tested regularly."
