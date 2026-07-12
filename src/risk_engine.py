"""CADRE-Risk — score findings and emit board-facing risk language."""

from __future__ import annotations

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
