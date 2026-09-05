# VW-EX-003 — AI model inventory management

**Platform:** VerifyWise  
**Time:** 20 minutes  
**CISSP Domains:** 2 (Asset Security), 8 (Software Development Security)  
**Prerequisites:** VW-EX-002 completed, AI projects registered

---

## Objective

Register the specific AI models used by each Cadre Corp project in VerifyWise's model inventory. Track model version, provider, purpose, and known limitations. This is the AI equivalent of an asset inventory — essential for model supply chain security and regulatory compliance.

---

## Steps

### Step 1 — Register the RevAI model
1. Navigate to the RevAI project → **Model Inventory** → **Register Model**.
2. Fill in:
   - **Model Name:** `DeepSeek-V3 (RevAI Analysis)`
   - **Provider:** DeepSeek (API)
   - **Version:** Latest (auto-updated via API)
   - **Purpose:** Malware decompilation analysis, YARA rule generation, verdict classification
   - **Training Data Provenance:** Proprietary — DeepSeek training corpus, not fine-tuned by Cadre Corp
   - **Known Limitations:** Hallucination in complex unpacked binaries; may generate syntactically incorrect YARA rules; confidence varies with obfuscation level
   - **Input Data:** Decompiled code (C pseudocode from Ghidra), function call graphs, strings output
   - **Output Data:** Malware verdict (malicious/benign/suspicious), YARA rules, function summaries
   - **HITL Gate:** All outputs are DRAFT until human examiner cryptographically approves (DFIR-Nexus HITL)

### Step 2 — Register the DarkAI model
1. **Model Name:** `Claude (Anthropic) — DarkAI Prompt Testing`
2. **Provider:** Anthropic (API)
3. **Purpose:** Prompt injection research, security tool evaluation, synthetic adversarial testing
4. **Known Limitations:** May refuse ethically ambiguous prompts (safety filters); prompt injection research may trigger provider rate limiting or account review
5. **Safeguards:** Isolated Docker network; no production data in prompts; synthetic test data only

### Step 3 — Register the Praxis model(s)
1. **Model Name:** `Claude + GPT-4o (Multi-Provider) — Praxis Deep Analysis`
2. **Provider:** Anthropic + OpenAI (API)
3. **Purpose:** Deep code analysis for vulnerability detection, secret identification, compliance mapping
4. **Data Egress Concern:** Source code sent to third-party LLM APIs — requires client consent for proprietary code analysis; local-only mode (Ollama) available for sensitive codebases

### Step 4 — Verify the model inventory
Navigate to the model inventory dashboard. Confirm all models are listed with provider, version, and project association. This inventory enables: (a) rapid assessment when a model CVE or vulnerability is disclosed, (b) verification that models are obtained from trusted sources, (c) documentation for ISO 42001 certification.

---

## Verification Checklist

- [ ] 3 models registered across 3 projects
- [ ] Each model has provider, version, purpose, and limitations documented
- [ ] RevAI model has HITL gate documented
- [ ] Praxis model has data egress concern documented

---

## CISSP Connection

**Domain 2:** The AI model inventory is the extension of asset inventory principles to AI systems. Just as `config/asset-inventory.csv` tracks traditional assets, the model inventory tracks AI-specific assets — model version, training data provenance, and known limitations.

**Domain 8:** Model supply chain security. When a vulnerability in a model architecture is disclosed, the model inventory enables rapid identification of affected systems — same principle as SBOM for software dependencies.

---

## Interview Talking Points

1. **"Models are assets too":** "You can't secure AI systems without knowing which models you're running, where they came from, and what they're doing. The model inventory is the AI asset register. When the next 'Log4Shell for LLMs' drops, I can query VerifyWise and answer 'are we affected?' in 60 seconds."

2. **"HITL is documented, not assumed":** "The RevAI model entry explicitly states that all outputs are DRAFT until human approval. That's not just a process note — it's a control requirement documented in the AI governance platform. The auditor sees it; the regulator sees it; the client sees it."