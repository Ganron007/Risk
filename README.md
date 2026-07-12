# CADRE-Risk

<p align="center">
  <img src="assets/risk-logo.svg" alt="Risk Logo" width="620">
</p>

**Hands-on GRC lab for the CADRE platform — CISSP risk practice against a real AD/SOC estate.**

> **Plan:** [`plan_v2.md`](plan_v2.md) · **Tracker:** [`CHECKLIST.md`](CHECKLIST.md) · **Eramba notes:** [`docs/eramba-notes.md`](docs/eramba-notes.md)

---

## Status

| Sprint | State |
|--------|--------|
| 0 Hygiene | ✅ |
| 1 Portfolio MVP | ✅ |
| 2 Eramba bridge | ✅ code/CSV · **[!]** UI screenshot needs your VM |
| 3 Domains + adapters | ✅ |
| Tests | **11 passed** |

---

## Quick demos

```powershell
cd C:\STUDY\Github\CADRE-Platform\CADRE-Risk
python -m pip install pyyaml pytest
python -m pytest tests/ -q

# Board memo (Sprint 1)
python -m src.board_report --samples samples/findings --out artifacts/board-memo.md

# Eramba CE import pack (Sprint 2 — primary path)
python -m src.eramba_export --out artifacts/eramba-import
# Then follow artifacts/eramba-import/IMPORT.md in the Eramba UI
```

**Important:** Eramba **Community Edition has no REST API** (Enterprise-only). CADRE-Risk’s CE path is CSV import. Enterprise users can use `python -m src.eramba_client --env config/eramba.local.env --push-samples` after filling credentials (never commit `eramba.local.env`).

---

## Portfolio artifacts

| Artifact | Path |
|----------|------|
| Enterprise context | `docs/enterprise-context.md` |
| Risk appetite | `docs/risk-appetite-statement.md` |
| Risk register (18) | `docs/risk-register-baseline.md` |
| Control register | `docs/control-register.md` |
| Board memo sample | `docs/examples/board-memo-sample.md` |
| CISSP exercises | `docs/exercises/` (Domains 1, 2, 3, 6, 7, 8) |
| Eramba CSV pack | `artifacts/eramba-import/` (regenerate anytime) |

---

## Architecture

```text
CADRE tool samples / SARIF / JSONL
        │
        ▼
 adapters → ingest → dedupe → risk_engine → board_report
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
              Markdown memo                    Eramba CE CSV import
                                               (or Enterprise REST)
```

---

## Blocker for you

Complete **R2-S2.3**: import CSVs into your Eramba UI → save screenshot as `docs/img/eramba-risk-register.png` → tell me to wire it into this README.

---

## License

MIT — same as the rest of the CADRE platform.
