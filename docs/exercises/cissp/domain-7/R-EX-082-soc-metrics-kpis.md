# R-EX-082 — Security operations center (SOC) metrics and KPIs

**CISSP Reference:** Chapter 16, Section "Foundational Security Operations Concepts"; Chapter 17, Section "Logging and Monitoring"  
**Exam Objective:** 7.1.1 Manage security operations; 7.2.3 Measure SOC effectiveness  
**Study Guide Key Terms:** SOC metrics, KPIs, KRIs, MTTD, MTTR, alert volume, false positive rate, analyst utilization, dwell time  

---

## Scenario Context

Cadre Corp's SOC team (10 analysts) handles alerts from Elastic, Suricata, Zeek, and Velociraptor. The CISO has asked for SOC performance metrics to justify the SOC budget to the board. The SOC Lead provided these numbers:

- "We handle about 500 alerts per day" (but can't say how many are false positives).
- "We respond pretty quickly" (but has no measurement of detection or response time).
- "The team is busy" (but can't quantify analyst utilization or burnout risk).

The board needs data, not adjectives. The CISO asks you to define meaningful SOC metrics.

---

## Multiple-Choice Questions

**Question 1:** MTTD (Mean Time to Detect) measures:

A. How long it takes to resolve an incident after detection  
B. The average time between an attacker's initial action and the SOC's detection of that action — shorter MTTD means faster detection  
C. How long analysts spend on each alert  
D. The time between tool deployments

**Question 2:** Why is alert volume alone a poor SOC metric?

A. It's too complex to calculate  
B. High alert volume could mean good detection coverage OR overwhelming false positives — without false positive rate and alert quality context, volume is meaningless; 500 alerts/day with 98% false positives is a tuning problem, not a success metric  
C. Alert volume is only relevant for compliance  
D. Alert volume is always accurate and meaningful

**Question 3:** Dwell time in cybersecurity refers to:

A. How long analysts spend in the SOC building  
B. The time between an attacker's initial compromise and detection/containment — if an attacker was in the network for 73 days before being detected, dwell time = 73 days  
C. How long it takes to deploy a new security tool  
D. The time security cameras retain footage

---

## Answer Explanations

**Answer 1: B**  
**MTTD measures detection speed**: from initial malicious action to SOC awareness. If an attacker compromises ws01 at 08:00 and Suricata fires an alert at 08:03, MTTD = 3 minutes. If the compromise happened 73 days ago and was only found during a quarterly scan, MTTD = 73 days. Lower MTTD = faster detection = less time for attacker to accomplish objectives.

**Answer 2: B**  
**Alert volume needs quality context**. 500 alerts/day could mean: (a) excellent detection coverage catching real attacks, or (b) poorly tuned rules generating noise that analysts ignore. Metrics that complement volume: false positive rate (aim for <20%), true positive rate, alert-to-incident conversion rate, and analyst time spent on false positives (burnout indicator).

**Answer 3: B**  
**Dwell time is the attacker's undetected residency period**. Industry median is often measured in weeks or months. Reducing dwell time is the ultimate SOC effectiveness metric — it captures how well detection, triage, and response work together. MTTD + MTTR should be less than the attacker's time-to-objective; otherwise, the attacker wins before you respond.

---

## Cadre Corp Application

1. **SOC Dashboard Metrics:** Build in Elastic: (a) alerts per day (by severity, by source), (b) MTTD (by alert type), (c) MTTR (Mean Time to Respond/Remediate), (d) false positive rate (alerts closed as FP / total alerts), (e) dwell time estimate (for campaign exercises where ground truth is known), (f) analyst workload (alerts per analyst per shift).

2. **Campaign as SOC Benchmark:** Each campaign phase provides known ground truth: the attack happens at time X, is detected at time Y, contained at time Z. MTTD = Y - X, MTTR = Z - Y. This is a controlled, repeatable SOC performance measurement.

3. **Alert Tuning Feedback Loop:** Every false positive closed by an analyst should be reviewed weekly: can the rule be tuned? Can an exception be documented? This drives the FP rate down over time and prevents alert fatigue.

---

## Interview Talking Points

1. **"We're Busy" Is Not a Metric:** "When the board asks for SOC performance and the answer is 'we handle a lot of alerts,' that's not data — that's an anecdote. MTTD, MTTR, dwell time, and false positive rate. These are numbers the board can track quarter over quarter."

2. **Dwell Time Is the Ultimate Score:** "All the tools, all the alerts, all the analysts — they serve one purpose: reduce dwell time. How long was the attacker in our network before we knew? If that number isn't trending down, we're not improving."
