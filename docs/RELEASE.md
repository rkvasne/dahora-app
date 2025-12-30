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

Este repositório usa Git LFS para binários grandes (`.exe` e `.zip`).

### 4.1) O que é Git LFS?

**Git LFS** (Large File Storage) armazena arquivos grandes em um servidor separado, evitando inchaço do repositório:
- Sem LFS: Um arquivo `.exe` de 50 MB no repositório = repositório fica grande
- Com LFS: Apenas um pointer (texto pequeno) no Git + arquivo real no LFS storage

### 4.2) Configuração Inicial (Setup)

Execute **uma única vez** no repositório:

```powershell
git lfs install
git lfs version  # Verificar instalação
```

Isso configura hooks de Git para rastrear arquivos automaticamente.

### 4.3) Rastrear Tipos de Arquivo

As regras ficam em `.gitattributes`. Para garantir rastreamento de `.exe` e `.zip`, mantenha:

```gitattributes
*.exe filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
```

Se precisar adicionar mais tipos (ex: `.iso`, `.dmg`):

```powershell
git lfs track "*.iso"
git add .gitattributes
git commit -m "chore: Rastrear .iso no Git LFS"
```

### 4.4) Fluxo Completo de Envio (Push)

#### Passo 1: Preparar arquivo
```powershell
# Seu .exe ou .zip está em dist/ ou raiz
ls dist/*.exe
ls *.zip
```

#### Passo 2: Adicionar ao Git (com -f se no .gitignore)
```powershell
git add -f dist/DahoraApp_v0.2.4.exe
git add DahoraApp_v0.2.4.zip
git add .gitattributes
```

#### Passo 3: Commit
```powershell
git commit -m "v0.2.4: Binários para LFS

- DahoraApp_v0.2.4.exe (~50 MB)
- DahoraApp_v0.2.4.zip (~50 MB)
- GitHub LFS ativado"
```

#### Passo 4: Push
```powershell
git push origin main
```

**Saída esperada:**
```
Uploading LFS objects: 100% (2/2), 101 MB | 8.5 MB/s, done
```

### 4.5) Verificação e Troubleshooting

#### ✅ Verificar se arquivo está no LFS
```powershell
git lfs ls-files
```

**Saída esperada:**
```
f3d7e4a9c2 * dist/DahoraApp_v0.2.4.exe
a8b2c1d9e5 * DahoraApp_v0.2.4.zip
```

#### ✅ Ver status do LFS
```powershell
git lfs status
```

#### ❌ Problema: Arquivo enviado via Git (não LFS)

Se você adicionou o arquivo ANTES de configurar `.gitattributes`, ele foi enviado como arquivo normal (não LFS):

**Solução:**
```powershell
# 1. Remover do histórico (cuidado!)
git rm --cached dist/DahoraApp_v0.2.4.exe

# 2. Adicionar novamente (agora com LFS)
git add dist/DahoraApp_v0.2.4.exe

# 3. Amend commit anterior
git commit --amend --no-edit

# 4. Force push (cuidado: modifica histórico)
git push origin main --force
```

#### ❌ Problema: Git LFS não instalado no clone

Se alguém clonar o repositório sem LFS:

```powershell
git lfs install
git lfs pull  # Baixar arquivos do LFS
```

#### ❌ Problema: Autenticação no LFS

Se receber erro de autenticação ao push:

```powershell
# Verificar credenciais
git config credential.helper

# Reconfigurar credenciais (Windows)
git credential approve  # Digitar credenciais novamente
```

### 4.6) Para Contribuidores Novos

Se você está **clonando este repositório pela primeira vez**:

```powershell
# 1. Clone normal
git clone https://github.com/rkvasne/dahora-app.git
cd dahora-app

# 2. Instale Git LFS
git lfs install

# 3. Baixe arquivos grandes
git lfs pull

# 4. Pronto! Arquivos .exe e .zip estarão completos
ls dist/*.exe
ls *.zip
```

### 4.7) Checklist antes de Push

- [ ] `git lfs version` retorna versão (LFS instalado)
- [ ] `.gitattributes` contém `*.exe` e `*.zip`
- [ ] Arquivo adicionado: `git add -f seu_arquivo.exe`
- [ ] `.gitattributes` adicionado: `git add .gitattributes`
- [ ] Commit realizado: `git commit -m "..."`
- [ ] Push seguro: `git push origin main` (mostra upload LFS)

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
