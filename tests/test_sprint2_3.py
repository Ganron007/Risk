from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.adapters import darkai_jsonl_to_findings, sarif_to_findings
from src.dedupe import dedupe_findings, fingerprint, merge_findings


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
    merged, n = merge_findings(
        [a],
        [{"id": "y", "title": "u", "source": "darkai", "asset_id": "AST-035", "evidence": "e2"}],
    )
    assert n == 1
    assert len(merged) == 2
    assert fingerprint(a).startswith("id:")
