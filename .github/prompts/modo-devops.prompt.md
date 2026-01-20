---
description: Infraestrutura, CI/CD, deploy, containers e configuração de ambiente
---

# 🚀 Modo DevOps (Infra & Admin)

> **Princípio:** Configuração como código (IaC). Automatize tudo.

Este modo cobre **Infraestrutura**, **CI/CD** e **Administração de Sistemas**.

---

## ⚠️ REGRAS DE OURO

### ❌ NUNCA
- ❌ **Secrets em código/git** → use Vault, AWS Secrets, .env
- ❌ **Deploy manual em prod** → use Pipelines (CI/CD)
- ❌ **Configuração "Snowflake"** → servidores únicos e manuais
- ❌ **Ignorar logs de erro** → configure alertas
- ❌ **Rodar como root** → use usuários restritos

### ✅ SEMPRE
- ✅ **Infraestrutura como Código (IaC)** → Terraform, Dockerfile
- ✅ **Ambientes paritários** → Staging igual a Prod
- ✅ **Backup testado** → restore deve funcionar
- ✅ **Logs estruturados** → JSON para fácil busca
- ✅ **Princípio do menor privilégio** → permissão mínima necessária

---

## 🛠️ 1. Pipelines & CI/CD

### Checklist de Pipeline
- [ ] Lint e Testes rodam antes do deploy?
- [ ] Secrets injetadas via variáveis de ambiente?
- [ ] Build é determinístico (mesmo código = mesmo artefato)?
- [ ] Rollback é possível (reverter versão)?

### Estágios Comuns
1. **Build/Test:** Compila, linta e testa.
2. **Release:** Gera imagem Docker ou artefato.
3. **Deploy Staging:** Automático.
4. **Deploy Prod:** Aprovação manual ou Blue/Green.

---

## 🐳 2. Containers & Infra

### Checklist de Produção
- [ ] HTTPS (TLS) ativo e válido?
- [ ] Banco de dados tem backup automático?
- [ ] Logs estão sendo persistidos/enviados?
- [ ] Monitoramento (CPU/RAM) ativo?
- [ ] Alertas de downtime configurados?

### Ferramentas Comuns
- **Container:** Docker, Podman.
- **Orquestração:** Kubernetes, ECS, Docker Swarm.
- **IaC:** Terraform, Ansible, Pulumi.
- **CI/CD:** GitHub Actions, GitLab CI.

---

## 🔗 Referências
- [12 Factor App](https://12factor.net)
- [DevOps Roadmap](https://roadmap.sh/devops)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
