# R-EX-038 — Detection gap analysis: host-only telemetry limitations

**CISSP Reference:** Chapter 16, Section "Logging and Monitoring"; Chapter 17, Sections "Detection and Preventive Measures", "Logging and Monitoring"  
**Exam Objective:** 7.2.1 Implement logging and monitoring; 7.2.2 Assess detection coverage; 6.1.3 Analyze testing results for detection gaps  
**Study Guide Key Terms:** Detection gap, host-based detection, network-based detection, telemetry diversity, single-source risk, corroboration, detection engineering  
**Inputs:** Campaign Phase 3 telemetry (Elastic Endpoint Events), RISK-010, plan1.7 §10

---

## Scenario Context

During the campaign exercise, the SOC team tested a scenario where ONLY host-based telemetry was available — simulating a failure of the monitor VM (AST-012) that runs Zeek and Suricata. The attack chain was: **Kerberoast → SQL Server IMPERSONATE → xp_cmdshell → SYSTEM → lateral SMB to DC01.**

With only Elastic Defend events (process creation, network connections, file modifications, registry changes), the SOC detected:

- **✅ Kerberoast:** Event ID 4769 (TGS request with RC4 encryption) — detected but with lower confidence (could be legitimate service ticket request).
- **⚠️ SQL IMPERSONATE:** MSSQL error log entry — detected but no network evidence of WHERE the SQL connection came from.
- **✅ xp_cmdshell:** Process creation event (cmd.exe spawned by sqlservr.exe) — clearly malicious.
- **❌ Lateral SMB to DC01:** Event ID 5140 (network share access) fired — but without Zeek's smb.log showing WHICH files were accessed and the SMB command sequence, the SOC couldn't determine the scope of the lateral movement.

Key finding: three of four attack steps were detected, but with significantly lower confidence and context than when network telemetry was available.

---

## Multiple-Choice Questions

**Question 1:** Without Suricata/Zeek network telemetry, the Kerberoast detection (Event 4769) had lower confidence because:

A. Event 4769 doesn't fire for Kerberoast attacks  
B. Host telemetry alone cannot distinguish between a legitimate TGS request (user accessing a file share) and a Kerberoast TGS request (attacker requesting a ticket for offline cracking) — the network-level evidence (encryption type 0x17, unusual requesting source, TGS request patterns) provides the discrimination  
C. Kerberoast detection requires full packet capture  
D. Elastic Endpoint events don't include Kerberos logs

**Question 2:** The lateral SMB movement detection gap (Event 5140 fired but file access details were missing) is most significant because:

A. Lateral movement is the least important attack phase to detect  
B. Without network-level SMB logs, the SOC knows the attacker accessed a share but NOT which files — making it impossible to determine: (a) was client evidence accessed?, (b) were credential files (SAM, NTDS.dit) exfiltrated?, (c) what was the attacker's objective? — the scope of compromise is unknown  
C. SMB logging is not available on Windows Server 2025  
D. Lateral movement detection is only relevant for compliance

**Question 3:** The SQL IMPERSONATE step was detected via MSSQL error logs but the SOC couldn't determine WHERE the connection came from without network telemetry. This gap affects:

A. Only compliance reporting  
B. Incident scoping — without the source IP, the SOC can't determine if the attacker connected from an internal compromised host (lateral movement) or externally (initial access); the response strategy differs significantly based on the source  
C. Only the performance of the investigation  
D. Only the post-incident report quality

**Question 4:** What is the appropriate compensating control when network telemetry is unavailable?

A. Accept the gap — nothing can be done  
B. Enhanced host-based logging — enable additional Windows Event Log channels (SMB Client/Server operational logs, PowerShell ScriptBlock logging 4104, Sysmon Event ID 18 for pipe connections), increase log verbosity, and deploy additional VR hunts for lateral movement artifacts (Prefetch, ShimCache, AmCache)  
C. Disable all detection until network telemetry is restored  
D. Purchase a second SIEM to replace network telemetry

---

## Answer Explanations

**Answer 1: B**  
Event 4769 fires for **all TGS requests** — legitimate and malicious. The host event shows: user X requested a ticket for service Y. Without network context, this could be: (a) a user accessing a file server (normal), or (b) an attacker requesting a ticket for offline Kerberoasting (malicious). Network telemetry adds: encryption type (RC4 = 0x17 is suspicious), the network flow showing the request came from an unusual workstation, and correlation with other suspicious activity from the same source. Host telemetry gives the event; network telemetry gives the context.

**Answer 2: B**  
Without network-level SMB logs, the **scope of data access is unknown**. Event 5140 says "a share was accessed" — but not which files within the share. If the share contains client evidence, the SOC can't confirm or deny evidence access. This is the difference between "we detected an intrusion" and "we can tell the client exactly what was accessed." For a DFIR firm, this distinction is existential — client notification requirements depend on whether their data was actually accessed.

**Answer 3: B**  
The **source attribution gap** directly impacts incident response strategy. External source = the attacker has internet access to the SQL Server (firewall misconfiguration, exposed port) → response: close the external access. Internal source = the attacker is already inside the network, pivoting from a compromised host → response: larger-scope incident, hunt for initial access vector, potentially multiple compromised hosts. The same detection (SQL IMPERSONATE) requires different responses based on source — which only network telemetry can provide.

**Answer 4: B**  
**Enhanced host-based logging** is the correct compensating control. When network telemetry is unavailable: (a) enable SMB Client/Server operational logs for file-level access auditing, (b) enable PowerShell ScriptBlock logging (4104) for command-line auditing, (c) deploy Sysmon for detailed process/network/pipe event logging, (d) increase VR hunt frequency for lateral movement IOCs. Host telemetry can partially compensate — not replace, but reduce the gap until network telemetry is restored.

---

## Cadre Corp Application

1. **Network Telemetry as Critical Infrastructure:** Reclassify AST-012 (monitor VM) reliability as a Critical detection dependency. If Zeek/Suricata are down for >15 minutes, trigger a High-severity incident and activate enhanced host-based logging as compensating control. Update RISK-010 score from 4 to 6 based on campaign findings.

2. **Host Logging Enhancement:** Deploy additional Windows Event Log channels via Ansible: SMB operational logs, PowerShell 4104 (already partially deployed), Sysmon 18 (named pipe events), and Windows Defender Firewall operational logs. These provide host-level context that partially compensates for missing network telemetry.

3. **Detection Confidence Scoring:** Add a confidence score to each detection rule: Host-only detection = Medium confidence; Host + Network corroborated = High confidence. This guides the SOC: Medium confidence alerts require additional investigation before escalation; High confidence alerts can be escalated immediately.

---

## Interview Talking Points

1. **Host Tells You Something Happened; Network Tells You Why It Matters:** "Event 5140 says 'SMB share accessed.' That's the what. Network telemetry says 'the attacker copied payroll.xlsx, client_evidence.img, and NTDS.dit.' That's the why it matters. Detection without context is an alarm; detection with context is an incident response."

2. **Detection Confidence Requires Corroboration:** "A single-source detection should never be the basis for client notification. You need corroboration from an independent source. Host says DCSync. Network says DCSync. Now you have confidence. Either alone is a lead; both together is a finding."

3. **Every Monitoring Source Is a Single Point of Detection Failure:** "When Zeek is down, you lose the ability to scope lateral movement. When Suricata is down, you lose signature-based attack detection. Your detection architecture should document what you lose when each source fails — and have documented compensating controls ready."
