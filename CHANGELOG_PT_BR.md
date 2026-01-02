# Registro de Mudanças

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.4] - 2025-12-30

### Adicionado
- **Implementação Completa da Phase 6:**
  - Módulo base CallbackManager (265 linhas)
  - 4 implementações de handlers (495 linhas)
  - Testes de integração (370 linhas)
  - 84 novos testes (todos passando)

- **Documentação Consolidada:**
  - Novo `DOCUMENTATION_INDEX.md` como referência central
  - Rastreamento de status unificado entre todas as fases
  - Formato e estrutura padronizados

- **Melhorias na Landing Page:**
  - Subtítulo do hero comunicando diferencial real
  - Versão de download genérica para evitar confusão
  - Link para página de releases do GitHub

### Alterado
- Versão incrementada para 0.2.4 (release de consolidação de documentação)
- Estrutura de documentação unificada em todas as pastas
- Removidos arquivos de status redundantes em favor do rastreamento centralizado
- Aprimorado docs/README.md com referências consolidadas

### Melhorado
- Consistência de documentação em todos os arquivos
- Validação de links internos e padronização
- Rastreamento de versão em todos os pontos de documentação

### Métricas
- **Testes:** 262/262 passando (100%)
- **Código:** 4500+ linhas adicionadas
- **Documentação:** 3000+ linhas adicionadas
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

---

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
  - `test_ui_modernization.py`: Teste completo da interface moderna
  - `test_shortcut_editor.py`: Teste específico do editor de atalhos
  - Validação de todos os componentes modernizados

### 🎉 Experiência do Usuário
- **Interface mais próxima do Windows 11**: Visual nativo e familiar
- **Menos ruído visual**: Bordas removidas, foco limpo, cores sutis
- **Melhor feedback**: Cursores apropriados, hover states, transições suaves
- **Consistência total**: Todos os componentes seguem o mesmo padrão

---

## [0.2.2-modern-ui] - 2025-12-29 🎨 **TRANSFORMAÇÃO VISUAL COMPLETA: INTERFACE MODERNA**

### 🎨 Redesenho Completo da Interface
- **Nova paleta de cores moderna**: Inspirada em VS Code, Discord e aplicações contemporâneas
- **Hierarquia visual aprimorada**: text_bright, text_muted, surface, bg_secondary para melhor organização
- **Cores mais equilibradas**: Transição de tons Windows para paleta moderna e profissional

### ✨ Componentes Redesenhados
- **Botões modernos**: Padding generoso (20x10), estados hover/pressed aprimorados, novos estilos (Success, Danger)
- **Inputs elegantes**: Bordas sólidas, foco destacado, padding interno aumentado (12x8)
- **Cards elevados**: Visual de profundidade com background diferenciado
- **Abas espaçosas**: Padding aumentado (20x12) com transições visuais suaves

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

---

## [0.2.2-landing-improvements] - 2025-12-29 🎨 **LANDING PAGE: DESIGN & COPY PROFISSIONAL**

### 🎨 Melhorias de Design
- **Tipografia otimizada**: Melhor contraste de texto e hierarquia visual refinada
- **Espaçamento equilibrado**: Padding reduzido de 10rem para 6rem nas seções
- **Cards mais elegantes**: Border-radius menos arredondado (1rem), sombras mais sutis
- **Ícones refinados**: Tamanho reduzido (56px), bordas menos arredondadas
- **Hover effects**: Movimento sutil com translateY(-2px) para melhor feedback
- **Cores suavizadas**: Gradientes e sombras com opacidade reduzida para visual mais profissional

### ✍️ Otimização de Copy
- **Seção Novidades**: Textos 60% mais concisos, eliminando verbosidade
- **Seção Hero**: Subtitle mais direta e impactante
- **Tom profissional**: Substituição de palavras informais por elegantes
- **Maiúsculas corrigidas**: CTRL+SHIFT → Ctrl+Shift
- **Linguagem técnica**: Vocabulário mais elegante e confiável

### 🌐 Traduções Atualizadas
- **Português (pt-BR)**: Textos otimizados e profissionalizados
- **Inglês (en)**: Traduções consistentes com melhorias em português
- **Consistência**: Tom uniforme entre idiomas

### 📱 Melhorias Responsivas
- **Mobile otimizado**: Hero com padding 6rem, título 2.5rem
- **Seção desenvolvedor**: Avatar menor (120px), textos proporcionais
- **Espaçamento mobile**: Padding de 4rem para 3.5rem

### 🎯 Resultados
- **40-60% redução** no tamanho dos textos
- **Leitura mais rápida** e escaneabilidade melhorada
- **Visual mais profissional** e confiável
- **Experiência consistente** em todos os dispositivos
- **Todas as animações preservadas**

---

## [0.0.9] - 2025-11-04

### Adicionado
- **Arquitetura Modular Completa**: Refatoração total em 14 módulos especializados
- **13 Módulos Python Criados** com responsabilidade única:
  - `constants.py` (48L) - Constantes e configurações globais
  - `utils.py` (67L) - Funções utilitárias
  - `settings.py` (93L) - SettingsManager com validação
  - `counter.py` (63L) - UsageCounter
  - `clipboard_manager.py` (184L) - ClipboardManager inteligente
  - `datetime_formatter.py` (61L) - DateTimeFormatter
  - `notifications.py` (153L) - NotificationManager multi-canal
  - `hotkeys.py` (103L) - HotkeyManager
  - Módulos de UI: prefix_dialog, icon_manager, menu
- **Novo arquivo `main.py`** (392L): Aplicação principal com classe `DahoraApp`
- **Estrutura de testes completa**: 15 testes (95% de cobertura)
- **Type hints** em 10+ funções críticas
- **Documentação arquitetural** completa

### Alterado
- **Build system**: `build.py` atualizado para usar `main.py`
- **Imports organizados**: Importações explícitas mostram dependências
- **Testes atualizados**: Todos os testes usam módulos reais

### Melhorado
- **Testabilidade**: Componentes podem ser testados isoladamente
- **Manutenibilidade**: Código organizado com arquitetura clara
- **Reutilização**: Módulos podem ser importados em outros projetos
- **Escalabilidade**: Fácil adicionar novos componentes
- **Legibilidade**: Separação clara entre domínios

---

## [0.0.8] - 2025-11-04

### Adicionado
- Rotação automática de logs com `RotatingFileHandler` (limite de 5MB, mantém 3 backups)
- Validação e sanitização de configurações do usuário
- Aviso de privacidade na primeira execução
- Marcador `.privacy_accepted` para evitar repetição
- Seção "Privacidade e Segurança" na documentação
- Arquivo `CHECKLIST_MELHORIAS.md` com 134 tarefas organizadas por prioridade

### Corrigido
- **CRÍTICO:** Path hardcoded em `build.py` que impedia build em outras máquinas
  - Substituído por caminho relativo usando `os.path.dirname(__file__)`
  - Build agora é portável e funciona em qualquer máquina/diretório
- Tratamento robusto para arquivos `settings.json` corrompidos
- Sanitização de caracteres de controle ASCII em configurações
- Limite de 100 caracteres para prefixo com truncamento automático

---

## [0.0.7] - 2025-11-04

### Alterado
- Notificação rápida via Tkinter ajustada para ~1.5s
- Clique esquerdo no ícone aciona a mesma notificação curta do atalho
- README atualizado com versões e comportamento das notificações
- `build.py` atualizado para gerar `dahora_app_v0.0.7.exe`

### Adicionado
- Exceção no `.gitignore` para versionar `001_pyinstaller.spec`

---

## [0.0.6] - 2025-11-03

### Adicionado
- Janela "Definir Prefixo" com visual próximo ao Windows 11 (ttk, tema `vista`)
- Atalho interno `Ctrl+Shift+R` para "Recarregar Itens" no menu da bandeja

### Alterado
- Documentação revisada e unificada
- Item do menu renomeado para "Recarregar Itens"
- Ordem dos botões na janela de prefixo ajustada

---

## [0.0.5] - 2025-11-02

### Adicionado
- **Monitoramento inteligente de clipboard**: Sistema adaptativo que reduz sobrecarga do sistema
- **Detecção de Ctrl+C**: Captura automaticamente quando usuário pressiona Ctrl+C
- **Polling adaptativo**: Intervalos dinâmicos de 0.5s a 10s baseados em atividade

---

## [0.0.4] - 2025-11-02

### Adicionado
- Atualização de ícone personalizado: Novo arquivo icon.ico incorporado no executável

---

## [0.0.3] - 2025-11-02

### Adicionado
- Melhoria no monitoramento de clipboard (intervalo de 1 para 3 segundos)
- Funcionalidade de limpeza de histórico
- Histórico persistente em `clipboard_history.json`

### Corrigido
- Bug de limpeza de histórico
- Bug de menu recursivo
- Carregamento correto do ícone de bandeja

---

## [0.0.2] - 2025-01-02

### Adicionado
- Melhoria no monitoramento de clipboard (atualização em tempo real)
- Melhoria no intervalo de monitoramento (reduzido de 2 para 1 segundo)
- Logging aprimorado

---

## [0.0.1] - 2025-01-02

### Adicionado
- Versão inicial do Dahora App
- Sistema de bandeja do Windows com ícone personalizado
- Copia data e hora para a área de transferência no formato `[DD.MM.AAAA-HH:MM]`
- Tecla de atalho global: `Ctrl+Shift+Q`
- Notificações toast de 2 segundos
- Prevenção de múltiplas instâncias
- Janela "Sobre" modal
- Contador de uso
- Histórico de clipboard (mantém últimos 100 itens)
- Monitoramento automático de clipboard
- Menu com acesso rápido aos 5 itens mais recentes
- Script de build automatizado com PyInstaller
- Documentação completa
