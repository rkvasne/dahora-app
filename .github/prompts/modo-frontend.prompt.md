---
name: frontend
description: Modo Frontend - UI, componentes e interfaces (React, CSS)
agent: agent
---

# Modo Frontend

> **Doc oficial:** https://react.dev | https://tailwindcss.com

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Lógica de negócio em componente** → extraia para hooks/services
- ❌ **Prop drilling > 2 níveis** → Context ou state management
- ❌ **CSS inline para tudo** → classes reutilizáveis
- ❌ **`any` em props** → TypeScript com interfaces
- ❌ **useEffect para tudo** → considere react-query, SWR
- ❌ **Componente > 200 linhas** → quebre menor
- ❌ **Ignorar acessibilidade** → a11y desde o início
- ❌ **Estado derivado em useState** → calcule no render

### ✅ SEMPRE

- ✅ **Componentes pequenos** → uma responsabilidade
- ✅ **Props tipadas** → interface TypeScript
- ✅ **Estados de UI** → loading, error, empty, success
- ✅ **Mobile-first** → responsivo de início
- ✅ **Keyboard navigation** → Tab, Enter, Escape
- ✅ **Labels em inputs** → acessibilidade básica
- ✅ **Keys únicas em listas** → não use index
- ✅ **Lazy loading** → componentes pesados

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| Re-render excessivo | Lento | React.memo, useMemo |
| Fetch em useEffect | Race conditions | react-query/SWR |
| Estado global para tudo | Complexidade | Estado local quando possível |
| CSS conflitante | Estilos quebrados | CSS Modules ou Tailwind |
| `onClick={() => fn()}` | Recria função | useCallback ou handler |
| Imagens sem dimensão | Layout shift | width/height ou aspect-ratio |

## 📋 Checklist de Componente

- [ ] Props tipadas com interface?
- [ ] Todos estados de UI (loading/error/empty)?
- [ ] Acessível (labels, ARIA, keyboard)?
- [ ] Responsivo (mobile-first)?
- [ ] Sem prop drilling excessivo?
- [ ] Testável (lógica extraída)?

## 🎨 Acessibilidade Mínima

| Elemento | Requisito |
|----------|-----------|
| Imagens | `alt` descritivo (ou vazio se decorativa) |
| Botões | Texto visível ou `aria-label` |
| Forms | `label` associado via `htmlFor` |
| Modais | Focus trap, ESC fecha |
| Cores | Contraste 4.5:1 mínimo |
