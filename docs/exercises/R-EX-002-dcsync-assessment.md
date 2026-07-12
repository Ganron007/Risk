# R-EX-002 — DCSync qualitative assessment

**CISSP skill:** Qualitative risk analysis  
**Inputs:** `samples/findings/elastic-dcsync-alert.json`, RISK-001, appetite statement

## Task

1. Assign Likelihood and Impact (1–3) for finding-elastic-001; justify each.
2. State treatment per Cadre Corp appetite.
3. Name two controls that should detect or reduce this risk.

## Answer key

1. L=3 (campaign-proven / alert fired), I=3 (Restricted DC / DA path) → score 9 Critical.
2. **Remediate / mitigate immediately** — not accept; identity takeover violates low appetite.
3. CTL-SIEM-IDENTITY (4662 / DRSUAPI), CTL-AD-BASELINE (tiering, privileged access workstations).

**Tool check:** `score_finding` on the sample should yield score 9.
