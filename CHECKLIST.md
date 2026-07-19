# CADRE-Risk — Checklist

> **SSoT for status.** Flip here first. **Plan:** [`plan_v2.md`](plan_v2.md)  
> **Legend:** `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked on operator input

---

## Sprint 0 — Hygiene

| ID | Item | Status | Notes |
|----|------|--------|-------|
| R2-S0.1–S0.4 | Hygiene pack | [x] | 2026-07-12 |

## Sprint 1 — Portfolio MVP (no GRC UI)

| ID | Item | Status | Notes |
|----|------|--------|-------|
| R2-S1.1–S1.14 | Full MVP | [x] | 2026-07-12 |

## Sprint 2 — GRC sinks

| ID | Item | Status | Notes |
|----|------|--------|-------|
| R2-S2.9 | CISO Assistant Docker + notes | [x] | HTTP `:8080` · [`docs/ciso-notes.md`](docs/ciso-notes.md) |
| R2-S2.10 | VerifyWise Docker + notes | [x] | `:18080` · nginx 502 fix · [`docs/verifywise-notes.md`](docs/verifywise-notes.md) |
| R2-S2.11 | Two-sink hub docs | [x] | `docker/README.md` + `docs/grc-sinks.md` |
| R2-S2.12 | UI screenshots | [x] | `ciso-risk-register.png` + `verifywise-ai-risk.png` |
| — | Eramba path | **removed** | 2026-07-13 — does not work; purged from repo |

## Sprint 3 — Expand

| ID | Item | Status | Notes |
|----|------|--------|-------|
| R2-S3.1–S3.5 | Domains + adapters + dedupe | [x] | 2026-07-13 |

## Tests

| Suite | Status |
|-------|--------|
| `pytest tests/` | **8 passed** (2026-07-13) |

---

## Practice (re-run anytime)

1. **CISO Assistant:** [`docs/ciso-notes.md`](docs/ciso-notes.md) — `ciso-up` → PAT → `ciso-seed-baseline` → UI  
2. **VerifyWise:** [`docs/verifywise-notes.md`](docs/verifywise-notes.md) — `verifywise-up` → `verifywise-seed-baseline` → UI as `org-admin@cadre.local`

---

*Last updated: 2026-07-13 — Eramba removed*
