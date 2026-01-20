---
description: Guia unificado de debug para Web, Backend, Mobile e DevOps.
---

# 🕵️‍♂️ Modo Depurador Unificado

> **Princípio Fundamental:** Sem reprodução, não há debug.

Este modo centraliza estratégias de depuração para todas as camadas. Use a seção relevante para o seu problema.

---

## ⚠️ REGRAS DE OURO (Universais)

### ❌ NUNCA
- ❌ **Mudar código sem reproduzir** → pode criar bug novo
- ❌ **Múltiplas mudanças de uma vez** → não saberá qual resolveu
- ❌ **Fix sem teste de regressão** → bug voltará
- ❌ **Assumir a causa** → "deve ser X" sem verificar (Zero Achismo)

### ✅ SEMPRE
- ✅ **Reproduzir primeiro** → passos exatos, ambiente, frequência
- ✅ **Uma hipótese por vez** → método científico
- ✅ **Isolar o problema** → menor código que falha
- ✅ **Verificar logs** → servidor, browser console, network, logcat

---

## 🌐 1. Depuração Web / Frontend
*Para: Tela branca, hydration error, CORS, requests falhando, UI quebrada.*

### Ferramentas Essenciais
- **Console:** Erros de JS, warnings de React.
- **Network Tab:** Status HTTP, payload, headers, timing.
- **React DevTools:** Props, State, Context.

### Checklist Web
- [ ] Verificou o Console por erros vermelhos?
- [ ] Verificou a aba Network (requests falhando ou pendentes)?
- [ ] Limpou o cache (Hard Refresh `Ctrl+Shift+R`)?
- [ ] Testou em aba anônima (sem extensões)?
- [ ] O erro acontece em produção e staging?

**Causas Comuns:**
- `Hydration Mismatch`: HTML do servidor diferente do cliente.
- `CORS`: Falta de headers no backend.
- `Undefined is not a function`: Import circular ou nulo.

---

## 🔙 2. Depuração Backend / API
*Para: Erro 500, timeout, dados incorretos, performance.*

### Ferramentas Essenciais
- **Logs Estruturados:** JSON logs (não `console.log` solto).
- **Stack Trace:** Leia a primeira linha do erro e a linha do seu código.
- **DB Client:** Verifique se a query SQL retorna o esperado.

### Checklist Backend
- [ ] Reproduziu o erro com um cURL ou Postman?
- [ ] Analisou o Stack Trace completo?
- [ ] Verificou variáveis de ambiente (`.env`)?
- [ ] O banco de dados está acessível e respondendo?
- [ ] Há logs de "Connection Timeout" ou "Pool Exhausted"?

**Causas Comuns:**
- `N+1 Queries`: Loop fazendo queries no banco.
- `Env Var Missing`: Chave de API faltando ou errada.
- `Unhandled Promise Rejection`: Falta de `catch` ou `try/await`.

---

## 📱 3. Depuração Mobile
*Para: Crash no boot, build falhando, layout quebrado no device.*

### Ferramentas Essenciais
- **Logcat (Android) / Console.app (iOS):** Logs nativos reais.
- **Device Físico:** Emuladores mentem (especialmente sobre performance e câmera).
- **Metro Bundler:** Logs de JS do React Native.

### Checklist Mobile
- [ ] Testou em dispositivo físico?
- [ ] Limpou caches (`gradlew clean`, `pod install`, `metro reset`)?
- [ ] Verificou permissões (Câmera, Localização) no manifesto?
- [ ] O erro acontece no iOS E no Android?

**Causas Comuns:**
- `Cache`: Metro bundler ou Gradle com lixo antigo.
- `Permissões`: App crasha ao tentar acessar recurso sem pedir permissão.
- `Estilos`: `flex: 1` faltando faz conteúdo sumir.

---

## 🚀 4. Depuração DevOps / Infra
*Para: Pipeline CI falhando, Docker crashando, SSL, DNS.*

### Ferramentas Essenciais
- **CI Logs:** GitHub Actions / GitLab CI output.
- **Docker Logs:** `docker logs <container_id>`.
- **Curl/Dig:** Testar conectividade e DNS.

### Checklist DevOps
- [ ] O erro é reproduzível localmente (Docker)?
- [ ] As Secrets do CI estão configuradas corretamente?
- [ ] O container tem memória/CPU suficientes (OOM Killed)?
- [ ] O certificado SSL é válido (`openssl s_client`)?

**Causas Comuns:**
- `Secrets`: Variável vazia no CI mas presente localmente.
- `Network`: Container não consegue acessar banco (host incorreto).
- `Disk Space`: Runner ou servidor sem espaço.

---

## 📋 Processo Universal (7 Passos)

1. **Reproduzir:** Crie um cenário onde o erro acontece 100% das vezes.
2. **Coletar:** Junte logs, screenshots e contexto.
3. **Isolar:** Remova variáveis até sobrar só o erro.
4. **Hipótese:** "Acho que é X porque Y".
5. **Teste:** Valide a hipótese.
6. **Fix:** Aplique a correção mínima.
7. **Regressão:** Garanta que não quebrou outra coisa.

---

*Versão Unificada 1.0*
