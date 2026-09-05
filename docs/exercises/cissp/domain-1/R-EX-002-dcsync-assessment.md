# R-EX-002 — DCSync qualitative assessment

**CISSP Reference:** Chapter 2, Section "Understand and Apply Risk Management Concepts", Pages 171-215  
**Exam Objective:** 1.2.2 Perform qualitative risk analysis  
**Study Guide Key Terms:** Qualitative risk analysis, likelihood, impact, risk matrix, risk treatment, risk appetite  
**Inputs:** `samples/findings/elastic-dcsync-alert.json`, [`../risk-register-baseline.md`](../risk-register-baseline.md), [`../risk-appetite-statement.md`](../risk-appetite-statement.md)

---

## Scenario Context

Cadre Corp's SOC team has received a critical alert from Elastic (AST-010) indicating potential DCSync replication activity on the domain controllers. DCSync is a technique that allows attackers with domain admin privileges to replicate password hashes from Active Directory, effectively providing credentials for all domain accounts.

The alert details show:
- Source: AST-001 (dc01.cadre.local)
- Event ID: 4662 (Directory Service Access) with DRSUAPI operations
- Target: Multiple service accounts including krbtgt
- Timestamp: 2026-07-15T14:30:00Z
- Context: Unusual timing—DCSync activity during non-maintenance window

The Cadre Corp AD estate includes:
- AST-001, AST-002, AST-003: Domain controllers for cadre.local and child.cadre.local
- Cross-forest trust to range.local
- 120 client accounts across multiple forests
- Domain admin accounts with access to all client evidence systems

As the Risk Manager, you need to perform a qualitative risk assessment of this finding, determine the appropriate risk treatment based on Cadre Corp's risk appetite, and recommend controls to detect or mitigate this threat.

---

## Multiple-Choice Questions

**Question 1:** When assigning a likelihood score (1-3) for this DCSync finding, which of the following justifications is most appropriate for a score of 3 (High)?

A. DCSync attacks are theoretical and have never been observed in the wild  
B. The alert fired during a maintenance window where DCSync is expected  
C. DCSync is a well-documented attack technique in campaign activity and the alert fired outside normal maintenance windows  
D. Domain controllers are isolated from the network and cannot be reached

**Question 2:** When assigning an impact score (1-3) for this DCSync finding, which of the following justifications is most appropriate for a score of 3 (High)?

A. DCSync only affects service accounts, not user accounts  
B. Successful DCSync provides credential access to all domain accounts, including those with access to client evidence (AST-030)  
C. Domain controllers have backups that can restore any compromised credentials  
D. The attack only affects the cadre.local forest, not trusted forests

**Question 3:** Based on Cadre Corp's risk appetite statement (low appetite for client-evidence compromise), which of the following is the appropriate risk treatment for this finding?

A. Accept the risk because DCSync attacks are rare  
B. Transfer the risk through cyber insurance  
C. Remediate or mitigate immediately  
D. Monitor the situation without taking action

**Question 4:** Which of the following control combinations would be most effective in detecting and reducing DCSync risk in the Cadre Corp environment?

A. Only implement password complexity requirements  
B. Deploy SIEM rules for DCSync detection (4662/DRSUAPI) and implement AD tiering with privileged access workstations  
C. Rely on Windows Event Forwarding without specific DCSync rules  
D. Implement only network segmentation without AD-specific controls

---

## Answer Explanations

**Answer 1: C**  
DCSync is a well-documented attack technique in campaign activity and the alert fired outside normal maintenance windows, justifying a High likelihood (3). DCSync is a proven attack vector used in real-world campaigns (e.g., Mimikatz, SharpDCSync). The alert firing outside maintenance windows increases the likelihood that this is malicious activity rather than legitimate replication. Option A is incorrect because DCSync is a well-known attack. Option B is incorrect because the timing is unusual. Option D is incorrect because domain controllers must be accessible for normal operations.

**Answer 2: B**  
Successful DCSync provides credential access to all domain accounts, including those with access to client evidence (AST-030), justifying a High impact (3). DCSync allows attackers to harvest password hashes for all accounts in the domain, including domain admins and service accounts with access to Restricted systems. This could lead to complete compromise of the identity plane and client evidence. Option A is incorrect because DCSync affects all accounts. Option C is incorrect because backups don't prevent credential theft. Option D is incorrect because cross-forest trust extends the impact.

**Answer 3: C**  
Remediate or mitigate immediately is the appropriate treatment based on Cadre Corp's low risk appetite for client-evidence compromise. DCSync represents an existential risk because it could lead to client evidence compromise. Accepting the risk (A) contradicts the stated risk appetite. Transferring the risk (B) through insurance doesn't address the immediate threat. Monitoring without action (D) is insufficient for a critical finding.

**Answer 4: B**  
Deploying SIEM rules for DCSync detection (4662/DRSUAPI) and implementing AD tiering with privileged access workstations provides both detection and prevention. SIEM rules enable early detection of DCSync activity, while AD tiering reduces the attack surface by limiting where domain admin credentials are used. Password complexity (A) doesn't prevent DCSync. Windows Event Forwarding without specific rules (C) may not detect DCSync. Network segmentation (D) alone doesn't prevent AD-specific attacks.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's risk assessment process by:

1. **Qualitative Analysis:** Applying the 1-3 likelihood/impact scoring model to real security findings
2. **Risk Appetite Alignment:** Using the risk appetite statement to drive treatment decisions
3. **Control Mapping:** Linking findings to specific controls in the control register
4. **Identity Plane Risk:** Understanding the criticality of AD security for DFIR operations

**Lab Connection:** After completing this exercise, you can:
- Run `python -m src.risk_engine` to score the sample finding and verify the score of 9
- Review the control register (`docs/control-register.md`) to identify CTL-SIEM-IDENTITY and CTL-AD-BASELINE
- Examine the risk register (`docs/risk-register-baseline.md`) to see RISK-001 (DCSync)
- Test the SIEM rules in the CADRE lab environment for DCSync detection

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Qualitative Assessment Methodology:** "I use a structured qualitative risk assessment process with likelihood and impact scoring. For DCSync, I assigned High likelihood because it's a proven attack technique and the alert fired outside maintenance windows. I assigned High impact because DCSync provides credential access to all domain accounts, including those with access to client evidence."

2. **Risk Appetite-Driven Treatment:** "Risk treatment decisions are driven by our risk appetite statement. Cadre Corp has low appetite for client-evidence compromise, so DCSync requires immediate remediation rather than acceptance or monitoring. We don't accept risks that could result in existential business impact."

3. **Control Selection Strategy:** "I select controls based on their effectiveness in detecting and preventing specific threats. For DCSync, SIEM detection rules (4662/DRSUAPI) provide early warning, while AD tiering and privileged access workstations reduce the attack surface. This layered defense approach addresses both detection and prevention."

4. **Identity Plane Criticality:** "In DFIR environments, the identity plane is particularly critical because domain admin credentials provide access to client evidence systems. I prioritize identity security controls higher than in other environments because the business impact of identity compromise is existential."

5. **Risk Scoring Communication:** "When presenting risk scores to the board, I translate technical findings into business impact. A DCSync finding with a score of 9 (Critical) is presented as 'High likelihood of credential theft that could compromise client evidence and violate attorney-client privilege,' rather than technical details about event IDs."

---

## Task

1. Assign Likelihood and Impact (1–3) for finding-elastic-001; justify each.
2. State treatment per Cadre Corp appetite.
3. Name two controls that should detect or reduce this risk.

## Answer key

1. L=3 (campaign-proven / alert fired), I=3 (Restricted DC / DA path) → score 9 Critical.
2. **Remediate / mitigate immediately** — not accept; identity takeover violates low appetite.
3. CTL-SIEM-IDENTITY (4662 / DRSUAPI), CTL-AD-BASELINE (tiering, privileged access workstations).

**Tool check:** `score_finding` on the sample should yield score 9.
