# R-EX-036 — Incident classification: DarkAI prompt injection

**CISSP Reference:** Chapter 17, Sections "Incident Management", "Detection and Preventive Measures", Pages 1230–1260  
**Exam Objective:** 7.3.1 Manage incident response; 7.3.2 Classify and prioritize incidents  
**Study Guide Key Terms:** Incident classification, severity levels, incident prioritization, impact assessment, notification triggers, GDPR breach notification, escalation criteria  
**Inputs:** `samples/findings/darkai-prompt-inject.json`, RISK-012, RISK-013, [`../enterprise-context.md`](../enterprise-context.md)

---

## Scenario Context

At 09:15 UTC, a DarkAI researcher reported unusual LLM output: the chatbot, configured to simulate a security analyst, began returning messages containing what appeared to be lab API keys and internal IP addresses. Investigation revealed:

1. A prompt injection attack successfully extracted environment variables from the DarkAI container, including: `DARKAI_API_KEY`, `NEXUS_AUDIT_SECRET` (a DFIR-Nexus HMAC secret used for audit chain signing), and internal IPs of the DarkAI Docker network (`172.20.0.0/24`).
2. The extracted `NEXUS_AUDIT_SECRET` could allow an attacker to forge valid DFIR-Nexus audit entries — making forged findings appear cryptographically legitimate.
3. DarkAI is isolated on `172.20.0.0/24` with no direct route to the lab production network (`192.168.77.0/24`) or client evidence (AST-030). However, the Nexus audit secret is shared between environments.
4. The researcher who discovered the incident waited 4 hours before reporting it — "I wanted to reproduce it first to make sure it was real."

The SOC Lead must classify this incident, determine notification requirements, and decide whether GDPR's 72-hour notification clock has started.

---

## Multiple-Choice Questions

**Question 1:** What is the appropriate severity classification for this incident?

A. Low — it's just a research lab, not production  
B. High — a prompt injection extracted SHARED secrets (Nexus audit secret) that are also used in the production DFIR workflow; the lab isolation prevented direct production access, but a shared credential bridge was compromised  
C. Critical — all incidents involving AI are automatically critical  
D. Informational — no client data was involved

**Question 2:** The extracted `NEXUS_AUDIT_SECRET` is concerning because:

A. It's just a lab secret with no production value  
B. The secret is shared between DarkAI and DFIR-Nexus production — if the attacker obtained it, they could forge cryptographically valid audit entries in the production Nexus instance, undermining the integrity of the entire forensic audit chain  
C. Audit secrets are automatically rotated daily  
D. HMAC secrets can't be used maliciously

**Question 3:** Does this incident trigger GDPR's 72-hour notification clock?

A. Yes — any security incident triggers the clock  
B. No — the incident did not involve personal data of EU data subjects; prompt injection extracted infrastructure secrets, not PII; the GDPR clock starts when personal data breach is confirmed, not for all security incidents  
C. Yes — because DarkAI researchers might be EU citizens  
D. No — research labs are exempt from GDPR

**Question 4:** The researcher's 4-hour delay in reporting the incident is problematic because:

A. It's not problematic — reproducing the issue was the right priority  
B. Incident response timeliness starts at detection — the researcher detected anomalous behavior at 09:15 but the SOC wasn't notified until 13:15; those 4 hours are lost containment time; incident response policy should require immediate notification upon suspicion, not after self-directed investigation  
C. GDPR requires reporting within 4 hours  
D. Researchers are not required to report incidents

---

## Answer Explanations

**Answer 1: B**  
**High severity** — not because of the lab environment, but because of the **shared credential bridge**. The `NEXUS_AUDIT_SECRET` extracted from DarkAI is the same secret used in production DFIR-Nexus. Lab isolation prevented direct network access to production, but a shared secret is a credential bridge that bypasses network isolation. Until the secret is rotated, production audit integrity is compromised. Lab incidents can escalate to production impact when credentials are shared. Critical (C) is excessive because client data wasn't directly accessed. Low (A) underestimates the shared-secret risk.

**Answer 2: B**  
A **shared secret between environments** means lab compromise = production compromise for that secret. The Nexus audit secret is used for HMAC chain signing — every audit entry in production is validated with this key. An attacker with the secret can forge audit entries that pass cryptographic verification, undermining the non-repudiation of every finding in the system. This is why secrets should NEVER be shared between environments — lab secrets stay in lab, production secrets stay in production.

**Answer 3: B**  
GDPR notification is triggered by **personal data breach**, not all security incidents. The extracted data (API keys, internal IPs, audit secrets) are infrastructure credentials — not personal data of identified or identifiable natural persons. If the prompt injection had extracted employee PII, client data, or user credentials, the clock would start. The key distinction: security incident ≠ personal data breach. GDPR Article 4(12) defines "personal data breach" specifically.

**Answer 4: B**  
**IR policy requires immediate notification**, not self-directed investigation. The researcher's intent (reproducing the issue) was good, but the effect (4 hours of unreported active compromise) was harmful. During those 4 hours: (a) the attacker could have extracted additional secrets, (b) the Nexus audit secret remained valid and potentially abused, (c) containment was delayed. IR policy should state: "Notify SOC immediately upon suspicion. Do NOT attempt to reproduce, investigate, or contain without SOC coordination."

---

## Cadre Corp Application

1. **Incident Classification Matrix:** Define a clear severity matrix: Critical (client data at risk, active breach of Restricted assets, GDPR notification triggered), High (infrastructure compromise, shared secrets exposed, potential escalation path to Restricted), Medium (isolated lab incident, no cross-environment impact), Low (policy violation, unsuccessful attack attempt). Map to notification requirements and response SLAs.

2. **Shared Secret Remediation:** Immediately rotate `NEXUS_AUDIT_SECRET` in production. Audit all shared secrets between lab and production — eliminate sharing. Each environment gets its own secrets, generated independently. Lab secrets that leak should never impact production.

3. **IR Reporting Policy:** Update incident response policy: "Upon reasonable suspicion of a security incident, notify SOC immediately via [channel]. Do not attempt independent investigation, reproduction, or containment. The SOC coordinates the response. Delayed notification extends the attacker's free operation time."

---

## Interview Talking Points

1. **Lab Incidents Escalate Through Shared Secrets:** "A prompt injection in an isolated research lab shouldn't be able to compromise production audit integrity. But it did — because we used the same audit secret everywhere. Lab isolation means nothing if credentials are shared. Environment-specific secrets, always."

2. **Security Incident ≠ GDPR Breach:** "Not every incident triggers the 72-hour clock. GDPR notification requires personal data breach — PII of living individuals. Infrastructure secret extraction is a security incident, not a personal data breach. Knowing the difference prevents over-notification (which desensitizes regulators) and under-notification (which gets you fined)."

3. **Report First, Investigate Second:** "The researcher who spent 4 hours reproducing the bug instead of reporting it — their intentions were good but their actions extended the incident. IR policy must be crystal clear: notify SOC immediately upon suspicion. The SOC decides whether to reproduce, contain, or escalate."
