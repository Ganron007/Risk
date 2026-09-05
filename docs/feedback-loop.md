# CADRE-Risk Feedback Loop Workflow

> **How security findings flow from CADRE tools → risk scoring → lab feedback → board reporting**  
> Last updated: 2026-07-27

---

## Overview

The CADRE-Risk feedback loop connects security tool outputs to risk management, lab remediation, and executive reporting. This workflow enables:

1. **Tool output ingestion** from CADRE security tools (Praxis, RevAI, DarkAI, Velociraptor, Zeek, Suricata, Elastic)
2. **Risk scoring** using likelihood × impact matrix
3. **Platform integration** (CISO Assistant for classic GRC, VerifyWise for AI governance)
4. **Lab feedback** to trigger remediation actions in the CADRE environment
5. **Board reporting** for executive communication

---

## Architecture

```
CADRE Security Tools
       ↓
   Adapters (src/adapters.py)
       ↓
   Unified Findings (samples/findings/)
       ↓
   Risk Engine (src/risk_engine.py)
       ↓
   ┌──────────────┬──────────────┐
   ↓              ↓              ↓
CISO Assistant  VerifyWise   Lab Feedback
   (Classic GRC)  (AI Gov)    (Remediation)
   ↓              ↓              ↓
   CADRE          DarkAI        AST-013
   (Main Lab)     (AI Lab)      (Provisioning)
       ↓              ↓              ↓
   Board Report (src/board_report.py)
```

**Strategic Alignment:**
- **CISO Assistant** → Classic GRC (ISO 27001, SOC 2, NIST CSF) → Integrated with **CADRE main lab**
- **VerifyWise** → AI Governance (EU AI Act, ISO 42001, NIST AI RMF) → Integrated with **DarkAI project**

---

## Step 1: Tool Output Ingestion

### Supported Tools

| Tool | Output Format | Adapter Function | Use Case |
|------|--------------|-----------------|----------|
| **Praxis** | SARIF | `sarif_to_findings()` | SAST findings for CI/CD security gate |
| **RevAI** | JSON verdict | `revai_verdict_to_finding()` | Malware analysis verdicts |
| **DarkAI** | JSONL audit | `darkai_jsonl_to_findings()` | LLM prompt injection detection |
| **Velociraptor** | JSON | (direct ingest) | Forensic artifact collection |
| **Zeek** | JSON | (direct ingest) | Network telemetry (kerberos.log) |
| **Suricata** | JSON | (direct ingest) | Network alerts (eve.json) |
| **Elastic** | JSON | (direct ingest) | SIEM rule alerts |

### Sample Data Location

All sample findings are stored in `samples/findings/`:

- `praxis-sarif-sample.sarif` - SAST findings
- `revai-lumma-verdict.json` - Malware verdict
- `darkai-audit-sample.jsonl` - Prompt audit log
- `velociraptor-schtask.json` - Scheduled task detection
- `zeek-kerberos.json` - Kerberoast telemetry
- `suricata-smb-alert.json` - Lateral movement alert
- `elastic-dcsync-alert.json` - DCSync SIEM alert
- `nexus-audit-entry.json` - DFIR-Nexus audit chain
- `ansible-drift.json` - Configuration drift
- `velociraptor-artifact-result.json` - Full artifact results

---

## Step 2: Adapter Functions

### Unified Finding Format

All adapters convert tool-specific outputs to a unified finding format:

```json
{
  "id": "finding-unique-id",
  "source": "tool-name",
  "severity": "critical|high|medium|low",
  "title": "Human-readable title",
  "description": "Detailed description",
  "asset_id": "AST-XXX",
  "discovered_at": "2026-07-27T12:00:00Z",
  "evidence": "path/to/evidence",
  "likelihood": 1-3,
  "impact": 1-3,
  "mitre": ["TXXXX.XXX"],
  "related_risk_id": "RISK-XXX",
  "raw": { ... }
}
```

### Platform-Specific Adapters

#### CISO Assistant Integration

**Function:** `sarif_to_ciso_finding()`

Converts Praxis SARIF to CISO Assistant finding format for classic GRC (ISO 27001, SOC 2, NIST CSF).

```python
from src.adapters import sarif_to_ciso_finding

finding = sarif_to_ciso_finding(
    sarif_path=Path("samples/findings/praxis-sarif-sample.sarif"),
    asset_id="AST-035",
    risk_id="RISK-013",
    likelihood=2,
    impact=2
)
```

#### VerifyWise Integration

**Functions:** 
- `darkai_jsonl_to_verifywise_risk()` - DarkAI audit → AI risk
- `revai_verdict_to_verifywise_usecase()` - RevAI verdict → AI use case

Converts AI tool outputs to VerifyWise format for AI governance (EU AI Act, ISO 42001, NIST AI RMF).

```python
from src.adapters import darkai_jsonl_to_verifywise_risk, revai_verdict_to_verifywise_usecase

# DarkAI → AI risk
risk = darkai_jsonl_to_verifywise_risk(
    path=Path("samples/findings/darkai-audit-sample.jsonl"),
    project_id=1,
    risk_owner_id=2,
    framework_id=1
)

# RevAI → AI use case
usecase = revai_verdict_to_verifywise_usecase(
    path=Path("samples/findings/revai-lumma-verdict.json"),
    project_id=2,
    owner_id=2,
    framework_id=1
)
```

### Configuration Mode

Set `ADAPTER_MODE` environment variable:

- `ADAPTER_MODE=frozen` - Use static sample data only (default)
- `ADAPTER_MODE=live` - Process actual tool outputs from live CADRE environment

```bash
export ADAPTER_MODE=live
python -m src.board_report --live
```

---

## Step 3: Risk Scoring

### Risk Engine (src/risk_engine.py)

The risk engine scores findings using a 3×3 likelihood × impact matrix:

```
Impact →    1      2      3
Likelihood
    1      1      2      3
    2      2      4      6
    3      3      6      9
```

### Score Bands

| Score | Band | Treatment |
|-------|------|-----------|
| 1-2 | Low | Accept/monitor |
| 3-5 | Medium | Mitigate |
| 6-8 | High | Mitigate/transfer |
| 9 | Critical | Remediate immediately |

### Asset Classification Impact

Asset classification affects impact scoring:

- **Restricted** (client evidence, identity plane): impact = 3
- **Confidential** (internal systems): impact = 2
- **Internal** (lab infrastructure): impact = 1

### Usage

```python
from src.risk_engine import score_findings, generate_cadre_feedback

# Score findings find
scored = score_findings(findings)

# Generate lab feedback actions
feedback = generate_cadre_feedback(scored)
```

---

## Step 4: Lab Feedback Mechanism

### Feedback Actions

The `generate_cadre_feedback()` function creates actionable feedback for the CADRE lab:

**Critical Risks (score ≥ 9):**
- DCSync detection → `disable_account` on svc_mssql
- Persistence detection → `isolate_host`
- Secret leakage → `rotate_secret` (NEXUS_AUDIT_SECRET)

**High Risks (score 6-8):**
- Firewall issues → `review_firewall_rules`
- AD/Kerberos issues → `review_ad_configuration`

### Feedback Format

```json
{
  "generated_at": "2026-07-27T12:00:00Z",
  "total_risks": 10,
  "critical_count": 2,
  "high_count": 3,
  "actions": [
    {
      "action": "disable_account",
      "target": "svc_mssql",
      "reason": "Critical risk finding-elastic-001: DCSync detected",
      "priority": "immediate"
    },
    {
      "action": "isolate_host",
      "target": "AST-004",
      "reason": "Critical risk finding-vr-001: Scheduled task persistence",
      "priority": "immediate"
    }
  ]
}
```

### Integration Point

This feedback JSON can be sent to the CADRE provisioning VM (AST-013) via Ansible playbooks to trigger automated remediation.

---

## Step 5: Board Reporting

### Board Report Generator (src/board_report.py)

Generates executive-facing risk memos from scored findings.

### Modes

**Frozen Mode (default):**
```bash
python -m src.board_report
```
Uses static sample data from `samples/findings/`.

**Live Mode:**
```bash
export SIEM_MODE=live
python -m src.board_report --live --siem-url http://127.0.0.1:9200
```
Fetches alerts from live Elastic SIEM via REST API.

### Output

Generates Markdown memo at `artifacts/board-memo.md`:

```markdown
# Cadre Corp — Quarterly Risk Memo (2026-07-27)

**Date:** 2026-07-27
**Prepared for:** Board / CEO
**Prepared by:** CISO (CADRE-Risk Sprint 1 tooling)

## Executive summary

This memo scores **frozen sample findings** from CADRE labs...

**Findings scored:** 12
**Critical/High (score ≥ 6):** 5

## Top risks (from samples)

| Rank | Score | Band | Finding | Asset | Treatment |
|------|-------|------|---------|-------|-----------|
| 1 | 9 | Critical | Elastic alert: DCSync | AST-001 | Remediate immediately |
...
```

---

## Complete Workflow Example

### 1. Ingest Tool Outputs

```python
from src.adapters import sarif_to_findings, darkai_jsonl_to_findings
from pathlib import Path

# Praxis SAST
praxis_findings = sarif_to_findings(Path("samples/findings/praxis-sarif-sample.sarif"))

# DarkAI audit
darkai_findings = darkai_jsonl_to_findings(Path("samples/findings/darkai-audit-sample.jsonl"))

# Combine all findings
all_findings = praxis_findings + darkai_findings
```

### 2. Score Risks

```python
from src.risk_engine import score_findings, generate_cadre_feedback

scored = score_findings(all_findings)
for risk in scored:
    print(f"{risk.finding_id}: {risk.score} ({risk.band})")
```

### 3. Generate Lab Feedback

```python
feedback = generate_cadre_feedback(scored)
print(f"Actions to execute: {len(feedback['actions'])}")
for action in feedback['actions']:
    print(f"  - {action['action']} on {action['target']}")
```

### 4. Generate Board Report

```python
from src.board_report import render_memo

memo = render_memo(scored, title="Cadre Corp — Weekly Risk Update")
print(memo)
```

### 5. Platform Integration (Optional)

```python
# CISO Assistant
from src.adapters import sarif_to_ciso_finding
ciso_finding = sarif_to_ciso_finding(Path("samples/findings/praxis-sarif-sample.sarif"))

# VerifyWise
from src.adapters import darkai_jsonl_to_verifywise_risk
vw_risk = darkai_jsonl_to_verifywise_risk(Path("samples/findings/darkai-audit-sample.jsonl"))
```

---

## Configuration

### Environment Variables

| Variable | Values | Purpose |
|----------|--------|---------|
| `ADAPTER_MODE` | `frozen` (default), `live` | Adapter data source |
| `SIEM_MODE` | `frozen` (default), `live` | Board report data source |

### Configuration Files

- `config/risk-mapping.yml` - Source likelihood defaults, risk mapping
- `config/asset-inventory.csv` - Asset classifications (Restricted/Confidential/Internal)

---

## Next Steps

### R2-S6.3: Cross-Platform Dashboard Integration

- Create unified dashboard showing CISO Assistant + VerifyWise risks
- Implement real-time risk aggregation across platforms
- Add single-pane-of-glass for board visibility

### Live SIEM Integration

- Implement actual Elasticsearch Python client in `fetch_live_siem_alerts()`
- Add authentication via API keys
- Implement proper error handling and retry logic

### Automated Remediation

- Integrate feedback JSON with Ansible playbooks on AST-013
- Add approval workflow for critical remediation actions
- Implement rollback capabilities

---

*Last updated: 2026-07-27 — Sprint 4 feedback loop documentation*
