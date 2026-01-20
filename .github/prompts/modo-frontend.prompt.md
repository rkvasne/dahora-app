---
description: Interfaces, UX e melhores práticas de frontend — componentes, acessibilidade, performance de render e testes UI
---

# Modo Frontend

> **Doc oficial:** https://react.dev | https://tailwindcss.com
> **Ver também:** `@tecnologias/react.md`, `@tecnologias/tailwind.md`

---

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

### 3. Hierarquia de Ações (Frequência & Segurança)

Regra de Ouro para Header/Menu:
- **Alta Frequência (Expostos):** Ações diárias (Tema, Notificações).
- **Baixa Frequência (Protegidos):** Ações destrutivas ou raras (Sair, Configurações).

**Por que esconder "Sair"?**
1. **Lei de Fitts:** Botão "Sair" exposto aumenta risco de clique acidental ao buscar "Notificações".
2. **Lei de Jakob:** Padrão da indústria (Google, GitHub) é Avatar = Menu de Conta.
3. **Redução de Ruído:** Header deve focar na navegação, não na administração da conta.

```tsx
// ❌ Ruído visual e risco de erro
<Header>
  <Button>Tema</Button>
  <Button>Config</Button>
  <Button variant="danger">Sair</Button>
  <Avatar />
</Header>

// ✅ Padrão mental correto (Avatar = Menu)
<Header>
  <Button>Tema</Button> // Alta frequência
  <DropdownMenu>
    <DropdownTrigger><Avatar /></DropdownTrigger>
    <DropdownContent>
      <DropdownItem>Configurações</DropdownItem> // Baixa frequência
      <DropdownSeparator />
      <DropdownItem variant="danger">Sair</DropdownItem> // Protegido (2 cliques)
    </DropdownContent>
  </DropdownMenu>
</Header>
```

### 4. Prevenção de Erros

---

## 🚨 Armadilhas Comuns

| Armadilha | Consequência | Solução |
|-----------|--------------|---------|
| Re-render excessivo | Lento | React.memo, useMemo |
| Fetch em useEffect | Race conditions | react-query/SWR |
| Estado global para tudo | Complexidade | Estado local quando possível |
| CSS conflitante | Estilos quebrados | CSS Modules ou Tailwind |
| `onClick={() => fn()}` | Recria função | useCallback ou handler |
| Imagens sem dimensão | Layout shift | width/height ou aspect-ratio |

---

## 📋 Checklist de Componente

[markdown]
[ ] Props tipadas com interface?
[ ] Todos estados de UI (loading/error/empty)?
[ ] Acessível (labels, ARIA, keyboard)?
[ ] Responsivo (mobile-first)?
[ ] Sem prop drilling excessivo?
[ ] Testável (lógica extraída)?
```

---

## 🎨 Acessibilidade Mínima

| Elemento | Requisito |
|----------|-----------|
| Imagens | `alt` descritivo (ou vazio se decorativa) |
| Botões | Texto visível ou `aria-label` |
| Forms | `label` associado via `htmlFor` |
| Modais | Focus trap, ESC fecha |
| Cores | Contraste 4.5:1 mínimo |

---

## 📍 Quando Aplicar / Quando Relaxar

### Aplique rigorosamente:
- Produto em produção
- UI pública
- Formulários de dados

### Pode relaxar:
- Admin interno
- Protótipos
- Dashboards internos

---

## 🔗 Referências

| Recurso | URL |
|---------|-----|
| React Docs | https://react.dev |
| Tailwind | https://tailwindcss.com |
| A11y Checklist | https://www.a11yproject.com/checklist |
| `@tecnologias/react.md` | Detalhes React |

---

*Versão: 0.3.2*
