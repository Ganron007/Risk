# R-EX-087 — AI/ML system security in SDLC

**CISSP Reference:** Chapter 20, Section "Knowledge-Based Systems"; Chapter 21, Section "Application Attacks"; Domain 3 (AI Architecture)  
**Exam Objective:** 8.1.3 Secure emerging technologies; 8.2.3 Manage software supply chain (AI models)  
**Study Guide Key Terms:** AI/ML security, model integrity, training data poisoning, adversarial examples, model inversion, OWASP LLM Top 10, MITRE ATLAS, MLSecOps  

---

## Scenario Context

Cadre Corp integrates AI/ML into three products:

1. **RevAI:** LLM-assisted malware analysis — decompiled code → LLM → verdict + YARA rules.
2. **Praxis:** AI-native security scanner — source code → LLM → vulnerability findings.
3. **DarkAI (research):** Prompt injection testing against LLM-integrated security tools.

These AI components introduce SDLC risks that traditional application security doesn't address:

- The **LLM model itself** is a dependency — what if it's poisoned or backdoored?
- **Training data provenance** — was the fine-tuning dataset tampered with?
- **Prompt injection** — the #1 OWASP LLM risk — can attacker-crafted input override system instructions.
- **Output validation** — an LLM that generates YARA rules could generate malicious rules if prompt-injected.

---

## Multiple-Choice Questions

**Question 1:** Model supply chain security in MLSecOps refers to:

A. The physical supply chain for GPU hardware  
B. Verifying the integrity and provenance of AI models — ensuring the model weights haven't been tampered with, the model card documents training data sources and known limitations, and the model was obtained from a trusted source with verified hashes  
C. Managing the electricity supply for model training  
D. Supply chain attacks that only affect traditional software

**Question 2:** Prompt injection (OWASP LLM #1) is an SDLC concern because:

A. It only affects chatbot applications  
B. If attacker-crafted input can override the LLM's system instructions, any downstream action the LLM takes (generating code, writing YARA rules, classifying malware) can be subverted — this must be addressed in the application's design, not just at runtime  
C. LLM APIs automatically prevent prompt injection  
D. Prompt injection only works on open-source models

**Question 3:** What SDLC control is appropriate for RevAI's LLM-generated YARA rules?

A. Trust the LLM — it's trained on vast data and makes fewer errors than humans  
B. Human-in-the-loop validation with cryptographic approval — every AI-generated YARA rule, malware verdict, or code suggestion is DRAFT until a human examiner reviews and approves it, with an audit trail proving the approval  
C. Run the LLM output through a second LLM for verification — two AIs can't both be wrong  
D. Publish AI-generated rules immediately with an "AI-generated" disclaimer

---

## Answer Explanations

**Answer 1: B**  
**Model supply chain security** ensures the AI model itself is trustworthy. Key practices: (a) verify model hash against the publisher's published hash, (b) review the model card (documentation of training data, intended use, known biases/limitations), (c) obtain models from trusted sources (official repositories, not random Hugging Face uploads), (d) scan model files for embedded malware (pickle-based models can execute arbitrary code on deserialization). A poisoned model is a supply chain attack, same as a poisoned npm package.

**Answer 2: B**  
**Prompt injection subverts the LLM's behavior**, and if the LLM's output drives downstream actions (YARA rule generation, malware classification, code analysis), those actions can be attacker-controlled. The SDLC must address this at design time: (a) strict separation of system instructions from user data, (b) output validation/sandboxing before any LLM output takes effect, (c) never directly execute LLM output without human or automated validation.

**Answer 3: B**  
**Human-in-the-loop (HITL) with cryptographic approval** is the correct control for safety-critical AI outputs. An AI-generated YARA rule that's wrong can cause false positives (blocking legitimate software) or false negatives (missing malware). A prompt-injected AI could generate a YARA rule that specifically excludes the attacker's malware. HITL (as implemented in DFIR-Nexus's DRAFT → approve flow) ensures human accountability for every operational AI output.

---

## Cadre Corp Application

1. **AI/ML BOM:** Extend the SBOM concept: an AI Bill of Materials listing: model name and version, model hash, training data provenance, known limitations, and intended use. This enables rapid response if a model vulnerability is disclosed.

2. **Prompt Injection Testing in SDLC:** Every prompt-template used in RevAI, Praxis, or DarkAI should be tested against prompt injection payloads before deployment. This is a new category of security test — not SAST, not DAST, but "prompt AST."

3. **HITL Gate for All AI Outputs:** Operationalize the existing DFIR-Nexus HITL workflow: every AI-generated finding → DRAFT → human review → cryptographic approval → operational. No exception for "low-risk" outputs — the risk classification should itself be human-validated.

---

## Interview Talking Points

1. **AI Is Software — With New Attack Surface:** "An AI model is a dependency like any other — except it can be poisoned, prompt-injected, or adversarially manipulated in ways a traditional library can't. We need MLSecOps: SCA for models, prompt injection testing in CI, and HITL for AI outputs."

2. **Never Trust the LLM's Output Without Verification:** "An LLM that generates YARA rules is a tool, not an authority. Every rule it writes goes through human review. The day we skip that review is the day an attacker's prompt injection generates a rule that whitelists their malware."
