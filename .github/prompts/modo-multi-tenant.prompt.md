---
name: multi-tenant
description: Modo Multi-Tenant - Isolamento de dados entre tenants (SaaS)
agent: agent
---

# Modo Multi-Tenant

> **Doc oficial Supabase RLS:** https://supabase.com/docs/guides/auth/row-level-security
> **Princípio:** Vazamento de dados entre tenants = fim do negócio.

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Filtro de tenant só no backend** → use RLS no banco também
- ❌ **Confiar em tenant_id do frontend** → derive do token/session
- ❌ **Queries sem WHERE tenant_id** → RLS como safety net
- ❌ **Lógica de isolamento espalhada** → centralize em middleware/RLS
- ❌ **Testes sem trocar tenant** → teste cruzamento de dados
- ❌ **Admin vê tudo por padrão** → admin também precisa de contexto

### ✅ SEMPRE

- ✅ **RLS habilitado em todas tabelas com dados de tenant**
- ✅ **tenant_id derivado do auth (não do request)**
- ✅ **Teste de isolamento automatizado** → "tenant A não vê dados de B"
- ✅ **Índice em tenant_id** → performance em queries
- ✅ **Audit log com tenant_id** → quem fez o quê, onde
- ✅ **Default deny** → sem tenant = sem acesso

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| Esquecer RLS em nova tabela | Vazamento de dados | Checklist de PR |
| Cache sem tenant key | Tenant A vê cache de B | `cache_key = tenant_id:resource` |
| Filtro só no SELECT | UPDATE/DELETE sem filtro | RLS em todas operações |
| Jobs assíncronos sem contexto | Processa dados errados | Passar tenant_id no job |
| Busca global (search) | Retorna dados de outros | Filtro no índice de busca |
| Uploads sem isolamento | Arquivos acessíveis por URL | Paths com tenant_id |

## 📋 Checklist Multi-Tenant

- [ ] RLS habilitado em tabelas com dados de tenant?
- [ ] tenant_id vem do auth, não do request?
- [ ] Índice em tenant_id em tabelas grandes?
- [ ] Teste automatizado de isolamento?
- [ ] Jobs/workers têm contexto de tenant?
- [ ] Cache inclui tenant na key?
- [ ] Uploads isolados por tenant?
- [ ] Busca/search filtrada por tenant?

## 🏗️ Estratégias de Isolamento

| Estratégia | Isolamento | Custo | Quando usar |
|------------|------------|-------|-------------|
| **Coluna tenant_id** | Lógico (RLS) | Baixo | Maioria dos casos |
| **Schema por tenant** | Físico (schema) | Médio | Compliance específico |
| **DB por tenant** | Total | Alto | Enterprise, regulação |

**Recomendação:** Comece com tenant_id + RLS. Mude só se compliance exigir.
