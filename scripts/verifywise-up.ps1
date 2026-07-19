#Requires -Version 5.1
<#
.SYNOPSIS
  Clone VerifyWise and start the CADRE-Risk AI-governance stack.
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
$DockerDir = Join-Path $RepoRoot 'docker'
$VendorDir = Join-Path $DockerDir 'vendor\verifywise'
$Override = Join-Path $DockerDir 'verifywise-compose.yml'
$EnvFile = Join-Path $DockerDir 'verifywise.env'
$EnvExample = Join-Path $DockerDir 'verifywise.env.example'
$Project = 'cadre-risk-verifywise'
$Upstream = 'https://github.com/verifywise-ai/verifywise.git'

function Test-Command($Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

if (-not (Test-Command git)) { throw 'git is required.' }
if (-not (Test-Command docker)) { throw 'Docker Desktop is required.' }

if (-not (Test-Path $EnvFile)) {
    if (-not (Test-Path $EnvExample)) { throw "Missing $EnvExample" }
    Copy-Item $EnvExample $EnvFile
    Write-Host "Created $EnvFile - edit JWT_SECRET / SUPERADMIN_PASSWORD before first up."
    Write-Host 'Edit the file, then re-run this script.'
    exit 1
}

New-Item -ItemType Directory -Force -Path (Split-Path $VendorDir) | Out-Null

if (-not (Test-Path (Join-Path $VendorDir '.git'))) {
    Write-Host "Cloning $Upstream -> $VendorDir"
    git clone --depth 1 --single-branch -b develop $Upstream $VendorDir
} else {
    Write-Host "Updating $VendorDir"
    Push-Location $VendorDir
    git fetch --depth 1 origin develop
    git checkout develop
    git pull --ff-only origin develop
    Pop-Location
}

# Ensure FRONTEND_PORT for prod overlay
$envText = Get-Content -Raw $EnvFile
if ($envText -notmatch 'FRONTEND_PORT=') {
    Add-Content $EnvFile "`nFRONTEND_PORT=18080"
}

Push-Location $VendorDir
try {
    # Copy lab env into vendor as .env.prod (upstream install pattern)
    Copy-Item $EnvFile (Join-Path $VendorDir '.env.prod') -Force

    Write-Host "Starting VerifyWise (project=$Project)..."
    docker compose `
        -p $Project `
        -f docker-compose.yml `
        -f docker-compose.prod.yml `
        -f $Override `
        --env-file $EnvFile `
        pull

    docker compose `
        -p $Project `
        -f docker-compose.yml `
        -f docker-compose.prod.yml `
        -f $Override `
        --env-file $EnvFile `
        up -d

    Write-Host ''
    Write-Host 'VerifyWise UI:  http://127.0.0.1:18080'
    Write-Host 'VerifyWise API: http://127.0.0.1:13000'
    Write-Host 'Login: SUPERADMIN_EMAIL / SUPERADMIN_PASSWORD from docker/verifywise.env'
    Write-Host 'Containers: cadre-risk-vw-*'
} finally {
    Pop-Location
}
