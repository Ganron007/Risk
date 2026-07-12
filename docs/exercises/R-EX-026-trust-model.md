# R-EX-026 — Forest trust risk

**Domain 3**

## Task
Explain why `cadre.local` ↔ `range.local` trust matters for RISK-003. What control review is required?

## Answer key
Cross-forest auth expands blast radius. Review SID filtering, selective auth, monitoring of inter-realm Kerberos. CTL-TRUST-REVIEW.
