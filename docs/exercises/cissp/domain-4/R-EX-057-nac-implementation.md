# R-EX-057 — Network access control (NAC) implementation

**CISSP Reference:** Chapter 11, Section "Secure Network Components"; Chapter 13, Section "Identity and Access Provisioning"  
**Exam Objective:** 4.1.2 Secure network components; 5.1.1 Control physical and logical access  
**Study Guide Key Terms:** NAC, 802.1X, RADIUS, posture assessment, quarantine VLAN, persistent agent vs agentless, BYOD  
**Inputs:** Cadre Corp lab network topology, asset inventory

---

## Scenario Context

Recall the contractor laptop incident from R-EX-032: an unmanaged device was plugged into a lab switch and received a DHCP address on the production `192.168.77.0/24` subnet, gaining immediate network access to DC01. Additionally, the DFIR team occasionally connects client-provided evidence laptops to the lab network for imaging — these devices are potentially compromised and should NEVER have network access.

The CISO has asked you to design a NAC solution that: (1) prevents unknown devices from accessing the production network, (2) quarantines client evidence devices to an isolated imaging VLAN, and (3) verifies that managed devices meet security posture requirements before granting access.

---

## Multiple-Choice Questions

**Question 1:** In a NAC architecture using 802.1X, what is the role of the RADIUS server?

A. It assigns IP addresses to connecting devices  
B. It acts as the authentication server — it receives credentials from the supplicant (device) via the authenticator (switch/AP), validates them against a directory (e.g., Active Directory), and returns an access decision  
C. It encrypts all network traffic after authentication  
D. It monitors network bandwidth usage

**Question 2:** What is a quarantine VLAN in NAC terminology?

A. A VLAN with the fastest network speeds for priority devices  
B. A restricted network segment where non-compliant or unauthenticated devices are placed — they can access remediation services (patch server, AV updates) but cannot reach production resources  
C. A VLAN dedicated to virus scanning  
D. A VLAN that deletes itself after 30 days

**Question 3:** For client evidence laptops that may be compromised, which NAC policy is appropriate?

A. Full network access — the forensic tools need internet access  
B. Dynamic VLAN assignment to an isolated imaging network that has NO route to the production network or internet — only the forensic imaging server is reachable  
C. The same access as employee laptops — they need email and internet  
D. No NAC policy needed — forensic devices are exempt from security controls

**Question 4:** What is the difference between persistent and agentless NAC?

A. Persistent NAC uses an installed agent on the endpoint for continuous posture checking; agentless NAC uses browser-based or 802.1X-only assessment at connection time  
B. Persistent NAC requires physical access; agentless works remotely  
C. Persistent NAC is always more secure than agentless  
D. There is no difference — the terms are interchangeable

---

## Answer Explanations

**Answer 1: B**  
The RADIUS server is the **authentication and authorization decision point** in 802.1X. The switch/Wi-Fi AP (authenticator) forwards credentials from the device (supplicant) to the RADIUS server, which validates against AD and returns: accept (with VLAN assignment), reject, or quarantine. RADIUS doesn't assign IPs (A — that's DHCP), encrypt traffic (C — that's the role of the encrypted wireless/TLS layer), or monitor bandwidth (D).

**Answer 2: B**  
A **quarantine VLAN** is a restricted segment for devices that fail authentication or posture checks. It typically allows access only to remediation resources (patch management, antivirus updates, captive portal for registration). This is the "fix yourself, then try again" model — the device can't reach production until it passes compliance.

**Answer 3: B**  
Client evidence devices must go to an **isolated imaging VLAN** with exactly one reachable destination: the forensic imaging server. No internet access (prevents malware from phoning home), no production network access (prevents lateral movement from a compromised device). This is a practical application of least privilege networking.

**Answer 4: A**  
**Persistent NAC uses an agent** installed on the endpoint that continuously monitors posture (AV running? Patches current? Firewall on?) and can enforce policies even after initial connection. **Agentless NAC** assesses posture only at connection time via browser redirect or 802.1X attributes — simpler to deploy but provides only point-in-time assessment, not continuous enforcement.

---

## Cadre Corp Application

1. **Lab NAC Implementation:** Deploy Windows NPS (RADIUS) on a member server. Configure 802.1X on lab switch ports (or VMware virtual switch port security). Managed VMs authenticate via computer certificates (ADCS auto-enrollment). Unknown devices → quarantine VLAN.

2. **Evidence Imaging VLAN:** Create a dedicated port group in VMware for client evidence devices. Firewall rules: only the forensic imaging server is reachable. No default gateway (no internet). This VLAN is the NAC-assigned segment for evidence devices.

3. **Posture Assessment:** For managed VMs, verify: domain-joined, specific security patches installed, Windows Defender running, specific services enabled. Non-compliant → quarantine VLAN with access to WSUS and remediation scripts.

---

## Interview Talking Points

1. **NAC Answers "What's on My Network?":** "Without NAC, any device with an Ethernet port can join your network. The contractor's laptop, the compromised evidence machine, the rogue AP someone plugged in for better Wi-Fi — they all get IPs and access. NAC says: no authentication, no IP. No compliance, no production access."

2. **Quarantine, Not Deny:** "The goal isn't to block devices — it's to isolate them safely. A device that fails posture check goes to quarantine, gets remediated, and tries again. This is security that enables, not just blocks."
