"""Ansible integration for automated remediation on AST-013 provisioning VM."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]

# Configuration flag
# Set ANSIBLE_MODE=dry-run to generate playbooks without execution
# Set ANSIBLE_MODE=execute to actually run playbooks on AST-013
ANSIBLE_MODE = os.getenv("ANSIBLE_MODE", "dry-run")


@dataclass
class AnsibleTask:
    """Represents a single Ansible task for remediation."""
    name: str
    module: str
    args: dict[str, Any]
    become: bool = False
    when: str | None = None


def feedback_to_ansible_tasks(feedback: dict[str, Any]) -> list[AnsibleTask]:
    """Convert CADRE-Risk feedback JSON to Ansible tasks.
    
    Maps feedback actions to appropriate Ansible modules for AST-013 remediation.
    """
    tasks = []
    
    for action in feedback.get("actions", []):
        action_type = action.get("action")
        target = action.get("target")
        reason = action.get("reason", "")
        priority = action.get("priority", "medium")
        
        if action_type == "disable_account":
            # Use win_domain_user module to disable AD account
            tasks.append(AnsibleTask(
                name=f"Disable AD account: {target}",
                module="ansible.windows.win_domain_user",
                args={
                    "name": target,
                    "enabled": False,
                    "domain_ou": "OU=Users,DC=cadre,DC=local",
                },
                become=True,
                when=priority == "immediate",
            ))
            
        elif action_type == "isolate_host":
            # Use win_firewall_rule to block all traffic
            tasks.append(AnsibleTask(
                name=f"Isolate host: {target}",
                module="ansible.windows.win_firewall_rule",
                args={
                    "name": f"Isolate {target}",
                    "direction": "in",
                    "action": "block",
                    "enabled": True,
                    "profile": ["domain", "private", "public"],
                },
                become=True,
                when=priority == "immediate",
            ))
            
        elif action_type == "rotate_secret":
            # Use win_command to trigger secret rotation script
            tasks.append(AnsibleTask(
                name=f"Rotate secret: {target}",
                module="ansible.windows.win_command",
                args={
                    "cmd": f"C:\\scripts\\rotate-secret.ps1 -SecretName {target}",
                },
                become=True,
                when=priority == "immediate",
            ))
            
        elif action_type == "review_firewall_rules":
            # Use win_command to trigger firewall review script
            tasks.append(AnsibleTask(
                name=f"Review firewall rules for: {target}",
                module="ansible.windows.win_command",
                args={
                    "cmd": f"C:\\scripts\\review-firewall.ps1 -Target {target}",
                },
                become=True,
                when=priority == "high",
            ))
            
        elif action_type == "review_ad_configuration":
            # Use win_command to trigger AD configuration review
            tasks.append(AnsibleTask(
                name="Review Active Directory configuration",
                module="ansible.windows.win_command",
                args={
                    "cmd": "C:\\scripts\\review-ad-config.ps1",
                },
                become=True,
                when=priority == "high",
            ))
    
    return tasks


def generate_ansible_playbook(
    tasks: list[AnsibleTask],
    playbook_name: str = "cadre-risk-remediation",
    inventory: str = "provisioning",
) -> dict[str, Any]:
    """Generate an Ansible playbook from remediation tasks."""
    playbook = {
        "name": f"{playbook_name} - {datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "hosts": inventory,
        "gather_facts": True,
        "vars": {
            "ansible_connection": "ssh",
            "ansible_user": "vagrant",
            "ansible_ssh_private_key_file": "~/.vagrant.d/insecure_private_key",
        },
        "tasks": [],
    }
    
    for task in tasks:
        task_dict = {
            "name": task.name,
            task.module: task.args,
        }
        if task.become:
            task_dict["become"] = True
        if task.when:
            task_dict["when"] = task.when
        playbook["tasks"].append(task_dict)
    
    return playbook


def write_playbook(
    playbook: dict[str, Any],
    output_dir: Path | None = None,
) -> Path:
    """Write Ansible playbook to file."""
    if output_dir is None:
        output_dir = REPO_ROOT / "artifacts" / "ansible"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    playbook_name = playbook["name"].replace(" ", "_").lower()
    playbook_path = output_dir / f"{playbook_name}.yml"
    
    with open(playbook_path, "w", encoding="utf-8") as f:
        import yaml
        yaml.dump([playbook], f, default_flow_style=False, sort_keys=False)
    
    return playbook_path


def execute_playbook(
    playbook_path: Path,
    inventory: str = "provisioning",
    extra_vars: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute Ansible playbook on AST-013.
    
    Returns execution result with status and output.
    """
    if ANSIBLE_MODE != "execute":
        return {
            "status": "dry_run",
            "playbook": str(playbook_path),
            "message": "Dry run - playbook not executed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    try:
        import subprocess
    except ImportError:
        return {
            "status": "error",
            "message": "subprocess module not available",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    cmd = [
        "ansible-playbook",
        str(playbook_path),
        "-i", inventory,
        "-v",
    ]
    
    if extra_vars:
        extra_vars_str = ",".join(f"{k}={v}" for k, v in extra_vars.items())
        cmd.extend(["--extra-vars", extra_vars_str])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )
        
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "playbook": str(playbook_path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "message": "Playbook execution timed out",
            "playbook": str(playbook_path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "playbook": str(playbook_path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def process_feedback_for_ansible(
    feedback: dict[str, Any],
    *,
    execute: bool = False,
    output_dir: Path | None = None,
    inventory: str = "provisioning",
) -> dict[str, Any]:
    """Complete workflow: feedback → tasks → playbook → optional execution."""
    # Convert feedback to Ansible tasks
    tasks = feedback_to_ansible_tasks(feedback)
    
    if not tasks:
        return {
            "status": "no_actions",
            "message": "No remediation actions found in feedback",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    # Generate playbook
    playbook = generate_ansible_playbook(tasks, inventory=inventory)
    
    # Write playbook
    playbook_path = write_playbook(playbook, output_dir)
    
    result = {
        "status": "playbook_generated",
        "playbook_path": str(playbook_path),
        "tasks_count": len(tasks),
        "tasks": [{"name": t.name, "module": t.module} for t in tasks],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    
    # Execute if requested
    if execute or ANSIBLE_MODE == "execute":
        exec_result = execute_playbook(playbook_path, inventory)
        result["execution"] = exec_result
        result["status"] = exec_result.get("status", "unknown")
    
    return result


def generate_rollback_playbook(
    original_playbook: Path,
    output_dir: Path | None = None,
) -> Path:
    """Generate a rollback playbook from an original remediation playbook.
    
    This creates inverse tasks to undo the remediation actions.
    """
    if output_dir is None:
        output_dir = REPO_ROOT / "artifacts" / "ansible"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    import yaml
    
    with open(original_playbook, "r", encoding="utf-8") as f:
        original = yaml.safe_load(f)
    
    rollback_tasks = []
    
    for play in original:
        for task in play.get("tasks", []):
            module = None
            for key in task.keys():
                if key not in ["name", "become", "when", "register", "vars"]:
                    module = key
                    break
            
            if module == "ansible.windows.win_domain_user":
                # Re-enable the account
                rollback_tasks.append({
                    "name": f"Rollback: Re-enable {task[module]['name']}",
                    module: {
                        **task[module],
                        "enabled": True,
                    },
                    "become": task.get("become", False),
                })
            
            elif module == "ansible.windows.win_firewall_rule":
                # Remove the block rule
                rollback_tasks.append({
                    "name": f"Rollback: Remove firewall rule {task['name']}",
                    "ansible.windows.win_firewall_rule": {
                        "name": task[module]["name"],
                        "state": "absent",
                    },
                    "become": task.get("become", False),
                })
    
    rollback_playbook = {
        "name": f"rollback-{original_playbook.stem}",
        "hosts": play.get("hosts", "provisioning"),
        "gather_facts": False,
        "tasks": rollback_tasks,
    }
    
    rollback_path = output_dir / f"rollback-{original_playbook.stem}.yml"
    
    with open(rollback_path, "w", encoding="utf-8") as f:
        yaml.dump([rollback_playbook], f, default_flow_style=False, sort_keys=False)
    
    return rollback_path


def main(argv: list[str] | None = None) -> int:
    import argparse
    
    parser = argparse.ArgumentParser(description="CADRE-Risk Ansible integration")
    parser.add_argument(
        "--feedback",
        type=Path,
        required=True,
        help="Path to feedback JSON file",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute playbook on AST-013 (requires ANSIBLE_MODE=execute)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for playbooks",
    )
    parser.add_argument(
        "--inventory",
        type=str,
        default="provisioning",
        help="Ansible inventory name",
    )
    args = parser.parse_args(argv)
    
    # Load feedback
    with open(args.feedback, "r", encoding="utf-8") as f:
        feedback = json.load(f)
    
    # Process feedback
    result = process_feedback_for_ansible(
        feedback,
        execute=args.execute,
        output_dir=args.output_dir,
        inventory=args.inventory,
    )
    
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in ["playbook_generated", "success", "no_actions"] else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
