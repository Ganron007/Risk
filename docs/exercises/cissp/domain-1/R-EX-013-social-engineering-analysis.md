# R-EX-013 — Social engineering scenario analysis

**CISSP Reference:** Chapter 2, Section "Social Engineering", Pages 215-238  
**Exam Objective:** 1.3.1 Analyze and differentiate social engineering attacks  
**Study Guide Key Terms:** Social engineering, phishing, pretexting, baiting, tailgating, whaling, vishing, quid pro quo  
**Inputs:** [`../enterprise-context.md`](../enterprise-context.md), [`../risk-register-baseline.md`](../risk-register-baseline.md)

---

## Scenario Context

Cadre Corp's DFIR analysts regularly handle highly sensitive client evidence and have privileged access to domain controllers, forensic data stores, and cloud identity systems. The company's security awareness program has been informal, relying primarily on analyst experience rather than structured training. Recent industry intelligence indicates that DFIR firms are increasingly targeted by sophisticated social engineering campaigns aimed at accessing client evidence for competitive intelligence or extortion.

A junior DFIR analyst receives an email that appears to be from a long-term client, "GlobalTech Enterprises," requesting urgent assistance with a suspected nation-state intrusion. The email contains:
- A convincing client logo and branding
- Specific references to previous engagements
- A sense of urgency ("we need your team onsite within 4 hours")
- An attachment labeled "preliminary_forensic_images.zip" (password: "GlobalTech2024!")
- A request for the analyst to access a shared OneDrive link to upload "additional evidence"

The analyst is preparing to open the attachment and access the OneDrive link when they recall a recent security awareness reminder about social engineering. They pause and escalate the situation to the SOC Lead.

As the Risk Manager, you need to analyze this social engineering attempt, identify the attack vectors, assess the potential impact, and recommend improvements to Cadre Corp's security awareness program.

---

## Multiple-Choice Questions

**Question 1:** Which of the following social engineering techniques is primarily demonstrated in this scenario?

A. Tailgating  
B. Pretexting  
C. Baiting  
D. Quid pro quo

**Question 2:** The email attachment "preliminary_forensic_images.zip" with password "GlobalTech2024!" represents which additional social engineering or attack vector?

A. Whaling  
B. Vishing  
C. Malware delivery via password-protected archive  
D. Business email compromise (BEC)

**Question 3:** If the analyst had opened the attachment and accessed the OneDrive link, which of the following would be the most likely immediate impact to Cadre Corp?

A. Direct compromise of client evidence stored on AST-030  
B. Installation of malware on the analyst's workstation (AST-007)  
C. Immediate domain admin compromise via DCSync  
D. Deletion of SIEM data on AST-010

**Question 4:** Which of the following controls would be most effective in preventing this type of social engineering attack in the future?

A. Implementing DMARC, SPF, and DKIM for email authentication  
B. Requiring all analysts to complete annual security awareness training  
C. Deploying endpoint detection and response (EDR) on all workstations  
D. Isolating analyst workstations from the internet

---

## Answer Explanations

**Answer 1: B**  
Pretexting is the primary technique demonstrated. The attacker created a fabricated scenario (urgent nation-state intrusion from a known client) to manipulate the analyst into taking actions (opening attachments, accessing links). Pretexting involves creating a false scenario or pretext to gain trust and access. While the email could be considered phishing (a broader category), the specific use of a detailed, fabricated scenario with urgency and client context makes pretexting the more precise classification.

**Answer 2: C**  
The password-protected archive represents malware delivery. Attackers often use password-protected archives to bypass email security filters that cannot scan encrypted content. The password provided in the email ("GlobalTech2024!") allows the analyst to decrypt and execute the malware. This technique combines social engineering (trusting the email) with technical malware delivery. While this could be part of a broader business email compromise, the immediate vector is malware delivery via the archive.

**Answer 3: B**  
The most likely immediate impact would be malware installation on the analyst's workstation (AST-007). Social engineering attacks typically start with endpoint compromise through malicious attachments or links. While the attacker's ultimate goal might be client evidence (AST-030) or domain admin access, the immediate impact would be workstation compromise. This could then lead to lateral movement, credential theft, and broader estate compromise, but the workstation is the initial foothold.

**Answer 4: A**  
Implementing DMARC, SPF, and DKIM for email authentication would be most effective in preventing this type of attack. These technical controls help prevent email spoofing by verifying that emails claiming to be from GlobalTech Enterprises actually originate from their legitimate mail servers. While security awareness training (B) is important, technical controls provide more reliable prevention. EDR (C) is a detection/control measure but doesn't prevent the initial delivery. Internet isolation (D) would impact DFIR operations and is not practical for analysts who need internet access for investigations.

---

## Cadre Corp Application

This exercise applies directly to Cadre Corp's security awareness needs by:

1. **DFIR-Specific Threats:** Addressing social engineering attacks that target DFIR firms specifically (client impersonation, evidence theft)
2. **High-Value Target Analysis:** Understanding why DFIR analysts are attractive targets (access to client evidence, domain credentials)
3. **Control Implementation:** Identifying technical controls (email authentication) and process controls (verification procedures)
4. **Incident Response:** Practicing the escalation and analysis workflow for social engineering incidents

**Lab Connection:** After completing this exercise, you can:
- Review the risk register (`docs/risk-register-baseline.md`) to identify social engineering-related risks
- Consider how DarkAI (AST-035) could be used to analyze social engineering patterns
- Evaluate current email security controls in the CADRE lab environment
- Develop a social engineering simulation exercise for the team

---

## Interview Talking Points

**For Business Risk Leadership interviews, emphasize:**

1. **DFIR-Specific Risk Assessment:** "DFIR firms are high-value targets for social engineering because analysts have access to sensitive client evidence and privileged credentials. I assess social engineering risk in the context of our specific threat profile—client impersonation, evidence theft, and credential harvesting."

2. **Layered Defense Strategy:** "I implement technical controls like email authentication (DMARC, SPF, DKIM) as the first line of defense, supported by security awareness training and clear verification procedures. No single control is sufficient—layered defenses are essential."

3. **Security Awareness Program Design:** "Effective security awareness goes beyond annual training. I implement continuous education through phishing simulations, threat intelligence briefings, and scenario-based exercises that reflect real attacks against DFIR firms."

4. **Incident Response Integration:** "Social engineering incidents require specific response procedures. I've established escalation paths for suspicious communications, verification procedures for urgent client requests, and forensic analysis workflows for potential malware delivery."

5. **Business Impact Communication:** "When discussing social engineering risk with the board, I translate technical threats into business impact: 'A successful social engineering attack could compromise client evidence, violate attorney-client privilege, and result in loss of retainers and legal liability.'"

---

## Task

1. Identify the social engineering techniques used in this scenario.
2. Assess the potential impact if the attack had succeeded.
3. Recommend technical and administrative controls to prevent similar attacks.
4. Design a security awareness exercise for Cadre Corp analysts.

## Answer key

1. **Social engineering techniques identified:**
   - **Pretexting:** Fabricated urgent scenario (nation-state intrusion) to manipulate the analyst
   - **Phishing:** Email-based attack with malicious attachment and link
   - **Authority exploitation:** Impersonating a legitimate client to leverage trust
   - **Urgency:** "4-hour response time" to pressure the analyst into bypassing verification
   - **Malware delivery:** Password-protected archive to bypass email filters

2. **Potential impact assessment:**
   - **Immediate:** Malware installation on analyst workstation (AST-007)
   - **Secondary:** Credential theft, lateral movement to domain controllers (AST-001-003)
   - **Tertiary:** Access to client evidence (AST-030), SIEM data (AST-010), cloud identity (AST-020)
   - **Business impact:** Client evidence breach, legal liability, loss of retainers, reputational damage
   - **Compliance impact:** SOC 2 attestation failure, GDPR breach notification requirements

3. **Recommended controls:**
   - **Technical controls:**
     - Implement DMARC, SPF, DKIM for email authentication
     - Deploy email security gateway with attachment sandboxing
     - Enable EDR on all workstations with behavioral monitoring
     - Implement conditional access for cloud storage links
   
   - **Administrative controls:**
     - Establish verification procedures for urgent client requests
     - Implement out-of-band verification for sensitive data transfers
     - Create social engineering incident response procedures
     - Regular phishing simulations tailored to DFIR scenarios

4. **Security awareness exercise design:**
   - **Scenario:** Client impersonation with urgent request and evidence transfer
   - **Target:** All DFIR analysts and SOC staff
   - **Metrics:** Report rate, click rate, time to escalation
   - **Follow-up:** Debrief with lessons learned, control gap analysis
   - **Frequency:** Quarterly simulations with varying sophistication

**Pass criteria:** You can analyze social engineering attacks in the context of DFIR-specific threats and recommend layered defenses that balance security with operational requirements.
