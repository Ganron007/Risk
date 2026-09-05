# CADRE-Risk — Exercise Map

> **Navigate 122 exercises across CISSP domains and GRC platforms.**  
> Use this map to find exercises by topic, domain, platform, campaign phase, or interview scenario.  
> **Last updated:** 2026-07-27

---

## Quick Stats

| Track | Location | Count | Purpose |
|-------|----------|-------|---------|
| **CISSP Core** | `cissp/domain-{1..8}/` | 87 | CISSP exam + Business Risk Leadership interview prep |
| **CISO Assistant** | `platform/ciso-assistant/` | 15 | Classic GRC platform hands-on (ISO 27001, SOC 2, NIST CSF, GDPR) |
| **VerifyWise** | `platform/verifywise/` | 15 | AI governance platform hands-on (EU AI Act, ISO 42001, NIST AI RMF) |
| **Cross-Platform** | `platform/cross-platform/` | 5 | Multi-platform integration and unified governance |
| **TOTAL** | | **122** | |

---

## How to Use This Map

- **By CISSP domain:** Jump to [Section 1](#section-1-cissp-domain-exercises) — exercises grouped by the 8 CISSP CBK domains
- **By platform:** Jump to [Section 2](#section-2-grc-platform-exercises) — CISO Assistant, VerifyWise, or cross-platform
- **By topic:** Use the [Quick-Find Index](#quick-find-index) at the bottom
- **By campaign phase:** Use the Campaign Phase column to find exercises that map to specific CADRE campaign phases (Phase 0-8)

Each entry shows: **ID** · **What it covers** · **Campaign Phase** · **What you'll accomplish** · **File path**

---

## Section 1 — CISSP Domain Exercises

### Domain 1 — Security & Risk Management (15 exercises)

> Governance, risk frameworks, compliance, legal, leadership communication

| ID | Covers | Campaign Phase | You'll accomplish | File |
|----|--------|----------------|-------------------|------|
| R-EX-001 | Risk register setup from asset inventory | — | Build a risk register tied to real assets; justify Restricted classification | `cissp/domain-1/R-EX-001-*.md` |
| R-EX-002 | Qualitative risk analysis of DCSync attack | Phase 6 | Score likelihood × impact using the 3×3 matrix; determine treatment | `cissp/domain-1/R-EX-002-*.md` |
| R-EX-003 | Business impact analysis for SIEM outage | — | Define RTO/RPO/MTD for critical SOC infrastructure | `cissp/domain-1/R-EX-003-*.md` |
| R-EX-004 | Quantitative ALE for client evidence breach | — | Calculate SLE, ARO, ALE; justify security spend to the board | `cissp/domain-1/R-EX-004-*.md` |
| R-EX-005 | Risk treatment decisions for DarkAI prompt injection | — | Choose Accept/Mitigate/Transfer/Avoid per risk appetite | `cissp/domain-1/R-EX-005-*.md` |
| R-EX-006 | Multi-framework control mapping (NIST/ISO/SOC 2) | — | Map one control to three frameworks simultaneously | `cissp/domain-1/R-EX-006-*.md` |
| R-EX-007 | Security policy hierarchy development | — | Draft policy → standard → procedure → guideline chain | `cissp/domain-1/R-EX-007-*.md` |
| R-EX-008 | Third-party cloud vendor risk assessment | — | Evaluate vendor SOC 2 reports; identify due diligence gaps | `cissp/domain-1/R-EX-008-*.md` |
| R-EX-009 | Key Risk Indicators for SOC operations | — | Define leading/lagging KRIs; set board notification thresholds | `cissp/domain-1/R-EX-009-*.md` |
| R-EX-010 | Board memo generation from risk register | — | Translate technical findings into executive business language | `cissp/domain-1/R-EX-010-*.md` |
| R-EX-011 | Governance framework selection (NIST CSF vs ISO 27001 vs COBIT) | — | Evaluate and recommend primary governance framework for a DFIR firm | `cissp/domain-1/R-EX-011-*.md` |
| R-EX-012 | Security policy hierarchy design | — | Build policies, standards, procedures aligned to frameworks | `cissp/domain-1/R-EX-012-*.md` |
| R-EX-013 | Social engineering scenario analysis | — | Assess personnel security risks; design awareness training | `cissp/domain-1/R-EX-013-*.md` |
| R-EX-014 | Business continuity strategy selection | — | Evaluate BCP strategies against BIA findings and RTO targets | `cissp/domain-1/R-EX-014-*.md` |
| R-EX-015 | Legal and regulatory requirements analysis | — | Map GDPR, HIPAA, CCPA obligations to Cadre Corp operations | `cissp/domain-1/R-EX-015-*.md` |

### Domain 2 — Asset Security (12 exercises)

> Classification, data lifecycle, privacy, retention, destruction

| ID | Covers | Campaign Phase | You'll accomplish | File |
|----|--------|----------------|-------------------|------|
| R-EX-016 | Asset classification disputes (ws01, DarkAI, provisioning) | — | Justify Restricted/Confidential/Internal per business impact | `cissp/domain-2/R-EX-016-*.md` |
| R-EX-017 | Evidence lifecycle (create→store→use→share→archive→destroy) | — | Map 6-stage lifecycle with controls per stage | `cissp/domain-2/R-EX-017-*.md` |
| R-EX-018 | GDPR data flow for EU client evidence | — | Map processing purposes; define 72h breach clock trigger; cross-border controls | `cissp/domain-2/R-EX-018-*.md` |
| R-EX-019 | Velociraptor artifact retention policy | — | Design tiered retention (hot/warm/destroy); legal hold exceptions | `cissp/domain-2/R-EX-019-*.md` |
| R-EX-020 | Media sanitation and data remanence | — | Apply NIST SP 800-88 Clear/Purge/Destroy to lab VMs | `cissp/domain-2/R-EX-020-*.md` |
| R-EX-021 | Data owner vs data custodian roles | — | Clarify client=owner, Cadre Corp=custodian; avoid role confusion in SOC 2 audit | `cissp/domain-2/R-EX-021-*.md` |
| R-EX-022 | Classification handling procedures | — | Draft tiered handling rules (storage, transmission, printing, disposal) | `cissp/domain-2/R-EX-022-*.md` |
| R-EX-023 | DPIA under GDPR for forensic collection | — | Determine when DPIA required; identify special category data triggers | `cissp/domain-2/R-EX-023-*.md` |
| R-EX-024 | Cross-border data transfer compliance | — | Apply SCCs + TIA for EU→US transfers; assess India and Singapore scenarios | `cissp/domain-2/R-EX-024-*.md` |
| R-EX-025 | Asset inventory accuracy and drift | — | Design event-driven inventory updates; prevent un-inventoried asset risk | `cissp/domain-2/R-EX-025-*.md` |
| R-EX-027 | Cloud asset classification challenges | — | Classify Azure Blob, Entra ID, Log Analytics under shared responsibility | `cissp/domain-2/R-EX-027-*.md` |
| R-EX-043 | Data minimization principles | — | Apply GDPR Art. 5(1)(c) to forensic collection; design targeted collection | `cissp/domain-2/R-EX-043-*.md` |

### Domain 3 — Security Architecture (8 exercises)

> Cryptography, PKI, trust models, zero trust, AI architecture

| ID | Covers | Campaign Phase | You'll accomplish | File |
|----|--------|----------------|-------------------|------|
| R-EX-026 | Forest trust boundaries and risk | Phase 2/3 | Analyze cross-forest trust blast radius; enable SID filtering and selective auth | `cissp/domain-3/R-EX-026-*.md` |
| R-EX-028 | ADCS as architectural design weakness | Phase 2 | Frame ESC1 as design flaw (not patch issue); apply compensating controls | `cissp/domain-3/R-EX-028-*.md` |
| R-EX-029 | Symmetric vs asymmetric encryption use cases | — | Design hybrid crypto for forensic evidence delivery (AES + ECC/RSA) | `cissp/domain-3/R-EX-029-*.md` |
| R-EX-030 | Hash functions and digital signatures | — | Replace MD5 with SHA-256; implement signature-based non-repudiation for reports | `cissp/domain-3/R-EX-030-*.md` |
| R-EX-032 | Zero trust architecture principles | Phase 3 | Design micro-segmentation; implement NAC; eliminate "trusted internal network" | `cissp/domain-3/R-EX-032-*.md` |
| R-EX-033 | Secure network segmentation design | Phase 3 | Segment lab into Restricted/Confidential/Internal zones; reduce blast radius | `cissp/domain-3/R-EX-033-*.md` |
| R-EX-041 | Key management lifecycle | — | Design generation→storage→distribution→rotation→revocation→destruction for CA keys, vault, PGP | `cissp/domain-3/R-EX-041-*.md` |
| R-EX-042 | AI system security architecture | — | Apply OWASP LLM Top 10; design HITL gates and model isolation | `cissp/domain-3/R-EX-042-*.md` |

### Domain 4 — Network Security (10 exercises)

> OSI model, DMZ/VLAN, firewalls, VPN, wireless, SDN, NAC, DNS/DHCP, load balancing, monitoring

| ID | Covers | Campaign Phase | You'll accomplish | File |
|----|--------|----------------|-------------------|------|
| R-EX-051 | OSI model security per layer | — | Map attacks and controls to Layers 1-7; demonstrate defense-in-depth | `cissp/domain-4/R-EX-051-*.md` |
| R-EX-052 | DMZ, VLAN, and subnet architecture | — | Design screened subnet for client portal; apply least-privilege networking | `cissp/domain-4/R-EX-052-*.md` |
| R-EX-053 | Firewall rule design and review | — | Replace "allow all" with least-privilege rules; define rule review cadence | `cissp/domain-4/R-EX-053-*.md` |
| R-EX-054 | VPN security (IPsec vs SSL/TLS vs WireGuard) | — | Compare VPN technologies; disable split tunneling; deploy WireGuard | `cissp/domain-4/R-EX-054-*.md` |
| R-EX-055 | Wireless security (WPA3 Enterprise vs Personal) | — | Deploy WPA3-Enterprise with EAP-TLS; eliminate shared PSK | `cissp/domain-4/R-EX-055-*.md` |
| R-EX-056 | SDN security and micro-segmentation | — | Separate control/data planes; apply policy-as-code via Ansible | `cissp/domain-4/R-EX-056-*.md` |
| R-EX-057 | Network Access Control (NAC) | — | Deploy 802.1X with RADIUS; quarantine unknown devices; isolate evidence VMs | `cissp/domain-4/R-EX-057-*.md` |
| R-EX-058 | Secure DNS and DHCP | — | Enable DNSSEC; deploy DHCP snooping; detect DNS tunneling | `cissp/domain-4/R-EX-058-*.md` |
| R-EX-059 | Load balancer security and TLS termination | — | Evaluate TLS termination vs pass-through; deploy re-encryption | `cissp/domain-4/R-EX-059-*.md` |
| R-EX-060 | Network monitoring and anomaly detection | Phase 3 | Correlate Suricata + Zeek + SiLK; close detection gaps | `cissp/domain-4/R-EX-060-*.md` |

### Domain 5 — Identity & Access Management (8 exercises)

> Authentication, authorization, identity lifecycle, PAM, SSO, federation, AD, cloud IAM, IGA

| ID | Covers | Campaign Phase | You'll accomplish | File |
|----|--------|----------------|-------------------|------|
| R-EX-061 | Authentication factors (MFA, biometrics, FIDO2) | — | Compare Type 1/2/3 factors; deploy phishing-resistant MFA for privileged accounts | `cissp/domain-5/R-EX-061-*.md` |
| R-EX-062 | Authorization models (RBAC, ABAC, MAC, DAC) | — | Compare models; implement RBAC for 45-employee DFIR firm | `cissp/domain-5/R-EX-062-*.md` |
| R-EX-063 | Identity lifecycle (joiner-mover-leaver) | — | Automate provisioning/deprovisioning; eliminate dormant accounts | `cissp/domain-5/R-EX-063-*.md` |
| R-EX-064 | Privileged Access Management (PAM) | — | Implement JIT access; eliminate shared DA accounts; deploy tiered admin model | `cissp/domain-5/R-EX-064-*.md` |
| R-EX-065 | SSO and federation (SAML, OIDC) | — | Deploy AD FS; federate with client Entra ID; configure break-glass accounts | `cissp/domain-5/R-EX-065-*.md` |
| R-EX-066 | Active Directory security | Phase 2 | Enable SID filtering; replace unconstrained delegation; harden service accounts | `cissp/domain-5/R-EX-066-*.md` |
| R-EX-067 | Cloud identity (Azure AD, AWS IAM) | — | Mitigate hybrid escalation path; deploy PIM + Conditional Access | `cissp/domain-5/R-EX-067-*.md` |
| R-EX-068 | Identity governance (IGA) | — | Implement access certification; enforce SoD; conduct role mining | `cissp/domain-5/R-EX-068-*.md` |

### Domain 6 — Assessment & Testing (12 exercises)

> Pentest, vulnerability assessment, audit, continuous monitoring, reporting

| ID | Covers | Campaign Phase | You'll accomplish | File |
|----|--------|----------------|-------------------|------|
| R-EX-031 | Pentest scoping and rules of engagement | — | Define in-scope/out-of-scope; exclude client evidence and hypervisor | `cissp/domain-6/R-EX-031-*.md` |
| R-EX-032 | SARIF findings review and triage | — | Triage SAST output; distinguish real secrets from false positives | `cissp/domain-6/R-EX-032-*.md` |
| R-EX-033 | Telemetry gap analysis (host vs network) | Phase 3 | Map detection gaps when NSM is down; deploy compensating host logging | `cissp/domain-6/R-EX-033-*.md` |
| R-EX-034 | SOC 2 audit preparation | — | Map controls to TSCs; collect operating effectiveness evidence | `cissp/domain-6/R-EX-034-*.md` |
| R-EX-035 | Remediation tracking and Definition of Done | — | Define DoD for risk closure; distinguish detective vs preventative controls | `cissp/domain-6/R-EX-035-*.md` |
| R-EX-069 | Pentest methodologies (PTES, OSSTMM) | — | Compare PTES lifecycle vs OSSTMM metrics; select per engagement type | `cissp/domain-6/R-EX-069-*.md` |
| R-EX-070 | Vulnerability assessment vs penetration testing | — | Contrast VA (breadth) and pentest (depth); design complementary cadence | `cissp/domain-6/R-EX-070-*.md` |
| R-EX-071 | Third-party security assessments | — | Evaluate vendor SOC 2 reports; handle "proprietary security" refusals | `cissp/domain-6/R-EX-071-*.md` |
| R-EX-072 | Security audit planning and execution | — | Organize audit evidence; distinguish qualified vs adverse opinions | `cissp/domain-6/R-EX-072-*.md` |
| R-EX-073 | Continuous monitoring vs periodic assessment | — | Deploy drift detection; implement ISCM per NIST SP 800-137 | `cissp/domain-6/R-EX-073-*.md` |
| R-EX-074 | Report writing and executive summaries | — | Tailor findings to audience (board vs CISO vs SOC); translate CVSS to business risk | `cissp/domain-6/R-EX-074-*.md` |
| R-EX-075 | Test environment isolation and safety | — | Isolate pentest scope from production; implement rollback snapshots | `cissp/domain-6/R-EX-075-*.md` |

### Domain 7 — Security Operations (12 exercises)

> Incident response, BCP/DRP, forensics, SIEM, change management, SOC metrics

| ID | Covers | Campaign Phase | You'll accomplish | File |
|----|--------|----------------|-------------------|------|
| R-EX-036 | Incident classification (DarkAI prompt injection) | — | Assign severity; determine GDPR notification triggers; handle reporting delays | `cissp/domain-7/R-EX-036-*.md` |
| R-EX-037 | IR playbook for credential dumping on mbr01 | Phase 2/3 | Execute NIST 800-61 lifecycle; isolate vs shut down; lessons learned | `cissp/domain-7/R-EX-037-*.md` |
| R-EX-038 | Detection gap analysis (host-only telemetry) | Phase 3 | Assess what's missed without network telemetry; deploy compensating controls | `cissp/domain-7/R-EX-038-*.md` |
| R-EX-039 | Chain of custody checklist | — | Define CoC fields (case ID, hash, custodian, timestamp); dual-verification | `cissp/domain-7/R-EX-039-*.md` |
| R-EX-040 | SIEM disaster recovery (Elastic outage) | — | Define RTO/RPO for SIEM; implement interim monitoring; board notification thresholds | `cissp/domain-7/R-EX-040-*.md` |
| R-EX-076 | Log management and SIEM operations | — | Monitor agent heartbeats; enforce NTP; implement retention policies | `cissp/domain-7/R-EX-076-*.md` |
| R-EX-077 | Change management and configuration control | — | Implement IaC-based change control; prevent Friday 4:55 PM changes | `cissp/domain-7/R-EX-077-*.md` |
| R-EX-078 | IR lifecycle per NIST SP 800-61 | — | Execute Preparation→Detection→Containment→Eradication→Recovery→Lessons | `cissp/domain-7/R-EX-078-*.md` |
| R-EX-079 | Business continuity planning (BCP) | — | Conduct BIA; define RTO/RPO/MTD; evaluate hot/warm/cold site strategies | `cissp/domain-7/R-EX-079-*.md` |
| R-EX-080 | Disaster recovery planning (DRP) | — | Implement 3-2-1 backup rule; test restores quarterly; document DR runbook | `cissp/domain-7/R-EX-080-*.md` |
| R-EX-081 | Forensic evidence collection and preservation | — | Apply order of volatility; use write blockers; maintain court-admissible chain of custody | `cissp/domain-7/R-EX-081-*.md` |
| R-EX-082 | SOC metrics and KPIs | — | Define MTTD, MTTR, dwell time, false positive rate; build SOC dashboard | `cissp/domain-7/R-EX-082-*.md` |

### Domain 8 — Software Development Security (10 exercises)

> SDLC, DevSecOps, SAST/DAST, SCA/SBOM, AI/ML security, database security

| ID | Covers | Campaign Phase | You'll accomplish | File |
|----|--------|----------------|-------------------|------|
| R-EX-046 | Praxis as CI/CD security gate | — | Integrate SAST into pipeline; define fail criteria; document override process | `cissp/domain-8/R-EX-046-*.md` |
| R-EX-047 | Ansible pipeline risk (IaC security) | — | Harden provisioning host; pin and review Galaxy roles; vault secret management | `cissp/domain-8/R-EX-047-*.md` |
| R-EX-048 | Database security in the SDLC | Phase 3 | Disable xp_cmdshell; revoke IMPERSONATE; restrict linked servers; parameterize queries | `cissp/domain-8/R-EX-048-*.md` |
| R-EX-049 | Threat intel feed supply chain risk | — | Assess stale/poisoned feed risk; implement multi-source cross-validation | `cissp/domain-8/R-EX-049-*.md` |
| R-EX-050 | Malware analysis risk assessment | — | Isolate detonation VMs; enforce handling SOP; respond to acceptance violations | `cissp/domain-8/R-EX-050-*.md` |
| R-EX-083 | Secure coding (OWASP Top 10) | — | Prevent SQL injection, XSS, IDOR; implement parameterized queries and output encoding | `cissp/domain-8/R-EX-083-*.md` |
| R-EX-084 | DevSecOps pipeline integration | — | Shift-left security testing; implement fast security gates in CI/CD | `cissp/domain-8/R-EX-084-*.md` |
| R-EX-085 | SAST vs DAST comparison | — | Deploy SAST in CI (code-level) + DAST in staging (runtime); compare coverage | `cissp/domain-8/R-EX-085-*.md` |
| R-EX-086 | Software Composition Analysis (SCA) and SBOM | — | Scan dependencies; generate SBOM; detect transitive vulnerabilities | `cissp/domain-8/R-EX-086-*.md` |
| R-EX-087 | AI/ML system security in SDLC | — | Secure model supply chain; test for prompt injection; HITL for AI outputs | `cissp/domain-8/R-EX-087-*.md` |

---

## Section 2 — GRC Platform Exercises

### CISO Assistant — Classic GRC (15 exercises)

> ISO 27001, SOC 2, NIST CSF, GDPR on a real GRC platform

| ID | Covers | You'll accomplish | File |
|----|--------|-------------------|------|
| CISO-EX-001 | Cold start: bring-up, admin, domain, PAT | Bootstrap a GRC platform from Docker to operational in 20 minutes | `platform/ciso-assistant/CISO-EX-001-*.md` |
| CISO-EX-002 | Risk scenario creation (DCSync, ADCS, evidence breach) | Create and score risks using 5×5 ISO-27005 matrix; seed 18 baseline risks via API | `platform/ciso-assistant/CISO-EX-002-*.md` |
| CISO-EX-003 | Control library mapping | Map 8 Cadre Corp controls to risks and frameworks (ISO/SOC 2/NIST) | `platform/ciso-assistant/CISO-EX-003-*.md` |
| CISO-EX-004 | Framework selection (ISO 27001, SOC 2, NIST CSF) | Load frameworks; create implementation instances; map one control to three frameworks | `platform/ciso-assistant/CISO-EX-004-*.md` |
| CISO-EX-005 | Risk matrix configuration (5×5 ISO-27005) | Map Cadre Corp 3×3 scale to ISO 5×5; define acceptance thresholds | `platform/ciso-assistant/CISO-EX-005-*.md` |
| CISO-EX-006 | Perimeter and domain organization | Group assets into Identity, SOC, and Lab perimeters by classification tier | `platform/ciso-assistant/CISO-EX-006-*.md` |
| CISO-EX-007 | Dashboard navigation and interpretation | Read heatmaps, treatment breakdowns, and perimeter charts; extract board-ready insights | `platform/ciso-assistant/CISO-EX-007-*.md` |
| CISO-EX-008 | Executive report generation | Generate and tailor board reports; cross-reference with Markdown SSoT | `platform/ciso-assistant/CISO-EX-008-*.md` |
| CISO-EX-009 | REST API auth and PAT management | Create, test, rotate PATs; implement least-privilege token strategy | `platform/ciso-assistant/CISO-EX-009-*.md` |
| CISO-EX-010 | REST API risk ingestion automation | Build automated pipeline from security tools → unified findings → CISO API | `platform/ciso-assistant/CISO-EX-010-*.md` |
| CISO-EX-011 | SOC 2 Type II audit preparation | Map controls to TSCs; assess operating effectiveness; generate readiness report | `platform/ciso-assistant/CISO-EX-011-*.md` |
| CISO-EX-012 | ISO 27001 Statement of Applicability | Review 93 Annex A controls; document applicability; justify exclusions | `platform/ciso-assistant/CISO-EX-012-*.md` |
| CISO-EX-013 | NIST CSF implementation tracking | Score maturity tiers (1-4) per function; generate improvement roadmap | `platform/ciso-assistant/CISO-EX-013-*.md` |
| CISO-EX-014 | GDPR compliance assessment | Map Articles 5/30/32/33/35 to controls; simulate regulatory inquiry response | `platform/ciso-assistant/CISO-EX-014-*.md` |
| CISO-EX-015 | Multi-framework risk assessment | Assess once, map to ISO 27001 + SOC 2 + NIST CSF + GDPR simultaneously | `platform/ciso-assistant/CISO-EX-015-*.md` |

### VerifyWise — AI Governance (15 exercises)

> EU AI Act, ISO 42001, NIST AI RMF on a real AI governance platform

| ID | Covers | You'll accomplish | File |
|----|--------|-------------------|------|
| VW-EX-001 | Cold start: bring-up, org creation, user setup | Bootstrap AI governance platform; create Cadre Corp org; configure superadmin/org-admin RBAC | `platform/verifywise/VW-EX-001-*.md` |
| VW-EX-002 | AI use case creation and EU AI Act classification | Register DarkAI, RevAI, Praxis; classify as High/Limited Risk per EU AI Act | `platform/verifywise/VW-EX-002-*.md` |
| VW-EX-003 | AI model inventory management | Register 3 models (DeepSeek, Claude, GPT-4o) with provenance, limitations, HITL gates | `platform/verifywise/VW-EX-003-*.md` |
| VW-EX-004 | EU AI Act risk classification workflow | Apply Prohibited/High/Limited/Minimal tiers; document rationale and required controls | `platform/verifywise/VW-EX-004-*.md` |
| VW-EX-005 | AI risk assessment (prompt injection, supply chain, data poisoning) | Create 3 AI-specific risks for RevAI; score likelihood × severity; document mitigations | `platform/verifywise/VW-EX-005-*.md` |
| VW-EX-006 | ISO 42001 AI Management System mapping | Map Cadre Corp AI controls to ISO 42001 clauses; identify AIMS gaps | `platform/verifywise/VW-EX-006-*.md` |
| VW-EX-007 | NIST AI RMF integration | Map to Govern/Map/Measure/Manage functions; contrast with EU AI Act | `platform/verifywise/VW-EX-007-*.md` |
| VW-EX-008 | AI risk mitigation tracking | Update mitigation status; link evidence; schedule quarterly reviews | `platform/verifywise/VW-EX-008-*.md` |
| VW-EX-009 | AI approval workflow management | Configure dual-approval for classification changes; test governance trail | `platform/verifywise/VW-EX-009-*.md` |
| VW-EX-010 | AI governance dashboard and reporting | Navigate AI heatmaps; generate executive AI risk report | `platform/verifywise/VW-EX-010-*.md` |
| VW-EX-011 | REST API auth and JWT management | Obtain JWT; test CRUD; implement token lifecycle (rotation, least privilege) | `platform/verifywise/VW-EX-011-*.md` |
| VW-EX-012 | REST API project and risk ingestion | Push DarkAI/Praxis findings to VerifyWise via automated pipeline | `platform/verifywise/VW-EX-012-*.md` |
| VW-EX-013 | AI governance reporting for executives | Extract AI metrics; frame for board presentation; export PDF | `platform/verifywise/VW-EX-013-*.md` |
| VW-EX-014 | Multi-project AI risk aggregation | Identify systemic AI risks across DarkAI + RevAI + Praxis | `platform/verifywise/VW-EX-014-*.md` |
| VW-EX-015 | AI system lifecycle management | Track design→deploy→monitor→decommission stages; create decommission procedure | `platform/verifywise/VW-EX-015-*.md` |

### Cross-Platform Integration (5 exercises)

> Unified governance across CISO Assistant + VerifyWise

| ID | Covers | You'll accomplish | File |
|----|--------|-------------------|------|
| INT-EX-001 | Classic GRC + AI governance sync | Map VerifyWise AI risks to CISO Assistant enterprise risks; ensure score consistency | `platform/cross-platform/INT-EX-001-*.md` |
| INT-EX-002 | Multi-framework control mapping (7 frameworks) | Map one control (CTL-HITL) to ISO 27001 + SOC 2 + NIST CSF + GDPR + EU AI Act + ISO 42001 + NIST AI RMF | `platform/cross-platform/INT-EX-002-*.md` |
| INT-EX-003 | Unified risk register consolidation | Merge 18 CISO risks + 6 VerifyWise risks → 21 unique risks; produce single board view | `platform/cross-platform/INT-EX-003-*.md` |
| INT-EX-004 | Audit evidence collection across platforms | Collect SOC 2 + ISO 42001 evidence from both platforms; organize into audit package | `platform/cross-platform/INT-EX-004-*.md` |
| INT-EX-005 | Executive dashboard integration | Define unified KPIs spanning both platforms; build single-pane-of-glass for the board | `platform/cross-platform/INT-EX-005-*.md` |

---

## Quick-Find Index

### By CISSP Topic

| Topic | Exercises |
|-------|-----------|
| **Access reviews / IGA** | R-EX-068 |
| **AD CS / PKI** | R-EX-028, R-EX-041 |
| **AD security / Kerberos** | R-EX-026, R-EX-066 |
| **AI governance** | R-EX-042, R-EX-087, VW-EX-001–015 |
| **ALE / quantitative risk** | R-EX-004 |
| **Asset classification** | R-EX-016, R-EX-022, R-EX-025, R-EX-027 |
| **Audit preparation** | R-EX-034, R-EX-072, CISO-EX-011 |
| **Authentication / MFA** | R-EX-061 |
| **Authorization models** | R-EX-062 |
| **BCP / BIA** | R-EX-003, R-EX-014, R-EX-079 |
| **Board communication** | R-EX-010, R-EX-074, CISO-EX-008, INT-EX-005 |
| **Chain of custody** | R-EX-039, R-EX-081 |
| **Change management** | R-EX-077 |
| **Cloud identity** | R-EX-067 |
| **Continuous monitoring** | R-EX-073 |
| **Cross-border transfers** | R-EX-024 |
| **Cryptography (symmetric/asymmetric)** | R-EX-029, R-EX-030 |
| **Data lifecycle / retention** | R-EX-017, R-EX-019 |
| **Data minimization** | R-EX-043 |
| **Database security** | R-EX-048 |
| **DevSecOps / CI/CD** | R-EX-046, R-EX-084 |
| **Disaster recovery** | R-EX-040, R-EX-080 |
| **DNS / DHCP security** | R-EX-058 |
| **DPIA / privacy** | R-EX-023 |
| **EU AI Act** | VW-EX-002, VW-EX-004 |
| **Firewall rules** | R-EX-053 |
| **Forensic evidence** | R-EX-039, R-EX-081 |
| **Framework mapping** | R-EX-006, R-EX-011, CISO-EX-004, CISO-EX-015, INT-EX-002 |
| **GDPR** | R-EX-018, R-EX-023, R-EX-024, CISO-EX-014 |
| **Governance frameworks** | R-EX-011 |
| **Hash functions / signatures** | R-EX-030 |
| **Incident response** | R-EX-036, R-EX-037, R-EX-078 |
| **ISO 27001** | CISO-EX-012 |
| **ISO 42001** | VW-EX-006 |
| **Key management** | R-EX-041 |
| **Load balancer security** | R-EX-059 |
| **Log management / SIEM** | R-EX-076 |
| **Malware analysis** | R-EX-050 |
| **Media sanitation** | R-EX-020 |
| **NAC** | R-EX-057 |
| **Network monitoring** | R-EX-060 |
| **Network segmentation** | R-EX-033, R-EX-052 |
| **NIST AI RMF** | VW-EX-007 |
| **NIST CSF** | CISO-EX-013 |
| **OSI model** | R-EX-051 |
| **OWASP Top 10** | R-EX-083 |
| **PAM / JIT access** | R-EX-064 |
| **Pentest methodologies** | R-EX-031, R-EX-069 |
| **Policy development** | R-EX-007, R-EX-012 |
| **Remediation tracking** | R-EX-035 |
| **Risk matrix / scoring** | R-EX-002, CISO-EX-005 |
| **Risk register** | R-EX-001 |
| **Risk treatment** | R-EX-005 |
| **RMF / NIST SP 800-37** | CISO-EX-013 |
| **SAST / DAST** | R-EX-032, R-EX-085 |
| **SBOM / SCA** | R-EX-086 |
| **SDLC** | R-EX-046, R-EX-083, R-EX-084 |
| **SDN** | R-EX-056 |
| **SOC 2** | R-EX-034, CISO-EX-011 |
| **SOC metrics / KPIs** | R-EX-009, R-EX-082 |
| **Social engineering** | R-EX-013 |
| **SSO / federation** | R-EX-065 |
| **Supply chain** | R-EX-008, R-EX-049, R-EX-071 |
| **Telemetry / detection gaps** | R-EX-033, R-EX-038 |
| **Third-party risk** | R-EX-008, R-EX-071 |
| **VA vs pentest** | R-EX-070 |
| **VPN** | R-EX-054 |
| **Wireless security** | R-EX-055 |
| **Zero trust** | R-EX-032 |

### By Interview Scenario

| If the interviewer asks about... | Go to... |
|----------------------------------|----------|
| "How do you build a risk register?" | R-EX-001, R-EX-002, CISO-EX-002 |
| "How do you communicate risk to the board?" | R-EX-010, R-EX-074, CISO-EX-008 |
| "Walk me through a SOC 2 audit prep" | R-EX-034, CISO-EX-011, INT-EX-004 |
| "How do you handle a security incident?" | R-EX-036, R-EX-037, R-EX-078 |
| "What's your disaster recovery plan?" | R-EX-040, R-EX-079, R-EX-080 |
| "How do you govern AI systems?" | VW-EX-001–005, R-EX-042, R-EX-087 |
| "Explain zero trust to the board" | R-EX-032 |
| "How do you manage third-party risk?" | R-EX-008, R-EX-071 |
| "What GRC tools have you used?" | CISO-EX-001–015, VW-EX-001–015 |
| "How do you handle cross-border data?" | R-EX-024 |
| "How do you secure Active Directory?" | R-EX-026, R-EX-028, R-EX-066 |
| "What's your IAM strategy?" | R-EX-061–068 |
| "How do you integrate security into DevOps?" | R-EX-046, R-EX-084, R-EX-085 |
| "How do you measure SOC performance?" | R-EX-009, R-EX-082 |
| "How do you handle malware analysis safely?" | R-EX-050 |
| "What's your approach to multi-framework compliance?" | R-EX-006, CISO-EX-015, INT-EX-002 |

---

## Exercise Format Legend

Every exercise follows a consistent structure:

| Section | What it provides |
|---------|-----------------|
| **CISSP Reference** | Chapter, pages, exam objective, key terms |
| **Scenario Context** | Realistic Cadre Corp DFIR firm situation (200-400 words) |
| **Multiple-Choice Questions** | 3-4 questions with plausible distractors |
| **Answer Explanations** | Why each answer is correct/incorrect with CISSP rationale |
| **Cadre Corp Application** | How this maps to the actual lab/risk program |
| **Interview Talking Points** | 3-5 concise, memorable statements for interviews |

---

*Last updated: 2026-07-24 — 122 exercises mapped.*