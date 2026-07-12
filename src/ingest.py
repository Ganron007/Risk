"""Load CADRE-Risk unified finding JSON files (and optional Praxis SARIF sidecar)."""

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
    """Load all *.json finding objects; skip *.sarif and non-finding JSON."""
    findings: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        if "id" in data and "source" in data and "asset_id" in data:
            findings.append(load_finding(path))
    return findings
