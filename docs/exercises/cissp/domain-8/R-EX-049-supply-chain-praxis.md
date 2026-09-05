# R-EX-049 — Software supply chain security: threat intel feed risk

**CISSP Reference:** Chapter 21, Sections "Malicious Code and Application Attacks"; Chapter 20, Section "Systems Development Controls"; Chapter 1, Section "Supply Chain Risk Management"  
**Exam Objective:** 8.2.3 Manage software supply chain security; 8.3.1 Understand supply chain risks in security tooling  
**Study Guide Key Terms:** Supply chain security, dependency risk, threat intelligence feed integrity, transitive trust, software bill of materials (SBOM), poisoning attacks, pinned dependencies  
**Inputs:** Praxis threat-intel module, samples/findings/, `CTL-PRAXIS-SCAN`

---

## Scenario Context

Praxis (`praxis scan`) uses a threat intelligence feed (`~/.praxis/threat-intel.json`) sourced from six open-source providers (OSV, GHSA, KEV, EPSS, NVD, Gitleaks) to enrich vulnerability findings. The feed is refreshed via `praxis intel update`, which fetches data from each source, merges it into a unified index, and caches it locally.

The CISO raises a supply-chain concern: "Praxis's detection quality depends on the integrity of these threat intel feeds. If a feed is poisoned — false vulnerability data injected, or critical CVEs omitted — Praxis could miss real vulnerabilities or flag false ones, and we'd trust its output because 'Praxis said so.'"

Three specific scenarios:

1. **Stale feed:** The intel hasn't been updated in 90 days. New CVEs (including a critical RCE in a library Cadre Corp uses) are not in the feed. Praxis reports "no vulnerabilities found" — false confidence.

2. **Poisoned feed:** An attacker compromises the GHSA feed source and injects false vulnerability data that suppresses real CVEs for packages the attacker wants to target. Praxis reports "no vulnerabilities" for those packages.

3. **Supply chain of the supply chain:** Praxis itself depends on the threat-intel feed, which depends on NVD, which depends on CVE Numbering Authorities (CNAs) — a chain of transitive trust. A compromise anywhere in this chain affects Praxis's output.

---

## Multiple-Choice Questions

**Question 1:** A stale threat intelligence feed (90 days old) creates what PRIMARY risk?

A. No risk — vulnerabilities don't change that quickly  
B. False confidence — Praxis reports "no vulnerabilities found" because it doesn't know about CVEs published in the last 90 days; the software may actually be critically vulnerable, but the scan gives a clean result  
C. The scan runs slower with stale data  
D. Stale feeds only affect compliance reporting, not security

**Question 2:** A poisoned threat intel feed that suppresses real CVEs exploits what vulnerability in the security tooling supply chain?

A. There is no vulnerability — feeds can't be poisoned  
B. Transitive trust — Cadre Corp trusts Praxis, Praxis trusts GHSA, GHSA trusts its data sources; if an attacker compromises any link in this chain, the trust propagates downstream and Praxis's output becomes attacker-influenced without Cadre Corp ever knowing  
C. Only the Praxis binary can be compromised, not the feed  
D. Feed poisoning only affects network-based tools

**Question 3:** What is the most effective control against threat intel feed poisoning?

A. Trust all feed sources equally — they're all reputable  
B. Multi-source diversity with cross-validation — use 6 independent sources; if 5 sources report a CVE and 1 doesn't, flag the discrepancy; don't rely on any single source for critical decisions; additionally, pin feed versions with checksums and monitor for anomalous feed changes (sudden drops in CVE counts, unexpected data patterns)  
C. Disable threat intel entirely — it's too risky  
D. Only use the NVD feed — it's the most secure

**Question 4:** Under what conditions is it acceptable to run Praxis with a stale threat-intel feed?

A. Never — always update before every scan  
B. In air-gapped environments where network access is prohibited, with documented acceptance: "Threat intel last updated [date], [N] days stale. Scan results reflect known vulnerabilities as of that date. Residual risk: vulnerabilities discovered after that date will not be detected. Control: intel will be updated via offline transfer within [timeframe]."  
C. Stale feeds are always acceptable — they still provide value  
D. Only in development environments, never in CI/CD

---

## Answer Explanations

**Answer 1: B**  
A stale feed creates **false confidence** — the most dangerous kind of security finding. "No vulnerabilities found" means either: (a) there truly are no known vulnerabilities (rare), or (b) the tool doesn't know about recently published vulnerabilities (common with stale intel). The user sees a clean scan and assumes safety, when the software may be critically vulnerable to a CVE published last week. Staleness metadata (last update date, feed age) must be presented alongside scan results so the consumer can assess confidence.

**Answer 2: B**  
**Transitive trust** is the vulnerability. The chain: Cadre Corp trusts Praxis's output → Praxis trusts its threat-intel index → the index trusts GHSA → GHSA trusts its data pipeline. An attacker who compromises GHSA's data pipeline can influence what vulnerabilities Praxis reports (or doesn't report) — and Cadre Corp won't detect this because every link in the chain appears to be functioning normally. This is the same class of attack as poisoning an npm package's dependency — the end consumer trusts the entire chain implicitly.

**Answer 3: B**  
**Multi-source diversity with cross-validation** reduces reliance on any single source. If NVD, OSV, and GHSA all report CVE-2024-XXXX with CVSS 9.8, and one source is "missing" it, the discrepancy is a detection signal — not a reason to trust the outlier. Also: (a) pin feed versions with checksums (detect tampering), (b) monitor feed health metrics (CVE counts, update frequency — sudden drops indicate potential compromise or outage), (c) maintain a local cache of the last-known-good feed for comparison.

**Answer 4: B**  
Stale feeds are acceptable **only with documented risk acceptance** in constrained environments. Air-gapped systems can't update live — the intel must be transferred offline. The acceptance documents: (a) how stale the feed is, (b) what the user should and should NOT rely on (known vulnerabilities as of the feed date, NOT a guarantee of no vulnerabilities since), (c) compensating controls (offline update schedule, manual vulnerability monitoring for critical systems in the interim). Never (A) is impractical. Always acceptable (C) is dangerous.

---

## Cadre Corp Application

1. **Feed Freshness Policy:** Praxis scans must include feed metadata (last update date, feed age) in the output. If the feed is >7 days stale in CI/CD, the scan warns. If >30 days stale, the scan fails with an explicit message: "Threat intel is [N] days stale. Results may not reflect recently disclosed vulnerabilities."

2. **Cross-Validation Monitoring:** Monitor feed health: CVE counts per source, update frequency, and data schema consistency. Flag anomalies: a source that drops from 100 new CVEs/week to 0 may be compromised or malfunctioning.

3. **Offline Acceptance:** For air-gapped demonstrations, document the acceptance conditions explicitly. The board memo should never present stale-intel scan results as "clean" — always qualify with "based on threat intelligence as of [date]."

---

## Interview Talking Points

1. **Your Security Tools Have Supply Chains Too:** "We worry about supply-chain attacks on our software dependencies. But our security TOOLS have dependencies too — threat intel feeds, signature databases, detection rules. If someone poisons the GHSA feed, Praxis gives us false confidence. The supply chain of your security tooling is part of your supply chain risk."

2. **A Clean Scan With Stale Intel Is Worse Than a Dirty Scan:** "When Praxis says '0 vulnerabilities' with 90-day-old intel, that's not a clean bill of health — it's a measurement gap. The scan didn't find vulnerabilities because it didn't KNOW about them. Always check the feed date before you trust the results."
