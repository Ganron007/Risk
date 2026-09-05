# R-EX-051 — OSI model security considerations per layer

**CISSP Reference:** Chapter 11, Sections "OSI Model" and "TCP/IP Model", Pages 785–810  
**Exam Objective:** 4.1.1 Implement secure network architecture; 4.1.2 Secure network components  
**Study Guide Key Terms:** OSI model, TCP/IP model, encapsulation, Layer 2 attacks, Layer 3 attacks, Layer 7 attacks, defense-in-depth  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), CADRE lab network topology

---

## Scenario Context

Cadre Corp's SOC team detected an attack that traversed multiple layers of the network stack during a campaign exercise:

1. **Layer 1:** The attacker plugged a rogue device into an unsecured lab switch port (physical access).
2. **Layer 2:** ARP spoofing redirected traffic between ws01 and the default gateway.
3. **Layer 3:** ICMP tunneling exfiltrated data through ping packets that bypassed the egress firewall.
4. **Layer 4:** A TCP SYN flood against DC01's port 88 (Kerberos) caused authentication delays.
5. **Layer 7:** An HTTP POST to the Elastic API injected a malicious Sigma rule that disabled detection for the attacker's subsequent moves.

The junior SOC analyst said: "I don't get it — we had a firewall and Suricata running. Why didn't they stop this?" The SOC Lead responded: "Because the attack spanned seven layers, and our controls only covered three."

You have been asked to map each layer of the OSI model to the security controls that should protect it in Cadre Corp's environment.

---

## Multiple-Choice Questions

**Question 1:** ARP spoofing operates at which OSI layer?

A. Layer 3 (Network)  
B. Layer 2 (Data Link)  
C. Layer 4 (Transport)  
D. Layer 7 (Application)

**Question 2:** Which security control is specifically designed to prevent Layer 2 attacks like ARP spoofing?

A. TLS 1.3 encryption  
B. IPsec VPN  
C. Dynamic ARP Inspection (DAI) on managed switches, combined with DHCP snooping  
D. Web application firewall (WAF)

**Question 3:** The ICMP tunneling data exfiltration (Layer 3) bypassed the egress firewall because:

A. The firewall was misconfigured  
B. ICMP is a Layer 3 protocol — most firewalls allow ping by default, and detecting tunneled data inside ICMP payloads requires deep packet inspection (Layer 7 analysis), not just header filtering  
C. ICMP is encrypted and cannot be inspected  
D. The attacker used IPv6 which bypasses IPv4 firewall rules

**Question 4:** A defense-in-depth approach to network security across OSI layers means:

A. Deploying the strongest possible firewall at Layer 3 and relying on it for all protection  
B. Implementing security controls at multiple layers — if one layer's control fails, the next layer provides protection  
C. Using only encryption to protect data at all layers  
D. Focusing all security controls on Layer 7 where applications operate

---

## Answer Explanations

**Answer 1: B**  
ARP (Address Resolution Protocol) operates at **Layer 2 (Data Link)**. It resolves IP addresses to MAC addresses within a local network segment. ARP has no authentication mechanism — any host can claim any IP address. This is why ARP spoofing is a classic Layer 2 attack: the attacker sends forged ARP replies associating their MAC address with the gateway's IP, redirecting traffic through the attacker's machine.

**Answer 2: C**  
**Dynamic ARP Inspection (DAI) with DHCP snooping** is the correct Layer 2 defense. DAI validates ARP packets against a trusted binding database (built by DHCP snooping), dropping ARP packets with invalid IP-to-MAC bindings. TLS (A) and IPsec (B) operate at higher layers and don't prevent ARP spoofing. A WAF (D) operates at Layer 7.

**Answer 3: B**  
Firewalls filter on packet headers (source/destination IP, port, protocol). If ICMP is allowed (common for network diagnostics), the firewall passes the packet. The exfiltrated data is hidden INSIDE the ICMP payload, which requires **deep packet inspection** (Suricata/Zeek at Layer 7) to detect anomalous payload sizes, patterns, or entropy in ICMP packets. IPv6 (D) is a separate concern — the tunnel works over IPv4 ICMP too.

**Answer 4: B**  
**Defense-in-depth** means layered controls. If the attacker bypasses physical security (Layer 1), DAI at Layer 2 still blocks ARP spoofing. If DAI is misconfigured, a stateful firewall (Layer 3/4) should detect anomalous traffic patterns. If the firewall misses it, Suricata/Zeek (Layer 7 payload inspection) should flag the ICMP tunnel. No single layer is sufficient; security comes from overlapping controls.

---

## Cadre Corp Application

1. **Layer-by-Layer Control Mapping for Cadre Corp:**
   - **L1 (Physical):** Locked lab room, 802.1X on switch ports, disable unused ports
   - **L2 (Data Link):** DAI + DHCP snooping on lab switches (currently not deployed — gap)
   - **L3 (Network):** Windows Defender Firewall on each VM, subnet isolation
   - **L4 (Transport):** Stateful firewall rules, TCP SYN flood protection (SYN cookies)
   - **L5-6 (Session/Presentation):** Kerberos authentication, TLS for all management UIs
   - **L7 (Application):** Suricata IDS/IPS, Zeek network analysis, Elastic SIEM rules

2. **Current Gaps:** Cadre Corp's flat network means Layers 2-3 controls are minimal. DAI is not deployed on the virtual switch. Layer 7 detection (Suricata/Zeek) is deployed but needs tuning for ICMP tunnel detection.

3. **Lab Exercise:** Run the campaign Phase 0 network recon from Kali — identify which OSI layers the recon touches and which controls detect each touch. This maps directly to the source matrix in the main CADRE plan1.7.

---

## Interview Talking Points

1. **Security Is Laminated, Not Monolithic:** "Think of network security like laminated glass — each layer stops what the layer above missed. ARP spoofing (L2) bypasses your fancy L7 WAF. ICMP tunnels (L3) bypass your L4 stateful firewall. If you only secure one layer, you're not secured."

2. **Know What Lives Where:** "When someone says 'the firewall will stop it,' ask: at which layer? A network firewall sees IPs and ports. It doesn't see ARP poisoning, ICMP payloads, or HTTP body anomalies. Different layers, different controls."

3. **ICMP Is Not Benign:** "Ping is not 'just ping.' ICMP can tunnel data, map networks, and exfiltrate information. If you allow all ICMP everywhere, you're giving attackers a free covert channel. ICMP should be filtered and inspected like any other protocol."
