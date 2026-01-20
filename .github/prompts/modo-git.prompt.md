---
description: Versionamento, convenções de commit (Conventional Commits), estratégias de branching, merges e resolução de conflitos
---

# Modo Git

> **Doc oficial:** https://git-scm.com/doc
> **Conventional Commits:** https://conventionalcommits.org

---

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Amend em commit publicado** → reescreve história compartilhada
- ❌ **Force push em main/master** → quebra histórico de todos
- ❌ **Commit de secrets** → mesmo removido, fica no histórico
- ❌ **Commit sem mensagem descritiva** → "fix", "update", "wip"
- ❌ **Merge sem revisar conflitos** → código quebrado

### ✅ SEMPRE

- ✅ **Conventional Commits** → `tipo(escopo): descrição`
- ✅ **Commits atômicos** → uma mudança lógica por commit
- ✅ **Branch por feature** → `feat/nome-da-feature`
- ✅ **git status antes de commit** → verificar o que vai
- ✅ **git diff --staged** → revisar mudanças
- ✅ **Testes passando** → não commitar código quebrado

---

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| `git add .` cego | Commita lixo | `git add -p` ou revisar |
| Merge sem pull | Conflitos evitáveis | `git pull` antes |
| Branch desatualizada | Conflitos grandes | Rebase frequente |
| Secret commitado | Vazamento | git-secrets, .gitignore |
| Mensagem genérica | Histórico inútil | Conventional Commits |
| Force push | Perde trabalho de outros | `--force-with-lease` |

---

## 📋 Conventional Commits

| Tipo | Uso |
|------|-----|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação |
| `refactor` | Refatoração |
| `test` | Testes |
| `chore` | Manutenção |

**Formato:** `tipo(escopo): descrição curta`

---

## 📋 Branches Padrão

| Branch | Propósito |
|--------|-----------|
| `main`/`master` | Produção estável |
| `develop` | Integração |
| `feat/x` | Nova feature |
| `fix/x` | Correção |
| `hotfix/x` | Urgência em prod |

---

## 📍 Quando Aplicar / Quando Relaxar

### Aplique rigorosamente:
- Repositório compartilhado
- Código de produção
- Open source

### Pode relaxar:
- Projeto pessoal solo
- Experimentos locais

---

## 🔗 Referências

| Recurso | URL |
|---------|-----|
| Git Book | https://git-scm.com/book |
| Conventional Commits | https://conventionalcommits.org |
| git-secrets | https://github.com/awslabs/git-secrets |

---

*Versão: 0.3.2*

```
