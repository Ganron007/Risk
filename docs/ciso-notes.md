# CISO Assistant integration notes

> **Sprint 2 (2026-07-13):** GRC UI sink is **[CISO Assistant Community](https://github.com/intuitem/ciso-assistant-community)**.
> Bring-up: [`docker/README.md`](../docker/README.md) · Screenshot: [`img/ciso-risk-register.png`](img/ciso-risk-register.png)

**Rule:** Markdown (`docs/risk-register-baseline.md`) is SSoT. CISO Assistant is a **sink** — seeded for demos, not the system of record.

---

## Lab URL / creds

| Item | Value |
|------|-------|
| UI | **http://localhost:8080** (HTTP lab mode — see note below) |
| API base | `http://localhost:8080/api` |
| OpenAPI | `http://localhost:8080/api/schema/` · Swagger (DEBUG): `/api/schema/swagger/` |
| Auth header | `Authorization: Token <PAT>` (**Token**, not Bearer) |
| Admin | Local `createsuperuser` (e.g. `admin@cadre.local`) — never commit passwords |
| DB | SQLite under `docker/vendor/ciso-assistant/db/` (gitignored) |

**HTTP vs HTTPS:** Upstream default is `https://localhost:8443` with Caddy `tls internal`. On Windows Firefox that often fails with `SSL_ERROR_INTERNAL_ERROR_ALERT` (no cert bypass). Lab override [`docker/ciso-compose.yml`](../docker/ciso-compose.yml) serves plain HTTP on **:8080**.

---

## Operator path (screenshot)

1. `.\scripts\ciso-up.ps1`
2. Create admin if needed (see `ciso-up.ps1` output / `createsuperuser`)
3. In UI: create domain **Cadre Corp** (once), load library **5x5 ISO-27005** if missing
4. Seed baseline risks via REST: `.\scripts\ciso-seed-baseline.ps1 -Token <PAT>`
5. UI → Risk → **Cadre Corp Baseline Risk Register** → screenshot → `docs/img/ciso-risk-register.png`

### Practice checklist (self-drill)

- [ ] Cold start CISO HTTP `:8080`
- [ ] Create PAT; run `ciso-seed-baseline.ps1`
- [ ] Confirm RISK-001…018 subset in UI
- [ ] Cross-sink: VerifyWise practice — [`verifywise-notes.md`](verifywise-notes.md)

Done for R2-S2.12 (CISO). VerifyWise: same checklist item, separate runbook.

---

## REST API — auth (PAT)

Upstream docs: create a **Personal Access Token** from the user profile (Settings → Personal access tokens), or mint one via Django for lab-only:

```powershell
docker compose -p cadre-risk-ciso `
  -f docker\vendor\ciso-assistant\docker-compose.yml `
  -f docker\ciso-compose.yml `
  exec backend uv run python manage.py createsuperuser   # first time only
```

PAT create (UI preferred). Header on every call:

```http
Authorization: Token <your-pat>
Content-Type: application/json
```

Probe:

```powershell
$H = @{ Authorization = "Token $env:CISO_PAT"; "Content-Type" = "application/json" }
Invoke-RestMethod -Uri "http://localhost:8080/api/folders/" -Headers $H
```

---

## REST API — data ingestion (baseline register)

CISO models risks as **risk scenarios** inside a **risk assessment**, under a **perimeter**, under a **folder/domain**. Matrix scoring uses indices into the loaded matrix (lab uses **5x5 ISO-27005**, indices `0..4`).

### Object graph

```text
Folder (domain: Cadre Corp)
  └── Perimeter (Cadre Corp Lab)
        └── RiskAssessment (Cadre Corp Baseline Risk Register)
              ├── risk_matrix → 5x5 ISO-27005
              └── RiskScenario[]  (RISK-001 …)
                    ref_id, name, current_proba, current_impact,
                    residual_proba, residual_impact, treatment
```

### Endpoints used

| Step | Method | Path | Purpose |
|------|--------|------|---------|
| 1 | `GET` | `/api/folders/` | Find **Cadre Corp** domain id |
| 2 | `GET` | `/api/risk-matrices/` | Find **5x5 ISO-27005** id |
| 3 | `POST` | `/api/perimeters/` | Create **Cadre Corp Lab** (`folder`, `name`, `ref_id`) |
| 4 | `POST` | `/api/risk-assessments/` | Create assessment (`folder`, `perimeter`, `risk_matrix`, `status`, `version`) |
| 5 | `POST` | `/api/risk-scenarios/` | One call per baseline risk (`risk_assessment`, `ref_id`, scores, `treatment`) |
| — | `GET` | `/api/risk-scenarios/?risk_assessment=<uuid>` | Verify seed |

### Likelihood / impact mapping (markdown → matrix)

Markdown register uses L×I on **1–3**. Lab maps onto 5×5 indices:

| Markdown L or I | Matrix index | Typical label |
|-----------------|--------------|---------------|
| 1 | 0 | very low |
| 2 | 2 | medium |
| 3 | 4 | very high |

Product of indices drives the coloured **Current / Residual level** in the UI (e.g. 4×4 → very high).

### Seeded demo set (2026-07-13)

From [`risk-register-baseline.md`](risk-register-baseline.md):

| ref_id | Title (short) |
|--------|----------------|
| RISK-001 | Domain Admin compromise via DCSync / secretsdump |
| RISK-002 | ADCS ESC abuse |
| RISK-003 | Cross-forest trust / SID history |
| RISK-004 | Unconstrained delegation on mbr01 |
| RISK-005 | SCCM / WSUS misconfig |
| RISK-007 | Client forensic evidence / CoC |
| RISK-013 | Prompt-injection / LLM abuse |
| RISK-018 | AI finding without HITL |

### One-shot seed script

```powershell
# PAT from UI profile — do not commit
$env:CISO_PAT = "<paste-pat>"
.\scripts\ciso-seed-baseline.ps1
# or: .\scripts\ciso-seed-baseline.ps1 -Token "<paste-pat>"
```

Script: [`scripts/ciso-seed-baseline.ps1`](../scripts/ciso-seed-baseline.ps1)  
Idempotent enough for lab: reuses existing perimeter/assessment by name when present; posts scenarios (skip/update manually if re-run duplicates).

### Minimal PowerShell example (single scenario)

```powershell
$Base = "http://localhost:8080/api"
$H = @{ Authorization = "Token $env:CISO_PAT"; "Content-Type" = "application/json" }

# assume $folderId, $perimeterId, $matrixId, $assessmentId already resolved
$body = @{
  risk_assessment = $assessmentId
  ref_id          = "RISK-001"
  name            = "Domain Admin compromise via DCSync / secretsdump"
  current_proba   = 4
  current_impact  = 4
  residual_proba  = 4
  residual_impact = 4
  treatment       = "mitigate"
  description     = "From docs/risk-register-baseline.md"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "$Base/risk-scenarios/" -Headers $H -Body $body
```

---

## Future (optional)

- `src/ciso_client.py` — push scored findings from `risk_engine` (not required for Sprint 2)
- Full 18-row register sync on schedule
- VerifyWise remains the AI-governance sink (`docs/verifywise-notes.md`)

---

*Updated 2026-07-13 — HTTP :8080 + REST seed; Eramba removed*
