# CADRE-Risk — Docker & GRC Sinks

> **Markdown is SSoT.** The core CADRE-Risk application runs in a single container named `Risk`. The two GRC UIs are optional sinks for demos / CISSP practice, arranged under the same `Risk` Docker Desktop group.
> Prefer **one stack at a time** on a 16 GB laptop.

| Service | Focus | Project / Container | UI / Port | Control |
|---------|-------|---------------------|-----------|---------|
| **CADRE-Risk Engine** | GRC scoring, board memos, unified HTML dashboard | `Risk` / `Risk` | http://localhost:8895 | `docker compose up -d` |
| **[CISO Assistant](https://github.com/intuitem/ciso-assistant-community)** | Classic GRC + 150+ frameworks (ISO 27001, SOC 2, NIST CSF, GDPR) | `Risk` / `cadre-risk-ciso-*` | http://localhost:8080 | `scripts/ciso-up.ps1` + `ciso-seed-baseline.ps1` |
| **[VerifyWise](https://github.com/verifywise-ai/verifywise)** | AI governance (EU AI Act, ISO 42001, NIST AI RMF, LLM evals) | `Risk` / `cadre-risk-vw-*` | http://127.0.0.1:18080 | `scripts/verifywise-up.ps1` + `verifywise-seed-baseline.ps1` |

---

## Port map

| Port | Service |
|------|---------|
| `8895` | CADRE-Risk core web dashboard & artifacts API (`Risk`) |
| `8080` | CISO Assistant (HTTP lab; upstream default TLS is `:8443`) |
| `18080` | VerifyWise frontend |
| `13000` | VerifyWise backend API |
| `6333` | CISO Qdrant (loopback) |

---

## Quick starts

### 1. CADRE-Risk Core Container (standalone)

```powershell
# Build and run the single "Risk" container:
docker compose up -d

# Open unified dashboard:
# http://localhost:8895/
# Health check:
# http://localhost:8895/health
```

---

## Per-sink docs

| Sink | Notes |
|------|-------|
| CISO Assistant | [`docs/ciso-notes.md`](../docs/ciso-notes.md) |
| VerifyWise | [`docs/verifywise-notes.md`](../docs/verifywise-notes.md) |

Vendor clones live under `docker/vendor/` (gitignored). Overrides:

- `docker/ciso-compose.yml`
- `docker/verifywise-compose.yml` + `docker/verifywise.env.example` + `docker/verifywise-nginx.conf`

---

## Quick starts

### CISO Assistant (classic GRC)

```powershell
cd <repo-root>   # folder containing scripts/ and docker/
.\scripts\ciso-up.ps1
# http://localhost:8080 — create local superuser on first run
# Seed Cadre Corp risks via REST (PAT from UI profile):
#   $env:CISO_PAT = "<pat>"; .\scripts\ciso-seed-baseline.ps1
# Full API notes: docs/ciso-notes.md
```

### VerifyWise (AI governance)

```powershell
copy docker\verifywise.env.example docker\verifywise.env
notepad docker\verifywise.env   # set JWT_SECRET + SUPERADMIN_PASSWORD (+ DB/ENCRYPTION keys)
.\scripts\verifywise-up.ps1
.\scripts\verifywise-seed-baseline.ps1
# UI: http://127.0.0.1:18080  — login org-admin@cadre.local (created by seed)
# Practice runbook: docs/verifywise-notes.md
# nginx 502 fix: docker/verifywise-nginx.conf mounted by verifywise-compose.yml
```

### Stop / free RAM

```powershell
.\scripts\ciso-down.ps1
.\scripts\verifywise-down.ps1
```

---

## Screenshot targets

| File | Source |
|------|--------|
| `docs/img/ciso-risk-register.png` | CISO Assistant risk register |
| `docs/img/verifywise-ai-risk.png` | VerifyWise AI use-case risks |

---

*Two-sink model — Eramba removed 2026-07-13*
