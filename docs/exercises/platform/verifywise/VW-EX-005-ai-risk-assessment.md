# VW-EX-005 — AI risk assessment workflow

**Platform:** VerifyWise  
**Time:** 25 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 6 (Assessment & Testing)  
**Prerequisites:** VW-EX-002, VW-EX-004 completed

---

## Objective

Create a detailed AI risk assessment for RevAI (High Risk) in VerifyWise, scoring likelihood and severity for three AI-specific risks: prompt injection affecting malware verdicts, model supply chain compromise, and training data poisoning. Link risks to mitigation controls and document residual risk.

---

## Steps

### Step 1 — Create Risk 1: Prompt injection corrupting YARA rule generation
1. Navigate to RevAI → **Risk Assessment** → **Create Risk**.
2. Fill in:
   - **Risk:** Prompt injection in decompiled code leads LLM to generate malicious YARA rules
   - **Category:** AI Security — Prompt Injection (OWASP LLM #1)
   - **Likelihood:** Medium — decompiled malware may contain adversarial strings designed for LLM consumption
   - **Severity:** High — a prompt-injected YARA rule could whitelist the attacker's malware
   - **Mitigation:** HITL approval gate (DFIR-Nexus DRAFT → approve), output validation (YARA syntax check + sandbox testing before deployment), prompt-input sanitization
   - **Residual Risk:** Medium — HITL gate catches malicious output, but depends on human examiner diligence

### Step 2 — Create Risk 2: Model supply chain compromise
1. **Risk:** DeepSeek API model version is silently swapped for a backdoored variant
2. **Likelihood:** Low — major API provider, but supply chain attacks on model registries are emerging
3. **Severity:** Critical — a backdoored model could systematically misclassify malware as benign
4. **Mitigation:** Model version tracking in VerifyWise, output consistency monitoring (compare verdicts across model versions), provider SLA review, local model fallback (Ollama) for critical cases
5. **Residual Risk:** Low — multiple compensating controls reduce exploitability

### Step 3 — Create Risk 3: Training data poisoning (indirect)
1. **Risk:** Malware authors craft samples specifically designed to influence future LLM training (if provider uses user data for training) or fine-tuning datasets
2. **Likelihood:** Low — requires knowledge of provider training pipeline and influence over training data
3. **Severity:** Medium — could cause systematic bias in malware classification
4. **Mitigation:** Verify provider's data usage policy (does NOT use API inputs for training), use multiple model providers for critical verdicts (cross-validation), monitor for classification drift over time
5. **Residual Risk:** Low

### Step 4 — Review the risk heatmap
Navigate to the RevAI risk dashboard. Confirm the three risks appear on the heatmap with correct scores. The heatmap should show one Medium-High (prompt injection), one Low-Critical (supply chain), and one Low-Medium (data poisoning) risk — providing a visual risk profile for the RevAI project.

---

## Verification Checklist

- [ ] 3 AI-specific risks created for RevAI with likelihood, severity, and mitigation
- [ ] Residual risk documented for each
- [ ] Risk heatmap visible in RevAI project dashboard

---

## CISSP Connection

**Domain 1:** AI risk assessment follows the same methodology as traditional risk assessment (identify, analyze, evaluate, treat) — applied to a new asset class. The skills are transferable; the threat models are AI-specific.

**Domain 6:** This is an assessment activity — systematically evaluating AI-specific threats against a specific system, scoring risks, and documenting mitigations. The VerifyWise platform provides the structured assessment framework.

---

## Interview Talking Points

1. **"AI risk assessment uses the same framework — different threats":** "I assess AI risk the same way I assess AD risk: identify threats, score likelihood and impact, document mitigations, accept residual risk. The threats are different — prompt injection instead of DCSync, model supply chain instead of forest trust abuse — but the methodology is the same."

2. **"HITL is the universal AI mitigator":** "For AI systems that generate operational outputs, human-in-the-loop approval is the single most important control. Prompt injection risk? HITL catches malicious output. Model hallucination? HITL catches incorrect verdicts. It's not the only control, but it's the safety net that catches what automated controls miss."