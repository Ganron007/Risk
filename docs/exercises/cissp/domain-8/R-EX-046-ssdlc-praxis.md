# R-EX-046 — Secure SDLC: Praxis as a CI/CD security gate

**CISSP Reference:** Chapter 20, Sections "Systems Development Controls", "Testing Software"; Chapter 21, Section "Malicious Code and Application Attacks"  
**Exam Objective:** 8.1.1 Implement secure coding practices; 8.1.2 Integrate security into the SDLC; 8.2.1 Understand application vulnerabilities  
**Study Guide Key Terms:** Secure SDLC, CI/CD security gate, shift-left, SAST in pipeline, security as code, fail-open vs fail-closed, security acceptance criteria  
**Inputs:** Praxis CI integration, `CTL-PRAXIS-SCAN`, DarkAI release pipeline

---

## Scenario Context

Cadre Corp's DarkAI research team develops and releases containerized LLM applications weekly. The current release process: developer writes code → pushes to git → manual review (sometimes) → Docker build → push to registry → deploy. Security testing is ad-hoc — the team lead "looks at the code" when they remember.

The CISO mandates that `praxis scan ci` run as a CI/CD gate before any DarkAI container image is built. The scan checks for: hardcoded secrets, vulnerable dependency patterns, OWASP Top 10 anti-patterns in prompt handling code, and insecure Dockerfile configurations (running as root, exposed ports, missing HEALTHCHECK).

The development team pushes back: "This will slow down our weekly releases. What if a scan fails on a Friday — do we block the release?" The CISO counters: "What if a hardcoded API key ships to production on a Friday — do we explain to the board why DarkAI leaked secrets over the weekend?"

---

## Multiple-Choice Questions

**Question 1:** Where in the SDLC should `praxis scan ci` execute for maximum effectiveness?

A. After the Docker image is built and pushed to the registry  
B. Pre-merge / pre-build — before code is merged to the main branch and before the Docker image is built; this is "shift-left" — catching vulnerabilities at the earliest, cheapest stage  
C. After the release is deployed to production  
D. Only during annual security audits

**Question 2:** What should be the failure criteria — when should the pipeline BLOCK a release?

A. Never — security scans should be informational only  
B. Critical/High severity findings block the pipeline — hardcoded secrets, known vulnerable dependency versions with CVSS ≥ 9.0, and OWASP injection patterns in prompt handlers should prevent the build; Medium/Low findings warn but don't block  
C. Any finding, regardless of severity, blocks the pipeline  
D. Only findings in production code block; test code findings are exempt

**Question 3:** The "Friday afternoon release" problem (pipeline blocks, team wants to ship) should be handled by:

A. Disabling the security scan for Friday releases — convenience over security  
B. A pre-defined exception process: the team lead can override the block WITH documented justification, CISO notification, and a remediation ticket created before the override — the release proceeds but the risk is formally accepted, not ignored; the override is audited monthly  
C. Always allowing the release — security can wait until Monday  
D. Requiring the CISO's personal approval for every Friday release

**Question 4:** What evidence does `praxis scan ci` provide for SOC 2 audit purposes?

A. No evidence — CI scans are not auditable  
B. SARIF output artifacts stored as CI build artifacts — these prove: (a) a security scan ran at this commit, (b) the findings at that point in time, (c) whether the pipeline passed or was overridden (with justification); this demonstrates that security testing is integrated into the SDLC, not performed ad-hoc  
C. Only the pass/fail status, not the findings  
D. The scan results are stored only in the developer's local machine

---

## Answer Explanations

**Answer 1: B**  
**Pre-merge/pre-build** is the earliest and cheapest point to catch vulnerabilities. A secret found during coding costs minutes to fix (rotate the secret, remove from code). The same secret found in a deployed container costs hours (incident response, rotation, redeployment). This is the "shift-left" principle in practice — move security testing as early in the SDLC as possible. Post-build (A) means the vulnerable code is already packaged. Post-deploy (C) means it's already in production.

**Answer 2: B**  
**Risk-based failure criteria** balance security with development velocity. Hardcoded secrets (API keys, tokens, passwords) are never acceptable — they indicate a real credential has been compromised. Critical dependency vulnerabilities (CVSS ≥ 9.0, known exploits) should block — the risk of shipping known-exploitable code is too high. Injection patterns in code handling untrusted input (prompt injection vectors) should block — these are the primary attack surface for LLM applications. Blocking on every finding (C) creates alert fatigue and developer resentment. Exempting test code (D) is dangerous — secrets in test code are still in git history.

**Answer 3: B**  
A **documented override process** acknowledges reality (releases sometimes need to ship) while maintaining security accountability. The override: (a) documents WHY the risk is accepted (e.g., "finding is a false positive in test config — verified no real secret"), (b) notifies the CISO (visibility), (c) creates a remediation ticket (the risk isn't forgotten — it's tracked), (d) is audited monthly (overuse of overrides indicates a process problem). Disabling the scan (A) removes the control entirely. Always allowing (C) makes the scan meaningless. CISO approval for every release (D) doesn't scale.

**Answer 4: B**  
**SARIF artifacts as CI build evidence** provide auditable proof of security testing integration. For SOC 2: the auditor asks "do you perform security testing during development?" The CI pipeline artifacts demonstrate: (a) testing occurred (build timestamp, commit hash), (b) what was tested (SARIF rule set), (c) what was found (findings with severity), (d) what was done (pipeline passed = all findings addressed or accepted). This is automated, consistent evidence — far stronger than "the team lead reviews code when they remember."

---

## Cadre Corp Application

1. **Security Gate Implementation:** Add `praxis scan ci` to the CI pipeline for DarkAI, DFIR-Nexus, and client portal repositories. Configure: Critical/High → block merge; Medium → warn + ticket; Low → informational. Store SARIF artifacts with build logs. Review override usage monthly.

2. **Exception Process:** Document: override requires team lead approval + justification in the override comment + automatic CISO notification + linked remediation ticket. Override expires after 30 days — if not remediated, the finding re-blocks the pipeline.

3. **Pipeline Evolution:** Start with secret detection + dependency scanning (highest value, lowest false positive rate). Add code pattern scanning (injection, XSS) after tuning false positives. Add Dockerfile security scanning (running as root, exposed ports) as maturity increases.

---

## Interview Talking Points

1. **Security Gates Are Contracts, Not Obstacles:** "The CI pipeline is where the security team and development team negotiate risk automatically. The rules are defined in advance, applied consistently, and generate auditable evidence. The developer doesn't argue with the security team — they argue with the SARIF output. And the SARIF output doesn't get tired, doesn't play favorites, and doesn't forget."

2. **Override Is Acceptance, Not Avoidance:** "When a pipeline blocks on Friday and the team overrides to ship, that's a risk acceptance — not a bug in the pipeline. The override documents who accepted the risk, why, and creates a remediation ticket. If overrides become routine, the failure criteria need tuning — but the override process ensures no risk is accepted invisibly."
