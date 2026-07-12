# R-EX-046 — Praxis as SSDLC gate

**Domain 8**

## Task
Where does `praxis scan ci` fit in DarkAI release? Fail criteria?

## Answer key
Pre-merge / pre-compose publish gate. Fail on high secrets or policy threshold. CTL-PRAXIS-SCAN. Evidence: SARIF in CI artifacts.
