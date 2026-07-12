# R-EX-001 — Risk register setup

**CISSP skill:** Risk identification  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md), `config/asset-inventory.csv`

## Task

1. List five Restricted assets and one plausible threat to each.
2. Confirm each appears (or should appear) in the baseline register.
3. Propose one new RISK-019 for an asset currently under-covered.

## Answer key

1. Examples: AST-001 (DCSync), AST-034 (ADCS ESC), AST-030 (evidence theft), AST-010 (SIEM wipe), AST-020 (Entra admin takeover).
2. RISK-001, 002, 007, 009, 011 cover those themes.
3. Example RISK-019: “Provisioning Ansible vault leak → mass config change” on AST-013 — High if secrets unprotected.

**Pass criteria:** You can defend asset→threat→register linkage without inventing hosts outside the inventory.
