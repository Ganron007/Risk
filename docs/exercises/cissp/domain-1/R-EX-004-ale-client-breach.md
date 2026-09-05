# R-EX-004 — ALE for client evidence breach

**CISSP Reference:** Chapter 2, Section "Understand and Apply Risk Management Concepts", Pages 171-215  
**Exam Objective:** 1.2.3 Perform quantitative risk analysis using ALE  
**Study Guide Key Terms:** Quantitative risk analysis, Single Loss Expectancy (SLE), Annualized Rate of Occurrence (ARO), Annualized Loss Expectancy (ALE), cost-benefit analysis  
**Inputs:** [`../risk-register-baseline.md`](../risk-register-baseline.md), [`../regulatory-obligations.md`](../regulatory-obligations.md), [`../enterprise-context.md`](../enterprise-context.md), RISK-007

---

## Scenario Context

Cadre Corp is evaluating whether to invest $150,000 annually in additional controls to prevent client evidence breaches. The proposed controls include:
- Data Loss Prevention (DLP) for evidence storage and transfer
- Secure access gateway for evidence systems
- Enhanced chain-of-custody (CoC) tooling with audit trails

The company's current risk assessment (RISK-007) identifies client evidence compromise as a critical risk. Cadre Corp has $12M ARR and serves 120 enterprise clients, including several in the EU subject to GDPR. A client evidence breach could result in:
- GDPR fines (up to 4% of global turnover)
- Lost client retainers
- Legal liability and litigation costs
- Reputational damage affecting future business

The CISO has requested a quantitative risk analysis using Annualized Loss Expectancy (ALE) to determine if the $150K annual mitigation investment is cost-justified.

---

## Multiple-Choice Questions

**Question 1:** When calculating Single Loss Expectancy (SLE) for a client evidence breach, which of the following components must be included?

A. Only the direct cost of technical remediation  
B. Regulatory fines, lost retainers, legal costs, and reputational damage  
C. Only the cost of notifying affected clients  
D. The cost of replacing compromised hardware

**Question 2:** If the Annualized Rate of Occurrence (ARO) for a client evidence breach is estimated at 0.2 (once per 5 years), and the SLE is calculated at $800,000, what is the Annualized Loss Expectancy (ALE)?

A. $40,000  
B. $160,000  
C. $800,000  
D. $4,000,000

**Question 3:** When comparing the ALE ($160,000) to the mitigation cost ($150,000), which of the following correctly describes the cost-benefit relationship?

A. Mitigation is not cost-justified because it costs more than the ALE  
B. Mitigation is cost-justified because it costs less than the ALE  
C. Mitigation is cost-justified only if it reduces the ALE to zero  
D. Cost-benefit analysis cannot be applied to security investments

**Question 4:** Even if the ALE were lower than the mitigation cost, which of the following factors would still justify the $150K investment for Cadre Corp?

A. The company has excess budget that needs to be spent  
B. Cadre Corp's low risk appetite for client-evidence compromise  
C. The mitigation controls are required by ISO 27001  
D. The CISO prefers to invest in preventive controls

---

## Answer Explanations

**Answer 1: B**  
Regulatory fines, lost retainers, legal costs, and reputational damage must all be included in SLE calculation. SLE represents the total impact of a single loss event, not just technical costs. For a DFIR firm, a client evidence breach has multiple impact dimensions: GDPR fines (up to 4% of global turnover), lost client retainers (recurring revenue loss), legal liability (litigation and defense costs), and reputational damage (future business impact). Options A, C, and D are incomplete because they only consider specific cost components.

**Answer 2: B**  
ALE = ARO × SLE = 0.2 × $800,000 = $160,000. The Annualized Loss Expectancy represents the expected annual loss from a risk, calculated by multiplying the Single Loss Expectancy by the Annualized Rate of Occurrence. An ARO of 0.2 means the event is expected to occur once every 5 years on average, so the annualized impact is $160,000. Options A, C, and D are incorrect calculations.

**Answer 3: B**  
Mitigation is cost-justified because it costs less than the ALE. When mitigation cost ($150,000) is less than the ALE ($160,000), the investment provides positive return on investment by reducing expected annual losses. The cost-benefit principle suggests investing in controls when the mitigation cost is less than the expected loss. Option A is incorrect because the mitigation costs less than the ALE. Option C is incorrect because controls don't need to reduce risk to zero to be cost-justified. Option D is incorrect because cost-benefit analysis is a standard risk management practice.

**Answer 4: B**  
Cadre Corp's low risk appetite for client-evidence compromise would justify the investment even if ALE were lower than mitigation cost. Risk appetite represents the organization's willingness to accept risk. When risk appetite is low (as with client evidence for a DFIR firm), the organization may choose to mitigate risks even when the quantitative analysis suggests acceptance might be cost-effective. This is because some risks (existential business threats) cannot be fully captured in financial terms. Options A, C, and D are not valid justifications for investment decisions.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's risk management process by:

1. **Quantitative Analysis:** Applying ALE methodology to real business risks with illustrative financial impact
2. **Cost-Benefit Decision Making:** Using quantitative analysis to inform mitigation investment decisions
3. **Risk Appetite Integration:** Understanding when qualitative factors (risk appetite) override quantitative analysis
4. **GDPR Impact:** Incorporating regulatory fines into SLE calculations for EU client data

**Lab Connection:** After completing this exercise, you can:
- Review RISK-007 in the risk register (`docs/risk-register-baseline.md`) for client evidence breach details
- Examine the regulatory obligations document (`docs/regulatory-obligations.md`) for GDPR fine calculations
- Consider how DLP and access controls could be implemented in the CADRE lab environment
- Evaluate the cost-benefit of other mitigation investments using the same ALE methodology

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Quantitative + Qualitative Approach:** "I use quantitative risk analysis (ALE) to inform investment decisions, but I also consider qualitative factors like risk appetite. For client evidence breach, the ALE of $160K justified the $150K mitigation investment, but even if ALE were lower, our low risk appetite for client-evidence compromise would still drive mitigation."

2. **SLE Component Analysis:** "When calculating Single Loss Expectancy, I ensure all impact dimensions are included: regulatory fines, lost revenue, legal costs, and reputational damage. For DFIR firms, reputational damage is particularly significant because client trust is the foundation of the business model."

3. **Cost-Benefit Communication:** "When presenting mitigation investments to the board, I translate quantitative analysis into business terms. 'The $150K investment reduces expected annual losses from $160K to near-zero, providing positive ROI while protecting our client relationships and regulatory compliance.'"

4. **Risk Appetite Override:** "Quantitative analysis is a tool, not a decision rule. When risk appetite is low for existential threats like client evidence compromise, we may invest in mitigation even when the numbers suggest acceptance could be cost-effective. Some risks cannot be fully captured in financial terms."

5. **Regulatory Impact Inclusion:** "For DFIR firms handling EU client data, GDPR fines significantly impact SLE calculations. At up to 4% of global turnover, regulatory fines can dwarf other cost components. This makes GDPR compliance a critical factor in quantitative risk analysis."

---

## Task

Use illustrative numbers (label them as such):

1. Define SLE for a single EU-client evidence breach (fines + lost retainers + legal).
2. Assume ARO = 0.2 (once per 5 years). Compute ALE.
3. Compare ALE to a $150K/year mitigation (DLP + access gateway + CoC tooling). Recommend yes/no.

## Answer key (example numbers)

1. SLE = $800K (illustrative: regulatory + two lost retainers + legal).
2. ALE = 0.2 × $800K = **$160K/year**.
3. Mitigation $150K/year < ALE → **cost-justified mitigate** (plus appetite is low regardless of ALE).

**Exam tip:** Quantitative supports decisions; appetite can still force mitigate when ALE is lower.
