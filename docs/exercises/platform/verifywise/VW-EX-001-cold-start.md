# VW-EX-001 — Cold start and organization setup

**Platform:** VerifyWise  
**Time:** 20 minutes  
**CISSP Domains:** 1 (Security & Risk Management), 5 (Identity & Access Management)  
**Prerequisites:** Docker Desktop running, `verifywise-up.ps1` executed, `docker/verifywise.env` configured

---

## Objective

Bring up VerifyWise from cold state, create the Cadre Corp organization, and configure user access. VerifyWise is Cadre Corp's AI governance platform — tracking AI system risks under the EU AI Act, ISO 42001, and NIST AI RMF for DarkAI, RevAI, and Praxis projects.

---

## Steps

### Step 1 — Bring up the stack
```powershell
cd <repo-root>   # folder containing scripts/ and docker/
.\scripts\verifywise-up.ps1
```
Wait for all containers to report healthy. The stack includes: frontend (UI on `:18080`), backend API (`:13000`), PostgreSQL database, and supporting services.

### Step 2 — Log in as superadmin
1. Open `http://127.0.0.1:18080` in your browser.
2. Log in with superadmin credentials from `docker/verifywise.env`:
   - **Email:** `admin@cadre.local`
   - **Password:** from `SUPERADMIN_PASSWORD` in the env file
3. The superadmin creates organizations but doesn't manage them — that's the org admin's role.

### Step 3 — Create the Cadre Corp organization
1. Navigate to **Organizations** → **Create Organization**.
2. Name: `Cadre Corp`. Description: `AI governance domain for Cadre Corp DFIR services — tracking AI/ML systems (DarkAI, RevAI, Praxis) under EU AI Act, ISO 42001, and NIST AI RMF.`
3. Save. The organization is created.

### Step 4 — Create the org admin account
1. Navigate to **Users** → **Create User**.
2. Create: `org-admin@cadre.local` with role **Organization Admin**.
3. Set password: **your choice** — reuse the `SUPERADMIN_PASSWORD` from `docker/verifywise.env`; the seed script gives org-admin the same password unless you pass `-OrgAdminPassword`.
4. This is the account used for ALL Cadre Corp data management — superadmin only touches organization-level operations.

### Step 5 — Log in as org admin and verify
1. Log out of superadmin.
2. Log in as `org-admin@cadre.local`.
3. You should see the Cadre Corp organization dashboard with zero projects, zero AI systems — ready for VW-EX-002.

---

## Verification Checklist

- [ ] VerifyWise UI loads at `http://127.0.0.1:18080`
- [ ] Superadmin logged in, Cadre Corp organization created
- [ ] Org admin account created and able to log in
- [ ] Org admin sees empty Cadre Corp dashboard

---

## CISSP Connection

**Domain 1:** AI governance is an emerging sub-discipline of security governance. The EU AI Act's risk-based classification system (Prohibited, High, Limited, Minimal) parallels traditional risk management frameworks — demonstrating that governance principles extend to AI systems.

**Domain 5:** The two-tier account model (superadmin for org management, org admin for data management) demonstrates role-based access control and separation of duties in a GRC platform — core IAM principles.

---

## Interview Talking Points

1. **"I can operationalize AI governance":** "When the EU AI Act takes effect, companies deploying AI systems need governance platforms to track risk classifications, maintain model inventories, and document compliance. I've evaluated VerifyWise as an AI governance solution, deployed it in our lab, and configured it for Cadre Corp's three AI projects."

2. **"GRC isn't just spreadsheets anymore":** "CISO Assistant handles classic GRC. VerifyWise handles AI governance. I can work with both — understanding that different risk domains need different tooling, but both feed into a unified risk view."