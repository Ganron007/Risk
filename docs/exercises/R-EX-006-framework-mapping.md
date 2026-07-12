# R-EX-006 — Framework mapping

**CISSP skill:** Framework alignment  
**Inputs:** [`../control-register.md`](../control-register.md)

## Task

1. Map CTL-HITL, CTL-COC, CTL-SIEM-IDENTITY, CTL-LAB-ISOLATION to NIST CSF functions.
2. Pick one ISO 27001 control for each.
3. Explain how intentional AD vulnerabilities in the lab should appear in an SoA.

## Answer key

1. HITL→PR.IP; COC→PR.IP; SIEM-IDENTITY→DE.AE; LAB-ISOLATION→PR.PT (or PR.AC).
2. Examples: A.5.37, A.5.33, A.8.15, A.8.22 (approx — memorize concepts not exact clause numbers for CISSP).
3. SoA should mark production-equivalent controls as **implemented**; lab attack surfaces as **accepted residual risk for training**, scoped out of production client estates.

**Pass criteria:** You can explain Detect vs Protect without conflating them.
