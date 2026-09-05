# R-EX-020 — Media sanitation and data remanence

**CISSP Reference:** Chapter 5, Sections "Data Destruction", "Media Sanitation", Pages 408–415; NIST SP 800-88 Rev 1  
**Exam Objective:** 2.1.5 Manage data destruction and media sanitation  
**Study Guide Key Terms:** Data remanence, media sanitation, clear, purge, destroy, crypto-shredding, degaussing, NIST SP 800-88, residual data  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`config/asset-inventory.csv`](../../config/asset-inventory.csv)

---

## Scenario Context

Cadre Corp is decommissioning mbr01 (AST-004) — a member server that hosted SQL Server 2025 with "client-like" data used in campaign exercises. The VM's virtual disk (500 GB) contains: MSSQL databases with simulated client PII, AD service account credentials cached in LSASS memory dumps, SCCM deployment logs with network topology details, and Ansible-deployed configurations with lab secrets.

The VM will be deleted from the VMware host, but the CISO is concerned about data remanence: deleted files on the virtual disk could be recovered by the next tenant if the underlying physical storage is re-provisioned. Additionally:

1. Three VMware snapshots of mbr01 exist from campaign checkpoint saves — these also contain the MSSQL data and credentials.
2. The VM was backed up to the cloud backup provider (AST-023) nightly — those backups retain data per the provider's 90-day retention policy.
3. A junior admin suggests: "Just delete the VM from VMware — the data's gone, right?"

The CISO asks you to design a media sanitation procedure that addresses the VM disk, snapshots, and cloud backups.

---

## Multiple-Choice Questions

**Question 1:** According to NIST SP 800-88, what is the difference between "Clear," "Purge," and "Destroy" for media sanitation?

A. They are interchangeable terms with no practical difference  
B. Clear = logical techniques to prevent non-invasive recovery (overwrite); Purge = physical or logical techniques making data infeasible to recover even with laboratory attacks (crypto-shred, degauss); Destroy = physically render the media unusable (shred, incinerate)  
C. Clear = delete files; Purge = format the disk; Destroy = unplug the device  
D. Only Destroy is acceptable for any data; Clear and Purge are obsolete

**Question 2:** The junior admin's suggestion to "just delete the VM" is insufficient because:

A. VMware deletion automatically performs secure erase  
B. Deleting a VM removes the VM configuration but typically does NOT overwrite the virtual disk — the disk blocks remain on physical storage and can be recovered by the next tenant or with forensic tools; the data is "deleted" but not "sanitized"  
C. VMware requires a 30-day waiting period before deletion  
D. VM deletion requires CISO approval

**Question 3:** The three VMware snapshots of mbr01 also contain the MSSQL data. What must be done with them?

A. Nothing — snapshots are automatically deleted with the VM  
B. Snapshots must be deleted as part of the sanitation procedure — each snapshot is a separate virtual disk containing the data as it existed at the snapshot time; deleting the base VM without deleting snapshots leaves recoverable data  
C. Snapshots can be kept for historical purposes indefinitely  
D. Snapshots are read-only and don't contain actual data

**Question 4:** For the cloud backups (AST-023) that retain mbr01 data per the provider's 90-day policy, what is the correct approach?

A. Wait 90 days for the backups to expire — no action needed  
B. Request immediate deletion of the specific backup data from the provider, verify deletion, and document the destruction — do not wait for automatic expiration, which leaves data recoverable for 90 days after decommissioning  
C. Cloud backups are automatically encrypted and don't need sanitation  
D. Download all backups, sanitize them locally, and re-upload

---

## Answer Explanations

**Answer 1: B**  
NIST SP 800-88 defines three levels: **Clear** — overwrite with non-sensitive data, protecting against simple non-invasive recovery (suitable for Internal data); **Purge** — cryptographic erase (destroy encryption keys) or degaussing, protecting against laboratory-level recovery (suitable for Confidential/Restricted data); **Destroy** — physical destruction (shred, incinerate, pulverize), rendering the media unusable (required for highest-sensitivity media that cannot be purged). For Cadre Corp's Restricted data (client evidence, credentials), Purge is the minimum standard.

**Answer 2: B**  
Deleting a VM removes configuration metadata but typically doesn't overwrite the virtual disk. The disk blocks — containing MSSQL databases, credentials, and configurations — remain on the physical storage until overwritten by new data. A forensic analyst (or the next tenant of that physical storage) could recover this data. NIST SP 800-88 requires that sanitation renders data "infeasible to recover" — VM deletion alone does not meet this standard.

**Answer 3: B**  
VMware snapshots are delta disks that preserve the VM's state at the snapshot time — including all data. If the base VM is sanitized but snapshots remain, the data survives in the snapshot files. All snapshots must be identified, deleted, and the underlying storage blocks sanitized as part of the decommissioning procedure. Snapshots are not automatically cleaned up (A) and they contain the full VM data at the time of the snapshot (D is false).

**Answer 4: B**  
**Immediate, verified deletion** — not waiting for automatic expiration. The 90-day retention period means the data remains recoverable for 90 days post-decommissioning. If the VM is decommissioned because it contained Restricted data, leaving backups online for 90 days creates a window where the data still exists and could be accessed or breached. Request immediate deletion, obtain confirmation from the provider, and document the destruction in the asset decommissioning record.

---

## Cadre Corp Application

1. **Media Sanitation Procedure:** For decommissioning any lab VM that processed Restricted or Confidential data: (a) identify all data locations (VM disk, snapshots, backups, replicas), (b) for Restricted data: crypto-shred the virtual disk (destroy encryption keys, then overwrite), (c) delete all snapshots, (d) request immediate cloud backup deletion with verification, (e) update `config/asset-inventory.csv` to mark the asset as "decommissioned — sanitized" with date and method, (f) retain the sanitation certificate for audit.

2. **Sanitation Level by Classification:** Internal data → Clear (single-pass overwrite); Confidential → Purge (crypto-shred); Restricted → Purge with verification (crypto-shred + verification read). Physical destruction only when media leaves Cadre Corp's control (e.g., failed drives sent for disposal).

3. **Cloud Backup Sanitation Clause:** Review the cloud backup provider contract — ensure it includes a provision for immediate, verified deletion upon request. If the contract only offers "wait for retention period," this is a risk acceptance that must be documented and approved.

---

## Interview Talking Points

1. **Delete Is Not Sanitize:** "'Just delete the VM' is what people say before a data breach. Deletion removes pointers to data; sanitation removes the data. NIST SP 800-88 exists because these are fundamentally different operations. For Restricted data, you purge — never just delete."

2. **Snapshots Are Backup Copies:** "Every VMware snapshot is a separate copy of the data at that point in time. Sanitizing the base VM while leaving snapshots is like shredding the original document but keeping the photocopies. Track and sanitize every copy — VM, snapshots, backups, and replicas."

3. **Cloud Backups Don't Self-Destruct:** "Your cloud provider's 90-day retention policy is a feature for recovery, not a sanitation control. When you decommission a Restricted asset, those 90 days are 90 days of unnecessary exposure. Request immediate deletion and get written confirmation."
