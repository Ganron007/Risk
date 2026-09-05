# R-EX-052 — Secure network architecture (DMZ, VLAN, subnetting)

**CISSP Reference:** Chapter 11, Sections "Network Segmentation", "Edge Networks", "Secure Network Components"  
**Exam Objective:** 4.1.1 Implement secure network architecture  
**Study Guide Key Terms:** DMZ, VLAN, subnetting, screened subnet, bastion host, zero trust, micro-segmentation, defense-in-depth  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`config/asset-inventory.csv`](../../config/asset-inventory.csv)

---

## Scenario Context

Cadre Corp is expanding its SOC services to include a client-facing threat intelligence portal where clients can view their own real-time SIEM alerts and forensic case status. This portal will be hosted on a new VM (`portal01`, 192.168.77.70) running a web application that queries Elasticsearch and Velociraptor APIs.

The architecture team has proposed three designs:

**Design A (Flat):** Place portal01 on the existing `192.168.77.0/24` subnet with all other assets. "It's simpler — one subnet, no routing complexity."

**Design B (DMZ):** Place portal01 in a screened subnet (DMZ) with two firewalls — external firewall allowing HTTPS from internet clients, internal firewall restricting portal01 to only Elastic and Velociraptor API ports.

**Design C (Three-Tier):** Web tier (portal01 in DMZ), App tier (API gateway in app segment), Data tier (Elastic/VR in SOC segment) — each tier in its own security zone with strict ingress/egress rules.

---

## Multiple-Choice Questions

**Question 1:** Design A (flat network) creates what PRIMARY risk for the client-facing portal?

A. Slower network performance due to shared broadcast domain  
B. Portal compromise directly exposes DCs, evidence stores, and all lab infrastructure with no network barriers  
C. Increased IP address consumption  
D. Difficulty configuring DNS for the portal

**Question 2:** In Design B (DMZ), what is the correct firewall rule set for portal01?

A. Allow all traffic from portal01 to internal network — it needs full access for monitoring  
B. Deny all inbound from internet except TCP/443 (HTTPS); deny all outbound to internal except specific API ports to Elastic (9200) and Velociraptor (8000); deny all other traffic  
C. Allow unrestricted access between portal01 and internal network since they're in the same DMZ  
D. Only allow ICMP between portal01 and internal network

**Question 3:** Why is a "screened subnet" (DMZ with firewalls on both sides) superior to a single external firewall with internal hosts exposed?

A. It provides two layers of defense — even if the external firewall is compromised, the internal firewall still protects the internal network  
B. It costs the same as a single firewall  
C. It eliminates the need for host-based firewalls  
D. It's required by SOC 2 compliance

**Question 4:** For Cadre Corp's specific risk profile, where should the SOC monitoring segment sit relative to the DMZ?

A. In the DMZ with the web portal — monitoring tools need internet access  
B. In the internal network, with strict ingress rules allowing only monitored assets to push data to SOC, and analyst access via authenticated proxy — never in the DMZ  
C. Completely air-gapped from both DMZ and internal network  
D. On the same segment as domain controllers for maximum visibility

---

## Answer Explanations

**Answer 1: B**  
A flat network means **portal compromise = infrastructure-wide access**. If an attacker exploits a vulnerability in the client portal (the most internet-exposed asset), they land on the same subnet as DC01, evidence stores, and all lab systems. There are zero network barriers to lateral movement. This is the exact scenario segmentation prevents.

**Answer 2: B**  
The correct DMZ rule set follows **least privilege**: portal01 needs exactly two things — accept HTTPS from clients (internet → portal:443) and query SOC APIs (portal → Elastic:9200, VR:8000). Everything else is denied. "Allow all" (A) defeats the DMZ purpose. "Unrestricted internal" (C) means the DMZ is a false front. ICMP-only (D) is insufficient for API queries.

**Answer 3: A**  
A screened subnet provides **defense-in-depth**: two independently configured firewalls from potentially different vendors/configurations. Compromising one doesn't automatically compromise the other. If the external firewall has a zero-day, the internal firewall (with a different rule set and attack surface) still blocks access to internal assets. SOC 2 (D) doesn't specifically mandate dual firewalls.

**Answer 4: B**  
SOC monitoring tools should be in the **internal network behind both firewalls**, NOT in the DMZ. The DMZ is the most exposed zone — putting your monitoring infrastructure there means an attacker who compromises the DMZ can disable or manipulate monitoring. SOC tools accept push data from monitored assets; they don't need to be internet-accessible.

---

## Cadre Corp Application

1. **Recommended Architecture:** For the client portal, begin with Design B (DMZ) as a practical first step. The existing VMware virtual networking can implement this with host-based firewall rules and separate port groups per zone. Design C (three-tier) is the long-term target.

2. **Existing Lab as DMZ Testbed:** The `192.168.77.0/24` lab already has SOC monitoring (elk, vr, monitor) and production (DCs, members) on one subnet. A practical exercise: use Windows Defender Firewall to simulate DMZ rules — restrict cross-zone traffic and verify with campaign recon tools.

3. **Portal01 Firewall Rules in Ansible:** If portal01 is deployed, its firewall rules should be managed via Ansible (same pattern as `04-vulnerabilities.yml`), not manually configured — ensuring consistency and auditability.

---

## Interview Talking Points

1. **DMZ Is Not Optional for Internet-Facing Services:** "Anything accessible from the internet that can reach your internal network is a bridge for attackers. A DMZ breaks that bridge. If your client portal sits on the same subnet as your domain controllers, you've built a highway from the internet to your crown jewels."

2. **Least Privilege Applies to Networks Too:** "A server needs exactly the network paths required for its function — nothing more. If portal01 only needs Elastic:9200 and VR:8000, every other port and destination is denied. That's network least privilege."

3. **Two Firewalls, Two Vendors, Two Configs:** "In high-security environments, the external and internal DMZ firewalls should be different vendors. A vulnerability in one vendor's OS doesn't automatically expose both. This is defense-in-depth at the network perimeter level."
