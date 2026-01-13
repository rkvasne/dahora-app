# 📚 Índice de Documentação - Dahora App

> **Ponto central de navegação** para toda documentação do projeto Dahora App v0.2.13

> Navegação: [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

> **Última atualização:** 13 de janeiro de 2026

---

## 🎉 Novidades (Janeiro 2026)

- ✅ **Migração para Handlers** - CallbackRegistry + 4 handlers
- ✅ **8 Protocols** para type hints em `callback_manager.py`
- ✅ **Thread-Safety** em UI root com Lock
- ✅ **Validação única com Pydantic** - removida duplicação
- ✅ **267 testes** passando
- ✅ **100% dos hacks tratados** (14 de 14)
- ✅ **UI refinada** - Spinbox com setas proporcionais
- 📊 Relatório completo: **[ANALISE_PROJETO.md](../ANALISE_PROJETO.md)**

---

## 🚀 Começando (Novos Usuários)

### Para Usuários Finais
- **[README.md](../README.md)** - 📖 Visão geral, instalação e uso do aplicativo
- **[CHANGELOG.md](../CHANGELOG.md)** - 📝 Histórico de mudanças por versão
- **[Apoie o projeto (opcional)](../README.md#-apoie-o-projeto-opcional)** - ☕ Doações (Sponsors/Mercado Pago/PayPal/Pix) + QR

### Para Desenvolvedores
- **[python-windows.md](python-windows.md)** - ⚠️ **LEIA PRIMEIRO!** Use `py` no Windows
- **[architecture.md](architecture.md)** - 🏗️ Arquitetura técnica e componentes
- **[ANALISE_PROJETO.md](../ANALISE_PROJETO.md)** - 📊 Relatório de análise e melhorias (13/01/2026)
- **[development-history.md](development-history.md)** - 📜 Histórico narrativo do desenvolvimento

### Para Manutenedores
- **[release.md](release.md)** - 🚀 Processo completo de build e release
- **[github-cli-guide.md](github-cli-guide.md)** - 🔧 Guia do GitHub CLI e autenticação

---

## 📖 Documentação Técnica

### Frontend (Landing)
- **[landing-template.md](landing-template.md)** - Specs visuais por seção (template reutilizável)

### Arquitetura e Design
- **[architecture.md](architecture.md)** - Estrutura, componentes e padrões
- **[hacks.md](hacks.md)** - Workarounds e soluções não-ideais documentadas
- **[clipboard-monitor.md](clipboard-monitor.md)** - Pesquisa sobre otimização de clipboard com Windows API Events
- **[logs-security.md](logs-security.md)** - Auditoria de segurança dos logs do aplicativo

### Planejamento e Negócio
- **[roadmap.md](roadmap.md)** - Próximos passos e melhorias planejadas
- **[pricing.md](pricing.md)** - Análise de mercado e precificação

### Produto
- **[prd.md](prd.md)** - Requisitos do produto (formal)

### Políticas do Repositório
- **[PRIVACY.md](../PRIVACY.md)** - Política de privacidade (offline/sem telemetria)
- **[SECURITY.md](../SECURITY.md)** - Como reportar vulnerabilidades
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Como contribuir
- **[CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)** - Código de conduta
- **[LICENSE](../LICENSE)** - Licença (MIT)

---

## 🔧 Ferramentas de Desenvolvimento

### GitHub e Versionamento
- **[github-cli-guide.md](github-cli-guide.md)** - Guia completo: instalação, autenticação, comandos
- **[release.md](release.md)** - Build, empacotamento ZIP e Git LFS

### Python no Windows
- **[python-windows.md](python-windows.md)** - ⚠️ Crítico: diferença entre `python` e `py`

### Pastas auxiliares
- **[scripts/README.md](../scripts/README.md)** - Scripts utilitários (build/debug/release)
- **[tests/README.md](../tests/README.md)** - Suíte de testes e como executar

---

## 📋 Estrutura de Diretórios

```
docs/
├── README.md                   ← Você está aqui!
├── architecture.md             # Arquitetura técnica (atualizado 12/01/2026)
├── development-history.md      # Histórico narrativo
├── landing-template.md         # Template da landing (specs por seção)
├── hacks.md                    # Workarounds documentados (atualizado 12/01/2026)
├── prd.md                      # Requisitos do produto (formal)
├── pricing.md                  # Análise de mercado
├── release.md                  # Processo de build e release
├── roadmap.md                  # Próximos passos (atualizado 12/01/2026)
├── github-cli-guide.md         # GitHub CLI completo
├── clipboard-monitor.md        # Pesquisa: clipboard monitor (Windows API Events)
├── logs-security.md            # Auditoria de segurança de logs
└── python-windows.md           # Configuração do Python no Windows

raiz/
└── ANALISE_PROJETO.md          # Relatório de análise completo (NOVO)
```

---

## 🔗 Links Úteis

### Repositório
- **[Repositório no GitHub](https://github.com/rkvasne/dahora-app)**
- **[Releases](https://github.com/rkvasne/dahora-app/releases)**
- **[Issues](https://github.com/rkvasne/dahora-app/issues)**

### Site
- **[Página do site (landing)](https://dahora-app.vercel.app/)**

---

## 🎯 Início rápido por perfil

### 👤 Novo Usuário
1. Leia [README.md](../README.md) - Instalação e uso
2. Baixe em [Releases](https://github.com/rkvasne/dahora-app/releases)
3. Consulte [CHANGELOG.md](../CHANGELOG.md) - Novidades

### 👨‍💻 Desenvolvedor
1. Leia [python-windows.md](python-windows.md) - **IMPORTANTE**
2. Explore [architecture.md](architecture.md) - Estrutura técnica
3. Veja [development-history.md](development-history.md) - Contexto
4. Consulte [hacks.md](hacks.md) - Soluções conhecidas

### 🚀 Manutenedor/Release
1. Configure [github-cli-guide.md](github-cli-guide.md) - Autenticação
2. Siga [release.md](release.md) - Processo completo
3. Atualize [CHANGELOG.md](../CHANGELOG.md) - Sempre!

---

## ⚙️ Convenções do Projeto

- **Terminologia (glossário por superfície):** veja [Glossário por superfície (terminologia)](#glossário-por-superfície-terminologia).

### Glossário por superfície (terminologia)

**Regra geral:** dentro de uma mesma superfície, evite misturar termos PT‑BR e termos técnicos em inglês.

- **Frontend (landing) e UI do app (usuário final):** preferir PT‑BR 100%.
  - Exemplos: “área de transferência”, “bandeja do sistema”, “atalhos”, “notificações do Windows”.
- **Documentação (Markdown) e textos para dev/power users:** preferir termos técnicos comuns em inglês.
  - Exemplos: `clipboard`, `system tray`, `hotkeys`, `toasts`.
- **Código (identificadores):** manter nomes e APIs em inglês; strings exibidas ao usuário seguem o padrão da UI.

### Versionamento
- **Fonte da verdade:** `dahora_app/constants.py` (`APP_VERSION`)
- **Sempre atualizar:**
  - `dahora_app/constants.py`
  - `README.md` (badge e link de download)
  - `CHANGELOG.md` (nova entrada)
  - Arquivo `.spec` gerado em `build/` ao rodar `py build.py`

### Links Internos
- Use caminhos relativos: `docs/file.md`, `../README.md`
- Verifique links antes de commit

### Qualidade Antes de Commit
- ✅ Executar testes: `py -m pytest`
- ✅ Verificar links internos
- ✅ Atualizar `CHANGELOG.md`
- ✅ Versão consistente em todos os arquivos

---

**Última atualização:** 13 de janeiro de 2026 | **Versão:** v0.2.13
