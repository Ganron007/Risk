# CISO-EX-010 — REST API risk ingestion automation

**Platform:** CISO Assistant Community Edition  
**Time:** 25 minutes  
**CISSP Domains:** 6 (Assessment & Testing), 8 (Software Development Security)

---

## Objective

Build an automated pipeline that ingests security findings into CISO Assistant via REST API. Connect Praxis SARIF output and campaign findings to the risk platform — demonstrating the bridge between security operations and governance.

---

## Steps

### Step 1 — Understand the ingestion flow
```
Security Tool → Finding → adapters.py → Unified Finding Schema → CISO API → Risk Scenario
```
The `src/adapters.py` module converts tool-specific formats (SARIF, JSON) to the unified finding schema. `src/ingest.py` pushes findings to CISO Assistant.

### Step 2 — Ingest a Praxis SARIF finding
```powershell
python -m src.ingest `
  --source praxis `
  --input samples/findings/praxis-sarif-sample.sarif `
  --ciso-url http://localhost:8080 `
  --ciso-token "<your-pat>"
```
Verify: the hardcoded secret finding should appear as a new risk scenario in CISO Assistant.

### Step 3 — Ingest a campaign DCSync finding
```powershell
python -m src.ingest `
  --source elastic `
  --input samples/findings/elastic-dcsync-alert.json `
  --ciso-url http://localhost:8080 `
  --ciso-token "<your-pat>"
```
Verify: RISK-001 should be updated with new evidence (detection timestamp, alert details).

### Step 4 — Schedule automated ingestion
Create a scheduled task (Windows) or cron job (Linux) that runs `src/ingest.py` daily, scanning `samples/findings/` for new files and pushing them to CISO Assistant. This ensures the risk register stays current without manual intervention.

### Step 5 — Handle deduplication
If the same finding is ingested twice (e.g., the campaign DCSync alert fires every day), the ingestion script should UPDATE the existing risk (new evidence, updated timestamp) rather than create a duplicate. Verify this logic in `src/dedupe.py`.

---

## Verification Checklist

- [ ] Praxis SARIF finding ingested and visible in CISO Assistant
- [ ] Campaign finding updates existing risk (no duplicate)
- [ ] Scheduled ingestion configured and tested
- [ ] Deduplication logic verified

---

## CISSP Connection

**Domain 6:** Automated security assessment data flow — findings from security testing tools flow into the risk management platform without manual transcription. This closes the assessment-to-governance loop.

**Domain 8:** This is DevSecOps for GRC — security findings as code, pushed through an API pipeline, with deduplication and update logic. Same patterns as CI/CD, applied to governance.

---

## Interview Talking Points

1. **"My risk register updates itself":** "When our SOC detects a DCSync attempt or Praxis finds a hardcoded secret, those findings flow into CISO Assistant automatically. The risk register isn't a quarterly spreadsheet exercise — it's a living system fed by our security operations."

2. **"Deduplication means the register stays clean":** "If the same DCSync detection fires every day, the ingestion pipeline updates the existing risk with new timestamps and evidence — it doesn't create 30 duplicate risks. Deduplication logic keeps the register actionable, not cluttered."