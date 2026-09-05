# R-EX-025 — Asset inventory accuracy and maintenance

**CISSP Reference:** Chapter 5, Section "Identifying and Classifying Information and Assets", Pages 383–395  
**Exam Objective:** 2.1.1 Identify and classify information and assets  
**Study Guide Key Terms:** Asset inventory, asset lifecycle, configuration management, CMDB, asset tagging, inventory accuracy  
**Inputs:** [`config/asset-inventory.csv`](../../config/asset-inventory.csv), [`../enterprise-context.md`](../enterprise-context.md)

---

## Scenario Context

Cadre Corp's asset inventory (`config/asset-inventory.csv`) was created six months ago during the initial risk program setup. Since then, the IT team has:

1. Deployed a new Velociraptor collector VM (`.52`) that doesn't appear in the inventory.
2. Decommissioned an old SCCM distribution point that still shows as active in the CSV.
3. Migrated three client evidence stores from on-premises NTFS shares to Azure Blob Storage (now `AST-030A`, `AST-030B`, `AST-030C`), but the inventory still lists a single `AST-030`.
4. Added the CADRE-RevEng lab (`.41`, `.42`) and the C2Stack lab (`172.21.0.0/24`) — neither inventoried.

During a quarterly risk review, the CISO discovered these discrepancies when a RISK-008 (Velociraptor artifact store unauthorized access) assessment referenced the old single-server inventory, missing the new `.52` collector entirely. The board has asked: "How do we know our risk register covers everything if we don't know what we have?"

---

## Multiple-Choice Questions

**Question 1:** What is the PRIMARY risk of an inaccurate asset inventory for Cadre Corp?

A. Increased software licensing costs from unaccounted VMs  
B. Incomplete risk coverage — un-inventoried assets have no risk entries, no controls, and no monitoring  
C. SOC 2 audit finding for documentation gap (minor severity)  
D. Slower incident response due to unclear asset ownership

**Question 2:** Which asset lifecycle event should trigger an immediate inventory update?

A. Quarterly scheduled review  
B. Any change in asset status (deployed, modified, decommissioned, migrated)  
C. Annual SOC 2 audit preparation  
D. When the CISO remembers to ask

**Question 3:** The migration of client evidence from on-premises (AST-030) to three Azure Blob Storage containers (AST-030A/B/C) represents what kind of inventory management challenge?

A. Asset tagging inconsistency  
B. One-to-many asset decomposition requiring new unique identifiers  
C. Cloud asset discovery limitations  
D. Classification downgrade due to cloud migration

**Question 4:** What is the most effective control to prevent inventory drift like the un-inventoried Velociraptor `.52` collector?

A. Annual physical inventory of all server racks  
B. Automated discovery integrated with deployment pipelines — every provisioned VM auto-registers in the inventory  
C. Manager sign-off on all new server requests  
D. Quarterly manual review of all hypervisor VM lists

---

## Answer Explanations

**Answer 1: B**  
The primary risk of an inaccurate inventory is **incomplete risk coverage**. If an asset doesn't exist in the inventory, it can't have risk entries in the register, controls assigned to it, or monitoring configured for it. The Velociraptor `.52` collector is a perfect example — RISK-008 analysis was performed against stale data, missing the new attack surface entirely. SOC 2 findings (C) are a symptom, not the root risk.

**Answer 2: B**  
Inventory updates should be **event-driven** — any change in asset status triggers an immediate update. This is a foundational configuration management principle. Quarterly reviews (A) are a compensating control when event-driven updates aren't feasible, but they guarantee up to 90 days of drift. Waiting for audit prep (C) or CISO memory (D) is not a control at all.

**Answer 3: B**  
The migration from one on-premises store to three cloud containers represents a **one-to-many decomposition**. The original `AST-030` must be split into `AST-030A`, `AST-030B`, `AST-030C` with potentially different classification levels, access controls, and risk profiles. This is an inventory design challenge: the schema must support asset decomposition without losing lineage to the original identifier.

**Answer 4: B**  
**Automated discovery integrated with deployment pipelines** is the most effective control. Modern infrastructure-as-code (Ansible, Terraform — Cadre Corp uses Ansible) should auto-register every provisioned resource in the inventory at creation time. Manual processes (A, C, D) have latency and human error baked in. For a lab environment with frequent changes, automation is the only scalable answer.

---

## Cadre Corp Application

1. **Inventory Automation in Ansible:** The `cadre.py` deployment tool already knows every VM it creates. A post-deploy hook that appends new VMs to `config/asset-inventory.csv` with classification, owner, and category would close the drift gap for new assets.

2. **Decommissioning Workflow:** When VMs are destroyed (`vagrant destroy`), a cleanup script should mark them as `decommissioned` with a date in the inventory rather than deleting the row. Decommissioned assets still matter for historical risk context.

3. **Cloud Asset Discovery:** For Azure-based evidence stores, consider using Azure Resource Graph queries or Microsoft Defender for Cloud inventory export to feed into the inventory CSV. Hybrid inventory (on-prem + cloud) requires dual discovery mechanisms.

4. **Reconciliation Cycle:** Add a quarterly reconciliation task (`R2-S3.6`) to diff the inventory against live hypervisor VM lists, DNS records, and cloud resource groups. Any delta triggers an immediate risk review.

---

## Interview Talking Points

1. **Inventory = Risk Foundation:** "You can't protect what you don't know you have. An inaccurate asset inventory means your risk register is lying to the board. Every un-inventoried asset is an unmanaged risk."

2. **Event-Driven, Not Calendar-Driven:** "I don't update the inventory quarterly — I design processes so it updates itself. Every deploy, every decommission, every migration triggers an inventory change. Calendar-based reviews are a safety net, not the primary control."

3. **Decomposition Matters:** "When you split one asset into three, you create three new risk surfaces. Each needs its own entry, its own classification, its own controls. 'AST-030' that used to mean one thing now means three — that's not a typo, that's a risk gap."

4. **Automation as Control:** "Manual asset inventories are always wrong. Always. The only inventory you can trust is one that's generated by the same automation that deploys your infrastructure."
