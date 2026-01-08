---
name: documentacao
description: Modo Documentação - Criação e manutenção de docs
agent: agent
---

# Modo Documentação

> **Princípio:** Documentação desatualizada é pior que nenhuma.

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Documentar implementação** → muda rápido, desatualiza
- ❌ **Duplicar código como doc** → código é a verdade
- ❌ **Doc sem dono** → ninguém atualiza
- ❌ **Screenshots de UI** → quebra em toda mudança visual
- ❌ **Versão hardcoded** → "installar v2.3.1" fica errado
- ❌ **Doc em lugar separado do código** → desatualiza
- ❌ **Tudo em um README gigante** → ninguém lê

### ✅ SEMPRE

- ✅ **README com quick start** → rodar em < 5 min
- ✅ **Doc perto do código** → inline comments, JSDoc
- ✅ **Decisões em ADRs** → não no README
- ✅ **Exemplos executáveis** → que você pode copiar e rodar
- ✅ **Link para doc oficial** → detalhes ficam lá
- ✅ **Data da última revisão** → saber se está fresco
- ✅ **CHANGELOG atualizado** → o que mudou entre versões

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| Doc em wiki separada | Ninguém atualiza | Doc no repo |
| README com tutorial completo | TL;DR | Quick start + links |
| Doc de API manual | Desatualiza | OpenAPI gerado |
| Screenshot de cada tela | Quebra em redesign | Apenas fluxos críticos |
| "Ver código para detalhes" | Não ajuda | Resumo do porquê |
| Doc sem exemplo | Abstrato demais | Código que roda |

## 📋 Estrutura de README

```markdown
# Nome do Projeto

Descrição em 1-2 linhas.

## Quick Start
[Como rodar em < 5 min]

## Requisitos
[O que precisa ter instalado]

## Configuração
[Env vars necessárias]

## Uso
[Exemplos básicos]

## Links
- [Doc completa](../../docs)
- [Contributing](../../CONTRIBUTING.md)
```

## 📋 O que Documentar (e o que não)

| Documentar | Não documentar |
|------------|----------------|
| Quick start | Código auto-explicativo |
| Decisões arquiteturais | Detalhes de implementação |
| APIs públicas | Métodos privados |
| Configuração | Óbvio do código |
