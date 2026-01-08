---
name: seguranca
description: Modo Segurança - Segurança de aplicações (OWASP)
agent: agent
---

# Modo Segurança

> **Doc oficial:** https://owasp.org | https://cheatsheetseries.owasp.org
> **Princípio:** Defense in depth - múltiplas camadas de proteção.

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Verificar auth só no frontend** → backend SEMPRE valida
- ❌ **Concatenar SQL** → prepared statements apenas
- ❌ **Secrets no código** → env vars ou secrets manager
- ❌ **MD5/SHA1 para senhas** → bcrypt/argon2 apenas
- ❌ **Confiar em input do usuário** → validar TUDO server-side
- ❌ **CORS com `*` em prod** → liste domínios específicos
- ❌ **Logar dados sensíveis** → nunca senhas, tokens, PII
- ❌ **Deserializar input não confiável** → JSON.parse de user = perigo

### ✅ SEMPRE

- ✅ **Deny by default** → permissão explícita, nunca implícita
- ✅ **Princípio do menor privilégio** → só o necessário
- ✅ **Validação com schema** → zod, joi antes de processar
- ✅ **Rate limiting** → login, API, forms
- ✅ **HTTPS em produção** → sem exceção
- ✅ **Headers de segurança** → CSP, X-Frame-Options, etc
- ✅ **Audit trail** → quem fez o quê, quando
- ✅ **`npm audit` no CI** → bloquear deps vulneráveis

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| IDOR sem validação | Usuário acessa dados de outros | Verificar ownership |
| Reset password sem expirar | Token válido para sempre | Expira em 1h, uso único |
| Session sem invalidar logout | Sessão ativa após logout | Invalidar server-side |
| JWT sem expiração curta | Token roubado = acesso longo | Access 15min, refresh 7d |
| Erro revela info | "Usuário não existe" = enumeração | Erro genérico |
| Upload sem validação | RCE via arquivo malicioso | Validar tipo, tamanho, sanitizar nome |

## 📋 Checklist de Segurança

- [ ] Auth verificado server-side em toda rota protegida?
- [ ] Queries parametrizadas (não concat)?
- [ ] Senhas com bcrypt (cost ≥ 10)?
- [ ] Rate limiting em login e forms?
- [ ] HTTPS forçado em prod?
- [ ] Headers de segurança configurados?
- [ ] Secrets em env vars (não no código)?
- [ ] npm audit sem vulnerabilidades críticas?
- [ ] Input validado com schema?
- [ ] Logs não contêm dados sensíveis?

## 🔧 Headers de Segurança

| Header | Propósito |
|--------|-----------|
| `Content-Security-Policy` | Previne XSS |
| `X-Frame-Options: DENY` | Previne clickjacking |
| `X-Content-Type-Options: nosniff` | Previne MIME sniffing |
| `Strict-Transport-Security` | Força HTTPS |
| `Referrer-Policy` | Controla info de referrer |
