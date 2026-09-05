# R-EX-014 — Business continuity strategy selection

**CISSP Reference:** Chapter 3, Section "Continuity Planning", Pages 285-289  
**Exam Objective:** 1.4.1 Implement business continuity strategies  
**Study Guide Key Terms:** Business continuity planning (BCP), business impact analysis (BIA), recovery time objective (RTO), recovery point objective (RPO), continuity strategies  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-appetite-statement.md`](../risk-appetite-statement.md), [`../risk-register-baseline.md`](../risk-register-baseline.md)

---

## Scenario Context

Cadre Corp's DFIR operations depend heavily on continuous availability of several critical systems: the SIEM (AST-010) for real-time threat detection, Velociraptor (AST-011) for endpoint collection, and client evidence storage (AST-030) for forensic data. A recent risk assessment has identified that a prolonged outage of these systems would prevent Cadre Corp from fulfilling client SLAs, potentially resulting in contract penalties and reputational damage.

The CEO has requested a business continuity strategy that addresses the following scenarios:
- Ransomware attack encrypting the SIEM and evidence storage
- Data center failure affecting the on-premises VMware environment
- Cloud provider outage affecting Entra ID and Azure resources
- Key personnel unavailability during a major incident

The current state includes:
- No formal business continuity plan (BCP)
- No documented recovery time objectives (RTOs) or recovery point objectives (RPOs)
- No backup strategy for client evidence beyond local storage
- No alternate processing site or cloud failover capability
- No documented crisis management structure

You need to recommend appropriate continuity strategies for each critical system, considering Cadre Corp's risk appetite (low for client data, moderate for research labs) and budget constraints.

---

## Multiple-Choice Questions

**Question 1:** For client evidence storage (AST-030), which of the following continuity strategies would be most appropriate given Cadre Corp's low risk appetite for client data compromise?

A. Hot site with real-time replication to a geographically separate data center  
B. Cold site with weekly backup tapes shipped offsite  
C. Warm site with daily incremental backups  
D. Accept the risk and rely on local RAID storage

**Question 2:** The SIEM (AST-010) has an RTO of 4 hours and an RPO of 1 hour based on client SLA requirements. Which of the following continuity strategies best meets these requirements?

A. Daily backups to cloud storage with 24-hour recovery time  
B. Real-time log shipping to a cloud SIEM instance with automatic failover  
C. Weekly full backups with daily incremental backups stored locally  
D. No continuity strategy—accept downtime as operational risk

**Question 3:** For the DarkAI research lab (AST-035), which has a moderate risk appetite and lower business criticality, which of the following would be the most cost-effective continuity strategy?

A. Hot site with real-time replication  
B. Warm site with weekly backups  
C. Cold site with monthly backups  
D. No continuity strategy—rebuild from source code if needed

**Question 4:** When presenting the business continuity strategy to the board, which of the following arguments would be most compelling for investing in a hot site for critical systems?

A. "Hot sites are required by ISO 27001 and SOC 2 for all systems"  
B. "A hot site ensures we can meet client SLAs and avoid contract penalties during outages"  
C. "Hot sites are the cheapest continuity option available"  
D. "Hot sites eliminate the need for any other security controls"

---

## Answer Explanations

**Answer 1: A**  
A hot site with real-time replication to a geographically separate data center is most appropriate for client evidence storage given the low risk appetite. Client evidence is classified as Restricted because breach is existential to Cadre Corp. A hot site provides near-zero RTO and RPO, ensuring evidence availability even during catastrophic failures. Cold sites (B) and warm sites (C) have unacceptable recovery times for critical client data. Accepting the risk (D) contradicts the stated low risk appetite.

**Answer 2: B**  
Real-time log shipping to a cloud SIEM instance with automatic failover best meets the 4-hour RTO and 1-hour RPO requirements. Real-time shipping ensures minimal data loss (RPO near zero), and automatic failover enables rapid recovery (RTO within 4 hours). Daily cloud backups (A) have 24-hour RTO, exceeding the requirement. Local backups (C) don't protect against site-wide failures. Accepting the risk (D) violates client SLAs.

**Answer 3: D**  
No continuity strategy with rebuild from source code is the most cost-effective approach for the DarkAI research lab. With moderate risk appetite and lower business criticality, the cost of hot/warm/cold sites outweighs the benefit. The lab can be rebuilt from source code and configurations if needed, with acceptable downtime. This aligns risk management investment with business impact—critical systems get robust continuity, research systems get minimal investment.

**Answer 4: B**  
"A hot site ensures we can meet client SLAs and avoid contract penalties during outages" is the most compelling argument because it addresses business impact directly. Hot sites are not required by ISO 27001 or SOC 2 for all systems (A) - requirements are risk-based. Hot sites are typically the most expensive option (C), not the cheapest. Hot sites don't eliminate the need for other controls (D) - they're one part of a comprehensive strategy. The business case should focus on SLA compliance and revenue protection.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's business continuity needs by:

1. **Risk-Based Strategy:** Aligning continuity investment with risk appetite (low for client data, moderate for research labs)
2. **SLA-Driven Requirements:** Using RTO/RPO based on client contractual obligations
3. **Cost Optimization:** Applying appropriate continuity strategies based on system criticality
4. **BCP Foundation:** Establishing the basis for a formal business continuity plan

**Lab Connection:** After completing this exercise, you can:
- Review the risk register (`docs/risk-register-baseline.md`) to identify systems requiring continuity strategies
- Examine the risk appetite statement (`docs/risk-appetite-statement.md`) to guide investment decisions
- Consider how the SIEM (AST-010) and evidence storage (AST-030) could be configured for high availability
- Evaluate cloud options for failover capability (Azure, AWS)

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **Risk-Based Continuity Investment:** "I align business continuity investment with risk appetite and business impact. For Cadre Corp, client evidence and SIEM systems get hot site replication because they're critical to operations and SLA compliance. Research labs get minimal continuity investment because the business impact is lower."

2. **RTO/RPO-Driven Strategy:** "Recovery time and recovery point objectives drive continuity strategy selection. I work with business stakeholders to define RTOs based on client SLAs and operational needs, then select the most cost-effective strategy that meets those requirements."

3. **Cost Optimization:** "Not all systems need the same level of continuity protection. I use a tiered approach: critical systems get hot sites, important systems get warm sites, and non-critical systems get cold sites or rebuild strategies. This optimizes spend while protecting business-critical operations."

4. **Cloud vs. On-Premises:** "For DFIR operations, I evaluate cloud failover options carefully. Cloud provides geographic distribution and rapid scalability, but I must consider data sovereignty for client evidence and regulatory requirements. Hybrid approaches often provide the best balance."

5. **Testing and Maintenance:** "A continuity strategy is only valuable if it works when needed. I establish regular testing schedules—quarterly for critical systems, annually for others—and maintain the strategy through ongoing updates as systems and requirements change."

---

## Task

1. Define RTO and RPO for Cadre Corp's top 5 critical systems.
2. Recommend appropriate continuity strategies for each system based on risk appetite.
3. Estimate the cost-benefit ratio for each recommended strategy.
4. Describe the testing and maintenance approach for the selected strategies.

## Answer key

1. **RTO/RPO for critical systems:**
   - **AST-030 (Client evidence storage):** RTO 1 hour, RPO 0 minutes (zero tolerance for data loss)
   - **AST-010 (SIEM):** RTO 4 hours, RPO 1 hour (based on client SLAs)
   - **AST-011 (Velociraptor):** RTO 8 hours, RPO 4 hours (important but not critical)
   - **AST-001-003 (Domain controllers):** RTO 2 hours, RPO 15 minutes (identity plane critical)
   - **AST-020 (Entra ID):** RTO 1 hour, RPO 0 minutes (cloud identity, high availability built-in)

2. **Continuity strategies:**
   - **AST-030:** Hot site with real-time replication to geographically separate location
   - **AST-010:** Warm site with real-time log shipping to cloud SIEM, automatic failover
   - **AST-011:** Warm site with daily backups, 8-hour recovery capability
   - **AST-001-003:** Hot site with real-time replication (AD requires minimal downtime)
   - **AST-020:** Leverage cloud provider's built-in high availability (geo-redundancy)
   - **AST-035 (DarkAI):** Cold site or rebuild strategy (moderate risk appetite)

3. **Cost-benefit analysis:**
   - **Hot sites (AST-030, AST-001-003):** High cost ($50K-100K annually) but prevents existential client data loss
   - **Warm sites (AST-010, AST-011):** Medium cost ($20K-50K annually) with good balance of protection and cost
   - **Cloud high availability (AST-020):** Low incremental cost (built into cloud pricing)
   - **Rebuild strategy (AST-035):** Minimal cost ($5K annually for backups) with acceptable downtime

4. **Testing and maintenance:**
   - **Critical systems (hot sites):** Quarterly failover testing with full validation
   - **Important systems (warm sites):** Semi-annual testing with functional validation
   - **Cloud systems:** Annual review of HA configuration and failover procedures
   - **Documentation:** Update BCP after any system changes, quarterly review of RTO/RPO
   - **Training:** Annual BCP training for all staff, tabletop exercises semi-annually

**Pass criteria:** You can design a business continuity strategy that balances protection requirements with cost constraints while aligning with risk appetite and business priorities.
