"""CADRE-Risk — score findings and emit board-facing risk language."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING = REPO_ROOT / "config" / "risk-mapping.yml"
DEFAULT_INVENTORY = REPO_ROOT / "config" / "asset-inventory.csv"

CLASSIFICATION_IMPACT = {
    "Restricted": 3,
    "Confidential": 2,
    "Internal": 1,
}

TREATMENT = {
    (1, 1): "Accept/monitor",
    (1, 2): "Accept/monitor",
    (1, 3): "Mitigate",
    (2, 1): "Accept/monitor",
    (2, 2): "Mitigate",
    (2, 3): "Mitigate/transfer",
    (3, 1): "Mitigate",
    (3, 2): "Mitigate/transfer",
    (3, 3): "Remediate immediately",
}

ALE_BAND = {
    1: "< $10K (illustrative)",
    2: "$10K–$50K (illustrative)",
    3: "$50K–$100K (illustrative)",
    4: "$50K–$200K (illustrative)",
    6: "$200K–$500K (illustrative)",
    9: "> $500K (illustrative)",
}


@dataclass
class ScoredRisk:
    finding_id: str
    title: str
    source: str
    asset_id: str
    likelihood: int
    impact: int
    score: int
    band: str
    treatment: str
    ale_band: str
    related_risk_id: str | None
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "title": self.title,
            "source": self.source,
            "asset_id": self.asset_id,
            "likelihood": self.likelihood,
            "impact": self.impact,
            "score": self.score,
            "band": self.band,
            "treatment": self.treatment,
            "ale_band": self.ale_band,
            "related_risk_id": self.related_risk_id,
            "evidence": self.evidence,
        }


def load_mapping(path: Path | None = None) -> dict[str, Any]:
    p = path or DEFAULT_MAPPING
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_asset_classifications(path: Path | None = None) -> dict[str, str]:
    p = path or DEFAULT_INVENTORY
    out: dict[str, str] = {}
    with p.open(encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        idx_id = header.index("asset_id")
        idx_cls = header.index("classification")
        for line in f:
            parts = line.strip().split(",")
            if len(parts) <= max(idx_id, idx_cls):
                continue
            out[parts[idx_id]] = parts[idx_cls]
    return out


def score_band(score: int) -> str:
    if score >= 9:
        return "Critical"
    if score >= 6:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


def clamp(n: int, lo: int = 1, hi: int = 3) -> int:
    return max(lo, min(hi, n))


def resolve_likelihood(finding: dict[str, Any], mapping: dict[str, Any]) -> int:
    if "likelihood" in finding and finding["likelihood"] is not None:
        return clamp(int(finding["likelihood"]))
    source = finding.get("source", "")
    defaults = mapping.get("source_likelihood_defaults", {})
    return clamp(int(defaults.get(source, 2)))


def resolve_impact(
    finding: dict[str, Any],
    asset_class: dict[str, str],
) -> int:
    if "impact" in finding and finding["impact"] is not None:
        return clamp(int(finding["impact"]))
    asset_id = finding.get("asset_id", "")
    classification = asset_class.get(asset_id, "Internal")
    impact = CLASSIFICATION_IMPACT.get(classification, 1)
    severity = (finding.get("severity") or "").lower()
    if severity == "critical":
        impact = clamp(impact + 1)
    return impact


def score_finding(
    finding: dict[str, Any],
    mapping: dict[str, Any] | None = None,
    asset_class: dict[str, str] | None = None,
) -> ScoredRisk:
    mapping = mapping or load_mapping()
    asset_class = asset_class or load_asset_classifications()
    likelihood = resolve_likelihood(finding, mapping)
    impact = resolve_impact(finding, asset_class)
    score = likelihood * impact
    treatment = TREATMENT.get((likelihood, impact), "Mitigate")
    return ScoredRisk(
        finding_id=str(finding.get("id", "unknown")),
        title=str(finding.get("title", "")),
        source=str(finding.get("source", "")),
        asset_id=str(finding.get("asset_id", "")),
        likelihood=likelihood,
        impact=impact,
        score=score,
        band=score_band(score),
        treatment=treatment,
        ale_band=ALE_BAND.get(score, ALE_BAND.get(6, "illustrative")),
        related_risk_id=finding.get("related_risk_id"),
        evidence=str(finding.get("evidence", "")),
    )


def score_findings(findings: list[dict[str, Any]]) -> list[ScoredRisk]:
    mapping = load_mapping()
    asset_class = load_asset_classifications()
    scored = [score_finding(f, mapping, asset_class) for f in findings]
    return sorted(scored, key=lambda s: (-s.score, s.finding_id))


def generate_cadre_feedback(scored_risks: list[ScoredRisk]) -> dict[str, Any]:
    """Generate CADRE lab feedback actions based on scored risks.
    
    This creates actionable feedback that can be sent to the CADRE lab environment
    to trigger remediation, configuration changes, or alerts.
    """
    feedback_actions = []
    
    for risk in scored_risks:
        if risk.score >= 9:  # Critical risks
            if "DCSync" in risk.title or "4662" in risk.evidence:
                feedback_actions.append({
                    "action": "disable_account",
                    "target": "svc_mssql",
                    "reason": f"Critical risk {risk.finding_id}: {risk.title}",
                    "priority": "immediate",
                })
            elif "scheduled task" in risk.title.lower() or "persistence" in risk.title.lower():
                feedback_actions.append({
                    "action": "isolate_host",
                    "target": risk.asset_id,
                    "reason": f"Critical risk {risk.finding_id}: {risk.title}",
                    "priority": "immediate",
                })
            elif "prompt injection" in risk.title.lower() or "secret" in risk.title.lower():
                feedback_actions.append({
                    "action": "rotate_secret",
                    "target": "NEXUS_AUDIT_SECRET",
                    "reason": f"Critical risk {risk.finding_id}: {risk.title}",
                    "priority": "immediate",
                })
        elif risk.score >= 6:  # High risks
            if "firewall" in risk.title.lower() or "network" in risk.title.lower():
                feedback_actions.append({
                    "action": "review_firewall_rules",
                    "target": risk.asset_id,
                    "reason": f"High risk {risk.finding_id}: {risk.title}",
                    "priority": "high",
                })
            elif "kerberos" in risk.title.lower() or re.search(r"\bad\b", risk.title, re.IGNORECASE):
                feedback_actions.append({
                    "action": "review_ad_configuration",
                    "target": "domain_controllers",
                    "reason": f"High risk {risk.finding_id}: {risk.title}",
                    "priority": "high",
                })
    
    return {
        "generated_at": _now(),
        "total_risks": len(scored_risks),
        "critical_count": sum(1 for r in scored_risks if r.score >= 9),
        "high_count": sum(1 for r in scored_risks if 6 <= r.score < 9),
        "actions": feedback_actions,
    }


def main(argv: list[str] | None = None) -> int:
    """CLI: score sample findings and write the CADRE feedback JSON.

    This bridges the loop: score_findings → generate_cadre_feedback → file,
    which feeds src.approval_workflow / src.ansible_integration (--feedback).
    """
    import argparse

    from .ingest import load_findings_dir

    parser = argparse.ArgumentParser(description="CADRE-Risk feedback generator")
    parser.add_argument(
        "--samples",
        type=Path,
        default=REPO_ROOT / "samples" / "findings",
        help="Directory of unified finding JSON files",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "artifacts" / "feedback.json",
        help="Output feedback JSON path",
    )
    args = parser.parse_args(argv)

    findings = load_findings_dir(args.samples)
    if not findings:
        raise SystemExit(f"No findings found in {args.samples}")
    scored = score_findings(findings)
    feedback = generate_cadre_feedback(scored)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(feedback, f, indent=2)
        f.write("\n")
    print(f"Wrote {args.out} ({feedback['total_risks']} risks, {len(feedback['actions'])} actions)")
    return 0


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    import sys
    sys.exit(main())
