# Template da Landing (Specs por Seção)

Este arquivo descreve as especificações visuais (fontes, espaçamentos, tamanhos, grids, cores, etc.) da landing atual para ser reutilizada como modelo.

**Fontes de verdade**
- [index.html](../index.html) (estrutura das seções + alguns estilos inline)
- [variables.css](../landing/variables.css) (tokens)
- [styles.css](../landing/styles.css) (base, layout, cards, dev section)
- [dark-sections.css](../landing/dark-sections.css) (hero, section-dark e download)
- [donate.css](../landing/donate.css) (doações)
- [faq.css](../landing/faq.css) (FAQ)
- [process.css](../landing/process.css) (Como Funciona / diagrama)
- [footer.css](../landing/footer.css) (footer)
- [responsive.css](../landing/responsive.css) (media queries)
- [script.js](../landing/script.js) (interações: FAQ, spotlight)

## Tokens Globais (Design System)

**Cores e fundos** ([variables.css](../landing/variables.css#L7-L53))
- Primárias: `--primary-color #0078D4`, `--primary-light #2B88D8`, `--primary-dark #005A9E`, `--secondary-color #0C5DAA`
- Gradiente CTA: `--gradient-orange-red linear-gradient(135deg, #FF7B1A 0%, #FF4500 100%)`
- Textos: `--text-dark #0f172a`, `--text-gray #334155`, `--text-light #475569`
- Fundos: `--bg-white #ffffff`, `--light-bg #f1f5f9`, `--dark-bg #0f172a`, `--dark-card #1e293b`
- Bordas: `--border-color #e2e8f0`

**Sombras** ([variables.css](../landing/variables.css#L32-L38))
- `--shadow-sm 0 1px 2px 0 rgba(0,0,0,0.05)`
- `--shadow 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.03)`
- `--shadow-md 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -2px rgba(0,0,0,0.03)`
- `--shadow-lg 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04)`

**Hero / Glass** ([variables.css](../landing/variables.css#L39-L53))
- Hero mesh: `--hero-dark-1 #020617`, `--hero-dark-2 #0f172a`, `--hero-dark-3 #1e293b`
- Glass: `--glass-bg rgba(255,255,255,0.08)`, `--glass-border rgba(255,255,255,0.1)`, `--glass-shadow 0 8px 32px 0 rgba(0,0,0,0.36)`
- Header: `--header-bg rgba(255,255,255,0.85)`

**Dark mode overrides** ([variables.css](../landing/variables.css#L55-L65))
- `--text-dark #f8fafc`, `--text-gray #cbd5e1`, `--text-light #94a3b8`
- `--bg-white #0f172a`, `--light-bg #1e293b`, `--border-color #334155`, `--header-bg rgba(15,23,42,0.85)`
- `--shadow` e `--shadow-lg` ficam mais fortes (com alfa maior)

## Tipografia e Base

**Body** ([styles.css](../landing/styles.css#L14-L24))
- Font stack: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- `line-height: 1.6`
- `color: var(--text-dark)` / `background-color: var(--bg-white)`
- `transition: background-color 0.3s ease, color 0.3s ease`

**Headings (h1–h6)** ([styles.css](../landing/styles.css#L64-L73))
- Font: `Poppins`
- `letter-spacing: -0.03em`
- `line-height: 1.15`

## Primitivos de Layout (Seções/Container)

**Seção padrão** ([styles.css](../landing/styles.css#L224-L233))
- `.section`: `padding: 6rem 2rem`, `background-color: var(--bg-white)`
- `.section-alt`: `background-color: var(--light-bg)`

**Container** ([styles.css](../landing/styles.css#L234-L238))
- `.container`: `max-width: 1280px`, `margin: 0 auto`, `padding: 0 1rem`

**Cabeçalho de seção** ([styles.css](../landing/styles.css#L240-L259))
- `.section-header`: `text-align: center`, `margin-bottom: 3.5rem`
- `.section-title`: `font-size: 2.5rem`, `font-weight: 700`, `margin-bottom: 1rem`
- `.section-subtitle`: `font-size: 1.2rem`, `line-height: 1.6`, `max-width: 700px`, `margin: 0 auto`

## Header / Navegação

**Header sticky com blur** ([styles.css](../landing/styles.css#L76-L84))
- `.header`: `position: sticky; top: 0; z-index: 1000`
- `background: var(--header-bg)`, `backdrop-filter: blur(12px)`
- `box-shadow: var(--shadow-sm)` e `border-bottom: 1px solid var(--border-color)`

**Nav** ([styles.css](../landing/styles.css#L86-L116))
- `.nav`: `max-width: 1200px`, `margin: 0 auto`, `padding: 1rem 1.5rem`, `display:flex`, `justify-content: space-between`
- `.nav-menu`: `display:flex`, `gap: 1.5rem`, `list-style:none`, `align-items:center`
- `.nav-controls`: container para `ul.nav-menu`, ações (tema/idioma) e botão mobile.
- `.nav-actions`: container para `theme-btn` e `lang-btn` (fora do menu principal).

**Links** ([styles.css](../landing/styles.css#L118-L154))
- `.nav-link`: `font-weight: 500`, `padding: 0.5rem 1rem`, `border-radius: 2rem`, `display: inline-flex`, `align-items:center`
- Hover: `color: var(--primary-color)`, `background: var(--light-bg)`

**Botão tema (ícone)** ([styles.css](../landing/styles.css#L130-L149))
- `.theme-btn`: `width: 36px; height: 36px`, `border-radius: 50%`, `border: 1px solid var(--border-color)`
- Hover: `background: var(--light-bg)`, `border-color: var(--primary-color)`

**Botão idioma** ([styles.css](../landing/styles.css#L199-L222))
- `.lang-btn`: `padding: 0.5rem 1rem`, `border-radius: 2rem`, `font-size: 0.9rem`, `font-weight: 600` (no header, o `margin-left` pode ser zerado quando dentro de `.nav-actions`).
- Dark mode: `border-color rgba(255,255,255,0.2)` e `color: var(--text-light)`

## Botões (CTA)

**Base** ([styles.css](../landing/styles.css#L156-L169))
- `.btn`: `padding: 1rem 2.5rem`, `border-radius: 100px`, `font-weight: 600`, `font-size: 1rem`
- `display: inline-flex`, `align-items:center`, `gap: 0.75rem`

**Primário (gradiente laranja→vermelho)** ([styles.css](../landing/styles.css#L171-L182))
- `.btn-primary`: `background: var(--gradient-primary)`, `color: #fff`
- Hover: `transform: translateY(-2px)`, troca para `--gradient-primary-hover`

**Secundário** ([styles.css](../landing/styles.css#L184-L197))
- `.btn-secondary`: `background: var(--bg-white)`, `border: 1px solid var(--border-color)`
- Hover: `border-color: var(--primary-color)`, `background: var(--light-bg)`, `transform: translateY(-2px)`

## Hero (Seção #inicio)

**Markup** ([index.html](../index.html#L64-L106))
- `section#inicio.hero` → `.hero-container` → `.hero-version`, `.hero-icon`, `.hero-title`, `.hero-subtitle`, `.hero-buttons`, `.hero-badges`, `.hero-trust-links`
- `.hero-version`: texto de versão em formato "ATUALIZAÇÃO V.0.2.11"
- `.hero-subtitle`: texto simples "Cole datas e horas no cursor, sem interromper."
- `.hero-trust-links`: links de confiança (Releases oficiais, Código-fonte, Privacidade, Segurança, Licença MIT) separados por `•`

**Background e espaçamento** ([dark-sections.css](../landing/dark-sections.css#L9-L19))
- `.hero`: background em 3 camadas (2 radial + 1 linear), `color: white`
- Padding desktop: `8rem 2rem 6rem`, `text-align: center`

**Grid overlay** ([dark-sections.css](../landing/dark-sections.css#L21-L33))
- `.hero::before`: grid com `background-size: 64px 64px`, `opacity: 0.4`

**Container e ícone** ([dark-sections.css](../landing/dark-sections.css#L35-L45))
- `.hero-container`: `max-width: 900px`, centralizado
- `.hero-icon`: `width/height: 120px`, `margin-bottom: 1.5rem`

**Título e subtítulo** ([dark-sections.css](../landing/dark-sections.css#L47-L72))
- `.hero-title`: `font-size: 3.5rem`, `font-weight: 800`, `line-height: 1.1`, gradiente no texto
- `.hero-subtitle`: `font-size: 1.2rem`, `line-height: 1.6`, `max-width: 500px`, `margin-bottom: 2.5rem`

**Badge de versão (pílula)** ([dark-sections.css](../landing/dark-sections.css#L74-L88))
- `.hero-version`: `padding: 0.5rem 1.25rem`, `border-radius: 100px`, `font-size: 0.875rem`, `font-weight: 600`
- Cor do texto: `#38bdf8`, borda `rgba(56,189,248,0.2)`, `backdrop-filter: blur(8px)`

**Badges de atributos** ([dark-sections.css](../landing/dark-sections.css#L90-L133))
- `.hero-badges`: `display:flex`, `gap: 2.5rem`, `margin-bottom: 3rem`, `flex-wrap: wrap`
- `.hero-badge-item`: coluna, `gap: 0.8rem`, `font-size: 0.95rem`
- Ícone do badge: `48x48px`, `border-radius: 12px`, borda `rgba(56,189,248,0.2)`

**Botões** ([dark-sections.css](../landing/dark-sections.css#L146-L151))
- `.hero-buttons`: `display:flex`, `gap: 1.5rem`, centralizado, `flex-wrap: wrap`

**Links de confiança** ([index.html](../index.html#L94-L104))
- `.hero-trust-links`: links separados por `.hero-trust-sep` (•)
- Links: Releases oficiais, Código-fonte, Privacidade, Segurança, Licença MIT

## Seções com Cards (Recursos / Detalhes Técnicos / Guia Rápido / Segurança Executável)

**Grid de cards** ([styles.css](../landing/styles.css#L261-L266))
- `.features-grid`: `display:grid`, `grid-template-columns: repeat(auto-fit, minmax(320px, 1fr))`, `gap: 1.5rem`
- Variação "Para quem é" (desktop): `2 colunas` com largura máxima e centralização via `.features-grid.audience-grid`.

**Card** ([styles.css](../landing/styles.css#L268-L301))
- `.feature-card`: `padding: 2.5rem`, `border-radius: 1rem`, `border: 1px solid var(--border-color)`, `height: 100%`
- Hover: `box-shadow: 0 8px 25px rgba(0,0,0,0.08)` e borda `rgba(0,120,212,0.2)`
- Barra superior animada: pseudo-elemento com `height: 4px` (aparece no hover)

**Ícone "tecla" (padrão 56px)** ([styles.css](../landing/styles.css#L303-L352))
- `.feature-icon`: `56x56px`, `border-radius: 14px`, `font-size: 1.6rem`
- Borda: `1px solid rgba(56, 189, 248, 0.75)` + `border-bottom-width: 3px`
- Background: `linear-gradient(180deg, rgba(0,120,212,0.98), rgba(0,90,158,0.98))`
- Hover (no card): `transform: translateY(2px)` e troca do gradiente
- Active: "pressionado" com `transform: translateY(6px)` e `border-bottom-width: 0`

**Tipografia do card** ([styles.css](../landing/styles.css#L374-L386))
- Título: `font-size: 1.2rem`, `font-weight: 600`, `margin-bottom: 1rem`
- Texto: `font-size: 0.95rem`, `line-height: 1.6`

**Recursos Principais** ([index.html](../index.html#L110-L190))
- 6 cards: Colagem Automática, Atalhos Ilimitados, Histórico Inteligente, 100% Configurável, Interface Nativa, Privado & Offline

**Detalhes Técnicos** ([index.html](../index.html#L192-L279))
- 6 cards: Stack Tecnológico, Padrões de Projeto, Testes & Qualidade, Estrutura Modular, Integração OS, Performance

## Como Funciona (Diagrama)

**Markup** ([index.html](../index.html#L281-L321))
- `.process-flow` contendo 4 `.process-step` intercalados com `.step-arrow`
- Passos: 1. Você pressiona o atalho, 2. App monta timestamp, 3. Cola no cursor, 4. Preserva a área de transferência

**Layout desktop** ([process.css](../landing/process.css#L6-L14))
- `.process-flow`: `display:flex`, `justify-content: space-between`, `gap: 1.5rem`, `max-width: 1200px`

**Card do passo** ([process.css](../landing/process.css#L16-L38))
- `.process-step`: `padding: 2rem 1.5rem 1.5rem`, `border-radius: 1rem`, `border: 1px solid var(--border-color)`
- Hover: `box-shadow: var(--shadow-md)` e borda `var(--primary-light)`

**Ícone do passo (tecla 56px)** ([process.css](../landing/process.css#L62-L111))
- `.step-icon`: mesma "tecla" da `.feature-icon` (56px, raio 14px, border-bottom 3px)
- Hover no card: `translateY(2px)`; Active: `translateY(6px)` e "some" border-bottom

**Tipografia do passo** ([process.css](../landing/process.css#L133-L149))
- `h3`: `font-size: 1.1rem`, `line-height: 1.25`, `min-height: 3.2rem`
- `p`: `font-size: 0.9rem`, `line-height: 1.5`

## Para quem é (Seção #audience)

**Markup** ([index.html](../index.html#L323-L347))
- Seção `.section.section-alt` com `.features-grid.audience-grid`
- 3 cards: Suporte e atendimento, Desenvolvedores, Times administrativos

## Guia Rápido (Seção #guia-rapido)

**Markup** ([index.html](../index.html#L349-L373))
- Seção `.section.section-alt` com `.features-grid`
- 3 cards: Atalhos padrão, Personalização, Dicas rápidas

## Instalação (3 passos)

**Markup** ([index.html](../index.html#L404-L471))
- Seção `.section.section-alt` com `.features-grid.install-grid`
- Cada card de instalação usa `.feature-card.install-card` e também `style="text-align: center;"`
- Número usa `.feature-icon.install-number` com conteúdo `1`, `2`, `3`

**Grid** ([styles.css](../landing/styles.css#L564-L571))
- `.install-grid`: `grid-template-columns: repeat(3, 1fr)`, `gap: 2rem`, `max-width: 1000px`, `margin: 0 auto`

**Aviso de segurança do Windows (estilo inline)** ([index.html](../index.html#L439-L469))
- Wrapper do aviso: `margin-top: 3rem`, `max-width: 800px`, background `rgba(245,158,11,0.05)`, `border-left: 5px solid #f59e0b`, `padding: 1.5rem`, `font-size: 0.95rem`
- Título: `font-size: 1.1rem`, cor `#f59e0b`, `gap: 0.75rem`, `margin-bottom: 1rem`
- `details/summary`: `font-size: 0.9rem`, cor `#d97706`, `gap: 0.5rem`
- Imagens: `width: 300px`, `border-radius: 0.5rem`, `box-shadow: 0 4px 6px rgba(0,0,0,0.2)`
- 2 imagens: `tela_aviso1.png` e `tela_aviso2.png` dentro de `<details>`

## Download (Seção #download)

**Markup** ([index.html](../index.html#L473-L495))
- `section#download.download` → `.download-box` → `h2`, `p`, `.btn-download-large`, `.download-trust-links`, `.download-footer`
- O botão de download aponta para `.../releases/latest/download/DahoraApp_latest.zip` (arquivo "latest", sem versão no nome)

## Executável & Segurança (Seção #seguranca-executavel)

**Markup** ([index.html](../index.html#L375-L399))
- `section#seguranca-executavel.section` → `.features-grid` com 3 `.feature-card`
- O card "Como verificar" inclui link para `.../releases` (GitHub Releases) e instrução de build `py build.py`

## Doações (Seção #donate)

**Markup** ([index.html](../index.html#L497-L551))
- `section#donate.donate-section` → `.donate-container` → `.donate-header` → `.donate-grid` → `.donate-qr-box` → `.donate-note-box`

## FAQ (Seção #faq)

**Markup** ([index.html](../index.html#L553-L679))
- `section#faq.faq.section.section-alt` → `.faq-container` → `.faq-item` (com `button.faq-question` e `.faq-answer`)
- 10 perguntas (não 9): Q1-Q10

**Perguntas** ([index.html](../index.html#L561-L677))
1. O Dahora App é grátis?
2. Precisa de instalação?
3. Meus dados ficam salvos onde?
4. Como funciona o histórico da área de transferência?
5. Posso personalizar os atalhos?
6. O menu da bandeja do sistema não atualiza automaticamente?
7. É seguro? Tem vírus?
8. Funciona no Windows 11?
9. Como contribuir com o projeto?
10. Como pedir ajuda / suporte?

## Interações (JS)

**FAQ toggle** ([script.js](../landing/script.js#L4-L18))
- Clique em `.faq-question` alterna classe `.active` no `.faq-item` (e remove `.active` dos demais).
- Função `toggleFAQ(button)` implementada inline no HTML

**Spotlight (mouse)**
- Cards `.feature-card`: atualiza CSS vars `--x` e `--y` no elemento ([script.js](../landing/script.js#L21-L33)).
- Seções `.section-dark`: atualiza CSS vars `--mx` e `--my` ([script.js](../landing/script.js#L35-L46)).

**Menu mobile (implementado inline no HTML)** ([index.html](../index.html#L770-L803))
- Alterna `.active` em `#nav-menu.nav-menu` e `#menu-overlay.menu-overlay`
- Função `toggleMenu()` implementada inline
- Ícone alterna entre `fa-bars` e `fa-times`

**Theme Toggle** ([index.html](../index.html#L1200-L1226))
- Alterna classe `dark-mode` no `body`
- Salva preferência em `localStorage`
- Ícone alterna entre `fa-moon` e `fa-sun`

**Language Toggle** ([index.html](../index.html#L1131-L1153))
- Alterna entre `pt-BR` e `en`
- Atualiza todos os elementos com `data-i18n`
- Botão mostra "EN" ou "PT"

**Traduções** ([index.html](../index.html#L806-L1128))
- Objeto `translations` com `pt-BR` e `en`
- Nota: algumas traduções ainda referenciam v0.2.10 (deve ser atualizado para v0.2.11)

---

**Última atualização:** 12 de janeiro de 2026 | **Versão:** v0.2.11

