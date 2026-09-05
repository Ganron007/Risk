# R-EX-005 — Treatment: DarkAI lab risk

**CISSP Reference:** Chapter 2, Section "Understand and Apply Risk Management Concepts", Pages 171-215  
**Exam Objective:** 1.2.4 Select appropriate risk treatment options  
**Study Guide Key Terms:** Risk treatment, risk acceptance, risk mitigation, risk transfer, risk avoidance, compensating controls, risk appetite  
**Inputs:** [`../risk-register-baseline.md`](../risk-register-baseline.md), [`../enterprise-context.md`](../enterprise-context.md), [`../risk-appetite-statement.md`](../risk-appetite-statement.md), RISK-012/013, finding-darkai-001

---

## Scenario Context

Cadre Corp operates the DarkAI research lab (AST-035) as an isolated Docker environment on the `172.20.0.0/24` network for testing AI security scenarios and prompt injection techniques. The lab is designed to be isolated from the production estate (`192.168.77.0/24`) to prevent research activities from affecting client evidence or operational systems.

A recent security finding (finding-darkai-001) identified a prompt injection vulnerability in the DarkAI chatbot that could allow attackers to:
- Extract lab secrets and API keys from the chatbot context
- Potentially access client evidence if network isolation fails
- Bypass safety controls and generate malicious outputs

The risk register entries RISK-012 (DarkAI lab breakout) and RISK-013 (Prompt-injection / LLM abuse) document these concerns. Cadre Corp's risk appetite is moderate for research labs—higher than for client evidence systems, but not unlimited.

The CISO must determine the appropriate risk treatment (Accept, Mitigate, Transfer, Avoid) and specify any compensating controls required.

---

## Multiple-Choice Questions

**Question 1:** Given Cadre Corp's moderate risk appetite for research labs and the prompt injection finding, which of the following is the most appropriate initial risk treatment?

A. Accept the risk because research labs are expected to have vulnerabilities  
B. Mitigate the risk through prompt injection defenses and secret hygiene  
C. Transfer the risk through cyber insurance  
D. Avoid the risk by shutting down the DarkAI lab

**Question 2:** If the risk treatment is changed to Accept after mitigation, which of the following compensating controls would be required?

A. No controls needed if the risk is accepted  
B. Network isolation, no client data access, secret rotation, and input validation  
C. Only network isolation is required  
D. Annual penetration testing of the lab

**Question 3:** Under what condition would Cadre Corp need to choose the Avoid risk treatment (shut down the lab)?

A. When the lab becomes too expensive to operate  
B. When client evidence is found in the lab network or isolation controls fail  
C. When the lab cannot be patched within 30 days  
D. When the CISO decides to focus on other priorities

**Question 4:** Which of the following best describes the relationship between Cadre Corp's moderate risk appetite for research labs and the DarkAI prompt injection risk?

A. Moderate appetite means all research lab risks should be accepted  
B. Moderate appetite allows for some risk acceptance but not for existential threats like secret leakage  
C. Moderate appetite is irrelevant to risk treatment decisions  
D. Moderate appetite means the lab should be shut down

---

## Answer Explanations

**Answer 1: B**  
Mitigate the risk through prompt injection defenses and secret hygiene is the most appropriate initial treatment. Even with moderate risk appetite for research labs, prompt injection vulnerabilities that could leak secrets or access client data require mitigation. The moderate appetite allows for some residual risk after mitigation, but not for accepting the initial vulnerability. Acceptance (A) is inappropriate because the risk is not yet mitigated. Transfer (C) through insurance doesn't address the technical vulnerability. Avoidance (D) is premature because the lab can be secured.

**Answer 2: B**  
Network isolation, no client data access, secret rotation, and input validation are required compensating controls if the risk is accepted after mitigation. Risk acceptance should only occur with appropriate compensating controls in place. These controls ensure that even if prompt injection occurs, the impact is limited (no client data access, isolated network) and the attack surface is reduced (secret rotation, input validation). Option A is incorrect because accepted risks still require controls. Option C is insufficient because isolation alone doesn't prevent secret leakage. Option D is a good practice but not sufficient for risk acceptance.

**Answer 3: B**  
Avoid the risk (shut down the lab) is required when client evidence is found in the lab network or isolation controls fail. This represents an existential threat to Cadre Corp's business model—client evidence in an uncontrolled research environment violates the low risk appetite for client data. The lab must be shut down until the isolation is verified and any client data is removed. Options A, C, and D are not valid reasons for risk avoidance.

**Answer 4: B**  
Moderate appetite allows for some risk acceptance but not for existential threats like secret leakage. Risk appetite is not binary—it varies by system and impact. For research labs, Cadre Corp has moderate appetite, meaning some residual risk is acceptable after mitigation. However, risks that could leak secrets or access client data (existential threats) still require mitigation regardless of the moderate appetite. Option A is incorrect because moderate appetite doesn't mean blanket acceptance. Option C is incorrect because risk appetite directly informs treatment decisions. Option D is incorrect because moderate appetite supports continued lab operation with appropriate controls.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's risk treatment decisions by:

1. **Risk Treatment Framework:** Applying the four treatment options (Accept, Mitigate, Transfer, Avoid) to real research lab risks
2. **Risk Appetite Integration:** Understanding how moderate appetite for research labs differs from low appetite for client systems
3. **Compensating Controls:** Identifying specific controls required for risk acceptance
4. **Avoidance Criteria:** Establishing clear conditions for when systems must be shut down

**Lab Connection:** After completing this exercise, you can:
- Review RISK-012 and RISK-013 in the risk register (`docs/risk-register-baseline.md`)
- Examine the DarkAI lab architecture (AST-035) in the CADRE environment
- Verify network isolation between `172.20.0.0/24` (DarkAI) and `192.168.77.0/24` (production)
- Evaluate prompt injection defenses and secret hygiene practices in the lab

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Risk Treatment Decision Framework:** "I use a structured framework for risk treatment decisions: Mitigate first to reduce risk to acceptable levels, then consider Accept with compensating controls, Transfer for residual financial risk, and Avoid only for existential threats. For DarkAI, I chose Mitigate initially because prompt injection could leak secrets."

2. **Risk Appetite Nuance:** "Risk appetite is not one-size-fits-all. Cadre Corp has moderate appetite for research labs but low appetite for client evidence systems. This nuanced approach allows us to accept some research risk after mitigation while still protecting critical business functions."

3. **Compensating Control Requirements:** "Risk acceptance is never unconditional. Even when we accept residual risk in the DarkAI lab, we require compensating controls: network isolation, no client data access, secret rotation, and input validation. These controls ensure the accepted risk remains within our appetite."

4. **Avoidance Criteria:** "I establish clear criteria for risk avoidance—shutting down systems when they pose existential threats. For DarkAI, finding client evidence in the lab network or isolation failure would trigger immediate shutdown because this violates our low risk appetite for client data."

5. **Research Lab Risk Philosophy:** "Research labs need some operational freedom, but not at the expense of security. Our moderate appetite for research labs balances innovation with risk management—we accept calculated risks after mitigation, but not existential threats that could compromise client trust."

---

## Task

1. Choose Accept / Mitigate / Transfer / Avoid for finding-darkai-001.
2. List compensating controls required if Accept.
3. State the condition that would force Avoid (shut lab).

## Answer key

1. **Mitigate** (prompt injection + secret hygiene); residual research risk may be **Accept** only after fix.
2. CTL-LAB-ISOLATION, no AST-030 data, secret rotation, Praxis gate, disable STUB_INJECTABLE in shared demos.
3. Evidence of client data in `172.20.0.0/24` or bridge to `192.168.77.0/24` without capstone controls → **Avoid** until redesigned.

**Appetite:** Moderate for isolated research — not a blank check for secret leakage.
