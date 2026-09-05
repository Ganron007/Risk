# R-EX-056 — Software-defined networking (SDN) security

**CISSP Reference:** Chapter 11, Section "Secure Network Components"; Chapter 9, Section "Virtualization Security"  
**Exam Objective:** 4.1.2 Secure network components; 3.3.1 Apply secure design principles  
**Study Guide Key Terms:** SDN, network virtualization, control plane, data plane, NFV, micro-segmentation, overlay networks, SD-WAN  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), lab network topology

---

## Scenario Context

Cadre Corp's lab runs entirely on VMware virtual networking — all VMs connect to `vmnet2`, a virtual switch managed by VMware Workstation on the Windows host. The CISO has proposed migrating the lab to a more advanced virtual networking setup using VMware NSX or similar SDN technology to enable micro-segmentation and dynamic security policies.

The infrastructure team is skeptical: "Our VMs can already talk to each other. What problem does SDN solve that VLANs don't?" The CISO counters: "The problem where we can't enforce security policy between VMs on the same subnet without configuring every VM individually — and every time we add a VM, we forget to configure it."

---

## Multiple-Choice Questions

**Question 1:** What is the fundamental architectural difference between traditional networking and SDN?

A. SDN uses faster hardware than traditional networking  
B. SDN separates the control plane (decisions about where traffic goes) from the data plane (actual packet forwarding), enabling centralized, programmable network policy  
C. SDN eliminates the need for IP addresses  
D. SDN uses only wireless connections

**Question 2:** In an SDN environment, what security advantage does micro-segmentation provide over traditional VLANs?

A. Micro-segmentation uses a different encryption algorithm  
B. Micro-segmentation can enforce security policy at the individual workload level (per-VM, per-container), not just at the subnet/VLAN level — policies follow the workload regardless of IP or location  
C. Micro-segmentation eliminates the need for firewalls  
D. Micro-segmentation is always cheaper than VLANs

**Question 3:** What is the PRIMARY security risk of SDN's centralized controller architecture?

A. The controller uses too much CPU  
B. The SDN controller becomes a single point of compromise — if an attacker controls the controller, they can reprogram the entire network's forwarding behavior  
C. SDN controllers cannot be patched  
D. SDN controllers require physical access to manage

**Question 4:** For Cadre Corp's lab (VMware + Ansible), which SDN security principle is most immediately implementable without new hardware?

A. Full NSX deployment with distributed firewalls  
B. Policy-as-code — define network security rules in Ansible, apply consistently across all VMs, version-control the policies, and validate compliance automatically  
C. Replace all virtual switches with physical ones  
D. Deploy a separate SDN controller appliance

---

## Answer Explanations

**Answer 1: B**  
SDN's defining characteristic is **control plane / data plane separation**. In traditional networking, each switch/router makes its own forwarding decisions (distributed control plane). In SDN, a centralized controller makes decisions and programs the data plane devices. This enables network-wide policy, dynamic reconfiguration, and automation that's impossible with traditional distributed control. It doesn't eliminate IP (C) or use only wireless (D).

**Answer 2: B**  
**Workload-level policy enforcement** is the key advantage. Traditional VLANs segment at Layer 2 — all VMs in the same VLAN can talk to each other. Micro-segmentation applies policy per-VM: "DC01 can talk to DC02 on port 135, but ws01 cannot talk to DC01 at all" — even if all three are on the same subnet. This is granularity that VLANs can't achieve without unsustainable rule complexity.

**Answer 3: B**  
The **centralized controller is a single point of compromise**. If an attacker gains control of the SDN controller, they can redirect traffic, create mirror ports for eavesdropping, disable security policies, or isolate targets. This is why SDN controller security (strong authentication, API security, audit logging, high availability) is critical. It's the "keys to the kingdom" for the entire network.

**Answer 4: B**  
**Policy-as-code via Ansible** is the most practical first step. Cadre Corp already uses Ansible for VM configuration. Adding network security policy (firewall rules, service allowlists) to the same Ansible playbooks provides: version control, automated deployment, consistency across VMs, and audit trail — the core SDN value proposition, using existing tools.

---

## Cadre Corp Application

1. **Ansible as Poor Man's SDN Controller:** Until NSX or similar is deployed, treat Ansible as the network policy controller. Define per-VM ingress/egress rules in playbooks. Run compliance checks that validate actual firewall rules against the Ansible-defined policy. Flag drift.

2. **SDN Controller Hardening:** If an SDN controller is deployed in the future: (a) dedicated management network, (b) strong authentication (certificate-based, not passwords), (c) API rate limiting, (d) audit logging of all policy changes, (e) redundant controllers for high availability.

3. **Lab SDN Exercise:** Use VMware's virtual distributed switch (available in Workstation Pro) to experiment with per-VM security policies. Document which CADRE VMs should talk to which other VMs and on which ports — this becomes the micro-segmentation policy baseline.

---

## Interview Talking Points

1. **SDN = Programmable Security:** "Traditional networks are configured box by box, rule by rule. SDN lets me say 'no VM in the Internal zone can initiate connections to the Restricted zone' — and have that enforced everywhere, automatically. That's not a network upgrade — it's a security transformation."

2. **Controller Security Is Existential:** "The SDN controller is the most powerful device on your network. Compromise it, and you can reroute traffic, disable security, or isolate targets for attack. Controller security is priority zero — before any fancy micro-segmentation policies."

3. **Start With Policy-as-Code:** "You don't need NSX to start thinking like SDN. Define your network security rules in Ansible, apply them consistently, version control them. When you eventually adopt SDN, your policy is already defined — you just change the enforcement mechanism."
