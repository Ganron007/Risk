from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ingest import load_findings_dir
from src.risk_engine import clamp, score_band, score_finding, score_findings


def test_clamp():
    assert clamp(0) == 1
    assert clamp(9) == 3
    assert clamp(2) == 2


def test_score_band():
    assert score_band(9) == "Critical"
    assert score_band(6) == "High"
    assert score_band(3) == "Medium"
    assert score_band(2) == "Low"


def test_score_explicit_li():
    finding = {
        "id": "t1",
        "source": "elastic",
        "severity": "critical",
        "title": "x",
        "description": "y",
        "asset_id": "AST-001",
        "discovered_at": "2026-01-01T00:00:00Z",
        "evidence": "e",
        "likelihood": 3,
        "impact": 3,
    }
    s = score_finding(finding)
    assert s.score == 9
    assert s.band == "Critical"
    assert "Remediate" in s.treatment


def test_impact_from_classification():
    finding = {
        "id": "t2",
        "source": "darkai",
        "severity": "medium",
        "title": "x",
        "description": "y",
        "asset_id": "AST-035",
        "discovered_at": "2026-01-01T00:00:00Z",
        "evidence": "e",
        "likelihood": 2,
    }
    s = score_finding(finding)
    assert s.impact == 1  # Internal
    assert s.score == 2


def test_load_and_score_samples():
    findings = load_findings_dir(ROOT / "samples" / "findings")
    assert len(findings) >= 5
    scored = score_findings(findings)
    assert scored[0].score >= scored[-1].score
    ids = {f["id"] for f in findings}
    assert "finding-elastic-001" in ids
    elastic = next(s for s in scored if s.finding_id == "finding-elastic-001")
    assert elastic.score == 9
