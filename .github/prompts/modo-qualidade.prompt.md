---
description: Testes, QA, performance e otimização de código
---

# 💎 Modo Qualidade (Testes & Performance)

> **Princípio:** Se não tem teste, está quebrado. Se não mediu, não é lento.

Este modo unifica **Garantia de Qualidade (QA)** e **Engenharia de Performance**.

---

## ⚠️ REGRAS DE OURO

### ❌ NUNCA
- ❌ **Testar implementação** → teste o COMPORTAMENTO
- ❌ **Otimizar sem medir** → "acho que está lento" não vale
- ❌ **Mock de tudo** → teste perde valor real
- ❌ **Ignorar testes lentos/flaky** → corrija ou delete
- ❌ **Otimização prematura** → código complexo sem ganho real

### ✅ SEMPRE
- ✅ **Arrange-Act-Assert** → estrutura padrão de teste
- ✅ **Caminho triste** → teste erros e edge cases
- ✅ **Medir antes e depois** → use Profiler/Lighthouse
- ✅ **Identificar gargalo real** → CPU? Memória? I/O?
- ✅ **Testes em CI** → bloqueie PR se quebrar

---

## 🧪 1. Estratégia de Testes

### Pirâmide de Testes
1.  **Unitários (Base):** Rápidos, testam funções isoladas. Muitos.
2.  **Integração (Meio):** Testam API+DB, Componente+Store. Alguns.
3.  **E2E (Topo):** Testam fluxo completo do usuário. Poucos.

### Checklist de Qualidade
- [ ] Testes passam no CI?
- [ ] Coverage cobre regras de negócio críticas?
- [ ] Inputs inválidos são rejeitados?
- [ ] Erros são tratados graciosamente?

### Teoria das Janelas Quebradas
> "Uma janela quebrada, se não consertada, passa a ideia de que ninguém se importa, levando a mais vandalismo."

**Na prática (Dívida Técnica):**
- **Corrija imediatamente:** Um teste falhando ("flaky"), um warning de lint ou um erro "ignorado" no console.
- **Tolerância Zero:** Se você deixar passar "só hoje", semana que vem o código estará um caos. Mantenha o padrão alto.

---

## ⚡ 2. Engenharia de Performance

### Onde Otimizar (Regra 80/20)
Foque nos 20% do código que executam 80% do tempo (hot paths).

### Ferramentas & Métricas
| Contexto | Ferramenta | Métricas Chave |
|----------|------------|----------------|
| **Web** | Lighthouse | LCP, CLS, INP (Core Web Vitals) |
| **Backend** | APM / Profiler | Latência p95, Throughput |
| **DB** | EXPLAIN ANALYZE | Tempo de execução, Rows scan |

### Checklist de Performance
- [ ] N+1 queries eliminadas?
- [ ] Índices de banco verificados?
- [ ] Imagens otimizadas (WebP, Lazy Load)?
- [ ] Caching configurado (Redis/CDN) onde faz sentido?
- [ ] Bundle size do frontend auditado?

---

## 🔗 Referências
- **Guias Internos:**
  - [Jest (Unitário)](../../rules/tecnologias/testing/jest.md)
  - [Vitest (Moderno)](../../rules/tecnologias/testing/vitest.md)
  - [Playwright (E2E)](../../rules/tecnologias/testing/playwright.md)
- **Externos:**
  - [Testing Library](https://testing-library.com)
  - [Web Vitals](https://web.dev/vitals)
