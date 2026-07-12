# R-EX-040 — SIEM disaster recovery sketch

**Domain 7**  
**Asset:** AST-010 / RISK-009

## Task
Define RTO, backup target, and interim monitoring if elk is down 24h.

## Answer key
RTO ≤ 8h preferred. Restore from snapshots + ILM-aware backups. Interim: Suricata/Zeek local eve.json + VR hunts + manual Sysmon pulls. Board notified if >4h per KRI.
