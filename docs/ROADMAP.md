# 🗺️ Roadmap — Dahora App

> Navegação: [Documentação](README.md) • [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

> **Última atualização:** 12 de janeiro de 2026 | **Versão atual:** v0.2.11

Roadmap de alto nível para próximas melhorias. Detalhes específicos devem ser documentados em [Issues](https://github.com/rkvasne/dahora-app/issues) e/ou [Discussions](https://github.com/rkvasne/dahora-app/discussions) no GitHub.

---

## ✅ Concluído (v0.2.11 - Janeiro 2026)

### Arquitetura e Qualidade

| Item | Descrição | Status |
|------|-----------|--------|
| Migração para Handlers | Callbacks migrados para CallbackRegistry | ✅ Completo |
| Consolidação de Callbacks | `_sync_all_components()` centralizado | ✅ Completo |
| UI Root Thread-Safety | Lock implementado em `_ensure_ui_root()` | ✅ Completo |
| Type Hints (Protocols) | 8 Protocols em `callback_manager.py` | ✅ Completo |
| Single Instance | 21 testes, implementação completa | ✅ Verificado |
| Limpeza de Código | flake8 verificado, sem imports não usados | ✅ Verificado |

### Handlers Implementados

| Handler | Funcionalidade | Status |
|---------|----------------|--------|
| `CopyDateTimeHandler` | Ctrl+V automático | ✅ Completo |
| `ShowSearchHandler` | Diálogo de busca (UI moderna) | ✅ Completo |
| `ShowSettingsHandler` | Diálogo de configurações | ✅ Completo |
| `QuitAppHandler` | Shutdown seguro | ✅ Completo |

### Documentação

- ✅ `ARCHITECTURE.md` - Seções 3.7 (Handlers) e 3.8 (Otimizações) adicionadas
- ✅ `HACKS.md` - Tabela de status atualizada
- ✅ `ANALISE_PROJETO.md` - Relatório completo de melhorias

### Métricas

- **Testes:** 267 passando
- **Cobertura:** Handlers, schemas, validadores
- **Hacks resolvidos:** 8 de 14 (57%)

---

## 🎯 Foco Atual

- Estabilidade e consistência da UI moderna (CustomTkinter)
- Padronização de documentação e processo de release
- Qualidade: testes, lint/typing quando fizer sentido

---

## 📌 Próximos Passos (Fase 2)

### Prioridade Média

| Item | Descrição | Esforço |
|------|-----------|---------|
| Validação Duplicada | Remover fallback manual gradualmente | 2 dias |
| Métodos `*_legacy()` | Remover após validação extensiva | 1 dia |

### Prioridade Baixa (Backlog)

| Item | Descrição | Esforço |
|------|-----------|---------|
| Otimização Clipboard | Windows API events (vs polling) | Alto |
| Cache de Hotkeys | `lru_cache` para validação | Baixo |
| Context Manager | `__enter__`/`__exit__` em DahoraApp | Baixo |
| Diagramas | Arquitetura visual em ARCHITECTURE.md | Médio |
| Timestamps UTC | Avaliação de impacto | Baixo |

---

## 🔮 Visão Futura (v0.3.x)

- Melhorar observabilidade (logs, diagnósticos de hotkeys)
- Melhorar UX do editor de atalhos e mensagens de conflito
- Possível suporte a temas customizáveis
- Internacionalização (i18n) se houver demanda

---

## ✅ Como Contribuir

- Abra uma issue com:
  - problema/objetivo
  - passos para reproduzir (se bug)
  - comportamento esperado vs atual
  - versão do app

---

## 📎 Notas

Este arquivo substitui o antigo checklist longo de melhorias, que era útil no início do projeto, mas ficou difícil de manter sincronizado com o estado real do código.

**Relatório detalhado:** Consulte `ANALISE_PROJETO.md` na raiz do projeto para análise completa das implementações de Janeiro 2026.
