# 🚀 Release — Dahora App

> Navegação: [Documentação](README.md) • [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

> **Última atualização:** 20 de janeiro de 2026 | **Versão atual:** v0.2.16

Este guia descreve o fluxo recomendado para gerar um executável, empacotar em ZIP e versionar os artefatos (incluindo Git LFS), mantendo o repositório consistente.

## 📋 Checklist Pré-Release

Antes de criar uma nova release:

- [ ] Rodar testes: `py -m pytest`
- [ ] Sem erros de lint: `py -m flake8 dahora_app/`
- [ ] Versão atualizada em `dahora_app/constants.py`
- [ ] `CHANGELOG.md` atualizado com nova seção
- [ ] Documentação revisada (roadmap.md, architecture.md)

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

### 2.1) Solução de problemas (build/executável)

#### ❌ Erro ao executar: `No module named 'pydantic'`

Isso indica que o executável foi gerado sem embutir o `pydantic`.

Checklist:
- `pydantic` está listado em `requirements.txt`
- O ambiente de build tem as deps instaladas: `py -m pip install -r requirements.txt`
- O `build.py` inclui `pydantic`/`pydantic_core` como dependências/hidden imports do PyInstaller

## 3) Gerar ZIP para download

✅ Recomendado: o `build.py` já gera automaticamente um ZIP **somente com o artefato final** em `dist/`.

```powershell
py build.py
# (opcional) desabilitar zip automático:
# py build.py --no-zip
```

Alternativa (PowerShell):

```powershell
$exe = Get-ChildItem dist -Filter "DahoraApp_v*.exe" | Select-Object -First 1
if (-not $exe) { throw "Nenhum .exe encontrado em dist/" }
$zip = Join-Path "dist" ($exe.BaseName + ".zip")
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path $exe.FullName -DestinationPath $zip
Write-Host "ZIP gerado: $zip"
```

⚠️ Evite criar ZIP “na raiz do repositório” (ex: `dahora-app-X.Y.Z.zip` compactando a pasta toda).
Isso costuma incluir arquivos desnecessários (builds antigos, docs antigas, caches etc.). O ZIP de release deve conter apenas o executável (onefile) ou a pasta `dist/<nome>/` (onedir).

Dica: existe um helper que faz essa limpeza e garante o ZIP correto:

```bat
scripts\prepare_release_artifacts.bat
```

## 3.1) Distribuição recomendada (GitHub Releases)

✅ Para usuários finais, publique e recomende baixar pelos **Assets** do release:
- `DahoraApp_vX.Y.Z.zip` (recomendado)
- (opcional) `DahoraApp_vX.Y.Z.exe`

✅ Para ter um link fixo de “última versão”, publique também assets com nome estável:
- `DahoraApp_latest.zip`
- `DahoraApp_latest.exe`

Links recomendados:
- Página do release: https://github.com/rkvasne/dahora-app/releases/latest
- Download direto: https://github.com/rkvasne/dahora-app/releases/latest/download/DahoraApp_latest.zip

## 4) Git LFS (artefatos grandes)

Este repositório usa Git LFS para binários grandes (`.exe` e `.zip`).

### 4.1) O que é Git LFS?

**Git LFS** (Large File Storage) armazena arquivos grandes em um servidor separado, evitando inchaço do repositório:
- Sem LFS: Um arquivo `.exe` de 50 MB no repositório = repositório fica grande
- Com LFS: Apenas um pointer (texto pequeno) no Git + arquivo real no LFS storage

### 4.2) Configuração inicial

Execute **uma única vez** no repositório:

```powershell
git lfs install
git lfs version  # Verificar instalação
```

Isso configura hooks de Git para rastrear arquivos automaticamente.

### 4.3) Rastrear Tipos de Arquivo

As regras ficam em `.gitattributes`. Para garantir rastreamento de `.exe` e `.zip`, mantenha:

```gitattributes
dist/*.exe filter=lfs diff=lfs merge=lfs -text
dist/*.zip filter=lfs diff=lfs merge=lfs -text
```

Se precisar adicionar mais tipos (ex: `.iso`, `.dmg`):

```powershell
git lfs track "*.iso"
git add .gitattributes
git commit -m "chore: Rastrear .iso no Git LFS"
```

### 4.4) Fluxo Completo de Envio (Push)

✅ Atalho (1 comando):

```bat
scripts\push_release_lfs.bat
```

Isso executa: prepara artefatos (limpa raiz/gera ZIP) → `git add` → `git commit` → `git push` → valida `git lfs ls-files`.

#### Passo 1: Preparar arquivo
```powershell
# Seu .exe e .zip devem estar em dist/
ls dist/*.exe
ls dist/*.zip
```

#### Passo 2: Adicionar ao Git (com -f se no .gitignore)
```powershell
git add -f dist/DahoraApp_vX.Y.Z.exe
git add dist/DahoraApp_vX.Y.Z.zip
git add .gitattributes
```

#### Passo 3: Commit
```powershell
git commit -m "vX.Y.Z: Binários para LFS

- DahoraApp_vX.Y.Z.exe (~50 MB)
- DahoraApp_vX.Y.Z.zip (~50 MB)
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

### 4.5) Verificação e solução de problemas

#### ✅ Verificar se arquivo está no LFS
```powershell
git lfs ls-files
```

**Saída esperada:**
```
<hash> * dist/DahoraApp_vX.Y.Z.exe
<hash> * dist/DahoraApp_vX.Y.Z.zip
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
git rm --cached dist/DahoraApp_vX.Y.Z.exe

# 2. Adicionar novamente (agora com LFS)
git add dist/DahoraApp_vX.Y.Z.exe

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
ls dist/*.zip
```

### 4.7) Checklist antes de Push

- [ ] `git lfs version` retorna versão (LFS instalado)
- [ ] `.gitattributes` contém `*.exe` e `*.zip`
- [ ] Arquivo adicionado: `git add dist/seu_arquivo.exe` e `git add dist/seu_arquivo.zip`
- [ ] `.gitattributes` adicionado: `git add .gitattributes`
- [ ] Commit realizado: `git commit -m "..."`
- [ ] Push seguro: `git push origin main` (mostra upload LFS)

## 5) Publicação

Há dois jeitos comuns:

### A) Via GitHub Releases (automático por tag)

Existe um workflow em `.github/workflows/release.yml` que roda quando você cria uma tag `vX.Y.Z`.

Passos:

```powershell
git tag vX.Y.Z
git push origin vX.Y.Z
```

O workflow compila e anexa o `.exe` + `.sha256.txt` ao release.

### B) Via Git LFS no branch `main`

- Faça commit do `.zip` (e opcionalmente do `.exe`) e faça push normalmente.
- Use um link raw para download.

### C) Verificação pós-release (GitHub CLI)

```powershell
gh release view vX.Y.Z --repo rkvasne/dahora-app --json assets,url
```

```powershell
gh run list --repo rkvasne/dahora-app --workflow release.yml --limit 1
gh run view <RUN_ID> --repo rkvasne/dahora-app
```

Obs.: manter apenas o `.zip` geralmente reduz ruído no repositório.
