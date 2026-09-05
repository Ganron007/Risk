# R-EX-032 — Security testing results review (SARIF analysis)

**CISSP Reference:** Chapter 15, Sections "Testing Software", "Collecting Security Process Data", Pages 1100–1125; Chapter 20, Section "Testing Software"  
**Exam Objective:** 6.1.3 Analyze security testing results; 6.2.1 Interpret assessment findings  
**Study Guide Key Terms:** SARIF (Static Analysis Results Interchange Format), SAST findings, false positive triage, severity scoring, finding lifecycle, remediation prioritization  
**Inputs:** `samples/findings/praxis-sarif-sample.sarif`, `src/adapters.py`

---

## Scenario Context

Cadre Corp runs Praxis (`praxis scan`) as a CI/CD security gate against internal tool repositories (DFIR-Nexus, client portal, Ansible playbooks). The scan produces SARIF output — a standardized JSON format for static analysis results. A recent scan of the DFIR-Nexus repository produced 47 findings across three severity levels.

The SOC Lead has asked you to triage these findings:

1. **3 Critical findings:** Hardcoded API key patterns in test fixtures, an AWS secret key in a commented-out debug line, and a database connection string with embedded credentials in a configuration example.
2. **12 High findings:** Insecure cryptographic algorithms (MD5 used for checksums in legacy code), missing input validation in API handlers, and potential path traversal in file serving endpoints.
3. **32 Medium/Low findings:** Unused variables, missing docstrings, overly broad exception handling.

The challenge: not all SARIF findings are exploitable. Some are in test code (not deployed), some are false positives (the "hardcoded key" is a documentation example with a placeholder value), and some are real vulnerabilities that need immediate remediation.

---

## Multiple-Choice Questions

**Question 1:** When triaging SAST findings, what is the correct approach to a Critical finding in test code (not deployed to production)?

A. Ignore it — test code is never a security risk  
B. Assess the risk realistically — if the test uses a placeholder/example key (not a real secret), it's a false positive; if it uses a real key, it's a real finding regardless of being in test code — test files get committed to git, copied to developer machines, and may be accessible in CI logs  
C. All test-code findings should be treated as production findings  
D. Delete all test files containing security findings

**Question 2:** A SARIF finding of "hardcoded API key" in a commented-out debug line is:

A. A false positive — commented code doesn't execute  
B. A real finding — commented-out code still exists in the repository, may be uncommented accidentally, and the key (if real) is still exposed in git history forever unless rotated  
C. Only relevant if the code is in the main branch  
D. Automatically mitigated by the comment syntax

**Question 3:** When prioritizing 47 findings for remediation, which framework should guide the order?

A. Fix all Critical findings first, then High, then Medium — regardless of context  
B. Risk-based prioritization: (1) exploitable findings in production code with real secrets → immediate remediation, (2) exploitable findings in non-production code → scheduled remediation, (3) non-exploitable findings (false positives, test-only placeholders) → document and suppress  
C. Fix findings in alphabetical order by file name  
D. Fix the easiest findings first to reduce the count quickly

**Question 4:** What is the appropriate lifecycle for a SAST finding that is determined to be a false positive?

A. Delete it from the SARIF output  
B. Document the false positive determination with justification, suppress it in the SAST tool with a comment annotation or suppression rule, and periodically review suppressed findings to ensure they remain false positives  
C. Leave it as an open finding forever — better safe than sorry  
D. Convert it to a "Low" severity so it doesn't block CI

---

## Answer Explanations

**Answer 1: B**  
**Context matters, but repository presence matters more.** A test file with `API_KEY = "test-placeholder-123"` is a false positive — no real secret is exposed. But a test file with `API_KEY = "sk-abc123realproductionkey"` is a real finding — the key is in git history, on every developer's machine, and potentially in CI logs. Test code is not exempt from security review just because it doesn't run in production. The key's authenticity determines severity, not the file's deployment status.

**Answer 2: B**  
Commented-out code with real secrets is **still a finding**. The secret: (a) exists in git history — even if the line is later deleted, it's recoverable via `git log`, (b) may be uncommented accidentally during debugging, (c) indicates a developer had access to a real secret and handled it insecurely (wrote it in source code, even if commented). If the key is real, it must be rotated immediately regardless of the code's comment status.

**Answer 3: B**  
**Risk-based prioritization** focuses remediation effort where it reduces the most risk. Criteria: (a) Is the finding in production-deployed code? (b) Is a real secret exposed? (c) Is the vulnerability exploitable without authentication? (d) What's the blast radius? A real API key in production code is urgent; a placeholder key in test code is a documentation task. Fixing by severity alone (A) wastes time on high-severity false positives. Fixing easiest first (D) optimizes for metrics, not security.

**Answer 4: B**  
False positives should be **documented and suppressed, not deleted**. Suppression with justification: (a) proves the finding was reviewed and intentionally closed (audit trail), (b) prevents the finding from re-appearing on the next scan (the suppression rule persists), (c) enables periodic review of suppressions (are they still false positives?). Deleting from output (A) means it re-appears next scan. Leaving open (C) creates alert fatigue. Downgrading severity (D) hides the finding without the audit trail of a documented false positive determination.

---

## Cadre Corp Application

1. **SARIF Ingestion Pipeline:** Use `src/adapters.py` → `sarif_to_findings()` to convert Praxis SARIF output to the unified finding schema. This enables: (a) consistent scoring across different tools (Praxis, pip-audit, manual pentest), (b) centralized finding lifecycle tracking, (c) board memo generation from aggregated findings.

2. **Triage Workflow:** For each scan: (a) auto-classify: Critical/High → immediate review, Medium/Low → batch review, (b) for each finding: determine if exploitable (real secret? production code? reachable?), (c) exploitable → open remediation ticket with SLA, (d) false positive → document justification + suppress + periodic review.

3. **Secret Rotation:** Any SARIF finding of a real secret (API key, password, token) triggers immediate secret rotation REGARDLESS of whether the code is in production, test, or commented out. The secret is compromised the moment it hits git. Rotation is the first action; code cleanup is second.

---

## Interview Talking Points

1. **Test Code Is Source Code:** "A hardcoded secret in a test file is in git history forever. It's on every developer's laptop. It's in CI logs. Treat test code with the same security scrutiny as production code — the git repository doesn't distinguish between `main.py` and `test_main.py` when it stores your secrets."

2. **False Positives Need Documentation, Not Deletion:** "Don't delete false positives from your scan results. Document WHY it's a false positive, suppress it with that justification, and review suppressions quarterly. The audit trail proves you reviewed the finding — deletion just means it comes back next scan."

3. **Rotate First, Investigate Later:** "When a SAST tool finds a real secret in code, the clock is ticking. Rotate the secret immediately — don't wait for the code fix. The secret is compromised the moment it was committed. Cleanup can happen after the secret is no longer valid."
