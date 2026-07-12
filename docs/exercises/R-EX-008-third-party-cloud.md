# R-EX-008 — Third-party / cloud risk (Entra)

**CISSP skill:** Vendor / cloud risk  
**Inputs:** AST-020–023, RISK-011

## Task

1. Identify three risks of using a Microsoft cloud tenant for hybrid identity labs.
2. Propose due-diligence questions before enabling Cloud Sync to a more production-like tenant.
3. Choose treatment for RISK-011.

## Answer key

1. Token/admin compromise; sync of privileged on-prem accounts; misconfigured PIM/RBAC.
2. Who holds GA? Is PIM enforced? Conditional Access? Separate lab tenant vs client tenant? Sync filtering?
3. **Mitigate** — CTL-ENTRA-PIM, CTL-CLOUD-MONITOR, CTL-CLOUD-SYNC-REVIEW; do not Accept without those.

**Link:** Cloud plane is Restricted — appetite is low for hybrid identity takeover.
