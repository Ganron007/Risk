# R-EX-072 — Security audit planning and execution

**CISSP Reference:** Chapter 15, Section "Security Management Processes"; Chapter 1, Section "Security Governance"  
**Exam Objective:** 6.2.1 Conduct security audits; 6.2.2 Report audit findings  
**Study Guide Key Terms:** Internal audit, external audit, audit scope, audit evidence, finding, qualified opinion, management response, remediation tracking  

---

## Scenario Context

Cadre Corp's first SOC 2 Type II audit is in 60 days. The audit scope covers: client evidence handling (AST-030), identity and access management, change management, and SOC monitoring operations. The CISO is preparing the organization but has discovered that:

1. Evidence for several controls exists only in people's email inboxes and Slack messages — not in an organized, auditable repository.
2. Half the controls in `docs/control-register.md` have never been tested — they're documented but their operating effectiveness is unproven.
3. The previous internal audit (18 months ago) had 12 findings — only 4 have been remediated, and the remediation evidence for those 4 is inconsistent.

---

## Multiple-Choice Questions

**Question 1:** What is the PRIMARY difference between an internal audit and an external audit?

A. Internal audits use checklists; external audits use interviews  
B. Internal audits are conducted by (or on behalf of) the organization for self-assessment and improvement; external audits are conducted by independent third parties and result in a formal opinion relied upon by customers and regulators  
C. Internal audits are always less thorough  
D. External audits replace the need for internal audits

**Question 2:** For SOC 2, what constitutes sufficient "audit evidence"?

A. The auditor's personal opinion about whether controls work  
B. Documentation demonstrating that a control was designed appropriately AND operated effectively over the audit period — system configurations, logs, screen captures, approved change records, access review attestations  
C. A verbal confirmation from the CISO  
D. The organization's security policy documentation alone

**Question 3:** When an auditor issues a "qualified opinion," it means:

A. The auditor is not qualified to perform the audit  
B. Except for the matters described in the qualification, the controls meet the criteria — there are specific issues that prevent a clean opinion, but the overall control environment is not fundamentally unsound  
C. The audit found zero issues  
D. The organization failed the audit completely

---

## Answer Explanations

**Answer 1: B**  
**Internal audits** are self-assessments for internal improvement — the organization audits itself (or hires a firm to act as internal audit). **External audits** (like SOC 2) are performed by independent CPA firms and result in a formal opinion that clients and regulators rely upon. External audits don't replace internal audits (D) — mature organizations use internal audits as preparation and continuous improvement between external audits.

**Answer 2: B**  
Audit evidence must demonstrate **design AND operating effectiveness**. Design = the control exists (policy document, system configuration). Operating = the control worked consistently over the audit period (logs showing it fired, change records with approvals, access review documentation with manager sign-offs). Emails and Slack messages (A) are not organized evidence. Verbal confirmation (C) is not evidence. Policy alone (D) proves design, not operation.

**Answer 3: B**  
A **qualified opinion** means "good, except for these specific issues." It's not a failure — it's the auditor saying "overall your controls are designed and operating effectively, but we found specific exceptions in areas X and Y." This is distinct from an "adverse opinion" (controls are fundamentally deficient) or a "disclaimer of opinion" (auditor couldn't obtain enough evidence to form an opinion).

---

## Cadre Corp Application

1. **60-Day Audit Prep Checklist:** (a) Organize evidence repository — one folder per control, containing dated, named evidence files, (b) Test all controls at least once before the audit window, (c) Remediate the 8 open findings from the last internal audit, (d) Conduct a mock audit walkthrough with a senior team member playing auditor.

2. **Evidence Collection Automation:** Where possible, generate audit evidence automatically: scheduled reports of access reviews, automated configuration snapshots, system-generated change logs. This reduces reliance on people remembering to save emails.

3. **Remediation Tracking:** Use the existing `CHECKLIST.md` pattern — each finding has a unique ID, assigned owner, target date, and status. Evidence of remediation is linked from the tracking sheet.

---

## Interview Talking Points

1. **Audit Evidence Is a Product, Not an Afterthought:** "If your control evidence lives in people's inboxes, you don't have an audit trail — you have hope. Evidence must be collected, organized, and reviewed BEFORE the auditor arrives. The audit itself should be a confirmation of what you already know."

2. **Internal Audit Is Rehearsal; External Audit Is Performance:** "If your first real test of controls is the SOC 2 audit, you've already failed. Internal audits find the gaps when it's safe. External audits verify the gaps are closed."
