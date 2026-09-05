# R-EX-037 — Incident response playbook: Velociraptor scheduled task detection

**CISSP Reference:** Chapter 17, Sections "Incident Management", "Detection and Preventive Measures", "Automating Incident Response", Pages 1230–1270  
**Exam Objective:** 7.3.1 Manage incident response; 7.3.3 Develop IR playbooks  
**Study Guide Key Terms:** IR playbook, detection, containment, eradication, recovery, lessons learned, CSIRT roles, escalation triggers, playbook structure  
**Inputs:** `samples/findings/vr-001`, RISK-004 (unconstrained delegation on mbr01), AST-004

---

## Scenario Context

Velociraptor hunt `Windows.Detection.ScheduledTasks` flagged a suspicious scheduled task on mbr01 (AST-004). The task runs every 30 minutes, executing a base64-encoded PowerShell command that:

1. Dumps LSASS memory to `C:\Windows\Temp\lsass.dmp` using a renamed `procdump64.exe`.
2. Exfiltrates the dump to an external IP via a DNS TXT tunnel (chunked base64 in DNS queries to `exfil.attacker.com`).
3. Clears the PowerShell event log (Event ID 4104) after each execution.

This is active credential dumping (MITRE T1003.001) with DNS exfiltration (T1048.003) and log clearing (T1070.001). mbr01 has unconstrained Kerberos delegation enabled (RISK-004, score 9) — meaning any credential dumped from LSASS likely includes Domain Admin TGTs from administrators who recently authenticated to mbr01.

The CISO activates the incident response playbook. You are the Incident Commander.

---

## Multiple-Choice Questions

**Question 1:** In the NIST SP 800-61 IR lifecycle, what is the FIRST action after detecting active credential dumping on mbr01?

A. Immediately shut down mbr01 to stop the attack  
B. Begin containment while preserving evidence — isolate mbr01 from the network (but don't power off — memory contains volatile evidence), capture a memory dump and VR triage collection, then disable the scheduled task and block the exfiltration DNS domain at the firewall  
C. Notify all 120 clients that a breach has occurred  
D. Start writing the post-incident report

**Question 2:** Why should mbr01 be ISOLATED rather than SHUT DOWN during containment?

A. Shutting down is always the safest option  
B. Isolation preserves volatile evidence — memory contains the LSASS dump, running processes, network connections, and the attacker's active session; shutting down destroys this evidence; isolation stops the attacker's access while preserving forensic artifacts for analysis  
C. Isolation is faster than shutting down  
D. Shutting down might alert the attacker

**Question 3:** After containment, what is the correct eradication step for the scheduled task persistence mechanism?

A. Delete the scheduled task and move on  
B. Remove the scheduled task, delete the dropped `procdump64.exe` binary, identify how the task was created (which account? when? via what method — WMI, schtasks, GPO?), close the initial access vector, and verify no other persistence mechanisms exist on mbr01 or other hosts  
C. Re-image mbr01 immediately without investigation  
D. Leave the task disabled but present for future analysis

**Question 4:** The "lessons learned" phase of this incident should document:

A. Only the detection time  
B. Root cause (how did the attacker get on mbr01?), detection gap (why didn't Suricata catch the DNS tunnel?), response timeline (detection → containment → eradication intervals), playbook improvements, and prevention measures (remove unconstrained delegation, harden scheduled task creation logging)  
C. Only who was responsible for the incident  
D. A brief summary with no actionable items

---

## Answer Explanations

**Answer 1: B**  
**Contain while preserving evidence** is the correct first action. The NIST IR lifecycle sequence after detection is: (1) Contain — isolate the affected system to stop the attacker's activity, (2) Preserve evidence — capture volatile data (memory dump, running processes, network connections) BEFORE making changes, (3) Eradicate — remove the attacker's tools and persistence, (4) Recover — restore to known good state. Immediate shutdown (A) destroys evidence. Client notification (C) may be required but timing depends on impact assessment. Post-incident report (D) comes last.

**Answer 2: B**  
**Isolation preserves evidence; shutdown destroys it.** Memory contains: the LSASS dump with potentially Domain Admin credentials, the attacker's running processes, active C2 connections (IP addresses, protocols used), and registry artifacts. Shutting down writes these to disk (if at all) and destroys volatile state. Isolation — disconnect the network interface or apply a firewall rule blocking all traffic — stops the attacker's access while preserving the forensic crime scene.

**Answer 3: B**  
Eradication requires **understanding the full attack chain**, not just deleting the most visible artifact. Steps: (a) remove the scheduled task and dropped binary, (b) determine HOW the attacker created the task (compromised account? WMI lateral movement? GPO modification?), (c) close the initial access vector — if the attacker can get back on mbr01, they'll just re-create the task, (d) hunt for additional persistence (other scheduled tasks, services, registry Run keys, WMI event subscriptions), (e) verify eradication with a VR re-hunt.

**Answer 4: B**  
Lessons learned must be **comprehensive and actionable**: root cause, detection gaps, response timeline metrics, playbook improvements, and prevention measures. The unconstrained delegation on mbr01 (RISK-004) is a root cause — the playbook should recommend removing it. The DNS tunnel that bypassed Suricata is a detection gap — the playbook should recommend new Suricata rules. Every incident is a free security assessment — lessons learned captures the value.

---

## Cadre Corp Application

1. **Playbook Template:** Standardize IR playbooks with 6 phases: (1) Detection — trigger event + initial triage, (2) Containment — isolation procedure + evidence preservation checklist, (3) Eradication — persistence removal + root cause closure, (4) Recovery — service restoration + verification, (5) Post-Incident — timeline, root cause analysis, lessons learned, (6) Notification — who to notify, when, with what information.

2. **mbr01 Hardening (Post-Incident):** Remove unconstrained delegation (RISK-004). Replace with constrained delegation or resource-based constrained delegation. This prevents future credential dumping from yielding Domain Admin TGTs.

3. **DNS Tunnel Detection Gap:** Deploy new Suricata rules for DNS tunneling: high-entropy query names, unusual query length, high volume of TXT queries to a single external domain. Add to the playbook's detection section.

---

## Interview Talking Points

1. **Isolate, Don't Shut Down:** "The first instinct — 'pull the plug!' — destroys evidence. Isolate the system from the network. Capture memory. Then contain. You can always shut down later; you can never recover volatile evidence destroyed by panic."

2. **A Playbook Is Pre-Made Decisions Under Stress:** "When DCSync fires at 2 AM, nobody should be inventing the response. The playbook was written at 2 PM on a Tuesday when everyone was calm. It answers: who does what, in what order, with what tools, and who to call if it escalates. Pre-made decisions, not improvised panic."

3. **Every Incident Is a Free Penetration Test:** "The attacker just showed you exactly where your defenses failed. The lessons learned phase captures that intelligence: close the root cause, fill the detection gap, improve the playbook. If you skip lessons learned, you're paying for the incident twice."
