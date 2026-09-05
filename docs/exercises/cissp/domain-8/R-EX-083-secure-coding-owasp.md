# R-EX-083 — Secure coding practices (OWASP Top 10)

**CISSP Reference:** Chapter 20, Section "Systems Development Controls"; Chapter 21, Section "Application Attacks"  
**Exam Objective:** 8.1.1 Implement secure coding practices; 8.2.1 Understand application vulnerabilities  
**Study Guide Key Terms:** OWASP Top 10, SQL injection, XSS, CSRF, input validation, output encoding, parameterized queries, least privilege  

---

## Scenario Context

Cadre Corp's client threat intelligence portal is being developed by a small internal team (2 developers, no dedicated security reviewer). An external penetration test (see R-EX-069) found:

1. **SQL Injection** in the login form — entering `' OR '1'='1` as the username bypassed authentication entirely.
2. **Stored XSS** in the "case notes" field — an attacker could inject JavaScript that executes in other analysts' browsers when they view the case.
3. **Missing access controls** — changing the `case_id` parameter in the URL allowed any authenticated user to view any case, not just their own.

The CISO asks: "How do we prevent these in the next release, and how do we catch them before the pentesters do?"

---

## Multiple-Choice Questions

**Question 1:** The SQL injection vulnerability would have been prevented by:

A. Using a stronger password policy for the database  
B. Using parameterized queries (prepared statements) — which separate SQL code from user data, making injection impossible regardless of what the user types  
C. Encrypting the database connection with TLS  
D. Using a more complex database schema

**Question 2:** The correct defense against stored XSS in the case notes field is:

A. Telling users not to click suspicious links  
B. Output encoding — when displaying user-submitted content, encode HTML special characters (`<` → `&lt;`) so that any injected JavaScript is displayed as text, not executed as code  
C. Requiring users to log in before viewing cases  
D. Disabling the case notes feature entirely

**Question 3:** The missing access control (IDOR — Insecure Direct Object Reference) was possible because:

A. The application relied on obscuring case IDs instead of enforcing server-side authorization checks — the server never verified "does this user have permission to view case #123?"  
B. The case IDs were too short  
C. The application used HTTPS  
D. Users had weak passwords

---

## Answer Explanations

**Answer 1: B**  
**Parameterized queries** are the definitive defense against SQL injection. Instead of concatenating user input into SQL strings (`"SELECT * FROM users WHERE name = '" + userInput + "'"`), parameterized queries treat user input as data, never as code. No matter what the user types (`' OR '1'='1`), it's treated as a literal string value, not SQL syntax. Input validation is defense-in-depth; parameterization is the primary control.

**Answer 2: B**  
**Output encoding** is the primary XSS defense. When displaying user-submitted data in HTML, characters like `<`, `>`, `"`, `'`, and `&` must be converted to their HTML entity equivalents. This ensures `<script>alert(1)</script>` is displayed as text on the page, not executed as JavaScript. Context-aware encoding (HTML context vs JavaScript context vs URL context) is essential.

**Answer 3: A**  
**IDOR occurs when authorization checks are missing** or rely on client-side obscurity. The server must verify: "The authenticated user requesting case #123 has permission to access case #123." This check must happen server-side (client-side checks can be bypassed). Relying on "the user doesn't know other case IDs" is security through obscurity and fails when IDs are enumerable or guessable.

---

## Cadre Corp Application

1. **OWASP Top 10 Training:** All developers must complete OWASP Top 10 awareness training before committing code to the client portal. Focus on the vulnerabilities found in the pentest: injection, XSS, and broken access control.

2. **Code Review Gate:** Every pull request must pass: (a) automated SAST scan (see R-EX-085), (b) peer review with security checklist (input validation present? parameterized queries used? output encoding applied? authorization checks server-side?).

3. **Praxis as Developer Tool:** Use Praxis (`praxis scan`) in CI to detect secrets, vulnerable patterns, and missing security controls before code reaches production.

---

## Interview Talking Points

1. **SQL Injection in 2026 Is Unacceptable:** "Parameterized queries have been the standard defense for 20+ years. Finding SQL injection in a new application isn't a vulnerability — it's a development process failure. It means nobody reviewed the code for the #1 web vulnerability."

2. **Authorization Must Be Server-Side, Always:** "Never trust the client to enforce access control. The server must verify every request: 'Is this user authorized to access this resource?' If you're relying on hidden URLs or guessable IDs, you don't have access control — you have hope."
