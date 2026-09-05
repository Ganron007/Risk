# R-EX-048 — Database security in the SDLC

**CISSP Reference:** Chapter 20, Section "Databases and Data Warehousing", Pages 1430–1460  
**Exam Objective:** 8.1.1 Implement secure coding practices; 8.2.1 Understand application vulnerabilities  
**Study Guide Key Terms:** Database security, SQL injection, parameterized queries, least privilege database accounts, encryption at rest, column-level encryption, database activity monitoring, data warehousing security  
**Inputs:** Cadre Corp infrastructure (MSSQL on mbr01/mbr02/linux01), `09-sql-wsus-verify.yml`

---

## Scenario Context

Cadre Corp's lab infrastructure includes three SQL Server instances:

- **mbr01 (AST-004):** SQL Server 2025 Developer Edition hosting the client portal database, containing forensic case metadata and client contact information.
- **mbr02 (AST-005):** SQL Server + WSUS + SCCM, hosting the SCCM site database with service account credentials and deployment configurations.
- **linux01 (AST-006):** MSSQL on Linux, hosting lab inventory and research data.

During the campaign exercise (Phase 3), the attacker exploited a chain of database weaknesses:

1. Connected to mbr01's SQL Server as `analyst_t1` (a low-privilege login).
2. Used `IMPERSONATE` permission (granted during troubleshooting) to escalate to `sa`.
3. Enabled `xp_cmdshell` and executed OS commands as `NT AUTHORITY\SYSTEM`.
4. Extracted service account credentials from the SCCM database on mbr02 using linked server connections.

The CISO observed: "We spent weeks hardening AD, but our databases were wide open. The SQL Server was the easiest path to SYSTEM."

---

## Multiple-Choice Questions

**Question 1:** The `IMPERSONATE` permission granted to `analyst_t1` on the `sa` login violates which database security principle?

A. Encryption at rest for sensitive columns  
B. Least privilege — a low-privilege application login should never have the ability to impersonate the database system administrator  
C. Database backup encryption  
D. Connection string encryption in application configuration

**Question 2:** `xp_cmdshell` is a SQL Server extended stored procedure that:

A. Provides database encryption capabilities  
B. Executes arbitrary operating system commands in the context of the SQL Server service account — if that account runs as `SYSTEM` (as it did on mbr01), `xp_cmdshell` is a direct path to full OS compromise  
C. Provides high-availability database clustering  
D. Encrypts network connections between SQL Server and clients

**Question 3:** Parameterized queries prevent SQL injection by:

A. Encrypting the SQL query before sending it to the database  
B. Separating SQL code structure from user-supplied data — the query structure is pre-compiled with placeholders, and user input is bound as data parameters that can never be interpreted as SQL code  
C. Requiring all database users to authenticate with MFA  
D. Running all queries through a web application firewall

**Question 4:** Which of the following is the most effective defense against the linked server attack that allowed lateral movement from mbr01 to mbr02?

A. Using stronger passwords for linked server connections  
B. Disabling linked servers entirely unless explicitly needed, and configuring those that remain with a low-privilege dedicated security context (not `sa` or the current security context) restricted to specific databases and operations  
C. Encrypting all linked server traffic with TLS  
D. Running weekly vulnerability scans against linked servers

---

## Answer Explanations

**Answer 1: B**  
The `IMPERSONATE` permission grants one database principal the ability to assume the identity and privileges of another. Granting a low-privilege login the ability to impersonate `sa` is a direct **least privilege violation** — `analyst_t1` doesn't need `sa` privileges, and certainly shouldn't have a direct path to obtain them. The correct design: application logins have only the minimum permissions needed (SELECT/INSERT/UPDATE on specific tables, EXECUTE on specific stored procedures), never `IMPERSONATE` on privileged accounts.

**Answer 2: B**  
**`xp_cmdshell` executes OS commands** in the security context of the SQL Server service account. If that account is `LocalSystem` or a domain admin, `xp_cmdshell` is a full OS compromise vector. It's disabled by default in modern SQL Server versions for this reason. Cadre Corp's campaign exercise enabled it as part of the attack path — in production, it should remain disabled unless a specific, documented, audited business requirement exists, and even then, the SQL Server service account should be a low-privilege local account.

**Answer 3: B**  
**Parameterized queries (prepared statements)** are the definitive SQL injection defense. Example: instead of `"SELECT * FROM users WHERE name = '" + userInput + "'"` (concatenation — injectable), use `"SELECT * FROM users WHERE name = @name"` with `@name` bound to the user's input as a data parameter. The database engine compiles the query structure first, then plugs in data values — data can never become code. This is a coding practice, not a runtime defense like WAF (D).

**Answer 4: B**  
The most effective defense is **eliminating or restricting linked servers**. Linked servers that use the current security context (`EXECUTE AS LOGIN`) propagate the caller's privileges to the remote server — if the caller has `sa` (via `IMPERSONATE`), the remote connection also has `sa`. Mitigations: (a) remove unnecessary linked servers, (b) configure remaining linked servers with a dedicated low-privilege security context mapped to specific operations, (c) restrict linked server access to specific stored procedures rather than ad-hoc queries. TLS encryption (C) protects data in transit but doesn't prevent privilege escalation through the linked server.

---

## Cadre Corp Application

1. **SQL Server Hardening Playbook:** Based on the campaign findings, create a SQL Server security baseline for all lab instances: (a) `xp_cmdshell` disabled, (b) `IMPERSONATE` permissions revoked from non-administrative logins, (c) `sa` account disabled (use Windows Authentication with named admin accounts), (d) linked servers removed or restricted to specific low-privilege security contexts, (e) SQL Audit enabled for privileged operations.

2. **Least Privilege Database Roles:** For the client portal: (a) application login has SELECT/INSERT/UPDATE on application tables only — no DDL, no system procedures, (b) admin operations use separate named admin accounts (not `sa`), (c) all schema changes go through a change management process, not ad-hoc `ALTER TABLE` by developers.

3. **Database Activity Monitoring:** Enable SQL Server Audit to log: `IMPERSONATE` usage, `xp_cmdshell` enable/disable events, linked server logins, schema changes, and privileged user logins. Feed these to Elastic for correlation with campaign attack telemetry.

4. **Connection String Security:** Store database connection strings in Ansible vault (encrypted), not in application config files or environment variables visible in process listings. Use Windows Authentication (integrated security) where possible instead of SQL authentication with embedded passwords.

---

## Interview Talking Points

1. **Databases Are the Forgotten Crown Jewels:** "We harden AD, we segment networks, we deploy EDR — and then we leave `xp_cmdshell` enabled and `IMPERSONATE` grants lying around from troubleshooting sessions. The database is where the data lives. It deserves the same security rigor as the domain controller."

2. **Linked Servers Are Trust Relationships You Forgot About:** "Every linked server is a trust relationship between database instances. If you can escalate to `sa` on one, and linked servers propagate your security context, you've just moved laterally without touching the network. Audit linked servers as carefully as domain trusts."

3. **Parameterized Queries Are Not Optional:** "In 2026, finding SQL injection in production code is not a vulnerability disclosure — it's a development process failure. Parameterized queries have been the standard defense for over 20 years. Every developer on your team should use them by default, not as an afterthought."
