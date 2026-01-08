# Copilot Instructions - Dahora App

> Arquivo de configuração automática para GitHub Copilot e agentes de IA.
> Sincronizado com: `AGENTS.md`, `.github/prompts/`

---

## 📌 Referência Rápida de Modos

### Como Usar Prompt Files

Os modos estão disponíveis como **Prompt Files** em `.github/prompts/`. 

✅ **COMO USAR NO VS CODE:**
```
No chat do Copilot, digite / e selecione o modo:

/depurador          - Debug e correção de bugs
/seguranca          - Segurança de aplicações (OWASP)
/arquiteto          - Design e arquitetura
/banco-dados        - Modelagem e otimização de bancos
/frontend           - UI, componentes (React, CSS)
/api                - Design de APIs REST/GraphQL
/performance        - Otimização de performance
/documentacao       - Criação e manutenção de docs
/git                - Versionamento e commits
/admin              - Administração e deploy
/planejador         - Planejamento e estimativas
/qualidade          - Testes e QA
/multi-tenant       - Isolamento SaaS
/depurador-web      - Debug frontend específico
/depurador-backend  - Debug APIs/servidor
/depurador-devops   - Debug CI/CD e infra
/depurador-mobile   - Debug React Native
```

**Referência completa de modos disponíveis:**

| Contexto | Comando | Descrição |
|----------|---------|-----------|
| 🔒 Segurança | `/seguranca` | Auth, OWASP, vulnerabilidades |
| 🗄️ Banco de Dados | `/banco-dados` | SQL, migrations, índices |
| 🏗️ Arquitetura | `/arquiteto` | Design, patterns, ADRs |
| 🐛 Debugging | `/depurador` | Bugs, erros, fixes |
| 🎨 Frontend/UI | `/frontend` | React, CSS, componentes |
| 🔌 API | `/api` | REST, endpoints, validação |
| ⚡ Performance | `/performance` | Otimização, cache, métricas |
| 📋 Documentação | `/documentacao` | README, docs, guias |
| 🔀 Git | `/git` | Commits, branches, merges |
| 🛠️ Admin | `/admin` | Deploy, config, infra |
| 📊 Planejador | `/planejador` | Estimativas, priorização |
| ✅ Qualidade | `/qualidade` | Testes, QA, coverage |
| 🏢 Multi-tenant | `/multi-tenant` | SaaS, isolamento, RLS |

---

## 📋 Regras Globais (APLICÁVEIS A TUDO)

### ⚠️ REGRA MÁXIMA DE ALTERAÇÃO
**❌ NUNCA altere código que não foi explicitamente solicitado.**
- ✅ Edite APENAS o que for claramente pedido
- ✅ Pergunte antes se houver dúvida sobre escopo
- ❌ NÃO refatore, otimize ou "melhore" sem solicitação

### 🎯 REGRA DE HONESTIDADE
**❌ NUNCA invente informações ou faça afirmações sem base factual.**
- ✅ Diga "não sei" quando não souber
- ✅ Use "geralmente", "comumente" em vez de "sempre", "todos"
- ✅ Cite fonte em afirmações estatísticas

### 🚫 REGRA ANTI-CONCORDÂNCIA AUTOMÁTICA
**❌ NUNCA concorde automaticamente sem analisar primeiro.**
- ✅ ANALISE primeiro, responda depois
- ✅ Se o usuário estiver errado, explique educadamente por quê
- ✅ Apresente trade-offs e alternativas

---

## 🖥️ Ambiente do Projeto

- **Sistema Operacional:** Windows 11
- **Idioma de Resposta:** Português (pt-BR)
- **Modelo de IA:** Informe sempre qual modelo está usando
- **Stack Principal:** Python (Dahora App com PyQt/Tkinter)

---

## 📁 Estrutura do Projeto

```
dahora-app/
├── AGENTS.md                    # Instruções principais
├── main.py                      # Entrada da aplicação
├── build.py                     # Script de build
├── .github/
│   └── copilot-instructions.md  # Este arquivo
├── dahora_app/
│   ├── __init__.py
│   ├── handlers/                # Lógica de eventos
│   ├── ui/                      # Componentes de interface
│   ├── hotkeys.py               # Gerenciar hotkeys
│   ├── settings.py              # Configurações
│   └── ...
├── tests/                       # Testes unitários
├── docs/                        # Documentação
│   ├── ARCHITECTURE.md          # Design da aplicação
│   ├── RELEASE.md               # Processo de release
│   └── ...
└── scripts/                     # Scripts utilitários
```

---

## 🛠️ Comandos Principais do Projeto

```bash
# Desenvolvimento
python main.py                  # Executar aplicação
python -m pytest                # Rodar testes
python -m mypy dahora_app/      # Verificar tipos

# Build
python build.py                 # Gerar executável
python scripts/prepare_release_artifacts.ps1  # Preparar release

# Limpeza
python scripts/limpar_cache_icones.ps1  # Limpar cache
```

---

## 📐 Padrões de Código

### Convenções
- **Variáveis/Funções:** `snake_case`
- **Classes:** `PascalCase`
- **Constantes:** `UPPER_SNAKE_CASE`
- **Arquivos:** `snake_case.py`

### Tratamento de Erros
- Sempre use logging (não print em prod)
- Nunca logue dados sensíveis (senhas, tokens, PII)
- Validar INPUT do usuário no backend sempre

### Validação
- Use schemas/dataclasses para validação
- Validate no server-side sempre (nunca confie apenas em frontend)
- Rejeite dados inválidos explicitamente

---

## 🧪 Testes

- Rode testes antes de fazer PR
- Nomeie testes descritivamente (behavior-driven)
- Cobertura mínima: funcionalidades críticas

---

## 📝 Commits (Conventional Commits)

```
tipo(escopo): descrição

[corpo opcional]
[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `test`: Testes
- `chore`: Manutenção
- `perf`: Performance
- `refactor`: Refatoração

**Exemplo:**
```
feat(hotkeys): adicionar validação de hotkeys duplicados
fix(settings): corrigir bug de carregamento de configurações
docs: atualizar guia de instalação
```

---

## 🔒 Segurança (CRÍTICO)

**Use o modo:** `/seguranca`

### Regras de Ouro
- ❌ NUNCA concatenar SQL → prepared statements
- ❌ NUNCA secrets no código → env vars ou secrets manager
- ❌ NUNCA confiar input do usuário → validar SEMPRE
- ✅ SEMPRE validar no backend
- ✅ SEMPRE usar HTTPS em produção
- ✅ SEMPRE logar eventos sensíveis (sem revelar dados)

---

## 🔍 Debugging

1. Verifique os logs da aplicação
2. Use breakpoints no VS Code
3. Inspecione o estado das variáveis
4. Verifique a documentação em `docs/`

---

## 📚 Documentação Complementar

- **Arquitetura:** [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md)
- **Release:** [`docs/RELEASE.md`](../docs/RELEASE.md)
- **Desenvolvimento:** [`docs/DEVELOPMENT_HISTORY.md`](../docs/DEVELOPMENT_HISTORY.md)
- **Setup Windows/Python:** [`docs/WINDOWS_PYTHON_SETUP.md`](../docs/WINDOWS_PYTHON_SETUP.md)

---

## 🎯 Workflow Recomendado para Agentes

1. **Research/Analysis** → Leia `AGENTS.md`, `ARCHITECTURE.md`
2. **Planning** → Use modo relevante (`/planejador`, `/arquiteto`)
3. **Implementation** → Siga padrões do projeto
4. **Testing** → Rode testes antes de finalizar (`/qualidade`)
5. **Commit** → Use Conventional Commits (`/git`)

---

## ⚡ Quick Reference

| Ação | Comando |
|------|---------|
| Segurança | `/seguranca` |
| Banco de dados | `/banco-dados` |
| Arquitetura | `/arquiteto` |
| Debug | `/depurador` |
| Frontend/UI | `/frontend` |
| API | `/api` |
| Performance | `/performance` |
| Docs | `/documentacao` |
| Git | `/git` |
| Admin | `/admin` |
| Planejamento | `/planejador` |
| Qualidade | `/qualidade` |
| Multi-tenant | `/multi-tenant` |

---

**Última atualização:** 8 de janeiro de 2026

**Compatível com:** VS Code + Copilot Chat  
**Prompt Files em:** `.github/prompts/`
