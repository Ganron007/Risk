#Requires -Version 5.1
<#
.SYNOPSIS
  Clone CISO Assistant Community and start the CADRE-Risk lab stack.
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
$DockerDir = Join-Path $RepoRoot 'docker'
$VendorDir = Join-Path $DockerDir 'vendor\ciso-assistant'
$Override = Join-Path $DockerDir 'ciso-compose.yml'
$Project = 'Risk'
$Upstream = 'https://github.com/intuitem/ciso-assistant-community.git'

function Test-Command($Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

if (-not (Test-Command git)) { throw 'git is required.' }
if (-not (Test-Command docker)) { throw 'Docker Desktop is required.' }

New-Item -ItemType Directory -Force -Path (Split-Path $VendorDir) | Out-Null

if (-not (Test-Path (Join-Path $VendorDir '.git'))) {
    Write-Host "Cloning $Upstream -> $VendorDir"
    git clone --depth 1 --single-branch -b main $Upstream $VendorDir
} else {
    Write-Host "Updating $VendorDir"
    Push-Location $VendorDir
    git fetch --depth 1 origin main
    git checkout main
    git pull --ff-only origin main
    Pop-Location
}

$dbDir = Join-Path $VendorDir 'db'
New-Item -ItemType Directory -Force -Path $dbDir | Out-Null

Push-Location $VendorDir
try {
    Write-Host "Pulling images (project=$Project)..."
    docker compose -p $Project -f docker-compose.yml -f $Override pull

    Write-Host 'Starting CISO Assistant...'
    docker compose -p $Project -f docker-compose.yml -f $Override up -d

    Write-Host 'Waiting for backend health...'
    $deadline = (Get-Date).AddMinutes(8)
    $ok = $false
    do {
        Start-Sleep -Seconds 5
        try {
            $status = docker inspect -f '{{.State.Health.Status}}' cadre-risk-ciso-backend 2>$null
            if ($status -eq 'healthy') {
                $ok = $true
            } else {
                Write-Host "  backend status=$status ..."
            }
        } catch {
            Write-Host '  backend not ready yet...'
        }
    } while (-not $ok -and (Get-Date) -lt $deadline)

    if (-not $ok) { throw 'Backend health check timed out.' }

    Write-Host ''
    Write-Host 'Backend healthy.'
    $sqlite = Join-Path $dbDir 'ciso-assistant.sqlite3'
    if (-not (Test-Path $sqlite)) {
        Write-Host 'Create local admin (interactive) - or set env and re-run:'
        Write-Host '  email e.g. admin@cadre.local'
        docker compose -p $Project -f docker-compose.yml -f $Override exec backend uv run python manage.py createsuperuser
    } else {
        Write-Host 'Existing SQLite DB found - skipping createsuperuser.'
    }

    Write-Host ''
    Write-Host 'CISO Assistant: http://localhost:8080  (HTTP lab mode)'
    Write-Host 'Containers: cadre-risk-ciso-backend / -frontend / -huey / -caddy / -qdrant'
    Write-Host 'Seed risks via REST: .\scripts\ciso-seed-baseline.ps1  (see docs/ciso-notes.md)'
} finally {
    Pop-Location
}
