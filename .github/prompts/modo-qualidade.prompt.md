---
name: qualidade
description: Modo Qualidade - Testes, QA e garantia de qualidade
agent: agent
---

# Modo Qualidade

> **Doc oficial:** https://testing-library.com | https://jestjs.io
> **Princípio:** Teste comportamento, não implementação.

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Testar implementação** → teste o QUE faz, não COMO
- ❌ **Mock de tudo** → perde valor do teste
- ❌ **Testes que quebram em refactor** → sinal de teste ruim
- ❌ **Coverage como meta única** → 100% coverage ≠ qualidade
- ❌ **Testes lentos ignorados** → teste lento = teste não rodado
- ❌ **Testes sem assertion** → `expect()` obrigatório
- ❌ **Copiar código de prod no teste** → teste vira espelho, não validação

### ✅ SEMPRE

- ✅ **Teste comportamento observável** → output, efeitos, UI
- ✅ **Um conceito por teste** → falhou = sabe o que quebrou
- ✅ **Nomes descritivos** → `should_reject_invalid_email` não `test1`
- ✅ **Arrange-Act-Assert** → setup, execução, verificação
- ✅ **Testes rápidos** → <100ms por teste unitário
- ✅ **Teste o caminho triste** → erros, edge cases, limites
- ✅ **Testes em CI** → PR não merga se teste falha

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| Testar método privado | Quebra em refactor | Teste via interface pública |
| Snapshot de tudo | Aceita mudança sem revisar | Snapshot só para regressão visual |
| Mock de Date/Math.random | Flaky tests | Injetar dependência |
| Dados de teste hardcoded | Teste passa por coincidência | Factory/fixture com variação |
| Ordem de testes importa | Flaky, difícil debugar | Testes isolados |
| `any` em mocks | Perde type safety | Mock tipado |

## 📋 Pirâmide de Testes

| Tipo | Quantidade | Velocidade | Custo |
|------|------------|------------|-------|
| **E2E** | Poucos | Lentos | Alto |
| **Integração** | Alguns | Médios | Médio |
| **Unitário** | Muitos | Rápidos | Baixo |

**Regra:** Mais testes na base (unitário), menos no topo (E2E).

## 📋 O que Testar (Prioridade)

| Prioridade | O que | Por quê |
|------------|-------|---------|
| 🔴 Alta | Auth, pagamento, dados | Risco de negócio |
| 🟡 Média | Regras de negócio | Lógica crítica |
| 🟢 Baixa | UI simples, CRUD básico | Baixo risco |
