# 🚀 Release — Dahora App

Este guia descreve o fluxo recomendado para gerar um executável, empacotar em ZIP e versionar os artefatos (incluindo Git LFS), mantendo o repositório consistente.

## 1) Atualizar versão

1. Atualize `APP_VERSION` em `dahora_app/constants.py`.
2. Garanta que o `CHANGELOG.md` contém uma seção exatamente no formato:

```md
## [X.Y.Z] - AAAA-MM-DD
```

Isso é importante para automações que extraem notas de release por versão.

## 2) Build do executável

Da raiz do projeto:

```powershell
py build.py
```

O build gera o `.exe` em `dist/`.

## 3) Gerar ZIP para download

Exemplo (PowerShell):

```powershell
$exe = Get-ChildItem dist -Filter "DahoraApp_v*.exe" | Select-Object -First 1
if (-not $exe) { throw "Nenhum .exe encontrado em dist/" }
$zip = Join-Path "dist" ($exe.BaseName + ".zip")
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path $exe.FullName -DestinationPath $zip
Write-Host "ZIP gerado: $zip"
```

## 4) Git LFS (artefatos grandes)

Este repositório usa Git LFS para binários.

- Regras ficam em `.gitattributes`.
- Para garantir rastreamento de `.exe` e `.zip`, mantenha:

```gitattributes
*.exe filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
```

Se necessário:

```powershell
git lfs install
```

## 5) Publicação

Há dois jeitos comuns:

### A) Via GitHub Releases (automático por tag)

Existe um workflow em `.github/workflows/001_release.yml` que roda quando você cria uma tag `vX.Y.Z`.

Passos:

```powershell
git tag vX.Y.Z
git push origin vX.Y.Z
```

O workflow compila e anexa o `.exe` + `.sha256.txt` ao release.

### B) Via Git LFS no branch `main`

- Faça commit do `.zip` (e opcionalmente do `.exe`) e faça push normalmente.
- Use um link raw para download.

Obs.: manter apenas o `.zip` geralmente reduz ruído no repositório.
