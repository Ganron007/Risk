"""Generate a Markdown board risk memo from scored sample findings or live SIEM data."""

from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .ingest import load_findings_dir
from .risk_engine import score_findings

REPO_ROOT = Path(__file__).resolve().parents[1]

# Configuration flag for real-time mode
# Set SIEM_MODE=live to fetch from live SIEM, SIEM_MODE=frozen (default) for samples
SIEM_MODE = os.getenv("SIEM_MODE", "frozen")


def fetch_live_siem_alerts(
    siem_url: str = "http://127.0.0.1:9200",
    index: str = "logs-system.security-*",
    query: dict[str, Any] | None = None,
    *,
    api_key: str | None = None,
    username: str | None = None,
    password: str | None = None,
    lookback_hours: int = 24,
) -> list[dict[str, Any]]:
    """Fetch alerts from live Elastic SIEM via REST API.
    
    Uses Elasticsearch Python client with proper authentication and error handling.
    Falls back to sample data if connection fails or in frozen mode.
    """
    if SIEM_MODE != "live":
        return []
    
    try:
        from elasticsearch import Elasticsearch
        from elasticsearch.exceptions import ConnectionError, AuthenticationException, RequestError
    except ImportError:
        print("Elasticsearch Python client not installed. Install with: pip install elasticsearch")
        return []
    
    # Build Elasticsearch client
    client_config = {"hosts": [siem_url]}
    
    if api_key:
        client_config["api_key"] = api_key
    elif username and password:
        client_config["basic_auth"] = (username, password)
    
    try:
        es = Elasticsearch(**client_config)
        
        # Test connection
        if not es.ping():
            print(f"Failed to connect to Elasticsearch at {siem_url}")
            return []
        
        # Build query for security alerts in lookback window
        from datetime import datetime, timedelta, timezone
        
        now = datetime.now(timezone.utc)
        lookback = now - timedelta(hours=lookback_hours)
        
        if query is None:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"range": {"@timestamp": {"gte": lookback.isoformat(), "lte": now.isoformat()}}},
                            {"exists": {"field": "event.severity"}},
                        ]
                    }
                },
                "sort": [{"@timestamp": {"order": "desc"}}],
                "size": 100,
            }
        
        # Execute search
        response = es.search(index=index, body=query)
        
        # Extract hits
        alerts = []
        for hit in response.get("hits", {}).get("hits", []):
            source = hit.get("_source", {})
            alerts.append({
                "_id": hit.get("_id"),
                "_index": hit.get("_index"),
                "_source": source,
            })
        
        print(f"Fetched {len(alerts)} alerts from {siem_url}/{index}")
        return alerts
        
    except ConnectionError as e:
        print(f"Connection error to Elasticsearch: {e}")
        return []
    except AuthenticationException as e:
        print(f"Authentication error to Elasticsearch: {e}")
        return []
    except RequestError as e:
        print(f"Request error to Elasticsearch: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching SIEM alerts: {e}")
        return []


def convert_siem_alert_to_finding(alert: dict[str, Any]) -> dict[str, Any]:
    """Convert a raw SIEM alert to unified finding format."""
    return {
        "id": f"siem-{alert.get('_id', 'unknown')}",
        "source": "elastic",
        "severity": alert.get("_source", {}).get("severity", "medium"),
        "title": alert.get("_source", {}).get("title", "SIEM Alert"),
        "description": alert.get("_source", {}).get("description", ""),
        "asset_id": alert.get("_source", {}).get("asset_id", "AST-UNKNOWN"),
        "discovered_at": alert.get("_source", {}).get("@timestamp", datetime.now(timezone.utc).isoformat()),
        "evidence": f"SIEM index: {alert.get('_index', 'unknown')}",
        "likelihood": alert.get("_source", {}).get("likelihood", 2),
        "impact": alert.get("_source", {}).get("impact", 2),
        "raw": alert,
    }


def render_memo(
    scored,
    title: str | None = None,
    *,
    data_source: str = "frozen sample findings",
) -> str:
    today = date.today().isoformat()
    title = title or f"Cadre Corp — Quarterly Risk Memo ({today})"
    lines = [
        f"# {title}",
        "",
        f"**Date:** {today}  ",
        "**Prepared for:** Board / CEO  ",
        "**Prepared by:** CISO (CADRE-Risk Sprint 1 tooling)  ",
        "",
        "## Executive summary",
        "",
        f"This memo scores **{data_source}** from CADRE labs "
        "(DarkAI, Praxis, RevAI, Elastic, Velociraptor) using likelihood × impact. "
        "ALE bands are **illustrative** for CISSP Domain 1 practice — not audited financials.",
        "",
        f"**Findings scored:** {len(scored)}  ",
        f"**Critical/High (score ≥ 6):** {sum(1 for s in scored if s.score >= 6)}  ",
        "",
        "## Top risks",
        "",
        "| Rank | Score | Band | Finding | Asset | Treatment |",
        "|------|-------|------|---------|-------|-----------|",
    ]
    for i, s in enumerate(scored, 1):
        lines.append(
            f"| {i} | {s.score} | {s.band} | {s.title} | {s.asset_id} | {s.treatment} |"
        )
    lines.extend(
        [
            "",
            "## Detail",
            "",
        ]
    )
    for s in scored:
        lines.extend(
            [
                f"### {s.finding_id} — {s.title}",
                "",
                f"- **Source:** {s.source}",
                f"- **Asset:** {s.asset_id}",
                f"- **L×I:** {s.likelihood} × {s.impact} = **{s.score}** ({s.band})",
                f"- **Treatment:** {s.treatment}",
                f"- **ALE band (illustrative):** {s.ale_band}",
                f"- **Related register ID:** {s.related_risk_id or '—'}",
                f"- **Evidence:** `{s.evidence}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Appetite check",
            "",
            "Per Cadre Corp risk appetite: Critical/High items on Restricted assets "
            "(identity plane, client evidence) require mitigate/remediate — not silent accept. "
            "Research-lab items may be accepted only with isolation controls.",
            "",
            "## Ask of the board",
            "",
            "1. Confirm treatment owners for score ≥ 6 items.",
            "2. Reaffirm zero tolerance for GDPR/SOC 2 process failures.",
            "3. Accept residual lab malware-handling risk only with AST-035 isolation intact.",
            "",
            "---",
            "",
            "*Generated by `python -m src.board_report`*",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CADRE-Risk board memo generator")
    parser.add_argument(
        "--samples",
        type=Path,
        default=REPO_ROOT / "samples" / "findings",
        help="Directory of unified finding JSON files (frozen mode)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "artifacts" / "board-memo.md",
        help="Output Markdown path",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Enable live SIEM mode (requires SIEM_MODE=live env var)",
    )
    parser.add_argument(
        "--siem-url",
        type=str,
        default="http://127.0.0.1:9200",
        help="Elasticsearch URL for live SIEM mode",
    )
    parser.add_argument(
        "--siem-index",
        type=str,
        default="logs-system.security-*",
        help="Elasticsearch index pattern for live SIEM mode",
    )
    parser.add_argument(
        "--lookback-hours",
        type=int,
        default=24,
        help="Hours to look back for SIEM alerts in live mode",
    )
    parser.add_argument(
        "--siem-api-key",
        type=str,
        default=None,
        help="Elasticsearch API key for authentication",
    )
    parser.add_argument(
        "--siem-username",
        type=str,
        default=None,
        help="Elasticsearch username for basic auth",
    )
    parser.add_argument(
        "--siem-password",
        type=str,
        default=None,
        help="Elasticsearch password for basic auth",
    )
    args = parser.parse_args(argv)
    
    # Determine data source
    if args.live or SIEM_MODE == "live":
        print("Fetching live SIEM alerts...")
        alerts = fetch_live_siem_alerts(
            siem_url=args.siem_url,
            index=args.siem_index,
            lookback_hours=args.lookback_hours,
            api_key=args.siem_api_key,
            username=args.siem_username,
            password=args.siem_password,
        )
        findings = [convert_siem_alert_to_finding(alert) for alert in alerts]
        if not findings:
            print("No live SIEM alerts found, falling back to sample data")
            findings = load_findings_dir(args.samples)
    else:
        print("Using frozen sample data...")
        findings = load_findings_dir(args.samples)
    
    if not findings:
        raise SystemExit(f"No findings found (tried live SIEM and {args.samples})")
    
    scored = score_findings(findings)
    live_mode = args.live or SIEM_MODE == "live"
    text = render_memo(scored, data_source="live SIEM alerts" if live_mode else "frozen sample findings")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"Wrote {args.out} ({len(scored)} findings, mode={'live' if live_mode else 'frozen'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
