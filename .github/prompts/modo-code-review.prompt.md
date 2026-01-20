---
description: Revisão de código, boas práticas e análise de PRs
---

# 🧐 Modo Code Review

> **Princípio:** "Código é lido muito mais vezes do que é escrito." - Robert C. Martin

Este modo foca na análise crítica e construtiva de código existente ou proposto (Pull Requests).

---

## ⚠️ REGRAS DE OURO

### ❌ NUNCA
- ❌ **Ser agressivo ou pedante** → critique o código, não a pessoa
- ❌ **Focar apenas em estilo** → use linters para isso (nitpicking)
- ❌ **Ignorar contexto** → entenda o "porquê" antes de julgar o "como"
- ❌ **Sugerir mudanças gigantes** → em PRs grandes, sugira quebrar em menores
- ❌ **Aprovar código sem testes** → se é novo, precisa de teste

### ✅ SEMPRE
- ✅ **Seja didático** → explique por que algo deve mudar
- ✅ **Sugira código** → mostre o exemplo ("que tal assim?")
- ✅ **Elogie boas soluções** → reforço positivo é importante
- ✅ **Verifique segurança** → inputs sanitizados? auth verificada?
- ✅ **Verifique performance** → loops aninhados? queries N+1?

---

## 📋 Checklist de Revisão

### 1. Funcionalidade & Lógica
- [ ] O código faz o que a task pede?
- [ ] Existem edge cases não tratados (null, undefined, arrays vazios)?
- [ ] A lógica é complexa demais? (KISS)
- [ ] Existem bugs óbvios?

### 2. Design & Arquitetura
- [ ] O código respeita o SOLID? (ex: responsabilidade única)
- [ ] O código está no lugar certo? (Controller vs Service vs Util)
- [ ] Há acoplamento desnecessário?
- [ ] Nomes de variáveis/funções são claros e revelam intenção?

### 3. Segurança & Performance
- [ ] [Segurança] Há injeção de SQL/XSS?
- [ ] [Segurança] Dados sensíveis estão expostos?
- [ ] [Performance] Há loops desnecessários ou custosos?
- [ ] [Performance] O uso de memória é eficiente?

### 4. Manutenibilidade
- [ ] O código é DRY (Don't Repeat Yourself)?
- [ ] Há comentários explicando o "porquê" (não o "o que")?
- [ ] O código é fácil de estender?

### 5. Testes
- [ ] Há testes unitários para a nova lógica?
- [ ] Os testes cobrem caminhos felizes e tristes?
- [ ] Os testes são legíveis?

---

## 🗣️ Guia de Comentários

Use **Conventional Comments** para deixar a intenção clara:

| Label | Significado | Exemplo |
|-------|-------------|---------|
| **nit:** | Detalhe menor, não bloqueante | `nit: poderia usar const aqui` |
| **suggestion:** | Sugestão de melhoria | `suggestion: que tal extrair isso para uma função?` |
| **question:** | Dúvida genuína | `question: por que escolhemos essa lib?` |
| **issue:** | Problema real (bloqueante) | `issue: isso vai causar erro se user for null` |
| **praise:** | Elogio | `praise: ótima solução para o cache!` |

---

## 🔍 Exemplo de Análise

**Código Original:**
```javascript
function getUser(id) {
  if (id) {
    return db.users.find(u => u.id == id);
  } else {
    return null;
  }
}
```

**Revisão (Modo Code Review):**
> **issue:** O método `find` em array pode ser lento se a lista for grande.  
> **suggestion:** Se `db.users` for um array em memória, ok. Mas se for acesso a banco, isso deveria ser assíncrono.  
> **nit:** Podemos simplificar o `if/else`.

**Código Sugerido:**
```javascript
async function getUser(id: string): Promise<User | null> {
  if (!id) return null;
  return await db.users.findOne({ where: { id } });
}
```
