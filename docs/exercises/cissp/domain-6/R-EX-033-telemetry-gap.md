# R-EX-033 — Telemetry gap analysis

**CISSP Reference:** Chapter 15, Section "Collecting Security Process Data"; Chapter 16, Section "Logging and Monitoring"; Chapter 17, Section "Detection and Preventive Measures"  
**Exam Objective:** 6.1.3 Analyze testing results; 7.2.1 Implement logging and monitoring; 7.2.2 Assess telemetry coverage  
**Study Guide Key Terms:** Telemetry coverage, detection gap, host-based telemetry, network-based telemetry, correlation, SIEM, source matrix, telemetry source diversity  
**Inputs:** Lab telemetry architecture (AST-010 ELK, AST-012 monitor/Zeek/Suricata), RISK-010, plan1.7 source matrix

---

## Scenario Context

Cadre Corp's detection architecture relies on two primary telemetry sources:

- **Host-based (AST-010 — Elastic):** Windows Event Logs from all 7 VMs (Winlogbeat), Sysmon EID 1/3/7/8/10/11, PowerShell 4104, and Velociraptor artifacts.
- **Network-based (AST-012 — monitor VM):** Zeek connection/DNS/HTTP/Kerberos logs, Suricata IDS alerts (34 custom rules), and Arkime full packet capture.

During the campaign exercise, the SOC team discovered that three critical attack steps had detection gaps:

1. **Kerberoast (Phase 2):** Windows Event ID 4769 (Kerberos TGS request) fired on DC01 — but without network corroboration from Zeek's kerberos.log (which shows the same TGS request with encryption type), the SOC couldn't distinguish a legitimate TGS request from a Kerberoast attempt. Host telemetry alone was ambiguous.

2. **DCSync (Phase 6):** Event ID 4662 (Directory Service Access) with DRSUAPI GUID fired — but Zeek's dce_rpc.log showed the SAME replication activity from a non-DC source IP (mbr01), providing the critical corroboration that this wasn't legitimate DC-to-DC replication.

3. **Lateral SMB movement (Phase 3):** The attacker moved from ws01 to mbr01 via SMB — Windows Event ID 5140 (network share access) fired, but without Zeek's smb.log showing the file access patterns, the SOC couldn't determine WHAT files were accessed.

RISK-010 rates the NSM gap as score 4, but after the campaign exercise, the CISO suspects this should be higher.

---

## Multiple-Choice Questions

**Question 1:** Why is dual-source telemetry (host + network) important for detection confidence?

A. It provides redundancy in case one source fails  
B. Host telemetry tells you WHAT happened on a system; network telemetry tells you HOW the attacker got there and WHERE they went next — together they provide the full attack story; either alone is incomplete  
C. Network telemetry replaces the need for host telemetry  
D. It's a compliance requirement with no operational value

**Question 2:** The SOC couldn't distinguish legitimate TGS requests from Kerberoast using host telemetry alone because:

A. Windows doesn't log Kerberos TGS requests  
B. Event ID 4769 fires for ALL TGS requests — legitimate service ticket requests look identical to Kerberoast requests at the host level; the network-level discriminator is the encryption type (RC4 = 0x17 is suspicious for Kerberoast) and the requesting source (unusual clients requesting service tickets)  
C. Host telemetry is always encrypted  
D. Kerberoast doesn't generate any Windows events

**Question 3:** If AST-012 (monitor VM) were to go dark (Zeek/Suricata stopped), what specific detection capability would Cadre Corp lose?

A. All detection capability — host telemetry is useless without network telemetry  
B. Protocol-level corroboration and independent network perspective — host telemetry would still detect events, but the SOC would lose the ability to: (a) confirm host events with network evidence, (b) detect network-only attacks (DDoS, port scans, DNS tunneling), (c) establish attack timelines across multiple hosts via network flow correlation  
C. Only DNS monitoring  
D. Only Suricata signature-based detection

**Question 4:** What is the appropriate risk treatment for a known telemetry gap that cannot be immediately closed?

A. Ignore it — gaps are inevitable  
B. Document the gap as a risk acceptance with: (a) specific attacks that may be missed, (b) compensating controls (increased host monitoring, more frequent manual reviews), (c) a target closure date, (d) executive sign-off  
C. Disable all detection until the gap is closed  
D. Purchase a new SIEM immediately regardless of cost

---

## Answer Explanations

**Answer 1: B**  
**Host + network = complete picture**. Host telemetry shows: a process ran, a registry key changed, an event log was cleared. Network telemetry shows: the attacker connected from IP X to IP Y on port Z, transferred N bytes, used protocol P. Without network telemetry, you know something happened on the host but not how the attacker arrived or where they went next. Without host telemetry, you see network traffic but not what it accomplished. Together, they tell the full attack narrative — critical for incident response and forensic reporting.

**Answer 2: B**  
Event ID 4769 fires for **every TGS request** — legitimate and malicious. The key discriminator is in the details: (a) Ticket Encryption Type = 0x17 (RC4-HMAC) is unusual for modern environments and strongly indicative of Kerberoast, (b) the requesting user account — is it normal for THIS user to request a ticket for THAT service?, (c) Zeek's kerberos.log independently logs the same request with encryption type and source/destination, providing corroboration from a different telemetry source. Host-only detection of Kerberoast via 4769 has a high false positive rate without network correlation.

**Answer 3: B**  
Losing network telemetry means losing **independent corroboration and network-native detection**. Host telemetry still detects: process creation, registry changes, event log activity, file access. But you lose: (a) network flow visibility (who talked to whom), (b) protocol-level attack detection (DNS tunneling, Kerberoast encryption type analysis, DCE-RPC operation codes), (c) independent verification of host events (did 4662 on DC01 correlate with DRSUAPI from a non-DC?), (d) network-only attacks (port scans, DDoS). Detection continues but is significantly degraded.

**Answer 4: B**  
**Documented risk acceptance with compensating controls** is the appropriate risk management response to a known gap that can't be immediately closed. This demonstrates: (a) the gap is known (not a surprise during an incident), (b) the risk has been assessed and accepted at the appropriate level, (c) compensating controls are in place to reduce residual risk, (d) there's a plan to close the gap (target date and resource ask). Ignoring (A) is negligence. Disabling detection (C) worsens the situation. Immediate purchase (D) may not be feasible or proportional.

---

## Cadre Corp Application

1. **Telemetry Source Matrix:** Complete the plan1.7 source matrix: for each campaign attack step, map PRIMARY and SECONDARY telemetry sources. Example — DCSync: PRIMARY = Windows 4662 + DRSUAPI GUID, SECONDARY = Zeek dce_rpc.log corroboration. This identifies exactly which attacks lose detection if a source goes dark.

2. **NSM Health Monitoring:** Add heartbeat monitoring for AST-012: if Zeek or Suricata stops producing logs, fire a critical alert. The RISK-010 score should be re-evaluated post-campaign — the exercise demonstrated NSM is critical to detection confidence, not just "nice to have."

3. **Gap Register:** Create a telemetry gap register documenting: (a) attack step, (b) current detection (host only? network only? both?), (c) gap description, (d) compensating controls, (e) target closure date. Review quarterly.

---

## Interview Talking Points

1. **One Source Is a Single Point of Failure:** "If your DCSync detection relies entirely on Windows Event ID 4662, and the attacker clears the event log before you collect it, you've lost detection. Network telemetry gives you the same event from a different source that the attacker can't easily tamper with. Source diversity is detection resilience."

2. **Host Tells You What; Network Tells You How:** "Host telemetry says 'a TGS request was made.' Network telemetry says 'it used RC4 encryption, came from an unusual workstation, and was followed by lateral SMB to mbr01.' The network perspective provides the narrative that turns individual events into an attack story."

3. **Known Gaps Are Managed Risks; Unknown Gaps Are Incidents:** "Document every detection gap you know about. A gap in a register with a risk acceptance and target closure date is managed. A gap you discover during an incident because 'nobody realized Zeek was the only source for DNS tunnel detection' is a failure of assessment."
