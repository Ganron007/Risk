# R-EX-074 — Report writing and executive summaries

**CISSP Reference:** Chapter 15, Section "Reporting Findings"; Chapter 1, Section "Executive Communication"  
**Exam Objective:** 6.2.2 Report assessment findings; 1.1.1 Communicate risk to leadership  
**Study Guide Key Terms:** Executive summary, technical findings, risk rating, remediation recommendations, audience-appropriate communication  

---

## Scenario Context

Cadre Corp's external penetration test of the client portal is complete. The testing firm delivered a 127-page technical report with 34 findings, each with CVSS scores, proof-of-concept code, and packet captures. The CISO needs to present the results to the board in 10 minutes. The board members include: the CEO (business background), CFO (financial), and two independent directors (legal and healthcare backgrounds). None have technical security expertise.

The CISO asks you to prepare the board presentation. The 127-page report cannot go to the board — they won't read it. You need to extract what matters to them.

---

## Multiple-Choice Questions

**Question 1:** An executive summary of a penetration test should primarily communicate:

A. Technical details of each vulnerability with CVSS vector strings  
B. Business risk — what was tested, what was found, what's the potential business impact, what we're doing about it, and what resources we need — in language the board understands  
C. Complete command-line output from every tool used  
D. A list of CVEs with links to NVD

**Question 2:** When presenting a critical finding (CVSS 9.8) to the board, which framing is most effective?

A. "CVE-2024-XXXXX with CVSS vector AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H was discovered on the portal server"  
B. "The testers found a vulnerability in our client portal that could allow an attacker to access client forensic evidence without needing a password. We have already patched it. Here's what we're doing to prevent similar issues."  
C. "We found a critical vulnerability — it's very technical, so I won't explain it"  
D. "All 34 findings are critical and need immediate remediation"

**Question 3:** What is the appropriate level of technical detail for different audiences?

A. Same level for everyone — transparency is key  
B. Board: business impact + risk level + resource needs. CISO: findings summary + remediation status. SOC team: full technical report with PoC, packet captures, and remediation steps. Each audience gets what they need to make decisions.  
C. Board gets the full 127-page report; SOC team gets a one-page summary  
D. Technical details are never appropriate for anyone

---

## Answer Explanations

**Answer 1: B**  
The executive summary communicates **business risk**, not technical details. The board needs to know: (1) What did we test? (2) What did they find? (3) Could this affect our clients, revenue, or regulatory standing? (4) What are we doing about it? (5) What do we need (budget, time, people)? CVSS vectors (A) and command output (C) are for the SOC team, not the board.

**Answer 2: B**  
**Business impact + action taken** is the right framing. The board doesn't need to know the CVE number — they need to know there was a risk to client data, it's been addressed, and there's a plan to prevent recurrence. The CVSS string (A) is noise to a non-technical audience. "It's too technical to explain" (C) erodes trust. "All findings are critical" (D) is inaccurate — findings have different severities.

**Answer 3: B**  
**Audience-appropriate communication** is a core CISSP skill. The board needs business-level risk communication. The CISO needs a balanced view (what's bad, what's fixed, what's remaining). The SOC team needs full technical detail to remediate. Each audience gets a different product from the same underlying assessment data.

---

## Cadre Corp Application

1. **Board Memo Template:** Use the existing `artifacts/board-memo.md` and `src/board_report.py` infrastructure. Feed the pentest findings into the scoring engine → generate an executive summary mapping findings to business risks and Cadre Corp assets.

2. **Three-Tier Reporting:** (1) Board: 2-page executive memo with risk matrix and resource ask. (2) CISO/SOC Lead: 10-page findings summary with prioritization and remediation status. (3) SOC Team: full technical report with PoC, logs, and step-by-step remediation.

3. **Remediation Tracking Integration:** Each finding from the pentest becomes a tracked item with owner, due date, and status visible on the SOC dashboard.

---

## Interview Talking Points

1. **CVSS Is Not Business Language:** "The board doesn't care about CVSS vector strings. They care about 'can someone steal our clients' data?' and 'how much will it cost to fix?' My job as a security leader is translating between those two languages."

2. **Bad News Early, With a Plan:** "When presenting critical findings to the board, lead with: 'Here's what we found. Here's what we already fixed. Here's what we need from you.' Never present problems without solutions."
