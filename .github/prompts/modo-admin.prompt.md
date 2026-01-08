---
name: admin
description: Modo Admin - Administração e configuração de sistemas
agent: agent
---

# Modo Admin

> **Princípio:** Configuração como código, não como clique.

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Secrets em código/git** → env vars ou secrets manager
- ❌ **Config manual em prod** → IaC (Terraform, Pulumi)
- ❌ **Sem backup testado** → backup não testado não existe
- ❌ **Acesso root compartilhado** → contas individuais + audit
- ❌ **Deploy sexta à tarde** → Murphy's Law
- ❌ **Sem rollback plan** → sempre tenha como voltar
- ❌ **Logs sem rotação** → disco cheio = sistema parado

### ✅ SEMPRE

- ✅ **Infraestrutura como código** → versionado, auditável
- ✅ **Princípio do menor privilégio** → só permissões necessárias
- ✅ **Monitoramento + alertas** → saiba antes do usuário
- ✅ **Runbook para incidentes** → não dependa de memória
- ✅ **Backup automático + verificado** → restore funciona?
- ✅ **Staging = prod** → mesmo ambiente, menos dados
- ✅ **Blue/green ou canary** → deploy sem downtime

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| Backup sem teste restore | Descobre que não funciona quando precisa | Teste mensal |
| Senha em .env commitado | Vazamento de credenciais | git-secrets, pre-commit hook |
| Só 1 pessoa sabe fazer deploy | Bus factor = 1 | Documentar, pair deploy |
| Logs em texto livre | Difícil pesquisar | JSON estruturado |
| Alerta para tudo | Alert fatigue, ignora todos | Só alerta acionável |
| SSL manual | Expira, site cai | Let's Encrypt automático |

## 📋 Checklist de Produção

- [ ] Variáveis de ambiente configuradas?
- [ ] HTTPS forçado?
- [ ] Backup automático ativo?
- [ ] Monitoramento configurado?
- [ ] Alertas testados?
- [ ] Rollback documentado?
- [ ] Acesso restrito (least privilege)?
- [ ] Logs centralizados?
