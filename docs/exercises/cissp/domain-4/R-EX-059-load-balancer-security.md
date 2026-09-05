# R-EX-059 — Load balancer security considerations

**CISSP Reference:** Chapter 12, Section "Load Balancing Security"; Chapter 11, Section "Secure Network Components"  
**Exam Objective:** 4.1.2 Secure network components; 4.1.1 Implement secure network architecture  
**Study Guide Key Terms:** Load balancer, TLS termination, SSL offloading, DDoS mitigation, health checks, session persistence, reverse proxy  
**Inputs:** Cadre Corp lab infrastructure

---

## Scenario Context

Cadre Corp is deploying a cluster of three web servers behind a load balancer to serve the client threat intelligence portal. The architecture team is debating two configurations:

**Config A (TLS termination at LB):** The load balancer decrypts HTTPS, inspects traffic, then forwards unencrypted HTTP to backend servers. The team argues: "We can inspect traffic for attacks at the LB."

**Config B (TLS pass-through):** The load balancer forwards encrypted traffic to backends without decryption. The team argues: "End-to-end encryption — no cleartext anywhere."

Both teams have valid points. The CISO asks you to evaluate the security implications of TLS termination at the load balancer versus TLS pass-through, considering that the portal handles client forensic data.

---

## Multiple-Choice Questions

**Question 1:** TLS termination at the load balancer introduces what PRIMARY security risk?

A. It slows down the load balancer's performance  
B. The traffic between the load balancer and backend servers is unencrypted — anyone with access to that network segment can intercept client data in cleartext  
C. The load balancer cannot handle TLS certificates  
D. TLS termination is incompatible with HTTP/2

**Question 2:** What is the security BENEFIT of TLS termination at the load balancer?

A. It eliminates the need for any encryption  
B. The load balancer can inspect decrypted traffic for attacks (SQL injection, XSS, malicious payloads) before forwarding to backends — acting as a Web Application Firewall (WAF) inspection point  
C. It makes the backends run faster by eliminating all security processing  
D. It replaces the need for backend server authentication

**Question 3:** A load balancer's health check monitors backend servers. What is the security implication of a misconfigured health check?

A. Health checks have no security implications  
B. An overly permissive health check endpoint (e.g., `/status` returning internal IPs, software versions, or configuration details) can leak sensitive information to anyone who discovers the endpoint  
C. Health checks always require administrative credentials  
D. Health checks are encrypted by default

**Question 4:** Which load balancer configuration provides the best balance of security inspection and data protection for Cadre Corp's client portal?

A. TLS termination at LB only (Config A)  
B. TLS pass-through only (Config B)  
C. TLS termination at LB with WAF inspection, then re-encryption to backends (TLS from LB to backend) — providing both traffic inspection AND end-to-end encryption  
D. No load balancer — use a single server for simplicity

---

## Answer Explanations

**Answer 1: B**  
When TLS is terminated at the LB, traffic to backends is **unencrypted HTTP**. On Cadre Corp's flat lab network (`192.168.77.0/24`), any compromised VM on the same subnet can sniff this traffic — including client forensic data, session tokens, and credentials. This is a lateral movement goldmine. The risk is specifically the cleartext segment between LB and backends.

**Answer 2: B**  
TLS termination enables **traffic inspection**. The load balancer (or an integrated WAF) can examine the decrypted HTTP payload for SQL injection, XSS, command injection, and other application-layer attacks. Without termination, the LB only sees encrypted blobs and cannot inspect content. This is the valid argument for Config A.

**Answer 3: B**  
Health check endpoints that return **diagnostic information** (server version, internal IPs, database connection strings, build dates) are information leakage vulnerabilities. An attacker who discovers the health check URL (often `/health`, `/status`, `/ping`) can fingerprint backend infrastructure. Health checks should return minimal information (HTTP 200 + "OK"), not diagnostic details.

**Answer 4: C**  
**TLS termination + inspection + re-encryption** provides the best of both: the LB decrypts, inspects traffic for attacks (WAF), then re-encrypts to backends. Traffic is never in cleartext on the wire — the only cleartext exists momentarily in the LB's memory. This is the standard for handling sensitive data in modern architectures. It requires the LB to have a valid certificate for backend communication.

---

## Cadre Corp Application

1. **For Client Portal:** Use Config C (TLS termination + re-encryption). The load balancer holds the public-facing certificate; internal traffic uses a separate internal CA-issued certificate from ADCS. This provides WAF inspection AND end-to-end encryption on the wire.

2. **Health Check Hardening:** All health check endpoints must return HTTP 200 with body "OK" only — no version numbers, no configuration details, no internal IPs. Add health check endpoints to the penetration testing scope.

3. **DDoS Consideration:** Load balancers are the first line of defense against volumetric DDoS. Configure connection rate limiting, SYN cookie protection, and geographic IP filtering if appropriate.

---

## Interview Talking Points

1. **TLS Termination = Trust Boundary:** "When you decrypt at the load balancer, the LB-to-backend path becomes a trust boundary. On a flat network, that's a cleartext highway for anyone who compromises a single VM. Either encrypt LB-to-backend, or treat that network segment like it's public."

2. **Inspect AND Encrypt — Not OR:** "The false choice is 'inspect OR encrypt.' Modern architectures do both: terminate, inspect, re-encrypt. The only cleartext exists in protected memory, not on the wire. That's how you get security visibility without sacrificing data protection."
