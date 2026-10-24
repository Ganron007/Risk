"""Load CADRE-Risk unified finding JSON files and Praxis SARIF sidecars."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_finding(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    required = ("id", "source", "severity", "title", "description", "asset_id", "discovered_at", "evidence")
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"{path}: missing fields {missing}")
    return data


def load_findings_dir(directory: Path) -> list[dict[str, Any]]:
    """Load unified finding JSON objects; convert uncited SARIF sidecars.

    - ``*.json``: validated as unified findings (8 required fields).
    - ``*.sarif``: converted via ``adapters.sarif_to_findings`` — unless a loaded
      JSON finding already cites that SARIF file in its ``evidence`` field, in
      which case the hand-written JSON stand-in is treated as the canonical
      record (prevents double-counting the same alert).
    - ``*.jsonl`` is intentionally NOT auto-loaded: DarkAI audit lines need the
      explicit adapter (``adapters.darkai_jsonl_to_findings``), which applies
      its own asset defaults and flag rules.
    """
    findings: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        if "id" in data and "source" in data and "asset_id" in data:
            findings.append(load_finding(path))

    for sarif_path in sorted(directory.glob("*.sarif")):
        sarif_name = sarif_path.name
        if any(sarif_name in str(f.get("evidence", "")) for f in findings):
            continue  # already represented by a unified JSON stand-in
        from .adapters import sarif_to_findings

        findings.extend(sarif_to_findings(sarif_path))

    return findings
