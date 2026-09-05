# R-EX-078 — Incident response lifecycle (NIST SP 800-61)

**CISSP Reference:** Chapter 17, Sections "Incident Management", "Detection and Preventive Measures"  
**Exam Objective:** 7.3.1 Manage incident response; 7.3.2 Implement IR lifecycle  
**Study Guide Key Terms:** NIST SP 800-61, IR lifecycle (Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident Activity), CSIRT, playbooks  

---

## Scenario Context

During the campaign exercise, Cadre Corp's SOC detected a DCSync attack (RISK-001) at 14:03 UTC. What followed was chaos:

- The analyst who detected it spent 20 minutes searching Slack for the incident response playbook.
- Nobody knew who had authority to isolate DC01 from the network.
- The containment action (disabling the compromised `svc_mssql` account) also broke the MSSQL service on mbr01 — a production impact nobody anticipated.
- After recovery, no post-incident review was conducted — meaning the same attack will succeed again next campaign.

The CISO asks: "If this were a real incident with client data at risk, would our response have been defensible to clients and regulators?"

---

## Multiple-Choice Questions

**Question 1:** The NIST SP 800-61 incident response lifecycle consists of which four phases?

A. Plan, Execute, Review, Close  
B. Preparation; Detection & Analysis; Containment, Eradication & Recovery; Post-Incident Activity  
C. Alert, Triage, Escalate, Resolve  
D. Identify, Protect, Detect, Respond

**Question 2:** During the "Containment" phase, what is the PRIMARY consideration before taking action?

A. Speed — act immediately to stop the attack  
B. Preservation of evidence AND assessment of operational impact — the containment action (disabling svc_mssql) must not destroy forensic evidence, and its operational impact (MSSQL service outage) must be anticipated and communicated  
C. Notifying all 120 clients immediately  
D. Waiting for law enforcement approval

**Question 3:** The Post-Incident Activity phase (lessons learned) is critical because:

A. It satisfies regulatory reporting requirements  
B. It identifies root cause, documents what worked and what didn't, and drives improvements to prevent recurrence — without it, the organization will repeat the same mistakes  
C. It determines who gets fired  
D. It's optional if the incident was small

---

## Answer Explanations

**Answer 1: B**  
**NIST SP 800-61 defines four phases**: (1) **Preparation** — having playbooks, team, tools, and training ready before an incident; (2) **Detection & Analysis** — identifying and scoping the incident; (3) **Containment, Eradication & Recovery** — stopping the attack, removing attacker access, restoring operations; (4) **Post-Incident Activity** — lessons learned, improving for next time. The other options are simplified or from different frameworks.

**Answer 2: B**  
Containment must balance **stopping the attack with preserving evidence**. Disabling the compromised account stops the attack but also destroys volatile evidence (active sessions, memory artifacts). The IR playbook should specify evidence capture steps BEFORE containment actions. Additionally, operational impact must be assessed: disabling `svc_mssql` broke MSSQL — the team should have been warned and a workaround prepared.

**Answer 3: B**  
**Post-incident review drives improvement**. Without it, every incident is a standalone event — the root cause remains unaddressed, detection gaps persist, and the playbook never improves. This is the most commonly skipped phase (everyone wants to move on after recovery) and the most important for long-term security maturity.

---

## Cadre Corp Application

1. **IR Playbook Development:** Based on the campaign framework, develop specific playbooks for: DCSync detection, Kerberoast detection, Golden Ticket detection, ransomware in DarkAI lab, client evidence breach. Each playbook specifies: detection triggers, evidence collection steps, containment actions (with impact assessment), escalation contacts, and recovery procedures.

2. **CSIRT Definition:** Define the Computer Security Incident Response Team: Incident Commander (CISO or delegate), Technical Lead (SOC Lead), Communications Lead (GRC team for client/regulator notification), Legal counsel (external retainer). Document in the IR plan.

3. **Tabletop Exercise:** After every campaign phase, conduct a mini post-incident review: what was detected? How long from detection to containment? What broke during containment? Document and update playbooks.

---

## Interview Talking Points

1. **IR Without Playbooks = Chaos With Timestamps:** "When DCSync fires at 2 PM and your team spends 20 minutes searching Slack for what to do, you've already lost. Playbooks are pre-decided decisions — they take the thinking out of the first 15 minutes of an incident."

2. **Lessons Learned Is Not Optional:** "Every incident you don't learn from, you'll repeat. The post-incident review is where you close the loop: root cause → detection gap → playbook update → training. Skip it, and you're paying for the same incident twice."
