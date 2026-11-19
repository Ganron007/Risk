#Requires -Version 5.1
<#
.SYNOPSIS
  Stop CADRE-Risk VerifyWise stack. -RemoveVolumes wipes DB.
#>
param(
    [switch]$RemoveVolumes
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
$DockerDir = Join-Path $RepoRoot 'docker'
$VendorDir = Join-Path $DockerDir 'vendor\verifywise'
$Override = Join-Path $DockerDir 'verifywise-compose.yml'
$EnvFile = Join-Path $DockerDir 'verifywise.env'
$Project = 'Risk'
# Keep compose interpolation happy on `down` too (see docker/verifywise-compose.yml)
$env:VW_NGINX_CONF = Join-Path $DockerDir 'verifywise-nginx.conf'

if (-not (Test-Path (Join-Path $VendorDir 'docker-compose.yml'))) {
    Write-Host 'VerifyWise vendor not cloned - nothing to stop.'
    exit 0
}

Push-Location $VendorDir
try {
    $args = @(
        'compose', '-p', $Project,
        '-f', 'docker-compose.yml',
        '-f', 'docker-compose.prod.yml',
        '-f', $Override,
        '--env-file', $EnvFile,
        'down'
    )
    if ($RemoveVolumes) {
        $args += '-v'
        Write-Host 'Removing containers AND volumes.'
    }
    & docker @args
} finally {
    Pop-Location
}
