# CISO-EX-003 — Control library mapping

**Platform:** CISO Assistant Community Edition  
**Time:** 25 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 2 (Asset Security)  
**Prerequisites:** CISO-EX-001, CISO-EX-002 completed

---

## Objective

Map Cadre Corp's control register (`docs/control-register.md`) into CISO Assistant's control library, linking each control to the risks it mitigates and the frameworks it satisfies. This demonstrates the ability to build and maintain a control library — foundational for ISO 27001 Statement of Applicability and SOC 2 audit preparation.

---

## Steps

### Step 1 — Create the Cadre Corp control library
1. Navigate to **Controls** → **Create Control**.
2. Create each control from the register:

| Control ID | Name | Description | Risk(s) Mitigated | Framework Mapping |
|------------|------|-------------|-------------------|-------------------|
| CTL-SIEM-IDENTITY | SIEM detection for identity attacks | Deploy Elastic detection rules for 4662/DRSUAPI (DCSync), 4769 RC4 (Kerberoast), and cross-forest Kerberos anomalies | RISK-001, RISK-003, RISK-006 | ISO 27001 A.12.6.1, NIST DE.AE |
| CTL-EVIDENCE-ACCESS | Evidence access controls | Restricted share with RBAC, access logging, HITL approval for all evidence access, write blocker requirement for acquisitions | RISK-007, RISK-008 | ISO 27001 A.9.4.1, SOC 2 CC6.1 |
| CTL-HITL | Human-in-the-loop approval | All security findings stage as DRAFT; human examiner approves with cryptographic password before operational use | RISK-018, RISK-007 | ISO 27001 A.9.4.2, SOC 2 CC5.2 |
| CTL-COC | Chain of custody | SHA-256 hash at acquisition, documented custody transfers, dual-verification for critical evidence, DFIR-Nexus audit chain | RISK-007, RISK-018 | ISO 27001 A.12.4.2, SOC 2 CC6.3 |
| CTL-LAB-ISOLATION | Research lab isolation | DarkAI/RevAI labs on isolated Docker networks, no route to production or client evidence, egress filtering | RISK-012, RISK-013, RISK-014 | ISO 27001 A.13.1.3, NIST PR.AC-5 |
| CTL-PRAXIS-SCAN | Praxis CI security gate | Automated SAST + secret detection in CI pipeline, Critical/High findings block merge, SARIF evidence archived | RISK-013 | ISO 27001 A.14.2.8, NIST DE.CM-4 |
| CTL-TRUST-REVIEW | Forest trust quarterly review | Verify SID filtering enabled, selective authentication enforced, trust direction justified, inter-realm Kerberos monitoring active | RISK-003 | ISO 27001 A.13.1.1, NIST PR.AC-3 |
| CTL-ADCS-MONITOR | ADCS certificate issuance monitoring | Monitor Event ID 4886/4887 for anomalous certificate requests, template modifications, and enrollment agent abuse | RISK-002 | ISO 27001 A.12.4.1, NIST DE.CM-3 |

### Step 2 — Link controls to risks
For each control, navigate to the risk scenario and associate the mitigating control. Example: CTL-SIEM-IDENTITY → RISK-001 (DCSync).

### Step 3 — Verify framework coverage
1. Navigate to **Compliance** or framework view.
2. Confirm controls are mapped to ISO 27001 Annex A references and NIST CSF functions.
3. Identify gaps: which Annex A controls have no Cadre Corp controls mapped?

---

## Verification Checklist

- [ ] 8 controls created with descriptions, risk associations, and framework mappings
- [ ] Each RISK-001 through RISK-018 has at least one mitigating control linked
- [ ] Framework gap analysis identifies uncovered Annex A controls

---

## CISSP Connection

**Domain 1:** Control mapping to multiple frameworks (ISO 27001, NIST CSF, SOC 2) is a core CISSP governance competency. The Statement of Applicability (SoA) for ISO 27001 requires exactly this mapping.

**Domain 2:** Controls on evidence handling (CTL-COC, CTL-EVIDENCE-ACCESS) directly implement the asset security principles of classification-based handling and data lifecycle protection.

---

## Interview Talking Points

1. **"Controls bridge the gap between risks and frameworks":** "A risk register without controls is a list of problems. A control library without framework mapping is a list of solutions with no compliance proof. I built both — every control mitigates specific risks AND maps to specific framework requirements. The auditor asks 'how do you control DCSync risk?' and I point to CTL-SIEM-IDENTITY → Annex A.12.6.1 → validated detection rules."

2. **"Framework mapping is continuous, not one-time":** "As we add controls or frameworks change, I update the mapping. The SOC 2 audit next quarter will test controls that are mapped, documented, and evidenced — not theoretical."
