# GitHub CLI - Guia Completo

> Navegação: [Índice](INDEX.md) • [README do projeto](../README.md) • [Release](RELEASE.md)

## 📚 Índice
1. [O que é GitHub CLI?](#o-que-é-github-cli)
2. [Diferença entre Git e GitHub CLI](#diferença-entre-git-e-github-cli)
3. [Instalação](#instalação)
4. [Autenticação](#autenticação)
5. [Uso em Projetos](#uso-em-projetos)
6. [Comandos Principais](#comandos-principais)
7. [FAQ](#faq)

---

## O que é GitHub CLI?

**GitHub CLI** (`gh`) é uma ferramenta oficial do GitHub que permite gerenciar seu repositório e projeto **diretamente do terminal**, sem precisar abrir o navegador.

### Funcionalidades Principais:
- ✅ Criar, editar e deletar **releases**
- ✅ Criar e gerenciar **pull requests (PRs)**
- ✅ Criar e gerenciar **issues**
- ✅ Gerenciar **branches**
- ✅ Fazer **authentication automática**
- ✅ Executar **workflows** (GitHub Actions)

---

## Diferença entre Git e GitHub CLI

### `git` - Sistema de Controle de Versão
```
O que faz:
✅ git init          - Inicializa repositório local
✅ git add           - Prepara mudanças
✅ git commit        - Salva mudanças localmente
✅ git push          - Envia commits para GitHub
✅ git pull          - Recebe commits do GitHub
✅ git branch        - Gerencia branches
✅ git merge         - Mescla branches

O que NÃO faz:
❌ Gerenciar releases
❌ Criar pull requests
❌ Gerenciar issues
❌ Autenticar com GitHub automaticamente
```

### `gh` - GitHub CLI (Interação com API)
```
O que faz:
✅ gh release create    - Criar release
✅ gh release edit      - Editar release
✅ gh release delete    - Deletar release
✅ gh pr create         - Criar pull request
✅ gh issue create      - Criar issue
✅ gh auth login        - Autenticar com GitHub
✅ Tudo que git não consegue fazer no GitHub

O que NÃO faz:
❌ Controlar versão local
❌ Fazer commits
❌ Fazer push/pull (já tem git para isso)
```

### Exemplo Prático:

**Só com `git`:**
```powershell
git commit -m "Versão 1.0.0"
git tag v1.0.0
git push origin v1.0.0

# Mas a release não foi criada no GitHub!
# Precisa fazer no site manualmente...
```

**Com `gh`:**
```powershell
git commit -m "Versão 1.0.0"
git tag v1.0.0
git push origin v1.0.0

# Cria a release automaticamente:
gh release create v1.0.0 --title "Release 1.0.0" --notes "Notas da release"

# Pronto! Release criada no GitHub!
```

---

## Instalação

### Windows (Recomendado: winget)

```powershell
winget install GitHub.cli
```

#### Se não tiver winget:

**Opção 1: Chocolatey**
```powershell
choco install gh
```

**Opção 2: Download direto**
1. Acesse: https://github.com/cli/cli/releases
2. Baixe o instalador `.msi` mais recente
3. Execute e siga as instruções

### macOS

```bash
brew install gh
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install gh
```

### Verificar Instalação

```powershell
gh --version
# Resultado esperado:
# gh version 2.x.x (2025-01-02)
```

---

## Autenticação

### Método 1: Autenticação Interativa (Recomendado)

```powershell
gh auth login
```

**Siga as instruções:**
1. Escolha **GitHub.com**
2. Protocolo: **HTTPS**
3. Autenticar com credenciais: **Login via navegador** (recomendado)
4. Copie o código exibido
5. Abra o navegador e cole o código
6. Autorize o GitHub CLI

### Método 2: Token de Acesso Pessoal (Para Automação)

#### Passo 1: Gerar Personal Access Token (PAT)

1. Acesse: https://github.com/settings/tokens?type=pat
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Configure:
   - **Nome:** `Dahora Release Updates` ou `GitHub CLI Access`
   - **Expiration:** `90 days` (ou sua preferência)
   - **Scopes** (marque):
     - ✅ `repo` (Controle total de repositórios)
     - ✅ `workflow` (Atualizar workflows do GitHub Actions)
     - ✅ `gist` (opcional)

4. Clique em **"Generate token"**
5. **COPIE o token** (aparece apenas uma vez!)

#### Passo 2: Configurar Token

**Opção A: Autenticação via CLI (Recomendado)**
```powershell
gh auth login --with-token
# Cole o token e pressione Enter
# Ou:
echo "ghp_your_token_here" | gh auth login --with-token
```

**Opção B: Salvar em Arquivo (Para Scripts)**
```powershell
$token = "ghp_xxxxxxxxxxxxxxxxxxxx"  # Cole seu token aqui
$token | Out-File -FilePath "$HOME\.github_token" -Encoding UTF8
Write-Host "✅ Token salvo em: $HOME\.github_token"

# Autenticar usando o arquivo:
gh auth login --with-token < $HOME\.github_token
```

#### Passo 3: Verificar Autenticação

```powershell
gh auth status
```

Resultado esperado:
```
github.com
  ✓ Logged in to github.com as SEU_USUARIO
  ✓ Git operations configured to use https protocol
  ✓ Token: *******************
```

### ⚠️ Segurança do Token

- **NÃO compartilhe** o token com ninguém
- Arquivo `.github_token` deve estar no `.gitignore`
- Revogue tokens não utilizados em: https://github.com/settings/tokens
- Use tokens com escopo mínimo necessário
- Renove tokens periodicamente

---

## Uso em Projetos

### Para Projeto Novo

Você **NÃO precisa fazer nada especial**! O GitHub CLI está instalado globalmente.

```powershell
# Navegue para o projeto:
cd e:\novo-projeto

# Use normalmente:
gh release list
gh pr create
gh issue create
# ... qualquer comando gh funciona
```

### Primeira Vez no Projeto

Se o projeto já tem commits e tags:

```powershell
cd seu-projeto

# Visualizar releases existentes:
gh release list

# Criar nova release:
gh release create v1.0.0 --title "v1.0.0 - Descrição" --notes "Notas da release"

# Editar release existente:
gh release edit v1.0.0 --title "Novo titulo"
```

### Com Autenticação Automática

Se salvou o token em `$HOME\.github_token`:

```powershell
# No início do seu script PowerShell:
Set-Alias gh "C:\Program Files\GitHub CLI\gh.exe"
$env:GH_TOKEN = (Get-Content "$HOME\.github_token" -Raw).Trim()

# Agora todos os comandos gh funcionam:
gh release list --repo usuario/repo
```

---

## Comandos Principais

### Releases

```powershell
# Listar releases
gh release list --repo usuario/repo

# Ver detalhes de uma release
gh release view v1.0.0 --repo usuario/repo

# Criar release
gh release create v1.0.0 \
    --repo usuario/repo \
    --title "v1.0.0 - Título" \
    --notes "Notas de release" \
    --latest

# Editar release
gh release edit v1.0.0 \
    --repo usuario/repo \
    --title "Novo título" \
    --notes-file release-notes.md

# Deletar release
gh release delete v1.0.0 --repo usuario/repo --yes

# Upload de arquivo em release
gh release upload v1.0.0 ~/file.zip --repo usuario/repo
```

### Pull Requests

```powershell
# Criar PR
gh pr create --title "Título do PR" --body "Descrição"

# Listar PRs
gh pr list --repo usuario/repo

# Ver PR específico
gh pr view 123

# Merge de PR
gh pr merge 123
```

### Issues

```powershell
# Criar issue
gh issue create --title "Título" --body "Descrição"

# Listar issues
gh issue list --repo usuario/repo

# Fechar issue
gh issue close 123
```

### Autenticação

```powershell
# Login interativo
gh auth login

# Ver status de autenticação
gh auth status

# Fazer logout
gh auth logout
```

---

## FAQ

### P: Preciso instalar GitHub CLI em cada projeto?
**R:** NÃO! Instala uma vez no Windows, funciona para todos os projetos.

### P: Posso usar `gh` e `git` juntos?
**R:** SIM! São complementares. Use `git` para commits/push e `gh` para releases/PRs.

### P: Onde o token é armazenado?
**R:** 
- Se usou `gh auth login`: Em `$env:GH_CREDENTIALS` (criptografado)
- Se salvou em arquivo: `$HOME\.github_token`

### P: Qual é mais seguro, armazenar em arquivo ou deixar criptografado?
**R:** Deixar criptografado via `gh auth login` é mais seguro. Se armazenar em arquivo, **SEMPRE** adicione ao `.gitignore`.

### P: O token expira?
**R:** SIM! Tokens clássicos expiram em 90 dias (ou mais, depende da configuração). Você recebe notificação antes.

### P: Como renovar o token?
**R:** 
1. Gere um novo token em: https://github.com/settings/tokens
2. Revogue o antigo
3. Atualize no `$HOME\.github_token` ou execute `gh auth login` novamente

### P: Posso usar o mesmo token para múltiplos repositórios?
**R:** SIM! Um token funciona para todos os repos que você tem acesso (se tiver permissão).

### P: GitHub CLI funciona com repositórios privados?
**R:** SIM! Desde que o token tenha permissão `repo`.

### P: Posso automatizar releases com GitHub CLI?
**R:** SIM! Use scripts PowerShell ou Bash para automatizar criação de releases.

**Exemplo de automação:**
```powershell
# release.ps1
param(
    [string]$version = "1.0.0",
    [string]$title = "Release $version",
    [string]$notes = "Notas da release"
)

$env:GH_TOKEN = (Get-Content "$HOME\.github_token" -Raw).Trim()
gh release create $version --repo usuario/repo --title $title --notes $notes
```

Executar:
```powershell
.\release.ps1 -version "1.0.0" -title "v1.0.0 - Nova release" -notes "Muitos bugs corrigidos"
```

---

## Referências

- 📖 [Documentação Oficial GitHub CLI](https://cli.github.com/manual/)
- 🔗 [GitHub CLI Repository](https://github.com/cli/cli)
- 🎓 [Guia de Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

---

**Última atualização:** 2 de Janeiro de 2026

