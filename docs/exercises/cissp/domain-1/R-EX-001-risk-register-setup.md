# R-EX-001 — Risk register setup

**CISSP Reference:** Chapter 2, Section "Understand and Apply Risk Management Concepts", Pages 171-215  
**Exam Objective:** 1.2.1 Understand and apply risk management concepts  
**Study Guide Key Terms:** Risk identification, asset inventory, risk register, risk assessment, threat modeling  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md), `config/asset-inventory.csv`

---

## Scenario Context

Cadre Corp is a mid-size DFIR services firm with 45 employees managing forensic evidence for 120 enterprise clients. The company operates an on-premises Active Directory estate across two forests (`cadre.local` and `child.cadre.local`) with a bidirectional trust to `range.local`. The estate includes domain controllers, member servers, SOC monitoring infrastructure (Elastic, Velociraptor), cloud resources (Entra ID, Azure), and research labs (DarkAI, RevAI, Praxis).

As the newly appointed Risk Manager, you have been tasked with establishing a comprehensive risk register for the organization. The CEO has emphasized that client evidence compromise is an existential risk for the business, and the board requires visibility into the organization's risk posture. You have access to the asset inventory (`config/asset-inventory.csv`) which classifies assets as Restricted, Confidential, or Internal based on their business impact.

Your first step is to ensure that the most critical assets—those classified as Restricted—are properly identified in the risk register with associated threats. The current baseline risk register (`docs/risk-register-baseline.md`) contains 18 risks, but you need to verify coverage of the highest-value assets and identify any gaps.

---

## Multiple-Choice Questions

**Question 1:** According to the Cadre Corp asset inventory, which of the following assets should be classified as Restricted based on the company's risk posture?

A. AST-007 (Analyst workstation ws01)  
B. AST-035 (DarkAI research lab)  
C. AST-030 (Client forensic evidence storage)  
D. AST-013 (Provisioning Ansible server)

**Question 2:** When reviewing the baseline risk register, you notice that AST-034 (ADCS ESC abuse) is documented as RISK-002. Which of the following best describes the primary threat associated with this asset?

A. Unauthorized access to client evidence  
B. Certificate authority compromise leading to credential issuance  
C. SIEM data deletion preventing incident detection  
D. Cloud identity takeover via Entra ID

**Question 3:** You discover that AST-013 (Provisioning Ansible server) is not adequately covered in the current risk register. Which of the following would be the most appropriate new risk entry (RISK-019) for this asset?

A. "Ansible playbook syntax error causing deployment failures"  
B. "Provisioning Ansible vault leak → mass configuration change"  
C. "SSH brute-force attack on provisioning server"  
D. "Insufficient disk space on Ansible server"

**Question 4:** In the context of Cadre Corp's business model, why is AST-030 (Client forensic evidence storage) classified as Restricted rather than Confidential?

A. Because it contains company proprietary information  
B. Because breach would result in loss of client trust and legal liability  
C. Because it is stored on-premises rather than in the cloud  
D. Because it is accessed by more users than other assets

---

## Answer Explanations

**Answer 1: C**  
AST-030 (Client forensic evidence storage) is classified as Restricted because it contains client legal data and forensic evidence. According to the enterprise context, Restricted classification applies to "Client legal / PKI / identity plane — breach is existential." The other options are Internal (AST-007, AST-035) or Confidential (AST-013) based on their business impact.

**Answer 2: B**  
RISK-002 in the baseline register is "ADCS ESC abuse" which relates to AST-034 (ADCS). The primary threat is certificate authority compromise that could lead to unauthorized credential issuance. This is a critical identity plane risk that could allow attackers to issue legitimate certificates for domain accounts.

**Answer 3: B**  
"Provisioning Ansible vault leak → mass configuration change" is the most appropriate risk entry because it addresses the core security concern: if the Ansible vault containing secrets is compromised, an attacker could make unauthorized mass configuration changes across the estate. The other options are either operational issues (A, D) or generic threats (C) that don't capture the specific risk of vault compromise.

**Answer 4: B**  
AST-030 is Restricted because breach would result in loss of client trust and legal liability. Cadre Corp's business model is built on trust—clients hand over disks, memory, and privileged data. A single chain-of-custody or evidence-breach event threatens retainers and SOC 2 attestation. This makes it an existential risk, justifying the Restricted classification.

---

## Cadre Corp Application

This exercise directly applies to the Cadre Corp lab environment by:

1. **Asset-Driven Risk Identification:** Using the actual asset inventory (`config/asset-inventory.csv`) to identify Restricted assets that require the highest level of protection
2. **Register Validation:** Cross-referencing the baseline risk register to ensure critical assets have corresponding risk entries
3. **Gap Analysis:** Identifying assets like AST-013 that may be under-covered and proposing new risk entries
4. **Business Context:** Understanding how Cadre Corp's DFIR business model drives risk classification (client evidence = existential risk)

**Lab Connection:** After completing this exercise, you can verify your understanding by:
- Opening `config/asset-inventory.csv` and filtering for Restricted assets
- Reviewing `docs/risk-register-baseline.md` to confirm coverage
- Running `python -m src.board_report --samples samples/findings/ --out artifacts/board-memo.md` to see how risks feed into executive reporting

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Risk-Based Prioritization:** "I prioritize risk identification by starting with Restricted assets—those where breach would have existential business impact. For Cadre Corp, this means client evidence and identity systems take precedence over research labs."

2. **Asset-Risk Linkage:** "A risk register is only valuable when each risk can be traced to specific assets. I maintain a living asset inventory and ensure every critical asset has corresponding risk entries with clear threat scenarios."

3. **Gap Analysis Process:** "Regular gap analysis is essential. I review the risk register quarterly to identify under-covered assets, especially as new systems are deployed or business requirements change."

4. **Business Context Integration:** "Risk classification must reflect business reality, not just technical severity. For a DFIR firm, client evidence compromise is existential regardless of the technical exploit used."

5. **Executive Communication:** "I translate technical risks into business language for the board. Instead of discussing 'ADCS ESC abuse,' I present 'Certificate authority compromise risk that could allow unauthorized credential issuance across the estate.'"

---

## Task

1. List five Restricted assets and one plausible threat to each.
2. Confirm each appears (or should appear) in the baseline register.
3. Propose one new RISK-019 for an asset currently under-covered.

## Answer key

1. Examples: AST-001 (DCSync), AST-034 (ADCS ESC), AST-030 (evidence theft), AST-010 (SIEM wipe), AST-020 (Entra admin takeover).
2. RISK-001, 002, 007, 009, 011 cover those themes.
3. Example RISK-019: "Provisioning Ansible vault leak → mass config change" on AST-013 — High if secrets unprotected.

**Pass criteria:** You can defend asset→threat→register linkage without inventing hosts outside the inventory.
