# R-EX-053 — Firewall rule design and review

**CISSP Reference:** Chapter 11, Section "Secure Network Components"; Chapter 12, Section "Network Attack Prevention"  
**Exam Objective:** 4.1.2 Secure network components  
**Study Guide Key Terms:** Stateful firewall, stateless firewall, next-gen firewall (NGFW), implicit deny, rule shadowing, rule base optimization, ingress/egress filtering  
**Inputs:** Cadre Corp lab network topology, `13-net-monitor.yml`

---

## Scenario Context

Cadre Corp's SOC Lead is reviewing the lab's Windows Defender Firewall rules after discovering that:

1. The firewall on DC01 has a rule allowing "All Traffic" from subnet `192.168.77.0/24` — written during initial deployment "to make sure everything works."
2. The rule base has 47 rules accumulated over two years with no documentation about which rules are still needed.
3. Rules are ordered by creation date, not by security priority — a permissive rule added last month overrides a restrictive rule from last year.
4. There is no egress filtering — any compromised VM can initiate outbound connections to any destination on any port.

The CISO has asked: "If I asked you to justify every firewall rule on DC01 right now, could you? And if not, how do we fix this?"

---

## Multiple-Choice Questions

**Question 1:** The "Allow All Traffic from 192.168.77.0/24" rule on DC01 violates which firewall design principle?

A. Stateful inspection — the rule doesn't track connection state  
B. Least privilege — the rule allows all traffic from the entire subnet when DC01 only needs specific ports (Kerberos 88, LDAP 389, SMB 445, RPC 135) from specific sources  
C. Rule shadowing — the rule shadows more specific rules  
D. Implicit deny — the rule doesn't end with a deny statement

**Question 2:** During a firewall rule base review, what should be done with a rule that no one can explain or justify?

A. Keep it — it might be important  
B. Disable it in monitoring-only mode (log but don't block) for 30 days; if no legitimate traffic matches, remove it permanently  
C. Delete it immediately — unexplained rules are security risks  
D. Add a comment saying "purpose unknown"

**Question 3:** What is the correct default (implicit) rule at the END of every firewall rule base?

A. Allow all outbound traffic  
B. Deny all traffic that hasn't been explicitly allowed  
C. Log and allow all unmatched traffic  
D. Forward unmatched traffic to a DMZ

**Question 4:** Egress filtering (controlling outbound traffic from internal hosts) is important because:

A. It improves internet browsing speed  
B. It prevents compromised hosts from exfiltrating data via unauthorized protocols, connecting to C2 servers, or probing external targets  
C. It's required for firewall vendor certification  
D. It replaces the need for inbound filtering

---

## Answer Explanations

**Answer 1: B**  
The rule violates **least privilege**. DC01 needs a handful of specific ports for domain services — not "all traffic from everyone on the subnet." The permissive rule was a deployment convenience that became a permanent security gap. Least privilege in firewall design means: define the minimum necessary traffic, allow only that, deny everything else.

**Answer 2: B**  
The safe approach is **disable-and-monitor**. Delete an unexplained rule immediately (C) could break production. Keep it blindly (A) accumulates security debt. The correct process: disable the rule, enable logging for matching traffic, observe for 30 days. If no legitimate traffic matches, remove. If traffic matches, investigate and document the business justification before re-enabling.

**Answer 3: B**  
Every firewall rule base must end with an **implicit deny**: any traffic not explicitly allowed by a previous rule is denied. This is the foundational principle of firewall security. "Allow all outbound" (A) is a common but dangerous default. "Log and allow" (C) defeats the purpose. Forwarding to DMZ (D) is not an implicit deny.

**Answer 4: B**  
Egress filtering prevents **post-compromise data exfiltration and C2 communication**. If an attacker compromises ws01, they'll try to connect out to their C2 server, exfiltrate data via DNS tunneling, or probe the internet for additional targets. Egress filtering blocks these outbound attempts. It's a critical layer of defense-in-depth that many organizations neglect because they focus only on inbound threats.

---

## Cadre Corp Application

1. **DC01 Rule Cleanup:** Replace the "Allow All /24" rule with specific port-based rules: Kerberos (88), LDAP (389), LDAPS (636), SMB (445), RPC (135), DNS (53), Global Catalog (3268/3269). Restrict source to domain members and provisioning server only.

2. **Rule Review Cadence:** Add a quarterly firewall rule review to the SOC calendar. Each review: (a) disable unexplained rules in monitor mode, (b) document surviving rules, (c) remove stale rules after 30-day monitor period.

3. **Egress Filtering Deployment:** Deploy egress rules on all Windows VMs via Ansible: deny outbound to internet except for approved services (Windows Update, DNS forwarding). For SOC VMs, explicitly allow log shipping destinations. For DCs, deny all direct internet access.

4. **Ansible as Rule Source of Truth:** Store all firewall rules in Ansible playbooks (not manually configured on VMs). This ensures rules are version-controlled, documented, and reproducible.

---

## Interview Talking Points

1. **"Temporary" Rules Are Permanent Risk:** "Every 'allow all for now' rule written during deployment is still there two years later. Temporary firewall rules are a lie we tell ourselves. If you can't deploy securely from day one, at least put an expiration date on the rule."

2. **Unexplained Rules = Security Debt:** "If nobody can explain what a firewall rule does, it's not a control — it's a potential backdoor. Disable, monitor, document, or delete. Unexplained rules accumulate until one of them is the path the attacker uses."

3. **Ingress + Egress = Complete:** "Most teams obsess over inbound rules and forget outbound. But an attacker inside your network needs to phone home. Egress filtering is your last chance to catch exfiltration before data leaves the building."
