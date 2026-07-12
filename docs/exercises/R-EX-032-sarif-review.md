# R-EX-032 — Review Praxis SARIF

**Domain 6**  
**Inputs:** `samples/findings/praxis-sarif-sample.sarif`, `python -c` adapters

## Task
1. Convert SARIF → unified findings via `sarif_to_findings`.  
2. Score and decide Accept vs Mitigate.

## Answer key
Secret pattern → Mitigate (rotate, remove hardcode, Praxis CI gate). Severity medium/high depending on secret class. Ties to RISK-013 / CTL-PRAXIS-SCAN.
