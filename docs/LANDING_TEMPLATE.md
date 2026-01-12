# Template da Landing (Specs por Seção)

Este arquivo descreve as especificações visuais (fontes, espaçamentos, tamanhos, grids, cores, etc.) da landing atual para ser reutilizada como modelo.

**Fontes de verdade**
- [index.html](file:///e:/Dahora/dahora-app/index.html) (estrutura das seções + alguns estilos inline)
- [variables.css](file:///e:/Dahora/dahora-app/landing/variables.css) (tokens)
- [styles.css](file:///e:/Dahora/dahora-app/landing/styles.css) (base, layout, cards, dev section)
- [dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css) (hero, section-dark e download)
- [donate.css](file:///e:/Dahora/dahora-app/landing/donate.css) (doações)
- [faq.css](file:///e:/Dahora/dahora-app/landing/faq.css) (FAQ)
- [process.css](file:///e:/Dahora/dahora-app/landing/process.css) (Como Funciona / diagrama)
- [footer.css](file:///e:/Dahora/dahora-app/landing/footer.css) (footer)
- [responsive.css](file:///e:/Dahora/dahora-app/landing/responsive.css) (media queries)
- [script.js](file:///e:/Dahora/dahora-app/landing/script.js) (interações: FAQ, spotlight)

## Tokens Globais (Design System)

**Cores e fundos** ([variables.css](file:///e:/Dahora/dahora-app/landing/variables.css#L7-L53))
- Primárias: `--primary-color #0078D4`, `--primary-light #2B88D8`, `--primary-dark #005A9E`, `--secondary-color #0C5DAA`
- Gradiente CTA: `--gradient-orange-red linear-gradient(135deg, #FF7B1A 0%, #FF4500 100%)`
- Textos: `--text-dark #0f172a`, `--text-gray #334155`, `--text-light #475569`
- Fundos: `--bg-white #ffffff`, `--light-bg #f1f5f9`, `--dark-bg #0f172a`, `--dark-card #1e293b`
- Bordas: `--border-color #e2e8f0`

**Sombras** ([variables.css](file:///e:/Dahora/dahora-app/landing/variables.css#L32-L38))
- `--shadow-sm 0 1px 2px 0 rgba(0,0,0,0.05)`
- `--shadow 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.03)`
- `--shadow-md 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -2px rgba(0,0,0,0.03)`
- `--shadow-lg 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04)`

**Hero / Glass** ([variables.css](file:///e:/Dahora/dahora-app/landing/variables.css#L39-L53))
- Hero mesh: `--hero-dark-1 #020617`, `--hero-dark-2 #0f172a`, `--hero-dark-3 #1e293b`
- Glass: `--glass-bg rgba(255,255,255,0.08)`, `--glass-border rgba(255,255,255,0.1)`, `--glass-shadow 0 8px 32px 0 rgba(0,0,0,0.36)`
- Header: `--header-bg rgba(255,255,255,0.85)`

**Dark mode overrides** ([variables.css](file:///e:/Dahora/dahora-app/landing/variables.css#L55-L65))
- `--text-dark #f8fafc`, `--text-gray #cbd5e1`, `--text-light #94a3b8`
- `--bg-white #0f172a`, `--light-bg #1e293b`, `--border-color #334155`, `--header-bg rgba(15,23,42,0.85)`
- `--shadow` e `--shadow-lg` ficam mais fortes (com alfa maior)

## Tipografia e Base

**Body** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L14-L24))
- Font stack: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- `line-height: 1.6`
- `color: var(--text-dark)` / `background-color: var(--bg-white)`
- `transition: background-color 0.3s ease, color 0.3s ease`

**Headings (h1–h6)** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L64-L73))
- Font: `Poppins`
- `letter-spacing: -0.03em`
- `line-height: 1.15`

## Primitivos de Layout (Seções/Container)

**Seção padrão** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L224-L233))
- `.section`: `padding: 6rem 2rem`, `background-color: var(--bg-white)`
- `.section-alt`: `background-color: var(--light-bg)`

**Container** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L234-L238))
- `.container`: `max-width: 1280px`, `margin: 0 auto`, `padding: 0 1rem`

**Cabeçalho de seção** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L240-L259))
- `.section-header`: `text-align: center`, `margin-bottom: 3.5rem`
- `.section-title`: `font-size: 2.5rem`, `font-weight: 700`, `margin-bottom: 1rem`
- `.section-subtitle`: `font-size: 1.2rem`, `line-height: 1.6`, `max-width: 700px`, `margin: 0 auto`

## Header / Navegação

**Header sticky com blur** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L76-L84))
- `.header`: `position: sticky; top: 0; z-index: 1000`
- `background: var(--header-bg)`, `backdrop-filter: blur(12px)`
- `box-shadow: var(--shadow-sm)` e `border-bottom: 1px solid var(--border-color)`

**Nav** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L86-L116))
- `.nav`: `max-width: 1200px`, `margin: 0 auto`, `padding: 1rem 1.5rem`, `display:flex`, `justify-content: space-between`
- `.nav-menu`: `display:flex`, `gap: 1.5rem`, `list-style:none`, `align-items:center`
- `.nav-controls`: container para `ul.nav-menu`, ações (tema/idioma) e botão mobile.
- `.nav-actions`: container para `theme-btn` e `lang-btn` (fora do menu principal).

**Links** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L118-L154))
- `.nav-link`: `font-weight: 500`, `padding: 0.5rem 1rem`, `border-radius: 2rem`, `display: inline-flex`, `align-items:center`
- Hover: `color: var(--primary-color)`, `background: var(--light-bg)`

**Botão tema (ícone)** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L130-L149))
- `.theme-btn`: `width: 36px; height: 36px`, `border-radius: 50%`, `border: 1px solid var(--border-color)`
- Hover: `background: var(--light-bg)`, `border-color: var(--primary-color)`

**Botão idioma** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L199-L222))
- `.lang-btn`: `padding: 0.5rem 1rem`, `border-radius: 2rem`, `font-size: 0.9rem`, `font-weight: 600` (no header, o `margin-left` pode ser zerado quando dentro de `.nav-actions`).
- Dark mode: `border-color rgba(255,255,255,0.2)` e `color: var(--text-light)`

## Botões (CTA)

**Base** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L156-L169))
- `.btn`: `padding: 1rem 2.5rem`, `border-radius: 100px`, `font-weight: 600`, `font-size: 1rem`
- `display: inline-flex`, `align-items:center`, `gap: 0.75rem`

**Primário (gradiente laranja→vermelho)** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L171-L182))
- `.btn-primary`: `background: var(--gradient-primary)`, `color: #fff`
- Hover: `transform: translateY(-2px)`, troca para `--gradient-primary-hover`

**Secundário** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L184-L197))
- `.btn-secondary`: `background: var(--bg-white)`, `border: 1px solid var(--border-color)`
- Hover: `border-color: var(--primary-color)`, `background: var(--light-bg)`, `transform: translateY(-2px)`

## Hero (Seção #inicio)

**Markup** ([index.html](file:///e:/Dahora/dahora-app/index.html#L64-L98))
- `section#inicio.hero` → `.hero-container` → `.hero-version`, `.hero-icon`, `.hero-title`, `.hero-subtitle`, `.hero-badges`, `.hero-buttons`
- `.hero-version`: texto de versão em formato “ATUALIZAÇÃO V.0.2.10”
- `.hero-subtitle`: texto em 2 linhas com `<br>` e separador `•` (ex.: “Automaticamente na posição do cursor • Preserve sua área de transferência”)

**Background e espaçamento** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L9-L19))
- `.hero`: background em 3 camadas (2 radial + 1 linear), `color: white`
- Padding desktop: `8rem 2rem 6rem`, `text-align: center`

**Grid overlay** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L21-L33))
- `.hero::before`: grid com `background-size: 64px 64px`, `opacity: 0.4`

**Container e ícone** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L35-L45))
- `.hero-container`: `max-width: 900px`, centralizado
- `.hero-icon`: `width/height: 120px`, `margin-bottom: 1.5rem`

**Título e subtítulo** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L47-L72))
- `.hero-title`: `font-size: 3.5rem`, `font-weight: 800`, `line-height: 1.1`, gradiente no texto
- `.hero-subtitle`: `font-size: 1.2rem`, `line-height: 1.6`, `max-width: 500px`, `margin-bottom: 2.5rem`

**Badge de versão (pílula)** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L74-L88))
- `.hero-version`: `padding: 0.5rem 1.25rem`, `border-radius: 100px`, `font-size: 0.875rem`, `font-weight: 600`
- Cor do texto: `#38bdf8`, borda `rgba(56,189,248,0.2)`, `backdrop-filter: blur(8px)`

**Badges de atributos** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L90-L133))
- `.hero-badges`: `display:flex`, `gap: 2.5rem`, `margin-bottom: 3rem`, `flex-wrap: wrap`
- `.hero-badge-item`: coluna, `gap: 0.8rem`, `font-size: 0.95rem`
- Ícone do badge: `48x48px`, `border-radius: 12px`, borda `rgba(56,189,248,0.2)`

**Botões** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L146-L151))
- `.hero-buttons`: `display:flex`, `gap: 1.5rem`, centralizado, `flex-wrap: wrap`

## Seções com Cards (Recursos / Detalhes Técnicos / Guia Rápido / Segurança Executável)

**Grid de cards** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L261-L266))
- `.features-grid`: `display:grid`, `grid-template-columns: repeat(auto-fit, minmax(320px, 1fr))`, `gap: 1.5rem`
- Variação “Para quem é” (desktop): `2 colunas` com largura máxima e centralização via `.features-grid.audience-grid`.   

**Card** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L268-L301))
- `.feature-card`: `padding: 2.5rem`, `border-radius: 1rem`, `border: 1px solid var(--border-color)`, `height: 100%`
- Hover: `box-shadow: 0 8px 25px rgba(0,0,0,0.08)` e borda `rgba(0,120,212,0.2)`
- Barra superior animada: pseudo-elemento com `height: 4px` (aparece no hover)

**Ícone “tecla” (padrão 56px)** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L303-L352))
- `.feature-icon`: `56x56px`, `border-radius: 14px`, `font-size: 1.6rem`
- Borda: `1px solid rgba(56, 189, 248, 0.75)` + `border-bottom-width: 3px`
- Background: `linear-gradient(180deg, rgba(0,120,212,0.98), rgba(0,90,158,0.98))`
- Hover (no card): `transform: translateY(2px)` e troca do gradiente
- Active: “pressionado” com `transform: translateY(6px)` e `border-bottom-width: 0`

**Tipografia do card** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L374-L386))
- Título: `font-size: 1.2rem`, `font-weight: 600`, `margin-bottom: 1rem`
- Texto: `font-size: 0.95rem`, `line-height: 1.6`

## Como Funciona (Diagrama)

**Markup** ([index.html](file:///e:/Dahora/dahora-app/index.html#L273-L313))
- `.process-flow` contendo vários `.process-step` intercalados com `.step-arrow`

**Layout desktop** ([process.css](file:///e:/Dahora/dahora-app/landing/process.css#L6-L14))
- `.process-flow`: `display:flex`, `justify-content: space-between`, `gap: 1.5rem`, `max-width: 1200px`

**Card do passo** ([process.css](file:///e:/Dahora/dahora-app/landing/process.css#L16-L38))
- `.process-step`: `padding: 2rem 1.5rem 1.5rem`, `border-radius: 1rem`, `border: 1px solid var(--border-color)`
- Hover: `box-shadow: var(--shadow-md)` e borda `var(--primary-light)`

**Ícone do passo (tecla 56px)** ([process.css](file:///e:/Dahora/dahora-app/landing/process.css#L62-L111))
- `.step-icon`: mesma “tecla” da `.feature-icon` (56px, raio 14px, border-bottom 3px)
- Hover no card: `translateY(2px)`; Active: `translateY(6px)` e “some” border-bottom

**Tipografia do passo** ([process.css](file:///e:/Dahora/dahora-app/landing/process.css#L133-L149))
- `h3`: `font-size: 1.1rem`, `line-height: 1.25`, `min-height: 3.2rem`
- `p`: `font-size: 0.9rem`, `line-height: 1.5`

## Instalação (3 passos)

**Markup** ([index.html](file:///e:/Dahora/dahora-app/index.html#L369-L404))
- Seção `.section.section-alt` com `.features-grid.install-grid`
- Cada card de instalação usa `.feature-card.install-card` e também `style="text-align: center;"`
- Número usa `.feature-icon.install-number` com conteúdo `1`, `2`, `3`

**Grid** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L564-L571))
- `.install-grid`: `grid-template-columns: repeat(3, 1fr)`, `gap: 2rem`, `max-width: 1000px`, `margin: 0 auto`

**Número (tecla 56px)** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L573-L619))
- `.install-number`: mesma base visual da `.feature-icon`, mas com `font-weight: 800`
- Hover no `.install-card`: `translateY(2px)`; Active: `translateY(6px)` e borda inferior 0

**Aviso de segurança do Windows (estilo inline)** ([index.html](file:///e:/Dahora/dahora-app/index.html#L405-L434))
- Wrapper do aviso: `margin-top: 3rem`, `max-width: 800px`, background `rgba(245,158,11,0.05)`, `border-left: 5px solid #f59e0b`, `padding: 1.5rem`, `font-size: 0.95rem`
- Título: `font-size: 1.1rem`, cor `#f59e0b`, `gap: 0.75rem`, `margin-bottom: 1rem`
- `details/summary`: `font-size: 0.9rem`, cor `#d97706`, `gap: 0.5rem`
- Imagens: `width: 300px`, `border-radius: 0.5rem`, `box-shadow: 0 4px 6px rgba(0,0,0,0.2)`

## Download (Seção #download)

**Markup** ([index.html](file:///e:/Dahora/dahora-app/index.html#L440-L461))
- `section#download.download` → `.download-box` → `h2`, `p`, `.btn-download-large`, `.download-trust-links`, `.download-footer`
- O botão de download aponta para `.../releases/latest/download/DahoraApp_latest.zip` (arquivo “latest”, sem versão no nome)

## Executável & Segurança (Seção #seguranca-executavel)

**Markup** ([index.html](file:///e:/Dahora/dahora-app/index.html#L341-L365))
- `section#seguranca-executavel.section` → `.features-grid` com 3 `.feature-card`
- O card “Como verificar” inclui link para `.../releases` (GitHub Releases) e instrução de build `py build.py`

**Background e padding da seção** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L211-L220))
- `.download`: `padding: 6rem 2rem`, background em 3 camadas (radial + radial + linear), `color: white`

**Box central (glass)** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L232-L246))
- `.download-box`: `max-width: 900px`, `text-align: center`, `border-radius: 20px`
- Background: `rgba(15,23,42,0.35)`, borda `rgba(255,255,255,0.12)`
- Padding: `3rem 2.25rem`, sombra `0 20px 40px rgba(0,0,0,0.25)`

**Links de confiança** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L258-L280))
- `.download-trust-links`: `display:flex`, `gap: 0.75rem 1.25rem`, `font-size: 0.9rem`, `opacity: 0.8`
- Links: `color rgba(255,255,255,0.7)`, `border-bottom: 1px dotted rgba(255,255,255,0.3)`

**Botão grande** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L303-L315))
- `.btn-download-large`: `font-size: 1.25rem`, `padding: 1.2rem 3.5rem`, `margin-bottom: 2.5rem`
- Sombra: `0 10px 20px -5px rgba(255,69,0,0.4)`
- Hover: `translateY(-3px) scale(1.02)` e sombra mais forte

**Rodapé do download** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L362-L387))
- `.download-footer`: `font-size: 0.9rem`, `opacity: 0.8`, `margin-top: 2rem`, `padding-top: 1rem`
- `code`: `padding: 0.4rem 1rem`, `border-radius: 6px`, fonte `Fira Code`, `color: #fca5a5`

## Doações (Seção #donate)

**Markup** ([index.html](file:///e:/Dahora/dahora-app/index.html#L464-L517))
- `section#donate.donate-section` → `.donate-container` → `.donate-header` → `.donate-grid` → `.donate-qr-box` → `.donate-note-box`

**Background, padding e container** ([donate.css](file:///e:/Dahora/dahora-app/landing/donate.css#L6-L20))
- `.donate-section`: background em gradiente claro, `padding: 4rem 2rem`
- Dark mode: background em gradiente `#1e293b → #0f172a`
- `.donate-container`: `max-width: 900px`, `padding: 0 1rem`

**Título e subtítulo** ([donate.css](file:///e:/Dahora/dahora-app/landing/donate.css#L22-L47))
- `.donate-title`: `font-size: 2rem`, `margin-bottom: 0.5rem`
- `.donate-subtitle`: `font-size: 1rem`

**Grid de cartões** ([donate.css](file:///e:/Dahora/dahora-app/landing/donate.css#L49-L54))
- `.donate-grid`: `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))`, `gap: 1.5rem`

**Cartão** ([donate.css](file:///e:/Dahora/dahora-app/landing/donate.css#L56-L84))
- `.donate-card`: `padding: 1.75rem 1.5rem`, `border-radius: 10px`, `box-shadow: 0 2px 8px rgba(0,0,0,0.06)`
- Hover: `transform: translateY(-5px)` e sombra `0 8px 16px rgba(0,0,0,0.1)`

**QR box** ([donate.css](file:///e:/Dahora/dahora-app/landing/donate.css#L125-L214))
- `.donate-qr-box`: `padding: 2rem`, `border-left: 4px solid #4CAF50`, `border-radius: 10px`
- `.donate-qr-flex`: `display:flex`, `gap: 6rem`, `flex-wrap: wrap`, `justify-content: center`
- `.donate-qr-img`: `width: 150px`
- `.donate-pix-key`: `font-size: 0.8rem`, `font-family: monospace`, `max-width: 200px`

## FAQ (Seção #faq)

**Markup** ([index.html](file:///e:/Dahora/dahora-app/index.html#L520-L609))
- `section#faq.faq.section.section-alt` → `.faq-container` → `.faq-item` (com `button.faq-question` e `.faq-answer`)

**Padding da seção** ([faq.css](file:///e:/Dahora/dahora-app/landing/faq.css#L3-L6))
- `.faq`: `padding: 5rem 2rem`

**Container** ([faq.css](file:///e:/Dahora/dahora-app/landing/faq.css#L8-L11))
- `.faq-container`: `max-width: 800px`, centralizado

**Pergunta** ([faq.css](file:///e:/Dahora/dahora-app/landing/faq.css#L18-L32))
- `.faq-question`: `padding: 1.25rem 0`, `font-size: 1.05rem`, `font-weight: 600`, `display:flex`, `justify-content: space-between`

**Resposta (colapsável)** ([faq.css](file:///e:/Dahora/dahora-app/landing/faq.css#L49-L61))
- `.faq-answer`: `max-height: 0`, `overflow: hidden`, `transition: max-height 0.3s ease-out`, `font-size: 0.95rem`, `line-height: 1.6`
- `.faq-item.active .faq-answer`: `max-height: 500px` e `padding-bottom: 1.25rem`

**Header do FAQ com override inline** ([index.html](file:///e:/Dahora/dahora-app/index.html#L522-L525))
- `.section-header` do FAQ usa `style="... margin-bottom: 3rem"` (diferente do padrão 3.5rem)

## Developer (Seção #about)

**Markup** ([index.html](file:///e:/Dahora/dahora-app/index.html#L639-L664))
- `section#about.developer-section.section-dark` → `.dev-container` → `.dev-image-wrapper`/`.dev-avatar-img` e `.dev-content`

**Seção** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L476-L490))
- `.developer-section`: `padding: 80px 20px`, `background-color: #0B0F19`, `color: #ECEFF4`

**Card/container** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L491-L505))
- `.dev-container`: `max-width: 1000px`, `border-radius: 24px`, `padding: 3.5rem`, `gap: 3.5rem`, `box-shadow: 0 15px 60px rgba(0,0,0,0.25)`

**Avatar** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L526-L548))
- `.dev-avatar-img`: `180x180px`, `border-radius: 20px`, `transform: rotate(-3deg)`
- Hover do container: `scale(1.05) translateY(-5px)` e glow sutil `rgba(255,69,0,0.2)`

**Textos** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L646-L683))
- `.dev-label`: `font-size: 0.9rem`, `font-weight: 600`, `letter-spacing: 2px`
- `.dev-name`: `font-size: 2.5rem`, `font-weight: 800`, `line-height: 1.1`
- `.dev-role`: `font-size: 1.1rem`
- `.dev-bio`: `font-size: 1rem`, `line-height: 1.6`, `max-width: 600px`

**Social buttons (tecla 48px)** ([styles.css](file:///e:/Dahora/dahora-app/landing/styles.css#L690-L737))
- `.social-btn`: `48x48px`, `border-radius: 12px`, borda com `border-bottom-width: 3px`
- Hover: `translateY(2px)`; Active: `translateY(5px)` e `border-bottom-width: 0`

## Footer

**Markup** ([index.html](file:///e:/Dahora/dahora-app/index.html#L666-L721))
- `footer.main-footer` → `.footer-content` com colunas: `.footer-brand`, `.footer-links`, `.footer-social` → `.footer-bottom`
- “Links Rápidos”: Recursos, Download, FAQ, Segurança.

**Estilos base** ([footer.css](file:///e:/Dahora/dahora-app/landing/footer.css#L2-L16))
- `.main-footer`: `padding: 60px 40px 20px`, background gradiente `#1e293b → #0f172a`
- `.footer-content`: grid `40% 30% 30%`, `gap: 40px`, `max-width: 1200px`

**Tipografia do footer** ([footer.css](file:///e:/Dahora/dahora-app/landing/footer.css#L25-L44))
- `.footer-brand p`: `font-size: 14px`, `line-height: 1.6`
- Títulos: `font-size: 16px`, `font-weight: 600`, `height: 32px`, `display:flex`, `align-items:center`

**Links e ícones** ([footer.css](file:///e:/Dahora/dahora-app/landing/footer.css#L52-L91))
- Links: `font-size: 14px`, hover sublinha
- `.social-icons a`: `44x44px`, `border-radius: 8px`, hover com `transform: translateY(-2px)`

**Observação: inline styles no HTML**
- Existem overrides inline no footer (ex.: tamanhos e cores em `.brand`, `.logo`, `h4`, textos do `.footer-bottom`) ([index.html](file:///e:/Dahora/dahora-app/index.html#L670-L720))

## Interações (JS)

**FAQ toggle** ([script.js](file:///e:/Dahora/dahora-app/landing/script.js#L4-L18))
- Clique em `.faq-question` alterna classe `.active` no `.faq-item` (e remove `.active` dos demais).

**Spotlight (mouse)**
- Cards `.feature-card`: atualiza CSS vars `--x` e `--y` no elemento ([script.js](file:///e:/Dahora/dahora-app/landing/script.js#L21-L33)).
- Seções `.section-dark`: atualiza CSS vars `--mx` e `--my` ([script.js](file:///e:/Dahora/dahora-app/landing/script.js#L35-L46)).

**Menu mobile (implementado inline no HTML)**
- Alterna `.active` em `#nav-menu.nav-menu` e `#menu-overlay.menu-overlay` ([index.html](file:///e:/Dahora/dahora-app/index.html#L734-L759)).

## Breakpoints / Responsividade

**992px** ([responsive.css](file:///e:/Dahora/dahora-app/landing/responsive.css#L7-L15))
- `.hero-title`: `font-size: 3rem`
- `.install-grid`: vira `repeat(2, 1fr)`

**768px** ([responsive.css](file:///e:/Dahora/dahora-app/landing/responsive.css#L17-L163))
- Nav vira drawer: `.nav-menu` `position: fixed`, `width: 80%` (máx 300px), `height: 100vh`, `right: -100%` → `.active` `right: 0`
- `.hero`: `padding: 6rem 2rem 4rem`
- `.hero-title`: `font-size: 2.5rem`, `line-height: 1.2`
- `.hero-subtitle`: `font-size: 1.1rem`, `line-height: 1.5`, `padding: 0 1rem`
- `.hero-buttons`: coluna, `gap: 1rem`, `padding: 0 2rem`
- `.section`: `padding: 3.5rem 1.5rem`; `.section-title`: `font-size: 2rem`
- `.features-grid`: 1 coluna; `.install-grid`: 1 coluna
- `.download`: `padding: 3.5rem 1.5rem`; `.download-info`: coluna
- `.dev-container`: coluna, `padding: 2rem`, `gap: 2rem`; `.dev-name`: `font-size: 1.8rem`; `.dev-bio`: `0.95rem`

**600px (Hero badges)** ([dark-sections.css](file:///e:/Dahora/dahora-app/landing/dark-sections.css#L134-L144))
- `.hero-badge-item`: `width: calc(33.333% - 0.5rem)` e `font-size: 0.75rem`
- Ícone do badge: `42x42px`

**900px (Process flow)** ([process.css](file:///e:/Dahora/dahora-app/landing/process.css#L176-L217))
- `.process-flow`: vira coluna, `gap: 2rem`
- `.process-step`: vira layout em linha (row), `max-width: 400px`, `padding: 1.5rem`
- `.step-arrow`: gira 90°

**520px (Process flow)** ([process.css](file:///e:/Dahora/dahora-app/landing/process.css#L219-L242))
- `.process-step`: volta para layout em coluna (centralizado) para evitar conteúdo espremido

**Footer 768px e 480px** ([footer.css](file:///e:/Dahora/dahora-app/landing/footer.css#L143-L214))
- 768px: footer vira 1 coluna; padding reduz; fontes do bottom menores
- 480px: padding reduz mais; sem margem superior; ícones sociais 40px; títulos 14px; links 13px

