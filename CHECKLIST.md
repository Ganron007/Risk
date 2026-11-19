# CADRE-Risk — Checklist

> **SSoT for status.** Flip here first. **Plan:** [`docs/plan_v2.md`](docs/plan_v2.md)  
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

## Sprint 4 — Exercise quality standardization (2026-07-27)

| ID | Item | Status | Priority | Notes |
|----|------|--------|----------|-------|
| R2-S4.1 | Audit all 87 CISSP exercises for full format consistency | [x] | High | 100% complete - all follow full format; see docs/exercise-quality-audit.md |
| R2-S4.2 | Upgrade Domains 2-8 exercises to match Domain 1 quality standard | [x] | High | Not required - Domains 2-8 already at quality standard |
| R2-S4.3 | Add campaign-phase mapping to EXERCISE-MAP.md | [x] | Medium | Campaign phase column added; Phase 2/3 mapped to relevant exercises |
| R2-S4.4 | Expand samples/findings/ with real CADRE tool outputs | [x] | Medium | Added Zeek, Suricata, Nexus, Ansible, Velociraptor samples |

## Sprint 5 — Live adapter integration (2026-07-27)

| ID | Item | Status | Priority | Notes |
|----|------|--------|----------|-------|
| R2-S5.1 | Implement DarkAI JSONL → VerifyWise AI risk adapter | [x] | Medium | `darkai_jsonl_to_verifywise_risk()` in src/adapters.py |
| R2-S5.2 | Implement RevAI verdict → VerifyWise AI use-case adapter | [x] | Medium | `revai_verdict_to_verifywise_usecase()` in src/adapters.py |
| R2-S5.3 | Implement Praxis SARIF → CISO Assistant finding adapter | [x] | Medium | `sarif_to_ciso_finding()` in src/adapters.py |
| R2-S5.4 | Add adapter configuration flag (frozen vs live mode) | [~] | Low | ADAPTER_MODE removed (dead code, F15); adapters are pure functions; live push via cross_platform.py |

## Sprint 6 — Feedback loop and integration (2026-07-27)

| ID | Item | Status | Priority | Notes |
|----|------|--------|----------|-------|
| R2-S6.1 | Create Risk → CADRE feedback mechanism | [x] | High | `generate_cadre_feedback()` in src/risk_engine.py |
| R2-S6.2 | Implement real-time board memo generation from live SIEM data | [x] | Medium | `fetch_live_siem_alerts()` + `--live` flag in src/board_report.py |
| R2-S6.3 | Add cross-platform dashboard integration | [x] | Low | src/cross_platform.py - unified CISO + VerifyWise view |
| R2-S6.4 | Document feedback loop workflow in docs/feedback-loop.md | [x] | Medium | Complete workflow documentation |

## Sprint 7 — Live integration and automation (2026-07-27)

**Strategic focus:** CISO Assistant → CADRE main lab, VerifyWise → DarkAI project

| ID | Item | Status | Priority | Notes |
|----|------|--------|----------|-------|
| R2-S7.1 | Implement actual Elasticsearch Python client for live SIEM integration | [x] | High | Elasticsearch client in src/board_report.py with auth support |
| R2-S7.2 | Implement CISO Assistant REST API client for live risk push (CADRE main lab) | [~] | Medium | `fetch_ciso_risks()` + `push_risk_to_ciso()` in src/cross_platform.py (frozen verified; live push pending running stack) |
| R2-S7.3 | Implement VerifyWise REST API client for live AI risk push (DarkAI project) | [~] | Medium | `fetch_verifywise_risks()` + `push_risk_to_verifywise()` in src/cross_platform.py (frozen verified; live push pending running stack) |
| R2-S7.4 | Integrate feedback JSON with Ansible playbooks on AST-013 for automated remediation | [x] | High | src/ansible_integration.py - feedback → tasks → playbook → execution |
| R2-S7.5 | Add approval workflow for critical remediation actions | [x] | Medium | src/approval_workflow.py - human-in-the-loop for critical actions |
| R2-S7.6 | Implement rollback capabilities for automated remediation | [x] | Low | `generate_rollback_playbook()` in src/ansible_integration.py |

## Tests

| Suite | Status |
|-------|--------|
| `pytest tests/` | **24 passed** (2026-11-19) |

---

## Practice (re-run anytime)

1. **CISO Assistant:** [`docs/ciso-notes.md`](docs/ciso-notes.md) — `ciso-up` → PAT → `ciso-seed-baseline` → UI  
2. **VerifyWise:** [`docs/verifywise-notes.md`](docs/verifywise-notes.md) — `verifywise-up` → `verifywise-seed-baseline` → UI as `org-admin@cadre.local`

---

*Last updated: 2026-10-24 - Batches A-D complete; v0.1.0 released*
