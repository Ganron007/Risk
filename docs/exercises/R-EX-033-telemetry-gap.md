# R-EX-033 — Telemetry gap review

**Domain 6**  
**Inputs:** architecture telemetry, RISK-010

## Task
Name three attack steps that need both host (Elastic) and network (monitor) telemetry. Identify one gap if NSM is dark.

## Answer key
Kerberoast (host 4769 + optional network), DCSync (4662 + DRSUAPI), lateral SMB. Gap: without AST-012 you lose protocol-level corroboration and Suricata SID confirmation.
