"""Eramba Enterprise REST client + dry-run.

Community Edition has no REST API — use ``eramba_export`` CSV path instead.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class ErambaConfig:
    base_url: str
    edition: str
    user: str
    password: str
    api_prefix: str
    risks_path: str
    assets_path: str
    verify_tls: bool

    @property
    def api_enabled(self) -> bool:
        return self.edition.lower() in {"enterprise", "ee", "ent"}


def load_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def config_from_env(env_path: Path | None = None) -> ErambaConfig:
    file_env = load_env_file(env_path) if env_path else {}
    merged = {**file_env, **{k: v for k, v in os.environ.items() if k.startswith("ERAMBA_")}}
    return ErambaConfig(
        base_url=merged.get("ERAMBA_BASE_URL", "").rstrip("/"),
        edition=merged.get("ERAMBA_EDITION", "ce"),
        user=merged.get("ERAMBA_USER", ""),
        password=merged.get("ERAMBA_PASSWORD", ""),
        api_prefix=merged.get("ERAMBA_API_PREFIX", "/api"),
        risks_path=merged.get("ERAMBA_RISKS_PATH", "/security-risks"),
        assets_path=merged.get("ERAMBA_ASSETS_PATH", "/assets"),
        verify_tls=merged.get("ERAMBA_VERIFY_TLS", "true").lower()
        not in {"0", "false", "no"},
    )


class ErambaClient:
    """Thin HTTP Basic client. Paths must match your Swagger."""

    def __init__(self, cfg: ErambaConfig, dry_run: bool = False):
        self.cfg = cfg
        self.dry_run = dry_run

    def _url(self, path: str) -> str:
        prefix = self.cfg.api_prefix.rstrip("/")
        path = path if path.startswith("/") else f"/{path}"
        return urljoin(self.cfg.base_url + "/", f"{prefix.lstrip('/')}{path}".lstrip("/"))

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        url = self._url(path)
        payload = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.cfg.user:
            token = base64.b64encode(f"{self.cfg.user}:{self.cfg.password}".encode()).decode()
            headers["Authorization"] = f"Basic {token}"

        if self.dry_run:
            return {
                "dry_run": True,
                "method": method,
                "url": url,
                "body": body,
            }

        if not self.cfg.api_enabled:
            raise RuntimeError(
                "ERAMBA_EDITION is not enterprise — REST API unavailable on Community Edition. "
                "Use: python -m src.eramba_export"
            )
        if not self.cfg.base_url or not self.cfg.user:
            raise RuntimeError("Set ERAMBA_BASE_URL and ERAMBA_USER/PASSWORD in eramba.local.env")

        req = urllib.request.Request(url, data=payload, headers=headers, method=method)
        ctx = ssl.create_default_context()
        if not self.cfg.verify_tls:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {"status": resp.status}
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Eramba HTTP {e.code} on {url}: {detail}") from e

    def create_asset(self, asset: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", self.cfg.assets_path, asset)

    def create_risk(self, risk: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", self.cfg.risks_path, risk)

    def push_scored_finding(self, scored: dict[str, Any]) -> dict[str, Any]:
        """Map CADRE-Risk scored finding → generic risk payload (adjust fields to Swagger)."""
        body = {
            "title": scored.get("title"),
            "description": (
                f"Source={scored.get('source')} asset={scored.get('asset_id')} "
                f"score={scored.get('score')} treatment={scored.get('treatment')} "
                f"evidence={scored.get('evidence')}"
            ),
            "risk_score": scored.get("score"),
            "likelihood": scored.get("likelihood"),
            "impact": scored.get("impact"),
            "cadre_finding_id": scored.get("finding_id"),
            "related_risk_id": scored.get("related_risk_id"),
        }
        return self.create_risk(body)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Eramba Enterprise client / dry-run")
    parser.add_argument("--env", type=Path, default=REPO_ROOT / "config" / "eramba.local.env")
    parser.add_argument("--dry-run", action="store_true", help="Print requests only")
    parser.add_argument(
        "--push-samples",
        action="store_true",
        help="Score samples/findings and POST as risks (or dry-run)",
    )
    args = parser.parse_args(argv)
    cfg = config_from_env(args.env if args.env.exists() else None)
    client = ErambaClient(cfg, dry_run=args.dry_run or not cfg.api_enabled)

    if not args.push_samples:
        print(
            json.dumps(
                {
                    "edition": cfg.edition,
                    "api_enabled": cfg.api_enabled,
                    "base_url": cfg.base_url or None,
                    "hint": "Use --push-samples [--dry-run] or python -m src.eramba_export for CE",
                },
                indent=2,
            )
        )
        return 0

    from .ingest import load_findings_dir
    from .risk_engine import score_findings

    findings = load_findings_dir(REPO_ROOT / "samples" / "findings")
    scored = score_findings(findings)
    results = []
    for s in scored:
        results.append(client.push_scored_finding(s.to_dict()))
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
