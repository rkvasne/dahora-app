---
description: Desenvolvimento de APIs, modelagem de banco de dados e lógica de servidor
---

# 🔙 Modo Backend (API & Dados)

> **Princípio:** Contratos claros (API) e dados íntegros (DB).

Este modo unifica o design de **APIs** (REST/GraphQL) e **Banco de Dados** (Schema/SQL).

---

## ⚠️ REGRAS DE OURO

### ❌ NUNCA
- ❌ **Verbos na URL** (`/getUser`) → use métodos HTTP
- ❌ **200 OK para erros** → use 4xx/5xx
- ❌ **N+1 Queries** → loop de queries no banco
- ❌ **Migrations destrutivas sem backup** → `DROP COLUMN` perigoso
- ❌ **Dados sensíveis em logs/URL** → PII, senhas, tokens
- ❌ **SQL Concatenado** → use Prepared Statements (SQL Injection)

### ✅ SEMPRE
- ✅ **Validação no Server** → nunca confie no frontend
- ✅ **Paginação** → nunca retorne `SELECT *` ilimitado
- ✅ **Índices em colunas de busca** → WHERE, JOIN, ORDER BY
- ✅ **Transações (ACID)** → para operações multi-tabela
- ✅ **Migrations versionadas** → código e banco sincronizados

---

## 🔌 1. API Design

### Checklist de Endpoint
- [ ] URL no plural (`/users`)?
- [ ] Métodos corretos (`GET`, `POST`, `PUT`, `DELETE`)?
- [ ] Status codes corretos (`201`, `204`, `400`, `401`, `404`)?
- [ ] Input validado (Zod/Joi/Pydantic)?
- [ ] Rate limiting configurado?

### Padrões REST
| Ação | Método | Status Sucesso |
|------|--------|----------------|
| Criar | POST | `201 Created` |
| Ler | GET | `200 OK` |
| Atualizar | PATCH | `200 OK` |
| Deletar | DELETE | `204 No Content` |

### Lei de Postel (Robustez)
> "Seja liberal no que aceita, e conservador no que envia."

**Na prática:**
- **Entrada (Liberal):** Se o cliente mandar JSON com campos extras irrelevantes, ignore-os em vez de quebrar (desde que os obrigatórios estejam lá). Aceite variações de formatação quando seguro (ex: trim em strings).
- **Saída (Conservador):** Siga a spec estritamente. Retorne JSON válido, status codes corretos e estrutura consistente.

---

## 🗄️ 2. Banco de Dados

### Checklist de Migration
- [ ] Backup feito antes?
- [ ] Migration tem rollback (down)?
- [ ] Campos novos têm `default` ou permitem `null` (para não quebrar)?
- [ ] Índices criados para chaves estrangeiras?

### Armadilhas de Performance
| Problema | Solução |
|----------|---------|
| **N+1** | Use `JOIN` ou `include` (eager loading) |
| **Full Table Scan** | Crie índice nas colunas do `WHERE` |
| **Connection Pool** | Configure limites no driver do DB |

---

## 🔗 Referências
- [REST API Tutorial](https://restfulapi.net)
- [PostgreSQL Docs](https://www.postgresql.org/docs)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
