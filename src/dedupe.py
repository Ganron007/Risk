"""Deduplicate findings / scored risks for re-ingest."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable


def fingerprint(finding: dict[str, Any]) -> str:
    """Stable fingerprint: prefer id, else hash of key fields."""
    if finding.get("id"):
        return f"id:{finding['id']}"
    payload = {
        "source": finding.get("source"),
        "title": finding.get("title"),
        "asset_id": finding.get("asset_id"),
        "evidence": finding.get("evidence"),
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
    return f"hash:{digest}"


def dedupe_findings(findings: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep first occurrence per fingerprint; later duplicates dropped."""
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for f in findings:
        fp = fingerprint(f)
        if fp in seen:
            continue
        seen.add(fp)
        out.append(f)
    return out


def merge_findings(
    existing: Iterable[dict[str, Any]],
    incoming: Iterable[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    """Merge incoming into existing; return (merged, new_count)."""
    merged = list(existing)
    seen = {fingerprint(f) for f in merged}
    new_count = 0
    for f in incoming:
        fp = fingerprint(f)
        if fp in seen:
            continue
        seen.add(fp)
        merged.append(f)
        new_count += 1
    return merged, new_count
