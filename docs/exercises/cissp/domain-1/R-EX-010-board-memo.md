# R-EX-010 — Board risk memo

**CISSP Reference:** Chapter 1, Section "Manage the Security Function", Pages 109-126  
**Exam Objective:** 1.1.7 Communicate security risks to executive leadership  
**Study Guide Key Terms:** Executive communication, board reporting, risk presentation, business language, security governance  
**Inputs:** [`../examples/board-memo-sample.md`](../examples/board-memo-sample.md), [`../risk-register-baseline.md`](../risk-register-baseline.md)

---

## Scenario Context

Cadre Corp's board of directors meets quarterly to review business performance and strategic initiatives. The CISO is scheduled to present the security risk posture at the next board meeting, which includes both technical findings and business impact assessments.

The current state includes:
- Technical security findings documented in the risk register
- No standardized executive communication format
- Ad-hoc board presentations with inconsistent messaging
- Risk findings presented in technical jargon rather than business language
- No clear "asks" or action items for the board

The CISO has requested a board risk memo that:
- Translates technical findings into business language
- Clearly articulates the business impact of each risk
- Provides specific, actionable asks for the board
- Enables non-technical executives to make informed decisions

As the Risk Manager, you need to generate a board memo from sample findings, rewrite the top three findings in business language, and state one clear ask of the board for each.

---

## Multiple-Choice Questions

**Question 1:** Which of the following is the most appropriate business language translation for a DCSync alert finding?

A. "Event ID 4662 fired on dc01 indicating DRSUAPI access"  
B. "Attacker-level access to our identity systems is plausible; client monitoring credibility at risk"  
C. "Active Directory replication requests were detected from an unusual source"  
D. "Kerberos ticket-granting ticket requests exceeded baseline thresholds"

**Question 2:** When presenting a prompt injection finding in the DarkAI lab to the board, which of the following is the most appropriate business impact statement?

A. "The LLM chatbot failed to sanitize user input allowing prompt injection"  
B. "Research lab isolation controls may be insufficient; verify no client evidence access occurred"  
C. "AI lab leaked a secret; confirm isolation from client evidence"  
D. "Natural language processing model vulnerabilities detected in testing environment"

**Question 3:** For a scheduled task persistence finding on a member server, which of the following is the most appropriate board ask?

A. "Deploy endpoint detection and response to all servers"  
B. "Close the attack path and verify detections are working as expected"  
C. "Increase security budget for additional monitoring tools"  
D. "Conduct a full penetration test of the entire estate"

**Question 4:** What is the primary criterion for evaluating whether a board memo is effective?

A. The memo includes all technical details from the SIEM  
B. The memo uses security industry terminology correctly  
C. A non-technical CEO could act on the memo without reading technical logs  
D. The memo is less than one page in length

---

## Answer Explanations

**Answer 1: B**  
"Attacker-level access to our identity systems is plausible; client monitoring credibility at risk" is the most appropriate business language translation. It focuses on the business impact (identity compromise, client credibility) rather than technical details (event IDs, protocols). Option A is too technical. Option C is still technical. Option D is unrelated to DCSync.

**Answer 2: C**  
"AI lab leaked a secret; confirm isolation from client evidence" is the most appropriate business impact statement. It clearly states the issue (secret leak) and the required action (verify isolation) in business terms. Option A is too technical. Option B is vague about the actual issue. Option D is overly technical without clear business impact.

**Answer 3: B**  
"Close the attack path and verify detections are working as expected" is the most appropriate board ask. It's specific, actionable, and addresses the root cause. Option A is a generic solution not tied to the specific finding. Option C is a budget request without clear justification. Option D is disproportionate to the specific finding.

**Answer 4: C**  
A non-technical CEO could act on the memo without reading technical logs is the primary effectiveness criterion. Board memos must enable executive decision-making without requiring technical expertise. Options A, B, and D are secondary concerns—technical details, terminology, and length don't matter if executives can't understand and act on the information.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's executive communication by:

1. **Technical-to-Business Translation:** Converting security findings into business impact language
2. **Board Presentation Skills:** Developing clear, actionable asks for executive leadership
3. **Risk Communication:** Presenting security risks in terms executives understand
4. **Decision Support:** Enabling informed board decisions without technical jargon

**Lab Connection:** After completing this exercise, you can:
- Review the board memo sample (`docs/examples/board-memo-sample.md`) for format reference
- Run `python -m src.board_report` to generate a memo from sample findings
- Practice translating technical findings from the risk register into business language
- Consider how CISO Assistant could generate board-ready risk summaries

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Executive Communication Strategy:** "I translate technical security findings into business language that executives can act on. For example, instead of discussing 'Event ID 4662 and DRSUAPI access,' I present 'Attacker-level access to our identity systems is plausible; client monitoring credibility at risk.' This enables informed decision-making without requiring technical expertise."

2. **Clear Actionable Asks:** "Every board memo includes specific, actionable asks. For a persistence finding, I ask the board to 'close the attack path and verify detections are working as expected' rather than generic requests for budget or tools. Specific asks enable clear accountability and measurable outcomes."

3. **Business Impact Focus:** "I focus on business impact rather than technical details. When presenting a prompt injection finding, I state 'AI lab leaked a secret; confirm isolation from client evidence' rather than explaining LLM vulnerabilities or input sanitization. The board needs to understand the business risk, not the technical exploit."

4. **Audience Adaptation:** "I adapt communication style to the audience. For technical teams, I provide detailed technical analysis. For the board, I provide business impact and clear asks. This audience adaptation ensures information is actionable at every level of the organization."

5. **Decision Support:** "My goal is to enable informed decision-making. A non-technical CEO should be able to act on my board memo without reading SIEM logs or understanding event IDs. If executives need technical expertise to understand my communication, I've failed to translate effectively."

---

## Task

1. Generate a memo from samples.
2. Rewrite the top three findings in **business language** (no jargon dump).
3. State one clear ask of the board for each.

## Answer key

1. Run from repo root after deps installed — see [`../examples/board-memo-sample.md`](../examples/board-memo-sample.md).
2. Examples:
   - DCSync alert → "Attacker-level access to our identity systems is plausible; client monitoring credibility at risk."
   - Prompt injection → "AI lab leaked a secret; confirm isolation from client evidence."
   - VR schtask → "Post-exploitation persistence on a member server — close the attack path and verify detections."
3. Asks: fund identity detection coverage; affirm lab isolation policy; accept residual only with dated review.

**Pass criteria:** A non-technical CEO could act on your memo without reading Elastic JSON.
