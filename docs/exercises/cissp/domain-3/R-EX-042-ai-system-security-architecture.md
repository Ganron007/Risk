# R-EX-042 — AI system security architecture

**CISSP Reference:** Chapter 8, Section "Security Capabilities of Information Systems"; Chapter 9, Section "Security Architecture Vulnerabilities"; Domain 8 SDLC  
**Exam Objective:** 3.3.1 Apply secure design principles; 3.6.1 Understand emerging technology security  
**Study Guide Key Terms:** AI security architecture, ML pipeline security, model integrity, prompt injection, RAG poisoning, AI supply chain, OWASP LLM Top 10, MITRE ATLAS  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md)

---

## Scenario Context

Cadre Corp operates two AI-integrated systems that raise novel architecture questions:

1. **DarkAI (AST-035):** A research lab running LLM-based prompt injection testing against security tools. It processes synthetic attack prompts in an isolated Docker network (`172.20.0.0/24`). RISK-012 (lab breakout) and RISK-013 (prompt injection leak secrets) are documented, but the CISO wonders: what NEW security architecture principles apply to AI systems that don't apply to traditional applications?

2. **RevAI (sister project):** An LLM-assisted malware reverse engineering pipeline. It submits decompiled code to an LLM for analysis and interpretation. The LLM's output (verdict, YARA rules, function summaries) flows into DFIR-Nexus findings. RISK-018 (AI-generated finding accepted without HITL) already captures the human-in-the-loop gap, but the architecture team is asking about model integrity, training data poisoning, and supply chain risks for the LLM itself.

3. **Praxis (sister project):** An AI-native security CLI that uses LLM agents to scan codebases for vulnerabilities. It sends source code snippets to LLM providers (Anthropic, OpenAI) for analysis. The privacy concern: is sending client source code to a third-party LLM API a data spill?

---

## Multiple-Choice Questions

**Question 1:** Which of the following is a security architecture concern UNIQUE to AI/ML systems (not applicable to traditional applications)?

A. Authentication and access control for system users  
B. Model poisoning — adversarial manipulation of training data that causes the model to produce attacker-chosen outputs at inference time  
C. Encryption of data at rest in databases  
D. Logging and monitoring of system access

**Question 2:** Praxis sends client source code to third-party LLM APIs (Anthropic, OpenAI) for vulnerability analysis. From a security architecture perspective, this creates what risk?

A. No risk — LLM APIs are encrypted in transit via TLS  
B. Data egress risk — proprietary source code leaves Cadre Corp's control and is processed on third-party infrastructure, potentially used for model training or retained in logs  
C. The LLM might produce incorrect vulnerability findings  
D. API rate limiting could delay scan results

**Question 3:** The OWASP Top 10 for LLM Applications identifies "prompt injection" as the #1 risk. Which architecture control is MOST effective against prompt injection in DarkAI's research environment?

A. Network firewall between DarkAI containers and the lab network  
B. Strict input sanitization AND context isolation — untrusted input is treated as data, never as instructions; LLM output is never directly executed without sandbox validation  
C. Stronger authentication for DarkAI lab access  
D. Encrypting all prompts before sending them to the LLM

**Question 4:** In RevAI's malware analysis pipeline, the LLM generates YARA rules and function summaries. What architectural safeguard ensures these outputs don't cause harm if they're incorrect?

A. Faster GPUs for LLM inference to reduce error rates  
B. Human-in-the-loop (HITL) approval gate — all LLM-generated findings are DRAFT until a human examiner cryptographically approves them  
C. Running the LLM output through a second LLM for validation  
D. Publishing all LLM outputs directly to clients with an AI-generated disclaimer

---

## Answer Explanations

**Answer 1: B**  
**Model poisoning** is unique to AI/ML systems. An attacker who can influence training data (via public dataset contamination, federated learning injection, or fine-tuning data manipulation) can implant backdoors that activate at inference time. Traditional applications don't have "training data" to poison. Authentication (A), encryption (C), and logging (D) are standard security controls applicable to all systems.

**Answer 2: B**  
The risk is **data egress** — proprietary client source code leaves Cadre Corp's infrastructure and is processed on a third party's servers. While major LLM providers have data processing agreements, the architectural concern is: (a) can the provider use this data for model training? (b) is the data retained in provider logs? (c) does this violate client confidentiality agreements or data residency requirements? Incorrect findings (C) is a separate accuracy concern. TLS (A) protects data in transit but not at the destination.

**Answer 3: B**  
**Input sanitization and context isolation** are the most effective architectural controls against prompt injection. The core defense is: (a) treat all user/external input as untrusted data, separated from system instructions by architectural boundaries (not just prompt text), (b) never directly execute LLM output — always validate through a sandbox or approval gate. Firewalls (A), authentication (C), and encryption (D) don't address the prompt injection attack vector, which exploits the LLM's inability to distinguish instructions from data.

**Answer 4: B**  
**Human-in-the-loop (HITL) approval** is the correct architectural safeguard. An LLM-generated YARA rule that's wrong could cause false positives (blocking legitimate software), false negatives (missing real malware), or even malicious rules if the LLM was prompt-injected. HITL ensures a human examiner reviews and cryptographically approves findings before they become operational. Running through a second LLM (C) adds latency but doesn't guarantee correctness — both LLMs could make the same mistake. Unreviewed publishing (D) is irresponsible.

---

## Cadre Corp Application

1. **DarkAI Isolation Verification:** The existing `CTL-LAB-ISOLATION` control and Docker network isolation (`172.20.0.0/24`) must be verified to prevent bridge misconfigurations (see R-EX-032). DarkAI's prompt injection research is valuable, but only if the lab stays isolated from production.

2. **RevAI HITL Gate:** RISK-018 documents this need. DFIR-Nexus's DRAFT → approve flow (`nexus approve --interactive` with PBKDF2-HMAC-SHA256) is the reference implementation. Every AI-generated malware verdict, YARA rule, or function summary must pass through this gate before becoming operational.

3. **Praxis Data Egress Assessment:** Before using Praxis with client code, conduct a data egress impact assessment: (a) does the client's DPA allow third-party LLM processing? (b) are the LLM providers' data processing terms acceptable? (c) can sensitive code be pre-processed to remove identifiers before sending? If any answer is "no," run Praxis with local-only LLM backends (Ollama).

4. **AI Architecture Principles to Add to Control Register:** Create `CTL-AI-ARCH` covering: model integrity verification, training data provenance, prompt injection defenses, output validation/HITL, data egress controls for third-party LLM APIs, and model supply chain security.

---

## Interview Talking Points

1. **AI Has New Attack Surface:** "Traditional apps have bugs. AI systems have bugs PLUS model poisoning, prompt injection, training data extraction, and adversarial examples. If you secure an AI system like a web app, you're missing 80% of the threat model."

2. **Third-Party LLM = Third-Party Risk:** "Sending client source code to OpenAI's API is a third-party data transfer. Would you upload client evidence to a random server because 'it uses TLS'? Same logic applies here. The architectural decision is: local model vs. API vs. pre-processing to strip sensitive data."

3. **HITL Is Non-Negotiable for AI Outputs:** "An AI that generates security findings without human review is not a tool — it's a liability. Our DFIR-Nexus DRAFT → approve flow ensures every AI-generated verdict has a human name and cryptographic signature attached before it touches a client report."

4. **OWASP LLM Top 10 Is the New OWASP Top 10:** "Just like every web developer needs to know SQL injection and XSS, every security architect in 2026 needs to know prompt injection, RAG poisoning, and model supply chain attacks. This isn't niche — it's table stakes for security leadership."
