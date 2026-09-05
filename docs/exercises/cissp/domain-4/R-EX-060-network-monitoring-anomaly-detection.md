# R-EX-060 — Network monitoring and anomaly detection

**CISSP Reference:** Chapter 12, Section "Network Monitoring and Management"; Chapter 16, Section "Logging and Monitoring"  
**Exam Objective:** 4.3.1 Implement network monitoring; 7.2.1 Implement logging and monitoring  
**Study Guide Key Terms:** IDS, IPS, network anomaly detection, flow analysis, Zeek, Suricata, SiLK, full packet capture, baseline deviation  
**Inputs:** Cadre Corp SOC infrastructure (monitor VM, Zeek, Suricata, Arkime), `plan1.7-defense-deepening.md`

---

## Scenario Context

Cadre Corp's monitor VM (`192.168.77.55`) runs Zeek 8.0.8 (network security monitoring), Suricata 8.0.5 (IDS/IPS), Arkime (full packet capture and search), and SiLK (flow analysis). During the last campaign exercise:

1. **Suricata detected** the Kerberoast attack (SID:1000015, 7 fires) and DCSync (SID:1000002, 63 fires) — the SOC team was alerted.
2. **Zeek detected** DNS tunneling (high-entropy query names to `.tk` TLD) — but the SOC team hadn't configured Zeek notice forwarding to Elastic, so the alert sat in a log file nobody read.
3. **SiLK flow data** showed an anomalous 2 AM spike in outbound traffic from ws01 to an IP in a country Cadre Corp has no business with — flagged as "informational" and ignored.
4. **Arkime full packet capture** contained the actual exfiltrated data, but nobody searched for it because nobody knew to look.

The CISO observed: "We have $500K worth of network monitoring tools and $0 worth of monitoring process. The tools work. The process doesn't."

---

## Multiple-Choice Questions

**Question 1:** What is the difference between an IDS (Intrusion Detection System) and an IPS (Intrusion Prevention System)?

A. IDS uses signatures; IPS uses AI  
B. IDS detects and alerts on suspicious traffic; IPS detects AND actively blocks/drops the malicious traffic — IDS is passive, IPS is inline  
C. IDS monitors inbound traffic; IPS monitors outbound  
D. There is no difference — the terms are interchangeable

**Question 2:** Zeek (formerly Bro) is best described as:

A. A signature-based IDS that matches patterns against a rule database  
B. A network security monitoring platform that logs comprehensive protocol-level metadata — it doesn't block traffic but provides rich forensic data about every connection  
C. A firewall with built-in antivirus  
D. A packet capture device with no analysis capabilities

**Question 3:** Cadre Corp's SOC had tools that detected the attack at multiple layers but failed to respond. This is a failure in:

A. Tool selection — the tools were inadequate  
B. Alert triage and SOC workflow — tools generated alerts, but alerts weren't aggregated, prioritized, or acted upon by humans  
C. Network bandwidth — the alerts were dropped due to congestion  
D. Encryption — the alerts were encrypted and unreadable

**Question 4:** Network flow analysis (NetFlow/IPFIX, SiLK) complements packet inspection (Suricata) by providing:

A. More detailed payload analysis than packet inspection  
B. Metadata-level visibility: who talked to whom, when, how much, on which ports — without the storage cost of full packet capture — enabling long-term traffic pattern and anomaly analysis  
C. Replacement for all other monitoring tools  
D. Real-time blocking of malicious traffic

---

## Answer Explanations

**Answer 1: B**  
**IDS detects and alerts; IPS detects and blocks.** This is the fundamental architectural difference. An IDS sits out-of-band (receives a copy of traffic via SPAN/mirror port) — if it misses an attack, the attack succeeds. An IPS sits inline (traffic flows THROUGH it) — if it detects an attack, it drops the packets before they reach the target. The tradeoff: IPS can block legitimate traffic (false positive → denial of service); IDS cannot.

**Answer 2: B**  
**Zeek is a network security monitoring platform**, not a signature-based IDS. It generates comprehensive logs (conn.log, dns.log, http.log, kerberos.log, etc.) with protocol-level metadata for every connection. This is fundamentally different from Suricata's signature-based approach — Zeek tells you WHAT happened (metadata), Suricata tells you if it was BAD (signature match). They're complementary.

**Answer 3: B**  
This is an **alert triage and workflow failure**. The tools functioned correctly — Suricata fired 63 alerts for DCSync. But alerts weren't aggregated into Elastic, weren't prioritized, and weren't reviewed by a human analyst within the detection timeframe. This is the most common SOC failure mode: tools work, process doesn't. No amount of tool investment fixes a broken triage workflow.

**Answer 4: B**  
**Flow analysis provides metadata-level visibility** at a fraction of the storage cost of full packet capture. While Suricata inspects packet payloads (expensive, high storage), SiLK records only connection metadata: source IP, destination IP, ports, protocol, bytes transferred, timestamps. This enables long-term trend analysis (e.g., "which internal hosts talked to this suspicious IP in the last 90 days?") that would be impossible with full PCAP storage alone.

---

## Cadre Corp Application

1. **Alert Pipeline Fix:** Connect Zeek notices to Elasticsearch (already configured via Custom Logs Filestream but needs validation). Ensure Suricata EVE JSON → Elastic pipeline is live. Create Elastic SIEM rules that correlate Suricata alerts + Zeek metadata + Windows Event Logs into actionable cases.

2. **Flow Analysis Baseline:** Run SiLK against 30 days of lab traffic to establish a baseline of normal behavior. Then flag deviations: unusual outbound destinations, after-hours traffic spikes, protocols on unexpected ports. This catches what signature-based tools miss.

3. **SOC Runbook:** Create an alert triage runbook: (1) alert fires → (2) enrich with Zeek connection metadata → (3) check SiLK for historical patterns → (4) pull relevant Arkime PCAP → (5) create Elastic case → (6) escalate or close. The process is as important as the tools.

---

## Interview Talking Points

1. **Tools Without Process = Expensive Noise:** "The tools detected every attack. Not one alert was acted upon. That's not a tool gap — that's a SOC maturity gap. I'd rather have 3 detection rules with a working triage process than 300 rules generating alerts nobody reads."

2. **Zeek + Suricata = Metadata + Verdicts:** "Zeek tells you what happened on your network. Suricata tells you if it was malicious. You need both. Zeek without Suricata is a historian; Suricata without Zeek is an alarm with no context."

3. **Flow Data Is the Long-Term Memory:** "Full packet capture is too expensive to store forever. Flow data gives you 90 days of 'who talked to whom' for the storage cost of about 4 hours of full PCAP. When an IOC drops weeks after an incident, flow data answers 'were we affected?'"
