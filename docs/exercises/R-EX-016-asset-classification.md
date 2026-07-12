# R-EX-016 — Classify the estate

**Domain 2 · Asset classification**  
**Inputs:** `config/asset-inventory.csv`

## Task
1. Pick AST-030, AST-031, AST-035, AST-007 — justify Restricted / Confidential / Internal.
2. Propose a labeling rule for new VMs.

## Answer key
1. AST-030 Restricted (client legal); AST-031 Confidential (telemetry); AST-035 Internal (research); AST-007 Internal (analyst endpoint).  
2. If holds client evidence or forest identity → Restricted; business ops/telemetry → Confidential; labs/workstations → Internal unless elevated.
