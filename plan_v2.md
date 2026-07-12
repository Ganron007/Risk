# CADRE-Risk — Plan v2 (execution SSoT)

> **Created:** 2026-07-12  
> **Status:** ACTIVE — Sprint 0–1 done; Sprint 2–3 **code done** 2026-07-13; **R2-S2.3** unblocked by Docker pivot (2026-07-13) — UI screenshot now reachable without a VM  
> **Supersedes:** [`docs/PLAN.md`](docs/PLAN.md) (v1 planning dump — keep as reference for Cadre Corp fiction + full exercise ID catalog)  
> **Cold-start:** This file → [`CHECKLIST.md`](CHECKLIST.md) → [`README.md`](README.md)  
> **Operator context:** CISSP exam ~3 months out; daily CADRE lab testing concurrent; ~14h/day capacity. Risk slots fit *between* lab runs — do not block RevAI / DFIR-Nexus / DarkAI / Eva7ion daily practice.

**Edition note (Sprint 2):** Eramba REST API is **Enterprise-only**. Community Edition uses `python -m src.eramba_export` CSV import — see [`docs/eramba-notes.md`](docs/eramba-notes.md).

**Deployment pivot (2026-07-13):** The VM approach is **abandoned**. Eramba CE runs as a local **Docker stack** (`docker/` — Eramba app + MySQL 8 + Redis), mirroring the public demo at <https://demo.cloud.eramba.org/dashboard>. This unblocks **R2-S2.3** (UI screenshot) without standing up a VM. Rationale (operator): *"eramba VM sucks, so i go docker."* See **§3 Sprint 2** for the new Docker tasks (R2-S2.5–S2.8).

---

## 1. Product definition (locked)

**CADRE-Risk is a hands-on GRC lab**, not a fat ingest product.

| Layer | What ships | CISSP |
|-------|------------|-------|
| **L1 — Enterprise context** | Cadre Corp profile, asset inventory, risk appetite, regulatory register | Domains 1, 2 |
| **L2 — Exercises** | Worked CISSP risk exercises against *real CADRE findings* | Domains 1→8 over time |
| **L3 — Tooling** | Score findings → Markdown board memo; later Eramba sink | Domains 1, 7 |

**Rules (non-negotiable):**

1. **Markdown is SSoT; Eramba is a sink.** Register + board memos must stand alone if Eramba is down.
2. **Findings-first.** Every scored risk cites a path under `samples/` or a documented tool output.
3. **10 excellent Domain 1 exercises before 60 stubs.** Expand domains after Sprint 1 is green.
4. **One writer repo:** `CADRE-Risk` only. Do not edit main CADRE ansible/campaign for Risk work.
5. **No secrets in git.** Eramba creds → local env / ignored file (`config/eramba.local.env`).

**Portfolio line (after Sprint 1):**  
*Built a CISSP-aligned GRC lab on a real AD/SOC estate: asset inventory, risk register, control mapping, and automated board memos from security-tool findings.*

---

## 2. Relationship to other CADRE work

| Project | How Risk uses it | Blocking? |
|---------|------------------|-----------|
| Main CADRE | Asset IDs from `docs/architecture.md` + campaign attack surfaces | No — cite docs / freeze samples |
| CADRE-RevAI | Malware verdict / report samples | No — copy sample JSON into `samples/` |
| DFIR-Nexus | Incident / case summary samples | No — wait for frozen export or hand-write sample |
| Praxis | SARIF from DarkAI / host scans | No — copy one SARIF into `samples/` |
| CADRE-DarkAI | Prompt-injection audit JSONL | No — copy lines into `samples/` |
| Eramba CE (Docker) | GRC UI (Sprint 2) — local stack, not a VM | Soft gate — Sprint 1 does **not** need it |

Daily lab testing continues on those projects. Risk work consumes **frozen samples**, not live coupling.

---

## 3. Sprint plan (execute in order)

### Sprint 0 — Repo hygiene (≤ half day)

| ID | Item | Done when |
|----|------|-----------|
| **R2-S0.1** | `git init` (and remote when you choose) | `.git` exists |
| **R2-S0.2** | Fix `CADRE-ALL.code-workspace` JSON (comma before Risk folder) | Workspace validates |
| **R2-S0.3** | `CHECKLIST.md` + this `plan_v2.md` + README aligned | Cold-start works |
| **R2-S0.4** | Mark `docs/PLAN.md` as superseded | Banner at top of PLAN.md |

### Sprint 1 — Portfolio MVP **without Eramba** (primary ship target)

Goal: openable artifacts for interviews + CISSP Domain 1 practice.

| ID | Deliverable | Path |
|----|-------------|------|
| **R2-S1.1** | Enterprise context (Cadre Corp + inventory narrative) | `docs/enterprise-context.md` |
| **R2-S1.2** | Board risk appetite statement | `docs/risk-appetite-statement.md` |
| **R2-S1.3** | Regulatory obligations (SOC 2 / GDPR / ISO 27001) | `docs/regulatory-obligations.md` |
| **R2-S1.4** | Machine-readable asset inventory | `config/asset-inventory.csv` |
| **R2-S1.5** | Asset → owner → classification → control map | `config/risk-mapping.yml` |
| **R2-S1.6** | Baseline risk register (15–20 risks, each tied to AST-* / attack surface) | `docs/risk-register-baseline.md` |
| **R2-S1.7** | Control register (CADRE capabilities → NIST CSF + ISO where easy) | `docs/control-register.md` |
| **R2-S1.8** | Five sample findings (DarkAI, Praxis, RevAI, Elastic-shaped, VR-shaped) | `samples/findings/` |
| **R2-S1.9** | Domain 1 exercises **R-EX-001–010** with answer keys | `docs/exercises/` |
| **R2-S1.10** | Unified finding schema + scorer | `src/risk_engine.py` (+ schema doc in `docs/finding-schema.md`) |
| **R2-S1.11** | Board memo generator | `src/board_report.py` |
| **R2-S1.12** | Minimal ingest of sample JSON | `src/ingest.py` |
| **R2-S1.13** | Unit tests for scoring | `tests/test_risk_engine.py` |
| **R2-S1.14** | README demo section + example board memo output | `docs/examples/board-memo-sample.md` |

**Sprint 1 exit criteria:**

```text
python -m pytest tests/ -q
python -m src.board_report --samples samples/findings/ --out artifacts/board-memo.md
# board-memo.md + risk-register-baseline.md reviewable without Eramba
```

### Sprint 2 — Thin Eramba bridge (after Sprint 1 green)

**Original tasks (code already done):**

| ID | Item | Status |
|----|------|--------|
| **R2-S2.1** | `docs/eramba-notes.md` — endpoint, auth model, CE limits (no secrets) | ✅ |
| **R2-S2.2** | `src/eramba_client.py` — create/link asset + risk + control (Enterprise REST + CE dry-run) | ✅ |
| **R2-S2.3** | E2E: one sample → score → Eramba UI; screenshot in README | **[!]→[~]** unblocked by Docker (was blocked on VM) |
| **R2-S2.4** | Import asset CSV + baseline risks (or document CSV import fallback) | ✅ |

**Docker tasks (new, 2026-07-13 — replace the VM approach):**

| ID | Item | Done when | Path |
|----|------|-----------|------|
| **R2-S2.5** | Eramba CE compose stack — app + MySQL 8 + Redis | `docker compose -f docker/eramba-compose.yml up -d` brings UI to `http://localhost:8080` (or chosen port); initial wizard completes | `docker/eramba-compose.yml` |
| **R2-S2.6** | `docker/.env.example` — DB passwords, ports, volume paths; real values in gitignored `docker/.env` | Copy `.example` → `.env`, fill, `docker compose config` validates | `docker/.env.example` |
| **R2-S2.7** | `docker/README.md` — bring-up guide: pull, first-run wizard (DB seed, admin user, settings), CE vs Enterprise toggle, teardown/persistence, resource notes | Operator who has never used Docker can stand up Eramba CE from this doc alone | `docker/README.md` |
| **R2-S2.8** | Wire existing CSV pack into Docker UI — import `artifacts/eramba-import/assets.csv` + `risks.csv` through the running container's web UI, screenshot → `docs/img/eramba-risk-register.png`, link from README | Screenshot committed; README "Blocker" section retired | closes **R2-S2.3** |

**Docker design notes (locked for S2.5–S2.8):**

- **Stack:** three services — `eramba` (official `eramba/eramba` image), `mysql` (MySQL 8.0 / MariaDB 10.6 per Eramba reqs), `redis` (cache). One compose file, one external network, three named volumes (`eramba_db`, `eramba_files`, `redis_cache`).
- **Reference sources:** official [eramba/docker](https://github.com/eramba/docker) `1.x` branch `docker-compose.simple-install.yml` + `.env`; cross-checked against community builds [digitorus/eramba](https://github.com/digitorus/eramba) and [markz0r/eramba-community-docker](https://github.com/markz0r/eramba-community-docker) for cron handling.
- **Ports:** Eramba HTTP on `127.0.0.1:8080` (loopback-only — this is a single-user lab, not an exposed service). MySQL/Redis **not** published (internal to the compose network).
- **First-run:** Eramba's web wizard handles DB seed, admin account, and initial settings — no SQL hand-seeding. The compose file only wires the connection env (`DB_HOST`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `CACHE_URL`).
- **Persistence:** named volumes so `docker compose down` (without `-v`) keeps data; `down -v` for a clean reset. Documented in `docker/README.md`.
- **Cron:** Eramba needs hourly/daily/yearly jobs. CE image runs these inside the container (community builds add a sidecar — confirm which during S2.5 and document).
- **No secrets in git:** DB passwords live in gitignored `docker/.env`, never in the compose file directly.
- **CE vs Enterprise:** the same compose file runs Enterprise if you mount a license; the CSV path is CE-only. `eramba_client.py` already handles both editions.
- **Existing CSV pack is unchanged** — `artifacts/eramba-import/{assets,risks}.csv` import through the Docker UI exactly as the VM would have. No `eramba_export.py` changes needed.

If Eramba CE API is weak: **CSV/Excel import path** still counts as GRC-tool integration.

### Sprint 3 — Broader CISSP curriculum + richer ingest

| ID | Item |
|----|------|
| **R2-S3.1** | Domain 2 exercises (asset/data lifecycle) — quality over quantity |
| **R2-S3.2** | Domain 6–7 exercises tied to campaign / SOC findings |
| **R2-S3.3** | Domain 3 / 8 as needed for exam weak areas |
| **R2-S3.4** | Optional live adapters (Praxis SARIF, RevAI verdict, DarkAI JSONL) — still prefer frozen samples for demos |
| **R2-S3.5** | Dedupe / update existing risks on re-ingest |

### Explicitly deferred

- Feedback loop into CADRE analysis queues  
- Live Elastic / Velociraptor API pulls as MVP requirement  
- Full 55–65 exercise stubs from v1 PLAN  
- Blocking DFIR-Nexus / RevAI public releases on Risk  

---

## 4. Cadre Corp context (carry forward from v1)

Keep the enterprise fiction from [`docs/PLAN.md`](docs/PLAN.md) §2 when writing Sprint 1 docs:

- **Cadre Corp** — mid-size DFIR services firm; low appetite for client-evidence compromise  
- **Assets** — AST-001… from architecture (DCs, members, elk/vr/monitor, cloud plane, forensic data)  
- **Frameworks** — SOC 2 Type II (contractual), GDPR (EU evidence), ISO 27001 (in progress)  
- **Risk appetite** — low for client data / CoC; moderate for isolated research labs (DarkAI, RevAI)

Do not invent new hostnames that contradict `CADRE/docs/architecture.md`.

---

## 5. Scoring model (v2 — ship in Sprint 1)

Qualitative 1–3 × 1–3 → score 1–9 (same matrix as v1 PLAN §4). ALE ranges are **teaching aids** for Domain 1 quantitative questions — label them as illustrative, not audited financials.

```json
{
  "id": "cadre-finding-001",
  "source": "darkai",
  "severity": "high",
  "title": "Prompt injection leaked lab secret via /chat",
  "description": "…",
  "asset_id": "AST-035",
  "discovered_at": "2026-07-12T14:30:00Z",
  "evidence": "samples/findings/darkai-prompt-inject.jsonl",
  "raw": {}
}
```

---

## 6. Suggested weekly rhythm (with CISSP + daily labs)

You are already testing CADRE projects daily. Treat Risk as a **fixed daily block**, not a weekend-only project.

| Block | Suggestion |
|-------|------------|
| **Daily CADRE labs** | Keep as-is (campaign / RevAI / Nexus / DarkAI / Eva7ion) |
| **CISSP study** | Book + practice questions (Domains rotate) |
| **CADRE-Risk** | 60–90 min after a lab run: either (a) write 1 exercise from that day’s finding, or (b) advance one Sprint 1 checklist row |

**3-month CISSP alignment:**

| Month | Risk focus | CISSP focus |
|-------|------------|-------------|
| **M1** | Finish Sprint 0 + Sprint 1 | Domain 1–2 heavy; Risk exercises *are* Domain 1 practice |
| **M2** | Sprint 2 Eramba + Domain 2–7 exercise expansion | Domains 3–7; use Risk memos as essay/communication drill |
| **M3** | Sprint 3 polish + mock board brief | Weak-domain review + full practice exams |

---

## 7. Target layout (after Sprint 1 + Sprint 2 Docker)

```text
CADRE-Risk/
├── README.md
├── plan_v2.md              ← THIS FILE (execution SSoT)
├── CHECKLIST.md            ← flip statuses here first
├── docker/                 ← Sprint 2 Docker pivot (R2-S2.5–S2.8)
│   ├── eramba-compose.yml  ← Eramba CE + MySQL + Redis
│   ├── .env.example        ← DB passwords, ports (copy → .env, gitignored)
│   └── README.md           ← bring-up guide for Docker newcomers
├── docs/
│   ├── PLAN.md             ← v1 archive / reference
│   ├── enterprise-context.md
│   ├── risk-appetite-statement.md
│   ├── regulatory-obligations.md
│   ├── risk-register-baseline.md
│   ├── control-register.md
│   ├── finding-schema.md
│   ├── eramba-notes.md     ← Sprint 2 (+ Docker deployment section)
│   ├── exercises/          ← R-EX-001…
│   └── examples/
├── config/
│   ├── asset-inventory.csv
│   ├── risk-mapping.yml
│   └── eramba.local.env.example  ← Enterprise creds (CE users ignore)
├── samples/findings/
├── src/
│   ├── ingest.py
│   ├── risk_engine.py
│   ├── board_report.py
│   ├── eramba_export.py    ← CSV pack generator (CE primary path)
│   └── eramba_client.py    ← Enterprise REST + CE dry-run
├── tests/
└── artifacts/              ← generated memos + eramba-import CSV pack (gitignored or sample-only)
```

---

## 8. Immediate next action

Sprint 0–1 + Sprint 2 (S2.1–S2.4) + Sprint 3 are **done**. The only remaining work is the **Docker pivot** (S2.5–S2.8), which closes the last open item (R2-S2.3 screenshot).

1. **R2-S2.5** — create `docker/eramba-compose.yml` (Eramba + MySQL + Redis).  
2. **R2-S2.6** — create `docker/.env.example`; update `.gitignore` for `docker/.env` + volume state.  
3. **R2-S2.7** — write `docker/README.md` (bring-up guide for a Docker newcomer).  
4. **R2-S2.8** — stand up the stack, import the existing CSV pack through the UI, screenshot → `docs/img/eramba-risk-register.png` → link from README.  
5. After each step: flip [`CHECKLIST.md`](CHECKLIST.md).

**Deferred until after the Docker stack is green:** update `docs/eramba-notes.md` with a "Docker deployment" section pointing at `docker/README.md`, and refresh `artifacts/eramba-import/IMPORT.md` to reference the Docker UI (`http://localhost:8080`) instead of the VM.

---

*Plan v2 — 2026-07-12; Docker pivot 2026-07-13. Execute sprints in order. CISSP exam ≈ 3 months; Risk supports Domain 1–2 practice without replacing book study.*
