from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.adapters import darkai_jsonl_to_findings, sarif_to_findings
from src.dedupe import dedupe_findings, fingerprint, merge_findings
from src.eramba_client import ErambaClient, ErambaConfig
from src.eramba_export import parse_baseline_risks, write_assets_csv


def test_sarif_adapter():
    findings = sarif_to_findings(ROOT / "samples" / "findings" / "praxis-sarif-sample.sarif")
    assert len(findings) >= 1
    assert findings[0]["source"] == "praxis"
    assert "secret" in findings[0]["title"].lower() or "SARIF" in findings[0]["title"]


def test_darkai_jsonl_adapter():
    findings = darkai_jsonl_to_findings(ROOT / "samples" / "findings" / "darkai-audit-sample.jsonl")
    assert len(findings) == 2  # health line skipped


def test_dedupe():
    a = {"id": "x", "title": "t", "source": "darkai", "asset_id": "AST-035", "evidence": "e"}
    b = dict(a)
    assert len(dedupe_findings([a, b])) == 1
    merged, n = merge_findings([a], [{"id": "y", "title": "u", "source": "darkai", "asset_id": "AST-035", "evidence": "e2"}])
    assert n == 1
    assert len(merged) == 2
    assert fingerprint(a).startswith("id:")


def test_eramba_dry_run_push():
    cfg = ErambaConfig(
        base_url="https://example.test",
        edition="enterprise",
        user="api",
        password="x",
        api_prefix="/api",
        risks_path="/security-risks",
        assets_path="/assets",
        verify_tls=True,
    )
    client = ErambaClient(cfg, dry_run=True)
    out = client.push_scored_finding(
        {
            "finding_id": "f1",
            "title": "t",
            "source": "elastic",
            "asset_id": "AST-001",
            "score": 9,
            "likelihood": 3,
            "impact": 3,
            "treatment": "Remediate",
            "evidence": "e",
        }
    )
    assert out["dry_run"] is True
    assert out["method"] == "POST"


def test_eramba_ce_blocks_live():
    cfg = ErambaConfig(
        base_url="https://example.test",
        edition="ce",
        user="a",
        password="b",
        api_prefix="/api",
        risks_path="/r",
        assets_path="/a",
        verify_tls=True,
    )
    client = ErambaClient(cfg, dry_run=False)
    try:
        client.create_risk({"title": "x"})
        assert False, "expected RuntimeError"
    except RuntimeError as e:
        assert "Community" in str(e) or "enterprise" in str(e).lower()


def test_parse_baseline_and_export_assets(tmp_path):
    risks = parse_baseline_risks(ROOT / "docs" / "risk-register-baseline.md")
    assert len(risks) >= 18
    n = write_assets_csv(ROOT / "config" / "asset-inventory.csv", tmp_path / "assets.csv")
    assert n >= 20
