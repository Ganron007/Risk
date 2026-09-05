# R-EX-079 — Business continuity planning (BCP)

**CISSP Reference:** Chapter 3, Section "Business Continuity Planning"; Chapter 18, Section "Disaster Recovery Planning"  
**Exam Objective:** 7.4.1 Develop BCP; 1.3.1 Understand business impact analysis  
**Study Guide Key Terms:** BCP, BIA, RTO, RPO, MTD, business continuity strategy, crisis management, succession planning  

---

## Scenario Context

Cadre Corp's entire lab runs on a single VMware Workstation host in the Chicago office. If that host fails — hardware failure, power outage, or ransomware — ALL lab operations stop: no forensic analysis, no SOC monitoring, no client evidence access, no campaign exercises.

The CISO asks: "What's our plan if the lab host dies?" The answer: "We'd order a new server and restore from backup — probably 3-5 days." The CISO counters: "Our client SLA says evidence analysis within 24 hours. Three to five days means we're in breach on day 2."

---

## Multiple-Choice Questions

**Question 1:** RTO (Recovery Time Objective) in BCP refers to:

A. The time it takes to order new hardware  
B. The maximum acceptable time a system or process can be unavailable before the business suffers unacceptable harm — for Cadre Corp's forensic analysis, this is 24 hours per client SLA  
C. The time it takes to restore from the most recent backup  
D. The time between disaster declaration and team notification

**Question 2:** RPO (Recovery Point Objective) defines:

A. The maximum acceptable amount of data loss measured in time — e.g., "we can lose up to 1 hour of SIEM logs" means backups must run at least hourly  
B. The point in time when recovery begins  
C. The physical recovery location  
D. The person responsible for recovery

**Question 3:** A Business Impact Analysis (BIA) is conducted BEFORE developing the BCP because:

A. It's a regulatory requirement with no practical value  
B. The BIA identifies which business functions are critical, what their maximum tolerable downtime (MTD) is, and what resources they depend on — this drives RTO/RPO targets and recovery prioritization  
C. It replaces the need for risk assessment  
D. It's the same as a vulnerability assessment

---

## Answer Explanations

**Answer 1: B**  
**RTO is the maximum acceptable downtime** before business impact becomes unacceptable. Cadre Corp's client SLA = 24 hours → RTO for forensic analysis capability must be less than 24 hours. "3-5 days" exceeds this by 3-4x, meaning the current recovery plan doesn't meet business requirements. RTO drives recovery strategy: if RTO = 4 hours, you need hot standby; if RTO = 7 days, you can order new hardware.

**Answer 2: A**  
**RPO is maximum acceptable data loss**, measured in time. RPO = 1 hour means you must back up at least hourly; losing up to 1 hour of data is acceptable. RPO = 0 means zero data loss (continuous replication, synchronous mirroring). For Cadre Corp's client evidence, RPO should be as close to 0 as practical — losing forensic evidence is not acceptable.

**Answer 3: B**  
The **BIA identifies what matters and how long you can live without it**. Before writing a BCP, you must know: which functions are critical? What's their MTD? What dependencies do they have (systems, people, vendors, data)? The BIA's output is the RTO/RPO targets that drive recovery strategy. Doing BCP without BIA is like buying insurance without knowing what you're insuring.

---

## Cadre Corp Application

1. **BIA for Cadre Corp:** Identify critical business functions: forensic analysis (MTD: 24 hours per SLA), SOC monitoring (MTD: 4 hours — detection blindness risk), client evidence access (MTD: 12 hours — contractual), lab infrastructure (MTD: 48 hours for non-client-facing research).

2. **BCP Strategy:** Given the single-host constraint, options: (a) cold standby — second host pre-purchased, configured, ready to restore backups → RTO ~24 hours, (b) warm standby — second host with replicated VMs, manual failover → RTO ~4 hours, (c) cloud burst — replicate critical VMs to Azure, failover in <1 hour → highest cost, best RTO. Recommend based on BIA and budget.

3. **Succession Planning:** Document who can operate the lab if the Infra Lead is unavailable. Cross-train at least one other person on VMware recovery, Ansible provisioning, and backup restoration.

---

## Interview Talking Points

1. **RTO Drives Everything:** "If your client SLA says 24 hours and your recovery plan says 3-5 days, you don't have a recovery plan — you have a breach plan. RTO is the number that drives whether you need cold standby, warm standby, or hot site."

2. **BIA Before BCP — Always:** "Don't write a business continuity plan until you know what's worth recovering and how fast. The BIA answers 'what matters?' The BCP answers 'how do we recover it?' Without the first, the second is guessing."
