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


def sarif_to_ciso_finding(
    sarif_path: Path,
    *,
    asset_id: str = "AST-035",
    risk_id: str = "RISK-013",
    likelihood: int = 2,
    impact: int = 2,
) -> dict[str, Any]:
    """Convert Praxis SARIF to CISO Assistant finding format for classic GRC."""
    findings = sarif_to_findings(sarif_path, asset_id=asset_id)
    
    if not findings:
        raise ValueError("No SARIF findings detected")
    
    # Aggregate findings into a single CISO Assistant finding
    high_count = sum(1 for f in findings if f.get("severity") == "high")
    medium_count = sum(1 for f in findings if f.get("severity") == "medium")
    
    return {
        "id": f"ciso-sarif-{sarif_path.stem}",
        "source": "praxis",
        "severity": "high" if high_count > 0 else "medium",
        "title": f"Praxis SAST scan: {len(findings)} findings detected ({high_count} high, {medium_count} medium)",
        "description": f"Praxis static analysis scan of {sarif_path.name} detected {len(findings)} security findings. High-severity findings include hardcoded secrets, vulnerable dependencies, or OWASP Top 10 anti-patterns. Requires review before CI/CD promotion.",
        "asset_id": asset_id,
        "discovered_at": _now(),
        "evidence": str(sarif_path).replace("\\", "/"),
        "likelihood": likelihood,
        "impact": impact,
        "mitre": ["T1059.006", "T1190"],  # Common SAST-related MITRE techniques
        "related_risk_id": risk_id,
        "raw": {
            "sarif_file": str(sarif_path),
            "total_findings": len(findings),
            "high_severity_count": high_count,
            "medium_severity_count": medium_count,
            "findings": findings[:10],  # Include first 10 findings for context
        },
    }


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


def revai_verdict_to_verifywise_usecase(
    path: Path,
    *,
    project_id: int = 2,
    owner_id: int = 2,
    framework_id: int = 1,
) -> dict[str, Any]:
    """Convert RevAI verdict to VerifyWise Project (use case) format for AI governance."""
    data = json.loads(path.read_text(encoding="utf-8"))
    raw = data.get("raw", data)
    verdict = raw.get("verdict", data.get("verdict", "unknown"))
    family = raw.get("family", data.get("family", "unknown"))
    score = int(raw.get("score", data.get("score", 50)))
    
    # Map verdict to EU AI Act classification
    ai_risk_classification = "High risk" if verdict == "malicious" else "Limited risk"
    type_of_high_risk_role = "Provider" if verdict == "malicious" else "Deployer"
    
    return {
        "project_title": f"RevAI malware analysis: {family}",
        "owner": owner_id,
        "start_date": data.get("discovered_at", _now())[:10],
        "geography": 1,  # Default geography ID
        "target_industry": "Malware analysis / DFIR research",
        "description": f"RevAI automated reverse engineering pipeline analyzed sample as {family} ({verdict}, score {score}). Pipeline includes static analysis, deep dive, and YARA generation. Handling requires isolation controls.",
        "ai_risk_classification": ai_risk_classification,
        "type_of_high_risk_role": type_of_high_risk_role,
        "goal": "Automated malware triage and signature generation for forensic investigations",
        "members": [owner_id],
        "framework": [framework_id],
        "enable_ai_data_insertion": False,
        "is_organizational": False,
        "evidence": {
            "source_file": str(path),
            "verdict": verdict,
            "family": family,
            "score": score,
            "sha256": raw.get("sha256", "unknown"),
        },
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


def darkai_jsonl_to_verifywise_risk(
    path: Path,
    *,
    project_id: int = 1,
    risk_owner_id: int = 2,
    framework_id: int = 1,
) -> dict[str, Any]:
    """Convert DarkAI JSONL audit to VerifyWise ProjectRisk format for AI governance."""
    findings = darkai_jsonl_to_findings(path)
    if not findings:
        raise ValueError("No DarkAI findings detected in JSONL")
    
    # Aggregate findings into a single risk entry
    secret_reflected_count = sum(1 for f in findings if f.get("severity") == "high")
    total_findings = len(findings)
    
    # Map likelihood/severity to VerifyWise format
    likelihood = "Likely" if secret_reflected_count > 0 else "Possible"
    severity = "Major" if secret_reflected_count > 0 else "Moderate"
    
    return {
        "risk_name": f"DarkAI prompt injection audit ({total_findings} events detected)",
        "risk_owner": risk_owner_id,
        "risk_description": f"DarkAI JSONL audit detected {total_findings} prompt-related events, {secret_reflected_count} with secret reflection. Evidence from {path.name}. Events include prompt_audit and potential injection attempts on LLM endpoints.",
        "ai_lifecycle_phase": "Deployment & integration",
        "likelihood": likelihood,
        "severity": severity,
        "risk_severity": severity,
        "risk_category": ["Cybersecurity risk", "Data privacy risk"],
        "impact": f"Secret reflection events could expose lab credentials or API keys. {secret_reflected_count} high-severity events detected.",
        "mitigation_status": "Pending",
        "projects": [project_id],
        "frameworks": [framework_id],
        "approval_status": "Pending",
        "evidence": {
            "source_file": str(path),
            "total_findings": total_findings,
            "secret_reflected_count": secret_reflected_count,
            "findings": findings[:5],  # Include first 5 findings for context
        },
    }
