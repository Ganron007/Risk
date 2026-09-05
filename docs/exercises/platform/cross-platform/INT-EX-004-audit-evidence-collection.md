# INT-EX-004 — Audit evidence collection across platforms

**Platforms:** CISO Assistant + VerifyWise | **Time:** 20 min | **CISSP:** 1, 6

---

## Objective

Collect and organize audit evidence from both GRC platforms to satisfy a simultaneous SOC 2 + ISO 42001 audit. Demonstrate the ability to efficiently produce evidence across multiple frameworks and platforms.

---

## Steps

### Step 1 — Identify evidence requirements
For a combined SOC 2 Type II + ISO 42001 surveillance audit:
- **SOC 2:** Evidence of control operating effectiveness over 6-12 months for Security and Confidentiality TSCs
- **ISO 42001:** Evidence of AI management system operation — AI risk assessments, model inventory, human oversight, monitoring

### Step 2 — Collect evidence from CISO Assistant
Export: SOC 2 control mapping report, risk treatment evidence (dated mitigation status changes), access review logs, and control effectiveness metrics.

### Step 3 — Collect evidence from VerifyWise
Export: AI system inventory (projects + models), EU AI Act classification documentation, AI risk assessments with mitigation tracking, HITL approval logs, and lifecycle stage documentation.

### Step 4 — Organize into audit package
Structure the evidence package:
```
audit-evidence/
├── soc2/
│   ├── control-mapping.pdf
│   ├── risk-treatment-evidence.pdf
│   └── access-review-logs.csv
├── iso42001/
│   ├── ai-inventory.pdf
│   ├── ai-risk-assessments.pdf
│   └── hitl-approval-logs.csv
└── cross-platform/
    └── unified-control-mapping.pdf
```

### Step 5 — Pre-audit dry run
Have a colleague play "auditor" — can they find the evidence for each control in under 5 minutes? If not, reorganize.

---

## Interview Talking Points

1. **"Evidence is organized before the auditor arrives":** "When the SOC 2 and ISO 42001 auditors show up, I don't scramble through email and Slack. I hand them a structured evidence package organized by framework and control — extracted from both GRC platforms, cross-referenced, and pre-validated."