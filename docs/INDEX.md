# 📚 Índice de Documentação - Dahora App

> **Ponto central de navegação** para toda documentação do projeto Dahora App v0.2.5

---

## 🚀 Começando (Novos Usuários)

### Para Usuários Finais
- **[README.md](../README.md)** - 📖 Visão geral, instalação e uso do aplicativo
- **[CHANGELOG.md](../CHANGELOG.md)** - 📝 Histórico de mudanças por versão

### Para Desenvolvedores
- **[WINDOWS_PYTHON_SETUP.md](WINDOWS_PYTHON_SETUP.md)** - ⚠️ **LEIA PRIMEIRO!** Use `py` no Windows
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - 🏗️ Arquitetura técnica e componentes
- **[DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)** - 📜 Histórico narrativo do desenvolvimento

### Para Manutenedores
- **[RELEASE.md](RELEASE.md)** - 🚀 Processo completo de build e release
- **[GITHUB_CLI_GUIDE.md](GITHUB_CLI_GUIDE.md)** - 🔧 Guia do GitHub CLI e autenticação

---

## 📖 Documentação Técnica

### Arquitetura e Design
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Estrutura, componentes e padrões
- **[HACKS.md](HACKS.md)** - Workarounds e soluções não-ideais documentadas

### Planejamento e Negócio
- **[ROADMAP.md](ROADMAP.md)** - Próximos passos e melhorias planejadas
- **[PRICING.md](PRICING.md)** - Análise de mercado e precificação

### Relatórios de Versão
- **[REPORTS/v0.2.4.md](REPORTS/v0.2.4.md)** - 📊 Relatório final v0.2.4

### Landing Page
- **[LANDING/analysis.md](LANDING/analysis.md)** - Análise e recomendações da landing page

---

## 🔧 Ferramentas de Desenvolvimento

### GitHub e Versionamento
- **[GITHUB_CLI_GUIDE.md](GITHUB_CLI_GUIDE.md)** - Guia completo: instalação, autenticação, comandos
- **[RELEASE.md](RELEASE.md)** - Build, empacotamento ZIP e Git LFS

### Python no Windows
- **[WINDOWS_PYTHON_SETUP.md](WINDOWS_PYTHON_SETUP.md)** - ⚠️ Crítico: diferença entre `python` e `py`

---

## 📊 Relatórios e Análises

### Relatórios de Versão (docs/REPORTS/)
- **[v0.2.4.md](REPORTS/v0.2.4.md)** - 🎯 Relatório final v0.2.4
  - Status de todas as fases
  - Métricas consolidadas
  - Arquivos criados/modificados

### Análises de Negócio (docs/LANDING/)
- **[analysis.md](LANDING/analysis.md)** - Análise da landing page

---

## 📋 Estrutura de Diretórios

```
docs/
├── INDEX.md                    ← Você está aqui!
├── README.md                   ← Visão geral do diretório
├── ARCHITECTURE.md             # Arquitetura técnica
├── DEVELOPMENT_HISTORY.md      # Histórico narrativo
├── HACKS.md                    # Workarounds documentados
├── PRICING.md                  # Análise de mercado
├── RELEASE.md                  # Processo de build e release
├── ROADMAP.md                  # Próximos passos
├── GITHUB_CLI_GUIDE.md         # GitHub CLI completo
├── WINDOWS_PYTHON_SETUP.md     # Setup Python Windows
├── REPORTS/                    # Relatórios de versão
│   ├── v0.2.4.md
└── LANDING/                    # Análises da landing
    └── analysis.md
```

---

## 🔗 Links Úteis

### Repositório
- **[GitHub Repository](https://github.com/rkvasne/dahora-app)**
- **[Releases](https://github.com/rkvasne/dahora-app/releases)**
- **[Issues](https://github.com/rkvasne/dahora-app/issues)**

### Site
- **[Landing Page](https://dahora-app.vercel.app/)**

---

## 🎯 Quick Start por Perfil

### 👤 Novo Usuário
1. Leia [README.md](../README.md) - Instalação e uso
2. Baixe em [Releases](https://github.com/rkvasne/dahora-app/releases)
3. Consulte [CHANGELOG.md](../CHANGELOG.md) - Novidades

### 👨‍💻 Desenvolvedor
1. Leia [WINDOWS_PYTHON_SETUP.md](WINDOWS_PYTHON_SETUP.md) - **IMPORTANTE**
2. Explore [ARCHITECTURE.md](ARCHITECTURE.md) - Estrutura técnica
3. Veja [DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md) - Contexto
4. Consulte [HACKS.md](HACKS.md) - Soluções conhecidas

### 🚀 Manutenedor/Release
1. Configure [GITHUB_CLI_GUIDE.md](GITHUB_CLI_GUIDE.md) - Autenticação
2. Siga [RELEASE.md](RELEASE.md) - Processo completo
3. Atualize [CHANGELOG.md](../CHANGELOG.md) - Sempre!

---

## ⚙️ Convenções do Projeto

### Versionamento
- **Fonte da verdade:** `dahora_app/constants.py` (`APP_VERSION`)
- **Sempre atualizar:**
  - `dahora_app/constants.py`
  - `README.md` (badge e link de download)
  - `CHANGELOG.md` (nova entrada)
  - Arquivos `.spec` do PyInstaller

### Links Internos
- Use caminhos relativos: `docs/FILE.md`, `../README.md`
- Verifique links antes de commit

### Qualidade Antes de Commit
- ✅ Executar testes: `py -m pytest`
- ✅ Verificar links internos
- ✅ Atualizar `CHANGELOG.md`
- ✅ Versão consistente em todos os arquivos

---

**Última atualização:** Janeiro 2026 | **Versão:** v0.2.5

