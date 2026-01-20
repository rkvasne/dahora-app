<#
.SYNOPSIS
  Prepara artefatos de release (dist/*.exe e dist/*.zip) e remove/move arquivos indevidos.

.DESCRIPTION
  - Move (por padrão) artefatos fora de dist/ para uma pasta .release_trash/ (timestamped).
  - Garante que exista um .zip correspondente ao .exe em dist/.
  - Imprime comandos de Git recomendados para adicionar somente dist/ ao LFS.

.PARAMETER Delete
  Se definido, remove arquivos indevidos em vez de mover para .release_trash/.

.PARAMETER Force
  Não pede confirmação antes de mover/remover.

.PARAMETER ExeName
  Permite escolher explicitamente o executável (ex: DahoraApp_v0.2.4).

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\prepare_release_artifacts.ps1

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\prepare_release_artifacts.ps1 -ExeName DahoraApp_v0.2.4 -Force
#>

[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
  [switch]$Delete,
  [switch]$Force,
  [string]$ExeName
)

$ErrorActionPreference = 'Stop'

function Write-Section([string]$Title) {
  Write-Host "" 
  Write-Host ('=' * 60)
  Write-Host $Title
  Write-Host ('=' * 60)
}

# Repo root = parent of scripts/
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

Write-Section "Dahora App - Preparar artefatos de release"
Write-Host "Repo: $RepoRoot"

$DistDir = Join-Path $RepoRoot 'dist'
if (-not (Test-Path $DistDir)) {
  throw "dist/ não encontrado. Rode o build primeiro: py build.py (ou scripts\\rebuild_clean.bat)."
}

# 1) Detect and handle unwanted artifacts outside dist/
$unwantedPatterns = @(
  'DahoraApp_v*.exe',
  'DahoraApp_v*.zip',
  'dahora-app-*.zip'
)

$unwanted = @()
foreach ($pat in $unwantedPatterns) {
  $unwanted += Get-ChildItem -Path $RepoRoot -Filter $pat -File -ErrorAction SilentlyContinue
}

if ($unwanted.Count -gt 0) {
  Write-Section "Arquivos indevidos fora de dist/ (não devem ir para o LFS)"
  $unwanted | Sort-Object FullName | ForEach-Object { Write-Host "- $($_.Name)" }

  $trashRoot = Join-Path $RepoRoot '.release_trash'
  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $trashDir = Join-Path $trashRoot $stamp

  if (-not $Delete) {
    if (-not (Test-Path $trashDir)) {
      New-Item -ItemType Directory -Path $trashDir | Out-Null
    }
  }

  foreach ($f in $unwanted) {
    if ($Delete) {
      $action = "Excluir"
      if ($Force -or $PSCmdlet.ShouldProcess($f.FullName, $action)) {
        Remove-Item -LiteralPath $f.FullName -Force
      }
    } else {
      $dest = Join-Path $trashDir $f.Name
      $action = "Mover para $dest"
      if ($Force -or $PSCmdlet.ShouldProcess($f.FullName, $action)) {
        Move-Item -LiteralPath $f.FullName -Destination $dest -Force
      }
    }
  }

  if (-not $Delete) {
    Write-Host "" 
    Write-Host "OK: movidos para $trashDir"
  } else {
    Write-Host "" 
    Write-Host "OK: arquivos indevidos removidos."
  }
} else {
  Write-Host "Nenhum ZIP/EXE indevido na raiz (OK)."
}

# 2) Determine which exe to package
$exeCandidates = Get-ChildItem -Path $DistDir -Filter 'DahoraApp_v*.exe' -File -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Descending

if ($ExeName -and $ExeName.Trim().Length -gt 0) {
  $desiredExe = Join-Path $DistDir ($ExeName.Trim() + '.exe')
  if (-not (Test-Path $desiredExe)) {
    throw "Exe não encontrado: $desiredExe"
  }
  $exe = Get-Item $desiredExe
} else {
  if (-not $exeCandidates -or $exeCandidates.Count -eq 0) {
    throw "Nenhum DahoraApp_v*.exe encontrado em dist/. Rode: py build.py"
  }
  $exe = $exeCandidates[0]
}

$baseName = [IO.Path]::GetFileNameWithoutExtension($exe.Name)
$zipPath = Join-Path $DistDir ($baseName + '.zip')

Write-Section "Artefato selecionado"
Write-Host "EXE: $($exe.FullName)"
Write-Host "ZIP: $zipPath"

# 3) Ensure zip exists and contains only dist artifact
if (-not (Test-Path $zipPath)) {
  Write-Host "ZIP não existe - criando..."
  if ($Force -or $PSCmdlet.ShouldProcess($zipPath, 'Criar ZIP')) {
    if (Test-Path $zipPath) {
      Remove-Item -LiteralPath $zipPath -Force
    }
    Compress-Archive -Path $exe.FullName -DestinationPath $zipPath
  }
} else {
  Write-Host "ZIP já existe (OK)."
}

# 4) Validate zip content quickly (count entries)
try {
  Add-Type -AssemblyName System.IO.Compression.FileSystem | Out-Null
  $zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
  $count = $zip.Entries.Count
  $zip.Dispose()
  Write-Host "ZIP entradas: $count"
} catch {
  Write-Host "Aviso: não foi possível inspecionar o ZIP: $($_.Exception.Message)"
}

# 5) Print recommended git commands
Write-Section "Comandos Git recomendados (somente dist/)"
Write-Host "git add .gitattributes"
Write-Host "git add dist/$($exe.Name)"
Write-Host "git add dist/$($baseName).zip"
Write-Host ""
Write-Host "# Opcional: verificar LFS"
Write-Host "git lfs ls-files"

Write-Host ""
Write-Host "Pronto. Se você estava enviando um ZIP do repositório inteiro, agora evite isso; use apenas dist/*.zip."
