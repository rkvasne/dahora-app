# 🗺️ Roadmap — Dahora App

> Navegação: [Documentação](README.md) • [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

> **Última atualização:** 20 de janeiro de 2026 | **Versão atual:** v0.2.16

Roadmap de alto nível para próximas melhorias. Detalhes específicos devem ser documentados em [Issues](https://github.com/rkvasne/dahora-app/issues) e/ou [Discussions](https://github.com/rkvasne/dahora-app/discussions) no GitHub.

---

## Registro oficial de mudanças (por versão)

- O registro oficial do que foi alterado por versão fica em [CHANGELOG.md](../CHANGELOG.md).
- Auditoria, alinhamentos e dívida técnica (Jan/2026): [technical_audit_2026_01.md](technical_audit_2026_01.md).

## 🎯 Foco Atual

- Estabilidade e consistência da UI moderna (CustomTkinter)
- Padronização de documentação e processo de release
- Qualidade: testes, lint/typing quando fizer sentido

---

## 📌 Próximos Passos (Fase 2)

### Prioridade Média

| Item | Descrição | Esforço |
|------|-----------|--------|
| Padronização de documentação | Revisar e manter docs sincronizados por release | 1–2 dias |
| UX do editor de atalhos | Melhorar mensagens de conflito/validação | 1–2 dias |

### Prioridade Baixa (Backlog)

| Item | Descrição | Esforço |
|------|-----------|--------|
| Otimização Clipboard | Windows API events (vs polling) | Alto |
| Cache de Hotkeys | `lru_cache` para validação | Baixo |
| Context Manager | `__enter__`/`__exit__` em DahoraApp | Baixo |
| Diagramas | Arquitetura visual em architecture.md | Médio |
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

**Relatório detalhado:** Consulte `docs/technical_audit_2026_01.md` na pasta `docs/` para auditoria, alinhamentos e próximos passos.
