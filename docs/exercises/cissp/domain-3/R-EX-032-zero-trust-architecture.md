# R-EX-032 — Zero trust architecture principles

**CISSP Reference:** Chapter 8, Sections "Secure Design Principles" and "Security Models", Pages 565–590; Chapter 14, Section "Zero-Trust Access Policy Enforcement"  
**Exam Objective:** 3.1.1 Understand security models and frameworks; 3.3.1 Apply secure design principles  
**Study Guide Key Terms:** Zero trust, never trust always verify, micro-segmentation, identity-aware proxy, ZTNA, SDP, perimeterless security, assume breach  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`config/asset-inventory.csv`](../../config/asset-inventory.csv)

---

## Scenario Context

Cadre Corp's network architecture follows a traditional perimeter model: a flat `192.168.77.0/24` subnet where domain controllers, member servers, SOC infrastructure, and analyst workstations all coexist with minimal internal segmentation. The assumption has been: "If you're on the internal network, you're trusted."

Three recent incidents have challenged this assumption:

1. During a campaign exercise, an attacker who compromised `ws01` (AST-007) could directly reach DC01 (AST-001) on port 389 because both are on the same flat subnet with no internal firewall.

2. The DarkAI research lab (AST-035, `172.20.0.0/24`) was supposed to be isolated, but because the Docker host sits on the lab network, a misconfigured bridge allowed DarkAI containers to reach the lab subnet.

3. A contractor's laptop was plugged into a lab switch port during a visit. It received a DHCP address in `192.168.77.0/24` and could ping DC01 before anyone noticed.

The CISO has asked: "What would a zero trust architecture look like for Cadre Corp, and which three changes would give us the most risk reduction for the least operational disruption?"

---

## Multiple-Choice Questions

**Question 1:** Which of the following is the CORE principle of zero trust architecture?

A. All users must use multi-factor authentication  
B. Network perimeters must be defended with next-generation firewalls  
C. No implicit trust based on network location — every access request must be authenticated, authorized, and encrypted  
D. All data must be encrypted at rest and in transit

**Question 2:** In Cadre Corp's flat network, an attacker on ws01 can reach DC01 directly. Which zero trust control would MOST effectively prevent this lateral movement?

A. Deploying a stronger password policy on DC01  
B. Implementing micro-segmentation — DC01 only accepts LDAP/Kerberos from authenticated, authorized sources, not arbitrary internal IPs  
C. Moving DC01 to a different subnet without changing access controls  
D. Installing antivirus on ws01

**Question 3:** The contractor laptop incident (unauthorized device on lab switch) would be best addressed by which zero trust capability?

A. MAC address filtering on all switches  
B. Network Access Control (NAC) with device identity verification — unknown devices get quarantined, not placed on the production subnet  
C. Disabling all unused switch ports  
D. Requiring contractors to sign an AUP before connecting

**Question 4:** What distinguishes zero trust from traditional defense-in-depth?

A. Zero trust uses more firewalls than defense-in-depth  
B. Zero trust eliminates the concept of a "trusted internal network" — defense-in-depth still assumes internal traffic is safer than external  
C. Defense-in-depth is obsolete; zero trust replaces it entirely  
D. There is no difference — they are the same concept

---

## Answer Explanations

**Answer 1: C**  
The core zero trust principle is **"never trust, always verify"** — no implicit trust based on network location. Every access request is individually authenticated, authorized, and encrypted, regardless of whether it originates from "inside" or "outside" the network. MFA (A) is a component but not the core principle. Perimeter firewalls (B) are the OPPOSITE of zero trust — they assume internal traffic is safe. Encryption (D) is important but not the defining principle.

**Answer 2: B**  
**Micro-segmentation** is the correct zero trust approach. Instead of allowing any host on `192.168.77.0/24` to talk to DC01, micro-segmentation enforces policy: only authenticated, authorized sources (specific IPs, specific services) can reach specific ports on DC01. An attacker on ws01 would be blocked by policy, not by network topology. Moving subnets (C) without policy change just moves the problem. Password policy (A) and antivirus (D) don't prevent network-level lateral movement.

**Answer 3: B**  
**Network Access Control (NAC) with device identity** is the correct answer. Zero trust applies to devices, not just users: before a device gets an IP on the production subnet, it must authenticate and prove compliance posture. Unknown/unmanaged devices go to a quarantine VLAN. MAC filtering (A) is trivially bypassed. Disabling ports (C) is operationally impractical. An AUP (D) is administrative, not technical.

**Answer 4: B**  
Zero trust **eliminates the "trusted internal network" assumption** that defense-in-depth still relies on. Defense-in-depth layers controls (firewall, IDS, auth, encryption) but still treats internal traffic as lower-risk. Zero trust says: the internal network is just as hostile as the internet — authenticate every connection. Zero trust doesn't replace defense-in-depth (C — it's an evolution, not a replacement), and they are not the same (D).

---

## Cadre Corp Application

1. **Three Highest-Impact ZT Changes for Cadre Corp:**
   - **Micro-segmentation for DCs:** Windows Defender Firewall rules on DC01-03 that restrict LDAP, Kerberos, SMB, RPC to only authorized management IPs and domain member subnets, not the entire `192.168.77.0/24`.
   - **NAC for lab access:** 802.1X on lab switch ports. Managed lab VMs get certificates; unknown devices (contractor laptops, rogue APs) get quarantined.
   - **Identity-aware access for SOC tools:** Elastic, Velociraptor, Arkime accessible only via authenticated proxy with MFA, not just "on the lab network = access granted."

2. **DarkAI Isolation as ZT Test Case:** The DarkAI Docker bridge misconfiguration is a perfect zero trust lesson — network adjacency should never imply trust. DarkAI containers should be on an isolated overlay network with explicit egress allowlists.

3. **Existing Controls to Leverage:** AD domain authentication (Kerberos), ADCS-issued certificates, and Windows Defender Firewall are already deployed — they just need zero trust policy enforcement, not new infrastructure.

---

## Interview Talking Points

1. **"Trusted Internal Network" Is Dead:** "The biggest lie in security is 'it's internal traffic, it's fine.' Every major breach of the last decade involved lateral movement inside the perimeter. Zero trust says: internal traffic is just as dangerous as internet traffic. Verify everything."

2. **Micro-Segmentation Before Macro-Budgets:** "You don't need a $500K zero trust platform. Start with: DCs only talk to authorized sources. Labs can't reach production. Unknown devices go to quarantine. Three firewall rules can reduce your blast radius by 80%."

3. **Assume Breach as Design Principle:** "Design like the attacker is already on your network — because in a DFIR firm, we know they eventually will be. If ws01 gets popped, can the attacker reach DC01? If the answer is yes, you don't have zero trust — you have zero segmentation."

4. **ZT Is a Journey, Not a Product:** "Zero trust isn't something you buy. It's a set of architectural principles you implement incrementally. Start with the crown jewels (DCs, evidence stores), enforce identity-based access, expand from there."
