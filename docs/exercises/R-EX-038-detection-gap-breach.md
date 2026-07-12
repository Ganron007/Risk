# R-EX-038 — What the SOC might miss

**Domain 7**

## Task
During a simulated Kerberoast→SQL→SYSTEM chain, list one miss if only Elastic Defend events exist (no Suricata).

## Answer key
Miss protocol-level Kerberos roasting burst / SMB admin share patterns that Suricata/Zeek catch. Host-only view under-corroborates. RISK-010.
