"""CADRE-Risk HTTP server — serves the unified dashboard and risk artifacts."""

from __future__ import annotations

import http.server
import json
import os
import socketserver
from pathlib import Path
from typing import Any

from .board_report import main as generate_board_memo
from .cross_platform import generate_unified_dashboard, render_dashboard_html
from .ingest import load_findings_dir
from .risk_engine import generate_cadre_feedback, score_findings

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
PORT = int(os.getenv("PORT", "8895"))
HOST = os.getenv("HOST", "0.0.0.0")


def refresh_artifacts() -> dict[str, Any]:
    """Score findings and generate all baseline artifacts."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Score findings & generate feedback
    samples_dir = REPO_ROOT / "samples" / "findings"
    findings = load_findings_dir(samples_dir)
    scored = score_findings(findings)
    feedback = generate_cadre_feedback(scored)

    feedback_path = ARTIFACTS_DIR / "feedback.json"
    with open(feedback_path, "w", encoding="utf-8") as f:
        json.dump(feedback, f, indent=2)

    # 2. Board memo
    memo_path = ARTIFACTS_DIR / "board-memo.md"
    try:
        generate_board_memo(["--samples", str(samples_dir), "--out", str(memo_path)])
    except SystemExit:
        pass

    # 3. Unified dashboard (frozen mode default)
    dashboard_data = generate_unified_dashboard()
    html = render_dashboard_html(dashboard_data)

    html_path = ARTIFACTS_DIR / "unified-dashboard.html"
    html_path.write_text(html, encoding="utf-8")

    json_path = ARTIFACTS_DIR / "unified-dashboard.json"
    json_path.write_text(json.dumps(dashboard_data, indent=2), encoding="utf-8")

    return {
        "status": "ready",
        "total_risks": len(scored),
        "artifacts": [
            str(html_path),
            str(json_path),
            str(memo_path),
            str(feedback_path),
        ],
    }


class RiskRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler serving dashboard on / and artifacts on demand."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ARTIFACTS_DIR), **kwargs)

    def do_GET(self):
        # Health check
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"healthy","service":"Risk"}\n')
            return

        # Trigger refresh
        if self.path == "/api/refresh":
            result = refresh_artifacts()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode("utf-8") + b"\n")
            return

        # Redirect root to unified-dashboard.html
        if self.path == "/" or self.path == "":
            self.path = "/unified-dashboard.html"

        super().do_GET()


def run_server(host: str = HOST, port: int = PORT):
    refresh_artifacts()
    print(f"CADRE-Risk server listening on http://{host}:{port}")
    print(f"Unified Dashboard: http://localhost:{port}/")
    print(f"Health check: http://localhost:{port}/health")

    with socketserver.TCPServer((host, port), RiskRequestHandler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()


if __name__ == "__main__":
    run_server()
