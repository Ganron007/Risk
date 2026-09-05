# R-EX-076 — Log management and SIEM operations

**CISSP Reference:** Chapter 16, Section "Logging and Monitoring"; Chapter 17, Section "Detection and Preventive Measures"  
**Exam Objective:** 7.2.1 Implement logging and monitoring; 7.2.2 Manage SIEM operations  
**Study Guide Key Terms:** SIEM, log aggregation, log retention, centralized logging, log integrity, time synchronization, use cases, correlation rules  

---

## Scenario Context

Cadre Corp's Elastic SIEM (AST-010) ingests logs from: Windows Event Logs (all 7 VMs), Zeek (conn/dns/http/kerberos), Suricata (eve.json), and Velociraptor. However, during the campaign exercise, several gaps emerged:

1. Windows Event Logs from `mbr01` stopped flowing to Elastic for 3 weeks due to a Winlogbeat service crash — nobody noticed because there was no heartbeat monitoring.
2. Log timestamps across VMs drifted by up to 8 minutes because NTP wasn't enforced — making it impossible to correlate an attack across Suricata (UTC) and Windows Event Logs (local time + drift).
3. The Elastic ILM policy accumulated 20 GB of logs with no delete phase (fixed in Sprint 0).
4. When the SOC Lead tried to investigate a 45-day-old incident, the relevant Zeek logs had already rolled over and were gone.

---

## Multiple-Choice Questions

**Question 1:** Why is time synchronization (NTP) critical for SIEM operations?

A. It ensures logs don't take up too much disk space  
B. Without synchronized timestamps, correlating events across multiple sources is unreliable — an attacker's action might appear in Zeek at 14:03:00 UTC and in Windows Event Log at 14:11:00 because of clock drift, breaking the attack timeline  
C. NTP improves SIEM search performance  
D. Time sync is only needed for compliance, not operations

**Question 2:** Cadre Corp's 3-week Winlogbeat outage represents a failure in:

A. Log parsing rules  
B. Log source health monitoring — there was no alert when a log source stopped sending data, creating a detection blind spot for 3 weeks  
C. Storage capacity planning  
D. Log encryption configuration

**Question 3:** What is the appropriate log retention period for a DFIR firm like Cadre Corp?

A. 7 days — anything older isn't relevant  
B. Risk-based: hot storage (immediately searchable) = 30-90 days for active investigations; warm/cold storage = 1 year for compliance and trend analysis; client evidence logs = per-engagement retention per contract  
C. Forever — storage is cheap  
D. Only retain logs that contain alerts

---

## Answer Explanations

**Answer 1: B**  
**Time synchronization is the foundation of log correlation**. If DC01 logs an authentication at 14:03:00 and Suricata logs the corresponding network connection at 14:11:00 (8 minutes of drift), an analyst searching for events "around 14:03" might miss the Suricata event entirely. Attack timelines become unreliable. NTP (or better, a local GPS-synced time appliance) keeps all sources within milliseconds.

**Answer 2: B**  
This is a **log source health monitoring** failure. Every log source (Winlogbeat agent, Zeek, Suricata) needs a heartbeat — if data stops flowing for more than X minutes, an alert fires. Without this, a silent agent crash creates a detection blackout that can last indefinitely. This is a fundamental SIEM operational requirement.

**Answer 3: B**  
Retention is **risk-based, not one-size-fits-all**. Hot storage (30-90 days) covers most active investigations. Warm/cold storage (1 year) covers compliance, trend analysis, and "we just found an IOC from 6 months ago — were we affected?" questions. Client evidence logs should follow contractual retention requirements (GDPR: "no longer than necessary"; specific client contracts may specify terms).

---

## Cadre Corp Application

1. **Agent Heartbeat Monitoring:** Configure Elastic Agent/Winlogbeat monitoring: if data from a host stops for >15 minutes, fire an alert. This prevents silent blackouts. This is a `cadre-e*` detection rule candidate.

2. **NTP Enforcement:** Ensure all VMs sync to DC01 (the domain's authoritative time source for Windows). For Linux VMs, configure chrony pointing to DC01. Verify with `w32tm /monitor` (Windows) and `chronyc tracking` (Linux).

3. **Retention Policy:** Implement in Elastic ILM: hot phase (30 days, full searchability) → warm phase (90 days, reduced replicas) → cold phase (1 year, searchable with delay) → delete. Document retention periods in `docs/control-register.md`.

---

## Interview Talking Points

1. **Silent Log Source Death Is a Silent SOC Death:** "When a Winlogbeat agent crashes and nobody notices for 3 weeks, your SIEM has a 3-week blind spot. Agent heartbeat monitoring is the most basic SIEM health check — and the most commonly forgotten."

2. **8 Minutes of Drift = Uncorrelatable Attack:** "Timestamps that drift by minutes make cross-source correlation impossible. You need NTP enforced on every log source, and you need to verify it. Time is the one field every log shares — if it's wrong, nothing correlates."
