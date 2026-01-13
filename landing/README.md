# 🎨 Dahora App Landing Page Kit

Este diretório contém o **Design System** da landing page do Dahora App, pronto para ser replicado em outros projetos ou novas páginas.

## 📁 Estrutura de Arquivos

- **`template.html`**: ✨ **Comece por aqui!** Um arquivo base limpo com toda a estrutura necessária.
- **`variables.css`**: 🎨 **Personalize aqui.** Define cores, fontes e espaçamentos globais.
- **`styles.css`**: O CSS base (reset, tipografia, botões, containers).
- **`responsive.css`**: Regras para adaptar o layout a celulares e tablets.
- **`script.js`**: Funcionalidades essenciais (Dark Mode, Menu Mobile, Efeitos de Mouse).

## 🚀 Como Usar

### 1. Criando uma Nova Página
1. Copie o arquivo `template.html`.
2. Renomeie para o nome desejado (ex: `promo.html` ou `index.html` em outro projeto).
3. Certifique-se de que os arquivos `.css` e `.js` estejam na mesma pasta (ou ajuste os caminhos no `<head>`).

### 2. Personalizando Cores e Fontes
Abra o arquivo `variables.css` e altere as variáveis CSS root:

```css
:root {
    /* Cores Principais */
    --primary-color: #seu-codigo-hex;
    --secondary-color: #seu-codigo-hex;
    
    /* Fontes */
    --font-heading: 'Sua Fonte', sans-serif;
}
```

### 3. Componentes Disponíveis

O sistema já inclui classes CSS prontas para uso:

- **Botões**: `.btn`, `.btn-primary`, `.btn-secondary`
- **Títulos**: `.hero-title`, `.section-title`
- **Grids**: `.features-grid` (colunas automáticas)
- **Cards**: `.feature-card` (com efeito de hover e ícone)
- **Seções**: `.section` (fundo branco), `.section-alt` (fundo cinza/destaque)

### 4. Funcionalidades Automáticas (`script.js`)
Ao incluir o `script.js`, sua página ganha automaticamente:
- 🌙 **Dark Mode**: Alternância de tema com persistência (localStorage).
- 📱 **Menu Mobile**: Hambúrguer menu funcional.
- ✨ **Spotlight Effect**: Efeito de iluminação suave ao passar o mouse nos cards.

---

## 📚 Referência Técnica (Design System)

### Tokens Globais
Consulte `variables.css` para a lista completa.

*   **Cores Primárias**: `--primary-color` (#0078D4), `--primary-light` (#2B88D8), `--primary-dark` (#005A9E).
*   **Gradientes**: `--gradient-orange-red` (usado em CTAs).
*   **Texto**: `--text-dark` (Slate 900), `--text-gray` (Slate 700).
*   **Sombras**: `--shadow-sm`, `--shadow`, `--shadow-md`, `--shadow-lg` (ajustadas para dark mode automaticamente).

### Tipografia
*   **Títulos**: `Poppins` (Pesos: 600, 700, 800).
*   **Corpo**: `Inter` (Pesos: 400, 500, 600).
*   **Tamanhos**:
    *   `h1` (Hero): 3.5rem (desktop) / 2.5rem (mobile)
    *   `h2` (Seções): 2.5rem
    *   `h3` (Cards): 1.2rem

### Layout
*   **Container**: `max-width: 1280px` com padding lateral.
*   **Seções**: Padding vertical de `6rem` para garantir respiro (estilo SaaS moderno).
*   **Grids**: Responsivos com `minmax(320px, 1fr)`.

---

**Dica:** Para manter a consistência com o estilo "SaaS Moderno" (estilo Perssua/Dahora), mantenha o espaçamento generoso (`padding`) nas seções e use fontes sem serifa (Inter/Poppins já configuradas).
