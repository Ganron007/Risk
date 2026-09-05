# R-EX-033 — Secure network segmentation design

**CISSP Reference:** Chapter 8, Section "Security Capabilities of Information Systems", Pages 590–600; Chapter 11, Section "Network Segmentation"  
**Exam Objective:** 3.3.1 Apply secure design principles; 4.1.1 Implement secure network architecture  
**Study Guide Key Terms:** Network segmentation, DMZ, VLAN, micro-segmentation, east-west traffic, defense-in-depth, blast radius, Purdue model  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`config/asset-inventory.csv`](../../config/asset-inventory.csv)

---

## Scenario Context

Cadre Corp's flat `192.168.77.0/24` lab network puts domain controllers, SOC monitoring, analyst workstations, and research labs on a single broadcast domain. The architecture diagram shows all VMs connected to `vmnet2` with no internal VLANs, no DMZ, and no segmentation between classification tiers.

The CISO is concerned: "We've got Restricted assets (DCs with client authentication data, forensic evidence stores) on the same subnet as Internal assets (analyst workstations, provisioning tools). If an attacker compromises ws01 through a phishing email, they're one hop from our domain controllers."

You have been asked to design a segmented network architecture that:
1. Separates Restricted, Confidential, and Internal assets into different security zones
2. Maintains operational functionality (Ansible provisioning, SOC monitoring, domain authentication)
3. Can be implemented without major infrastructure changes (no new hardware)
4. Reduces the blast radius of a workstation compromise

---

## Multiple-Choice Questions

**Question 1:** What is the PRIMARY security benefit of placing DC01 (Restricted) and ws01 (Internal) on different network segments with a firewall between them?

A. Improved network performance due to reduced broadcast traffic  
B. Blast radius reduction — compromise of ws01 does not grant direct network access to DC01  
C. Simplified IP addressing scheme  
D. Reduced bandwidth consumption between segments

**Question 2:** In a properly segmented Cadre Corp network, where should the SOC monitoring infrastructure (ELK, Velociraptor) be placed?

A. On the same segment as domain controllers for maximum visibility  
B. In a dedicated SOC/management segment with controlled inbound access from monitored assets and restricted outbound access  
C. On the internet-facing DMZ for remote analyst access  
D. On the same segment as analyst workstations for convenience

**Question 3:** Which of the following is a VALID reason NOT to over-segment a network?

A. Segmentation is never a bad idea — more is always better  
B. Excessive segmentation increases operational complexity, troubleshooting difficulty, and may break legitimate application flows if not carefully designed  
C. Firewalls between segments eliminate all security risks, so fewer segments are sufficient  
D. VLANs are deprecated and should not be used for segmentation

**Question 4:** For Cadre Corp's lab environment (which uses VMware virtual networking), what is the most practical first segmentation step?

A. Purchase hardware firewalls for each segment  
B. Implement VMware virtual distributed switches with NSX micro-segmentation  
C. Use existing Windows Defender Firewall on each VM to enforce host-based segmentation rules while planning longer-term VLAN architecture  
D. Move all Restricted assets to a physically separate network with dedicated switches

---

## Answer Explanations

**Answer 1: B**  
The primary benefit is **blast radius reduction**. If ws01 (an analyst workstation, most likely initial compromise vector) is compromised, the attacker has direct Layer 2/3 access to every host on the flat `192.168.77.0/24` subnet — including DC01. With segmentation, even if ws01 is fully compromised, the attacker must now traverse a firewall or access control list to reach DC01, buying detection time and limiting lateral movement options.

**Answer 2: B**  
SOC infrastructure should be in a **dedicated management segment**. This provides: (a) controlled inbound access — monitored assets push logs/telemetry to SOC, not the reverse, (b) restricted outbound access — SOC tools shouldn't initiate connections to arbitrary assets, (c) isolation from both the assets being monitored and the analyst workstations accessing dashboards. Option A puts the SOC at the same risk level as the DCs. Option C exposes SOC tools to the internet. Option D defeats the purpose.

**Answer 3: B**  
**Excessive segmentation increases operational complexity** and can break legitimate application flows. Every firewall rule is a potential troubleshooting point; every VLAN adds management overhead. The goal is risk-appropriate segmentation, not maximum segmentation. "More is always better" (A) ignores operational cost. Firewalls don't eliminate all risks (C). VLANs are not deprecated (D).

**Answer 4: C**  
**Host-based firewall rules** (Windows Defender Firewall, iptables) are the most practical first step. They require zero new infrastructure, can be deployed via existing Ansible playbooks, and provide immediate blast radius reduction. They're also reversible and testable per-host. Hardware firewalls (A) and NSX (B) are expensive/long-term. Physical separation (D) is impractical for a virtualized lab.

---

## Cadre Corp Application

1. **Proposed Three-Zone Segmentation:**
   - **Restricted Zone** (192.168.77.0/27): DC01-03, ADCS CA, Entra ID sync — only domain auth traffic and management from provisioning
   - **Confidential Zone** (192.168.77.32/27): mbr01-02, linux01, elk, vr, monitor — business services and SOC monitoring
   - **Internal Zone** (192.168.77.64/27): ws01, provisioning, DarkAI Docker host — workstations and deployment tooling

2. **Host-Based Firewall First:** Use the existing `04-vulnerabilities.yml` Ansible playbook pattern to deploy Windows Defender Firewall rules that restrict DC SMB/RPC/LDAP to only the provisioning server and domain members. This is immediate, testable, and reversible.

3. **SOC Monitoring Access Model:** ELK and Velociraptor should accept inbound connections from monitored assets (log shipping, VR agent check-ins) but NOT initiate outbound connections to them. Analyst access to dashboards via authenticated web proxy, not direct network access.

4. **Verification in Lab:** After deploying segmentation rules, re-run campaign Phase 0 network recon from Kali — the attack surface should be visibly reduced compared to the flat network.

---

## Interview Talking Points

1. **Flat Network = No Blast Radius:** "A flat network means every compromise is a potential domain admin. The attacker lands on ws01, and DC01 is one ping away. Segmentation is the single highest-impact control for reducing lateral movement."

2. **Start With What You Have:** "You don't need NSX or hardware firewalls for basic segmentation. Windows Defender Firewall rules on each DC — 'only accept LDAP from these IPs' — costs nothing and deploys in minutes via Ansible. That's immediate risk reduction."

3. **SOC Segregation Is Counterintuitive:** "People want SOC tools 'close to the action.' But if your SIEM is on the same segment as your DCs, a DC compromise could mean SIEM compromise — and now you're blind. The SOC segment should be a separate security zone."

4. **Operational Realism:** "I can design a 15-zone segmented architecture that looks beautiful on a whiteboard and breaks production on day one. Three zones — Restricted, Confidential, Internal — mapped to our existing classification scheme, is practical and defensible."
