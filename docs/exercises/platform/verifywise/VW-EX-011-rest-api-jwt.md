# VW-EX-011 — REST API authentication and JWT management

**Platform:** VerifyWise | **Time:** 15 min | **CISSP:** 5, 8

---

## Objective

Authenticate to VerifyWise's REST API, manage JWT tokens, and test CRUD operations on AI projects. Demonstrate API-driven AI governance — essential for integrating AI scanning tools with the governance platform.

---

## Steps

### Step 1 — Obtain a JWT token
```powershell
$body = @{
    email = "org-admin@cadre.local"
    password = "<your-org-admin-password>"  # set in docker/verifywise.env (SUPERADMIN_PASSWORD) or via -OrgAdminPassword
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:13000/auth/login" `
    -Method Post -Body $body -ContentType "application/json"
$TOKEN = $response.access_token
```

### Step 2 — List AI projects via API
```powershell
$headers = @{ "Authorization" = "Bearer $TOKEN" }
Invoke-RestMethod -Uri "http://127.0.0.1:13000/projects" -Headers $headers
```
Confirm the three Cadre Corp projects (DarkAI, RevAI, Praxis) are returned.

### Step 3 — Create an AI risk via API
POST a new risk assessment to the RevAI project. Verify it appears in the UI.

### Step 4 — JWT lifecycle management
JWTs expire. Implement token refresh logic. Document: token storage (never in git), rotation (on expiry), and least privilege (separate tokens for read vs write operations).

---

## Interview Talking Points

1. **"Both GRC platforms are API-driven":** "CISO Assistant uses PATs. VerifyWise uses JWTs. I can work with both — understanding token lifecycle, secure storage, and least privilege. The automation that feeds findings into governance depends on API competence."