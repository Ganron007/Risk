# CISO-EX-007 — Dashboard navigation and interpretation

**Platform:** CISO Assistant Community Edition  
**Time:** 15 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 7 (Security Operations)

---

## Objective

Navigate CISO Assistant's risk dashboard, interpret the visualizations, and extract actionable insights. Demonstrate the ability to use a GRC dashboard for executive communication and operational decision-making.

---

## Steps

### Step 1 — Navigate the main dashboard
1. From the CISO Assistant home screen, review the four key panels:
   - **Risk Heatmap:** 5×5 grid showing risk concentration — where do most risks cluster?
   - **Risk by Perimeter:** Bar chart — which perimeter has the most risks?
   - **Risk by Treatment:** Pie chart — how many risks are Mitigate vs Accept vs Transfer?
   - **Recent Activity:** Timeline of risk updates and assessments.

### Step 2 — Interpret the heatmap
1. Identify the "hot zone" — risks clustering in High-Likelihood × High-Impact (top-right quadrant).
2. For Cadre Corp: RISK-001, 002, and 004 should be in the Critical zone.
3. Question to answer: "If I could fix only three risks, which three would most reduce our risk exposure?"

### Step 3 — Extract a board-ready insight
From the Treatment pie chart: "Of 18 risks, 16 are Mitigate (89%), 1 is Accept (RISK-014 with isolation controls), 1 is Transfer (cyber insurance candidate). This demonstrates active risk management — we're not just cataloging risks, we're treating them."

### Step 4 — Set up a dashboard filter for operational use
Create a filtered view: "Risks scored ≥ 15 (High/Critical) where treatment is Mitigate and status is Open." This is the SOC and Infra team's priority backlog — refreshed daily.

---

## Verification Checklist

- [ ] Heatmap shows risk concentration zones
- [ ] Perimeter bar chart identifies highest-risk perimeter
- [ ] Treatment pie chart demonstrates active management
- [ ] Filtered view created for operational backlog

---

## CISSP Connection

**Domain 1:** Dashboard interpretation is the practical application of security metrics — turning risk register data into visual, actionable information for different audiences.

**Domain 7:** The filtered operational view (High/Critical risks, Open status) is a SOC KRI dashboard — answering "what should we be worried about right now?"

---

## Interview Talking Points

1. **"I don't just maintain a risk register — I use it":** "The dashboard answers 'what's our risk posture today?' in one screen. The board sees the heatmap and treatment breakdown. The SOC Lead sees the filtered operational backlog. Different audiences, same data, different views."

2. **"89% treatment rate proves active management":** "When the board asks 'are we doing anything about these risks?' I point to the treatment breakdown: 89% actively mitigated, with owners, deadlines, and progress tracking. That's a governance story, not just a compliance checkbox."