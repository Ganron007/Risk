# Eramba integration notes

> **Sprint 2:** R2-S2.1  
> **No secrets in git.** Put credentials in `config/eramba.local.env` (gitignored).

---

## Edition reality (blocker for pure API on CE)

| Edition | REST API | What CADRE-Risk uses |
|---------|----------|----------------------|
| **Community (CE)** | **Not available** — confirmed by Eramba staff ([forum](https://discussions.eramba.org/t/question-api-available-on-community-edition/5727)) | **CSV / Excel import** via UI (`src/eramba_export.py`) |
| **Enterprise** | REST + Swagger per module; HTTP Basic over TLS | `src/eramba_client.py` against your Swagger paths |

If your lab VM is **CE only**, Sprint 2.3 “API push → UI screenshot” becomes: **import CSV → screenshot**. That still counts as GRC-tool integration per `plan_v2.md`.

---

## Local env template

Copy to `config/eramba.local.env` (never commit):

```bash
# Required for any live call
ERAMBA_BASE_URL=https://eramba.lab.local
ERAMBA_EDITION=ce          # ce | enterprise

# Enterprise API only
ERAMBA_USER=
ERAMBA_PASSWORD=
# Optional overrides after you read Swagger on your build
ERAMBA_API_PREFIX=/api
ERAMBA_RISKS_PATH=/security-risks
ERAMBA_ASSETS_PATH=/assets
ERAMBA_VERIFY_TLS=true
```

Load with: `python -m src.eramba_client --env config/eramba.local.env ...`

---

## Enterprise auth model (when available)

1. Create an API user; enable **REST APIs** toggle on the account.  
2. Grant group permission for **API Documentation** on the modules you need (Risks, Assets, Controls).  
3. Calls use **HTTP Basic** over **HTTPS**.  
4. Discover exact paths in **Swagger** (module menu → API). Paths differ by Eramba version — do not hardcode production URLs from blog posts.  
5. Public Postman workspace (Enterprise testing): [eramba Postman](https://www.postman.com/eramba/workspace/eramba/overview). Demo env is Eramba’s, not Cadre Corp.

Reference learning: [REST APIs intro](https://www.eramba.org/learning/courses/29/episodes/271).

---

## CE import workflow (primary for most labs)

```powershell
cd C:\STUDY\Github\CADRE-Platform\CADRE-Risk
python -m src.eramba_export --out artifacts/eramba-import
```

Produces:

| File | Contents |
|------|----------|
| `artifacts/eramba-import/assets.csv` | From `config/asset-inventory.csv` (Eramba-friendly columns) |
| `artifacts/eramba-import/risks.csv` | Baseline RISK-* + optionally scored sample findings |
| `artifacts/eramba-import/IMPORT.md` | Click-path checklist for CE UI |

Then in Eramba CE: import assets → import risks → link controls manually if CE import is limited → screenshot for README.

---

## Operator inputs still needed (blockers)

Fill these when ready — nothing else in Sprint 2/3 waits on them:

1. **Is your Eramba VM CE or Enterprise?**  
2. **Base URL** reachable from the host running CADRE-Risk.  
3. If Enterprise: API user + password in `eramba.local.env`.  
4. Paste one Swagger risk-create schema snippet into this doc under “Local Swagger notes” (optional).  
5. Drop a PNG screenshot into `docs/img/eramba-risk-register.png` and link from README (**R2-S2.3**).

---

## Local Swagger notes (fill after login)

```text
Eramba version:
Risks list path:
Risk create method/path:
Asset create path:
Custom fields used:
```

---

*R2-S2.1 — 2026-07-13*
