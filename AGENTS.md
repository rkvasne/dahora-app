# AGENTS.md

> Este arquivo fornece instruções para agentes de IA que trabalham neste projeto.
> Compatível com: VS Code + Copilot, Cursor, Windsurf, Trae, Gemini CLI, e outros.
>
> Propósito: README.md é para humanos. AGENTS.md é para agentes de IA — contém contexto técnico detalhado que seria verboso demais num README: comandos de build, testes, convenções de código, estrutura do projeto.

---

## ✅ Fontes Canônicas

- **Documentação do projeto:** [docs/README.md](docs/README.md)
- **Comandos Python no Windows:** [docs/windows-setup.md](docs/windows-setup.md)

---

## 📋 Instruções de Uso

**Para monorepos/projetos grandes:**
- Você pode criar múltiplos `AGENTS.md` aninhados em subpastas
- O arquivo **mais próximo** do código editado tem precedência
- Exemplo: `packages/api/AGENTS.md` prevalece sobre `./AGENTS.md` quando editando arquivos em `packages/api/`

**Ordem de precedência (maior → menor):**
1. Instruções explícitas do usuário no chat
2. AGENTS.md mais próximo do arquivo sendo editado
3. AGENTS.md na raiz do projeto
4. `.github/copilot-instructions.md` (VS Code/Copilot)
5. Regras globais da IDE

**Localizações reconhecidas automaticamente (baseado no código do VS Code):**
- `AGENTS.md` - Raiz do projeto
- `.github/copilot-instructions.md` - GitHub Copilot (opcional, crie se precisar)
- `packages/*/AGENTS.md` - Monorepos (se habilitado)

**Configurações do VS Code (settings.json):**
```json
// Habilitar suporte a .github/copilot-instructions.md
"github.copilot.chat.codeGeneration.useInstructionFiles": true

// Habilitar suporte a AGENTS.md
"chat.useAgentsMdFile": true

// Habilitar AGENTS.md aninhados em subpastas (monorepos) - EXPERIMENTAL
"chat.useNestedAgentsMdFiles": true
```

**Como usar .github/copilot-instructions.md (Recomendado):**
1. Copie o arquivo de regras para `.github/copilot-instructions.md` na raiz do projeto
2. Customize conforme necessário para o projeto específico
3. VS Code carregará automaticamente (se `useInstructionFiles: true`)
4. **Não use** `github.copilot.chat.codeGeneration.instructions` no settings.json (deprecated)

**Agent Skills (recursos reutilizáveis):**
VS Code busca automaticamente em:
- `.github/skills/` (workspace)
- `.claude/skills/` (workspace)  
- `~/.copilot/skills/` (home do usuário)
- `~/.claude/skills/` (home do usuário)

**Beast Mode (integrado ao VS Code - Janeiro 2026):**
Microsoft integrou Beast Mode ao prompt do sistema do Copilot. Configurações opcionais:
```json
"github.copilot.chat.alternateGptPrompt.enabled": true,
"chat.todoListTool.enabled": true
```

Workflow recomendado (persona-based approach):
1. Pesquisa/Research → 2. PRD (Product Requirements) → 3. Tech Spec → 4. Implementação

Referências oficiais:
- [Beast Mode PR (microsoft/vscode)](https://github.com/microsoft/vscode-copilot-chat/pull/467)
- [OpenAI Prompting Guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)
- [Persona-based AI Programming (Nicholas Zakas)](https://humanwhocodes.com/blog/2025/06/persona-based-approach-ai-assisted-programming/)
- [Copilot + MCP Agents (Austen Stone)](https://austen.info/blog/github-copilot-agent-mcp/)

> Fonte: Código-fonte do VS Code (microsoft/vscode) - Janeiro 2026

---

## 🖥️ Ambiente

- **Sistema Operacional:** Windows 11
- **Idioma de Resposta:** Português (pt-BR)
- **Modelo de IA:** Sempre informe qual modelo está sendo usado

---

## ⚠️ REGRA MÁXIMA DE ALTERAÇÃO

**❌ NUNCA altere código que não foi explicitamente solicitado.**

### Obrigatório:
- ✅ Edite APENAS o que for claramente pedido
- ✅ Pergunte antes se houver qualquer dúvida sobre escopo
- ✅ Mantenha todo o resto do código intacto
- ❌ NÃO reescreva funções ou arquivos inteiros sem solicitação
- ❌ NÃO refatore, otimize ou "melhore" código por conta própria
- ❌ NÃO sugira alterações automáticas não solicitadas

---

## 🎯 REGRA DE HONESTIDADE (Zero Achismos)

**❌ NUNCA invente informações ou faça afirmações sem base factual.**

### Proibido:
- ❌ Percentuais sem fonte ("83% dos projetos usam X")
- ❌ Superlativos sem comprovação ("melhor solução", "sempre funciona")
- ❌ Estatísticas inventadas ("usado por milhões")
- ❌ Afirmações categóricas sobre preferências ("todo mundo usa Y")
- ❌ "Garantias" que você não pode cumprir

### Obrigatório:
- ✅ Diga "não sei" quando não souber
- ✅ Use "geralmente", "comumente", "pode" em vez de "sempre", "todos"
- ✅ Cite fonte quando fizer afirmação estatística
- ✅ Admita limitações e incertezas
- ✅ Seja específico sobre o que é fato vs opinião

---

## 🚫 REGRA ANTI-CONCORDÂNCIA AUTOMÁTICA

**❌ NUNCA concorde automaticamente sem analisar primeiro.**

### Proibido:
- ❌ "Você tem razão" sem análise prévia
- ❌ "Você está absolutamente certo" como primeira resposta
- ❌ "Concordo 100%" antes de verificar
- ❌ Concordar apenas para agradar
- ❌ Evitar discordância por receio

### Obrigatório:
- ✅ ANALISE primeiro, responda depois
- ✅ Se o usuário estiver errado, diga educadamente e explique por quê
- ✅ Se parcialmente correto, seja específico: "X está correto, mas Y precisa ajuste"
- ✅ Questione premissas quando necessário: "Antes de prosseguir, precisamos confirmar se..."
- ✅ Apresente trade-offs e alternativas, não apenas confirme a ideia do usuário
- ✅ Use "Vou analisar..." ou "Deixe-me verificar..." antes de concordar

**Exemplo ERRADO:**
```text
Usuário: Acho que devemos usar MongoDB aqui.
IA: Você tem razão! MongoDB é a melhor escolha.
```

**Exemplo CORRETO:**
```text
Usuário: Acho que devemos usar MongoDB aqui.
IA: Vou analisar o caso de uso primeiro. Para dados relacionais com transações ACID, 
PostgreSQL seria mais adequado. MongoDB faz sentido se você tiver:
- Dados não estruturados
- Necessidade de escala horizontal imediata
- Schema flexível

Qual é o caso específico do projeto?
```

---

## 🎯 Modos de Trabalho

**Este projeto usa Prompt Files do repositório canônico `E:\Agents` (pasta `.github/prompts/`) via workspace multi-root.**

### Usar Modos de Trabalho Especializados

No chat do Copilot, digite **`/`** seguido do nome do modo:

| Contexto | Comando | Descrição |
|----------|---------|-----------|
| 🏗️ **Arquitetura** | `/modo-arquiteto` | Design, planejamento, roadmap |
| � **Backend** | `/modo-backend` | APIs, banco de dados, lógica |
| � **Debugging** | `/modo-depurador` | Debug unificado |
| � **DevOps** | `/modo-devops` | Infra, CI/CD, administração |
| � **Documentação** | `/modo-documentacao` | Docs, README, guias |
| 🎨 **Frontend/UI** | `/modo-frontend` | React, CSS, componentes |
| 🧐 **Code Review** | `/modo-code-review` | Revisões de PR e boas práticas |
| 🔀 **Git/VCS** | `/modo-git` | Commits, branches, merges |
| ✅ **Qualidade** | `/modo-qualidade` | Testes, QA, performance |
| 🔒 **Segurança** | `/modo-seguranca` | Auth, OWASP, vulnerabilidades |

---

## 🔒 Execução de Comandos

- ❌ **NUNCA** execute comandos em terminal sem autorização explícita
- Isso inclui: instalações, scripts, migrações de banco, automações
- ✅ Sempre pergunte antes de executar qualquer comando

---

## 📁 Convenções de Arquivos

### Nomenclatura
- ✅ Use prefixos numéricos para ordenação: `001_criar_tabelas.sql`
- ❌ NUNCA use sufixos como `_fix`, `_v2`, `_novo`, `_final`
- ✅ Corrija o arquivo original até que funcione

### 📄 Regra de Documentação

**❌ NUNCA crie novos documentos desnecessários.**

- ✅ Atualizações de status → `CHANGELOG.md`
- ✅ Configurações de setup → Consolidar em `AGENTS.md`
- ✅ Validações e checklists → Adicionar ao doc existente mais relevante
- ❌ Não crie arquivos como `SETUP_COMPLETE.md`, `UPDATE_SUMMARY.md`, `VALIDATION_CHECKLIST.md`
- ✅ Antes de criar um arquivo, pergunte: "Existe doc que já cobre isso?"

### Estrutura do Projeto

```text
dahora-app/
├── main.py                    # Ponto de entrada da aplicação
├── build.py                   # Script de build (PyInstaller)
├── icon.ico                   # Ícone principal do app
├── requirements.txt           # Dependências de produção
├── requirements-dev.txt       # Dependências de desenvolvimento
├── settings.json.example      # Exemplo de configuração
│
├── dahora_app/                # Código-fonte principal
│   ├── __init__.py
│   ├── constants.py           # Constantes (APP_VERSION, paths)
│   ├── settings.py            # Gerenciador de configurações
│   ├── schemas.py             # Validação Pydantic
│   ├── hotkeys.py             # Gerenciador de hotkeys globais
│   ├── hotkey_validator.py    # Validação de hotkeys
│   ├── clipboard_manager.py   # Monitor de clipboard + histórico
│   ├── datetime_formatter.py  # Formatação de timestamps
│   ├── callback_manager.py    # Orquestrador de callbacks
│   ├── notifications.py       # Notificações Windows (winotify)
│   ├── single_instance.py     # Garantia de instância única
│   ├── thread_sync.py         # Coordenação de threads
│   ├── counter.py             # Contador de eventos
│   ├── utils.py               # Utilitários gerais
│   │
│   ├── handlers/              # Handlers de ações
│   │   ├── copy_datetime_handler.py
│   │   ├── quit_app_handler.py
│   │   ├── show_search_handler.py
│   │   └── show_settings_handler.py
│   │
│   └── ui/                    # Interface gráfica (CustomTkinter)
│       ├── menu.py            # Menu do system tray
│       ├── modern_settings_dialog.py
│       ├── modern_search_dialog.py
│       ├── modern_about_dialog.py
│       ├── modern_shortcut_editor.py
│       ├── modern_styles.py   # Temas escuro/claro
│       └── icon_manager.py    # Gerenciamento de ícones
│
├── tests/                     # Testes unitários e integração
│   ├── conftest.py            # Fixtures do pytest
│   ├── test_schemas.py
│   ├── test_hotkey_validator.py
│   ├── test_settings.py
│   ├── test_handlers.py
│   └── ... (13 arquivos de teste)
│
├── docs/technical_audit_2026_01.md # Auditoria técnica e dívida técnica (Jan/2026)
│
├── docs/                      # Documentação
│   ├── architecture.md        # Arquitetura detalhada (atualizado 12/01/2026)
│   ├── implementation-details.md # Workarounds (14 de 14 resolvidos)
│   ├── release-process.md     # Processo de release
│   ├── roadmap.md             # Plano futuro (atualizado 12/01/2026)
│   └── windows-setup.md       # Setup Python no Windows
│
├── scripts/                   # Scripts utilitários
│   ├── prepare_release_artifacts.ps1
│   ├── push_release_lfs.ps1
│   └── clean_icons.ps1
│
├── landing/                   # Landing page (HTML/CSS)
│   ├── styles.css
│   ├── variables.css
│   └── responsive.css
│
├── .github/                   # Configurações do GitHub
│
└── dist/                      # Executáveis gerados (Git LFS)
```

---

## 🛠️ Comandos do Projeto

⚠️ **IMPORTANTE:** Use `py` ao invés de `python` neste projeto (ver [windows-setup.md](docs/windows-setup.md))

```powershell
# Instalar dependências
py -m pip install -r requirements.txt
py -m pip install -r requirements-dev.txt

# Rodar em desenvolvimento
py main.py

# Build executável (PyInstaller)
py build.py

# Rodar testes
py -m pytest                    # Todos os testes
py -m pytest -v                 # Verbose
py -m pytest tests/test_schemas.py  # Arquivo específico
py -m pytest --cov=dahora_app   # Com cobertura

# Verificar tipos (mypy)
py -m mypy dahora_app/

# Lint (flake8)
py -m flake8 dahora_app/

# Formatação (black)
py -m black dahora_app/

# Release (Git LFS)
scripts\prepare_release_artifacts.ps1  # Preparar artefatos
scripts\push_release_lfs.ps1           # Push com LFS
```

---

## 📐 Padrões de Código

### Stack Tecnológica
- **Linguagem:** Python 3.12+
- **UI:** CustomTkinter (interface moderna)
- **System Tray:** pystray + Pillow
- **Hotkeys Globais:** keyboard
- **Notificações:** winotify (Windows)
- **Validação:** Pydantic v2
- **Criptografia:** DPAPI (pywin32)
- **Build:** PyInstaller

### Convenções de Nomenclatura
- **Variáveis/Funções:** `snake_case`
- **Classes:** `PascalCase`
- **Constantes:** `UPPER_SNAKE_CASE`
- **Arquivos:** `snake_case.py`
- **Handlers:** `*_handler.py`
- **Testes:** `test_*.py`

### Arquitetura
- **Camada UI:** `dahora_app/ui/` - Diálogos e menus
- **Camada Lógica:** `dahora_app/` - Managers e validators
- **Camada Handlers:** `dahora_app/handlers/` - Ações específicas
  - `CopyDateTimeHandler` - Copia timestamp + Ctrl+V automático
  - `ShowSearchHandler` - Diálogo de busca
  - `ShowSettingsHandler` - Diálogo de configurações
  - `QuitAppHandler` - Shutdown seguro
- **CallbackRegistry:** Orquestrador central de handlers com 8 Protocols
- **Validação:** `schemas.py` (Pydantic) + `hotkey_validator.py`

### Tratamento de Erros
- Use `logging` (nunca `print` em produção)
- Nunca logue dados sensíveis (senhas, tokens, PII)
- Fallback gracioso com defaults seguros

### Validação de Entrada
- Schemas Pydantic para configurações (`SettingsSchema`)
- `HotkeyValidator` para teclas de atalho
- Sanitização de prefixos (remove caracteres de controle)

---

## 🧪 Testes

**Framework:** pytest + pytest-cov + pytest-mock

**Suíte de testes:** `tests/` (pytest)
- Rode `py -m pytest tests/` para verificar o status no seu ambiente
- Arquivos principais: `test_schemas.py`, `test_hotkey_validator.py`, `test_single_instance.py`, `test_thread_sync.py`, `test_handlers.py`, `test_integration_handlers.py`

**Comandos:**
```powershell
py -m pytest                     # Todos os testes
py -m pytest -v                  # Verbose
py -m pytest --tb=short          # Traceback curto
py -m pytest --cov=dahora_app    # Com cobertura
py -m pytest -k "test_hotkey"    # Filtrar por nome
```

**Convenções:**
- Nomeie testes descritivamente: `test_should_validate_hotkey_format`
- Use fixtures do `conftest.py`
- Rode testes antes de PR e mudanças arriscadas

---

## 📝 Commits e Versionamento

### Formato de Commits (Conventional Commits)
```text
tipo(escopo): descrição

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade (incrementa MINOR em prod, PATCH em dev)
- `fix`: Correção de bug (incrementa PATCH)
- `docs`: Apenas documentação
- `style`: Formatação, sem mudança de lógica
- `refactor`: Refatoração sem mudar comportamento
- `test`: Adicionar/corrigir testes
- `chore`: Manutenção, configs, scripts
- `perf`: Melhorias de performance
- `ci`: Mudanças em CI/CD
- `build`: Sistema de build/dependências
- `revert`: Reverter commit anterior

**Breaking Changes:** Adicione `!` ou `BREAKING CHANGE:` no footer (MAJOR)

**Exemplos:**
```text
feat(auth): adicionar login com Google
fix(api): corrigir timeout em requisições
docs: atualizar README com instruções de deploy
feat!: remover suporte para Node 14
```

### Versionamento Semântico (SemVer)

**Formato:** `MAJOR.MINOR.PATCH` (ex: `0.1.5`)

- **MAJOR** (1.x.x): Produto pronto para mercado (lançamento oficial)
- **MINOR** (x.1.x): Versão estável com features completas
- **PATCH** (x.x.1): Incremento constante (commits, melhorias, fixes)

**Filosofia Conservadora:**
- Durante desenvolvimento: `0.0.x` (incrementa PATCH a cada commit relevante)
- Versão estável pronta: `0.1.0` (incrementa MINOR)
- Lançamento no mercado: `1.0.0` (incrementa MAJOR)
- Exemplo: `0.0.1` → `0.0.2` → `0.0.10` → `0.1.0` (estável) → `1.0.0` (release)

**Evite:**
- ❌ Pular versões (0.0.1 → 0.0.5 sem razão)
- ❌ Usar MAJOR antes do produto estar pronto para o mercado
- ❌ Usar MINOR antes de ter uma versão realmente estável

### CHANGELOG.md
Se o projeto mantiver changelog, use um padrão consistente (ex.: Keep a Changelog) e registre mudanças relevantes.

---

## 🔍 Debugging

1. **Logs:** Verifique `%APPDATA%/DahoraApp/dahora.log`
2. **Breakpoints:** Use VS Code (F5 com `main.py`)
3. **Debug manual:** `py debug_hotkey.py` (testa hotkeys)
4. **Testes isolados:** `py scripts/test_minimal.py`
5. **Inspecionar settings:** Abra `%APPDATA%/DahoraApp/settings.json`

---

## 📚 Documentação Adicional

### Docs do Projeto (em `docs/`)
- [architecture.md](docs/architecture.md) - Arquitetura detalhada
- [release-process.md](docs/release-process.md) - Processo de release e Git LFS
- [roadmap.md](docs/roadmap.md) - Plano de desenvolvimento
- [windows-setup.md](docs/windows-setup.md) - Configuração Python no Windows
- [CHANGELOG.md](CHANGELOG.md) - Registro oficial de mudanças por versão

### Modos de Trabalho (digite `/` no chat)

| Modo | Comando | Uso no Dahora |
|------|---------|---------------|
| Arquitetura | `/modo-arquiteto` | Design e planejamento |
| Backend | `/modo-backend` | Lógica, settings, storage |
| Debug | `/modo-depurador` | Bugs em handlers, hotkeys |
| DevOps | `/modo-devops` | Setup, CI/CD, release |
| Documentação | `/modo-documentacao` | Docs e textos do projeto |
| Frontend | `/modo-frontend` | UI da landing (HTML/CSS/JS) |
| Code Review | `/modo-code-review` | Revisões de PR e boas práticas |
| Git | `/modo-git` | Commits, releases |
| Qualidade | `/modo-qualidade` | Testes, cobertura, performance |
| Segurança | `/modo-seguranca` | Revisão OWASP e mitigação |

---

## ⚡ Quick Reference - Dahora App

| Ação | Comando |
|------|---------|
| Rodar app | `py main.py` |
| Rodar testes | `py -m pytest` |
| Build executável | `py build.py` |
| Verificar tipos | `py -m mypy dahora_app/` |
| Lint | `py -m flake8 dahora_app/` |
| Formatação | `py -m black dahora_app/` |
| Modo Segurança | `/modo-seguranca` |
| Modo Debug | `/modo-depurador` |
| Modo Arquitetura | `/modo-arquiteto` |
| Modo Backend | `/modo-backend` |
| Modo DevOps | `/modo-devops` |
| Modo Code Review | `/modo-code-review` |
| Modo Qualidade | `/modo-qualidade` |
| Modo Git | `/modo-git` |

---

**Última atualização:** 20 de janeiro de 2026  
**Versão do App:** 0.2.16  
**Status:** ✅ Projeto configurado com Prompt Files via `E:\Agents`  
**Testes:** suíte automatizada (pytest) | **Hacks tratados:** 14 de 14 (100%)
