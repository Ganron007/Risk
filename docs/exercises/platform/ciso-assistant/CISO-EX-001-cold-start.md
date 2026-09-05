# CISO-EX-001 — Cold start and initial configuration

**Platform:** CISO Assistant Community Edition  
**Time:** 20 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 2 (Asset Security)  
**Prerequisites:** Docker Desktop running, `ciso-up.ps1` executed

---

## Objective

Bring up CISO Assistant from cold state, create the admin account, define the Cadre Corp domain, and verify the platform is ready for risk management workflows. This demonstrates the ability to bootstrap a GRC platform — a common interview scenario for Business Risk Leadership roles.

---

## Scenario

You've joined Cadre Corp as Risk Manager. The CISO has selected CISO Assistant Community Edition as the GRC platform for the ISO 27001 certification program. Your first task: get the platform running, create the organizational domain, and confirm it's operational.

The platform runs in Docker and is started via `.\scripts\ciso-up.ps1`. The compose file serves HTTP on `:8080` (lab mode — no TLS) with a SQLite backend under `docker/vendor/ciso-assistant/db/`.

---

## Steps

### Step 1 — Bring up the stack
```powershell
cd <repo-root>   # folder containing scripts/ and docker/
.\scripts\ciso-up.ps1
```
Wait for the backend and frontend containers to report healthy. Verify with `docker ps` — you should see `ciso-backend` and `ciso-frontend` running.

### Step 2 — Create superuser (first time only)
```powershell
docker compose -p cadre-risk-ciso `
  -f docker\vendor\ciso-assistant\docker-compose.yml `
  -f docker\ciso-compose.yml `
  exec backend uv run python manage.py createsuperuser
```
Use `admin@cadre.local` as email. Store the password in your password manager — never commit it.

### Step 3 — Log in and create the Cadre Corp domain
1. Open `http://localhost:8080` in your browser.
2. Log in with the superuser credentials from Step 2.
3. Navigate to **Domains** → **Create Domain**.
4. Name: `Cadre Corp`. Description: `Primary GRC domain for Cadre Corp DFIR services — ISO 27001, SOC 2, NIST CSF.`
5. Save.

### Step 4 — Load the ISO 27005 risk matrix library
1. Navigate to **Libraries** → **Load Library**.
2. Select **5x5 ISO-27005 Risk Matrix**.
3. Confirm the library is loaded — you should see risk levels: Low, Medium, High, Critical mapped to a 5x5 likelihood × impact grid.

### Step 5 — Create a Personal Access Token (PAT)
1. Navigate to **Settings** → **Personal Access Tokens**.
2. Create a new token with description: `cadre-risk-lab`.
3. Copy the token immediately — it won't be shown again.
4. Store the token for API automation (CISO-EX-009, CISO-EX-010).

### Step 6 — Verify readiness
```powershell
# Test API reachability with your PAT
$TOKEN = "<your-pat>"
$headers = @{ "Authorization" = "Token $TOKEN" }
Invoke-RestMethod -Uri "http://localhost:8080/api/domains/" -Headers $headers
```
You should see the `Cadre Corp` domain in the JSON response.

---

## Verification Checklist

- [ ] CISO Assistant UI loads at `http://localhost:8080`
- [ ] Admin account created and login successful
- [ ] `Cadre Corp` domain exists
- [ ] 5x5 ISO-27005 risk matrix library loaded
- [ ] Personal Access Token generated and tested via REST API
- [ ] API returns domain list including Cadre Corp

---

## CISSP Connection

**Domain 1 (Security & Risk Management):** This exercise demonstrates the practical implementation of a risk management framework — the "how" behind the governance theory. The ISO 27005 risk matrix is a direct implementation of the qualitative risk analysis concepts tested in CISSP.

**Domain 2 (Asset Security):** The Cadre Corp domain is the organizational boundary for asset grouping, classification, and risk assignment — mapping directly to the asset inventory (`config/asset-inventory.csv`) and classification scheme.

---

## Interview Talking Points

1. **"I can bootstrap a GRC program":** "When I joined Cadre Corp, there was no GRC platform. I evaluated options, selected CISO Assistant Community Edition as a pragmatic starting point, and had it running with a risk matrix, domain structure, and API integration within the first week. Here's the screenshot and the API response proving it."

2. **"I understand the tooling, not just the theory":** "CISSP teaches you risk management frameworks. I can actually deploy and configure the tools that operationalize those frameworks. The 5x5 ISO-27005 matrix isn't just a diagram — I loaded it, configured it, and seeded it with Cadre Corp's actual risks."

3. **"API-first from day one":** "I configured a Personal Access Token during initial setup. That PAT enables automated risk ingestion from our security tools — Praxis SARIF findings, DarkAI audit logs — flowing directly into the risk register without manual data entry."

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `:8080` connection refused | Docker containers not running | `docker ps` — if empty, re-run `ciso-up.ps1` |
| Can't create superuser | Backend container not ready | Wait 30s after `ciso-up.ps1`, check `docker logs ciso-backend` |
| API returns 401 | PAT not sent correctly | Verify header is `Authorization: Token <pat>` (NOT `Bearer`) |
| Library not found | Libraries not fetched | Check `docker/ciso-compose.yml` library volume mount |
