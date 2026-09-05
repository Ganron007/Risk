# CISO-EX-008 — Report generation for executives

**Platform:** CISO Assistant Community Edition  
**Time:** 15 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 7 (Security Operations)

---

## Objective

Generate an executive risk report from CISO Assistant's risk register, export it in a board-ready format, and tailor the content for a non-technical audience. This directly maps to R-EX-010 (Board memo) and R-EX-074 (Report writing) — now with platform-generated data.

---

## Steps

### Step 1 — Generate the risk report
1. Navigate to **Reports** → **Generate Report**.
2. Configure:
   - **Scope:** Cadre Corp domain, all perimeters
   - **Risks:** All (18 risks)
   - **Format:** Executive Summary + Risk Matrix
   - **Audience:** Board of Directors

### Step 2 — Review and tailor the report
The platform-generated report will include technical details. For board presentation:
1. **Keep:** Risk heatmap, top 5 risks by score, treatment breakdown, trend (if historical data exists).
2. **Remove/Simplify:** Individual control details, CVSS scores, technical remediation steps.
3. **Add:** Executive narrative — "Three risks scored Critical (score 9+): DCSync domain compromise, ADCS certificate abuse, and unconstrained delegation on mbr01. All three have active mitigation plans with Q1 2027 target closure."

### Step 3 — Export to PDF
Export the tailored report to PDF. Save to `artifacts/board-memo-YYYY-MM-DD.pdf`. This PDF, combined with the Markdown board memo from `src/board_report.py`, provides both a platform-generated view and a custom narrative view.

### Step 4 — Cross-reference with Markdown SSoT
Compare the CISO Assistant report with `docs/risk-register-baseline.md`. Verify: (a) risk counts match, (b) scores match, (c) owners match. Any discrepancy indicates a sync issue between the Markdown SSoT and the GRC sink.

---

## Verification Checklist

- [ ] Executive report generated from CISO Assistant
- [ ] Report tailored for board audience (technical details removed)
- [ ] PDF exported to `artifacts/`
- [ ] Cross-reference confirms consistency with Markdown risk register

---

## CISSP Connection

**Domain 1:** Executive communication of risk is a CISSP leadership competency. The platform report provides the data; the CISO provides the narrative. Both are needed for effective board communication.

**Domain 7:** Report generation from operational data (dashboard → report) is a security operations function — translating monitoring data into management information.

---

## Interview Talking Points

1. **"I generate board reports, not just risk registers":** "CISO Assistant produces the report data — heatmap, top risks, treatment status. I add the narrative: why these risks matter to the business, what we're doing about them, and what we need from the board. The report is the product of the risk program, not just a data dump."

2. **"Cross-reference proves consistency":** "I compared the CISO Assistant export with our Markdown risk register — counts, scores, owners all match. The auditor sees two independent views of the same data, confirming the risk register is controlled and consistent."