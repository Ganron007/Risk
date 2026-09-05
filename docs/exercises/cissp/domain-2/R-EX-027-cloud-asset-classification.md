# R-EX-027 — Cloud asset classification challenges

**CISSP Reference:** Chapter 5, Section "Data Protection Methods", Pages 395–410; Chapter 9, Section "Shared Responsibility Models"  
**Exam Objective:** 2.1.2 Establish information and asset handling requirements; 3.5.1 Understand shared responsibility model  
**Study Guide Key Terms:** Cloud asset classification, shared responsibility model, data residency, cloud storage tiers, IaaS/PaaS/SaaS classification, CASB  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`config/asset-inventory.csv`](../../config/asset-inventory.csv)

---

## Scenario Context

Cadre Corp's migration of three client evidence stores to Azure Blob Storage (see R-EX-025) has surfaced a deeper problem: classifying cloud assets isn't the same as classifying on-premises servers. The IT team applied the same three-tier scheme (Restricted/Confidential/Internal) to the Azure resources, but several edge cases emerged:

1. **Azure Blob Storage containers** holding client evidence: The data is Restricted, but the storage account itself runs on Microsoft-managed infrastructure. Microsoft engineers with privileged access could theoretically access the data. Does the storage account inherit the Restricted classification, or is classification a data-layer concern only?

2. **Entra ID tenant (AST-020):** The identity plane spans both on-prem AD and cloud. If the Entra ID Global Administrator role is compromised, an attacker can reset passwords for on-prem synced accounts. Should Entra ID be classified at the same level as on-prem DCs?

3. **Log Analytics workspaces:** Ingesting Restricted evidence metadata into Azure Log Analytics for threat detection. The metadata isn't evidence, but patterns could reveal client names, investigation types, and timing. Classification?

4. **M365 Defender portal:** Displays alerts that reference client hostnames and file paths extracted from forensic evidence. The portal runs in a browser — is viewing it from a personal device a data spill?

---

## Multiple-Choice Questions

**Question 1:** Under the cloud shared responsibility model, who is responsible for classifying data stored in Azure Blob Storage?

A. Microsoft — they manage the physical infrastructure  
B. Cadre Corp — classification is always a customer responsibility for IaaS/PaaS data  
C. Shared — Microsoft classifies infrastructure, Cadre Corp classifies data and access  
D. The client who owns the data

**Question 2:** When classifying the Entra ID tenant (AST-020), which of the following factors most strongly supports a Restricted classification?

A. Entra ID is a cloud service and cannot be classified higher than Confidential  
B. Compromise of Entra ID Global Administrator enables password reset for synced on-prem accounts, including Domain Admins  
C. Microsoft's SLA guarantees classify Entra ID as Restricted by default  
D. Entra ID stores only email addresses, not sensitive data

**Question 3:** A SOC analyst reviews M365 Defender alerts (showing client hostnames from evidence) on their personal iPad at a coffee shop. This represents:

A. Acceptable use — the iPad has a PIN and the coffee shop Wi-Fi is encrypted  
B. A data spill — Restricted metadata was viewed on an unmanaged device in a public space  
C. A minor policy violation with no data exposure  
D. Normal operations — M365 Defender is designed for mobile access

**Question 4:** Which cloud security control is most effective for preventing misclassification of newly provisioned cloud resources?

A. Annual cloud security posture management (CSPM) review  
B. Automated tagging policies that enforce classification labels at resource creation  
C. Manual review by the cloud security lead before any resource is used  
D. SOC 2 audit findings that identify misclassified resources

---

## Answer Explanations

**Answer 1: C**  
Under the shared responsibility model, **classification is shared but in different layers**: Microsoft classifies and protects the physical infrastructure, hypervisor, and network fabric, while **Cadre Corp is responsible for classifying data, managing access, and configuring tenant-level security**. The client (D) owns the data, but Cadre Corp as the service provider must implement the classification controls. Option B is close but overstates — for SaaS, the provider does more; for IaaS, the customer does more. Blob Storage is PaaS, so the split falls in the middle.

**Answer 2: B**  
The **identity plane bridge** — Entra ID Global Administrator can reset on-premises synced account passwords — is the deciding factor. This creates a transitive escalation path: compromise cloud identity → reset on-prem Domain Admin password → full forest compromise. This makes AST-020 a Restricted asset because its breach has the same existential impact as compromising a DC (AST-001). Classification follows impact, not deployment model.

**Answer 3: B**  
This is a **data spill**. The M365 Defender portal displays Restricted metadata (client hostnames, file paths from forensic evidence) derived from Restricted evidence. Viewing it on an unmanaged personal device in a public space violates: (a) device control policy, (b) physical security (shoulder surfing risk), (c) data handling procedures for Restricted-derived information. The iPad PIN and coffee shop Wi-Fi encryption don't mitigate these risks.

**Answer 4: B**  
**Automated tagging policies at resource creation** are the most effective control. Azure Policy can enforce required tags (classification, owner, data sensitivity) and deny creation of untagged resources. This prevents misclassification at the source rather than detecting it later. Annual reviews (A) and audit findings (D) are detective controls that find problems after they exist. Manual review (C) doesn't scale.

---

## Cadre Corp Application

1. **Azure Policy for Classification Tags:** Deploy an Azure Policy that requires `classification`, `data-owner`, and `sensitivity` tags on all resource groups. Non-compliant resources are denied creation or flagged for review. This directly maps to the CSV inventory schema.

2. **Entra ID as Restricted:** Update `config/asset-inventory.csv` to explicitly list AST-020 (Entra ID) as Restricted with a note: "Identity plane bridge to on-prem AD — compromise impact equals DC compromise." The existing Restricted classification is correct; the justification needs documentation.

3. **M365 Defender Access Policy:** Define acceptable client endpoints for viewing Restricted-derived data in cloud portals. Managed devices only, no public Wi-Fi, screen privacy filters required in public spaces.

4. **Shared Responsibility Documentation:** Add a section to `docs/enterprise-context.md` clarifying Cadre Corp's shared responsibility boundaries for each cloud service in use (Azure IaaS, Entra ID SaaS, M365 Defender SaaS).

---

## Interview Talking Points

1. **Classification Follows Impact, Not Location:** "Whether a system runs in my datacenter or Azure doesn't change its classification. If compromising Entra ID gets you Domain Admin on-prem, Entra ID is Restricted. Period."

2. **Shared Responsibility Is a Risk Boundary:** "Microsoft secures the cloud; I secure what's IN the cloud. Classification, access control, encryption — these are my responsibility regardless of where the servers live. Confusing this is how cloud breaches happen."

3. **Metadata = Data:** "Log Analytics metadata about Restricted evidence IS Restricted-derived. Patterns in metadata reveal clients, cases, and timelines. I classify the derived data at the same level as the source until proven otherwise."

4. **Cloud Portals Are Endpoints:** "A browser viewing Restricted data is an endpoint. If it's an unmanaged iPad at Starbucks, that's a data spill — same as if you left a printed evidence report on the table."
