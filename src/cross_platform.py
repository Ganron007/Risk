"""Cross-platform dashboard integration for CISO Assistant + VerifyWise unified risk view."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]

# Configuration flags
# Set CISO_MODE=frozen to use sample data, CISO_MODE=live for API calls
# Set VW_MODE=frozen to use sample data, VW_MODE=live for API calls
CISO_MODE = os.getenv("CISO_MODE", "frozen")
VW_MODE = os.getenv("VW_MODE", "frozen")


@dataclass
class UnifiedRisk:
    """Unified risk representation across CISO Assistant and VerifyWise."""
    id: str
    source: str  # "ciso" or "verifywise"
    title: str
    description: str
    severity: str  # "critical", "high", "medium", "low"
    likelihood: int
    impact: int
    score: int
    band: str
    treatment: str
    category: str  # "classic_grc" or "ai_governance"
    framework: list[str]  # ["ISO 27001", "SOC 2", "NIST CSF"] or ["EU AI Act", "ISO 42001"]
    created_at: str
    updated_at: str
    raw: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "likelihood": self.likelihood,
            "impact": self.impact,
            "score": self.score,
            "band": self.band,
            "treatment": self.treatment,
            "category": self.category,
            "framework": self.framework,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _score_band(score: int) -> str:
    if score >= 9:
        return "Critical"
    if score >= 6:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


def _treatment_from_score(score: int) -> str:
    if score >= 9:
        return "Remediate immediately"
    if score >= 6:
        return "Mitigate/transfer"
    if score >= 3:
        return "Mitigate"
    return "Accept/monitor"


def _coerce_score(value: Any, default: int = 2) -> int:
    """Coerce a risk-probability/impact value from an API body into a 1-3 int.

    VerifyWise/CISO Assistant live APIs can return word scales or non-numeric
    junk; anything int()-able is clamped to 1-3, everything else falls back to
    the default instead of crashing on arithmetic.
    """
    if value is None:
        return default
    try:
        return max(1, min(3, int(value)))
    except (TypeError, ValueError):
        return default


def fetch_ciso_risks(
    api_url: str = "http://127.0.0.1:8080",
    *,
    api_key: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch risks from CISO Assistant via REST API.
    
    Uses actual REST API calls with proper authentication and error handling.
    Falls back to sample data if connection fails or in frozen mode.
    """
    if CISO_MODE != "live":
        # Return sample data for frozen mode
        return [
            {
                "id": "RISK-001",
                "title": "DCSync attack on domain controller",
                "description": "Domain Admin compromise via DCSync attack detected",
                "severity": "critical",
                "likelihood": 3,
                "impact": 3,
                "framework": ["ISO 27001", "SOC 2", "NIST CSF"],
                "created_at": "2026-07-01T00:00:00Z",
                "updated_at": "2026-07-27T12:00:00Z",
            },
            {
                "id": "RISK-013",
                "title": "Prompt injection in DarkAI chatbot",
                "description": "LLM prompt injection could leak lab secrets",
                "severity": "high",
                "likelihood": 2,
                "impact": 2,
                "framework": ["ISO 27001", "SOC 2"],
                "created_at": "2026-07-12T00:00:00Z",
                "updated_at": "2026-07-27T12:00:00Z",
            },
        ]
    
    try:
        import requests
    except ImportError:
        print("requests library not installed. Install with: pip install requests")
        return []
    
    headers = {}
    if api_key:
        headers["Authorization"] = f"Token {api_key}"
    
    try:
        response = requests.get(
            f"{api_url}/api/risk-scenarios/",
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        
        risks = response.json()
        print(f"Fetched {len(risks)} risks from CISO Assistant at {api_url}")
        return risks
        
    except requests.exceptions.ConnectionError:
        print(f"Connection error to CISO Assistant at {api_url}")
        return []
    except requests.exceptions.Timeout:
        print(f"Timeout connecting to CISO Assistant at {api_url}")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error from CISO Assistant: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching CISO risks: {e}")
        return []


def push_risk_to_ciso(
    risk: dict[str, Any],
    api_url: str = "http://127.0.0.1:8080",
    *,
    api_key: str | None = None,
) -> dict[str, Any] | None:
    """Push a risk to CISO Assistant via REST API.
    
    Used for CADRE main lab integration - pushes scored risks to CISO Assistant.
    """
    try:
        import requests
    except ImportError:
        print("requests library not installed. Install with: pip install requests")
        return None
    
    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Token {api_key}"
    
    try:
        response = requests.post(
            f"{api_url}/api/risk-scenarios/",
            headers=headers,
            json=risk,
            timeout=30,
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"Pushed risk {risk.get('id')} to CISO Assistant")
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"Connection error to CISO Assistant at {api_url}")
        return None
    except requests.exceptions.Timeout:
        print(f"Timeout connecting to CISO Assistant at {api_url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error from CISO Assistant: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error pushing risk to CISO: {e}")
        return None


def fetch_verifywise_risks(
    api_url: str = "http://127.0.0.1:13000",
    *,
    jwt_token: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch AI risks from VerifyWise via REST API.
    
    Uses actual REST API calls with proper authentication and error handling.
    Falls back to sample data if connection fails or in frozen mode.
    """
    if VW_MODE != "live":
        # Return sample data for frozen mode
        return [
            {
                "id": "RISK-012",
                "title": "DarkAI lab breakout / mix with client evidence",
                "description": "AI system could access client evidence without proper isolation",
                "severity": "high",
                "likelihood": 2,
                "impact": 3,
                "framework": ["EU AI Act", "ISO 42001"],
                "created_at": "2026-07-13T00:00:00Z",
                "updated_at": "2026-07-27T12:00:00Z",
            },
            {
                "id": "RISK-014",
                "title": "Malware sample mishandling on RevAI path",
                "description": "Malware analysis pipeline lacks proper isolation controls",
                "severity": "critical",
                "likelihood": 3,
                "impact": 2,
                "framework": ["EU AI Act", "ISO 42001", "NIST AI RMF"],
                "created_at": "2026-06-30T00:00:00Z",
                "updated_at": "2026-07-27T12:00:00Z",
            },
        ]
    
    try:
        import requests
    except ImportError:
        print("requests library not installed. Install with: pip install requests")
        return []
    
    headers = {}
    if jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"
    
    try:
        response = requests.get(
            f"{api_url}/api/projectRisks",
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        
        data = response.json()
        risks = data.get("data", [])
        print(f"Fetched {len(risks)} AI risks from VerifyWise at {api_url}")
        return risks
        
    except requests.exceptions.ConnectionError:
        print(f"Connection error to VerifyWise at {api_url}")
        return []
    except requests.exceptions.Timeout:
        print(f"Timeout connecting to VerifyWise at {api_url}")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error from VerifyWise: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching VerifyWise risks: {e}")
        return []


def push_risk_to_verifywise(
    risk: dict[str, Any],
    api_url: str = "http://127.0.0.1:13000",
    *,
    jwt_token: str | None = None,
) -> dict[str, Any] | None:
    """Push an AI risk to VerifyWise via REST API.
    
    Used for DarkAI project integration - pushes AI risks to VerifyWise.
    """
    try:
        import requests
    except ImportError:
        print("requests library not installed. Install with: pip install requests")
        return None
    
    headers = {
        "Content-Type": "application/json",
    }
    if jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"
    
    try:
        response = requests.post(
            f"{api_url}/api/projectRisks",
            headers=headers,
            json=risk,
            timeout=30,
        )
        response.raise_for_status()
        
        result = response.json()
        print(f"Pushed AI risk {risk.get('risk_name')} to VerifyWise")
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"Connection error to VerifyWise at {api_url}")
        return None
    except requests.exceptions.Timeout:
        print(f"Timeout connecting to VerifyWise at {api_url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error from VerifyWise: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error pushing risk to VerifyWise: {e}")
        return None


def normalize_ciso_risk(risk: dict[str, Any]) -> UnifiedRisk:
    """Normalize CISO Assistant risk to unified format."""
    likelihood = _coerce_score(risk.get("likelihood"))
    impact = _coerce_score(risk.get("impact"))
    score = likelihood * impact
    
    return UnifiedRisk(
        id=risk.get("id", "unknown"),
        source="ciso",
        title=risk.get("title", ""),
        description=risk.get("description", ""),
        severity=risk.get("severity", "medium"),
        likelihood=likelihood,
        impact=impact,
        score=score,
        band=_score_band(score),
        treatment=_treatment_from_score(score),
        category="classic_grc",
        framework=risk.get("framework", []),
        created_at=risk.get("created_at", _now()),
        updated_at=risk.get("updated_at", _now()),
        raw=risk,
    )


def normalize_verifywise_risk(risk: dict[str, Any]) -> UnifiedRisk:
    """Normalize VerifyWise risk to unified format."""
    likelihood = _coerce_score(risk.get("likelihood"))
    impact = _coerce_score(risk.get("impact"))
    score = likelihood * impact
    
    return UnifiedRisk(
        id=risk.get("id", "unknown"),
        source="verifywise",
        title=risk.get("title", ""),
        description=risk.get("description", ""),
        severity=risk.get("severity", "medium"),
        likelihood=likelihood,
        impact=impact,
        score=score,
        band=_score_band(score),
        treatment=_treatment_from_score(score),
        category="ai_governance",
        framework=risk.get("framework", []),
        created_at=risk.get("created_at", _now()),
        updated_at=risk.get("updated_at", _now()),
        raw=risk,
    )


def generate_unified_dashboard(
    ciso_url: str = "http://127.0.0.1:8080",
    vw_url: str = "http://127.0.0.1:13000",
) -> dict[str, Any]:
    """Generate unified dashboard data from both platforms."""
    ciso_risks = fetch_ciso_risks(ciso_url)
    vw_risks = fetch_verifywise_risks(vw_url)
    
    normalized_ciso = [normalize_ciso_risk(r) for r in ciso_risks]
    normalized_vw = [normalize_verifywise_risk(r) for r in vw_risks]
    
    all_risks = normalized_ciso + normalized_vw
    sorted_risks = sorted(all_risks, key=lambda r: (-r.score, r.id))
    
    # Calculate statistics
    critical_count = sum(1 for r in all_risks if r.score >= 9)
    high_count = sum(1 for r in all_risks if 6 <= r.score < 9)
    medium_count = sum(1 for r in all_risks if 3 <= r.score < 6)
    low_count = sum(1 for r in all_risks if r.score < 3)
    
    ciso_count = len(normalized_ciso)
    vw_count = len(normalized_vw)
    
    # Framework breakdown
    framework_counts: dict[str, int] = {}
    for risk in all_risks:
        for fw in risk.framework:
            framework_counts[fw] = framework_counts.get(fw, 0) + 1
    
    return {
        "generated_at": _now(),
        "total_risks": len(all_risks),
        "by_severity": {
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
        },
        "by_source": {
            "ciso_assistant": ciso_count,
            "verifywise": vw_count,
        },
        "by_category": {
            "classic_grc": ciso_count,
            "ai_governance": vw_count,
        },
        "by_framework": framework_counts,
        "top_risks": [r.to_dict() for r in sorted_risks[:10]],
        "all_risks": [r.to_dict() for r in sorted_risks],
    }


def render_dashboard_html(dashboard_data: dict[str, Any]) -> str:
    """Render unified dashboard as HTML for web display."""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>CADRE-Risk Unified Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        .header {{ border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff; }}
        .stat-card.critical {{ border-left-color: #dc3545; }}
        .stat-card.high {{ border-left-color: #fd7e14; }}
        .stat-card.medium {{ border-left-color: #ffc107; }}
        .stat-card.low {{ border-left-color: #28a745; }}
        .stat-value {{ font-size: 24px; font-weight: bold; }}
        .stat-label {{ color: #666; font-size: 14px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f8f9fa; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
        .badge-critical {{ background: #dc3545; color: white; }}
        .badge-high {{ background: #fd7e14; color: white; }}
        .badge-medium {{ background: #ffc107; color: black; }}
        .badge-low {{ background: #28a745; color: white; }}
        .source-ciso {{ background: #007bff; color: white; }}
        .source-verifywise {{ background: #6f42c1; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CADRE-Risk Unified Dashboard</h1>
            <p>Generated: {dashboard_data['generated_at']}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{dashboard_data['total_risks']}</div>
                <div class="stat-label">Total Risks</div>
            </div>
            <div class="stat-card critical">
                <div class="stat-value">{dashboard_data['by_severity']['critical']}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-card high">
                <div class="stat-value">{dashboard_data['by_severity']['high']}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat-card medium">
                <div class="stat-value">{dashboard_data['by_severity']['medium']}</div>
                <div class="stat-label">Medium</div>
            </div>
            <div class="stat-card low">
                <div class="stat-value">{dashboard_data['by_severity']['low']}</div>
                <div class="stat-label">Low</div>
            </div>
        </div>
        
        <h2>By Source</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{dashboard_data['by_source']['ciso_assistant']}</div>
                <div class="stat-label">CISO Assistant</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{dashboard_data['by_source']['verifywise']}</div>
                <div class="stat-label">VerifyWise</div>
            </div>
        </div>
        
        <h2>Top Risks</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Source</th>
                    <th>Title</th>
                    <th>Score</th>
                    <th>Band</th>
                    <th>Treatment</th>
                    <th>Frameworks</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for risk in dashboard_data["top_risks"]:
        badge_class = f"badge-{risk['band'].lower()}"
        source_class = f"source-{risk['source']}"
        frameworks = ", ".join(risk["framework"])
        
        html += f"""
                <tr>
                    <td>{risk['id']}</td>
                    <td><span class="badge {source_class}">{risk['source']}</span></td>
                    <td>{risk['title']}</td>
                    <td>{risk['score']}</td>
                    <td><span class="badge {badge_class}">{risk['band']}</span></td>
                    <td>{risk['treatment']}</td>
                    <td>{frameworks}</td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    return html


def main(argv: list[str] | None = None) -> int:
    import argparse
    
    parser = argparse.ArgumentParser(description="CADRE-Risk cross-platform dashboard")
    parser.add_argument(
        "--ciso-url",
        type=str,
        default="http://127.0.0.1:8080",
        help="CISO Assistant API URL",
    )
    parser.add_argument(
        "--vw-url",
        type=str,
        default="http://127.0.0.1:13000",
        help="VerifyWise API URL",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "artifacts" / "unified-dashboard.html",
        help="Output HTML path",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=REPO_ROOT / "artifacts" / "unified-dashboard.json",
        help="Output JSON path",
    )
    args = parser.parse_args(argv)
    
    dashboard_data = generate_unified_dashboard(args.ciso_url, args.vw_url)
    
    # Write HTML
    html = render_dashboard_html(dashboard_data)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"Wrote {args.out}")
    
    # Write JSON
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(dashboard_data, indent=2), encoding="utf-8")
    print(f"Wrote {args.json}")
    
    print(f"Total risks: {dashboard_data['total_risks']}")
    print(f"Critical: {dashboard_data['by_severity']['critical']}")
    print(f"High: {dashboard_data['by_severity']['high']}")
    print(f"Medium: {dashboard_data['by_severity']['medium']}")
    print(f"Low: {dashboard_data['by_severity']['low']}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
