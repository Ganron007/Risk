# R-EX-016 — Asset classification

**CISSP Reference:** Chapter 5, Sections "Identifying and Classifying Information and Assets", "Establishing Information and Asset Handling Requirements", Pages 383–410  
**Exam Objective:** 2.1.1 Identify and classify information and assets; 2.1.2 Establish information and asset handling requirements  
**Study Guide Key Terms:** Asset classification, classification scheme, Restricted/Confidential/Internal, classification labeling, data owner, classification downgrade  
**Inputs:** [`config/asset-inventory.csv`](../../config/asset-inventory.csv), [`../enterprise-context.md`](../enterprise-context.md)

---

## Scenario Context

Cadre Corp maintains a three-tier classification scheme: **Restricted** (client legal / PKI / identity plane — breach is existential), **Confidential** (business ops / telemetry / member servers), and **Internal** (lab / workstation / deploy tooling). The asset inventory (`config/asset-inventory.csv`) classifies 35 assets across this scheme.

However, during a quarterly risk review, the CISO discovered three classification inconsistencies:

1. **AST-007 (ws01)** is classified as Internal — but it's the primary analyst workstation used to access Restricted forensic evidence daily. The SOC manager argues it should be Confidential because "a compromised workstation is a direct path to client data."

2. **AST-035 (DarkAI lab)** is classified as Internal — but it processes synthetic attack prompts that, if leaked, could reveal Cadre Corp's detection methodologies and tool configurations to adversaries. The R&D Lead argues it should be Confidential.

3. **AST-013 (provisioning)** is classified as Internal — but it holds the Ansible vault with credentials for every VM in the estate. The Infra Lead argues it should be Restricted because "if provisioning is compromised, everything is compromised."

The CISO asks you to review these three classification disputes and determine the correct classification based on the scheme's definitions and business impact.

---

## Multiple-Choice Questions

**Question 1:** Based on Cadre Corp's classification scheme, what is the correct classification for AST-007 (ws01)?

A. Restricted — because it can access Restricted evidence  
B. Confidential — because its compromise provides a path to Restricted data, but the workstation itself does not STORE Restricted data; it's a conduit, not a repository  
C. Internal — workstations are always Internal regardless of use  
D. The classification should match whichever data is currently displayed on screen

**Question 2:** AST-035 (DarkAI lab) is currently Internal. Which factor most strongly supports reclassifying it to Confidential?

A. The lab uses Docker containers which are inherently more secure  
B. The lab processes synthetic attack prompts that could reveal detection methodologies and security tool configurations — this is business-sensitive operational data, fitting the Confidential definition  
C. All research labs should be Internal to encourage innovation  
D. The lab is isolated on a separate Docker network

**Question 3:** AST-013 (provisioning) is classified as Internal, but holds the Ansible vault with credentials for the entire estate. What is the correct classification?

A. Internal — provisioning tools are always low-sensitivity  
B. Confidential — it holds business-critical deployment credentials but not client evidence directly  
C. Restricted — compromise of the Ansible vault means compromise of every system in the estate, including Restricted assets; the impact is existential  
D. The classification should follow the most common asset type it provisions

**Question 4:** When proposing a labeling rule for classifying new VMs, which of the following is the most defensible principle?

A. All new VMs default to Internal until proven otherwise  
B. Classification follows business impact, not technical function — if the VM's compromise would expose client evidence (Restricted), business-critical telemetry (Confidential), or only lab functionality (Internal), classify accordingly  
C. Classification follows the subnet — all VMs on 192.168.77.0/24 get the same classification  
D. Classification is determined by the team that requested the VM

---

## Answer Explanations

**Answer 1: B**  
AST-007 should be **Confidential**, not Internal. While the workstation doesn't store Restricted data permanently, its compromise provides a direct access path to Restricted evidence through the analyst's authenticated sessions and cached credentials. The classification scheme defines Confidential as "business ops / telemetry / member servers" — a forensic analyst's primary workstation fits this category because its compromise impacts business operations and provides a conduit to Restricted systems. The SOC manager's argument is valid: elevation from Internal to Confidential is warranted due to the access path, but Restricted would be excessive since the workstation doesn't store client evidence.

**Answer 2: B**  
The strongest reclassification argument is that DarkAI processes **synthetic attack prompts revealing detection methodologies** — this is business-sensitive operational IP, fitting the Confidential definition of "business ops." If leaked to adversaries, they could craft attacks that evade Cadre Corp's detection stack. The Docker isolation (A, D) is a compensating control, not a reason to keep classification low — controls should match classification, not determine it. "All research labs should be Internal" (C) is an arbitrary rule that ignores business impact.

**Answer 3: C**  
AST-013 should be **Restricted**. The Ansible vault contains credentials for domain controllers, evidence stores, and all infrastructure. Compromise of provisioning means mass configuration change capability across the entire estate — including Restricted assets. This meets the Restricted definition: "breach is existential." The Infra Lead's argument is correct. Classifying provisioning as Internal because it's a "deployment tool" ignores that it holds the keys to the kingdom.

**Answer 4: B**  
**Classification follows business impact**, not technical convenience. A VM that processes client evidence is Restricted regardless of which subnet it's on or which team requested it. Subnet-based classification (C) fails when multiple classification levels share a subnet (as Cadre Corp's flat network currently does). Default-to-Internal (A) guarantees under-classification of new critical systems. Team-based classification (D) creates inconsistent results based on team risk awareness.

---

## Cadre Corp Application

1. **Reclassify AST-007 and AST-013 immediately:** Update `config/asset-inventory.csv` to reflect ws01 as Confidential and provisioning as Restricted. This triggers review of: (a) access controls appropriate for the new classification, (b) monitoring coverage for the reclassified assets, (c) risk register entries that reference these assets.

2. **DarkAI Classification Review:** Evaluate whether DarkAI's detection methodology exposure justifies elevation to Confidential. If so, document the justification and update controls accordingly. If not, document why the current Internal classification is appropriate despite the methodology concern.

3. **Classification Decision Tree:** Create a simple decision tree for new assets: (1) Does it hold or process client evidence/PKI/identities? → Restricted. (2) Does it hold or process business-critical ops data/telemetry/configurations? → Confidential. (3) Is it a lab/research/workstation with no direct path to higher classifications? → Internal. Apply consistently and document exceptions.

---

## Interview Talking Points

1. **Classification Drives Controls, Not Vice Versa:** "Don't classify something as Internal because you don't want to apply Restricted controls. Apply the controls that match the business impact. If provisioning holds credentials for your entire estate, it's Restricted — and you need Restricted-level controls on it."

2. **Conduit Assets Inherit Risk:** "A workstation that accesses Restricted data daily is not Internal just because it doesn't store the data. It's a conduit, and conduit compromise leads directly to the Restricted asset. Classification must account for access paths, not just storage."

3. **Reclassification Is a Risk Signal:** "When an asset's classification changes, that's a signal to re-evaluate everything: access controls, monitoring, risk register entries, and control mappings. Classification isn't a label — it's the foundation of your control framework."
