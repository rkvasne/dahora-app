---
name: performance
description: Modo Performance - Otimização de performance
agent: agent
---

# Modo Performance

> **Doc oficial:** https://web.dev/performance
> **Princípio:** Não otimize sem medir. Meça, identifique, otimize, meça novamente.

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Otimizar sem medir** → pode piorar ou ser irrelevante
- ❌ **Cache sem invalidação** → dados stale
- ❌ **Otimização prematura** → complexidade sem ganho
- ❌ **Ignorar métricas reais** → Core Web Vitals, p95 latency

### ✅ SEMPRE

- ✅ **Medir antes e depois** → EXPLAIN, Profiler, Lighthouse
- ✅ **Identificar gargalo real** → não adivinhe
- ✅ **Otimizar o hot path** → 80/20, foque no crítico
- ✅ **Monitorar em produção** → usuários reais ≠ dev

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| Otimizar tudo | Complexidade sem ganho | Medir primeiro |
| Cache agressivo | Dados desatualizados | TTL adequado |
| Bundle grande | LCP ruim | Code splitting |
| N+1 queries | Latência alta | JOIN, eager loading |
| Imagens grandes | Core Web Vitals ruim | WebP, lazy loading |
| Sem índice | Query lenta | EXPLAIN ANALYZE |

## 📋 Métricas Chave

| Contexto | Métricas |
|----------|----------|
| Frontend | LCP, INP, CLS (Core Web Vitals) |
| Backend | p95 latency, throughput, error rate |
| Database | Query time, connection pool |
| Infra | CPU, memory, network I/O |

## 📋 Ferramentas por Contexto

| Contexto | Ferramenta |
|----------|------------|
| Web | Lighthouse, WebPageTest |
| React | React DevTools Profiler |
| Node.js | `--cpu-prof`, clinic.js |
| SQL | EXPLAIN ANALYZE, pg_stat_statements |
| Geral | APM (Datadog, NewRelic, Sentry) |

## 📍 Quando Aplicar / Quando Relaxar

### Aplique rigorosamente:
- Páginas públicas (SEO)
- Core user flows
- APIs de alto volume

### Pode relaxar:
- Admin interno
- Features de baixo uso
- Protótipos
