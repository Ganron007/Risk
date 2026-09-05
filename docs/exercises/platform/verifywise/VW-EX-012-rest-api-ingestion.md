# VW-EX-012 — REST API project and risk ingestion

**Platform:** VerifyWise | **Time:** 15 min | **CISSP:** 6, 8

---

## Objective

Build an automated pipeline that pushes AI system metadata and risk assessments into VerifyWise via REST API. Connect DarkAI audit logs and Praxis SARIF AI-related findings to the AI governance platform.

---

## Steps

### Step 1 — Ingest a DarkAI audit finding
When DarkAI prompt injection testing detects a new vulnerability pattern, push it to VerifyWise:
```powershell
$body = @{
    projectId = "<revai-or-darkai-id>"
    title = "New prompt injection vector discovered in DarkAI testing"
    severity = "Medium"
    category = "AI Security - Prompt Injection"
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:13000/risks" `
    -Method Post -Headers $headers -Body $body
```

### Step 2 — Ingest Praxis AI-related findings
When Praxis detects insecure AI model usage patterns (e.g., hardcoded API keys for LLM providers), push the finding to VerifyWise with the project association.

### Step 3 — Schedule daily sync
Integrate with the same scheduled task from CISO-EX-010 — one daily job that pushes findings to both platforms: classic risks → CISO Assistant, AI risks → VerifyWise.

---

## Interview Talking Points

1. **"AI findings flow to the AI governance platform":** "When DarkAI discovers a new prompt injection vector or Praxis finds an LLM API key in code, those findings go to VerifyWise — not a spreadsheet, not an email. The AI governance platform is fed by the AI security tools, automatically."