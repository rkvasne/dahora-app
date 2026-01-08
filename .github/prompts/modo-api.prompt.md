---
name: api
description: Modo API - Design e desenvolvimento de APIs REST/GraphQL
agent: agent
---

# Modo API

> **Doc oficial:** https://restfulapi.net | https://swagger.io/specification/

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Verbos na URL** (`/getUser`) → métodos HTTP existem para isso
- ❌ **IDs sequenciais** → UUID previne enumeração
- ❌ **Sem versionamento** → `/api/v1/` desde o início
- ❌ **200 para erros** → status codes existem, use-os
- ❌ **Dados sensíveis em query params** → vazam em logs
- ❌ **Paginação ilimitada** → sempre tenha max server-side
- ❌ **Validação só no client** → server SEMPRE valida
- ❌ **CORS `*` em produção** → liste domínios

### ✅ SEMPRE

- ✅ **Recursos no plural** → `/users`, `/orders`
- ✅ **Status codes corretos** → 201 criado, 204 delete, 422 validação
- ✅ **Paginação em listas** → cursor ou offset
- ✅ **Rate limiting** → protege contra abuse
- ✅ **Validação com schema** → zod, joi na entrada
- ✅ **Erros estruturados** → `{ error: { code, message, details } }`
- ✅ **Documentação OpenAPI** → Swagger para contratos
- ✅ **Auth em todas rotas protegidas** → middleware

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| PUT para update parcial | Apaga campos | Use PATCH |
| Array vazio = 404 | Confunde "não existe" | 200 + `[]` |
| N+1 em relacionamentos | Lento | Include/expand params |
| Sem idempotência | Duplica recursos | Idempotency key |
| Erros genéricos | Debug impossível | Códigos específicos |
| Filtros no body | Não cacheável | Query params |

## 📋 Checklist de Endpoint

- [ ] Autenticação verificada?
- [ ] Input validado com schema?
- [ ] Status code correto?
- [ ] Erro estruturado se falhar?
- [ ] Rate limit aplicado?
- [ ] Documentado no OpenAPI?
- [ ] Teste de integração existe?
