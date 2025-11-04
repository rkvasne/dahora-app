# 📋 PLANO DE MIGRAÇÃO CSS/JS - DAHORA APP LANDING PAGE

**Data:** 04/11/2025  
**Versão atual:** index.html com CSS/JS inline (1356 linhas)  
**Objetivo:** Migrar para arquivos separados na pasta `landing/`  
**Status:** ✅ FASE 1 COMPLETA - Auditoria realizada

---

## 📊 AUDITORIA DO CÓDIGO ATUAL

### **Estrutura do index.html:**

```
index.html (1356 linhas totais)
├── HEAD (linhas 1-9)
│   ├── Meta tags
│   └── Link para icon.ico
│
├── STYLE INLINE (linhas 10-750) ~740 linhas CSS
│   ├── Reset & Base (linhas 12-16)
│   ├── CSS Variables :root (linhas 18-50)
│   ├── Typography (linhas 52-63)
│   ├── Header & Navigation (linhas 65-118)
│   ├── Hero Section (linhas 120-248)
│   ├── Stats Section (linhas 250-275)
│   ├── Features Section (linhas 277-470)
│   ├── Screenshots (linhas 472-484)
│   ├── Download Section (linhas 486-527)
│   ├── Footer (linhas 529-558)
│   ├── Responsive (linhas 560-580)
│   ├── Animations (linhas 582-596)
│   ├── FAQ Section (linhas 598-685)
│   └── Developer Section (linhas 687-750)
│
├── HTML BODY (linhas 752-1303) ~551 linhas HTML
│   ├── Header/Nav
│   ├── Hero
│   ├── Recursos Principais
│   ├── Novidades (dark)
│   ├── Detalhes Técnicos
│   ├── Como Instalar
│   ├── Download
│   ├── FAQ
│   ├── Developer
│   └── Footer
│
└── SCRIPT INLINE (linhas 1305-1356) ~51 linhas JS
    ├── Versão log
    ├── toggleFAQ()
    └── Mouse tracking (spotlight)
```

---

## 🎨 MAPEAMENTO CSS INLINE

### **1. CSS VARIABLES (linhas 18-50) - 32 linhas**

```css
:root {
    /* Cores primárias */
    --primary-color: #0078D4;
    --primary-light: #2B88D8;
    --primary-dark: #005A9E;
    --secondary-color: #0C5DAA;
    
    /* Gradiente Laranja → Vermelho (CUSTOMIZAÇÃO RECENTE) */
    --gradient-orange-red: linear-gradient(135deg, #FF6B00 0%, #FF4500 100%);
    --gradient-orange-red-hover: linear-gradient(135deg, #FF4500 0%, #CC3700 100%);
    
    /* Textos */
    --text-dark: #1A1A1A;
    --text-gray: #64748b;
    --text-light: #cbd5e1;
    
    /* Fundos */
    --bg-white: #ffffff;
    --border-color: #e2e8f0;
    --light-bg: #f8fafc;
    --dark-bg: #0f172a;
    --dark-card: #1e293b;
    
    /* Sombras */
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    
    /* Hero (azul escuro original - CUSTOMIZAÇÃO RECENTE) */
    --hero-dark-1: #0B1E3C;
    --hero-dark-2: #0F2E5C;
    --hero-dark-3: #0956A3;
    --glass-bg: rgba(255,255,255,0.14);
    --glass-border: rgba(255,255,255,0.28);
}
```

**Destino:** `landing/variables.css` (NOVO)

---

### **2. RESET & BASE (linhas 12-16, 54-63) - 15 linhas**

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
    color: var(--text-dark);
    overflow-x: hidden;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

**Destino:** `landing/styles.css` (início)

---

### **3. HEADER & NAVIGATION (linhas 65-118) - 53 linhas**

```css
.header { ... }
.nav { ... }
.nav-brand { ... }
.nav-brand img { ... }
.nav-menu { ... }
.nav-link { ... }
.nav-link:hover { ... }
```

**Destino:** `landing/styles.css` (seção Header)

---

### **4. HERO SECTION (linhas 120-248) - 128 linhas**

```css
.hero { ... }
.hero::before { ... }
.hero-container { ... }
.hero-icon { ... }
.hero-title { ... }
.hero-subtitle { ... }
.hero-version { ... }
.hero-badges { ... }
.badge { ... }
.hero-buttons { ... }
.btn { ... }
.btn-primary { ... }
.btn-primary:hover { ... }
.btn-secondary { ... }
.btn-secondary:hover { ... }
```

**Destino:** `landing/dark-sections.css` (Hero é dark)

---

### **5. FEATURES SECTION (linhas 277-470) - 193 linhas**

```css
.section { ... }
.section-alt { ... }
.section-dark { ... }  ← IMPORTANTE: Seções escuras
.container { ... }
.section-header { ... }
.section-title { ... }
.section-subtitle { ... }
.features-grid { ... }
.feature-card { ... }
.feature-card::before { ... }  ← Spotlight effect
.feature-card:hover { ... }
.feature-card:hover .feature-icon { ... }
.feature-icon { ... }
.section-dark .feature-card { ... }
.section-dark .feature-icon { ... }  ← CUSTOMIZAÇÃO: monocromático
.section-dark .feature-card:hover .feature-icon { ... }  ← CUSTOMIZAÇÃO: hover laranja
.install-card:hover .install-number { ... }  ← CUSTOMIZAÇÃO: sem hover nos números
.install-number { ... }
code { ... }
.section-dark code { ... }
```

**Destino:** 
- Base: `landing/styles.css`
- Dark: `landing/dark-sections.css`

---

### **6. DOWNLOAD SECTION (linhas 486-527) - 41 linhas**

```css
.download { ... }  ← Fundo escuro com gradientes laranjas
.download-box { ... }
.download-box h2 { ... }
.download-box p { ... }
.download-info { ... }
.download-detail { ... }
```

**Destino:** `landing/dark-sections.css`

---

### **7. FAQ SECTION (linhas 598-685) - 87 linhas**

```css
.faq { ... }
.faq-container { ... }
.faq-item { ... }
.faq-item:hover { ... }
.faq-question { ... }
.faq-question:hover { ... }
.faq-icon { ... }  ← CUSTOMIZAÇÃO: 0.875rem, opacity 0.5
.faq-item.active .faq-icon { ... }
.faq-question:hover .faq-icon { ... }
.faq-answer { ... }
.faq-item.active .faq-answer { ... }
```

**Destino:** `landing/styles.css` (seção FAQ)

---

### **8. RESPONSIVE (linhas 560-580) - 20 linhas**

```css
@media (max-width: 768px) {
    .nav-menu { display: none; }
    .hero-title { font-size: 2.5rem; }
    .hero-subtitle { font-size: 1.2rem; }
    .features-grid { grid-template-columns: 1fr; }
    .screenshots-grid { grid-template-columns: 1fr; }
}
```

**Destino:** `landing/responsive.css` (NOVO)

---

### **9. ANIMATIONS (linhas 582-596) - 14 linhas**

```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
    animation: fadeInUp 0.6s ease-out;
}
```

**Destino:** `landing/animations.css` (NOVO)

---

## ⚡ MAPEAMENTO JAVASCRIPT INLINE

### **Script Inline (linhas 1305-1356) - 51 linhas**

```javascript
// VERSÃO: 2.0.6 - 2025-11-04-14:06
console.log('🎨 Landing Page v2.0.6 carregada! Ícones monocromáticos ativos.');

// FAQ Toggle
function toggleFAQ(button) {
    const faqItem = button.parentElement;
    const isActive = faqItem.classList.contains('active');
    
    document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
    });
    
    if (!isActive) {
        faqItem.classList.add('active');
    }
}

// Mouse tracking para spotlight effect
document.addEventListener('DOMContentLoaded', () => {
    const darkSections = document.querySelectorAll('.section-dark');
    
    darkSections.forEach(section => {
        section.addEventListener('mousemove', (e) => {
            const rect = section.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            section.style.setProperty('--mx', `${x}%`);
            section.style.setProperty('--my', `${y}%`);
        });
    });

    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            card.style.setProperty('--x', `${x}%`);
            card.style.setProperty('--y', `${y}%`);
        });
    });
});
```

**Destino:** 
- FAQ: `landing/script.js`
- Spotlight: `landing/animations-dark.js` (já existe)

---

## 🎯 CUSTOMIZAÇÕES RECENTES A PRESERVAR

### **✅ Implementadas e funcionando:**

1. **Gradiente Laranja→Vermelho nos botões CTA**
   - Variáveis: `--gradient-orange-red`, `--gradient-orange-red-hover`
   - Aplicado em: `.btn-primary`, `.btn-primary:hover`

2. **Ícones monocromáticos → hover laranja**
   - Seções claras: cinza 30% → hover gradiente laranja
   - Seções escuras: branco → hover gradiente laranja
   - Classes: `.feature-icon`, `.section-dark .feature-icon`

3. **Azul escuro original (landing-old)**
   - Variáveis: `--hero-dark-1: #0B1E3C`, `--hero-dark-2: #0F2E5C`, `--hero-dark-3: #0956A3`
   - Aplicado em: `.hero`, `.section-dark`, `.download`

4. **Fonte Poppins (títulos) + Inter (texto)**
   - Import: Google Fonts
   - Aplicado: `h1-h6 { font-family: 'Poppins' }`, `body { font-family: 'Inter' }`

5. **Ícones 56px, border-radius 8px/12px**
   - `.feature-icon { width: 56px; height: 56px; border-radius: 12px; }`
   - `.btn { border-radius: 8px; }`

6. **Setas FAQ discretas**
   - `.faq-icon { font-size: 0.875rem; opacity: 0.5; }`

7. **python build.py com contraste**
   - `background: rgba(255,255,255,0.25); border: 1px solid rgba(255,255,255,0.3); font-weight: 600;`

8. **Números seção instalar sem hover**
   - Classes: `.install-card`, `.install-number`
   - Hover desabilitado com `!important`

---

## 📂 ESTRUTURA ALVO

```
landing/
├── variables.css          ← NOVO: Todas as variáveis CSS
├── styles.css             ← Base + Components + FAQ
├── dark-sections.css      ← Hero + Seções dark + Download
├── animations.css         ← NOVO: Keyframes e animações
├── responsive.css         ← NOVO: Media queries
├── animations-dark.js     ← Spotlight effect (já existe)
└── script.js              ← FAQ toggle + inicializações
```

---

## 🗺️ PLANO DE EXECUÇÃO

### **FASE 2: MIGRAÇÃO CSS BÁSICO** (Próxima)

**Ordem:**
1. Criar `landing/variables.css` com todas as variáveis
2. Mover Reset & Base para `landing/styles.css`
3. Importar no `index.html`
4. Testar
5. Remover do inline

**Tempo estimado:** 30-45 minutos

### **FASE 3: MIGRAÇÃO CSS SEÇÕES ESCURAS**

**Ordem:**
1. Mover Hero, .section-dark, Download para `landing/dark-sections.css`
2. Preservar customizações (gradientes laranjas, azul escuro)
3. Importar no `index.html`
4. Testar spotlight effect
5. Remover do inline

**Tempo estimado:** 30-45 minutos

### **FASE 4: MIGRAÇÃO JAVASCRIPT**

**Ordem:**
1. Mover toggleFAQ para `landing/script.js`
2. Verificar se spotlight já está em `animations-dark.js`
3. Importar scripts no `index.html`
4. Testar FAQ e spotlight
5. Remover do inline

**Tempo estimado:** 20-30 minutos

### **FASE 5: LIMPEZA FINAL**

**Ordem:**
1. Criar `landing/animations.css` e `landing/responsive.css`
2. Mover conteúdo restante
3. Remover TODO CSS/JS inline
4. Testar TUDO
5. Documentar

**Tempo estimado:** 20-30 minutos

---

## ✅ CHECKLIST FASE 1

- [x] Backup criado (`index.html.backup`)
- [x] Auditoria CSS completa
- [x] Auditoria JavaScript completa
- [x] Customizações documentadas
- [x] Estrutura alvo definida
- [x] Plano de execução criado
- [x] Documento `MIGRACAO_PLANO.md` criado

---

## 📊 ESTATÍSTICAS

| Item | Linhas | Destino |
|------|--------|---------|
| CSS Variables | 32 | `landing/variables.css` |
| Reset & Base | 15 | `landing/styles.css` |
| Header & Nav | 53 | `landing/styles.css` |
| Hero Section | 128 | `landing/dark-sections.css` |
| Features | 193 | `landing/styles.css` + `dark-sections.css` |
| Download | 41 | `landing/dark-sections.css` |
| FAQ | 87 | `landing/styles.css` |
| Responsive | 20 | `landing/responsive.css` |
| Animations | 14 | `landing/animations.css` |
| **Total CSS** | **~583** | **5 arquivos** |
| JavaScript | 51 | `landing/script.js` + `animations-dark.js` |
| **HTML puro** | **~551** | Fica no `index.html` |

---

## 🎯 PRÓXIMOS PASSOS

**Quando estiver pronto para FASE 2:**
1. Avisar que vai começar
2. Eu crio os arquivos e faço as migrações
3. Você testa cada etapa
4. Commitamos juntos

**Tempo total estimado:** 2-3 horas distribuídas em sessões

---

**Status:** ✅ FASE 2 EM TESTE  
**Próximo:** Validar funcionamento → Remover CSS inline duplicado
