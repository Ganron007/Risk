#Requires -Version 5.1
<#
.SYNOPSIS
  Stop CADRE-Risk CISO Assistant stack. -RemoveData wipes local SQLite + compose volumes.
#>
param(
    [switch]$RemoveData
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
$DockerDir = Join-Path $RepoRoot 'docker'
$VendorDir = Join-Path $DockerDir 'vendor\ciso-assistant'
$Override = Join-Path $DockerDir 'ciso-compose.yml'
$Project = 'Risk'

if (-not (Test-Path (Join-Path $VendorDir 'docker-compose.yml'))) {
    Write-Host 'CISO vendor not cloned - nothing to stop.'
    exit 0
}

Push-Location $VendorDir
try {
    $composeArgs = @(
        'compose', '-p', $Project,
        '-f', 'docker-compose.yml',
        '-f', $Override,
        'down'
    )
    if ($RemoveData) {
        $composeArgs += '-v'
        Write-Host 'Stopping and removing volumes...'
    }
    & docker @composeArgs

    if ($RemoveData) {
        $dbDir = Join-Path $VendorDir 'db'
        if (Test-Path $dbDir) {
            Remove-Item -Recurse -Force $dbDir
            Write-Host "Removed $dbDir"
        }
    }
} finally {
    Pop-Location
}
