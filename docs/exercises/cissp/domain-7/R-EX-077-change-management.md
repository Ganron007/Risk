# R-EX-077 — Change management and configuration control

**CISSP Reference:** Chapter 16, Sections "Change Management", "Configuration Management"  
**Exam Objective:** 7.1.1 Manage security operations; 7.1.2 Implement change management  
**Study Guide Key Terms:** Change advisory board (CAB), change request, rollback plan, configuration baseline, version control, Infrastructure as Code (IaC)  

---

## Scenario Context

Cadre Corp's lab infrastructure is managed via Ansible playbooks — all VMs are configured from code. However, three incidents highlight gaps in change management:

1. The Infra Lead manually added a firewall rule on DC01 during a troubleshooting session ("just to see if it fixes the issue"). The rule was never added to Ansible, and the next playbook run will silently remove it — causing the "fixed" issue to reappear unpredictably.

2. A "quick config change" on Friday at 4:55 PM caused Elasticsearch to stop indexing logs for the entire weekend. No rollback plan existed. No change request was filed.

3. Three different versions of the `cadre_passwords.txt` file exist: one in Ansible vault, one on the Infra Lead's desktop, and one emailed to a contractor 6 months ago. Nobody knows which is current.

---

## Multiple-Choice Questions

**Question 1:** Infrastructure as Code (IaC) with Ansible supports change management by:

A. Eliminating the need for human review of changes  
B. Providing version-controlled, auditable, reproducible configuration — every change is a git commit with author, timestamp, and diff; rollback is `git revert`  
C. Automatically approving all changes  
D. Replacing the need for a CAB

**Question 2:** Every change request should include:

A. Only the change description  
B. Description, justification, impact assessment, rollback plan, approver, scheduled window, and post-change validation steps  
C. The CISO's signature regardless of impact  
D. A 50-page risk analysis document

**Question 3:** The "Friday 4:55 PM change" that broke Elasticsearch violated what change management principle?

A. The change was too complex for a Friday  
B. Change windows — high-risk changes should be scheduled during business hours with staff available to respond, not right before a weekend when the team is away  
C. All changes must be approved by the board  
D. Elasticsearch should never be changed

---

## Answer Explanations

**Answer 1: B**  
**IaC makes configuration auditable and reproducible**. Ansible playbooks in git provide: who changed what, when, why (commit message), and the ability to roll back to any previous state. Manual changes ("just to see if it fixes the issue") have none of these properties. IaC doesn't eliminate human review (A) — it makes review possible by showing exactly what will change (`--check` mode).

**Answer 2: B**  
A change request must include all elements needed for informed approval and safe execution: **why** (justification), **what** (description), **what if it goes wrong** (impact + rollback), **when** (window), **who** (approver and implementer), and **did it work** (validation). Not every change needs the CISO (C) — risk-appropriate approvers. Not every change needs 50 pages (D) — risk-appropriate documentation.

**Answer 3: B**  
**Change windows** are the principle. High-risk, low-urgency changes should be scheduled when: (a) support staff are available to respond to issues, (b) users are minimally impacted (or notified), (c) there's time to roll back and recover before critical business periods. Friday at 4:55 PM violates all three — the team went home, the weekend's log monitoring was down, and nobody could fix it until Monday.

---

## Cadre Corp Application

1. **Ansible = SSoT:** All configuration changes MUST flow through Ansible playbooks. Manual changes to VMs are treated as drift and auto-remediated (or flagged for review). The git log IS the change log.

2. **Change Request Lite:** For the small team (45 people), a lightweight change process: (a) create a GitHub issue with the change template, (b) get one peer review, (c) schedule during business hours, (d) merge PR = deploy change, (e) verify post-deploy. No CAB overhead for a team this size — peer review + audit trail is sufficient.

3. **Password SSoT:** The Ansible vault is the single source of truth for all credentials. Desktop copies and emailed copies are prohibited. `cadre_passwords.txt` files found outside the vault are treated as a security incident.

---

## Interview Talking Points

1. **Manual Changes Are Unplanned Outages Waiting to Happen:** "Every manual config change is a future outage — either the next automation run will revert it, or it'll be forgotten and nobody will know why the system behaves differently. IaC + change management turns 'I typed something on a server' into 'I committed a reviewed, tested change.'"

2. **Friday Afternoon Changes Are Resume-Generating Events:** "Never deploy to production on Friday afternoon unless you want to work all weekend. For a SOC that monitors 24/7, a Friday change that breaks logging means 48+ hours of detection blindness."
