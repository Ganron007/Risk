# Risk

<p align="center">
  <img src="assets/risk-logo.svg" alt="Risk Logo" width="620">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Python-%E2%89%A53.11-blue.svg" alt="Python: >=3.11">
  <img src="https://img.shields.io/badge/CISSP-87%20exercises-blue.svg" alt="CISSP: 87 exercises">
  <img src="https://img.shields.io/badge/Status-Work%20in%20Progress-yellow.svg" alt="Status: Work in Progress">
</p>

Part of the [CADRE](https://github.com/Ganron007/CADRE) platform — hands-on GRC and CISSP risk practice against a real AD / SOC estate.

> [!NOTE]
> **Work in progress.** Risk is an active lab — Markdown registers are complete enough to practice, and **two live GRC tools** (CISO Assistant + VerifyWise) are wired as optional UI sinks. Expect APIs, seeds, and dashboards to keep evolving.

---

## What is Risk?

**Risk** turns security-tool findings into scored risks, board-ready language, and optional GRC UI demos. Markdown registers are the source of truth; Docker GRC tools are optional sinks for practice — not a production GRC suite.

| Layer | What you get |
|-------|----------------|
| **Enterprise context** | Cadre Corp profile, asset inventory, risk appetite, control register |
| **CISSP practice** | 87 domain exercises (Domains 1–8) tied to lab findings and interview talking points |
| **Tooling** | Score findings → board memo; push to CISO Assistant / VerifyWise when you want a UI |

**Design rules:** findings-first (every scored risk cites sample or tool output) · no secrets in git · Markdown stands alone if every Docker UI is down.

---

## Active GRC tooling (optional UIs)

Two third-party GRC products run in Docker as **live practice sinks**. Markdown remains the source of truth — these UIs show the same Cadre Corp baseline in classic GRC and AI-governance form.

| | Product | Focus | Lab UI | Practice |
|---|---------|--------|--------|----------|
| <img src="assets/grc/ciso-assistant.svg" alt="" width="28" height="28"> | **[CISO Assistant](https://github.com/intuitem/ciso-assistant-community)** | Classic GRC — ISO 27001, SOC 2, NIST CSF, GDPR → CADRE main lab | http://localhost:8080 | [`docs/ciso-notes.md`](docs/ciso-notes.md) |
| <img src="assets/grc/verifywise.svg" alt="" width="28" height="28"> | **[VerifyWise](https://github.com/verifywise-ai/verifywise)** | AI governance — EU AI Act, ISO 42001, model inventory → DarkAI | http://127.0.0.1:18080 | [`docs/verifywise-notes.md`](docs/verifywise-notes.md) |

### CISO Assistant — classic GRC

Lab: **http://localhost:8080** · Seed: `.\scripts\ciso-seed-baseline.ps1`

![Cadre Corp Baseline Risk Register in CISO Assistant](docs/img/ciso-risk-register.png)

### VerifyWise — AI governance

Lab: **http://127.0.0.1:18080** · Seed: `.\scripts\verifywise-seed-baseline.ps1`

![Cadre Corp AI risks in VerifyWise](docs/img/verifywise-ai-risk.png)

Run **one stack at a time** on constrained hosts — see [`docker/README.md`](docker/README.md).

---

## Architecture

```text
CADRE tool outputs (Zeek, Suricata, Nexus, Ansible, Velociraptor, …)
        │
        ▼
 adapters → ingest → dedupe → risk_engine
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                   CISO Assistant              VerifyWise
                   (classic GRC)               (AI governance)
                         │                         │
                         └────────────┬────────────┘
                                      ▼
                         feedback → approval → ansible (optional)
                                      │
                                      ▼
                              board_report / cross_platform
```

| Module | Role |
|--------|------|
| `adapters` | SARIF / JSON / JSONL → unified findings (Praxis, RevAI, DarkAI, …) |
| `risk_engine` | 3×3 likelihood × impact scoring |
| `board_report` | Executive memo from frozen samples or live SIEM |
| `cross_platform` | Unified CISO + VerifyWise view |
| `approval_workflow` | Human gate for critical remediation proposals |
| `ansible_integration` | Dry-run / generate remediation playbooks |

---

## Quickstart

```powershell
pip install pyyaml pytest requests elasticsearch
pytest tests/ -q

# Board memo — no Docker required
python -m src.board_report --samples samples/findings --out artifacts/board-memo.md

# Optional: live SIEM
$env:SIEM_MODE = "live"
python -m src.board_report --live --siem-url http://127.0.0.1:9200 `
  --siem-index logs-system.security-* --out artifacts/board-memo-live.md

# Optional: GRC UIs (one at a time)
.\scripts\ciso-up.ps1
.\scripts\ciso-seed-baseline.ps1      # needs CISO Assistant PAT

.\scripts\verifywise-up.ps1
.\scripts\verifywise-seed-baseline.ps1
```

Seeded VerifyWise login and credentials are documented in [`docs/verifywise-notes.md`](docs/verifywise-notes.md) — not repeated here.

---

## Portfolio artifacts

| Artifact | Path |
|----------|------|
| Enterprise context | [`docs/enterprise-context.md`](docs/enterprise-context.md) |
| Risk appetite | [`docs/risk-appetite-statement.md`](docs/risk-appetite-statement.md) |
| Risk register (18) | [`docs/risk-register-baseline.md`](docs/risk-register-baseline.md) |
| Control register | [`docs/control-register.md`](docs/control-register.md) |
| Board memo sample | [`docs/examples/board-memo-sample.md`](docs/examples/board-memo-sample.md) |
| CISSP exercises (87) | [`docs/exercises/`](docs/exercises/) · map: [`EXERCISE-MAP.md`](docs/exercises/EXERCISE-MAP.md) |
| Feedback loop | [`docs/feedback-loop.md`](docs/feedback-loop.md) |
| GRC sink hub | [`docs/grc-sinks.md`](docs/grc-sinks.md) |

---

## License

MIT — same as the rest of the CADRE platform.

**CISO Assistant** and **VerifyWise** are third-party products (their licenses apply). VerifyWise is BSL 1.1 upstream. Marks under `assets/grc/` — see [`assets/grc/README.md`](assets/grc/README.md).
