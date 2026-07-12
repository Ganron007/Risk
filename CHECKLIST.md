# CADRE-Risk — Checklist

> **SSoT for status.** Flip here first. **Plan:** [`plan_v2.md`](plan_v2.md)  
> **Legend:** `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked on operator input

---

## Sprint 0 — Hygiene

| ID | Item | Status | Notes |
|----|------|--------|-------|
| R2-S0.1–S0.4 | Hygiene pack | [x] | 2026-07-12 |

## Sprint 1 — Portfolio MVP (no Eramba)

| ID | Item | Status | Notes |
|----|------|--------|-------|
| R2-S1.1–S1.14 | Full MVP | [x] | 2026-07-12 · 5 tests at ship |

## Sprint 2 — Eramba

| ID | Item | Status | Notes |
|----|------|--------|-------|
| R2-S2.1 | docs/eramba-notes.md | [x] | CE has **no** REST API — CSV primary |
| R2-S2.2 | src/eramba_client.py | [x] | Enterprise + dry-run; CE blocked with clear error |
| R2-S2.3 | E2E UI screenshot in README | **[!]** | Needs your Eramba VM: import CSV → screenshot → `docs/img/eramba-risk-register.png` |
| R2-S2.4 | CSV import package | [x] | `python -m src.eramba_export` → `artifacts/eramba-import/` |

## Sprint 3 — Expand

| ID | Item | Status | Notes |
|----|------|--------|-------|
| R2-S3.1 | Domain 2 exercises | [x] | R-EX-016–020 |
| R2-S3.2 | Domain 6–7 exercises | [x] | R-EX-031–040 |
| R2-S3.3 | Domain 3 / 8 exercises | [x] | R-EX-026,028,046,047,049,050 |
| R2-S3.4 | Ingest adapters | [x] | `src/adapters.py` SARIF / RevAI / DarkAI JSONL |
| R2-S3.5 | Risk dedupe on re-ingest | [x] | `src/dedupe.py` |

## Tests

| Suite | Status |
|-------|--------|
| `pytest tests/` | **11 passed** (2026-07-13) |

---

## Your inputs (only remaining blockers)

1. Confirm Eramba edition (**CE vs Enterprise**) and base URL.  
2. If CE: import `artifacts/eramba-import/*.csv` per `IMPORT.md`, screenshot → `docs/img/eramba-risk-register.png`.  
3. If Enterprise: fill `config/eramba.local.env` (from `.example`), align Swagger paths in `eramba-notes.md`, then `python -m src.eramba_client --push-samples`.  

---

*Last updated: 2026-07-13 — Sprint 2/3 code complete; S2.3 awaiting your Eramba UI*
