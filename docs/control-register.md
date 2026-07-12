# Cadre Corp — Control Register

> **Sprint 1:** R2-S1.7  
> Crosswalk: CADRE capabilities → NIST CSF → ISO 27001 (illustrative).  
> IDs match `config/risk-mapping.yml`.

| Control ID | CADRE capability | NIST CSF | ISO 27001 (approx) | Protects |
|------------|------------------|----------|--------------------|----------|
| CTL-AD-BASELINE | Hardened AD deploy + Sysmon / WEF baseline | PR.AC, DE.CM | A.5.15, A.8.2 | AST-001–003 |
| CTL-ADCS-MONITOR | ADCS deploy awareness + ESC detection engineering | DE.AE, DE.CM | A.8.9 | AST-034 |
| CTL-TRUST-REVIEW | Forest trust / SID filter review | ID.AM, PR.AC | A.5.14 | AST-003 |
| CTL-HOST-HARDEN | Member server baseline (vuln intentional in lab only) | PR.PT | A.8.9 | AST-004–005 |
| CTL-SQL-CONTROLS | SQL auth mode / least privilege (lab documents abuse paths) | PR.AC | A.8.3 | AST-033 |
| CTL-SCCM-REVIEW | SCCM site CAD attack-surface review | ID.RA, DE.CM | A.8.9 | AST-005 |
| CTL-LINUX-HARDEN | linux01 AD-join + auditd / Sysmon-for-Linux plans | PR.PT | A.8.9 | AST-006 |
| CTL-EDR-MDE | MDE / Elastic Agent on ws01 | DE.CM, PR.PT | A.8.16 | AST-007 |
| CTL-SIEM-IDENTITY | Elastic rules for Kerberos / LDAP / DCSync patterns | DE.AE | A.8.15 | Identity plane |
| CTL-SIEM-ENDPOINT | Endpoint process / PowerShell telemetry | DE.CM | A.8.15 | Members / ws01 |
| CTL-SIEM-AVAIL | Fleet + ILM + capacity for elk | RC.RP | A.8.13 | AST-010 |
| CTL-ACCESS-SIEM | Restricted Kibana / API access | PR.AC | A.5.15 | AST-010–031 |
| CTL-DETECTION-RULES | Suricata / Zeek / cadre-* rules on monitor | DE.AE | A.8.16 | AST-012 |
| CTL-NSM | Promiscuous capture + Arkime | DE.CM | A.8.16 | AST-012 |
| CTL-VR-ACCESS | Velociraptor ACL + TLS | PR.AC | A.5.15 | AST-011–032 |
| CTL-COC | Case CoC procedures + DFIR-Nexus audit chain | PR.IP | A.5.33 | AST-030–032 |
| CTL-EVIDENCE-ACCESS | Least privilege to evidence stores | PR.AC | A.5.15 | AST-030 |
| CTL-HITL | Examiner password / DRAFT findings (DFIR-Nexus) | PR.IP | A.5.37 | AST-030 |
| CTL-ENTRA-PIM | PIM / RBAC on Azure / Entra lab | PR.AC | A.5.15 | AST-020–021 |
| CTL-CLOUD-MONITOR | Graph / cloud log ingest to Elastic | DE.CM | A.8.15 | Cloud plane |
| CTL-CLOUD-SYNC-REVIEW | Cloud Sync agent monitoring on dc01 | DE.CM | A.8.9 | AST-022 |
| CTL-ANSIBLE-ACCESS | Provisioning SSH / vault discipline | PR.AC | A.8.9 | AST-013 |
| CTL-CHANGE-MGMT | Playbook PR / verify-only cadence | PR.IP | A.5.37 | Estate |
| CTL-LAB-ISOLATION | DarkAI 172.20/Eva7ion 78.x isolation rules | PR.PT | A.8.22 | AST-035 |
| CTL-PRAXIS-SCAN | Praxis CI / SARIF on lab apps | DE.CM | A.8.25 | AST-035 / SDLC |
| CTL-YARA-SIGMA | RevAI / detection rule generation | DE.AE | A.8.16 | Malware analysis |
| CTL-SANDBOX | Speakeasy / detonation in RevAI path | PR.PT | A.8.7 | Analysis VMs |

---

## Coverage notes

- Lab intentionally **deploys vulnerable AD surfaces** for training — document as accepted training risk on non-client networks; never present as production control failure without context.
- Controls marked “lab documents abuse paths” are **detective / educational** until hardened-variant track is enabled.

---

*R2-S1.7 — 2026-07-12*
