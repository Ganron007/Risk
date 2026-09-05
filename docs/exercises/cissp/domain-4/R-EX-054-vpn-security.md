# R-EX-054 — VPN security (IPsec vs SSL/TLS)

**CISSP Reference:** Chapter 12, Sections "VPN Technologies", "Remote Access Security Management"  
**Exam Objective:** 4.2.1 Secure remote access; 4.2.2 Implement secure communication channels  
**Study Guide Key Terms:** IPsec, SSL/TLS VPN, IKEv2, split tunneling, always-on VPN, Perfect Forward Secrecy, IKEv2 vs SSL-VPN  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md)

---

## Scenario Context

Cadre Corp's DFIR analysts need secure remote access to the lab environment for after-hours incident response. Currently, analysts RDP directly to ws01 over the internet (port 3389 forwarded through the lab's NAT), authenticating with domain credentials. The SOC Lead calls this "a breach waiting to happen."

Three VPN options are proposed:

1. **IPsec IKEv2 VPN** — client-to-site, requires client software, operates at Layer 3, encrypts all IP traffic.
2. **SSL/TLS VPN** — browser-based or thin client, operates at Layer 7, can be portal-based (access specific apps via web) or tunnel-based (full network access via SSL tunnel).
3. **WireGuard** — modern kernel-level VPN, simpler codebase, UDP-based, designed for ease of configuration.

The CISO has asked you to recommend the appropriate VPN technology considering that analysts will be transferring large forensic images (50–500 MB) and need low-latency access to SOC dashboards.

---

## Multiple-Choice Questions

**Question 1:** What is the PRIMARY security advantage of IPsec IKEv2 over SSL/TLS VPN for Cadre Corp's use case?

A. IPsec is easier to configure than SSL VPN  
B. IPsec operates at Layer 3, encrypting ALL IP traffic uniformly, while SSL VPN often defaults to split tunneling where only specific traffic goes through the tunnel  
C. IPsec doesn't require certificates — it uses pre-shared keys only  
D. IPsec is faster than SSL VPN for all workloads

**Question 2:** Split tunneling in a VPN context refers to:

A. Encrypting traffic with two different algorithms simultaneously  
B. Routing only corporate-bound traffic through the VPN tunnel while internet-bound traffic goes directly to the internet — bypassing corporate security controls  
C. Using two VPN connections simultaneously for redundancy  
D. Splitting a single VPN tunnel across multiple physical links

**Question 3:** Perfect Forward Secrecy (PFS) in IPsec means:

A. The VPN connection never drops  
B. If the VPN server's long-term private key is compromised, past session keys cannot be decrypted because ephemeral keys were used for each session  
C. The VPN tunnel automatically reroutes around network failures  
D. All traffic is perfectly encrypted with no overhead

**Question 4:** For analysts transferring large forensic images, which VPN consideration is MOST important?

A. The VPN client's graphical user interface design  
B. MTU/MSS considerations — VPN encapsulation adds overhead; IPsec ESP can fragment large packets, while SSL VPN's TCP-over-TCP problem can cause severe performance degradation on lossy links  
C. The VPN vendor's market share  
D. The VPN's ability to display connection duration

---

## Answer Explanations

**Answer 1: B**  
IPsec's Layer 3 operation means **all traffic is encrypted by default** — no split tunneling unless explicitly configured. SSL VPNs commonly default to split tunneling for performance, which means the analyst's internet traffic (including potentially malicious sites) bypasses corporate controls, and sensitive DNS queries may leak. IPsec requires more setup (A is false), supports certificates (C is false), and isn't universally faster (D is false).

**Answer 2: B**  
**Split tunneling** routes only corporate traffic through the VPN; everything else goes directly to the internet. The security risk: the analyst's machine is simultaneously on the corporate network (via VPN) AND the internet (direct), creating a bridge that malware can exploit to pivot from the internet into the corporate network.

**Answer 3: B**  
**Perfect Forward Secrecy** ensures compromise of the server's long-term key doesn't compromise past sessions. Each session uses ephemeral Diffie-Hellman key exchange — the session keys are derived per-session and discarded afterward. Even if an attacker records all encrypted traffic and later steals the server's private key, they cannot decrypt past sessions. IKEv2 supports PFS; not all VPN configurations enable it.

**Answer 4: B**  
**MTU/MSS and protocol overhead** are critical for large file transfers. IPsec ESP encapsulation adds ~50-70 bytes per packet, which can cause fragmentation if path MTU discovery fails. SSL VPN's TCP-over-TCP problem (TCP tunnel inside TCP transport) causes multiplicative backoff on packet loss — devastating for large transfers on lossy links. WireGuard avoids both issues with UDP transport and clean MTU handling.

---

## Cadre Corp Application

1. **Recommendation:** WireGuard for analyst remote access. Simpler than IPsec (4,000 lines of code vs. 400,000+ for IPsec/OpenVPN), UDP-based (no TCP-over-TCP), modern cryptography (Curve25519, ChaCha20, BLAKE2s), and kernel-level performance for large forensic transfers.

2. **Split Tunneling Policy:** Disable split tunneling. All analyst traffic routes through the VPN when connected. This prevents DNS leaks and internet-to-corporate pivoting.

3. **RDP over VPN, Not RDP to Internet:** The current RDP-to-internet setup must be decommissioned. RDP access only via VPN tunnel. Port 3389 must not be exposed to the internet.

4. **Certificate-Based Authentication:** Use ADCS-issued certificates (AST-034) for VPN authentication, not pre-shared keys. Certificates can be revoked; pre-shared keys can't be individually invalidated.

---

## Interview Talking Points

1. **Split Tunneling = Split Security:** "When an analyst's traffic goes to Netflix via their home ISP and to client evidence via VPN simultaneously, their compromised smart TV is now a bridge to our corporate network. Disable split tunneling. Route everything through the tunnel."

2. **TCP-over-TCP Is a Performance Killer:** "SSL VPN tunnels TCP inside TCP. When the outer TCP connection experiences packet loss, both layers retransmit independently — exponential backoff on exponential backoff. For large forensic file transfers, this is unusable. Use UDP-based VPNs."

3. **WireGuard Is the Modern Answer:** "4,000 lines of auditable code vs. hundreds of thousands for legacy VPNs. WireGuard isn't just simpler to configure — it's simpler to verify. For a security firm, auditable infrastructure is a competitive advantage."
