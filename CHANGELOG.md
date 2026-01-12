# Registro de Mudanças

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Não lançado]

### Corrigido
- Landing (mobile): menu sanduíche sem desfoque nas opções.
- Landing (mobile): “Como Funciona” sem espaçamento excessivo no texto dos passos.
- Landing (mobile): badges do Hero alinhados em 1 linha (3 itens).
- Landing: alternância de fundos pós-Download mais evidente e consistente.
- Landing (mobile): removida faixa escura entre “Sobre o dev” e rodapé.
- Landing (mobile): removido card extra (glass) na seção Download.
- Landing (desktop): seção “Para quem é” ajustada para grid 2×2 (4 cards).

### Documentação
- Template da landing com specs por seção em `docs/LANDING_TEMPLATE.md`.
- Índice de documentação consolidado em `docs/README.md` (remoção de `docs/INDEX.md`).
- Roadmap agora aponta para links diretos de Issues/Discussions.
- Template da landing atualizado (header, hero e “Para quem é”).

### Melhorado
- Landing: tooltips em botões sem texto (tema, idioma e ícones do rodapé).
- Landing (desktop): header com menu menos poluído (itens secundários ocultos).

## [0.2.10] - 2026-01-10

### Corrigido
- Manifest do Windows alinhado com a versão do app.

### Build
- Artefatos de release gerados em `dist/` para `v0.2.10`.

## [0.2.9] - 2026-01-10

### Alterado
- Versão alinhada em docs, landing e metadados do app.

### Build
- Artefatos de release gerados em `dist/` para `v0.2.9`.

## [0.2.8] - 2026-01-09

### Corrigido
- Build (PyInstaller): executável inclui dependências do Pydantic (`pydantic`/`pydantic_core`).

### Documentação
- Revisão geral: versões e referências alinhadas para `0.2.8`.
- Exemplos em `docs/RELEASE.md` padronizados com `X.Y.Z` (sem hardcode por release).

## [0.2.7] - 2026-01-08

### Adicionado
- **Prompt Files para VS Code Copilot** - 17 modos de trabalho em `.github/prompts/`
  - Uso: digite `/` no chat e selecione o modo (ex: `/depurador`, `/seguranca`)
  - Modos: admin, api, arquiteto, banco-dados, depurador, depurador-backend, depurador-devops, depurador-mobile, depurador-web, documentacao, frontend, git, multi-tenant, performance, planejador, qualidade, seguranca

### Corrigido
- Landing: enquadramento da foto do dev na seção "Sobre o dev".

### Documentação
- Atualização de versão (0.2.6 → 0.2.7) em docs, manifesto e landing.
- Consolidado `AGENTS_SETUP.md` no `AGENTS.md` (arquivo removido)
- Removidos arquivos redundantes: `DIAGNOSTIC_REPORT.md`, `UPDATE_SUMMARY.md`, `VALIDATION_CHECKLIST.md`
- Adicionada "Regra de Documentação" no `AGENTS.md` (evitar criar docs desnecessários)
- Atualizado `README.md` para refletir consolidação
- Corrigido `copilot-instructions.md` (linhas duplicadas removidas)
- **Atualizado `AGENTS.md` e `copilot-instructions.md`** - Sintaxe correta para modos (`/comando` em vez de `@agents:`)

## [0.2.6] - 2026-01-05

### Adicionado
- Configurações avançadas expostas na UI (logs, prewarm da UI e cache do menu do tray).
- Campo de descrição opcional para atalhos personalizados.

### Corrigido
- Aplicação efetiva dos valores configuráveis de monitoramento do clipboard (intervalo e limiar de inatividade).

### Documentação
- Atualização geral da documentação (backend + frontend) para refletir as mudanças recentes.
- Landing page atualizada (versão, novidades e contagem de testes).

### Manutenção
- Lint: flake8 ignora `.release_trash/` (artefatos de release).

## [0.2.5] - 2026-01-02

### Corrigido
- Persistência do histórico do clipboard quando DPAPI falha ao carregar arquivo antigo.
- Busca do histórico (UI moderna) executa automaticamente ao abrir.
- Botão minimizar removido da janela Sobre (UI moderna).

### Manutenção
- Build (PyInstaller): inclusão explícita de dependências do DPAPI (win32crypt/pywintypes).

## [0.2.4] - 2025-12-30

### Adicionado
- **Implementação Completa da Fase 6:**
  - Módulo base CallbackManager (265 linhas)
  - 4 implementações de handlers (495 linhas)
  - Testes de integração (370 linhas)
  - 84 novos testes (todos passando)

- **Documentação Consolidada e Unificada:**
  - Novo [docs/README.md](docs/README.md) como ponto central único de navegação
  - Unificado GITHUB_CLI_GUIDE.md (inclui autenticação completa)
  - Removido arquivos redundantes: STATUS.md, GITHUB_TOKEN_SETUP.md, GUIDES/RELEASE_PROCESS.md
  - Simplificado docs/README.md para redirecionar ao INDEX.md
  - Padronizada estrutura e formatação de todos os documentos
  - Guias de início rápido organizados por perfil (Usuário, Desenvolvedor, Manutenedor)
  - Convenções do projeto claramente documentadas

### Alterado
- Estrutura de documentação unificada em todas as pastas
- Removidos arquivos de status redundantes em favor do rastreamento centralizado
- Aprimorado docs/README.md com referências consolidadas

### Melhorado
- Navegação mais clara e intuitiva entre documentos
- Eliminação de redundâncias e informações conflitantes
- Consistência de documentação em todos os arquivos
- Validação de links internos e padronização
- Rastreamento de versão em todos os pontos de documentação

### Métricas
- **Testes:** 266/266 passando (100%)
- **Código:** 4500+ linhas adicionadas
- **Documentação:** 3000+ linhas adicionadas (+ consolidação posterior)
- **Mudanças Quebrantáveis:** ZERO
- **Compatibilidade com Versões Anteriores:** 100% mantida

---

## [0.2.3] - 2025-12-30

### Adicionado
- Índice de documentação unificada e guias em `docs/`.
- Guia de release descrevendo build, empacotamento ZIP e uso de Git LFS.

### Alterado
- Metadados de versão alinhados para `0.2.3` (constantes da app, nome do build, manifesto do Windows).
- Instruções de instalação agora preferem o artefato `.zip`.

### Corrigido
- Diálogos sobre agora renderizam a versão atual da app (sem valor hardcoded).

### Manutenção
- Git LFS agora rastreia artefatos `*.zip` (além de `*.exe`).

## [0.2.3-ui-modernization] - 2025-12-29 🎨 **INTERFACE ULTRA-MODERNA: WINDOWS 11 FLUENT DESIGN**

### 🎨 Modernização Completa da Interface
- **Abas redesenhadas**: Corrigido problema onde aba ativa ficava menor que as outras
  - Padding uniforme (24x14) para todas as abas
  - Remoção de margens desnecessárias (`tabmargins=[0,0,0,0]`)
  - Estados consistentes (selected, active, !active) com cores apropriadas
  - Foco visual removido (`focuscolor='none'`) para visual mais limpo

### ✨ Componentes Aprimorados
- **Scrollbars modernas**: Estilo overlay minimalista
  - Largura reduzida (12px) para visual mais sutil
  - Cores adaptativas com hover states melhorados
  - Background transparente que se mistura ao fundo
  - Setas coloridas que respondem a interações

- **Botões ultra-modernos**: Padding aumentado (24x12) e efeitos visuais
  - Cursor "hand2" em todos os botões para melhor UX
  - Estados hover/pressed mais definidos
  - Cores específicas para Success (#45a049) e Danger (#d32f2f)
  - Remoção completa de foco visual (`focuscolor='none'`)

- **Inputs aprimorados**: Experiência de digitação melhorada
  - Padding generoso (16x12) para melhor usabilidade
  - Cursor colorido (cor de destaque) para melhor visibilidade
  - Estados de foco mais definidos
  - Bordas que respondem dinamicamente ao foco

### 🎯 Aprimoramentos Visuais
- **Cards com elevação**: Simulação de sombras e profundidade
  - Múltiplas bordas sutis para efeito de elevação
  - Background diferenciado para criar hierarquia visual
  - Fallback seguro para cards simples se houver erro

- **Listbox interativa**: Melhor feedback visual
  - Remoção de bordas de seleção (`selectborderwidth=0`)
  - Preparação para efeitos hover (comentado para não interferir)
  - Estilo de ativação removido para visual mais limpo

### 🛠️ Melhorias Técnicas
- **Métodos utilitários aprimorados**:
  - `create_modern_card()`: Agora com simulação de sombra
  - `create_modern_button()`: Efeitos hover personalizados
  - `configure_listbox()`: Configuração mais robusta

- **Testes de modernização**: Scripts de teste criados
  - `scripts/manual_ui_modernization.py`: Teste completo da interface moderna
  - `scripts/manual_shortcut_editor.py`: Teste específico do editor de atalhos
  - Validação de todos os componentes modernizados

### 🎉 Experiência do Usuário
- **Interface mais próxima do Windows 11**: Visual nativo e familiar
- **Menos ruído visual**: Bordas removidas, foco limpo, cores sutis
- **Melhor feedback**: Cursores apropriados, hover states, transições suaves
- **Consistência total**: Todos os componentes seguem o mesmo padrão

### 📁 Arquivos Modificados
- `dahora_app/ui/styles.py`: Melhorias extensivas em todos os componentes
- `scripts/manual_ui_modernization.py`: Novo script de teste da interface
- `scripts/manual_shortcut_editor.py`: Novo teste específico do editor

### 🎯 Resultados
- **Abas com tamanho consistente**: Problema da aba ativa menor resolvido
- **Scrollbars overlay**: Visual moderno similar ao Windows 11
- **Botões responsivos**: Feedback visual imediato em todas as interações
- **Interface profissional**: Visual indistinguível de apps nativos do Windows

## [0.2.2-modern-ui] - 2025-12-29 🎨 **TRANSFORMAÇÃO VISUAL COMPLETA: INTERFACE MODERNA**

### 🎨 Complete UI Overhaul
- **Nova paleta de cores moderna**: Inspirada em VS Code, Discord e aplicações contemporâneas
- **Hierarquia visual aprimorada**: text_bright, text_muted, surface, bg_secondary para melhor organização
- **Cores mais equilibradas**: Transição de tons Windows para paleta moderna e profissional

### ✨ Componentes Redesenhados
- **Botões modernos**: Padding generoso (20x10), estados hover/pressed aprimorados, novos estilos (Success, Danger)
- **Inputs elegantes**: Bordas sólidas, foco destacado, padding interno aumentado (12x8)
- **Cards elevados**: Visual de profundidade com background diferenciado
- **Tabs espaçosas**: Padding aumentado (20x12) com transições visuais suaves

### 📏 Layout Moderno
- **Espaçamento respirável**: Padding generoso em todos os elementos, hierarquia clara (6-48px)
- **Tipografia aprimorada**: Fontes maiores, hierarquia clara (Title 18px, Heading 14px, Default 10px)
- **Novos estilos de texto**: Subtitle, Muted, Large para melhor organização visual

### 🎯 Diálogo de Edição Modernizado
- **Layout em seções**: Organização clara com cards separados para cada seção
- **Cabeçalhos descritivos**: Títulos e textos explicativos para melhor UX
- **Preview destacado**: Card separado para visualização do resultado
- **Botões alinhados**: Posicionamento moderno com espaçamento adequado
- **Janela ampliada**: 500x380 → 600x500 para acomodar novo design

### 🛠️ Métodos Utilitários
- `create_modern_card()`: Cards elevados padronizados
- `create_modern_button()`: Botões consistentes
- `create_section_header()`: Títulos de seção uniformes
- `create_modern_entry()`: Inputs padronizados

### 🎉 Resultado
- Interface completamente modernizada e profissional
- Visual similar a aplicações contemporâneas (VS Code, Discord, etc.)
- Experiência do usuário significativamente melhorada
- Mantém toda a funcionalidade existente

## [0.2.2-color-improvements] - 2025-12-29 🎨 **MELHORIA SIGNIFICATIVA: ESQUEMA DE CORES**

### 🎨 Melhorado
- **Detecção automática de tema**: Agora detecta automaticamente se o Windows está em modo claro ou escuro e aplica o esquema correspondente
- **Modo escuro melhorado**: Background menos escuro (`#121212` → `#1C1C1C`) para reduzir fadiga visual
- **Legibilidade aprimorada**: Texto branco puro (`#E0E0E0` → `#FFFFFF`) e texto secundário mais claro (`#A0A0A0` → `#B3B3B3`)
- **Cores oficiais Windows 11**: Azul accent atualizado para o oficial (`#4CC2FF` → `#0078D4`)
- **Melhor definição visual**: Bordas mais visíveis (`#2b2b2b` → `#323130`) e superfícies mais claras
- **Modo claro otimizado**: Background mais suave (`#F3F3F3` → `#FAFAFA`) e melhor contraste de texto
- **Botões aprimorados**: Botão primário com texto branco sobre azul e hover states mais consistentes

### 🎯 Benefícios
- Melhor legibilidade e contraste em ambos os modos
- Menos fadiga visual com cores mais equilibradas
- Consistência total com as diretrizes de design do Windows 11
- Adaptação automática às preferências do usuário

## [0.2.2-shortcut-editor-fix] - 2025-12-29 🔧 **CORREÇÃO CRÍTICA: EDIÇÃO DE ATALHOS NO FRONTEND**

### 🐛 Corrigido
- **Diálogo de edição de atalhos não abria**: Corrigido problema onde os botões "Adicionar" e "Editar" na aba "Atalhos Personalizados" não abriam o diálogo de edição
- **Janela modal inadequada**: Implementado `grab_set()` para tornar o diálogo adequadamente modal
- **Problemas de visibilidade**: Adicionado `lift()`, `focus_force()` e `topmost` temporário para garantir que o diálogo seja visível
- **Validação de janela pai**: Adicionada verificação se a janela pai existe antes de criar o diálogo
- **Limpeza inadequada**: Implementado `grab_release()` nos métodos de fechar/cancelar

### ✨ Melhorado
- **Atalhos de teclado**: Adicionado Escape (cancelar) e Enter (salvar) no diálogo de edição
- **Mecanismo de fallback**: Se o diálogo principal falhar, usa `simpledialog` como backup
- **Logging detalhado**: Adicionado logs abrangentes para debug do processo de criação do diálogo
- **Protocolo de janela**: Adicionado tratamento adequado do botão de fechar (X)

### 🧪 Testado
- Teste isolado confirmou funcionamento correto do diálogo
- Aplicação principal testada com 3 atalhos personalizados existentes
- Logs confirmam criação e exibição bem-sucedida do diálogo

### 📁 Arquivos modificados
- `dahora_app/ui/shortcut_editor.py`: Melhorias na criação e exibição do diálogo
- `dahora_app/ui/custom_shortcuts_dialog.py`: Logging aprimorado e validação de janela

## [0.2.2-landing-improvements] - 2025-12-29 🎨 **LANDING PAGE: DESIGN & COPY PROFISSIONAL**

### 🎨 Design Improvements
- **Tipografia otimizada**: Melhor contraste de texto e hierarquia visual refinada
- **Espaçamento equilibrado**: Padding reduzido de 10rem para 6rem nas seções
- **Cards mais elegantes**: Border-radius menos arredondado (1rem), sombras mais sutis
- **Ícones refinados**: Tamanho reduzido (56px), bordas menos arredondadas
- **Hover effects**: Movimento sutil com translateY(-2px) para melhor feedback
- **Cores suavizadas**: Gradientes e sombras com opacidade reduzida para visual mais profissional

### ✍️ Copy Optimization
- **Seção Novidades**: Textos 60% mais concisos, eliminando verbosidade
- **Hero Section**: Subtitle mais direta e impactante
- **Tom profissional**: Substituição de palavras informais:
  - "Irritantes" → "Desnecessários"
  - "Adoramos" → "Valorizamos" 
  - "Facilmente" → "Com eficiência"
  - "Basta" → "Apenas"
- **Maiúsculas corrigidas**: CTRL+SHIFT → Ctrl+Shift, VÊ → vê, ÚTEIS → úteis
- **Linguagem técnica**: Vocabulário mais elegante e confiável

### 🌐 Translations Updated
- **Português (pt-BR)**: Textos otimizados e profissionalizados
- **Inglês (en)**: Traduções consistentes com melhorias em português
- **Consistência**: Tom uniforme entre idiomas

### 📱 Responsive Improvements
- **Mobile otimizado**: Hero com padding 6rem, título 2.5rem
- **Seção desenvolvedor**: Avatar menor (120px), textos proporcionais
- **Espaçamento mobile**: Padding de 4rem para 3.5rem

### 🎯 Results
- **40-60% redução** no tamanho dos textos
- **Leitura mais rápida** e escaneabilidade melhorada
- **Visual mais profissional** e confiável
- **Experiência consistente** em todos os dispositivos
- **Todas as animações preservadas**

### 📁 Arquivos modificados
- `index.html`: Copy otimizado e traduções atualizadas
- `landing/variables.css`: Cores e sombras refinadas
- `landing/styles.css`: Espaçamento e componentes otimizados
- `landing/dark-sections.css`: Seções escuras mais elegantes
- `landing/responsive.css`: Mobile melhorado
- `landing/faq.css`: FAQ mais compacto e elegante

---
## [0.2.2-site-update] - 2025-12-29 🌐 **LANDING PAGE: TEXTOS E UX**

### 🔄 Alterado
- **Copywriting Refinado**: Textos da Landing Page (`index.html`) ajustados para serem menos promocionais e mais diretos.
- **Correção de Contraste no FAQ**: Correção de contraste nas respostas do FAQ no modo claro (`landing/faq.css`).
- **Seção Novidades**: Textos dos cards simplificados e padronizados (Sentence Case).
- **SEO**: Meta description atualizada para ser mais informativa e menos "marketing".

---

## [0.2.2] - 2025-11-29 🎨 **MODERNIZAÇÃO UI: WINDOWS 11 FLUENT DESIGN**

### ✨ Adicionado
- **🎨 Design Fluent do Windows 11**:
  - **Inputs Modernos**: Caixas de texto com altura ~32px, padding refinado e cores flat.
  - **Botões Flat**: Sem bordas, cores de fundo distintas (#333333) e hover states suaves.
  - **Botão Primário**: Azul vibrante (#4CC2FF) com texto preto para ações principais.
  - **Scrollbars Invisíveis**: Estilo flat minimalista que se mistura ao fundo.
  - **Cards & Panels**: Remoção de bordas desnecessárias para um visual mais limpo e "clean".
  - **Abas Modernas**: Navegação por abas sem bordas, com destaque de cor no texto.

### 🔄 Alterado
- **Refatoração de Estilos**: Centralização e padronização de todos os estilos em `Windows11Style`.
- **Limpeza de Código**: Remoção do arquivo legado `dahora_app.py`.
- **Organização de Arquivos**: Scripts movidos para `scripts/`, assets para `assets/`.
- **Correção de Bugs**: Fix no `SearchDialog` para usar os novos estilos de Card.

### 🎯 Impacto Visual
- Interface muito mais próxima do **padrão nativo do Windows 11**.
- Menos ruído visual (menos bordas, mais espaço).
- Melhor feedback visual em interações (hover, focus).

---


## [0.2.1] - 2025-11-06 🔧 **FIX: Registro Automático de Atalhos**

### 🐛 Corrigido
- **Registro automático de custom shortcuts**: Atalhos agora são registrados **instantaneamente** ao adicionar/editar
- **Problema anterior**: Atalhos só funcionavam após reiniciar o app
- **Solução**: Implementados wrappers que registram/desregistram hotkeys em tempo real

### ✨ Adicionado
- **`_on_add_custom_shortcut_wrapper()`**: Registra hotkey imediatamente ao adicionar
- **`_on_update_custom_shortcut_wrapper()`**: Re-registra hotkey ao atualizar
- **`_on_remove_custom_shortcut_wrapper()`**: Desregistra hotkey ao remover
- **Import de `Optional`**: Adicionado para type hints nos novos métodos

### 🔄 Alterado
- Custom shortcuts dialog agora usa wrappers com registro automático
- Logs informativos mostram status de registro em tempo real

### 📝 Detalhes Técnicos
- Arquivos modificados: `main.py` (3 novos métodos)
- Versão atualizada em `constants.py`: 0.2.0 → 0.2.1
- Build atualizado: `dahora_app_v0.2.1.spec`

### 🎯 Impacto do Usuário
**ANTES (v0.2.0):**
1. Adiciona atalho CTRL+SHIFT+3
2. Precisa **reiniciar o app** 🔄
3. Atalho funciona

**AGORA (v0.2.1):**
1. Adiciona atalho CTRL+SHIFT+3
2. Atalho funciona **NA HORA!** ⚡

---

## [0.2.0] - 2025-11-05 🚀 **REVOLUÇÃO: COLA AUTOMATICAMENTE!**

### 🔥 BREAKING CHANGES
- **Atalhos agora COLAM diretamente** onde o cursor está (antes apenas copiava)
- **Timestamps não vão mais para o histórico** (desnecessário - sempre pode gerar novo)
- **Comportamento do clipboard mudou** (preservado automaticamente)

### ✨ Adicionado
- **⚡ Colagem Automática**: 
  - Atalhos customizados colam timestamp diretamente onde cursor está
  - Sistema salva clipboard atual, cola e restaura automaticamente
  - Zero interrupção no workflow do usuário
  
- **🎯 Atalhos Personalizados Ilimitados**:
  - CRUD completo para gerenciar atalhos (CTRL+SHIFT+1, CTRL+SHIFT+2, etc.)
  - Cada atalho com seu próprio prefixo personalizado
  - Interface de detecção automática de teclas
  - Habilitar/desabilitar individualmente
  - Preview em tempo real

- **⚙️ Interface Windows 11 Nativa**:
  - 5 abas: Atalhos Personalizados, Formato, Notificações, Teclas de Atalho, Info
  - Botões padrão Windows (OK azul + Cancelar)
  - Fonte monoespaçada (Consolas) no listbox
  - Padding e fontes padrão Microsoft
  - Janela reduzida (600x500) mais compacta

- **🆕 Tela Sobre Estilo Windows**:
  - Design nativo Windows com LabelFrames
  - Link para repositório no GitHub
  - Informações de versão e recursos

- **🔧 Configuração Total**:
  - Caracteres de delimitação configuráveis ([ ] → << >> ou qualquer)
  - Formato de data/hora customizável com códigos strftime
  - Teclas de busca e refresh configuráveis
  - Atalhos dinâmicos exibidos no menu

### 🔄 Alterado
- **📋 Histórico Inteligente**: 
  - Guarda apenas textos copiados pelo usuário (não timestamps)
  - Útil como backup quando Windows clipboard está desabilitado
  - Foco em ser útil, não poluir

- **🔇 Notificações Desativadas para Atalhos**:
  - Você já vê o texto colado - popup seria redundante
  - Experiência mais limpa e rápida
  
- **🧹 Logs Otimizados**:
  - Verbosidade reduzida drasticamente (120x menos logs)
  - Monitor de clipboard silencioso (log apenas a cada 1 minuto)
  - Logs focados em mudanças importantes

- **🎨 Interface Melhorada**:
  - Janela de configurações 600x500 (antes 800x600)
  - Listbox com 10 linhas (antes 15)
  - Labels concisos estilo Windows
  - Sem emojis nos botões

### 🛠️ Corrigido
- Aplicação de atalhos configurados no menu após salvar
- Sincronização de bracket_open/close ao salvar configurações
- Import faltante de `keyboard` e `time` no main.py

### 📚 Documentação
- README.md completamente reescrito para v0.2.0
- Seção de uso atualizada com guia passo a passo
- Landing page (index.html) atualizada com novos recursos
- CHANGELOG.md com entrada detalhada da v0.2.0

### 🎯 Detalhes Técnicos
- Arquivos novos: `custom_shortcuts_dialog.py`, `about_dialog.py`, `styles.py`
- 21 arquivos modificados, 3477 inserções, 126 deleções
- Versão atualizada em todos os pontos: `__init__.py`, `constants.py`, about dialog

---

## [0.1.1] - 2025-11-04 🧹 **LIMPEZA & ORGANIZAÇÃO**

### Alterado
- **📁 Documentação Reorganizada e Limpa**:
  - Criada pasta `docs/` para centralizar documentação técnica
  - Criado `docs/DEVELOPMENT_HISTORY.md` consolidando histórico completo
  - Criado `docs/README.md` como índice da documentação
  - **Deletados 9 documentos redundantes** (conteúdo consolidado)
  - Estrutura final: 4 documentos essenciais (README, DEVELOPMENT_HISTORY, IMPROVEMENTS, PRICING)
  - Raiz do projeto limpa (apenas README.md e CHANGELOG.md)
  
- **🎯 Padronização Completa**:
  - Renomeados 8 documentos de PT-BR para inglês (mantendo conteúdo PT-BR)
  - Ícone padronizado: `icone-novo.ico` → `icon.ico`
  - Removido `create_icon.py` (gerava ícone laranja antigo)
  - Todos os arquivos Python agora usam `icon.ico` diretamente
  
- **🗑️ Limpeza de Arquivos**:
  - Deletados 8 arquivos temporários e backups
  - Removido `landing-old/` e `__pycache__/`
  - Deletados arquivos `.spec` de versões antigas
  - Movidos scripts de teste para `scripts/`

- **📦 Organização de Scripts**:
  - Criada pasta `scripts/` para utilitários
  - Movidos: `rebuild_clean.bat`, `test_menu.py`, `test_minimal.py`
  - Atualizado `rebuild_clean.bat` para versão 0.1.1

### Corrigido
- **🔧 Correção de Ícone**:
  - Build agora usa `icon.ico` (azul) em vez de gerar ícone laranja
  - Removida função `ensure_icon_exists()` do `build.py`
  - Atualizados `main.py`, `dahora_app.py`, `icon_manager.py`
  - Ícone azul padronizado em todo o projeto

### Documentação
- **📚 Documentos Consolidados**:
  - `DEVELOPMENT_HISTORY.md` unifica Fases 1-3, correções e padronizações
  - `ORGANIZATION_SUMMARY.md` documenta reorganização
  - `STANDARDIZATION.md` estabelece padrões do projeto
  - README.md atualizado com seção de documentação

---

## [0.1.0] - 2025-11-04 🎉 **MVP RELEASE**

### 🎯 MVP Completo!
Esta versão marca a conclusão do **MVP (Minimum Viable Product)** do Dahora App com todas as funcionalidades essenciais implementadas, testadas e documentadas.

### Adicionado
- **🔍 Busca no Histórico (Tarefa 13)**:
  - Janela moderna de busca com Tkinter (265 linhas)
  - Busca em tempo real (KeyRelease) - digita e filtra instantaneamente
  - Exibe timestamp formatado: `[DD/MM/YYYY HH:MM]`
  - Double-click para copiar item selecionado
  - Listbox com scrollbar para navegação
  - Contador de resultados encontrados
  - Atalho `F5` para refresh manual
  - Atalho `ESC` para fechar janela
  - **Hotkey global `Ctrl+Shift+F`** para abrir busca de qualquer lugar
  - Item "Buscar no Histórico" no menu do system tray
  - Callbacks configuráveis: get_history, copy, notification
  
- **⚙️ Configurações Avançadas (Tarefa 11)**:
  - Janela completa de configurações com 4 abas (259 linhas)
  - **Aba Geral**: Prefixo e formato de data/hora personalizável
  - **Aba Histórico**: Máximo de itens (10-1000), intervalos de monitoramento (0.5s-60s), threshold idle (5s-300s)
  - **Aba Notificações**: Habilitar/desabilitar, duração customizável (1-15s)
  - **Aba Atalhos**: Hotkeys personalizáveis para copy_datetime e refresh_menu
  - Validação completa de todos os campos com feedback visual
  - Botão "Restaurar Padrões" funcional
  - **Aplicação SEM RESTART** (exceto hotkeys - aviso automático quando necessário)
  - Salva automaticamente em `settings.json`
  - Item "Configurações" no menu do system tray

- **📚 Documentação Completa**:
  - README.md completamente reescrito para MVP v0.1.0
  - Badges de versão, Python, licença e testes
  - Seções reorganizadas com emojis e categorização clara
  - Nova seção "Estrutura do Projeto" com árvore completa
  - Guia de uso expandido com menu, atalhos, busca e configurações
  - Solução de problemas atualizada
  - Documentação da arquitetura modular

### Alterado
- **SettingsManager expandido** com 8 configurações:
  - `hotkey_copy_datetime` (padrão: "ctrl+shift+q")
  - `hotkey_refresh_menu` (padrão: "ctrl+shift+r")
  - `max_history_items` (10-1000, padrão: 100)
  - `clipboard_monitor_interval` (0.5s-60s, padrão: 3s)
  - `clipboard_idle_threshold` (5s-300s, padrão: 30s)
  - `datetime_format` (personalizável, padrão: "%d.%m.%Y-%H:%M")
  - `notification_duration` (1-15s, padrão: 2s)
  - `notification_enabled` (bool, padrão: True)

- **HotkeyManager** agora suporta:
  - `Ctrl+Shift+Q` - Copiar data/hora
  - `Ctrl+Shift+R` - Recarregar menu
  - **`Ctrl+Shift+F` - Buscar no histórico (NOVO)**
  - Callbacks configuráveis para cada hotkey

- **MenuBuilder** expandido com novos itens:
  - "Buscar no Histórico (Ctrl+Shift+F)" (NOVO)
  - "Configurações" (NOVO)
  - Mantém itens anteriores: Copiar Data/Hora, Definir Prefixo, Recarregar, Histórico, Limpar, Sobre, Sair

### Corrigido
- **Revert: Tentativa de atualização automática do menu**:
  - Removida tentativa de callback `on_history_updated_callback` (não funciona com pystray)
  - Documentação atualizada explicando limitação técnica do pystray
  - Menu só atualiza quando usuário fecha e abre novamente (comportamento do pystray)
  - Soluções alternativas documentadas: "Recarregar Itens", `Ctrl+Shift+R`, ou fechar/abrir menu
  - Busca (`Ctrl+Shift+F`) sempre mostra dados atualizados

### Técnica
- **7 novos arquivos criados**:
  - `dahora_app/ui/settings_dialog.py` (259L) - Janela de configurações com 4 abas
  - `dahora_app/ui/search_dialog.py` (265L) - Janela de busca no histórico
  - Atualizações em 5+ arquivos existentes para integração

- **Arquitetura**:
  - Padrão de callbacks para comunicação entre módulos
  - Thread-safe com `threading.Thread` para janelas
  - Validação robusta de inputs do usuário
  - Atomic writes para persistência de configurações

- **Qualidade**:
  - ✅ 15/15 testes passando (100%)
  - ✅ Imports verificados
  - ✅ Build testado: ~31MB executável
  - ✅ Zero regressões

### Documentação
- README.md: 168 linhas adicionadas, 39 linhas removidas
- Seção "Estrutura do Projeto" com árvore completa
- Guia de uso expandido com todas as features
- Documentação de limitações técnicas (menu não atualiza em tempo real)

### Desempenho
- Busca em tempo real sem travamentos
- Aplicação de configurações instantânea (exceto hotkeys)
- Janelas responsivas com feedback visual imediato

### Notas
- **🎊 MVP COMPLETO!** Todas as funcionalidades essenciais implementadas
- **🔍 Busca inteligente** no histórico com hotkey global
- **⚙️ Configurações avançadas** com interface gráfica moderna
- **📚 Documentação profissional** completa
- **🧪 Testes 100%** passando
- **🚀 Pronto para uso em produção!**

---

## [0.0.9] - 2025-11-04

### Adicionado
- **Arquitetura Modular Completa**: Refatoração total de `dahora_app.py` (1126 linhas) em 14 módulos especializados
- **13 Módulos Python Criados**:
  - `dahora_app/constants.py` (48L) - Constantes e configurações globais
  - `dahora_app/utils.py` (67L) - Funções utilitárias (atomic_write_text/json, truncate_text, sanitize_text)
  - `dahora_app/settings.py` (93L) - SettingsManager com validação integrada
  - `dahora_app/counter.py` (63L) - UsageCounter para gerenciamento de uso
  - `dahora_app/clipboard_manager.py` (184L) - ClipboardManager com monitor inteligente
  - `dahora_app/datetime_formatter.py` (61L) - DateTimeFormatter com prefixo configurável
  - `dahora_app/notifications.py` (153L) - NotificationManager multi-canal (toast/tkinter/messagebox)
  - `dahora_app/hotkeys.py` (103L) - HotkeyManager para gerenciamento de atalhos globais
  - `dahora_app/ui/prefix_dialog.py` (166L) - PrefixDialog com interface gráfica moderna
  - `dahora_app/ui/icon_manager.py` (95L) - IconManager para gerenciamento de ícones (suporta PyInstaller)
  - `dahora_app/ui/menu.py` (167L) - MenuBuilder para criação de menus dinâmicos
  - `dahora_app/__init__.py` - API pública do pacote
  - `dahora_app/README.md` - Documentação completa da arquitetura
- **Novo arquivo `main.py`** (392L): Aplicação principal com classe `DahoraApp` e arquitetura orientada a objetos
- **Estrutura de testes completa**: 15 testes (95% de cobertura) com pytest e fixtures reutilizáveis
- **Type hints**: Adicionadas anotações de tipo em 10+ funções críticas para melhor manutenibilidade
- **Documentação arquitetural**: README.md completo explicando cada módulo e seus benefícios

### Alterado
- **Responsabilidade única**: Cada módulo agora tem uma função clara e bem definida
- **Build system**: `build.py` atualizado para usar `main.py` ao invés de `dahora_app.py`
- **Imports organizados**: Importações explícitas mostram dependências claras entre módulos
- **Testes atualizados**: Todos os testes agora importam e usam módulos reais ao invés de mocks
- **Código ~160 linhas mais limpo**: Remoção de duplicações e código morto da sprint anterior

### Melhorado
- **Testabilidade**: Componentes podem ser testados isoladamente com facilidade
- **Manutenibilidade**: Código organizado e fácil de entender com arquitetura clara
- **Reutilização**: Módulos podem ser importados e usados em outros projetos Python
- **Escalabilidade**: Fácil adicionar novos componentes sem afetar código existente
- **Legibilidade**: Separação clara entre domínios (UI, clipboard, notificações, etc)

### Técnico
- **9 Classes gerenciadoras** criadas com responsabilidade única:
  - `SettingsManager`: Gerencia configurações com validação
  - `UsageCounter`: Contador de uso com persistência atômica
  - `ClipboardManager`: Histórico e monitoramento com polling adaptativo
  - `DateTimeFormatter`: Formatação com prefixo configurável
  - `NotificationManager`: Sistema multi-canal de notificações
  - `HotkeyManager`: Gerenciamento centralizado de hotkeys
  - `PrefixDialog`: Interface gráfica Tkinter moderna
  - `IconManager`: Carregamento de ícones com suporte PyInstaller
  - `MenuBuilder`: Construção dinâmica de menus do sistema
- **Padrão de projeto**: Uso extensivo de injeção de dependência via callbacks
- **Compatibilidade 100%**: `dahora_app.py` original mantido para retrocompatibilidade
- **Build testado**: Executável `dahora_app_v0.0.7.exe` (31.3 MB) funcionando perfeitamente
- **Tempo de desenvolvimento**: 6h (50% mais rápido que as 12h estimadas)

### Documentação
- Documentação completa em `dahora_app/README.md` com:
  - Visão geral da arquitetura modular
  - Descrição detalhada de cada módulo
  - Exemplos de uso e imports
  - Benefícios da modularização
  - Guia de testes

### Testes
- ✅ 15/15 testes passando (100%)
- ✅ Cobertura de 95% do código
- ✅ Testes integrados com módulos reais
- ✅ Fixtures reutilizáveis em `conftest.py`
- ✅ Tempo de execução: 0.32s

### Desempenho
- Código organizado em ~1650 linhas distribuídas em 14 arquivos
- Redução de acoplamento entre componentes
- Melhor isolamento de responsabilidades
- Facilita otimizações futuras por módulo

## [0.0.8] - 2025-11-04

### Adicionado
- Implementa rotação automática de logs com `RotatingFileHandler` (limite de 5MB, mantém 3 backups)
- Adiciona validação e sanitização de configurações do usuário
- Implementa aviso de privacidade na primeira execução do aplicativo
- Cria marcador `.privacy_accepted` para evitar repetição do aviso
- Adiciona nova seção "Privacidade e Segurança" na documentação (README.md)
- Adiciona arquivo `CHECKLIST_MELHORIAS.md` com 134 tarefas de melhoria organizadas por prioridade

### Corrigido
- **CRÍTICO:** Corrige path hardcoded em `build.py` que impedia build em outras máquinas
  - Substitui `E:\Dahora\dahora-app\icon.ico` por caminho relativo usando `os.path.dirname(__file__)`
  - Build agora é portável e funciona em qualquer máquina/diretório
- Adiciona tratamento robusto para arquivos `settings.json` corrompidos (JSONDecodeError)
- Implementa sanitização de caracteres de controle ASCII em configurações
- Adiciona limite de 100 caracteres para prefixo com truncamento automático

### Alterado
- Renomeia arquivo de log de `qopas.log` para `dahora.log` (mais consistente com nome do app)
- Melhora documentação sobre armazenamento de dados no README
- Logs agora incluem mensagem informativa sobre sistema de rotação no startup
- Settings são automaticamente validados antes de serem aplicados

### Segurança
- Implementa validação de entrada para prevenir caracteres perigosos em configurações
- Adiciona aviso transparente sobre dados armazenados localmente
- Documenta práticas de privacidade (zero telemetria, dados 100% locais)

### Técnica
- Adiciona import `from logging.handlers import RotatingFileHandler`
- Cria função `validate_settings()` para sanitização de configurações
- Cria função `show_privacy_notice()` para primeira execução
- Atualiza `load_settings()` com validação integrada
- Build testado e funcionando: `dahora_app_v0.0.7.exe` (31.3 MB)

### Documentação
- Expande seção "Armazenamento de dados" com detalhes sobre todos os arquivos
- Adiciona informações sobre rotação automática de logs
- Documenta política de privacidade e segurança
- Cria roadmap detalhado de melhorias futuras

## [0.0.7-3] - 2025-11-04

### Purpose
- Release de teste para validar YAML e fix do passo de hash

### Corrigido
- Indentação corrigida do passo "Compute SHA-256" no workflow para permanecer dentro de `steps`
- Geração correta do nome do arquivo `.sha256` usando variável simples (`$basename`)

### Técnico
- Workflow acionado por tags `v*` com build em Windows e criação de release
- Upload de `.exe` e `.sha256.txt` e extração de notas do `CHANGELOG.md`
- Usa `softprops/action-gh-release@v1`

## [0.0.7-2] - 2025-11-04

### Purpose
- Release de teste para revalidar o workflow após correção no passo de hash

### Corrigido
- Correção no PowerShell ao gerar o nome do arquivo `.sha256` (remoção de subexpressão `$(...)`); agora o arquivo é criado como `<basename>.sha256.txt`

### Técnico
- Ajuste no passo "Compute SHA-256" do workflow `release.yml` usando variáveis simples (`$basename`) para montar o nome do arquivo
- A execução do workflow em tags `v*` deve anexar `.exe` e `.sha256.txt` corretamente ao release

## [0.0.7-1] - 2025-11-04

### Purpose
- Release de teste para validar o workflow de build e release por tag (GitHub Actions)

### Adicionado
- Workflow `.github/workflows/release.yml` (Windows runner)
- Automação de build com `py build.py` e upload de assets (.exe e .sha256)
- Extração automática de notas do `CHANGELOG.md` para compor o corpo do release

### Técnica
- Dispara em `push` de tags `v*` (ex.: `v0.0.7-1`)
- Calcula SHA-256 no runner e anexa ao release
- Usa `softprops/action-gh-release@v1` para criar o release e enviar arquivos

## [0.0.7] - 2025-11-04

### Alterado
- Notificação rápida via Tkinter ajustada para ~1.5s e visual próximo ao Windows
- Clique esquerdo no ícone aciona a mesma notificação curta do atalho
- README atualizado (versões, comportamento das notificações e clique esquerdo)
- `build.py` atualizado para gerar `dahora_app_v0.0.7.exe`

### Adicionado
- Exceção no `.gitignore` para versionar `001_pyinstaller.spec`

### Removido
- Arquivo obsoleto `qopas_app_v0.0.5.spec` (limpeza)

### Técnica
- `001_pyinstaller.spec` canônico incluído no repositório

## [0.0.6] - 2025-11-03

### Adicionado
- Janela "Definir Prefixo" atualizada com visual próximo ao Windows 11 (ttk, tema `vista`)
- Atalho interno `Ctrl+Shift+R` para "Recarregar Itens" no menu do system tray
- Item do menu renomeado para "Recarregar Itens" e posicionado acima do histórico

### Alterado
- Documentação revisada e unificada (README e CHANGELOG)
- Correção de referências antigas para `dahora_app.py`
- README atualizado com executável correto `dahora_app_v0.0.6.exe`
- Ordem dos botões na janela de prefixo ajustada para "Cancelar | Salvar"

### Removido
- Documentos redundantes/obsoletos: `CLAUDE.md` e `SUGESTOES_NOMES.md`

### Técnica
- `build.py` atualizado para gerar `dahora_app_v0.0.6.exe`
- Mantida estratégia segura de atualização de menu via ação dedicada

## [0.0.4] - 2025-11-02

### Adicionado
- **Atualização de ícone personalizado**: Novo arquivo icon.ico incorporado no executável
- **Versão 0.0.4**: Executável atualizado com novo ícone do sistema bandeja

### Alterado
- **Atualização de build**: PyInstaller configurado para usar o novo arquivo icon.ico (10,052 bytes)
- **Versão incrementada**: Atualizada de v0.0.3 para v0.0.4 para refletir nova versão do ícone

---

---

## [0.0.5] - 2025-11-02

### Adicionado
- **Monitoramento inteligente de clipboard**: Sistema adaptativo que reduz sobrecarga do sistema
- **Detecção de Ctrl+C**: Captura automaticamente quando usuário pressiona Ctrl+C
- **Polling adaptativo**: Intervalos dinâmicos de 0.5s a 10s baseados em atividade
- **Otimização de recursos**: Maior intervalo quando clipboard está ocioso (>30s)

### Alterado
- **Performance clipboard monitoring**: Substituído polling constante por detecção inteligente
- **Eficiência do sistema**: Reduz consumo de CPU quando não há atividade no clipboard
- **Hotkeys expandidas**: Agora captura Ctrl+Shift+Q e Ctrl+C globalmente

### Técnica
- **Intelligent polling**: 0.5s resposta rápida com atividade, até 10s quando ocioso
- **Activity detection**: Detecta mudanças reais no clipboard em vez de verificação constante
- **Ctrl+C interception**: Adiciona conteúdo ao histórico quando Ctrl+C é pressionado
- **Idle optimization**: Aumenta intervalos automaticamente quando sistema está ocioso

---

## [0.0.3] - 2025-11-02

### Adicionado
- **Melhoria no monitoramento de clipboard**: Intervalo atualizado de 1 para 3 segundos para melhor performance
- **Funcionalidade de limpeza de histórico**: Opção "Limpar Histórico" no menu de clique direito para remover todo o histórico de clipboard
- **Histórico persistente**: Agora o histórico é salvo em `clipboard_history.json` e mantém entre reinicializações
- **Monitoramento ativo**: Clipboard é monitorado automaticamente a cada 3 segundos, detectando novas cópias
- **Interface aprimorada**: Melhor feedback visual e notificações ao limpar histórico

### Corrigido
- **Corrigido bug de limpeza de histórico**: A função de limpar histórico agora funciona corretamente, removendo permanentemente todos os itens do arquivo
- **Corrigido bug de menu recursivo**: Eliminada recursão infinita ao atualizar menu após definir prefixo
- **Corrigido ícone de bandeja**: O ícone personalizado agora é carregado corretamente no executável sem erros
- **Melhorado tratamento de erros**: Logging robusto com fallbacks ao remover arquivo de histórico
- **Otimizado desempenho**: Intervalo de monitoramento reduzido para 3 segundos com melhor tratamento de exceções
- **Corrigido estado consistente**: Após limpar histórico, o aplicativo recarrega estado do arquivo para garantir consistência

---

## [0.0.2] - 2025-01-02

### Adicionado
- **Melhoria no monitoramento de clipboard**: O histórico agora é atualizado instantaneamente sempre que o clipboard é modificado, não apenas ao iniciar o aplicativo
- **Melhoria no intervalo de monitoramento**: Reduzido de 2 para 1 segundo para detecção mais rápida de mudanças
- **Logging aprimorado**: Adicionado logs detalhados para monitoramento do clipboard em `dahora.log`
- **Inicialização aprimorada**: O aplicativo agora inicializa o estado atual do clipboard ao iniciar para evitar duplicações

### Corrigido
- **Corrigido bug de histórico de clipboard**: O histórico só era atualizado ao abrir o aplicativo, não em tempo real
- **Corrigida inicialização do estado do clipboard**: Agora captura o estado atual do clipboard ao iniciar para comparação correta
- **Melhorado tratamento de erros**: Logging detalhado para depuração de problemas de clipboard
- **Otimizado desempenho**: Menor intervalo de verificação (1s) com melhor tratamento de erros

---

## [0.0.1] - 2025-01-02

### Adicionado
- Versão inicial do Qopas App 0.0.1
- System tray do Windows com ícone de relógio personalizado
- Copia data e hora para o clipboard no formato `[DD.MM.AAAA-HH:MM]`
- Hotkey global: `Ctrl+Shift+Q` para copiar de qualquer lugar
- Notificações do Windows (toasts) de 2 segundos com auto-dismiss
- Prevenção de múltiplas instâncias do aplicativo
- Janela "Sobre" modal que fica aberta até o usuário fechar
- Interface intuitiva com clique esquerdo (instruções) e clique direito (menu)
- Contador de uso - quantas vezes o app foi acionado
- Histórico de clipboard - mantém últimos 100 itens copiados
- Monitoramento automático de clipboard - detecta mudanças no clipboard
- Menu com acesso rápido aos 5 itens de clipboard mais recentes
- Opção para limpar o histórico de clipboard manualmente
- Ícone personalizado incluso no executável .exe
- Script de build automatizado com PyInstaller
- Documentação completa em README.md e CLAUDE.md

### Alterado
- Alterado hotkey global de `Ctrl+Shift+D` para `Ctrl+Shift+Q` para evitar conflitos
- Interface melhorada com tooltips claros e mensagens intuitivas
- Notificações otimizadas para 2 segundos de duração
- Menu organizado com submenus para histórico de clipboard

### Técnica
- PyInstaller para build de executável Windows
- Python 3.8+ como dependência
- Bibliotecas: pystray, pyperclip, keyboard, Pillow, winotify, pywin32
- Arquivo .gitignore para controle de versão
- Repositório GitHub: https://github.com/rkvasne/dahora-app
- Executável nomeado como `qopas_app_v0.0.1.exe` com identificação de versão

### Corrigido
- Corrigido erro de menu em `pystray` usando método `__add__` ao invés de `add`
- Melhorado tratamento de erros e exceções
- Corrigida inicialização de múltiplas instâncias
- Otimizado gerenciamento de threads e recursos

---

## [Versões Futuras]

### Planejado para 0.0.2
- [ ] Suporte para múltiplos formatos de data/hora configuráveis
- [ ] Opção para personalizar hotkey global
- [ ] Exportação de histórico de clipboard para arquivo
- [ ] Integração com cloud storage (opcional)
- [ ] Temas personalizados para o ícone

### Planejado para 0.1.0
- [ ] Interface gráfica completa para configurações
- [ ] Plugin system para extensões
- [ ] Suporte para macOS e Linux
- [ ] Autostart configuration
- [ ] Atalhos de teclado configuráveis via interface

### Planejado para 1.0.0
- [ ] Versão estável com todas as funcionalidades planejadas
- [ ] Documentação completa para desenvolvedores
- [ ] Testes automatizados unitários e de integração
- [ ] Instalador MSI para Windows
- [ ] Assinatura digital do executável
