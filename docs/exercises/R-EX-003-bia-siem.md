# R-EX-003 — BIA for Elastic SIEM (AST-010)

**CISSP skill:** Business impact analysis  
**Inputs:** enterprise context, RISK-009

## Task

1. Identify two business processes that depend on AST-010.
2. Estimate RTO/RPO (illustrative) for SOC retainer monitoring.
3. State the worst-case impact if SIEM is dark for 72 hours during an active client IR.

## Answer key

1. Continuous monitoring for retainers; detection engineering / campaign validation telemetry.
2. Example: RTO 4–8h (SOC Lead escalate), RPO near-zero for security events (prefer short ILM hot retention, not loss).
3. Missed DCSync/Kerberoast telemetry → delayed containment → contractual SLA breach + appetite violation on detection capability.

**Link:** RISK-009 treatment remains Mitigate (availability + access controls).
