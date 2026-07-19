#Requires -Version 5.1
<#
.SYNOPSIS
  Seed Cadre Corp AI use cases + risks into local VerifyWise via REST.

.DESCRIPTION
  Markdown SSoT for classic risks: docs/risk-register-baseline.md (RISK-012/013/014/018).
  Docs: docs/verifywise-notes.md

.EXAMPLE
  .\scripts\verifywise-seed-baseline.ps1
  .\scripts\verifywise-seed-baseline.ps1 -Email admin@cadre.local -Password '***REMOVED***'
#>
[CmdletBinding()]
param(
    [string] $BaseUrl = "http://127.0.0.1:13000/api",
    [string] $Email = "admin@cadre.local",
    [string] $Password = "***REMOVED***",
    [string] $OrgName = "Cadre Corp",
    [string] $OrgAdminEmail = "org-admin@cadre.local",
    [string] $OrgAdminPassword = "***REMOVED***"
)

$ErrorActionPreference = "Stop"

function Invoke-Vw {
    param(
        [string] $Method = "Get",
        [string] $Path,
        [object] $Body = $null,
        [string] $Token
    )
    $headers = @{ "Content-Type" = "application/json" }
    if ($Token) { $headers["Authorization"] = "Bearer $Token" }
    $params = @{
        Method      = $Method
        Uri         = "$BaseUrl$Path"
        Headers     = $headers
        ErrorAction = "Stop"
    }
    if ($null -ne $Body) {
        $params["Body"] = ($Body | ConvertTo-Json -Depth 8 -Compress)
    }
    return Invoke-RestMethod @params
}

function Get-Data($resp) {
    if ($null -ne $resp.data) { return $resp.data }
    return $resp
}

Write-Host "VerifyWise seed → $BaseUrl"

# 1) Superadmin login
$login = Get-Data (Invoke-Vw -Method Post -Path "/users/login" -Body @{ email = $Email; password = $Password })
$saToken = $login.token
if (-not $saToken) { throw "Superadmin login failed — check docker/verifywise.env SUPERADMIN_*" }
Write-Host "superadmin OK"

# 2) Org — create or login as org admin
$orgToken = $null
$orgAdminUserId = $null
try {
    $orgCreate = Get-Data (Invoke-Vw -Method Post -Path "/organizations" -Token $saToken -Body @{
            name         = $OrgName
            logo         = "https://verifywise.ai/favicon.ico"
            userEmail    = $OrgAdminEmail
            userName     = "Cadre"
            userSurname  = "Admin"
            userPassword = $OrgAdminPassword
        })
    $orgToken = $orgCreate.token
    $orgAdminUserId = $orgCreate.user.id
    Write-Host "org CREATED id=$($orgCreate.organization.id) admin=$OrgAdminEmail"
} catch {
    Write-Host "org create skipped/failed: $($_.ErrorDetails.Message)"
    $orgLogin = Get-Data (Invoke-Vw -Method Post -Path "/users/login" -Body @{
            email    = $OrgAdminEmail
            password = $OrgAdminPassword
        })
    $orgToken = $orgLogin.token
    # decode not needed — fetch users if required
    Write-Host "org admin login OK"
}

if (-not $orgToken) { throw "No org admin token" }

# Resolve owner id if missing
if (-not $orgAdminUserId) {
    try {
        $me = Get-Data (Invoke-Vw -Path "/users" -Token $orgToken)
        if ($me -is [array]) {
            $u = $me | Where-Object { $_.email -eq $OrgAdminEmail } | Select-Object -First 1
            $orgAdminUserId = $u.id
        } elseif ($me.id) {
            $orgAdminUserId = $me.id
        }
    } catch { }
}
if (-not $orgAdminUserId) { $orgAdminUserId = 2 }  # typical after org create
Write-Host "ownerId=$orgAdminUserId"

# Complete onboarding if endpoint exists
try {
    $orgs = Get-Data (Invoke-Vw -Path "/organizations/exists")
    Write-Host "orgsExist=$orgs"
} catch { }

$projectsSpec = @(
    @{
        Title       = "DarkAI lab chatbot"
        Industry    = "Security research / AI lab"
        Description = "CADRE-DarkAI Docker lab — LLM chatbot for AI-300 practice. Isolation required (RISK-012/013)."
        Classification = "High risk"
        Role        = "Deployer"
        Goal        = "Govern DarkAI LLM use without client evidence mix"
        Model       = "DarkAI-Chatbot"
        Provider    = "CADRE-DarkAI / Ollama"
    }
    @{
        Title       = "RevAI malware analysis pipeline"
        Industry    = "Malware reverse engineering"
        Description = "CADRE-RevAI / RevEng pipeline — sample intake to verdict. RISK-014 mishandling."
        Classification = "High risk"
        Role        = "Provider"
        Goal        = "Track malware AI pipeline under EU AI Act + ISO 42001"
        Model       = "RevAI-Pipeline"
        Provider    = "CADRE-RevAI"
    }
    @{
        Title       = "Praxis CI security scanner"
        Industry    = "Software security tooling"
        Description = "Praxis agentic SAST/SCA CLI used in DarkAI and CI. AI-assisted findings need HITL (RISK-018)."
        Classification = "Limited risk"
        Role        = "Provider"
        Goal        = "Inventory Praxis as AI-assisted security tooling"
        Model       = "Praxis-Scanner"
        Provider    = "Praxis"
    }
)

$existing = @()
try { $existing = @(Get-Data (Invoke-Vw -Path "/projects" -Token $orgToken)) } catch { $existing = @() }
$existingTitles = @{}
foreach ($p in $existing) { if ($p.project_title) { $existingTitles[$p.project_title] = $p } }

$createdProjects = @()
$start = (Get-Date).ToString("yyyy-MM-dd")

foreach ($spec in $projectsSpec) {
    if ($existingTitles.ContainsKey($spec.Title)) {
        Write-Host "SKIP project $($spec.Title)"
        $createdProjects += $existingTitles[$spec.Title]
        continue
    }
    $body = @{
        project_title            = $spec.Title
        owner                    = [int]$orgAdminUserId
        start_date               = $start
        geography                = 1
        target_industry          = $spec.Industry
        description              = $spec.Description
        ai_risk_classification   = $spec.Classification
        type_of_high_risk_role   = $spec.Role
        goal                     = $spec.Goal
        members                  = @([int]$orgAdminUserId)
        framework                = @(1)   # EU AI Act
        enable_ai_data_insertion = $false
        is_organizational        = $false
    }
    try {
        $proj = Get-Data (Invoke-Vw -Method Post -Path "/projects" -Token $orgToken -Body $body)
        Write-Host "OK project $($spec.Title) id=$($proj.id)"
        $createdProjects += $proj
    } catch {
        Write-Host "FAIL project $($spec.Title): $($_.ErrorDetails.Message)"
    }

    # Model inventory
    try {
        $model = Get-Data (Invoke-Vw -Method Post -Path "/modelInventory" -Token $orgToken -Body @{
                model    = $spec.Model
                provider = $spec.Provider
                status   = "Approved"
            })
        Write-Host "OK model $($spec.Model) id=$($model.id)"
    } catch {
        Write-Host "FAIL model $($spec.Model): $($_.ErrorDetails.Message)"
    }
}

# Risks from Cadre AI-related baseline
$risks = @(
    @{ Name = "RISK-012 DarkAI lab breakout / data mix with client evidence"; Desc = "Isolation failure between DarkAI lab and client forensic evidence."; Likelihood = "Possible"; Severity = "Major"; Phase = "Deployment & integration"; Projects = @("DarkAI lab chatbot") }
    @{ Name = "RISK-013 Prompt-injection / LLM abuse leaks lab secrets"; Desc = "Prompt injection against DarkAI chatbot exposes secrets."; Likelihood = "Likely"; Severity = "Major"; Phase = "Deployment & integration"; Projects = @("DarkAI lab chatbot") }
    @{ Name = "RISK-014 Malware sample mishandling on RevAI analysis path"; Desc = "Unsafe sample handling on RevAI/RevEng path."; Likelihood = "Possible"; Severity = "Moderate"; Phase = "Data collection & processing"; Projects = @("RevAI malware analysis pipeline") }
    @{ Name = "RISK-018 AI-generated forensic finding accepted without HITL"; Desc = "LLM finding promoted without examiner approval (DFIR-Nexus DRAFT gate)."; Likelihood = "Possible"; Severity = "Major"; Phase = "Monitoring & maintenance"; Projects = @("Praxis CI security scanner", "RevAI malware analysis pipeline") }
)

# Map title → id
$titleToId = @{}
$allProj = @(Get-Data (Invoke-Vw -Path "/projects" -Token $orgToken))
foreach ($p in $allProj) { $titleToId[$p.project_title] = $p.id }

$existingRisks = @()
try { $existingRisks = @(Get-Data (Invoke-Vw -Path "/projectRisks" -Token $orgToken)) } catch { }
$existingNames = @{}
foreach ($r in $existingRisks) { if ($r.risk_name) { $existingNames[$r.risk_name] = $true } }

foreach ($rk in $risks) {
    if ($existingNames.ContainsKey($rk.Name)) {
        Write-Host "SKIP risk $($rk.Name)"
        continue
    }
    $pids = @()
    foreach ($t in $rk.Projects) {
        if ($titleToId.ContainsKey($t)) { $pids += [int]$titleToId[$t] }
    }
    $body = @{
        risk_name               = $rk.Name
        risk_owner              = [int]$orgAdminUserId
        risk_description        = $rk.Desc
        ai_lifecycle_phase      = $rk.Phase
        likelihood              = $rk.Likelihood
        severity                = $rk.Severity
        risk_severity           = if ($rk.Severity -eq "Catastrophic") { "Critical" } elseif ($rk.Severity -eq "Major") { "Major" } else { "Moderate" }
        mitigation_status       = "In Progress"
        risk_category           = @("Cybersecurity risk", "Data privacy risk")
        impact                  = $rk.Desc
        projects                = $pids
        frameworks              = @(1)
        approval_status         = "Pending"
    }
    try {
        $created = Get-Data (Invoke-Vw -Method Post -Path "/projectRisks" -Token $orgToken -Body $body)
        Write-Host "OK risk $($rk.Name) id=$($created.id)"
    } catch {
        Write-Host "FAIL risk $($rk.Name): $($_.ErrorDetails.Message)"
    }
}

Write-Host ""
Write-Host "UI: http://127.0.0.1:18080"
Write-Host "Login: $OrgAdminEmail / (password from script params / verifywise.env pattern)"
Write-Host "Screenshot: docs/img/verifywise-ai-risk.png"
