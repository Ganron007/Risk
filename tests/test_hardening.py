"""Release-hardening regression tests (Sprint 4-7 fix batch).

Covers: live-API score coercion (cross_platform), Kerberos feedback action
(risk_engine), non-interactive approval deferral (approval_workflow), SARIF
sidecar ingest (ingest), feedback CLI (risk_engine main), and win_command
rollback flagging (ansible_integration).
"""

import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import yaml

from src import risk_engine
from src.approval_workflow import (
    create_approval_request,
    request_approval,
)
from src.cross_platform import normalize_ciso_risk, normalize_verifywise_risk
from src.ingest import load_findings_dir
from src.risk_engine import generate_cadre_feedback, score_findings
from src.ansible_integration import generate_rollback_playbook

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples" / "findings"


# --- F4: live-API string scores must not crash normalization -----------------

def test_normalize_coerces_non_numeric_scores():
    risk = normalize_verifywise_risk({"id": "r1", "likelihood": "Likely", "impact": "Moderate"})
    assert risk.score == 4  # both coerce to default 2
    risk2 = normalize_ciso_risk({"id": "r2", "likelihood": None, "impact": "bogus"})
    assert risk2.score == 4  # missing/None → default 2, no TypeError


def test_normalize_clamps_numeric_scores():
    risk = normalize_verifywise_risk({"id": "r3", "likelihood": 9, "impact": 0})
    assert risk.likelihood == 3 and risk.impact == 1  # clamped 1-3


# --- F7: Kerberos case bug must produce review_ad_configuration ---------------

def test_zeek_generates_review_ad_configuration():
    feedback = generate_cadre_feedback(score_findings(load_findings_dir(SAMPLES)))
    types = [a["action"] for a in feedback["actions"]]
    assert "review_ad_configuration" in types


# --- F5: approval must fail closed without a TTY -------------------------------

def test_approval_defers_without_tty(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO())  # isatty() == False
    action = {"action": "isolate_host", "target": "AST-004", "reason": "test", "priority": "immediate"}
    request = create_approval_request(action)
    assert request_approval(request) is False
    assert request.status == "deferred"
    assert request.rejection_reason


def test_approval_approves_non_critical_no_tty(monkeypatch):
    # Non-critical actions in auto mode still auto-approve regardless of TTY.
    monkeypatch.setattr(sys, "stdin", io.StringIO())
    monkeypatch.setattr("src.approval_workflow.APPROVAL_MODE", "auto")
    action = {"action": "review_firewall_rules", "target": "AST-001", "reason": "test", "priority": "high"}
    assert request_approval(create_approval_request(action)) is True


def test_approval_defers_on_eof_even_if_input_available(monkeypatch):
    # Some envs report isatty()=True but EOF on the first prompt — must defer, not crash.
    def _eof(*args, **kwargs):
        raise EOFError

    monkeypatch.setattr("builtins.input", _eof)
    action = {"action": "rotate_secret", "target": "NEXUS_AUDIT_SECRET", "reason": "test", "priority": "immediate"}
    request = create_approval_request(action)
    assert request_approval(request) is False
    assert request.status == "deferred"
    assert request.rejection_reason


# --- F9: SARIF sidecar ingest ---------------------------------------------------

def test_sarif_sidecar_ingested_when_uncited(tmp_path):
    src = SAMPLES / "praxis-sarif-sample.sarif"
    (tmp_path / src.name).write_bytes(src.read_bytes())
    findings = load_findings_dir(tmp_path)
    assert len(findings) == 1
    assert findings[0]["id"].startswith("sarif-")
    assert findings[0]["source"] == "praxis"


def test_sarif_cited_by_json_standin_is_not_double_counted():
    findings = load_findings_dir(SAMPLES)
    assert findings  # sanity: 10 unified JSON findings
    assert not any(f["id"].startswith("sarif-") for f in findings)


# --- F12: feedback CLI writes the JSON the other CLIs consume -------------------

def test_feedback_cli_writes_json(tmp_path):
    out = tmp_path / "feedback.json"
    rc = risk_engine.main(["--samples", str(SAMPLES), "--out", str(out)])
    assert rc == 0
    feedback = json.loads(out.read_text(encoding="utf-8"))
    assert feedback["total_risks"] == len(load_findings_dir(SAMPLES))
    assert any(a["action"] == "review_ad_configuration" for a in feedback["actions"])


# --- F13: win_command tasks get flagged, not silently dropped -------------------

def test_rollback_flags_win_command(tmp_path):
    original_path = tmp_path / "cadre-risk-remediation-test.yml"
    original = [
        {
            "name": "cadre-risk remediation",
            "hosts": "ashlab",
            "gather_facts": False,
            "tasks": [
                {
                    "name": "Disable account svc_mssql",
                    "ansible.windows.win_domain_user": {"name": "svc_mssql", "state": "disabled"},
                    "become": True,
                },
                {
                    "name": "Rotate NEXUS_AUDIT_SECRET",
                    "ansible.windows.win_command": {"cmd": "C:\\scripts\\rotate-secret.ps1 -Target NEXUS_AUDIT_SECRET"},
                    "become": True,
                },
            ],
        }
    ]
    original_path.write_text(yaml.dump(original, sort_keys=False), encoding="utf-8")

    rollback_path = generate_rollback_playbook(original_path, output_dir=tmp_path / "out")
    rolled = yaml.safe_load(rollback_path.read_text(encoding="utf-8"))[0]

    assert rolled["hosts"] == "ashlab"  # propagated from original play
    modules = [list(t.keys()) for t in rolled["tasks"]]
    flat = [m for task in modules for m in task]
    assert "ansible.builtin.debug" in flat  # win_command flagged, not dropped
    reenable = [t for t in rolled["tasks"] if "ansible.windows.win_domain_user" in t][0]
    assert reenable["ansible.windows.win_domain_user"]["enabled"] is True


def test_rollback_empty_playbook_no_crash(tmp_path):
    empty_path = tmp_path / "empty.yml"
    empty_path.write_text(yaml.dump([]), encoding="utf-8")  # regression: old ``play`` NameError
    rollback_path = generate_rollback_playbook(empty_path, output_dir=tmp_path / "out")
    rolled = yaml.safe_load(rollback_path.read_text(encoding="utf-8"))[0]
    assert rolled["hosts"] == "provisioning"
    assert rolled["tasks"] == []
