# R-EX-058 — Secure DNS and DHCP configuration

**CISSP Reference:** Chapter 11, Section "DNS Security"; Chapter 12, Section "Network Attacks"  
**Exam Objective:** 4.1.1 Implement secure network architecture; 4.1.2 Secure network components  
**Study Guide Key Terms:** DNSSEC, DNS over HTTPS (DoH), DNS over TLS (DoT), DHCP snooping, DNSSEC validation, cache poisoning, DNS tunneling  
**Inputs:** Cadre Corp lab DNS infrastructure (DC01 as primary DNS), `00-domain-deploy.yml`

---

## Scenario Context

Cadre Corp's lab DNS infrastructure runs on DC01 (the forest root domain controller), which provides DNS for `cadre.local`, `child.cadre.local`, and `range.local`. During a campaign exercise, the SOC team discovered:

1. **DNS cache poisoning test:** An attacker on Kali successfully poisoned DC01's DNS cache by spoofing a response to a recursive query, redirecting `elk.cadre.local` to the attacker's IP. Analysts who then browsed to the ELK dashboard were sent to the attacker's fake login page.

2. **DNS tunneling:** The attacker exfiltrated 12 MB of simulated client data by encoding it in DNS TXT queries to `exfil.attacker.com` — traffic that looked like normal DNS resolution and passed through the firewall.

3. **No DNSSEC:** `cadre.local` is an internal domain with no DNSSEC signing. The infrastructure team argues "DNSSEC is only for public domains."

4. **DHCP rogue server:** During a lab reconfiguration, a test VM accidentally ran a DHCP server and started handing out IP addresses with the attacker's DNS server as the default — redirecting all DNS queries from new DHCP clients.

---

## Multiple-Choice Questions

**Question 1:** DNSSEC protects against DNS cache poisoning by:

A. Encrypting all DNS queries end-to-end  
B. Adding cryptographic signatures to DNS records — resolvers can verify that a response came from the authoritative server and wasn't tampered with in transit  
C. Blocking all recursive DNS queries  
D. Using only TCP for DNS instead of UDP

**Question 2:** DNS tunneling (exfiltrating data via DNS queries) is difficult to block because:

A. DNS uses strong encryption that firewalls can't inspect  
B. DNS is typically allowed through firewalls (UDP/53 is often open by default), and the exfiltrated data looks like normal DNS query traffic without deep inspection  
C. DNS tunneling only works on IPv6  
D. DNS tunneling is impossible to detect with any technology

**Question 3:** DHCP snooping on network switches prevents rogue DHCP servers by:

A. Encrypting all DHCP traffic  
B. Designating trusted ports (where legitimate DHCP servers reside) — DHCP offers from untrusted ports are dropped, preventing rogue DHCP servers from operating  
C. Requiring all DHCP clients to authenticate with 802.1X  
D. Disabling DHCP entirely and requiring static IP configuration

**Question 4:** For Cadre Corp's internal `cadre.local` domain, is DNSSEC appropriate?

A. No — DNSSEC is only for public internet domains  
B. Yes — internal domains benefit from DNSSEC's integrity protection; domain-joined clients can validate DNSSEC-signed internal records, preventing cache poisoning and man-in-the-middle attacks against internal services  
C. No — Active Directory DNS doesn't support DNSSEC  
D. Yes — but only if the domain is also accessible from the internet

---

## Answer Explanations

**Answer 1: B**  
DNSSEC adds **cryptographic signatures** (RRSIG records) to DNS data. A resolver can follow the chain of trust from the root zone down to the specific record, verifying each signature. If an attacker spoofs a response, the signature won't validate, and the resolver rejects it. DNSSEC provides integrity and authenticity, not confidentiality — it doesn't encrypt queries (A — that's DoH/DoT).

**Answer 2: B**  
DNS is **universally allowed** through firewalls because DNS is essential for almost all network communication. Attackers exploit this by encoding data in DNS query names (e.g., `base64encodeddata.exfil.attacker.com`). Without deep packet inspection that analyzes DNS query entropy, length, and frequency patterns, this looks identical to legitimate DNS traffic. This is exactly why Cadre Corp needs Suricata/Zeek DNS anomaly rules.

**Answer 3: B**  
**DHCP snooping** classifies switch ports as trusted (uplink to legitimate DHCP server) or untrusted (end-user ports). DHCP OFFER and ACK messages from untrusted ports are dropped. This prevents anyone plugging in a rogue DHCP server from hijacking the network's IP assignment. It's a Layer 2 security feature on managed switches.

**Answer 4: B**  
**Internal domains absolutely benefit from DNSSEC**. Windows Server DNS supports DNSSEC signing and validation for AD-integrated zones. Domain-joined clients can be configured (via Group Policy) to require DNSSEC validation for specific zones. This prevents the exact cache poisoning attack demonstrated in the campaign exercise — redirecting `elk.cadre.local` to an attacker's IP.

---

## Cadre Corp Application

1. **DNSSEC for cadre.local:** Enable DNSSEC signing on DC01's DNS server for the `cadre.local` zone. Configure Group Policy to require DNSSEC validation on domain-joined clients. This directly mitigates the DNS cache poisoning RISK-010 (NSM gap) sub-risk.

2. **DHCP Snooping:** In VMware virtual networking, implement DHCP filtering at the virtual switch level or via Windows DHCP server's "DHCP Guard" feature. Authorize only the designated DHCP server (DC01). All other DHCP offers are dropped.

3. **DNS Tunneling Detection:** Deploy Suricata rules for DNS tunneling: high-entropy query names, unusually long query names (>52 characters), high volume of TXT queries to a single domain, and queries to recently registered domains. Complement with Zeek's `cadre-dns-anomaly.zeek` script.

4. **DoH/DoT Policy:** For lab VMs that need internet DNS, consider DNS over HTTPS (DoH) to prevent DNS manipulation. However, this bypasses internal DNS monitoring — the tradeoff requires a DoH proxy that logs queries.

---

## Interview Talking Points

1. **DNS Is Both Critical and Fragile:** "DNS is the phonebook of your network. If an attacker controls DNS, they control where your users go. DNSSEC is the caller ID for DNS — it proves the answer came from the right place."

2. **DNS Tunneling Is the Covert Channel That Works Everywhere:** "Firewalls block everything except DNS, because nothing works without DNS. Attackers know this. DNS tunneling encodes data in queries that look completely normal unless you're doing deep entropy analysis on DNS traffic."

3. **Rogue DHCP Is a One-Box Takeover:** "A single misconfigured VM running a DHCP server can redirect every new client's DNS and gateway. DHCP snooping is a 5-minute switch configuration that prevents a catastrophic network hijack."
