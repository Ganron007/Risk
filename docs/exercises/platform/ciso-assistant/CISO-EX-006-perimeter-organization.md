# CISO-EX-006 — Perimeter and domain organization

**Platform:** CISO Assistant Community Edition  
**Time:** 15 minutes  
**CISSP Domains:** 2 (Asset Security), 3 (Security Architecture)

---

## Objective

Organize Cadre Corp's assets into logical perimeters and domains in CISO Assistant, mapping the three-tier classification scheme (Restricted, Confidential, Internal) to the platform's organizational model.

---

## Steps

### Step 1 — Create perimeters matching asset classification
1. Navigate to **Settings** → **Perimeters**.
2. Create three perimeters:

| Perimeter | Assets Included | Classification |
|-----------|----------------|----------------|
| **Identity & PKI Plane** | AST-001–003 (DCs), AST-034 (ADCS), AST-020 (Entra ID) | Restricted |
| **SOC & Business Ops** | AST-010–012 (elk, vr, monitor), AST-004–006 (mbr01, mbr02, linux01), AST-030–033 (data stores) | Restricted/Confidential |
| **Lab & Research** | AST-007 (ws01), AST-013 (provisioning), AST-035 (DarkAI), RevAI, Praxis | Internal/Confidential |

### Step 2 — Map perimeters to risk scenarios
For each perimeter, associate the relevant risks:
- Identity Plane → RISK-001 (DCSync), RISK-002 (ADCS ESC), RISK-003 (Cross-forest trust)
- SOC & Business Ops → RISK-007 (Evidence breach), RISK-009 (SIEM outage), RISK-010 (NSM gap)
- Lab & Research → RISK-012 (Lab breakout), RISK-013 (Prompt injection), RISK-014 (Malware mishandling)

### Step 3 — Verify perimeter-risk coverage
Review the UI: each risk should be associated with a perimeter. Perimeters without risks = no security monitoring focus. Risks without perimeters = unowned risks.

---

## Verification Checklist

- [ ] 3 perimeters created matching Cadre Corp's classification scheme
- [ ] All 18 risks associated with at least one perimeter
- [ ] No perimeter has zero risks

---

## CISSP Connection

**Domain 2:** Asset grouping by classification tier is an asset security fundamental. The perimeters in CISO Assistant operationalize the classification scheme.

**Domain 3:** Security architecture defines trust boundaries. The perimeters map to Cadre Corp's security zones — a practical implementation of the network segmentation principles from R-EX-033.

---

## Interview Talking Points

1. **"Perimeters group risk by impact zone":** "I don't manage 35 assets individually — I group them into three perimeters by classification tier. Each perimeter has its own risk profile: Identity Plane is all about credential compromise; SOC Ops is about detection continuity; Lab is about isolation. The board understands perimeters better than individual asset IDs."