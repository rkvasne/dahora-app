---
description: Planejamento técnico, design de sistemas, arquitetura e quebra de tarefas
---

# 🏗️ Modo Arquiteto (Design & Planejamento)

> **Princípio:** Pense antes de codar. Entenda O QUE (Planejamento) e COMO (Arquitetura).

Este modo unifica o **Planejamento** (Roadmap, Tarefas) e a **Arquitetura** (Design Patterns, Trade-offs).

---

## ⚠️ REGRAS DE OURO

### ❌ NUNCA
- ❌ **Estimar sem entender escopo** → garantia de erro
- ❌ **Microservices para MVP** → complexidade operacional mata
- ❌ **Decisão sem documentar (ADR)** → por que escolhemos X?
- ❌ **Otimização prematura** → escale quando doer
- ❌ **"Uns 2-3 dias"** → range vago = não entendeu a tarefa

### ✅ SEMPRE
- ✅ **Monolito modular primeiro** → extraia quando necessário
- ✅ **Critérios de aceite claros** → defina "pronto"
- ✅ **Quebre em tarefas pequenas** → 2h a 1 dia
- ✅ **Defina requisitos não-funcionais** → latência, custo, escala
- ✅ **Buffer de 30%** → imprevistos acontecem

---

## 📅 1. Planejamento (O Quê & Quando)

### Checklist de Tarefa
- [ ] Escopo definido por escrito?
- [ ] Critérios de aceite listados?
- [ ] Dependências identificadas?
- [ ] Quebrado em subtarefas pequenas?
- [ ] Prioridade definida (P0/P1/P2)?

### Matriz de Priorização
| Impacto / Esforço | Baixo Esforço | Alto Esforço |
|-------------------|---------------|--------------|
| **Alto Impacto** | 🔥 Fazer AGORA | 📅 Planejar bem |
| **Baixo Impacto** | ✅ Quick wins | ❌ Descartar |

---

## 🏛️ 2. Arquitetura (Como & Onde)

### Decisões Críticas (ADR)
Documente sempre que decidir sobre:
1. **Banco de Dados:** SQL vs NoSQL?
2. **Linguagem/Framework:** Node vs Python?
3. **Estrutura:** Monolito vs Microservices?
4. **Auth:** JWT vs Session?

### Lei de Conway (Estrutura)
> "Organizações que projetam sistemas são restritas a produzir designs que são cópias das estruturas de comunicação dessas organizações."

**Na prática:**
- **Monolito vs Microservices:** Se você tem um time pequeno (3-5 pessoas), faça um Monolito. Microservices exigem times independentes para cada serviço.
- **Alinhamento:** A arquitetura do software deve refletir como o time está organizado, senão haverá fricção constante.

### Lei de Gall (Simplicidade)
> "Um sistema complexo que funciona é invariavelmente encontrado como tendo evoluído de um sistema simples que funcionava."

**Na prática:**
- Comece simples (MVP funcional).
- Não tente construir o sistema "perfeito" e complexo do zero.
- Evolua a complexidade apenas quando necessário.

### Armadilhas de Design
| Armadilha | Solução |
|-----------|---------|
| **Over-engineering** | Use YAGNI (You Ain't Gonna Need It) |
| **Database per service cedo** | Use monolito com schemas separados |
| **Cache agressivo** | Só use cache se mediu o gargalo |
| **Lock-in de Cloud** | Use containers/Docker para portabilidade |

---

## 🔗 Referências
- [Martin Fowler Architecture](https://martinfowler.com/architecture)
- [Shape Up (Basecamp)](https://basecamp.com/shapeup)
- [ADR Templates](https://adr.github.io)
