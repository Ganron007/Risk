# R-EX-086 — Software composition analysis (SCA)

**CISSP Reference:** Chapter 21, Section "Application Attacks"; Chapter 20, Section "Systems Development Controls"  
**Exam Objective:** 8.2.3 Manage software supply chain; 8.1.1 Implement secure coding  
**Study Guide Key Terms:** SCA, SBOM, dependency scanning, known vulnerabilities, open-source risk, transitive dependencies, license compliance  

---

## Scenario Context

Cadre Corp's applications rely heavily on open-source libraries:

- **DFIR-Nexus:** 45 Python dependencies (FastMCP, ChromaDB, Typer, Velociraptor SDK, etc.)
- **Client Portal:** React frontend with 200+ npm packages; Express.js backend with 80+ npm packages
- **Ansible Playbooks:** Community collections and roles from Ansible Galaxy

During a routine review, the SOC Lead ran `pip-audit` on DFIR-Nexus and discovered a critical vulnerability (CVSS 9.8) in a transitive dependency — a library 4 levels deep that nobody knew was there. The vulnerability allowed remote code execution and had been publicly known for 6 months.

---

## Multiple-Choice Questions

**Question 1:** Software Composition Analysis (SCA) primarily addresses:

A. Code quality and style issues in custom code  
B. Identifying and managing risks in third-party and open-source components — known vulnerabilities, license compliance issues, and outdated dependencies — that make up 70-90% of modern applications  
C. Network vulnerability scanning  
D. Database performance optimization

**Question 2:** An SBOM (Software Bill of Materials) is:

A. A bill for software licensing costs  
B. A machine-readable inventory of ALL components, libraries, and dependencies in an application — enabling rapid identification of affected systems when a new vulnerability (like Log4Shell) is disclosed  
C. A list of software features requested by users  
D. A software development methodology

**Question 3:** A transitive dependency vulnerability (vulnerability in a library 4 levels deep) is dangerous because:

A. It affects more users than direct dependencies  
B. It's invisible to developers — they didn't intentionally include it, may not know it exists, and won't patch it unless SCA tooling surfaces it  
C. Transitive dependencies are always more critical than direct ones  
D. It requires rewriting the entire application

---

## Answer Explanations

**Answer 1: B**  
**SCA manages third-party/open-source risk**. Modern applications are 70-90% open-source code. SCA tools inventory all dependencies (direct and transitive), check them against vulnerability databases (NVD, OSV, GHSA), flag known vulnerabilities with severity and fix versions, and check licenses for compliance. It's the supply chain security tool for software composition.

**Answer 2: B**  
An **SBOM is a formal inventory of software components**. It lists every library, its version, its dependencies, and its origin. When a Log4Shell-level vulnerability is disclosed, organizations with SBOMs can query "do we have Log4j, any version, anywhere?" and answer in minutes. Organizations without SBOMs spend days or weeks manually searching. SBOMs are increasingly required by regulation (US Executive Order 14028) and customer contracts.

**Answer 3: B**  
**Transitive dependencies are invisible** unless SCA tooling surfaces them. A developer adds library A → A depends on B → B depends on C → C depends on D (vulnerable). The developer only sees A. Without SCA scanning the full dependency tree, the vulnerability in D remains unknown and unpatched indefinitely. This is how the DFIR-Nexus vulnerability went unpatched for 6 months.

---

## Cadre Corp Application

1. **SCA in CI/CD:** Add dependency scanning to the pipeline: `pip-audit` for Python, `npm audit` for Node.js, `ansible-galaxy collection list` validation. Critical vulnerabilities → pipeline blocks. Re-scan at least daily (new CVEs are published constantly, not just when you commit code).

2. **SBOM Generation:** Generate an SBOM (CycloneDX or SPDX format) for each application as a build artifact. Store with the release. When a critical CVE is announced, query SBOMs → identify affected apps → prioritize patching.

3. **Dependency Hygiene:** Regular dependency updates (monthly): review and update outdated packages, remove unused dependencies, pin versions (no floating `latest` tags). This reduces the attack surface and makes vulnerability response faster.

---

## Interview Talking Points

1. **You're 80% Open Source — You Just Don't Know Which 80%:** "Modern apps are mostly other people's code. SCA tells you whose code, which versions, and which versions have known vulnerabilities. Without it, you're flying blind on 80% of your attack surface."

2. **SBOM = 'Am I Affected?' in 5 Minutes:** "When the next Log4Shell drops on a Friday night, the difference between 'we know we're not affected' in 5 minutes and 'we're still searching on Monday' is whether you have SBOMs. That's the business case. It's not hypothetical."
