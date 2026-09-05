# R-EX-055 — Wireless security (WPA3, enterprise vs personal)

**CISSP Reference:** Chapter 11, Section "Wireless Networks"; Chapter 12, Section "Secure Communications"  
**Exam Objective:** 4.1.3 Implement secure wireless architecture  
**Study Guide Key Terms:** WPA3, WPA2, WPA3-Enterprise, WPA3-Personal, SAE (Simultaneous Authentication of Equals), 802.1X, EAP-TLS, PMF, OWE  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md)

---

## Scenario Context

Cadre Corp's office Wi-Fi runs WPA2-PSK (Pre-Shared Key) with a single passphrase shared by all 45 employees and posted on the breakroom whiteboard "for visitors." During a recent penetration test, the tester:

1. Captured the WPA2 4-way handshake from the parking lot.
2. Cracked the passphrase in 4 minutes using a wordlist attack (the passphrase was "CadreCorp2024!").
3. Joined the corporate Wi-Fi and accessed the internal network, including DC01.

The penetration tester noted: "WPA2-PSK with a shared passphrase is security theater in 2026." The CISO has asked you to recommend a wireless security upgrade.

---

## Multiple-Choice Questions

**Question 1:** What is the fundamental security weakness of WPA2-PSK (Pre-Shared Key) compared to WPA3-Enterprise?

A. WPA2-PSK uses weaker encryption (AES-128 vs WPA3's AES-256)  
B. WPA2-PSK uses a shared passphrase — anyone with the passphrase can derive the Pairwise Master Key (PMK) and decrypt all users' traffic; WPA3-Enterprise uses per-user authentication via 802.1X  
C. WPA2-PSK has slower connection speeds  
D. WPA2-PSK doesn't support 5 GHz channels

**Question 2:** WPA3's SAE (Simultaneous Authentication of Equals) replaces WPA2's PSK 4-way handshake. What is the key security improvement?

A. SAE uses a stronger encryption algorithm  
B. SAE is resistant to offline dictionary attacks — each authentication attempt requires an active interaction, preventing passive capture-and-crack attacks  
C. SAE eliminates the need for passwords entirely  
D. SAE supports more simultaneous users

**Question 3:** For Cadre Corp's 45 employees, why is WPA3-Enterprise with 802.1X and EAP-TLS the recommended over WPA3-Personal?

A. It's cheaper to implement  
B. Per-user certificates (from the existing ADCS CA) provide individual authentication, accountability, and the ability to revoke a single user's access without changing a shared password for everyone  
C. It provides faster Wi-Fi speeds  
D. It doesn't require a RADIUS server

**Question 4:** What is OWE (Opportunistic Wireless Encryption) in the context of Wi-Fi security?

A. A feature that only encrypts "opportunistic" connections  
B. Encrypted open Wi-Fi networks — provides encryption for public/open networks without requiring a password, protecting against passive eavesdropping (RFC 8110)  
C. An encryption mode that activates only when attacks are detected  
D. A deprecated WEP replacement

---

## Answer Explanations

**Answer 1: B**  
WPA2-PSK's fundamental weakness is the **shared passphrase model**. Every user shares the same passphrase, which is used to derive the PMK. Anyone who knows the passphrase can capture the 4-way handshake for ANY user, derive their session keys, and decrypt their traffic (or inject frames). WPA3-Enterprise with 802.1X gives each user unique credentials — compromise of one user doesn't expose others. The encryption algorithm (A) is the same (AES-CCMP).

**Answer 2: B**  
SAE (the "Dragonfly" handshake) is **resistant to offline dictionary attacks**. Unlike WPA2's 4-way handshake (which can be captured passively and cracked offline at billions of attempts per second), SAE requires an active interaction for each password guess. This makes brute-force attacks impractical. It doesn't eliminate passwords (C) but makes cracking them dramatically harder.

**Answer 3: B**  
**Per-user certificates via EAP-TLS** provide individual authentication. If an employee leaves Cadre Corp, their certificate is revoked — no need to change the Wi-Fi password and redistribute it to 44 remaining employees. The existing ADCS CA (AST-034) can issue these certificates; a RADIUS server (NPS on Windows Server) is needed but is a standard role.

**Answer 4: B**  
**OWE provides encryption for open networks** without requiring a password. It uses Diffie-Hellman key exchange during association to establish an encrypted link, preventing passive eavesdropping. It doesn't authenticate the network (no protection against evil twin attacks), but it prevents the trivial sniffing that unencrypted open Wi-Fi allows.

---

## Cadre Corp Application

1. **Recommendation:** Deploy WPA3-Enterprise with 802.1X/EAP-TLS. Use the existing ADCS CA to issue computer and user certificates via Group Policy auto-enrollment. Deploy NPS (RADIUS) on a member server. This ties Wi-Fi authentication to domain credentials with per-user accountability.

2. **Guest Network:** For visitors, deploy a separate SSID with WPA3-Personal (unique passphrase, rotated monthly) on a VLAN with internet-only access — no route to internal networks.

3. **OWE for DFIR Lab Open SSID:** If the lab ever offers an open Wi-Fi for test devices, use OWE instead of completely unencrypted open authentication.

4. **Legacy Device Handling:** Some older lab devices may not support WPA3. Configure WPA3-Transition Mode (allows WPA2 devices to connect with PMF required) rather than dropping to WPA2-only.

---

## Interview Talking Points

1. **Shared Passphrases Are Shared Liability:** "A Wi-Fi password that 45 people know is not a secret — it's a memo. WPA2-PSK with a shared passphrase means one person's compromise (or one photo of the breakroom whiteboard) exposes everyone's traffic. Enterprise auth with per-user certificates eliminates this."

2. **SAE Makes Wi-Fi Cracking Impractical:** "WPA2 handshakes can be cracked offline at GPU speed. WPA3's SAE requires live interaction for each guess — millions of guesses per second becomes one guess per round trip. That's the difference between crackable in 4 minutes and crackable in 4 centuries."

3. **You Already Have the PKI for This:** "We invested in ADCS. EAP-TLS for Wi-Fi uses the same certificates our domain controllers already trust. The infrastructure exists — we just need to turn it on for wireless."
