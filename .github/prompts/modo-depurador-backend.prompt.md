---
name: depurador-backend
description: Modo Depurador Backend - Debug de APIs e servidor (Node, Python)
agent: agent
---

# Modo Depurador Backend

> **Doc oficial:** https://nodejs.org/en/docs/guides/debugging-getting-started

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Debug sem reproduzir** → sem reprodução, sem solução
- ❌ **`console.log` em produção** → use logger estruturado
- ❌ **Ignorar stack trace** → a resposta geralmente está ali
- ❌ **Fix + refactor junto** → commits separados
- ❌ **Assumir causa sem dados** → prove com logs/traces

### ✅ SEMPRE

- ✅ **Logs estruturados** → JSON com requestId, userId
- ✅ **EXPLAIN ANALYZE** para queries lentas
- ✅ **Verificar N+1** → sintoma: muitas queries similares
- ✅ **Testar auth em staging** → diferentes roles/tokens
- ✅ **Verificar env vars** → diferença entre ambientes

## 🚨 Causas Comuns

| Sintoma | Causa Provável | Verificar |
|---------|----------------|-----------|
| 500 Internal Error | Exception não tratada | Logs do servidor |
| Resposta lenta (>500ms) | N+1, query sem índice | EXPLAIN ANALYZE |
| 401/403 inesperado | Token expirado, role errado | JWT decode, permissions |
| Timeout | Query longa, external API | Connection pool, timeouts |
| Memory crash | Leak, buffer grande | Heap snapshot, conexões |

## 📋 Processo de Debug

1. Reproduzir com request específico
2. Coletar logs + stack trace
3. Verificar diferenças de ambiente
4. Isolar componente (API? DB? External?)
5. EXPLAIN se for query
6. Fix mínimo + teste

## 📋 Ferramentas por Stack

| Stack | Ferramenta |
|-------|------------|
| Node.js | `--inspect`, VS Code debugger |
| Python | pdb, VS Code debugger |
| SQL | EXPLAIN ANALYZE, pg_stat_statements |
| HTTP | Postman, curl, httpie |
| Logs | grep, jq, log aggregator |
