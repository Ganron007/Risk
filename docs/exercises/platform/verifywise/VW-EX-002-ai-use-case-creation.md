# VW-EX-002 — AI use case creation and EU AI Act classification

**Platform:** VerifyWise  
**Time:** 25 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 8 (Software Development Security)  
**Prerequisites:** VW-EX-001 completed, org admin logged in

---

## Objective

Register Cadre Corp's three AI/ML projects in VerifyWise, classify each under the EU AI Act risk categories, and document their purpose, data flows, and risk profiles. This demonstrates AI system inventory management — foundational for AI governance under emerging regulations.

---

## Steps

### Step 1 — Register Project 1: DarkAI
1. Navigate to **Projects** → **Create Project** (or **AI Use Cases** depending on UI version).
2. Fill in:
   - **Name:** `DarkAI — LLM Prompt Injection Testing Lab`
   - **Category/Type:** Research & Development
   - **Description:** Research lab running LLM-based prompt injection testing against security tools. Generates synthetic attack prompts to evaluate LLM-integrated security products. Model: Claude via API (Anthropic). Isolated on Docker network `172.20.0.0/24`.
   - **EU AI Act Classification:** **Limited Risk** — research environment, no direct consumer impact, but generates adversarial content that could be misused if leaked.
   - **Data processed:** Synthetic attack prompts (no PII), lab API keys, detection methodology outputs.
   - **Risk Owner:** R&D Lead

### Step 2 — Register Project 2: RevAI
1. **Name:** `RevAI — LLM-Assisted Malware Reverse Engineering`
2. **Description:** Automated malware analysis pipeline: sample intake → static analysis → LLM-assisted decompilation → YARA rule generation → verdict reporting. Uses DeepSeek API for code analysis. Processes real malware samples (MTA corpus).
3. **EU AI Act Classification:** **High Risk** — system generates security findings (YARA rules, malware verdicts) that feed into DFIR-Nexus operational findings. Incorrect AI output could cause false positives (blocking legitimate software) or false negatives (missing real malware). HITL approval gate mitigates but does not eliminate risk.
4. **Risk Owner:** DFIR Lead

### Step 3 — Register Project 3: Praxis
1. **Name:** `Praxis — AI-Native Security Scanner`
2. **Description:** AI-powered code scanning CLI: 25 parallel agents analyze codebases for vulnerabilities, secrets, and compliance issues. Uses LLM providers (Anthropic, OpenAI) for deep analysis mode. Sends source code snippets to third-party LLM APIs.
3. **EU AI Act Classification:** **Limited Risk** — security tool, not consumer-facing. Primary concern: source code egress to third-party LLM APIs (data residency, confidentiality). CI gate integration prevents unsupervised operation.
4. **Risk Owner:** SOC Lead

### Step 4 — Verify the AI system inventory
Navigate to the project dashboard. You should see all three projects with their EU AI Act classifications. The Risk Owner should be assigned for each. This inventory is the foundation for VW-EX-003 (model inventory) and VW-EX-004 (detailed AI risk assessment).

---

## Verification Checklist

- [ ] DarkAI registered with Limited Risk classification
- [ ] RevAI registered with High Risk classification
- [ ] Praxis registered with Limited Risk classification
- [ ] All three have Risk Owners assigned
- [ ] EU AI Act classifications visible in dashboard

---

## CISSP Connection

**Domain 1:** EU AI Act risk classification (Prohibited, High, Limited, Minimal) maps directly to traditional risk management — it's a regulatory risk taxonomy applied to a specific asset class (AI systems).

**Domain 8:** AI systems in the SDLC context — RevAI and Praxis are both developer tools with AI components. Their security impacts the software they analyze and generate. The EU AI Act classification exercise demonstrates understanding that AI supply chain and output integrity are SDLC concerns.

---

## Interview Talking Points

1. **"I classify AI risk, not just IT risk":** "The EU AI Act requires organizations to classify AI systems by risk tier. I've classified Cadre Corp's three AI projects: RevAI as High Risk (generates security findings that affect operations), DarkAI and Praxis as Limited Risk. This classification drives the controls we apply — High Risk systems get HITL approval gates, enhanced monitoring, and documented model cards."

2. **"AI inventory is the new asset inventory":** "Just like you can't secure what you don't know you have, you can't govern AI systems you haven't inventoried. The three projects in VerifyWise are Cadre Corp's AI system inventory — the foundation for ISO 42001 certification and EU AI Act compliance."
