"""Approval workflow for critical remediation actions."""

from __future__ import annotations

import getpass
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]

# Configuration flag
# Set APPROVAL_MODE=auto to auto-approve non-critical actions
# Set APPROVAL_MODE=manual to require approval for all actions
APPROVAL_MODE = os.getenv("APPROVAL_MODE", "manual")


@dataclass
class ApprovalRequest:
    """Represents an approval request for a remediation action."""
    id: str
    action: str
    target: str
    reason: str
    priority: str
    requested_at: str
    status: str = "pending"
    approved_by: str | None = None
    approved_at: str | None = None
    rejection_reason: str | None = None


def generate_approval_id(action: dict[str, Any]) -> str:
    """Generate a unique approval ID from action details."""
    content = f"{action.get('action')}:{action.get('target')}:{action.get('priority')}:{datetime.now(timezone.utc).isoformat()}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def is_critical_action(action: dict[str, Any]) -> bool:
    """Determine if an action requires approval based on priority and type."""
    priority = action.get("priority", "medium")
    action_type = action.get("action", "")
    
    # Critical actions always require approval
    if priority == "immediate":
        return True
    
    # Specific action types require approval
    critical_actions = ["disable_account", "isolate_host", "rotate_secret"]
    if action_type in critical_actions:
        return True
    
    return False


def create_approval_request(action: dict[str, Any]) -> ApprovalRequest:
    """Create an approval request from a remediation action."""
    return ApprovalRequest(
        id=generate_approval_id(action),
        action=action.get("action"),
        target=action.get("target"),
        reason=action.get("reason"),
        priority=action.get("priority", "medium"),
        requested_at=datetime.now(timezone.utc).isoformat(),
    )


def request_approval(request: ApprovalRequest) -> bool:
    """Request human approval for a remediation action.
    
    Returns True if approved, False if rejected.
    """
    if APPROVAL_MODE == "auto" and not is_critical_action({
        "action": request.action,
        "priority": request.priority,
    }):
        # Auto-approve non-critical actions in auto mode
        request.status = "approved"
        request.approved_by = "system-auto"
        request.approved_at = datetime.now(timezone.utc).isoformat()
        return True
    
    print(f"\n{'='*60}")
    print(f"APPROVAL REQUIRED: {request.id}")
    print(f"{'='*60}")
    print(f"Action: {request.action}")
    print(f"Target: {request.target}")
    print(f"Priority: {request.priority}")
    print(f"Reason: {request.reason}")
    print(f"Requested: {request.requested_at}")
    print(f"{'='*60}")
    
    while True:
        response = input("Approve this action? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            request.status = "approved"
            request.approved_by = getpass.getuser()
            request.approved_at = datetime.now(timezone.utc).isoformat()
            print(f"✓ Action {request.id} approved by {request.approved_by}")
            return True
        elif response in ["no", "n"]:
            request.status = "rejected"
            request.rejection_reason = input("Rejection reason (optional): ").strip() or "User rejected"
            print(f"✗ Action {request.id} rejected: {request.rejection_reason}")
            return False
        else:
            print("Please enter 'yes' or 'no'")


def process_actions_with_approval(
    feedback: dict[str, Any],
    *,
    auto_approve_non_critical: bool = False,
) -> dict[str, Any]:
    """Process remediation actions with approval workflow.
    
    Returns summary of approved/rejected actions.
    """
    actions = feedback.get("actions", [])
    
    if not actions:
        return {
            "total_actions": 0,
            "approved": 0,
            "rejected": 0,
            "auto_approved": 0,
            "results": [],
        }
    
    results = []
    approved_count = 0
    rejected_count = 0
    auto_approved_count = 0
    
    for action in actions:
        request = create_approval_request(action)
        
        # Check if approval is needed
        if not is_critical_action(action) and (auto_approve_non_critical or APPROVAL_MODE == "auto"):
            # Auto-approve non-critical actions
            request.status = "approved"
            request.approved_by = "system-auto"
            request.approved_at = datetime.now(timezone.utc).isoformat()
            auto_approved_count += 1
            approved_count += 1
            results.append({
                "action": action,
                "approval": request.__dict__,
                "approved": True,
                "auto_approved": True,
            })
        else:
            # Request human approval
            approved = request_approval(request)
            if approved:
                approved_count += 1
                results.append({
                    "action": action,
                    "approval": request.__dict__,
                    "approved": True,
                    "auto_approved": False,
                })
            else:
                rejected_count += 1
                results.append({
                    "action": action,
                    "approval": request.__dict__,
                    "approved": False,
                    "auto_approved": False,
                })
    
    return {
        "total_actions": len(actions),
        "approved": approved_count,
        "rejected": rejected_count,
        "auto_approved": auto_approved_count,
        "results": results,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def save_approval_log(
    approval_summary: dict[str, Any],
    output_dir: Path | None = None,
) -> Path:
    """Save approval log to file for audit trail."""
    if output_dir is None:
        output_dir = REPO_ROOT / "artifacts" / "approvals"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    log_path = output_dir / f"approval-{timestamp}.json"
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(approval_summary, f, indent=2)
    
    return log_path


def filter_approved_actions(feedback: dict[str, Any], approval_summary: dict[str, Any]) -> dict[str, Any]:
    """Filter feedback to include only approved actions."""
    approved_actions = []
    
    for result in approval_summary.get("results", []):
        if result.get("approved"):
            approved_actions.append(result["action"])
    
    return {
        **feedback,
        "actions": approved_actions,
        "filtered_at": datetime.now(timezone.utc).isoformat(),
        "original_action_count": feedback.get("actions", []).__len__(),
        "approved_action_count": len(approved_actions),
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    
    parser = argparse.ArgumentParser(description="CADRE-Risk approval workflow")
    parser.add_argument(
        "--feedback",
        type=Path,
        required=True,
        help="Path to feedback JSON file",
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Auto-approve non-critical actions",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for approval logs",
    )
    parser.add_argument(
        "--filter",
        action="store_true",
        help="Output filtered feedback with only approved actions",
    )
    args = parser.parse_args(argv)
    
    # Load feedback
    with open(args.feedback, "r", encoding="utf-8") as f:
        feedback = json.load(f)
    
    # Process with approval
    summary = process_actions_with_approval(
        feedback,
        auto_approve_non_critical=args.auto_approve,
    )
    
    # Save approval log
    log_path = save_approval_log(summary, args.output_dir)
    print(f"\nApproval log saved to: {log_path}")
    
    # Print summary
    print(f"\n{'='*60}")
    print("APPROVAL SUMMARY")
    print(f"{'='*60}")
    print(f"Total actions: {summary['total_actions']}")
    print(f"Approved: {summary['approved']}")
    print(f"Rejected: {summary['rejected']}")
    print(f"Auto-approved: {summary['auto_approved']}")
    print(f"{'='*60}")
    
    # Output filtered feedback if requested
    if args.filter:
        filtered = filter_approved_actions(feedback, summary)
        filtered_path = args.feedback.parent / f"{args.feedback.stem}-approved.json"
        with open(filtered_path, "w", encoding="utf-8") as f:
            json.dump(filtered, f, indent=2)
        print(f"Filtered feedback saved to: {filtered_path}")
    
    return 0 if summary["rejected"] == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
