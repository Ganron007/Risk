# Cadre Corp — Enterprise Context

> **Sprint 1:** R2-S1.1  
> **Source of truth for hosts:** `CADRE/docs/architecture.md` (lab topology).  
> **Fiction note:** Company profile (revenue, headcount, clients) is a teaching scenario for CISSP Domain 1–2 practice. Technical assets map to the real CADRE lab.

---

## Company profile

| Attribute | Value |
|-----------|-------|
| **Name** | Cadre Corp |
| **Industry** | Digital Forensics & Incident Response (DFIR) services |
| **Revenue** | $12M ARR (mid-size, illustrative) |
| **Employees** | 45 (15 DFIR analysts, 10 SOC, 5 R&D, 10 GRC/audit, 5 leadership) |
| **Customers** | 120 enterprise clients under DFIR retainers |
| **Regulatory** | SOC 2 Type II (contractual), GDPR (EU client evidence), ISO 27001 (in progress) |
| **Risk posture** | Low appetite for client-evidence compromise — see [`risk-appetite-statement.md`](risk-appetite-statement.md) |
| **On-prem forests** | `cadre.local` (root) + `child.cadre.local` + forest trust to `range.local` |

Cadre Corp’s product is **trust**: clients hand over disks, memory, and privileged data. A single chain-of-custody or evidence-breach event threatens retainers and SOC 2 attestation.

---

## Network context (lab = estate)

All on-prem lab assets live on VMware host-only `192.168.77.0/24` (vmnet2), isolated from production home/office networks. Research labs (DarkAI) use Docker `172.20.0.0/24` and must stay isolated from client evidence stores.

### Trust topology (risk-relevant)

```text
cadre.local ◄── parent-child ──► child.cadre.local
     │
     └── bidirectional forest trust ──► range.local
```

Cross-forest trust and ADCS/SCCM attack surfaces on the estate are primary **identity and privilege** risk drivers. See the baseline risk register for scored items.

---

## Asset inventory (summary)

Full machine-readable list: [`../config/asset-inventory.csv`](../config/asset-inventory.csv).

| Class | Asset IDs | Examples |
|-------|-----------|----------|
| Windows AD / members | AST-001–007 | dc01–03, mbr01–02, linux01, ws01 |
| SOC / monitoring | AST-010–013 | elk, vr, monitor, provisioning |
| Cloud plane | AST-020–023 | Entra ID, Azure, Cloud Sync, Arc |
| Data & apps | AST-030–035 | Client evidence, SIEM indices, VR artifacts, MSSQL, ADCS, DarkAI lab |

### Classification scheme

| Label | Meaning | Examples |
|-------|---------|----------|
| **Restricted** | Client legal / PKI / identity plane — breach is existential | AST-001–003, AST-030, AST-032, AST-034, AST-020 |
| **Confidential** | Business ops / telemetry / member servers | AST-004–006, AST-011–012, AST-031, AST-033 |
| **Internal** | Lab / workstation / deploy tooling | AST-007, AST-013, AST-035 |

---

## Risk ownership (RACI-style roles)

| Role | Unit | Owns |
|------|------|------|
| CEO | Leadership | Final risk acceptance (board) |
| CISO | GRC / Audit | Risk register, treatment decisions |
| DFIR Lead | Operations | Client forensic data, IR, CoC |
| SOC Lead | Operations | Detection gaps, SIEM/NSM coverage |
| Infra Lead | Infrastructure | AD, PKI, cloud sync, Ansible |
| Cloud security lead | Cloud | Entra / Azure / Arc |
| R&D Lead | Engineering | DarkAI, RevAI, Praxis research risk |
| App team | Engineering | MSSQL / IIS / member apps |
| SOC manager | Operations | Analyst workstation (ws01) |

---

## How this feeds Sprint 1 artifacts

| Artifact | Uses this doc for |
|----------|-------------------|
| [`risk-appetite-statement.md`](risk-appetite-statement.md) | Board language |
| [`regulatory-obligations.md`](regulatory-obligations.md) | Framework drivers |
| [`risk-register-baseline.md`](risk-register-baseline.md) | AST-* linkage |
| [`control-register.md`](control-register.md) | Capability → framework map |
| CISSP R-EX-001–010 | Scenario grounding |

---

*R2-S1.1 — 2026-07-12*
