# CISSP Official Study Guide Chapter Mapping to Exercise Plan

> **Source:** CISSP Official Study Guide 10th Edition 2024  
> **Purpose:** Map study guide chapters to domain-specific exercise development  
> **Last updated:** 2026-07-24

---

## Chapter-to-Domain Mapping

| Chapter | Title | Domain | Current Exercises | Target Exercises | Priority |
|---------|-------|--------|-------------------|------------------|----------|
| **1** | Security Governance Through Principles and Policies | 1 | 10 | 15 | HIGH |
| **2** | Personnel Security and Risk Management Concepts | 1 | 10 | 15 | HIGH |
| **3** | Business Continuity Planning | 1/7 | 10 | 15 | HIGH |
| **4** | Laws, Regulations, and Compliance | 1 | 10 | 15 | HIGH |
| **5** | Protecting Security of Assets | 2 | 5 | 12 | HIGH |
| **6** | Cryptography and Symmetric Key Algorithms | 3 | 2 | 8 | MEDIUM |
| **7** | PKI and Cryptographic Applications | 3 | 2 | 8 | MEDIUM |
| **8** | Principles of Security Models, Design, and Capabilities | 3 | 2 | 8 | MEDIUM |
| **9** | Security Vulnerabilities, Threats, and Countermeasures | 3 | 2 | 8 | MEDIUM |
| **10** | Physical Security Requirements | 3 | 2 | 8 | MEDIUM |
| **11** | Secure Network Architecture and Components | 4 | **0** | 10 | HIGH |
| **12** | Secure Communications and Network Attacks | 4 | **0** | 10 | HIGH |
| **13** | Managing Identity and Authentication | 5 | **0** | 8 | HIGH |
| **14** | Controlling and Monitoring Access | 5 | **0** | 8 | HIGH |
| **15** | Security Assessment and Testing | 6 | 5 | 12 | HIGH |
| **16** | Managing Security Operations | 7 | 5 | 12 | HIGH |
| **17** | Preventing and Responding to Incidents | 7 | 5 | 12 | HIGH |
| **18** | Disaster Recovery Planning | 7 | 5 | 12 | HIGH |
| **19** | Investigations and Ethics | 7 | 5 | 12 | HIGH |
| **20** | Software Development Security | 8 | 5 | 10 | HIGH |
| **21** | Malicious Code and Application Attacks | 8 | 5 | 10 | HIGH |

---

## Domain 1 — Security and Risk Management (Chapters 1-4)

**Target:** 15 exercises | **Current:** 10 exercises | **Gap:** 5 exercises

### Chapter 1: Security Governance Through Principles and Policies
**Key Topics:**
- Security concepts (CIA triad, security principles)
- Security boundaries (trusted vs untrusted)
- Security governance principles
- Managing the security function
- Security policy, standards, procedures, guidelines
- Threat modeling
- Supply chain risk management

**Exercise Plan:**
- R-EX-001: Risk register setup (existing - upgrade to full)
- R-EX-011: **NEW** - Security governance framework selection
- R-EX-012: **NEW** - Security policy hierarchy and development

### Chapter 2: Personnel Security and Risk Management Concepts
**Key Topics:**
- Personnel security policies and procedures
- Risk management concepts (quantitative, qualitative)
- Social engineering
- Security awareness, education, and training

**Exercise Plan:**
- R-EX-002: DCSync assessment (existing - upgrade to full)
- R-EX-003: BIA SIEM (existing - upgrade to full)
- R-EX-004: ALE client breach (existing - upgrade to full)
- R-EX-013: **NEW** - Social engineering scenario analysis

### Chapter 3: Business Continuity Planning
**Key Topics:**
- Business continuity planning
- Project scope and planning
- Business impact analysis (BIA)
- Continuity planning strategies
- Plan approval and implementation

**Exercise Plan:**
- R-EX-003: BIA SIEM (existing - covers BIA)
- R-EX-014: **NEW** - Business continuity strategy selection

### Chapter 4: Laws, Regulations, and Compliance
**Key Topics:**
- Categories of laws (criminal, civil, administrative)
- Specific laws (GDPR, HIPAA, FERPA, GLBA, etc.)
- State privacy laws
- Compliance frameworks
- Contracting and procurement

**Exercise Plan:**
- R-EX-006: Framework mapping (existing - upgrade to full)
- R-EX-008: Third-party cloud (existing - upgrade to full)
- R-EX-015: **NEW** - Legal and regulatory requirements analysis

---

## Domain 2 — Asset Security (Chapter 5)

**Target:** 12 exercises | **Current:** 5 exercises | **Gap:** 7 exercises

### Chapter 5: Protecting Security of Assets
**Key Topics:**
- Identifying and classifying information and assets
- Establishing information and asset handling requirements
- Data protection methods
- Understanding data roles (owner, custodian, controller, processor)
- Using security baselines

**Exercise Plan:**
- R-EX-016: Asset classification (existing - upgrade to full)
- R-EX-017: Evidence lifecycle (existing - upgrade to full)
- R-EX-018: GDPR data flow (existing - upgrade to full)
- R-EX-019: VR retention (existing - upgrade to full)
- R-EX-020: Media sanitation (existing - upgrade to full)
- R-EX-021: **NEW** - Data owner vs data custodian roles
- R-EX-022: **NEW** - Data classification handling procedures
- R-EX-023: **NEW** - Privacy impact assessment (DPIA)
- R-EX-024: **NEW** - Cross-border data transfer compliance
- R-EX-025: **NEW** - Asset inventory accuracy and maintenance
- R-EX-026: **NEW** - Data minimization principles
- R-EX-027: **NEW** - Cloud asset classification challenges

---

## Domain 3 — Security Architecture (Chapters 6-10)

**Target:** 8 exercises | **Current:** 2 exercises | **Gap:** 6 exercises

### Chapter 6: Cryptography and Symmetric Key Algorithms
**Key Topics:**
- Cryptographic foundations
- Modern cryptography
- Symmetric cryptography (AES, DES, 3DES, Blowfish)
- Cryptographic life cycle

**Exercise Plan:**
- R-EX-029: **NEW** - Symmetric vs asymmetric encryption use cases
- R-EX-030: **NEW** - Hash functions and digital signatures

### Chapter 7: PKI and Cryptographic Applications
**Key Topics:**
- Asymmetric cryptography (RSA, ECC)
- Hash functions
- Digital signatures
- Public key infrastructure (PKI)
- Asymmetric key management
- Hybrid cryptography
- Applied cryptography
- Cryptographic attacks

**Exercise Plan:**
- R-EX-028: ADCS design flaw (existing - upgrade to full)
- R-EX-031: **NEW** - Key management lifecycle

### Chapter 8: Principles of Security Models, Design, and Capabilities
**Key Topics:**
- Secure design principles
- Techniques for ensuring CIA
- Security models (Bell-LaPadula, Biba, Clark-Wilson, Brewer-Nash)
- Selecting controls based on system security requirements
- Security capabilities of information systems

**Exercise Plan:**
- R-EX-026: Trust model (existing - upgrade to full)
- R-EX-032: **NEW** - Zero trust architecture principles

### Chapter 9: Security Vulnerabilities, Threats, and Countermeasures
**Key Topics:**
- Shared responsibility models
- Data localization and data sovereignty
- Security architecture vulnerabilities
- Various system types (client, server, ICS, distributed, IoT, containers, etc.)
- Essential security protection mechanisms
- Common security architecture flaws

**Exercise Plan:**
- R-EX-033: **NEW** - Secure network segmentation design

### Chapter 10: Physical Security Requirements
**Key Topics:**
- Security principles for site and facility design
- Site and facility security controls
- Physical security management

**Exercise Plan:**
- R-EX-034: **NEW** - Physical security control selection

---

## Domain 4 — Network Security (Chapters 11-12)

**Target:** 10 exercises | **Current:** 0 exercises | **Gap:** 10 exercises

### Chapter 11: Secure Network Architecture and Components
**Key Topics:**
- OSI model
- TCP/IP model
- Network traffic analysis
- Application layer protocols
- Transport layer protocols
- DNS security
- IP networking
- ARP security
- Secure communication protocols
- Network segmentation
- Edge networks
- Wireless networks
- Satellite and cellular communications
- CDNs
- Secure network components

**Exercise Plan:**
- R-EX-051: **NEW** - OSI model security considerations per layer
- R-EX-052: **NEW** - Secure network architecture (DMZ, VLAN, subnetting)
- R-EX-053: **NEW** - Firewall rule design and review
- R-EX-054: **NEW** - VPN security (IPsec vs SSL/TLS)
- R-EX-055: **NEW** - Wireless security (WPA3, enterprise vs personal)
- R-EX-056: **NEW** - Software-defined networking (SDN) security
- R-EX-057: **NEW** - Network access control (NAC) implementation
- R-EX-058: **NEW** - Secure DNS and DHCP configuration

### Chapter 12: Secure Communications and Network Attacks
**Key Topics:**
- Protocol security mechanisms
- Secure voice communications
- Remote access security management
- Multimedia collaboration security
- Network monitoring and management
- Load balancing security
- Email security
- VPN technologies
- Switching and VLANs
- NAT security
- Third-party connectivity
- WAN technologies
- Fiber-optic link security
- Network attack prevention and mitigation

**Exercise Plan:**
- R-EX-059: **NEW** - Load balancer security considerations
- R-EX-060: **NEW** - Network monitoring and anomaly detection

---

## Domain 5 — Identity and Access Management (Chapters 13-14)

**Target:** 8 exercises | **Current:** 0 exercises | **Gap:** 8 exercises

### Chapter 13: Managing Identity and Authentication
**Key Topics:**
- Controlling access to assets
- AAA model (Authentication, Authorization, Accounting)
- Identity management implementation
- Identity and access provisioning life cycle

**Exercise Plan:**
- R-EX-061: **NEW** - Authentication factors (MFA, biometrics, knowledge-based)
- R-EX-062: **NEW** - Authorization models (RBAC, ABAC, MAC, DAC)
- R-EX-063: **NEW** - Identity lifecycle management (provisioning, deprovisioning)
- R-EX-064: **NEW** - Privileged access management (PAM)

### Chapter 14: Controlling and Monitoring Access
**Key Topics:**
- Access control models comparison
- Authentication systems implementation
- Zero-trust access policy enforcement
- Access control attacks

**Exercise Plan:**
- R-EX-065: **NEW** - Single sign-on (SSO) and federation (SAML, OIDC)
- R-EX-066: **NEW** - Active Directory security (domain trusts, delegation)
- R-EX-067: **NEW** - Cloud identity (Azure AD, AWS IAM, GCP IAM)
- R-EX-068: **NEW** - Identity governance and administration (IGA)

---

## Domain 6 — Assessment and Testing (Chapter 15)

**Target:** 12 exercises | **Current:** 5 exercises | **Gap:** 7 exercises

### Chapter 15: Security Assessment and Testing
**Key Topics:**
- Building a security assessment and testing program
- Performing vulnerability assessments
- Testing software
- Training and exercises
- Security management processes and data collection

**Exercise Plan:**
- R-EX-031: Pentest scope (existing - upgrade to full)
- R-EX-032: SARIF review (existing - upgrade to full)
- R-EX-033: Telemetry gap (existing - upgrade to full)
- R-EX-034: SOC 2 audit prep (existing - upgrade to full)
- R-EX-035: Remediation tracking (existing - upgrade to full)
- R-EX-069: **NEW** - Penetration testing methodologies (PTES, OSSTMM)
- R-EX-070: **NEW** - Vulnerability assessment vs penetration testing
- R-EX-071: **NEW** - Third-party security assessments
- R-EX-072: **NEW** - Security audit planning and execution
- R-EX-073: **NEW** - Continuous monitoring vs periodic assessment
- R-EX-074: **NEW** - Report writing and executive summaries
- R-EX-075: **NEW** - Test environment isolation and safety

---

## Domain 7 — Security Operations (Chapters 16-19)

**Target:** 12 exercises | **Current:** 5 exercises | **Gap:** 7 exercises

### Chapter 16: Managing Security Operations
**Key Topics:**
- Foundational security operations concepts
- Personnel safety and security
- Secure provisioning of information and assets
- Resource protection
- Managed services in the cloud
- Configuration management
- Change management
- Patch management and vulnerability reduction

**Exercise Plan:**
- R-EX-038: Detection gap breach (existing - upgrade to full)
- R-EX-040: SIEM DR (existing - upgrade to full)
- R-EX-076: **NEW** - Log management and SIEM operations
- R-EX-077: **NEW** - Change management and configuration control

### Chapter 17: Preventing and Responding to Incidents
**Key Topics:**
- Incident management
- Detection and preventive measures
- Logging and monitoring
- Automating incident response

**Exercise Plan:**
- R-EX-036: Incident classify DarkAI (existing - upgrade to full)
- R-EX-037: IR playbook VR (existing - upgrade to full)
- R-EX-078: **NEW** - Incident response lifecycle (NIST SP 800-61)

### Chapter 18: Disaster Recovery Planning
**Key Topics:**
- Nature of disaster
- System resilience, high availability, and fault tolerance
- Recovery strategies
- Recovery plan development
- Training, awareness, and documentation
- Testing and maintenance

**Exercise Plan:**
- R-EX-040: SIEM DR (existing - covers DR)
- R-EX-079: **NEW** - Business continuity planning (BCP)
- R-EX-080: **NEW** - Disaster recovery planning (DRP)

### Chapter 19: Investigations and Ethics
**Key Topics:**
- Investigations
- Major categories of computer crime
- Ethics

**Exercise Plan:**
- R-EX-039: Chain of custody (existing - upgrade to full)
- R-EX-081: **NEW** - Forensic evidence collection and preservation
- R-EX-082: **NEW** - Security operations center (SOC) metrics and KPIs

---

## Domain 8 — Software Development Security (Chapters 20-21)

**Target:** 10 exercises | **Current:** 5 exercises | **Gap:** 5 exercises

### Chapter 20: Software Development Security
**Key Topics:**
- Systems development controls
- Databases and data warehousing
- Storage threats
- Knowledge-based systems

**Exercise Plan:**
- R-EX-046: SSDLC Praxis (existing - upgrade to full)
- R-EX-047: Ansible pipeline risk (existing - upgrade to full)
- R-EX-083: **NEW** - Secure coding practices (OWASP Top 10)
- R-EX-084: **NEW** - DevSecOps pipeline integration

### Chapter 21: Malicious Code and Application Attacks
**Key Topics:**
- Malware types and prevention
- Application attacks (OWASP, injection, XSS, etc.)

**Exercise Plan:**
- R-EX-049: Supply chain Praxis (existing - upgrade to full)
- R-EX-050: Malware analysis risk (existing - upgrade to full)
- R-EX-085: **NEW** - Static vs dynamic application security testing (SAST/DAST)
- R-EX-086: **NEW** - Software composition analysis (SCA)
- R-EX-087: **NEW** - AI/ML system security in SDLC (Domain 8 + AI governance)

---

## Recommended Implementation Order

Based on CISSP exam weight and interview relevance:

### Phase 1: High-Impact Domains (Weeks 1-4)
1. **Domain 1** (Chapters 1-4) - Foundation for all other domains, highest exam weight (16%)
2. **Domain 7** (Chapters 16-19) - Operations and incident response, critical for interviews
3. **Domain 2** (Chapter 5) - Asset security, fundamental to GRC

### Phase 2: Technical Domains (Weeks 5-7)
4. **Domain 4** (Chapters 11-12) - Network security, completely missing
5. **Domain 5** (Chapters 13-14) - Identity and access, completely missing
6. **Domain 6** (Chapter 15) - Assessment and testing, audit-focused

### Phase 3: Specialized Domains (Week 8)
7. **Domain 8** (Chapters 20-21) - Software development, DevSecOps
8. **Domain 3** (Chapters 6-10) - Cryptography and architecture, lower exam weight

---

## Study Guide Integration Strategy

**For each exercise:**
1. **Reference specific chapter sections** - e.g., "Chapter 1, pages 106-109"
2. **Map to exam objectives** - e.g., "1.1.1 Understand and apply security governance principles"
3. **Include study guide key terms** - Use official terminology from the text
4. **Cross-reference to Cadre Corp context** - Apply concepts to the lab environment
5. **Practice question style** - Match the study guide's question format

**Quality upgrade template:**
```markdown
## Exercise Title
**CISSP Reference:** Chapter X, Section Y, Pages ZZZ-ZZZ  
**Exam Objective:** X.Y.Z [Objective name]  
**Study Guide Key Terms:** [List 3-5 key terms from chapter]

## Scenario Context
[300-400 word scenario based on Cadre Corp context]

## Multiple-Choice Questions
1. [Question with 4 options, A-D]
2. [Question with 4 options, A-D]
3. [Question with 4 options, A-D]

## Answer Explanations
[Detailed explanations for each question, referencing study guide concepts]

## Cadre Corp Application
[How this applies to the specific lab environment]

## Interview Talking Points
[How to discuss this in a Business Risk Leadership interview]
```

---

*Last updated: 2026-07-24*
