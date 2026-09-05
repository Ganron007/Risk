# CISO-EX-009 — REST API authentication and PAT management

**Platform:** CISO Assistant Community Edition  
**Time:** 20 minutes  
**CISSP Domains:** 5 (Identity & Access Management), 8 (Software Development Security)

---

## Objective

Authenticate to the CISO Assistant REST API using Personal Access Tokens, test CRUD operations on risk scenarios, and implement secure token management practices. This demonstrates API-driven GRC automation — essential for integrating security tools with the risk platform.

---

## Steps

### Step 1 — Verify PAT authentication
```powershell
$TOKEN = "<your-pat-from-CISO-EX-001>"
$headers = @{
    "Authorization" = "Token $TOKEN"
    "Content-Type" = "application/json"
}
# Test authentication
Invoke-RestMethod -Uri "http://localhost:8080/api/risk-scenarios/" -Headers $headers
```
Confirm the response includes the 18 risks seeded in CISO-EX-002.

### Step 2 — Create a risk via API
```powershell
$body = @{
    name = "RISK-019 — API-created test risk"
    description = "Created via REST API to demonstrate automated risk ingestion"
    domain = "<domain-id>"  # Get from /api/domains/
    likelihood = 2
    impact = 3
    treatment = "Mitigate"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/risk-scenarios/" `
    -Method Post -Headers $headers -Body $body
```

### Step 3 — Update a risk via API (PATCH)
Update RISK-019's treatment status:
```powershell
$update = @{ treatment_status = "In Progress" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/api/risk-scenarios/<risk-id>/" `
    -Method Patch -Headers $headers -Body $update
```

### Step 4 — Secure token management
- **Never commit tokens to git.** Store in environment variables or a secrets manager.
- **Rotate tokens quarterly.** Create new PAT, update scripts, revoke old PAT.
- **Use least-privilege tokens.** Create separate PATs for read-only dashboards vs read-write ingestion.
- **Audit token usage.** Review API access logs monthly for anomalous patterns.

---

## Verification Checklist

- [ ] GET `/api/risk-scenarios/` returns 18-19 risks
- [ ] POST creates a new risk, visible in UI
- [ ] PATCH updates treatment status
- [ ] Token rotation procedure documented

---

## CISSP Connection

**Domain 5:** PAT management — creation, storage, rotation, revocation — is an IAM lifecycle function applied to API credentials. Same principles as user account management.

**Domain 8:** API-driven GRC integration is a DevSecOps pattern — security tools (Praxis, DFIR-Nexus) pushing findings into the risk platform via API. This is infrastructure-as-code for governance.

---

## Interview Talking Points

1. **"I automate risk ingestion, not manual data entry":** "When Praxis finds a hardcoded secret or DFIR-Nexus flags a DCSync attempt, those findings flow into CISO Assistant via REST API — not via someone retyping them. Automation eliminates the 'we forgot to update the risk register' gap."

2. **"API credentials get the same rigor as user credentials":** "PATs are rotated quarterly, scoped to least privilege, and never committed to git. The same IAM discipline I apply to user accounts applies to API tokens."