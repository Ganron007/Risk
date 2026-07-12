# Unified finding schema

> **Sprint 1:** R2-S1.10  
> Consumed by `src/ingest.py` and `src/risk_engine.py`.

## Required fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable finding ID |
| `source` | enum | `darkai` \| `praxis` \| `revai` \| `elastic` \| `velociraptor` \| `cadre_campaign` |
| `severity` | enum | `low` \| `medium` \| `high` \| `critical` |
| `title` | string | Short title |
| `description` | string | What happened |
| `asset_id` | string | AST-* from inventory |
| `discovered_at` | ISO-8601 | When observed |
| `evidence` | string | Path or locator to proof |

## Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `likelihood` | 1–3 | Override engine default |
| `impact` | 1–3 | Override classification-based default |
| `mitre` | string[] | Technique IDs |
| `raw` | object | Original tool payload |
| `related_risk_id` | string | Link to RISK-* if known |

## Example

```json
{
  "id": "cadre-finding-001",
  "source": "darkai",
  "severity": "high",
  "title": "Prompt injection leaked lab secret via /chat",
  "description": "STUB_INJECTABLE mode allowed override of system prompt.",
  "asset_id": "AST-035",
  "discovered_at": "2026-07-12T14:30:00Z",
  "evidence": "samples/findings/darkai-prompt-inject.json",
  "mitre": ["T1059"],
  "raw": {}
}
```

## Scoring defaults

- If `likelihood` omitted: use `config/risk-mapping.yml` `source_likelihood_defaults`.
- If `impact` omitted: map asset `classification` → Restricted=3, Confidential=2, Internal=1; bump +1 if severity is `critical` (cap 3).

---

*R2-S1.10 schema — 2026-07-12*
