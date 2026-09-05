# R-EX-073 — Continuous monitoring vs periodic assessment

**CISSP Reference:** Chapter 15, Section "Building a Security Assessment Program"; Chapter 16, Section "Logging and Monitoring"  
**Exam Objective:** 6.1.1 Design assessment strategy; 7.2.1 Implement continuous monitoring  
**Study Guide Key Terms:** Continuous monitoring, periodic assessment, ISCM (NIST SP 800-137), security metrics, KPIs, KRIs, dashboard  

---

## Scenario Context

Cadre Corp performs quarterly vulnerability scans and annual penetration tests — periodic assessments. Between scans, the following happened and went undetected for months:

1. A new VM was deployed without the standard security baseline (missing firewall rules, no EDR agent).
2. The SOC Lead accidentally removed `Domain Admins` from the `Protected Users` group during a maintenance window — DA credentials became cacheable (extractable from LSASS) for 73 days.
3. A firewall rule allowing RDP from the internet was added by a contractor during troubleshooting and never removed.

The CISO asks: "How do we know we're secure on days we're NOT scanning?"

---

## Multiple-Choice Questions

**Question 1:** Continuous monitoring differs from periodic assessment primarily by:

A. Using different scanning tools  
B. Providing near-real-time visibility into security posture — detecting configuration drift, new vulnerabilities, and control failures as they occur, not just at scheduled assessment intervals  
C. Being 100% automated with no human involvement  
D. Only monitoring network traffic, not system configurations

**Question 2:** Which of the following is an example of a continuous monitoring control that would have caught the RDP firewall rule change?

A. Quarterly vulnerability scan  
B. Configuration change monitoring — a tool that detects when firewall rules are added, generates an alert, and compares the change against an approved change request  
C. Annual penetration test  
D. Monthly team meeting to review configurations

**Question 3:** Drift detection in a continuous monitoring context refers to:

A. Network packets that drift to the wrong subnet  
B. Detecting when a system's actual configuration deviates from its approved baseline — the "RDP from internet" rule is drift from the baseline "no RDP from internet" policy  
C. Employee attention drifting during monitoring shifts  
D. Gradual degradation of monitoring tool performance

---

## Answer Explanations

**Answer 1: B**  
**Continuous monitoring** provides near-real-time visibility — not just a point-in-time snapshot. Where periodic assessment says "as of March 1, we were secure," continuous monitoring says "right now, at 2:37 PM on a Tuesday, we are secure — and I can prove it." It doesn't eliminate humans (C) — alerts still need triage — but it eliminates the blind spots between assessments.

**Answer 2: B**  
**Configuration change monitoring** detects the specific change (firewall rule added), alerts the SOC, and ideally correlates with approved change requests. The other options are periodic — they might catch the issue months later, or never if the rule is removed before the next scan. Continuous monitoring catches it in minutes.

**Answer 3: B**  
**Drift detection** compares actual state against desired/approved state (the baseline). The "RDP from internet" rule is a drift from the approved configuration. Any deviation generates an alert. This is the core value proposition of Infrastructure as Code (Ansible) combined with compliance scanning — define the desired state, detect any deviation, alert or auto-remediate.

---

## Cadre Corp Application

1. **Ansible Drift Detection:** Run `ansible-playbook --check` (dry-run mode) weekly against all VMs. Any task that would make a change indicates drift from the defined baseline. This is a lightweight continuous monitoring mechanism using existing tooling.

2. **SOC Dashboard KPIs:** Build an Elastic dashboard showing: number of VMs in compliance with baseline, number of open high-severity findings, days since last configuration drift detected, privileged group membership changes (real-time from Windows Event Logs).

3. **Change-Approval Integration:** Any configuration change that triggers a drift alert should be correlated with an approved change request. Unapproved drift = incident. This closes the loop between change management and continuous monitoring.

---

## Interview Talking Points

1. **Quarterly Scans = 89 Days of Blindness:** "A quarterly scan means you're secure 4 days a year — the day you scan. The other 361 days, you're hoping nothing changed. Continuous monitoring means every day is a scan day."

2. **Drift Is the Silent Killer:** "Nobody intentionally disables a security control. It drifts — someone troubleshooting at 2 AM adds a firewall rule, forgets to remove it, and it sits there for 73 days. Continuous monitoring catches the drift, not the intent."
