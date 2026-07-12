"""Adapters: Praxis SARIF / RevAI-ish JSON / DarkAI JSONL → unified findings."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sarif_to_findings(
    sarif_path: Path,
    *,
    asset_id: str = "AST-035",
    source: str = "praxis",
) -> list[dict[str, Any]]:
    data = json.loads(sarif_path.read_text(encoding="utf-8"))
    findings: list[dict[str, Any]] = []
    for run_i, run in enumerate(data.get("runs", [])):
        for res_i, result in enumerate(run.get("results", [])):
            rule = result.get("ruleId", "unknown")
            level = (result.get("level") or "warning").lower()
            severity = {
                "error": "high",
                "warning": "medium",
                "note": "low",
                "none": "low",
            }.get(level, "medium")
            msg = result.get("message", {}).get("text", rule)
            loc = ""
            locs = result.get("locations") or []
            if locs:
                phys = locs[0].get("physicalLocation", {})
                art = phys.get("artifactLocation", {}).get("uri", "")
                line = phys.get("region", {}).get("startLine", "")
                loc = f"{art}:{line}"
            findings.append(
                {
                    "id": f"sarif-{sarif_path.stem}-{run_i}-{res_i}",
                    "source": source,
                    "severity": severity,
                    "title": f"SARIF {rule}: {msg[:80]}",
                    "description": msg,
                    "asset_id": asset_id,
                    "discovered_at": _now(),
                    "evidence": str(sarif_path).replace("\\", "/") + (f" ({loc})" if loc else ""),
                    "raw": result,
                }
            )
    return findings


def revai_verdict_to_finding(
    path: Path,
    *,
    asset_id: str = "AST-035",
) -> dict[str, Any]:
    """Accept either unified finding JSON or a raw-ish verdict blob."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if "source" in data and data.get("source") == "revai" and "asset_id" in data:
        return data
    raw = data.get("raw", data)
    verdict = raw.get("verdict", data.get("verdict", "unknown"))
    family = raw.get("family", data.get("family", "unknown"))
    score = int(raw.get("score", data.get("score", 50)))
    severity = "critical" if score >= 90 else "high" if score >= 70 else "medium"
    return {
        "id": data.get("id", f"revai-{path.stem}"),
        "source": "revai",
        "severity": severity,
        "title": data.get("title", f"RevAI verdict: {family} — {verdict} (score {score})"),
        "description": data.get(
            "description",
            f"Automated RE pipeline verdict={verdict} family={family} score={score}",
        ),
        "asset_id": data.get("asset_id", asset_id),
        "discovered_at": data.get("discovered_at", _now()),
        "evidence": data.get("evidence", str(path).replace("\\", "/")),
        "likelihood": 3 if severity == "critical" else 2,
        "impact": 2,
        "raw": raw,
    }


def darkai_jsonl_to_findings(
    path: Path,
    *,
    asset_id: str = "AST-035",
    secret_keys: tuple[str, ...] = ("secret_reflected", "injected", "prompt_injection"),
) -> list[dict[str, Any]]:
    """Scan JSONL audit lines; emit findings when risk-ish flags appear."""
    findings: list[dict[str, Any]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        flagged = any(obj.get(k) for k in secret_keys) or obj.get("event") == "prompt_audit"
        if not flagged:
            continue
        findings.append(
            {
                "id": f"darkai-jsonl-{path.stem}-{i}",
                "source": "darkai",
                "severity": "high" if obj.get("secret_reflected") else "medium",
                "title": f"DarkAI audit: {obj.get('event', 'event')} on {obj.get('path', '/')}",
                "description": json.dumps(obj)[:500],
                "asset_id": asset_id,
                "discovered_at": obj.get("ts", _now()),
                "evidence": f"{path.as_posix()}:{i+1}",
                "likelihood": 3 if obj.get("secret_reflected") else 2,
                "impact": 2,
                "raw": obj,
            }
        )
    return findings
