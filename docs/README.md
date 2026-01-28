# 📚 Índice de Documentação - Dahora App

> **Ponto central de navegação** para toda documentação do projeto Dahora App v0.2.16

> Navegação: [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

> **Última atualização:** 20 de janeiro de 2026

---

## 🎉 Novidades (Janeiro 2026)

- ✅ **Migração para Handlers** - CallbackRegistry + 4 handlers
- ✅ **8 Protocols** para type hints em `callback_manager.py`
- ✅ **Thread-Safety** em UI root com Lock
- ✅ **Validação única com Pydantic** - removida duplicação
- ✅ **Suíte de testes automatizada** (pytest) — rode `py -m pytest tests/` para validar
- ✅ **100% dos hacks tratados** (14 de 14)
- ✅ **UI refinada** - Spinbox com setas proporcionais
- 📋 Auditoria e dívida técnica: **[technical-audit-2026-01.md](technical-audit-2026-01.md)**

---

## 🚀 Começando (Novos Usuários)

### Para Usuários Finais
- **[README.md](../README.md)** - 📖 Visão geral, instalação e uso do aplicativo
- **[CHANGELOG.md](../CHANGELOG.md)** - 📝 Histórico de mudanças por versão
- **[Apoie o projeto (opcional)](../README.md#-apoie-o-projeto-opcional)** - ☕ Doações (Sponsors/Mercado Pago/PayPal/Pix) + QR

### Para Desenvolvedores
- **[windows-setup.md](windows-setup.md)** - ⚠️ **LEIA PRIMEIRO!** Use `py` no Windows
- **[architecture.md](architecture.md)** - 🏗️ Arquitetura técnica e componentes
- **[technical-audit-2026-01.md](technical-audit-2026-01.md)** - 📋 Auditoria técnica e dívida técnica priorizada (Jan/2026)
- **[CHANGELOG.md](../CHANGELOG.md)** - 📝 Registro oficial de mudanças por versão

### Para Manutenedores
- **[release-process.md](release-process.md)** - 🚀 Processo completo de build e release
- **[github-guide.md](github-guide.md)** - 🔧 Guia do GitHub CLI e autenticação

---

## 📖 Documentação Técnica

### Frontend (Landing)
- **[Design System](../landing/README.md)** - Kit de UI e tokens reutilizáveis

### Arquitetura e Design
- **[architecture.md](architecture.md)** - Estrutura, componentes e padrões
- **[implementation-details.md](implementation-details.md)** - Workarounds e detalhes de implementação
- **[clipboard-monitor.md](clipboard-monitor.md)** - Pesquisa sobre otimização de clipboard com Windows API Events

### Qualidade e Auditorias
- **[technical-audit-2026-01.md](technical-audit-2026-01.md)** - Auditoria técnica, alinhamento de docs e auditoria de logs (Jan/2026)

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
- **[LICENSE.md](../LICENSE.md)** - Licença (MIT)
- **[AGENTS.md](../AGENTS.md)** - Instruções para agentes de IA e modos

---

## 🔧 Ferramentas de Desenvolvimento

### GitHub e Versionamento
- **[github-guide.md](github-guide.md)** - Guia completo: instalação, autenticação, comandos
- **[release-process.md](release-process.md)** - Build, empacotamento ZIP e Git LFS

### Python no Windows
- **[windows-setup.md](windows-setup.md)** - ⚠️ Crítico: diferença entre `python` e `py`

### Pastas auxiliares
- **[scripts/README.md](../scripts/README.md)** - Scripts utilitários (build/debug/release)
- **[tests/README.md](../tests/README.md)** - Suíte de testes e como executar

---

## 📋 Estrutura de Diretórios

```
docs/
├── README.md                   ← Você está aqui!
├── architecture.md             # Arquitetura técnica (atualizado 12/01/2026)
├── implementation-details.md   # Workarounds documentados (atualizado 12/01/2026)
├── technical-audit-2026-01.md  # Auditoria técnica e dívida técnica (Jan/2026)
├── prd.md                      # Requisitos do produto (formal)
├── pricing.md                  # Análise de mercado
├── release-process.md          # Processo de build e release
├── roadmap.md                  # Próximos passos (atualizado 12/01/2026)
├── github-guide.md             # GitHub CLI completo
├── clipboard-monitor.md        # Pesquisa: clipboard monitor (Windows API Events)
└── windows-setup.md            # Configuração do Python no Windows (use `py`)
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
1. Leia [windows-setup.md](windows-setup.md) - **IMPORTANTE**
2. Explore [architecture.md](architecture.md) - Estrutura técnica
3. Veja [technical-audit-2026-01.md](technical-audit-2026-01.md) - Auditoria, alinhamentos e dívida técnica
4. Consulte [implementation-details.md](implementation-details.md) - Workarounds e detalhes

### 🚀 Manutenedor/Release
1. Configure [github-guide.md](github-guide.md) - Autenticação e comandos
2. Siga [release-process.md](release-process.md) - Processo completo
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
