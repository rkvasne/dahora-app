<#
.SYNOPSIS
  Faz stage/commit/push dos artefatos de release em dist/ via Git LFS.

.DESCRIPTION
  Executa o checklist do docs/RELEASE.md:
  - git lfs install
  - prepara ZIP/limpa raiz (chama prepare_release_artifacts.ps1)
  - git add (somente arquivos necessários)
  - git commit
  - git push
  - git lfs ls-files

.PARAMETER Message
  Mensagem do commit. Se omitido, usa um padrão.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\push_release_lfs.ps1

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\push_release_lfs.ps1 -Message "v0.2.5: Binários para LFS"
#>

[CmdletBinding()]
param(
  [string]$Message
)

$ErrorActionPreference = 'Stop'

function Require-Command([string]$Name) {
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if (-not $cmd) { throw "Comando não encontrado: $Name" }
}

# Repo root = parent of scripts/
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

Require-Command git

Write-Host "== Git LFS install =="
& git lfs install

Write-Host "== Prepare artifacts =="
& powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\prepare_release_artifacts.ps1" -Force

$exe = Get-ChildItem dist -Filter 'DahoraApp_v*.exe' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $exe) { throw 'Nenhum .exe encontrado em dist/' }
$zip = Join-Path 'dist' ($exe.BaseName + '.zip')
if (-not (Test-Path $zip)) { throw "ZIP não encontrado: $zip" }

if (-not $Message -or $Message.Trim().Length -eq 0) {
  $Message = "chore(release): add dist artifacts for $($exe.BaseName) (LFS)"
}

Write-Host "== git add =="
& git add .gitattributes .gitignore build.py README.md docs/RELEASE.md scripts/README.md scripts/prepare_release_artifacts.ps1 scripts/prepare_release_artifacts.bat scripts/push_release_lfs.ps1
& git add $exe.FullName $zip

Write-Host "== git status =="
& git status --porcelain=v1

Write-Host "== git commit =="
& git commit -m $Message

Write-Host "== git lfs ls-files =="
& git lfs ls-files

Write-Host "== git push origin main =="
& git push origin main
