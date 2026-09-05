# INT-EX-005 — Executive dashboard integration

**Platforms:** CISO Assistant + VerifyWise | **Time:** 20 min | **CISSP:** 1, 7

---

## Objective

Create a unified executive dashboard that combines classic GRC metrics (CISO Assistant) and AI governance metrics (VerifyWise) into a single-pane-of-glass view for board and CISO consumption.

---

## Steps

### Step 1 — Define unified KPIs
| KPI | Source | Target |
|-----|--------|--------|
| Total risks under management | CISO + VW (deduplicated) | <25 (manageable span) |
| Risk treatment rate | Both platforms | >85% actively mitigated |
| Critical risks (score ≥9) | CISO Assistant | <5 at any time |
| AI systems compliant with EU AI Act | VerifyWise | 100% classified |
| HITL coverage for AI outputs | VerifyWise | 100% |
| Framework coverage (ISO 27001) | CISO Assistant | >80% Annex A |
| Framework coverage (ISO 42001) | VerifyWise | >75% |

### Step 2 — Build the unified dashboard
Option A: Use CISO Assistant's dashboard APIs + VerifyWise's APIs → feed into a Grafana/Elastic dashboard.
Option B: Manual consolidation — export both platform reports monthly, combine into a single executive PDF with commentary.

### Step 3 — Present the unified view
Sample board slide: "Cadre Corp manages 21 risks across 2 platforms. 89% actively mitigated. 3 Critical risks — all with active remediation plans targeting Q1 2027 closure. 3 AI systems — 100% EU AI Act classified, 100% under human oversight. ISO 27001: 82% Annex A coverage. ISO 42001: 78% clause coverage."

---

## Verification Checklist

- [ ] Unified KPIs defined with sources and targets
- [ ] Dashboard built or manual consolidation process documented
- [ ] Single-page executive summary template created

---

## Interview Talking Points

1. **"One slide, complete risk picture":** "I can present Cadre Corp's entire risk posture — classic AND AI — on one slide. 21 risks, 89% mitigated, 3 Critical, 100% AI oversight. The data comes from two platforms, but the board sees one picture. That's the GRC integration story."