# 🎨 CUSTOMIZAÇÕES ATUAIS - DAHORA APP LANDING PAGE

**Data:** 04/11/2025  
**Versão:** 2.0.6  
**Status:** ✅ Todas implementadas e funcionando

---

## 🔥 CUSTOMIZAÇÕES IMPLEMENTADAS

### **1. GRADIENTE LARANJA→VERMELHO NOS BOTÕES CTA**

**Variáveis CSS:**
```css
--gradient-orange-red: linear-gradient(135deg, #FF6B00 0%, #FF4500 100%);
--gradient-orange-red-hover: linear-gradient(135deg, #FF4500 0%, #CC3700 100%);
```

**Aplicação:**
```css
.btn-primary {
    background: var(--gradient-orange-red);
    color: white;
    border: none;
    box-shadow: 0 4px 15px rgba(255, 107, 0, 0.25);
}

.btn-primary:hover {
    background: var(--gradient-orange-red-hover);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(255, 69, 0, 0.4);
}
```

**Onde aparece:**
- Botão "Download Grátis" no Hero
- Botão "Baixar dahora_app_v0.1.0.exe" na seção Download

---

### **2. ÍCONES MONOCROMÁTICOS → HOVER LARANJA**

#### **Seções Claras (fundo branco):**
```css
.feature-icon {
    width: 56px;
    height: 56px;
    background: var(--light-bg);
    border: 2px solid var(--border-color);
    border-radius: 12px;
    filter: grayscale(0.3);  /* Cinza 30% */
}

.feature-card:hover .feature-icon {
    background: var(--gradient-orange-red);  /* Gradiente laranja→vermelho */
    border-color: transparent;
    color: white;
    filter: grayscale(0);
    box-shadow: 0 4px 15px rgba(255, 107, 0, 0.3);
}
```

#### **Seções Escuras (fundo azul escuro):**
```css
.section-dark .feature-icon {
    background: rgba(255, 255, 255, 0.1);    /* Fundo branco suave */
    border-color: rgba(255, 255, 255, 0.2);  /* Borda branca */
    color: rgba(255, 255, 255, 0.9);         /* BRANCO! */
}

.section-dark .feature-card:hover .feature-icon {
    background: var(--gradient-orange-red);  /* Gradiente laranja→vermelho */
    border-color: transparent;
    color: white;
    box-shadow: 0 4px 15px rgba(255, 107, 0, 0.4);
}
```

**Onde aparece:**
- Seção "Recursos Principais" (fundo claro)
- Seção "Novidades do MVP v0.1.0" (fundo escuro)
- Seção "Detalhes Técnicos" (fundo claro)

---

### **3. AZUL ESCURO ORIGINAL (landing-old)**

**Variáveis CSS:**
```css
--hero-dark-1: #0B1E3C;  /* Azul escuro rico */
--hero-dark-2: #0F2E5C;  /* Azul médio-escuro */
--hero-dark-3: #0956A3;  /* Azul vibrante */
```

**Aplicação:**
```css
/* Hero */
.hero {
    background: 
        radial-gradient(900px 600px at 15% -10%, rgba(43,136,216,0.25) 0%, rgba(0,120,212,0.18) 40%, transparent 65%),
        linear-gradient(135deg, var(--hero-dark-1) 0%, var(--hero-dark-2) 55%, var(--hero-dark-3) 100%);
}

/* Seções Dark */
.section-dark {
    background: 
        radial-gradient(900px circle at var(--mx, 50%) var(--my, 50%), rgba(255,107,0,0.08), transparent 40%),
        radial-gradient(1200px circle at 80% 100%, rgba(255,69,0,0.05), transparent 50%),
        linear-gradient(180deg, var(--hero-dark-1) 0%, var(--hero-dark-2) 50%, var(--hero-dark-3) 100%);
}

/* Download */
.download {
    background: 
        radial-gradient(800px circle at 20% 30%, rgba(255,107,0,0.12), transparent 50%),
        radial-gradient(600px circle at 80% 70%, rgba(255,69,0,0.1), transparent 50%),
        linear-gradient(135deg, #0B1E3C 0%, #0F2E5C 50%, #0956A3 100%);
}
```

**Onde aparece:**
- Hero Section
- Seção "Novidades do MVP v0.1.0"
- Seção "Download"

---

### **4. FONTE POPPINS (TÍTULOS) + INTER (TEXTO)**

**Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap');
```

**Aplicação:**
```css
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

**Resultado:**
- Títulos: Poppins (bold, impactante)
- Texto corpo: Inter (legível, clean)

---

### **5. ÍCONES 56PX, BORDER-RADIUS 8PX/12PX**

**Ícones:**
```css
.feature-icon {
    width: 56px;           /* Antes: 60px */
    height: 56px;          /* Antes: 60px */
    border-radius: 12px;   /* Antes: 1rem (16px) */
    font-size: 1.75rem;    /* Antes: 2rem */
}
```

**Botões:**
```css
.btn {
    border-radius: 8px;    /* Antes: 0.75rem (12px) */
}
```

**Inspiração:** link-assistant.com

---

### **6. SETAS FAQ DISCRETAS**

```css
.faq-icon {
    transition: transform 0.3s;
    font-size: 0.875rem;     /* Antes: 1.25rem (30% menor) */
    opacity: 0.5;            /* Antes: 1 (50% transparente) */
    color: var(--text-gray); /* Cinza */
}

.faq-question:hover .faq-icon {
    opacity: 0.7;            /* Hover sutil */
}
```

**Resultado:** Setas menos destacadas, não competem com o texto

---

### **7. PYTHON BUILD.PY COM CONTRASTE**

```css
code {
    background: rgba(255,255,255,0.25);           /* Antes: 0.2 (mais opaco) */
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    border: 1px solid rgba(255,255,255,0.3);      /* NOVO: borda */
    font-weight: 600;                              /* NOVO: bold */
}
```

**Onde aparece:** Seção Download, texto "Ou compile do código-fonte: python build.py"

---

### **8. NÚMEROS SEÇÃO INSTALAR SEM HOVER**

```css
/* Remove hover dos números 1️⃣ 2️⃣ 3️⃣ */
.install-number {
    background: transparent !important;
    border: none !important;
    filter: none !important;
}

.install-card:hover .install-number {
    background: var(--light-bg) !important;
    border-color: var(--border-color) !important;
    color: inherit !important;
    filter: none !important;
    box-shadow: none !important;
}
```

**Resultado:** Números ficam limpos, sem efeito hover estranho

---

## 🎯 GRADIENTES LARANJA SUTIS NOS FUNDOS ESCUROS

**Seções Dark:**
```css
background: 
    radial-gradient(900px circle at var(--mx, 50%) var(--my, 50%), rgba(255,107,0,0.08), transparent 40%),
    radial-gradient(1200px circle at 80% 100%, rgba(255,69,0,0.05), transparent 50%),
    linear-gradient(180deg, #0B1E3C 0%, #0F2E5C 50%, #12407D 100%);
```

**Download:**
```css
background: 
    radial-gradient(800px circle at 20% 30%, rgba(255,107,0,0.12), transparent 50%),
    radial-gradient(600px circle at 80% 70%, rgba(255,69,0,0.1), transparent 50%),
    linear-gradient(135deg, #0B1E3C 0%, #0F2E5C 50%, #0956A3 100%);
```

**Resultado:** Fundos escuros com brilhos laranjas sutis, mantendo escuros

---

## ⚠️ IMPORTANTE PARA MIGRAÇÃO

**Ao migrar para arquivos separados, PRESERVAR:**

1. ✅ Todas as variáveis CSS (especialmente gradientes laranja)
2. ✅ Ícones monocromáticos com hover laranja
3. ✅ Azul escuro original (#0B1E3C, #0F2E5C, #0956A3)
4. ✅ Fontes Poppins + Inter
5. ✅ Tamanhos 56px, border-radius 8px/12px
6. ✅ Setas FAQ discretas
7. ✅ Contraste do python build.py
8. ✅ Números instalar sem hover
9. ✅ Gradientes laranjas sutis nos fundos escuros

---

## 📝 HISTÓRICO DE CUSTOMIZAÇÕES

| Data | Customização | Status |
|------|--------------|--------|
| 04/11/2025 | Gradiente laranja→vermelho botões | ✅ |
| 04/11/2025 | Ícones monocromáticos → hover laranja | ✅ |
| 04/11/2025 | Azul escuro original (landing-old) | ✅ |
| 04/11/2025 | Fonte Poppins + Inter | ✅ |
| 04/11/2025 | Ícones 56px, border-radius 8px/12px | ✅ |
| 04/11/2025 | Setas FAQ discretas | ✅ |
| 04/11/2025 | python build.py com contraste | ✅ |
| 04/11/2025 | Números instalar sem hover | ✅ |

---

**Todas as customizações estão funcionando perfeitamente no `index.html` atual!**
