# R-EX-065 — Single sign-on and federation (SAML, OIDC)

**CISSP Reference:** Chapter 14, Section "Authentication Systems Implementation"; Chapter 13, Section "Identity Management"  
**Exam Objective:** 5.1.2 Implement authentication mechanisms; 5.2.1 Implement authorization mechanisms  
**Study Guide Key Terms:** SSO, SAML, OIDC, OAuth 2.0, federation, identity provider (IdP), service provider (SP), Relying Party Trust  

---

## Scenario Context

Cadre Corp's analysts use 8 different tools daily — Elastic, Velociraptor, Arkime, MISP, DFIR-Nexus, CISO Assistant, VerifyWise, and the client portal — each with its own username and password. Analysts cope by reusing passwords across tools, writing passwords in `passwords.txt` on their desktops, or staying perpetually logged in. The SOC Lead estimates 40% of helpdesk tickets are password resets.

The CISO wants to implement SSO using the existing on-prem AD as the identity provider, but also needs to support SAML/OIDC for cloud tools (VerifyWise) and the client-facing portal (which clients authenticate to via their own Entra ID tenants).

---

## Multiple-Choice Questions

**Question 1:** In a SAML federation, what is the role of the Identity Provider (IdP)?

A. It hosts the application the user wants to access  
B. It authenticates the user and issues a signed SAML assertion (token) that the Service Provider trusts, allowing the user to access multiple SPs with one authentication event  
C. It provides internet connectivity to the user  
D. It encrypts all traffic between the user and the application

**Question 2:** What is the PRIMARY difference between SAML and OIDC?

A. SAML uses XML and is heavier; OIDC is built on OAuth 2.0 and uses JSON/JWT — OIDC is generally simpler and preferred for modern web/mobile applications  
B. SAML is for on-prem; OIDC is for cloud only  
C. SAML is more secure than OIDC in all cases  
D. OIDC replaces the need for authentication entirely

**Question 3:** What security risk does SSO introduce that separate credentials per application do not?

A. SSO is always less secure than separate passwords  
B. Single point of authentication failure — if the IdP is compromised or unavailable, ALL connected applications are affected; similarly, if a user's SSO session is hijacked, the attacker gains access to ALL applications  
C. SSO requires more password resets  
D. SSO increases the number of credentials to manage

---

## Answer Explanations

**Answer 1: B**  
The **IdP authenticates the user once** and issues a signed assertion (SAML) or token (OIDC). Service Providers trust the IdP and accept the assertion without re-authenticating the user. This is the "single sign-on" — one authentication at the IdP grants access to multiple SPs. In Cadre Corp's context, AD FS (or Entra ID) would be the IdP; Elastic, VR, etc. would be SPs.

**Answer 2: A**  
SAML uses XML, SOAP, and is more complex with heavier payloads. **OIDC is built on OAuth 2.0, uses JSON Web Tokens (JWT)**, and is REST/API-native — making it simpler for modern web and mobile applications. OIDC is not "cloud only" (B) and SAML is not "always more secure" (C) — both can be configured securely or insecurely.

**Answer 3: B**  
SSO concentrates risk at the IdP. If the IdP is compromised, the attacker has access to everything. If the IdP is down, nobody can log in to anything. Mitigations: (a) high-availability IdP deployment, (b) strong IdP security (MFA, PAM, monitoring), (c) break-glass local accounts for critical systems that bypass SSO in emergencies. The tradeoff is accepted because the security improvement (eliminating password reuse, centralized access control) outweighs the concentration risk when properly mitigated.

---

## Cadre Corp Application

1. **On-Prem SSO with AD FS:** Deploy AD FS on a dedicated member server. Configure Relying Party Trusts for Elastic, Velociraptor, and Arkime. Analysts authenticate once to AD FS → access all SOC tools. Enforce MFA at the IdP level (one MFA protects all applications).

2. **Federation with Client Entra ID:** For the client portal, configure federation with clients' Entra ID tenants. Cadre Corp's portal trusts the client's Entra ID as IdP — clients authenticate with their own corporate credentials. This is B2B federation, not requiring Cadre Corp to manage client identities.

3. **Break-Glass Accounts:** For each critical system (ESXi host, DC local admin, firewall console), maintain a local break-glass account NOT connected to SSO. Password stored in physical safe. Used only when IdP is unavailable.

---

## Interview Talking Points

1. **SSO = Fewer Passwords = Better Security:** "8 tools, 8 passwords means 7 password reuse patterns and 40% of helpdesk time lost to resets. SSO with MFA means one strong authentication protects everything. The IdP concentration risk is real, but the alternative — password chaos — is demonstrably worse."

2. **Federation, Not Account Proliferation:** "When clients need portal access, don't create accounts for them. Federate with THEIR identity provider. They manage their own users; we trust their authentication. That's B2B federation, and it's how the enterprise world works."
