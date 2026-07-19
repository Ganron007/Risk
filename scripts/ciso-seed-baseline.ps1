#Requires -Version 5.1
<#
.SYNOPSIS
  Seed Cadre Corp baseline risks into local CISO Assistant via REST API.

.DESCRIPTION
  Markdown SSoT: docs/risk-register-baseline.md
  Docs: docs/ciso-notes.md

  Requires:
    - CISO stack up (.\scripts\ciso-up.ps1)
    - Domain folder named "Cadre Corp" (create once in UI)
    - Risk matrix "5x5 ISO-27005" loaded
    - Personal Access Token (UI profile) or -Token

.EXAMPLE
  $env:CISO_PAT = "...."
  .\scripts\ciso-seed-baseline.ps1
#>
[CmdletBinding()]
param(
    [string] $BaseUrl = "http://localhost:8080/api",
    [string] $Token = $env:CISO_PAT,
    [string] $DomainName = "Cadre Corp",
    [string] $PerimeterName = "Cadre Corp Lab",
    [string] $AssessmentName = "Cadre Corp Baseline Risk Register",
    [string] $MatrixName = "5x5 ISO-27005"
)

$ErrorActionPreference = "Stop"
if (-not $Token) {
    throw "Pass -Token or set env CISO_PAT (Personal Access Token from CISO UI profile)."
}

$H = @{
    Authorization  = "Token $Token"
    "Content-Type" = "application/json"
}

function Get-Results($path) {
    $r = Invoke-RestMethod -Uri "$BaseUrl$path" -Headers $H
    if ($null -ne $r.results) { return $r.results }
    return @($r)
}

function Find-ByName($items, $name) {
    $items | Where-Object { $_.name -eq $name } | Select-Object -First 1
}

# Markdown L/I 1–3 → 5x5 index 0–4
$LiMap = @{ 1 = 0; 2 = 2; 3 = 4 }

$Risks = @(
    @{ Ref = "RISK-001"; Name = "Domain Admin compromise via DCSync / secretsdump"; L = 3; I = 3 }
    @{ Ref = "RISK-002"; Name = "ADCS ESC abuse - auth as privileged user"; L = 3; I = 3 }
    @{ Ref = "RISK-003"; Name = "Cross-forest trust abuse / SID history"; L = 2; I = 3 }
    @{ Ref = "RISK-004"; Name = "Unconstrained delegation on mbr01"; L = 3; I = 3 }
    @{ Ref = "RISK-005"; Name = "SCCM / WSUS misconfig lateral abuse"; L = 2; I = 3 }
    @{ Ref = "RISK-007"; Name = "Client forensic evidence breach / CoC failure"; L = 2; I = 3 }
    @{ Ref = "RISK-013"; Name = "Prompt-injection / LLM abuse leaks lab secrets"; L = 3; I = 2 }
    @{ Ref = "RISK-018"; Name = "AI forensic finding accepted without HITL"; L = 2; I = 3 }
)

Write-Host "API $BaseUrl"

$folder = Find-ByName (Get-Results "/folders/") $DomainName
if (-not $folder) {
    throw "Domain folder '$DomainName' not found. Create it once in the CISO UI, then re-run."
}
Write-Host "folder=$($folder.id)"

$matrix = Find-ByName (Get-Results "/risk-matrices/") $MatrixName
if (-not $matrix) {
    throw "Risk matrix '$MatrixName' not found. Load it from Libraries in the UI, then re-run."
}
Write-Host "matrix=$($matrix.id)"

$perimeter = Find-ByName (Get-Results "/perimeters/") $PerimeterName
if (-not $perimeter) {
    $body = @{
        name        = $PerimeterName
        folder      = $folder.id
        description = "CADRE AD lab + sister tooling"
        ref_id      = "PER-CADRE"
    } | ConvertTo-Json
    $perimeter = Invoke-RestMethod -Method Post -Uri "$BaseUrl/perimeters/" -Headers $H -Body $body
    Write-Host "perimeter CREATED $($perimeter.id)"
} else {
    Write-Host "perimeter EXISTS $($perimeter.id)"
}

$assessment = Find-ByName (Get-Results "/risk-assessments/") $AssessmentName
if (-not $assessment) {
    $body = @{
        name        = $AssessmentName
        folder      = $folder.id
        perimeter   = $perimeter.id
        risk_matrix = $matrix.id
        description = "Seeded from docs/risk-register-baseline.md"
        status      = "in_progress"
        version     = "1.0"
    } | ConvertTo-Json
    $assessment = Invoke-RestMethod -Method Post -Uri "$BaseUrl/risk-assessments/" -Headers $H -Body $body
    Write-Host "assessment CREATED $($assessment.id)"
} else {
    Write-Host "assessment EXISTS $($assessment.id)"
}

$existing = Get-Results "/risk-scenarios/?risk_assessment=$($assessment.id)"
$existingRefs = @{}
foreach ($e in $existing) { if ($e.ref_id) { $existingRefs[$e.ref_id] = $true } }

foreach ($r in $Risks) {
    if ($existingRefs.ContainsKey($r.Ref)) {
        Write-Host "SKIP $($r.Ref) (already present)"
        continue
    }
    $p = $LiMap[$r.L]
    $i = $LiMap[$r.I]
    $body = @{
        risk_assessment = $assessment.id
        ref_id          = $r.Ref
        name            = $r.Name
        current_proba   = $p
        current_impact  = $i
        residual_proba  = $p
        residual_impact = $i
        treatment       = "mitigate"
        description     = "From markdown SSoT risk-register-baseline.md ($($r.Ref))"
    } | ConvertTo-Json
    $sc = Invoke-RestMethod -Method Post -Uri "$BaseUrl/risk-scenarios/" -Headers $H -Body $body
    Write-Host "OK $($r.Ref) $($sc.id)"
}

Write-Host ""
Write-Host "Open: http://localhost:8080 → Risk → $AssessmentName"
Write-Host "Screenshot target: docs/img/ciso-risk-register.png"
