# R-EX-040 — SIEM disaster recovery planning

**CISSP Reference:** Chapter 18, Sections "Disaster Recovery Planning", "Recovery Strategies", "Testing and Maintenance"; Chapter 16, Section "Managed Services in the Cloud"  
**Exam Objective:** 7.4.2 Develop disaster recovery plans; 7.4.1 Develop business continuity plans; 7.2.1 Implement logging and monitoring resilience  
**Study Guide Key Terms:** Disaster recovery, RTO, RPO, SIEM resilience, backup strategy, interim monitoring, detection continuity, business impact of monitoring loss  
**Inputs:** [`../risk-register-baseline.md`](../risk-register-baseline.md), RISK-009, AST-010 (ELK), plan1.7 §12

---

## Scenario Context

Cadre Corp's Elastic SIEM (AST-010) ingests, indexes, and correlates telemetry from: 7 Windows VMs (Winlogbeat), Zeek (conn/dns/http/kerberos), Suricata (eve.json), and Velociraptor. RISK-009 rates "SIEM prolonged outage → detection blindness" as score 6 (High).

On a Friday at 16:45, Elasticsearch crashed due to a disk space exhaustion bug in the ILM policy (the bug that was fixed in Sprint 0 — but the fix created a new issue where rollover failed silently). The cluster is down. Logs are not being ingested. The SOC is blind.

The SOC Lead estimates:
- **Best case:** Restore from snapshot → 4 hours downtime.
- **Worst case:** Snapshot corrupted, rebuild cluster from scratch, re-ingest backlog → 24+ hours downtime.
- **During the outage:** Suricata and Zeek continue running on AST-012, writing to local JSON logs — but with no SIEM, there's no alerting, no correlation, and no dashboard visibility.

The CISO activates the SIEM disaster recovery plan and asks: "What's our interim monitoring, and when do we notify the board?"

---

## Multiple-Choice Questions

**Question 1:** What is an appropriate RTO (Recovery Time Objective) for Cadre Corp's SIEM?

A. 7 days — the SOC can work without a SIEM for a week  
B. 4-8 hours — beyond 8 hours of detection blindness, the risk of missing a critical attack during the gap becomes unacceptable for a DFIR firm monitoring 120 client retainers  
C. 30 minutes — SIEM must never be down for more than half an hour  
D. RTO is not applicable to SIEM systems

**Question 2:** During the SIEM outage, Suricata and Zeek continue writing to local logs but there's no alerting. This interim state means:

A. Detection is fully operational — local logs are sufficient  
B. Detection is degraded but not absent — raw logs are being generated and stored; the SOC can manually query them for known IOCs, but real-time alerting, cross-source correlation, and dashboard visibility are lost until the SIEM is restored  
C. All security monitoring is completely disabled  
D. Local logs can only be used for compliance, not detection

**Question 3:** What is the appropriate board notification trigger for a SIEM outage?

A. Notify the board immediately for any outage regardless of duration  
B. Risk-based notification: notify the CISO immediately; notify the board if the outage exceeds the KRI threshold (e.g., >4 hours) — the board needs to know about prolonged detection blindness, not every brief technical outage  
C. Never notify the board about technical issues  
D. Only notify the board after the SIEM is restored

**Question 4:** What is the most important test to validate the SIEM DR plan?

A. Review the DR documentation annually  
B. A full restoration test — actually restore the SIEM from backup in an isolated environment, verify data integrity, confirm dashboards load, and measure the actual restoration time against the RTO  
C. Ask the SOC team if they've read the DR plan  
D. Run a tabletop exercise once every 3 years

---

## Answer Explanations

**Answer 1: B**  
An RTO of **4-8 hours** balances operational reality with risk tolerance. For a DFIR firm: (a) each hour of SIEM blindness is an hour an attacker could operate undetected, (b) client SLAs may require continuous monitoring, (c) some detection continues (Suricata/Zeek local logs, VR hunts) — the SIEM outage degrades but doesn't eliminate detection. 7 days (A) is unacceptable for a security monitoring provider. 30 minutes (C) may be infeasible without hot standby infrastructure (>$50K). The RTO should be achievable with current infrastructure and improved over time.

**Answer 2: B**  
**Detection is degraded but persists.** Suricata writes eve.json alerts locally; Zeek writes connection/DNS/HTTP logs locally. The SOC can: (a) SSH to AST-012 and grep Suricata logs for high-severity alerts, (b) run manual Zeek queries for known-bad IPs/domains, (c) check VR for recent hunts. What's lost: real-time alerting (no Elastic alert actions), cross-source correlation (can't join Windows 4662 with Zeek DRSUAPI automatically), dashboards (manual investigation only). This is "degraded detection," not "no detection" — a critical distinction for risk assessment and board communication.

**Answer 3: B**  
**Risk-based notification thresholds** prevent alert fatigue while ensuring leadership awareness of significant events. The CISO should be notified immediately for any SIEM outage (operational awareness). Board notification triggers when the outage exceeds a pre-defined KRI threshold (e.g., 4 hours) — this indicates the DR plan is not meeting RTO and the business impact (prolonged detection blindness) is material. The KRI threshold should be defined in the risk appetite statement and agreed with the board in advance.

**Answer 4: B**  
**Full restoration testing** is the only way to validate: (a) backups are actually restorable (not corrupted — the "worst case" scenario in this incident), (b) the restoration procedure works end-to-end, (c) the actual restoration time meets RTO, (d) restored data is complete and queryable. Documentation review (A) and tabletop exercises (D) are valuable but don't test the technical restoration. A DR plan that has never been tested is not a plan — it's a hope.

---

## Cadre Corp Application

1. **SIEM DR Plan:** Document: (a) RTO = 8 hours (target), RPO = 1 hour (snapshot frequency), (b) restoration procedure (step-by-step, tested quarterly), (c) interim monitoring procedure (Suricata/Zeek local log queries, VR hunt frequency increase), (d) board notification trigger (>4 hours), (e) post-restoration validation (confirm all data sources reconnected, dashboards functional, alerts firing).

2. **Backup Validation:** Schedule quarterly restoration tests — restore the SIEM from the most recent snapshot to an isolated VM, verify data integrity, measure restoration time. If restoration fails or exceeds RTO, escalate as a finding and remediate before the next test.

3. **Interim Monitoring Runbook:** Create a 1-page runbook for the SOC: "When SIEM is down — (1) Connect to AST-012 via SSH, (2) Run `suricata-log-check.sh` for critical alerts in last hour, (3) Run `zeek-query-iod.sh` for known IOCs, (4) Increase VR hunt frequency to every 15 minutes, (5) Notify CISO if outage exceeds 1 hour."

---

## Interview Talking Points

1. **SIEM Outage ≠ Detection Blackout:** "When Elastic goes down, we're not completely blind. Suricata and Zeek keep writing logs. The SOC shifts to manual queries and increased VR hunting. Detection is degraded — slower, less correlated, more manual — but not absent. The board needs to understand the distinction: 'degraded' vs. 'blind.'"

2. **RTO Is a Promise You Must Keep:** "If your DR plan says RTO = 4 hours and you've never tested restoration, your RTO is not 4 hours — it's 'unknown.' Test quarterly. Measure actual restoration time. If it's 12 hours, either improve the process or update the RTO. An RTO you can't meet is a lie you tell your board."

3. **Notify the Board by Threshold, Not by Instinct:** "Define the KRI threshold in advance: 'SIEM outage >4 hours = board notification.' This removes the judgment call under stress. At hour 3.5, the CISO isn't wondering 'should I tell the board?' — the policy already answered that question."
