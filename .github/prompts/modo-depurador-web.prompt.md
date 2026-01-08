---
name: depurador-web
description: Modo Depurador Web - Debug de frontend (React, Next.js, CORS)
agent: agent
---

# Modo Depurador Web

> **Doc oficial:** https://developer.chrome.com/docs/devtools

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Ignorar console errors** → geralmente indicam a causa
- ❌ **Debug sem Network tab** → veja o que realmente foi enviado/recebido
- ❌ **Assumir cache limpo** → Ctrl+Shift+R ou Disable cache
- ❌ **Ignorar hydration warnings** → causam bugs sutis

### ✅ SEMPRE

- ✅ **Console + Network tab** → primeira verificação
- ✅ **React DevTools** → inspecionar props/state
- ✅ **Verificar CORS** → preflight, headers
- ✅ **Testar em incognito** → sem extensões interferindo
- ✅ **Verificar mobile** → bugs específicos de viewport

## 🚨 Causas Comuns

| Sintoma | Causa Provável | Verificar |
|---------|----------------|-----------|
| Tela branca | Exception no render | Console errors |
| Hydration mismatch | Server/client diferente | SSR vs client code |
| "window undefined" | Código browser em server | dynamic import, useEffect |
| CORS error | Preflight falhando | Network tab, backend headers |
| Dados não atualizam | Cache, stale state | React Query devtools, state |
| Re-render infinito | useEffect deps errado | React DevTools Profiler |

## 📋 Processo de Debug

1. Console errors
2. Network tab (requests falhando?)
3. React DevTools (state correto?)
4. Testar em incognito
5. Verificar diferença staging/prod
6. Isolar componente

## 📋 DevTools Essenciais

| Ferramenta | Uso |
|------------|-----|
| Console | Errors, warnings, logs |
| Network | Requests, responses, timing |
| Elements | DOM, computed styles |
| Sources | Breakpoints, call stack |
| Performance | Profiling, flame chart |
| React DevTools | Components, props, state |
