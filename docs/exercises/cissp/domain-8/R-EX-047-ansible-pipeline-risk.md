# R-EX-047 — Infrastructure as Code security: Ansible pipeline risk

**CISSP Reference:** Chapter 20, Section "Systems Development Controls"; Chapter 16, Section "Configuration Management"; Chapter 8, Section "Security Capabilities of Information Systems"  
**Exam Objective:** 8.1.2 Integrate security into SDLC (IaC); 8.2.2 Test software security (IaC scanning); 7.1.2 Implement configuration management  
**Study Guide Key Terms:** Infrastructure as Code (IaC), Ansible security, pipeline security, immutable infrastructure, secret management, signed roles, configuration drift  
**Inputs:** [`../risk-register-baseline.md`](../risk-register-baseline.md), RISK-015, AST-013 (provisioning)

---

## Scenario Context

Cadre Corp's entire lab infrastructure — 7 Windows VMs, 4 Linux VMs, domain controllers, SOC stack — is deployed and managed via Ansible playbooks from the provisioning server (AST-013). The Ansible vault contains: domain admin credentials, service account passwords, API keys, TLS private keys, and Velociraptor client configurations.

RISK-015 rates "Ansible/provisioning credential misuse" as score 6 (High). Three specific concerns keep the CISO awake:

1. **Compromised provisioning host:** If AST-013 is compromised, the attacker can run Ansible playbooks against every VM in the estate — mass configuration change, credential rotation, backdoor deployment, or complete destruction.

2. **Malicious Ansible role:** Cadre Corp uses community Ansible roles from Galaxy. A compromised or malicious role could include backdoors — and Ansible runs as root/SYSTEM on target hosts.

3. **Vault secret sprawl:** The vault password is stored in a plaintext file on AST-013 and shared among three infrastructure team members via a Teams chat called "Admin Crew" (see R-EX-064). Anyone with vault access has every credential in the estate.

---

## Multiple-Choice Questions

**Question 1:** A compromised provisioning host (AST-013) represents what class of risk?

A. A minor operational inconvenience — VMs can be reconfigured manually  
B. A single point of infrastructure compromise — the provisioning host holds credentials and playbook authority over every system in the estate; its compromise is equivalent to compromising every system simultaneously  
C. Only the provisioning host itself is at risk — other VMs are unaffected  
D. Ansible playbooks are read-only and can't cause harm

**Question 2:** Community Ansible roles from Galaxy introduce what supply-chain risk?

A. No risk — community roles are always reviewed and safe  
B. Malicious code in a role can execute arbitrary commands on every target host during playbook execution — a poisoned role could deploy backdoors, exfiltrate credentials, or create persistent access across the entire estate  
C. Community roles can only affect the provisioning host  
D. Ansible Galaxy automatically scans all roles for malware

**Question 3:** What is the most effective control against malicious or vulnerable Ansible roles?

A. Download and run roles directly from Galaxy without review  
B. Pin roles to specific versions by commit hash, review role contents before first use, store approved roles in an internal repository (not pulled live from Galaxy), and use `ansible-lint` + custom policies to detect dangerous patterns  
C. Only use roles that have more than 1,000 downloads  
D. Disable all community roles — write everything from scratch

**Question 4:** The Ansible vault password shared via Teams chat violates what fundamental security principle?

A. Password complexity requirements  
B. Secret management — credentials should never be shared via general-purpose communication tools; the vault password should be stored in a secrets manager with access control, audit logging, and rotation capability  
C. Team collaboration policies  
D. Ansible doesn't support vault passwords

---

## Answer Explanations

**Answer 1: B**  
AST-013 is a **single point of infrastructure compromise** — it's the "keys to the kingdom." Ansible playbooks run with administrative privileges on every target host. An attacker who controls the provisioning server can: (a) deploy backdoors to all VMs, (b) extract all credentials from the vault, (c) modify firewall rules, disable security controls, or create new admin accounts, (d) destroy the entire lab with a single playbook run. This is why AST-013 should be classified Restricted (per R-EX-016) — its compromise impact is existential.

**Answer 2: B**  
Ansible roles execute arbitrary code on target hosts with the privileges of the Ansible user (typically root/SYSTEM). A malicious role could: (a) create backdoor user accounts, (b) deploy persistent malware, (c) exfiltrate credentials and data, (d) modify security configurations to weaken defenses, (e) establish C2 channels. This is a software supply-chain attack vector identical in principle to a malicious npm package or poisoned Docker image — except the blast radius is your entire infrastructure.

**Answer 3: B**  
**Version pinning + review + internal repository** is the defense-in-depth approach: (a) pin by commit hash (not tag — tags can be moved), (b) review role contents before first use (read the code — it's YAML and Python, not opaque binaries), (c) store approved versions in an internal repository (not pulled live from Galaxy on each run), (d) scan roles with `ansible-lint` and custom policies. Writing everything from scratch (D) eliminates the supply-chain risk but sacrifices the efficiency of community roles — a risk-based decision, not a default.

**Answer 4: B**  
Sharing secrets via Teams chat is a **secret management failure**. The vault password should be: (a) stored in a dedicated secrets manager (Azure Key Vault, HashiCorp Vault, or at minimum a GPG-encrypted file with access control), (b) accessed only by the Ansible service account (not individual users), (c) rotated periodically with an audit trail of who accessed it, (d) never transmitted via chat, email, or other general-purpose communication tools. A Teams chat message persists indefinitely, is visible to anyone with access to the chat, and may be exported or compromised.

---

## Cadre Corp Application

1. **Provisioning Host Hardening:** (a) Classify AST-013 as Restricted, (b) restrict access to named admin accounts only (no shared accounts), (c) enable full audit logging of all commands executed, (d) implement network isolation — provisioning host only connects to target VMs on specific management ports, no internet access.

2. **Ansible Role Governance:** (a) Pin all Galaxy roles to commit hashes in `requirements.yml`, (b) review new roles before adoption, (c) store approved roles in an internal git repository, (d) run `ansible-lint` in CI for every playbook change.

3. **Vault Secret Management:** (a) Move vault password to a secrets manager, (b) Ansible service account accesses vault via automated credential retrieval (no human knows the password), (c) rotate vault password quarterly, (d) audit vault access monthly.

---

## Interview Talking Points

1. **Your Provisioning Server Is Your Most Critical Asset:** "If an attacker compromises your Ansible server, they don't need to hack your domain controllers — they can just tell Ansible to create a Domain Admin account for them. The provisioning server is the single most powerful system in your infrastructure, and it should be protected accordingly."

2. **Community Roles Are Supply-Chain Dependencies:** "Every Ansible Galaxy role you use is code running as root on your production systems. Treat them like you'd treat a random npm package with network access: review before use, pin to a hash, store internally. 'Popular' doesn't mean 'safe.'"

3. **Secrets in Chat Are Not Secrets:** "If your Ansible vault password is in a Teams chat called 'Admin Crew,' it's not a secret — it's a memo. Every person in that chat, every person added later, every person who gains access to the chat history — they all have the vault password. Secrets belong in secrets managers, not chat messages."
