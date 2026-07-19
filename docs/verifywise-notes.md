# VerifyWise — practice lab & REST ingest

> **AI governance sink** for CADRE-Risk (DarkAI / RevAI / Praxis / LLM risk).  
> Upstream: [verifywise-ai/verifywise](https://github.com/verifywise-ai/verifywise) · user guide: https://verifywise.ai/user-guide/  
> Screenshot: [`img/verifywise-ai-risk.png`](img/verifywise-ai-risk.png)

**Rule:** Markdown (`docs/risk-register-baseline.md`) is SSoT. VerifyWise is a **sink** for Cadre Corp **AI systems** — not the system of record.

---

## Role vs other sinks

| Sink | Focus | Practice doc |
|------|--------|----------------|
| **CISO Assistant** | Classic GRC (ISO 27001, SOC 2, NIST CSF) | [`ciso-notes.md`](ciso-notes.md) |
| **VerifyWise** | **AI governance** — EU AI Act, ISO 42001, NIST AI RMF, model inventory, LLM risks | this file |

CISSP angles: Domains **1** (governance), **3** (security architecture — AI systems), **8** (software development — Praxis CI).

---

## Lab URLs / accounts

| Surface | URL |
|---------|-----|
| UI | **http://127.0.0.1:18080** |
| API (direct) | `http://127.0.0.1:13000` |
| API via UI proxy | `http://127.0.0.1:18080/api/...` (same paths) |
| Health | `http://127.0.0.1:13000/health` |

| Account | Email | Password | Role |
|---------|-------|----------|------|
| Superadmin | `admin@cadre.local` | from `docker/verifywise.env` → `SUPERADMIN_*` | Create orgs only |
| **Org admin (use this)** | `org-admin@cadre.local` | `***REMOVED***` (lab default from seed) | Cadre Corp data |

Never commit `docker/verifywise.env` (gitignored).

---

## Cold-start practice (full loop)

Do this from a clean machine or after `verifywise-down.ps1 -RemoveVolumes` to rebuild muscle memory.

### 1. Env file (once)

```powershell
cd C:\STUDY\Github\CADRE-Platform\CADRE-Risk
copy docker\verifywise.env.example docker\verifywise.env
notepad docker\verifywise.env
# Set at least: JWT_SECRET, SUPERADMIN_EMAIL, SUPERADMIN_PASSWORD,
# DB_PASSWORD, ENCRYPTION_KEY, AI_GATEWAY_INTERNAL_KEY
```

Lab defaults we used: `SUPERADMIN_EMAIL=admin@cadre.local`, password aligned with CISO lab (`***REMOVED***`).

### 2. Bring stack up

```powershell
.\scripts\verifywise-up.ps1
```

What this does:

1. Clones/updates `docker/vendor/verifywise` (gitignored) from upstream `develop`
2. Copies `docker/verifywise.env` → vendor `.env.prod`
3. `docker compose -p cadre-risk-verifywise` with:
   - `docker-compose.yml` + `docker-compose.prod.yml` + **`docker/verifywise-compose.yml`**
4. Pulls images, starts: postgres, redis, backend, frontend, worker, eval, ai_gateway

Containers: `cadre-risk-vw-*`  
Wait until `http://127.0.0.1:13000/health` returns `"status":"ok"`.

### 3. Seed Cadre Corp via REST

```powershell
.\scripts\verifywise-seed-baseline.ps1
# Optional overrides:
# .\scripts\verifywise-seed-baseline.ps1 -Email admin@cadre.local -Password '...'
```

Creates: org **Cadre Corp**, org-admin user, 3 use cases, 3 models, 4 AI risks.

### 4. UI walkthrough (screenshot path)

1. Open **http://127.0.0.1:18080**
2. Login **`org-admin@cadre.local`** / lab password
3. **Inventory → Use cases** — DarkAI, RevAI, Praxis (EU AI Act)
4. **Inventory → Model inventory** — DarkAI-Chatbot, RevAI-Pipeline, Praxis-Scanner
5. **Assurance → Risk management** — RISK-012 / 013 / 014 / 018  
   - Open a risk → edit modal shows likelihood/severity → inherent **HIGH RISK** (e.g. RISK-013 Likely × Major)
6. Screenshot → `docs/img/verifywise-ai-risk.png`

### 5. Tear down

```powershell
.\scripts\verifywise-down.ps1              # stop, keep volumes
.\scripts\verifywise-down.ps1 -RemoveVolumes   # wipe DB (full reset)
```

---

## What was seeded (demo data map)

Source: [`risk-register-baseline.md`](risk-register-baseline.md) AI-related rows.

| Use case (project) | EU AI Act class | Role | Model | Risks |
|--------------------|-----------------|------|-------|-------|
| DarkAI lab chatbot | High risk | Deployer | DarkAI-Chatbot | RISK-012, RISK-013 |
| RevAI malware analysis pipeline | High risk | Provider | RevAI-Pipeline | RISK-014, RISK-018 |
| Praxis CI security scanner | Limited risk | Provider | Praxis-Scanner | RISK-018 |

| Risk ID | Theme |
|---------|--------|
| RISK-012 | DarkAI lab breakout / mix with client evidence |
| RISK-013 | Prompt-injection / LLM abuse leaks secrets |
| RISK-014 | Malware sample mishandling on RevAI path |
| RISK-018 | AI forensic finding accepted without HITL |

---

## REST API — practice reference

Auth header style differs from CISO:

| Product | Auth header |
|---------|-------------|
| VerifyWise | `Authorization: Bearer <jwt>` |
| CISO Assistant | `Authorization: Token <pat>` |

### Login

```http
POST /api/users/login
Content-Type: application/json

{"email":"org-admin@cadre.local","password":"<lab-password>"}
```

Envelope: `{ "message": "Accepted", "data": { "token": "<jwt>", ... } }`

### Object graph

```text
Organization (Cadre Corp)
  └── Project / use case   framework [1] = EU AI Act
        ├── Model inventory
        └── ProjectRisk[]    path: /api/projectRisks  (camelCase!)
```

### Endpoints (seed script order)

| Step | Method | Path | Purpose |
|------|--------|------|---------|
| 1 | `POST` | `/api/users/login` | Superadmin JWT |
| 2 | `POST` | `/api/organizations` | Create Cadre Corp + org admin (needs logo URL, not empty string) |
| 3 | `POST` | `/api/users/login` | Org-admin JWT on re-run |
| 4 | `GET`/`POST` | `/api/projects` | List / create use cases |
| 5 | `POST` | `/api/modelInventory` | Register models |
| 6 | `GET`/`POST` | `/api/projectRisks` | List / create risks |

### Project body (AI use case)

```json
{
  "project_title": "DarkAI lab chatbot",
  "owner": 2,
  "start_date": "2026-07-13",
  "geography": 1,
  "target_industry": "Security research / AI lab",
  "description": "...",
  "ai_risk_classification": "High risk",
  "type_of_high_risk_role": "Deployer",
  "goal": "...",
  "members": [2],
  "framework": [1],
  "enable_ai_data_insertion": false,
  "is_organizational": false
}
```

Framework rule: non-organizational (AI) projects → **only** framework `1` (EU AI Act). Org-level ISO projects use `2` / `3`.

### ProjectRisk body

```json
{
  "risk_name": "RISK-013 Prompt-injection / LLM abuse leaks lab secrets",
  "risk_owner": 2,
  "risk_description": "...",
  "ai_lifecycle_phase": "Deployment & integration",
  "likelihood": "Likely",
  "severity": "Major",
  "risk_severity": "Major",
  "risk_category": ["Cybersecurity risk", "Data privacy risk"],
  "impact": "...",
  "mitigation_status": "In Progress",
  "projects": [1],
  "frameworks": [1],
  "approval_status": "Pending"
}
```

**Gotcha:** `risk_category` **must be an array** (string → 500: `.join is not a function`).

### Manual curl / PowerShell drills

```powershell
# Health
Invoke-RestMethod http://127.0.0.1:13000/health

# Login + list risks
$login = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:13000/api/users/login `
  -ContentType application/json `
  -Body '{"email":"org-admin@cadre.local","password":"***REMOVED***"}'
$H = @{ Authorization = "Bearer $($login.data.token)" }
(Invoke-RestMethod http://127.0.0.1:13000/api/projects -Headers $H).data | Format-Table id, project_title, ai_risk_classification
(Invoke-RestMethod http://127.0.0.1:13000/api/projectRisks -Headers $H).data | Format-Table id, risk_name, likelihood, severity
```

Script: [`scripts/verifywise-seed-baseline.ps1`](../scripts/verifywise-seed-baseline.ps1)

---

## Files we own (CADRE-Risk)

| Path | Purpose |
|------|---------|
| `scripts/verifywise-up.ps1` | Clone vendor + compose up |
| `scripts/verifywise-down.ps1` | Stop / optional `-RemoveVolumes` |
| `scripts/verifywise-seed-baseline.ps1` | REST seed Cadre Corp AI data |
| `docker/verifywise-compose.yml` | Container names, loopback ports, **nginx mount** |
| `docker/verifywise-nginx.conf` | `proxy_pass http://backend:3000` (fixes 502) |
| `docker/verifywise.env.example` | Template for gitignored env |
| `docs/img/verifywise-ai-risk.png` | Portfolio screenshot |

Vendor clone: `docker/vendor/verifywise/` (gitignored — never commit).

---

## Troubleshooting (lessons from lab)

| Symptom | Cause | Fix |
|---------|--------|-----|
| UI OK, login/API **502** | Upstream nginx uses `proxy_pass http://localhost:3000` inside frontend container | Mount [`docker/verifywise-nginx.conf`](../docker/verifywise-nginx.conf) via compose override (already wired). Re-run `verifywise-up.ps1` |
| Org create `Logo URL cannot be empty` | `logo: ""` rejected | Use a real URL string (seed script uses favicon URL) |
| Risk create 500 `.join is not a function` | `risk_category` sent as string | Send **array** of category strings |
| Email errors in backend logs | No `RESEND_API_KEY` | Harmless for lab login |
| Port clash | Another stack on 18080/13000 | `verifywise-down` other apps; ports are loopback-only |

---

## Practice checklist (self-drill)

- [ ] Cold start: env → up → health OK  
- [ ] Seed script: 3 projects, 3 models, 4 risks  
- [ ] UI login as org-admin; open Risk management  
- [ ] Edit RISK-013; confirm HIGH RISK from Likely × Major  
- [ ] API: login → GET projects → GET projectRisks  
- [ ] Break/fix: temporarily remove nginx mount → see 502 → restore  
- [ ] Down with `-RemoveVolumes` → full re-seed  

---

## License

VerifyWise is **BSL 1.1** (source-available). Fine for personal CISSP lab; check licensing before commercial redistribute.

---

*2026-07-13 — full practice runbook + screenshot + nginx 502 fix*
