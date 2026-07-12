# R-EX-028 — ADCS as design weakness

**Domain 3**  
**Asset:** AST-034 / RISK-002

## Task
Frame ESC1-style misconfig as a **design** issue, not only a patch issue. One compensating control.

## Answer key
Template permissions + enrollee-supplied subject are architecture choices. Compensate with CTL-ADCS-MONITOR + remove dangerous templates + SIEM ESC detections. Treatment: Mitigate, not Accept in production-like estates.
