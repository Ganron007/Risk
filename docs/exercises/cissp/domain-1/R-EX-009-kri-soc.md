# R-EX-009 — SOC KRIs and KPIs

**CISSP Reference:** Chapter 16, Section "Implementing Security Management Processes and Collecting Security Process Data", Pages 1201-1205  
**Exam Objective:** 1.7.1 Establish and monitor security metrics  
**Study Guide Key Terms:** Key Risk Indicators (KRIs), Key Performance Indicators (KPIs), leading indicators, lagging indicators, security metrics, risk monitoring  
**Inputs:** [`../risk-appetite-statement.md`](../risk-appetite-statement.md), [`../enterprise-context.md`](../enterprise-context.md), AST-010–012

---

## Scenario Context

Cadre Corp's SOC (Security Operations Center) is responsible for 24/7 monitoring of 120 client retainers, managing the SIEM (AST-010), Velociraptor endpoint response (AST-011), and detection engineering. The CISO has requested the development of security metrics to monitor both risk exposure and operational performance.

The current state includes:
- No formal metrics program
- Ad-hoc reporting based on incident volume
- No leading indicators for risk prediction
- No standardized KPIs for SOC performance
- Risk appetite statement with qualitative thresholds but no quantitative metrics

The CISO needs to define:
- **Key Risk Indicators (KRIs):** Metrics that indicate risk exposure and potential future issues
- **Key Performance Indicators (KPIs):** Metrics that measure operational performance and efficiency
- **Leading vs. Lagging classification:** Leading indicators predict future issues, lagging indicators measure past performance

As the Risk Manager, you need to define three KRIs and three KPIs for the Cadre Corp SOC, classifying each as leading or lagging.

---

## Multiple-Choice Questions

**Question 1:** Which of the following best describes the difference between a KRI and a KPI?

A. KRIs measure operational efficiency, KPIs measure risk exposure  
B. KRIs indicate risk exposure, KPIs indicate operational performance  
C. KRIs are leading indicators, KPIs are lagging indicators  
D. KRIs are for executives, KPIs are for operational staff

**Question 2:** Which of the following is an example of a **leading** KRI for the Cadre Corp SOC?

A. Number of incidents resolved in the past month  
B. Percentage of endpoints without Velociraptor agent  
C. Mean Time to Detect (MTTD) for the past quarter  
D. Total SIEM downtime hours last month

**Question 3:** Which of the following is an example of a **lagging** KPI for the Cadre Corp SOC?

A. Open Critical identity alerts older than 14 days  
B. Percentage of endpoints without agent coverage  
C. Mean Time to Respond (MTTR) for the past month  
D. Number of detection rules tested this month

**Question 4:** When presenting SOC metrics to the board, which of the following is the most appropriate approach?

A. Present only lagging indicators because they are more accurate  
B. Present a mix of leading and lagging indicators with clear explanations  
C. Present only technical metrics without business context  
D. Present only KPIs and omit KRIs to avoid confusion

---

## Answer Explanations

**Answer 1: B**  
KRIs indicate risk exposure, KPIs indicate operational performance. KRIs (Key Risk Indicators) measure the level of risk the organization is exposed to, while KPIs (Key Performance Indicators) measure how well processes are performing. Option A is incorrect because it reverses the definitions. Option C is incorrect because both KRIs and KPIs can be leading or lagging. Option D is incorrect because both metrics types are relevant for multiple audiences.

**Answer 2: B**  
Percentage of endpoints without Velociraptor agent is a leading KRI because it indicates future risk—if endpoints lack monitoring, future incidents may go undetected. This metric predicts potential issues before they occur. Options A, C, and D are lagging indicators because they measure past performance (incidents resolved, MTTD, downtime).

**Answer 3: C**  
Mean Time to Respond (MTTR) for the past month is a lagging KPI because it measures past operational performance. Lagging indicators look backward at what has already happened. Options A and B are leading KRIs because they predict future risk. Option D is a leading indicator because it measures proactive testing activity.

**Answer 4: B**  
Presenting a mix of leading and lagging indicators with clear explanations is the most appropriate approach. Leading indicators show where the organization is headed (future risk), while lagging indicators show where it has been (past performance). This comprehensive view enables informed decision-making. Option A is incorrect because lagging indicators alone don't predict future issues. Option C is incorrect because business context is essential for board communication. Option D is incorrect because KRIs are critical for risk visibility.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's SOC monitoring by:

1. **Metrics Program Development:** Establishing a structured approach to security metrics
2. **Risk Monitoring:** Using KRIs to track risk exposure and predict future issues
3. **Performance Measurement:** Using KPIs to measure SOC operational efficiency
4. **Leading vs. Lagging:** Understanding the difference between predictive and retrospective metrics

**Lab Connection:** After completing this exercise, you can:
- Review the risk appetite statement (`docs/risk-appetite-statement.md`) to inform KRI thresholds
- Examine the SIEM (AST-010) and Velociraptor (AST-011) configurations to identify available metrics
- Consider how CISO Assistant could track KRIs and KPIs
- Evaluate current SOC performance against the proposed metrics

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **KRI vs. KPI Distinction:** "I clearly distinguish between KRIs and KPIs. KRIs indicate risk exposure—like open Critical identity alerts older than 14 days—while KPIs indicate operational performance—like Mean Time to Detect. This distinction ensures we're monitoring both risk and efficiency."

2. **Leading vs. Lagging Indicators:** "I use a mix of leading and lagging indicators for comprehensive visibility. Leading indicators like percentage of endpoints without agent coverage predict future risk, while lagging indicators like MTTD measure past performance. This combination enables proactive risk management."

3. **Risk Appetite Alignment:** "I align KRIs with our risk appetite statement. For example, if our risk appetite specifies zero Critical alerts older than 14 days, the KRI tracks compliance with that threshold. This quantitative approach makes risk appetite measurable and actionable."

4. **Board Communication Strategy:** "When presenting metrics to the board, I provide a mix of leading and lagging indicators with clear business context. Leading indicators show where we're headed, lagging indicators show where we've been. This comprehensive view enables informed strategic decisions."

5. **Metrics-Driven Improvement:** "I use metrics to drive continuous improvement. If the KRI for open Critical alerts exceeds our threshold, I investigate root causes and implement corrective actions. If the KPI for MTTD is trending negatively, I review detection processes and optimize response procedures. Metrics drive data-driven decisions."

---

## Task

Define three KRIs and three KPIs for Cadre Corp SOC. Mark which are leading vs lagging.

## Answer key (examples)

**KRIs (risk):** open Critical identity alerts >14d (leading); SIEM downtime hours/month (lagging); % endpoints without agent (leading).  
**KPIs (performance):** MTTD, MTTR, % retainer reports on time.

**Exam tip:** KRI indicates risk exposure; KPI indicates operational performance — don't swap them.
