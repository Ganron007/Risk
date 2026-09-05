# R-EX-085 — Static vs dynamic application security testing (SAST/DAST)

**CISSP Reference:** Chapter 20, Section "Testing Software"; Chapter 15, Section "Testing Software"  
**Exam Objective:** 8.2.1 Understand application vulnerabilities; 8.2.2 Test software security  
**Study Guide Key Terms:** SAST (Static), DAST (Dynamic), IAST (Interactive), RASP, white-box testing, black-box testing, false positive rate  

---

## Scenario Context

After the SQL injection and XSS findings in the client portal pentest, Cadre Corp is evaluating application security testing tools. Two vendors have proposed:

- **Vendor A (SAST):** Analyzes source code without running the application. "Finds vulnerabilities during development, before the app is even built. Integrates with your IDE."
- **Vendor B (DAST):** Tests the running application from the outside. "Finds vulnerabilities the way attackers do — by probing running endpoints. No source code access needed."

The CISO asks: "Which one do we buy?" The answer is both — but for different purposes.

---

## Multiple-Choice Questions

**Question 1:** SAST (Static Application Security Testing) is BEST suited for finding:

A. Runtime configuration issues like missing HTTP security headers  
B. Code-level vulnerabilities — SQL injection, XSS, hardcoded credentials, insecure cryptography — by analyzing source code without executing it  
C. Network-level vulnerabilities like open ports  
D. Authentication bypass in a running application

**Question 2:** DAST (Dynamic Application Security Testing) is BEST suited for finding:

A. Code syntax errors that prevent compilation  
B. Runtime vulnerabilities — authentication bypass, session management flaws, server misconfigurations, information leakage — by testing the running application from an attacker's perspective  
C. Variables that are declared but never used  
D. Code style violations

**Question 3:** Why does Cadre Corp need BOTH SAST and DAST?

A. Vendor contracts require purchasing both  
B. SAST finds code-level issues during development (shift-left, fast feedback); DAST finds runtime and configuration issues that only manifest when the application is running — they find different classes of vulnerabilities at different stages of the SDLC  
C. DAST replaces the need for penetration testing  
D. SAST is for compliance; DAST is for security

---

## Answer Explanations

**Answer 1: B**  
**SAST analyzes source code, bytecode, or binary without execution** (white-box). It traces data flow from user input to dangerous functions: `userInput` → concatenated into SQL string → `executeQuery()` = SQL injection. It finds vulnerabilities in the code itself — injection, XSS, hardcoded secrets, weak crypto — not runtime behavior. Its primary disadvantage: false positives (the code path may never be reachable at runtime).

**Answer 2: B**  
**DAST tests the running application from the outside** (black-box). It sends malicious payloads to endpoints and observes responses: send `' OR '1'='1` to login → gets session token = authentication bypass. It finds vulnerabilities that exist at runtime: auth flaws, session issues, server misconfigurations, information leakage. Its primary disadvantage: it can only test exposed endpoints; unreachable code is invisible.

**Answer 3: B**  
**SAST + DAST = complementary coverage**. SAST finds: "you concatenated user input into a SQL query on line 247." DAST finds: "the login endpoint accepts `' OR '1'='1` and returns a valid session." They find different things at different times. SAST runs during development; DAST runs against deployed/staging environments. Together, they provide broader coverage than either alone.

---

## Cadre Corp Application

1. **SAST in CI/CD:** Integrate a SAST tool (Semgrep, SonarQube, or Bandit for Python) into the CI pipeline. Runs on every commit. Findings classified as critical/high block the merge. This catches injection, XSS, and hardcoded secrets before they leave the developer's machine.

2. **DAST in Staging:** Run DAST (OWASP ZAP or Burp Suite Enterprise) against the staging deployment of the client portal before each release. This catches runtime auth bypass, missing security headers, and server misconfigurations.

3. **IAST (Interactive) as Future Target:** IAST combines SAST and DAST — an agent inside the running application observes data flow during DAST testing, providing SAST-level detail with DAST-level runtime context. Best of both worlds; evaluate for future pipeline integration.

---

## Interview Talking Points

1. **SAST Sees the Code; DAST Sees the Behavior:** "SAST tells you there's a SQL injection pattern on line 247. DAST tells you someone can actually exploit it. You need both: SAST for coverage, DAST for confirmation. SAST during coding, DAST before release. Different tools, different stages, complementary coverage."

2. **SAST False Positives Are a Developer Experience Problem:** "A SAST tool that cries wolf on every commit gets ignored. Tune it. Suppress known false positives. Make critical findings block the build; let warnings be informational. Security tools must earn developers' trust."
