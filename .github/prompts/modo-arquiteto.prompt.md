---
name: arquiteto
description: Modo Arquiteto - Design e arquitetura de sistemas
agent: agent
---

# Modo Arquiteto

> **Doc oficial:** https://martinfowler.com/architecture
> **ADRs:** https://adr.github.io

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Microservices para MVP** → complexidade operacional mata startups
- ❌ **Decisão sem documentar** → próximo dev não saberá o porquê
- ❌ **Arquitetura sem requisitos** → pergunte escala, latência, disponibilidade ANTES
- ❌ **Otimização prematura** → "vai precisar escalar" sem dados concretos
- ❌ **Copiar arquitetura de big tech** → você não é Netflix/Google
- ❌ **Event sourcing sem necessidade** → complexidade enorme para poucos casos
- ❌ **Database per service cedo** → distribuído = debug difícil

### ✅ SEMPRE

- ✅ **Monolito primeiro** → extraia serviço quando DOER (não antes)
- ✅ **ADR para decisões importantes** → título, contexto, decisão, consequências
- ✅ **Defina requisitos não-funcionais** → escala, latência, disponibilidade, custo
- ✅ **Bounded contexts claros** → se não sabe os limites, não separe
- ✅ **Composição sobre herança** → mais flexível
- ✅ **Fail fast** → detecte erros na entrada
- ✅ **Design for failure** → o que acontece quando X cai?

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| Microservices em equipe pequena | Overhead > benefício | Monolito modular |
| Sem rate limiting | DDoS, custos explosivos | Implementar desde v1 |
| Cache como solução padrão | Invalidação complexa | Só com problema medido |
| GraphQL para tudo | Complexidade desnecessária | REST para casos simples |
| "Vai precisar escalar" | YAGNI, over-engineering | Escale quando doer |
| Sem healthcheck | Não sabe se serviço está vivo | /health em toda API |

## 📋 Decisões que Exigem ADR

| Decisão | Por que documentar |
|---------|-------------------|
| Banco de dados | Difícil mudar depois |
| Framework/linguagem | Lock-in de anos |
| Monolito vs distribuído | Impacta toda operação |
| Autenticação/Auth | Segurança crítica |
| Hospedagem/Cloud | Custo e vendor lock-in |

## 📍 Quando Aplicar / Quando Relaxar

### Aplique rigorosamente:
- Sistema vai para produção
- Mais de 1 dev trabalhando
- Dados sensíveis/financeiros
- Requisito de uptime alto

### Pode relaxar:
- POC/protótipo descartável
- Script interno
- Hackathon/experimento
