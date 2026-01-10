# 📜 HISTÓRICO DE DESENVOLVIMENTO - DAHORA APP

**Projeto:** Dahora App - System tray para Data/Hora  
**Última atualização:** 10 de janeiro de 2026

> Navegação: [Índice](INDEX.md) • [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

> Nota: o **histórico narrativo** fica aqui; o registro oficial de mudanças por versão fica no [CHANGELOG.md](../CHANGELOG.md).

---

## 📋 ÍNDICE

1. [v0.2.10 - Patch (manifest + rebuild)](#v0210---patch-manifest--rebuild) 🚀 **ATUAL**
2. [v0.2.8 - Documentação (revisão)](#v028---documentação-revisão)
3. [v0.2.7 - Documentação & Landing](#v027---documentação--landing)
3. [v0.2.6 - Configurações Avançadas na UI & Monitoramento Configurável](#v026---configurações-avançadas-na-ui--monitoramento-configurável)
4. [v0.2.5 - Privacidade (DPAPI) & Ajustes de UI/Landing](#v025---privacidade-dpapi--ajustes-de-uilanding)
5. [v0.2.3 - Documentação Unificada & Release](#v023---documentação-unificada--release)
6. [v0.2.2 - Produtividade & Dark Mode Web](#v022---produtividade--dark-mode-web)
7. [v0.2.0 - Revolução: Cola Automaticamente](#v020---revolução-cola-automaticamente)
8. [Migração CSS (Fases 1-3)](#migração-css-fases-1-3)
9. [Correção de Ícone](#correção-de-ícone)
10. [Padronização do Projeto](#padronização-do-projeto)
11. [Customizações de UI](#customizações-de-ui)

---

## 🚀 V0.2.10 - PATCH (MANIFEST + REBUILD)

**Data:** 10/01/2026  
**Status:** ✅ COMPLETA

### ✨ Principais Mudanças

- Manifest do Windows alinhado com a versão do app.
- Release gerado para `v0.2.10` com artefatos em `dist/`.

---

## 🚀 V0.2.9 - RELEASE (VERSÃO ALINHADA)

**Data:** 10/01/2026  
**Status:** ✅ COMPLETA

### ✨ Principais Mudanças

- Versão bump (0.2.8 → 0.2.9) alinhada em app, landing e documentação.
- Release gerado para `v0.2.9` com artefatos em `dist/`.

---

## 🚀 V0.2.8 - DOCUMENTAÇÃO (REVISÃO)

**Data:** 09/01/2026  
**Status:** ✅ COMPLETA

### ✨ Principais Mudanças

- Versão bump (0.2.7 → 0.2.8) alinhada na documentação.
- Exemplos em `docs/RELEASE.md` padronizados com `X.Y.Z` para evitar hardcode por versão.
- Atualização de índices e políticas (docs/INDEX, PRIVACY, SECURITY, PRD, ROADMAP).

---

## 🚀 V0.2.7 - DOCUMENTAÇÃO & LANDING

**Data:** 08/01/2026  
**Status:** ✅ COMPLETA

### ✨ Principais Mudanças

- Versão bump (0.2.6 → 0.2.7) propagada em docs, manifesto e landing.
- Ajustes pontuais na landing: enquadramento da foto do dev e textos de versão/novidades.

---

## 🚀 V0.2.6 - CONFIGURAÇÕES AVANÇADAS NA UI & MONITORAMENTO CONFIGURÁVEL

**Data:** 05/01/2026  
**Status:** ✅ COMPLETA

### ✨ Principais Mudanças

- Exposição de configurações avançadas na UI moderna (logs, prewarm da UI e cache do menu do tray).
- Campo de descrição opcional para atalhos personalizados (melhor identificação/organização).
- Correção para que o monitoramento do clipboard respeite as configurações do usuário (intervalo e limiar de inatividade).

---

## 🚀 V0.2.5 - PRIVACIDADE (DPAPI) & AJUSTES DE UI/LANDING

**Data:** 02/01/2026  
**Status:** ✅ COMPLETA

### ✨ Principais Mudanças

- Correção de persistência do histórico do clipboard em cenários onde DPAPI falha ao migrar arquivo antigo.
- Ajustes na UI moderna: melhoria do fluxo de busca e remoção de controles não necessários na janela Sobre.
- Refinos na landing (`index.html`): badges e textos alinhados (mensagem de privacidade como “Totalmente offline”).

---

## 🚀 V0.2.3 - DOCUMENTAÇÃO UNIFICADA & RELEASE

**Data:** 30/12/2025  
**Status:** ✅ COMPLETA

### ✨ Principais Mudanças

- Documentação consolidada e padronizada em `docs/`.
- Guia de release atualizado (build, ZIP e Git LFS): [docs/RELEASE.md](RELEASE.md).
- Roadmap simplificado em alto nível: [docs/ROADMAP.md](ROADMAP.md).
- Remoção de documentos redundantes/obsoletos que não refletiam mais o estado atual.

---

## 🚀 V0.2.2 - PRODUTIVIDADE & DARK MODE WEB

**Data:** 29/11/2025
**Status:** ✅ COMPLETA

### ✨ Principais Mudanças

#### 1. **Foco em Produtividade**
- Refinamento da comunicação: foco na utilidade real (colar timestamps) em vez de apenas estética.
- Ajustes na Landing Page para destacar "Mais Eficiência" e "Workflow Invisível".

#### 2. **Landing Page com Dark Mode**
- Implementação completa de tema escuro na documentação web (`index.html`).
- Toggle button (Sol/Lua) na barra de navegação.
- Persistência de preferência do usuário (localStorage).
- Ajustes de contraste para garantir legibilidade em ambos os temas.

#### 3. **Distribuição via Git LFS**
- Binários `DahoraApp_v*.exe` (e, posteriormente, `DahoraApp_v*.zip`) hospedados diretamente no repositório via Git LFS.
- Link de download direto (`raw/main/...`), facilitando o acesso sem depender de releases manuais.
- Configuração de `.gitattributes` para rastrear binários.

#### 4. **Organização de Arquivos**
- Scripts utilitários movidos para `scripts/`.
- Assets de imagem movidos para `assets/`.
- Limpeza da raiz do projeto.

#### 5. **Polimento de UI (Desktop)**
- **Ícone do App**: Correção na exibição do ícone nas janelas de Configurações, Busca e Sobre (agora carrega corretamente do executável PyInstaller).
- **Tela Sobre**: Redesign completo com logo em destaque, versão atualizada, links para GitHub/Site e layout centralizado.
- **Configurações & Busca**: Melhorias significativas no layout (padding, espaçamento, alinhamento) para uma aparência mais profissional e nativa.

### 🛠️ Arquivos Modificados

- `index.html`: Adicionado JS de tema, novos textos, link LFS.
- `landing/styles.css` & `variables.css`: Refatoração para CSS Variables.
- `README.md`: Atualização completa de estrutura e foco.
- `dahora_app/ui/*.py`: Atualizações de layout e ícones em todas as janelas.
- `.gitattributes`: Configuração LFS.

---

## 🚀 V0.2.0 - REVOLUÇÃO: COLA AUTOMATICAMENTE!

**Data:** 05/11/2025  
**Status:** ✅ COMPLETA - REVOLUCIONÁRIA!

### 🔥 Mudança de Paradigma

**ANTES (v0.1.x):**
```
CTRL+SHIFT+1 → Copia timestamp para clipboard → Usuário dá CTRL+V
```

**AGORA (v0.2.0):**
```
CTRL+SHIFT+1 → COLA timestamp DIRETAMENTE onde o cursor está! ✨
```

### ✨ Principais Mudanças

#### 1. **Colagem Automática**
- Atalhos customizados colam timestamp diretamente onde cursor está
- Sistema salva clipboard atual, cola e restaura automaticamente
- Zero interrupção no workflow do usuário
- Notificações desativadas (você já vê o texto!)

#### 2. **Atalhos Personalizados Ilimitados**
- CRUD completo (Adicionar, Editar, Remover)
- Cada atalho com prefixo individual
- Interface de detecção automática de teclas
- Habilitar/desabilitar individualmente
- Preview em tempo real

#### 3. **Interface Windows 11 Nativa**
- 5 abas: Atalhos Personalizados, Formato, Notificações, Teclas de Atalho, Info
- Botões padrão Windows (OK azul + Cancelar)
- Fonte monoespaçada (Consolas) no listbox
- Janela compacta 600x500

#### 4. **Histórico Inteligente**
- Guarda apenas textos copiados pelo usuário
- Timestamps NÃO poluem mais o histórico
- Foco em utilidade, não quantidade

#### 5. **Configuração Total**
- Caracteres de delimitação configuráveis [ ] → << >>
- Formato de data/hora customizável
- Teclas de busca e refresh dinâmicas no menu
- Aba Info com documentação integrada

### 🛠️ Arquivos Modificados

**Novos:**
- `dahora_app/ui/custom_shortcuts_dialog.py` (686 linhas)
- `dahora_app/ui/about_dialog.py` (121 linhas)
- `dahora_app/ui/styles.py` (utilitários)

**Modificados:**
- `main.py` - Cola automática + preserva clipboard
- `dahora_app/settings.py` - Novos parâmetros
- `dahora_app/datetime_formatter.py` - Brackets configuráveis
- `dahora_app/clipboard_manager.py` - Logs reduzidos
- `dahora_app/ui/menu.py` - Atalhos dinâmicos

### 📊 Estatísticas

- **21 arquivos modificados**
- **+3,477 inserções**
- **-126 deleções**
- **9 arquivos novos**

### 🎯 Impacto

- ⚡ **Workflow 3x mais rápido** - Um atalho faz tudo
- 🧹 **Logs 120x menos verbosos** - Performance otimizada
- 🔇 **Zero notificações irritantes** - Experiência limpa
- 🔄 **Clipboard preservado** - Não perde o que copiou

---

## 🎨 MIGRAÇÃO CSS (FASES 1-3)

### **FASE 1: AUDITORIA E PLANEJAMENTO**

**Data:** 04/11/2025  
**Status:** ✅ COMPLETA

#### Objetivo:
Auditar código atual e planejar migração de CSS inline para arquivos externos.

#### Estrutura Original:
```
index.html (1356 linhas totais)
├── HEAD (linhas 1-9)
├── STYLE INLINE (linhas 10-750) ~740 linhas CSS
│   ├── Reset & Base
│   ├── CSS Variables :root
│   ├── Typography
│   ├── Header & Navigation
│   ├── Hero Section
│   ├── Stats Section
│   ├── Features Section
│   ├── Screenshots
│   ├── Download Section
│   ├── Footer
│   ├── Responsive
│   ├── Animations
│   ├── FAQ
│   └── Developer Section
├── HTML (linhas 751-1306)
└── SCRIPT INLINE (linhas 1307-1356) ~50 linhas JS
```

#### Resultado:
- ✅ Auditoria completa realizada
- ✅ Plano de migração definido
- ✅ Estrutura de pastas planejada

---

### **FASE 2: MIGRAÇÃO PARA ARQUIVOS EXTERNOS**

**Data:** 04/11/2025  
**Versão:** 2.1.0  
**Status:** ✅ COMPLETA E TESTADA

#### Objetivo:
Migrar CSS inline do `index.html` para arquivos externos organizados na pasta `landing/`.

#### Estrutura Criada:
```
landing/
├── variables.css      (40 linhas)   - Variáveis CSS
├── styles.css         (550 linhas)  - Estilos principais
├── dark-sections.css  (240 linhas)  - Seções escuras
└── responsive.css     (180 linhas)  - Media queries
```

#### Resultado:
```
ANTES: index.html com 1356 linhas (750 CSS inline)
DEPOIS: index.html com ~600 linhas (só HTML + imports)

Redução: 56% no tamanho do arquivo
```

#### Arquivos Criados:

**1. `landing/variables.css`**
- Variáveis de cores
- Variáveis de tipografia
- Variáveis de espaçamento
- Variáveis de animação

**2. `landing/styles.css`**
- Reset e base
- Tipografia
- Header e navegação
- Hero section
- Stats section
- Features section
- Download section
- Footer
- Animações

**3. `landing/dark-sections.css`**
- Estilos para seções escuras
- Gradientes especiais
- Contraste otimizado

**4. `landing/responsive.css`**
- Media queries para mobile
- Media queries para tablet
- Media queries para desktop

#### Customizações Preservadas:
- ✅ Gradiente laranja→vermelho nos botões CTA
- ✅ Efeito "facho de luz" nos cards
- ✅ Ícones monocromáticos com hover laranja
- ✅ Código `py build.py` com contraste
- ✅ Todas as animações e transições

---

### **FASE 3: LIMPEZA E OTIMIZAÇÃO**

**Data:** 04/11/2025  
**Versão:** 0.1.2  
**Status:** 🔄 EM PROGRESSO

#### Etapa 1: Remover CSS Inline Duplicado ✅
- Removidas 763 linhas de CSS inline do `index.html`
- Arquivo reduzido de 1366 linhas → 603 linhas (redução de 56%)
- Mantidos apenas os imports CSS externos
- Atualizado comentário para "FASE 3: CSS 100% EXTERNO"

**Resultado:**
```html
<!-- ✅ FASE 3: CSS 100% EXTERNO (CSS INLINE REMOVIDO) -->
<link rel="stylesheet" href="landing/variables.css">
<link rel="stylesheet" href="landing/styles.css">
<link rel="stylesheet" href="landing/dark-sections.css">
<link rel="stylesheet" href="landing/responsive.css">
```

#### Etapa 2: Remover !important Desnecessários 🔄
**Status:** EM PROGRESSO

**Objetivo:** Remover declarações `!important` que foram adicionadas temporariamente para sobrescrever CSS inline.

**Arquivos a revisar:**
- `landing/styles.css` (3 ocorrências)
- `landing/dark-sections.css` (5 ocorrências)

#### Etapa 3: Substituir Emojis por Ícones SVG ⏳
**Status:** PENDENTE

**Objetivo:** Substituir emojis por ícones SVG para melhor controle de estilo e consistência.

**Emojis a substituir:**
- 🚀 (Rápido e Eficiente)
- ⚙️ (Personalizável)
- 🔒 (Seguro e Privado)
- 📋 (Histórico)
- ⌨️ (Atalhos)
- 🎨 (Interface)

---

## 🔧 CORREÇÃO DE ÍCONE

**Data:** 04/11/2025  
**Problema:** Build estava usando ícone laranja antigo gerado por `create_icon.py`  
**Solução:** Usar `icon.ico` (azul) como padrão da indústria

### Arquivos Modificados:

**1. build.py**
- ❌ Removida função `ensure_icon_exists()` que gerava ícone laranja
- ✅ Adicionada verificação simples se `icon.ico` existe
- ✅ PyInstaller agora usa `--icon=icon.ico`
- ✅ PyInstaller agora empacota `--add-data=icon.ico;.`

**2. main.py**
- ✅ Usa `icon.ico` (padrão da indústria)
- ✅ Mensagem de aviso atualizada

**3. dahora_app.py**
- ✅ Todas as referências agora usam `icon.ico`
- ✅ Comentários atualizados

**4. dahora_app/ui/icon_manager.py**
- ✅ `load_icon()` agora procura `icon.ico`
- ✅ `get_icon_path()` retorna caminho para `icon.ico`

### Limpeza:
- ✅ Removido `create_icon.py` (gerava ícone laranja)
- ✅ Renomeado `icone-novo.ico` → `icon.ico` (padrão)
- ✅ Limpado cache `build/` e `dist/`

### Resultado:
```
ANTES: Ícone laranja (relógio digital)
DEPOIS: Ícone azul (logo "D" moderno)
```

---

## 📋 PADRONIZAÇÃO DO PROJETO

**Data:** 04/11/2025  
**Objetivo:** Seguir padrões internacionais de nomenclatura mantendo conteúdo em PT-BR

### Arquivos Renomeados (8):

| Antes (PT-BR) | Depois (EN) |
|---------------|-------------|
| `ANALISE_PRECIFICACAO.md` | `PRICING.md` |
| `CHECKLIST_MELHORIAS.md` | `ROADMAP.md` |
| `CORRECAO_ICONE.md` | `ICON_FIX.md` |
| `CUSTOMIZACOES_ATUAIS.md` | `CUSTOMIZATIONS.md` |
| `FASE2_COMPLETA.md` | `PHASE2_COMPLETE.md` |
| `FASE3_PROGRESSO.md` | `PHASE3_PROGRESS.md` |
| `MIGRACAO_PLANO.md` | `MIGRATION_PLAN.md` |
| `MUDANCAS_PARA_TESTAR.md` | `TESTING_CHANGES.md` |

### Arquivos Deletados (8):

- `index.html.backup` - Backup temporário
- `001_pyinstaller.spec` - Arquivo de teste
- `001_serve.ps1` - Arquivo de teste
- `dahora_app_v0.0.6.spec` - Versão antiga
- `dahora_app_v0.0.7.spec` - Versão antiga
- `landing-old/` - Diretório de backup
- `__pycache__/` - Cache Python
- `create_icon.py` - Gerava ícone laranja

### Padrões Estabelecidos:

**Nomenclatura:**
- ✅ Nomes de arquivos em **inglês** (padrão internacional)
- ✅ Conteúdo dos docs em **PT-BR** (projeto brasileiro)
- ✅ Código Python: `snake_case`
- ✅ CSS: `kebab-case`
- ✅ Ícones: `icon.ico` (padrão universal)

**Estrutura:**
```
dahora-app/
├── 📄 *.md (nomes em inglês, conteúdo PT-BR)
├── 🐍 *.py (snake_case)
├── 🎨 *.css (kebab-case)
├── 🖼️ icon.ico (padrão)
└── 📂 dahora_app/ (snake_case)
```

---

## 🎨 CUSTOMIZAÇÕES DE UI

### 1. Gradiente Laranja→Vermelho nos Botões CTA

**Variáveis CSS:**
```css
--gradient-orange-red: linear-gradient(135deg, #FF6B00 0%, #FF4500 100%);
--gradient-orange-red-hover: linear-gradient(135deg, #FF4500 0%, #CC3700 100%);
```

**Aplicação:**
- Botão "Baixar Dahora App"
- Botão "Começar Agora"
- Hover com transformação e sombra

### 2. Efeito "Facho de Luz" nos Cards

**Implementação:**
```css
.feature-card::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 800px;
    height: 800px;
    background: radial-gradient(
        circle,
        rgba(255, 255, 255, 0.8) 0%,
        rgba(59, 130, 246, 0.4) 30%,
        transparent 70%
    );
    transform: translate(-50%, -50%);
    opacity: 0;
    transition: opacity 0.6s ease;
    pointer-events: none;
}

.feature-card:hover::before {
    opacity: 1;
}
```

### 3. Ícones Monocromáticos com Hover Laranja

**Estado normal:**
- Ícones em cinza (`grayscale(100%)`)
- Opacidade reduzida

**Estado hover:**
- Ícones coloridos (sem filtro)
- Opacidade total
- Transição suave

### 4. Código com Alto Contraste

**Seção Developer:**
```css
.download code {
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff !important;
    padding: 2px 8px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-weight: 600;
}
```

---

## 📊 RESUMO DE MELHORIAS

### Código:
- ✅ CSS 100% externo (redução de 56% no index.html)
- ✅ Arquivos organizados por função
- ✅ Variáveis CSS centralizadas
- ✅ Código modular e manutenível

### Nomenclatura:
- ✅ Padrões internacionais seguidos
- ✅ Arquivos renomeados para inglês
- ✅ Estrutura profissional

### Ícones:
- ✅ Ícone azul padronizado
- ✅ Processo de build limpo
- ✅ Sem geração automática de ícones

### Limpeza:
- ✅ Arquivos temporários removidos
- ✅ Cache limpo
- ✅ Backups deletados

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ v0.2.10 (estado atual) estabilizado e documentado
2. 🔮 Próximas features em [ROADMAP.md](ROADMAP.md)

---

**📌 Este documento consolida o histórico de desenvolvimento (complementar ao CHANGELOG).**
