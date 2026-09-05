# R-EX-084 — DevSecOps pipeline integration

**CISSP Reference:** Chapter 20, Section "Systems Development Controls"; Chapter 21, Section "Malicious Code"  
**Exam Objective:** 8.1.2 Integrate security into SDLC; 8.3.1 Implement DevSecOps  
**Study Guide Key Terms:** DevSecOps, CI/CD pipeline, shift-left, security as code, pipeline security, immutable infrastructure  

---

## Scenario Context

Cadre Corp's development pipeline for the client portal and internal tools (Praxis, DFIR-Nexus) currently works like this: developers write code → push to git → manual testing → deploy. Security testing happens AFTER deployment (the pentest that found SQL injection and XSS). The CISO wants to "shift left" — integrate security testing earlier in the pipeline so vulnerabilities are found before they reach production.

The development team is resistant: "Adding security scans will slow down our deploys." The CISO counters: "The pentest finding SQL injection in production already slowed us down — by weeks of emergency remediation."

---

## Multiple-Choice Questions

**Question 1:** "Shift-left" in DevSecOps means:

A. Moving all development work to earlier time zones  
B. Integrating security testing earlier in the development lifecycle — during coding and commit stages rather than waiting until pre-production or post-deployment  
C. Shifting responsibility for security entirely to developers  
D. Moving security tools to the left side of the data center

**Question 2:** In a DevSecOps pipeline, which security checks should run at the commit/pull request stage (earliest)?

A. Full penetration test with external testers  
B. Automated SAST (static analysis), secret detection, dependency vulnerability scanning, and IaC security scanning — fast, automated checks that provide immediate feedback to developers  
C. Manual security architecture review  
D. SOC 2 compliance audit

**Question 3:** What is the PRIMARY argument for integrating security into CI/CD rather than testing after deployment?

A. It's cheaper to hire security engineers than developers  
B. Cost of remediation — fixing a vulnerability found during coding costs ~1x; found during QA costs ~5x; found in production costs ~30x (plus potential breach costs, reputational damage, and emergency response)  
C. CI/CD pipelines are faster than manual testing  
D. Post-deployment testing requires more expensive tools

---

## Answer Explanations

**Answer 1: B**  
**Shift-left** moves security testing to earlier pipeline stages. Instead of: code → test → deploy → security scan → fix (expensive, slow), it's: code → security scan (instant feedback) → fix → test → deploy. The earlier a vulnerability is found, the cheaper and faster it is to fix. It doesn't mean developers own all security (C) — it means security is automated and integrated into their workflow.

**Answer 2: B**  
At commit/PR time, the pipeline should run **fast, automated checks**: SAST (code analysis for injection, XSS, hardcoded secrets), SCA (dependency vulnerabilities — see R-EX-086), secret detection (API keys, passwords in code), and IaC scanning (misconfigurations in Dockerfiles, Ansible playbooks). These complete in minutes, not hours. Full pentests and manual reviews happen later in the pipeline when the code is more stable.

**Answer 3: B**  
The **cost-of-remediation curve** is the primary economic argument for DevSecOps. Finding and fixing a vulnerability during development (developer is still in the code, context is fresh) costs a fraction of fixing it in production (emergency change, potential downtime, incident response, possible breach notification). The ratio (1x → 5x → 30x) is well-documented in industry studies.

---

## Cadre Corp Application

1. **Pipeline Security Gates:** Add to the CI/CD pipeline for client portal and DFIR-Nexus: (a) `praxis scan` for secret detection and code patterns, (b) `pip-audit` or Dependabot for dependency vulnerabilities, (c) `ansible-lint` + `checkov` for IaC security, (d) SAST tool (Semgrep or Bandit) for code analysis. Any critical finding → pipeline fails → developer must fix before merge.

2. **Immutable Infrastructure:** Move toward treating VMs as immutable — deploy from Ansible (IaC), never manually modify. This makes security baseline enforcement automatic and drift detection simpler.

3. **Developer Experience:** Keep pipeline checks under 10 minutes. If security gates are too slow, developers will bypass them. Fast feedback = adopted; slow feedback = ignored.

---

## Interview Talking Points

1. **Finding Bugs in Prod Is 30x More Expensive:** "Every CISO should be able to quote the cost-of-remediation curve to their board. It's the business case for DevSecOps: shift-left isn't about tools — it's about finding problems when they're cheapest to fix."

2. **Security Gates Must Be Fast or They'll Be Bypassed:** "A security scan that takes 2 hours in the CI pipeline will be disabled by developers within a week. Security must be fast and actionable. Under 10 minutes, clear output, no false positives that require manual triage."
