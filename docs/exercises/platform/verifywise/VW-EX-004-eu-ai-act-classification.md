# VW-EX-004 — EU AI Act risk classification workflow

**Platform:** VerifyWise  
**Time:** 25 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 3 (Security Architecture — AI systems)  
**Prerequisites:** VW-EX-002 completed (AI projects registered)

---

## Objective

Apply the EU AI Act's four-tier risk classification system to Cadre Corp's AI projects in VerifyWise, document the classification rationale, and identify required controls for each tier. This demonstrates the ability to operationalize emerging AI regulation.

---

## Steps

### Step 1 — Understand the EU AI Act risk tiers
The EU AI Act classifies AI systems into four tiers:

| Tier | Description | Cadre Corp Examples | Required Controls |
|------|-------------|---------------------|-------------------|
| **Prohibited** | Banned — unacceptable risk | None (Cadre Corp doesn't deploy social scoring, real-time biometric surveillance, etc.) | N/A — cannot deploy |
| **High Risk** | Significant impact on safety or fundamental rights | RevAI (generates security findings), potentially Praxis if used for regulatory compliance scanning | Conformity assessment, technical documentation, human oversight, accuracy/robustness, risk management system, transparency |
| **Limited Risk** | Transparency obligations | DarkAI (research), Praxis (developer tool) | Inform users they're interacting with AI, document capabilities and limitations |
| **Minimal Risk** | No specific obligations | Basic AI features (spell check, auto-complete in internal tools) | Voluntary codes of conduct |

### Step 2 — Classify RevAI as High Risk
1. Navigate to RevAI project → **Risk Classification**.
2. Select **High Risk**.
3. Document rationale:
   - **Safety impact:** Generates YARA rules and malware verdicts used in operational security decisions. Incorrect output could cause false positives (blocking legitimate software at client sites) or false negatives (missing live malware).
   - **Rights impact:** Processes malware samples that may contain third-party code — intellectual property implications.
   - **Automated decision-making:** The LLM generates findings automatically (with HITL gate, but the LLM output is the primary analysis).
4. Document required High Risk controls: conformity assessment, technical documentation (model card), human oversight (HITL approval gate), accuracy monitoring, risk management system.

### Step 3 — Classify DarkAI and Praxis as Limited Risk
1. For each project, select **Limited Risk**.
2. Document rationale: research/development use, no direct consumer impact, human supervision present, outputs are not operational without human review.
3. Document transparency requirements: "This system uses AI/ML for [purpose]. Outputs should be reviewed by a qualified human before operational use."

### Step 4 — Document the prohibition check
Create a note or compliance document confirming: "Cadre Corp has reviewed the EU AI Act Prohibited practices list (Article 5) and confirms that no deployed AI system engages in: subliminal manipulation, exploitation of vulnerabilities, social scoring by public authorities, real-time remote biometric identification in public spaces, or emotion recognition in workplace/education contexts."

---

## Verification Checklist

- [ ] RevAI classified as High Risk with documented rationale
- [ ] DarkAI and Praxis classified as Limited Risk with documented rationale
- [ ] Required controls identified for each tier
- [ ] Prohibition check documented

---

## CISSP Connection

**Domain 1:** The EU AI Act's tiered classification is a regulatory risk framework — the same governance principles as NIST CSF tiers or ISO 27001 control categories, applied to AI systems. Understanding how to classify systems under emerging regulation is a 2026-essential CISSP skill.

**Domain 3:** AI system security architecture must account for the risk tier. High Risk systems (RevAI) require architectural controls — HITL gates, output validation, model monitoring — that Limited Risk systems (DarkAI) may not.

---

## Interview Talking Points

1. **"I can classify AI risk under live regulation":** "The EU AI Act isn't theoretical — it's law. I can take an AI system, classify it under the Act's four tiers, document the rationale, and identify the required controls. For RevAI, that's High Risk with mandatory human oversight and conformity assessment. For DarkAI and Praxis, Limited Risk with transparency obligations."

2. **"Prohibited means prohibited":** "The first step in AI Act compliance is confirming you're not deploying a prohibited system. I documented that check for Cadre Corp. It's a one-page memo that could save millions in fines — proving you did the assessment."