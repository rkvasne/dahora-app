---
name: banco-dados
description: Modo Banco de Dados - Modelagem e otimização de bancos
agent: agent
---

# Modo Banco de Dados

> **Doc oficial:** https://www.postgresql.org/docs
> **Princípio:** Dados são o ativo mais valioso. Proteja com redundância e validação.

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **ALTER TABLE em produção sem backup** → pode perder dados
- ❌ **SELECT * em código** → quebra em schema change
- ❌ **Migration destrutiva sem rollback** → DROP COLUMN é irreversível
- ❌ **Query sem índice em WHERE/JOIN** → full scan em tabela grande
- ❌ **Concatenar SQL** → prepared statements apenas
- ❌ **NULL em campos obrigatórios** → `NOT NULL` é documentação viva
- ❌ **Logar queries com dados sensíveis** → senhas, tokens, PII

### ✅ SEMPRE

- ✅ **Índices em colunas filtradas** → WHERE, JOIN, ORDER BY
- ✅ **EXPLAIN ANALYZE** antes de deploy → entenda o plano
- ✅ **Migrations versionadas** → Prisma, Alembic, Flyway, goose
- ✅ **Backup testado** → backup sem teste não existe
- ✅ **snake_case para colunas** → padrão SQL
- ✅ **Plural para tabelas** → `users`, `orders`
- ✅ **UUID para IDs expostos** → não sequencial

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| N+1 queries | Lento, muitas requisições | JOIN ou eager loading |
| Índice em coluna errada | Não usado, query lenta | EXPLAIN ANALYZE |
| Transaction longa | Locks, deadlocks | Transações curtas |
| VARCHAR(255) para tudo | Desperdício ou truncamento | Tamanho adequado |
| Sem soft delete | Dados perdidos | `deleted_at` timestamp |
| Enum no banco | Difícil mudar | Tabela de lookup |

## 📋 Checklist de Migration

- [ ] Backup feito antes?
- [ ] Tem rollback possível?
- [ ] EXPLAIN ANALYZE nas queries afetadas?
- [ ] Índices necessários criados?
- [ ] Tempo de lock aceitável?
- [ ] Testado em staging com volume similar?

## 📋 Comandos de Diagnóstico

| Comando | Propósito |
|---------|-----------|
| `EXPLAIN ANALYZE` | Ver plano de execução |
| `pg_stat_statements` | Queries mais lentas |
| `pg_indexes` | Índices existentes |
| `\d+ tabela` | Estrutura detalhada |
