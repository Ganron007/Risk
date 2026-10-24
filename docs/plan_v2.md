# CADRE-Risk — Plan v2 (execution SSoT)

> **Created:** 2026-07-12  
> **Updated:** 2026-07-27 — Sprint 4–6 complete; feedback loop and cross-platform integration done  
> **Status:** ACTIVE — Sprint 0–6 **done** 2026-07-27; GRC sinks = **CISO Assistant** + **VerifyWise** only  
> **Supersedes:** [`docs/PLAN.md`](docs/PLAN.md) (v1 planning dump — keep as reference for Cadre Corp fiction + full exercise ID catalog)  
> **Cold-start:** This file → [`CHECKLIST.md`](CHECKLIST.md) → [`README.md`](README.md)  
> **Operator context:** CISSP exam ~3 months out; daily CADRE lab testing concurrent; ~14h/day capacity. Risk slots fit *between* lab runs — do not block RevAI / DFIR-Nexus / DarkAI / Eva7ion daily practice.

**GRC sinks (2026-07-13):** **CISO Assistant** = classic GRC (REST API, frameworks). **VerifyWise** = AI governance (EU AI Act / ISO 42001 / NIST AI RMF for DarkAI / Praxis / RevAI). **Eramba was removed** from the repo (did not work for this lab) — do not reintroduce without an explicit decision.

**Strategic alignment (2026-07-27):**
- **CISO Assistant** → Classic GRC (ISO 27001, SOC 2, NIST CSF) → Tightly integrated with **CADRE main lab**
- **VerifyWise** → AI Governance (EU AI Act, ISO 42001, NIST AI RMF) → Tightly integrated with **DarkAI project**

---

## 1. Product definition (locked)

**CADRE-Risk is a hands-on GRC lab**, not a fat ingest product.

| Layer | What ships | CISSP |
|-------|------------|-------|
| **L1 — Enterprise context** | Cadre Corp profile, asset inventory, risk appetite, regulatory register | Domains 1, 2 |
| **L2 — Exercises** | Worked CISSP risk exercises against *real CADRE findings* | Domains 1→8 over time |
| **L3 — Tooling** | Score findings → Markdown board memo; optional GRC UI sinks | Domains 1, 7 |

**Rules (non-negotiable):**

1. **Markdown is SSoT; GRC tools are sinks.** Register + board memos must stand alone if every Docker UI is down.
2. **Findings-first.** Every scored risk cites a path under `samples/` or a documented tool output.
3. **10 excellent Domain 1 exercises before 60 stubs.** Expand domains after Sprint 1 is green.
4. **One writer repo:** `CADRE-Risk` only. Do not edit main CADRE ansible/campaign for Risk work.
5. **No secrets in git.** Creds → `docker/*.env` / `config/*.local.env` (all gitignored).

**Portfolio line (after Sprint 1):**  
*Built a CISSP-aligned GRC lab on a real AD/SOC estate: asset inventory, risk register, control mapping, and automated board memos from security-tool findings.*

---

## 2. Relationship to other CADRE work

| Project | How Risk uses it | Blocking? |
|---------|------------------|-----------|
| Main CADRE | Asset IDs from `docs/architecture.md` + campaign attack surfaces | No — cite docs / freeze samples |
| CADRE-RevAI | Malware verdict / report samples → also VerifyWise AI use-case | No — copy sample JSON into `samples/` |
| DFIR-Nexus | Incident / case summary samples | No — wait for frozen export or hand-write sample |
| Praxis | SARIF from DarkAI / host scans → CISO Assistant finding / VerifyWise AI risk | No — copy one SARIF into `samples/` |
| CADRE-DarkAI | Prompt-injection audit JSONL → VerifyWise AI risk | No — copy lines into `samples/` |
| **CISO Assistant (Docker)** | **Primary classic-GRC sink** — REST API push of risks/controls/compliance | Soft gate — optional demos |
| **VerifyWise (Docker)** | **AI-governance sink** — EU AI Act / ISO 42001 / NIST AI RMF for DarkAI/Praxis risks | Soft gate — optional demos |

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

### Sprint 1 — Portfolio MVP **without GRC UIs** (primary ship target)

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
# board-memo.md + risk-register-baseline.md reviewable without Docker UIs
```

### Sprint 2 — GRC tool sinks (after Sprint 1 green)

**Two-sink model only** (Eramba path deleted 2026-07-13 — did not work for this lab):

| ID | Item | Done when |
|----|------|-----------|
| **R2-S2.9** | CISO Assistant compose + scripts (`cadre-risk-ciso-*`, HTTP `:8080`) | ✅ `scripts/ciso-up.ps1` + REST seed [`docs/ciso-notes.md`](docs/ciso-notes.md) + `ciso-seed-baseline.ps1` |
| **R2-S2.10** | VerifyWise compose + scripts (`cadre-risk-vw-*`, `:18080`) + nginx 502 fix | ✅ `scripts/verifywise-up.ps1` + seed + [`docs/verifywise-notes.md`](docs/verifywise-notes.md) |
| **R2-S2.11** | Hub doc for both sinks (ports, RAM note, screenshot targets) | ✅ [`docker/README.md`](docker/README.md) + [`docs/grc-sinks.md`](docs/grc-sinks.md) |
| **R2-S2.12** | Screenshots: CISO + VerifyWise | ✅ `docs/img/ciso-risk-register.png` + `docs/img/verifywise-ai-risk.png` |

**Run one stack at a time** on constrained hosts. CISO = classic GRC demos; VerifyWise = AI governance for DarkAI/RevAI/Praxis.

### Sprint 3 — Broader CISSP curriculum + richer ingest

| ID | Item |
|----|------|
| **R2-S3.1** | Domain 2 exercises (asset/data lifecycle) — quality over quantity |
| **R2-S3.2** | Domain 6–7 exercises tied to campaign / SOC findings |
| **R2-S3.3** | Domain 3 / 8 as needed for exam weak areas |
| **R2-S3.4** | Optional live adapters (Praxis SARIF, RevAI verdict, DarkAI JSONL) — still prefer frozen samples for demos |
| **R2-S3.5** | Dedupe / update existing risks on re-ingest |

### Sprint 4 — Exercise quality standardization (2026-07-27)

**Quality Assessment Findings:**
- Domain 1 (15 exercises) upgraded to full CISSP-style format (scenario context, MCQs, detailed explanations, interview talking points)
- Domains 2-8 exercises exist but quality consistency needs verification
- Strong technical alignment with CADRE lab topology maintained
- Missing live integration reduces practical hands-on value
- No feedback loop from Risk findings to CADRE security improvements

| ID | Item | Priority |
|----|------|----------|
| **R2-S4.1** | Audit all 87 CISSP exercises for full format consistency (scenario, MCQs, explanations, interview points) | High |
| **R2-S4.2** | Upgrade Domains 2-8 exercises to match Domain 1 quality standard | High |
| **R2-S4.3** | Add campaign-phase mapping to EXERCISE-MAP.md (e.g., "After Phase 4 DCSync, do R-EX-002") | Medium |
| **R2-S4.4** | Expand samples/findings/ with real CADRE tool outputs (Elastic alerts, Velociraptor artifacts, DarkAI logs) | Medium |

### Sprint 5 — Live adapter integration (2026-07-27)

**Goal:** Optional live integration while maintaining frozen-sample approach for demos

| ID | Item | Priority |
|----|------|----------|
| **R2-S5.1** | Implement DarkAI JSONL → VerifyWise AI risk adapter (optional, opt-in) | Medium |
| **R2-S5.2** | Implement RevAI verdict → VerifyWise AI use-case adapter (optional, opt-in) | Medium |
| **R2-S5.3** | Implement Praxis SARIF → CISO Assistant finding adapter (optional, opt-in) | Medium |
| **R2-S5.4** | Add adapter configuration flag (frozen vs live mode) in config | Low |

### Sprint 6 — Feedback loop and integration (2026-07-27)

**Goal:** Enable Risk findings to inform CADRE security improvements

| ID | Item | Priority | Status |
|----|------|----------|--------|
| **R2-S6.1** | Create Risk → CADRE feedback mechanism (e.g., "RISK-001 closed after DCSync detection rule deployed") | High | ✅ Complete |
| **R2-S6.2** | Implement real-time board memo generation from live SIEM data (optional) | Medium | ✅ Complete (placeholder + CLI flags) |
| **R2-S6.3** | Add cross-platform dashboard integration (CISO Assistant + VerifyWise + CADRE metrics) | Low | ✅ Complete |
| **R2-S6.4** | Document feedback loop workflow in docs/feedback-loop.md | Medium | ✅ Complete |

### Sprint 7 — Live integration and automation (2026-07-27)

**Goal:** Implement actual live API integrations and automated remediation

| ID | Item | Priority |
|----|------|----------|
| **R2-S7.1** | Implement actual Elasticsearch Python client for live SIEM integration | High |
| **R2-S7.2** | Implement CISO Assistant REST API client for live risk push | Medium |
| **R2-S7.3** | Implement VerifyWise REST API client for live AI risk push | Medium |
| **R2-S7.4** | Integrate feedback JSON with Ansible playbooks on AST-013 for automated remediation | High |
| **R2-S7.5** | Add approval workflow for critical remediation actions | Medium |
| **R2-S7.6** | Implement rollback capabilities for automated remediation | Low |

### Explicitly deferred

- Full 55–65 exercise stubs from v1 PLAN  
- Blocking DFIR-Nexus / RevAI public releases on Risk  
- Live Elastic / Velociraptor API pulls as MVP requirement (Sprint 5 optional adapters preferred)  

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
| **M2** | Sprint 2 GRC sinks + Domain 2–7 exercise expansion | Domains 3–7; use Risk memos as essay/communication drill |
| **M3** | Sprint 3 polish + mock board brief | Weak-domain review + full practice exams |

---

## 7. Target layout (after Sprint 1 + Sprint 2 Docker)

```text
Risk/
├── README.md
├── plan_v2.md              ← THIS FILE (execution SSoT)
├── CHECKLIST.md            ← flip statuses here first
├── docker/                 ← Sprint 2 GRC sinks
│   ├── ciso-compose.yml
│   ├── verifywise-compose.yml
│   └── README.md           ← bring-up guide
├── docs/
│   ├── PLAN.md             ← v1 archive / reference
│   ├── grc-sinks.md
│   ├── ciso-notes.md
│   ├── verifywise-notes.md
│   ├── enterprise-context.md
│   ├── risk-register-baseline.md
│   ├── exercises/          ← R-EX-001…
│   └── examples/
├── config/
│   ├── asset-inventory.csv
│   └── risk-mapping.yml
├── samples/findings/
├── src/
│   ├── ingest.py
│   ├── risk_engine.py
│   ├── board_report.py
│   └── adapters/           ← optional live adapters
├── scripts/                ← ciso-up / verifywise-up + seed
├── tests/
└── artifacts/              ← generated board memos (gitignored)
```

---

## 8. Immediate next action

Sprint 2 GRC sinks (**CISO Assistant** + **VerifyWise**) are **done**. Eramba is **gone** from the tree.

**Practice anytime** (bring stacks back up after Docker Desktop restart — `down -v` wiped volumes):

1. Classic GRC — [`docs/ciso-notes.md`](docs/ciso-notes.md)  
2. AI governance — [`docs/verifywise-notes.md`](docs/verifywise-notes.md)

---

*Plan v2 — 2026-07-12; CISO/VerifyWise sinks 2026-07-13; Eramba removed 2026-07-13. CISSP exam ≈ 3 months; Risk supports Domain 1–2 (+ AI gov Domain 3/8) without replacing book study.*
