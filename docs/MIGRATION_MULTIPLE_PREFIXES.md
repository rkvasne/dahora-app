# Migração para Múltiplas Palavras Personalizadas

## Objetivo
Permitir que o usuário defina múltiplas palavras personalizadas, cada uma com:
- **Atalho customizável**: O usuário escolhe qualquer combinação (ex: Ctrl+Shift+1, Alt+F1, Ctrl+Alt+D, etc.)
  - Sugestões padrão: Ctrl+Shift+1, Ctrl+Shift+2, Ctrl+Shift+3...
  - Totalmente editável pelo usuário
- **Prefixo próprio**: Cada atalho gera `[prefixo-DD.MM.AAAA-HH:MM]`
- **Configurações individuais**: Cada slot pode ter configurações específicas

## Estrutura Atual vs Nova

### Atual
```json
{
  "prefix": "DAHORA",
  "hotkey_copy_datetime": "ctrl+shift+q"
}
```
**Resultado**: `[DAHORA-05.11.2025-18:35]`

### Nova (Proposta)
```json
{
  "custom_shortcuts": [
    {
      "id": 1,
      "hotkey": "ctrl+shift+1",  // Sugestão padrão, editável pelo usuário
      "prefix": "DAHORA",
      "enabled": true,
      "description": "Prefixo padrão"
    },
    {
      "id": 2,
      "hotkey": "alt+f1",  // Usuário customizou para Alt+F1
      "prefix": "URGENTE",
      "enabled": true,
      "description": "Tarefas urgentes"
    },
    {
      "id": 3,
      "hotkey": "ctrl+alt+d",  // Usuário escolheu Ctrl+Alt+D
      "prefix": "REUNIAO",
      "enabled": true,
      "description": "Notas de reunião"
    }
  ],
  "legacy_prefix": "DAHORA",  // Para retrocompatibilidade
  "hotkey_copy_datetime": "ctrl+shift+q",  // Mantém comportamento legado
  "hotkey_refresh_menu": "ctrl+shift+r",
  // ... outras configurações existentes
}
```

**Resultados (exemplos)**:
- Ctrl+Shift+1 → `[DAHORA-05.11.2025-18:35]` (padrão sugerido)
- Alt+F1 → `[URGENTE-05.11.2025-18:35]` (customizado pelo usuário)
- Ctrl+Alt+D → `[REUNIAO-05.11.2025-18:35]` (customizado pelo usuário)
- Ctrl+Shift+Q → `[DAHORA-05.11.2025-18:35]` (legado, mantido)

## Análise de Impacto

### 🔴 Alto Impacto (Mudanças Significativas)

#### 1. **SettingsManager** (`dahora_app/settings.py`)
**Mudanças**:
- Adicionar lista `custom_shortcuts`
- Métodos para CRUD de shortcuts personalizados
- Migração automática de dados antigos
- Validação de conflitos de hotkeys

**Riscos**:
- Corrupção de dados se migração falhar
- Perda de configurações existentes

**Mitigação**:
- Backup automático antes da migração
- Validação rigorosa de dados
- Fallback para configuração padrão

#### 2. **HotkeyManager** (`dahora_app/hotkeys.py`)
**Mudanças**:
- Registrar hotkeys customizáveis dinamicamente (qualquer combinação)
- Mapeamento de hotkey → prefixo
- Remoção/adição dinâmica de hotkeys
- **Validação rigorosa de conflitos**:
  - Detectar hotkeys duplicados na própria aplicação
  - Avisar sobre conflitos com hotkeys do sistema
  - Tentar registrar e avisar se falhar

**Riscos**:
- Conflitos com outros aplicativos ou sistema
- Usuário escolher hotkey já usado
- Falha ao registrar hotkeys personalizados

**Mitigação**:
- Try/catch individual para cada hotkey
- Validação antes de salvar (testar se consegue registrar)
- Avisos claros na UI sobre conflitos
- Log detalhado de falhas
- Permitir continuar mesmo se alguns hotkeys falhem
- Sugerir alternativas se hotkey falhar

#### 3. **DateTimeFormatter** (`dahora_app/datetime_formatter.py`)
**Mudanças**:
- Método `format_with_prefix(prefix: str)` separado
- Manter `format_now()` para compatibilidade legada

**Riscos**:
- Quebra de código legado

**Mitigação**:
- Manter métodos antigos funcionando
- Adicionar novos métodos sem remover antigos

### 🟡 Médio Impacto (Adaptações)

#### 4. **DahoraApp** (`main.py`)
**Mudanças**:
- Callbacks para múltiplos hotkeys
- Passar `shortcut_id` ou `prefix` para formatação
- Atualizar notificações com indicador do atalho usado

**Riscos**:
- Lógica complexa de callbacks

**Mitigação**:
- Callbacks padronizados usando factory pattern

#### 5. **PrefixDialog** / Nova UI
**Mudanças**:
- Nova interface para gerenciar lista de shortcuts
- Adicionar/Editar/Remover shortcuts
- **Editor de hotkeys customizáveis**:
  - Campo de texto para digitar hotkey
  - Botão "Detectar Teclas" (usuário pressiona a combinação)
  - Validação em tempo real (detecta duplicatas)
  - Sugestões padrão (Ctrl+Shift+1-9)
  - Preview do resultado final: `[PREFIXO-DD.MM.YYYY-HH:MM]`
- Validação de hotkeys:
  - Duplicados dentro da app
  - Teste de registro (tenta registrar e avisa se falhar)
  - Conflitos com hotkeys reservados (Ctrl+C, Ctrl+V, etc.)

**Riscos**:
- UI complexa e confusa
- Usuário não entender formato de hotkeys
- Conflitos difíceis de detectar

**Mitigação**:
- Interface simples e intuitiva
- Botão "Detectar Teclas" para capturar pressionamento
- Validação em tempo real com feedback visual
- Começar com máximo de 5-9 shortcuts
- Exemplos e tooltips

#### 6. **MenuBuilder** (`dahora_app/ui/menu.py`)
**Mudanças**:
- Adicionar itens de menu para cada shortcut configurado
- Mostrar hotkey e prefixo no menu

**Riscos**:
- Menu muito grande

**Mitigação**:
- Submenu "Atalhos Personalizados"
- Mostrar apenas shortcuts habilitados

### 🟢 Baixo Impacto (Ajustes Menores)

#### 7. **UsageCounter**, **ClipboardManager**, **NotificationManager**
**Mudanças**: Nenhuma ou mínimas
**Razão**: Esses componentes são independentes de prefixos

#### 8. **Testes**
**Mudanças**: Adicionar testes para novos recursos
**Arquivos**: `tests/test_settings.py`, criar `tests/test_multiple_shortcuts.py`

## Estratégia de Migração em Etapas

### ✅ Etapa 0: Preparação (Antes de Codificar)
- [x] Criar este documento de análise
- [ ] Revisar e aprovar o plano
- [ ] Criar branch no Git: `feature/multiple-shortcuts`
- [ ] Backup de arquivos de configuração existentes

### 📝 Etapa 1: Modelo de Dados (Retrocompatível)
**Objetivo**: Atualizar `SettingsManager` sem quebrar código existente

**Tarefas**:
1. Adicionar estrutura de dados `custom_shortcuts` em `settings.py`
2. Criar métodos auxiliares:
   - `add_custom_shortcut(prefix, hotkey, description)`
   - `remove_custom_shortcut(id)`
   - `get_custom_shortcuts()`
   - `update_custom_shortcut(id, data)`
3. Implementar migração automática:
   - Detectar settings antigo (só `prefix`)
   - Criar primeiro shortcut com `prefix` existente + Ctrl+Shift+1
4. Manter propriedade `date_prefix` funcionando (retrocompat)
5. Testes unitários completos

**Critério de Sucesso**:
- Código antigo continua funcionando
- Novos métodos testados e validados
- Migração automática funcionando

**Tempo Estimado**: 2-3 horas

### 🎯 Etapa 2: DateTimeFormatter (Sem Quebrar Legado)
**Objetivo**: Adicionar suporte a múltiplos prefixos

**Tarefas**:
1. Adicionar método `format_with_prefix(prefix: str) -> str`
2. Manter `format_now()` usando `self.prefix` (legado)
3. Testes para ambos os métodos

**Critério de Sucesso**:
- Métodos antigos funcionando normalmente
- Novo método testado

**Tempo Estimado**: 1 hora

### ⌨️ Etapa 3: HotkeyManager Dinâmico
**Objetivo**: Registrar hotkeys customizáveis dinamicamente

**Tarefas**:
1. Adicionar `setup_custom_hotkeys(custom_shortcuts: List[dict])`
2. Criar callbacks dinâmicos com closure para passar `shortcut_id`
3. Implementar `unregister_custom_hotkeys()`
4. **Adicionar validação de hotkeys**:
   - `validate_hotkey(hotkey: str) -> Tuple[bool, str]` (retorna validade + mensagem)
   - `test_register_hotkey(hotkey: str) -> bool` (testa se consegue registrar)
   - Detectar conflitos internos
5. Manter hotkey legado (Ctrl+Shift+Q) funcionando
6. Log detalhado de sucesso/falha de cada hotkey com mensagens amigáveis

**Critério de Sucesso**:
- Qualquer hotkey pode ser registrado
- Validação funciona corretamente
- Avisos claros sobre conflitos
- Callbacks corretos para cada hotkey
- Hotkey legado funcionando

**Tempo Estimado**: 4-5 horas (aumentou por causa da validação)

### 🎨 Etapa 4: Interface de Usuário
**Objetivo**: Permitir gerenciar shortcuts via UI

**Tarefas**:
1. Criar `CustomShortcutsDialog` (tkinter):
   - Lista de shortcuts existentes (TreeView ou ListBox)
   - Botões: Adicionar, Editar, Remover, Habilitar/Desabilitar
   - **Editor de hotkey customizável**:
     - Campo Entry para hotkey (formato: ctrl+shift+1)
     - Botão "⌨️ Detectar Teclas" (captura pressionamento do usuário)
     - Label de preview: mostra resultado final
     - Validação em tempo real (feedback visual: ✅ ou ❌)
   - Campos: Prefixo, Descrição, Hotkey, Enabled
   - Validação de hotkeys duplicados com mensagem clara
   - Sugestões padrão ao criar novo (ctrl+shift+1, 2, 3...)
2. Atualizar `SettingsDialog` para incluir botão "Gerenciar Atalhos Personalizados"
3. Atualizar `MenuBuilder`:
   - Submenu "Atalhos Personalizados"
   - Item para cada shortcut configurado mostrando hotkey e prefixo
   - Indicador visual de qual está habilitado

**Critério de Sucesso**:
- UI funcional e intuitiva
- Detecção de teclas funcionando
- Validações em tempo real
- Preview do resultado
- Menu atualizado dinamicamente

**Tempo Estimado**: 6-7 horas (aumentou por causa do editor de hotkeys)

### 🔗 Etapa 5: Integração em main.py
**Objetivo**: Conectar tudo em `DahoraApp`

**Tarefas**:
1. Adicionar `_setup_custom_hotkeys()` em `DahoraApp.initialize()`
2. Criar callbacks para cada custom shortcut
3. Atualizar notificações para mostrar qual atalho foi usado
4. Passar `shortcut_id` ou `prefix` ao copiar data/hora
5. Atualizar mensagem "Sobre" com novos atalhos

**Critério de Sucesso**:
- Todos os shortcuts funcionando
- Notificações corretas
- Integração completa

**Tempo Estimado**: 2-3 horas

### 🧪 Etapa 6: Testes e Validação
**Objetivo**: Garantir que tudo funciona

**Tarefas**:
1. Testes manuais:
   - Instalar versão nova sobre versão antiga (testar migração)
   - Adicionar/editar/remover shortcuts
   - Testar todos os hotkeys
   - Verificar notificações
2. Testes automatizados:
   - `tests/test_multiple_shortcuts.py`
   - Testes de migração
   - Testes de conflitos de hotkeys
3. Testes de edge cases:
   - 9 shortcuts ativos
   - Desabilitar/reabilitar shortcuts
   - Conflitos de hotkeys

**Critério de Sucesso**:
- Testes passando
- Migração validada
- Nenhum bug crítico

**Tempo Estimado**: 3-4 horas

## Retrocompatibilidade Garantida

### Cenários de Upgrade
1. **Usuário sem configurações customizadas**:
   - Primeira execução cria shortcut padrão (Ctrl+Shift+1)
   - Hotkey legado (Ctrl+Shift+Q) continua funcionando

2. **Usuário com prefixo personalizado**:
   - Migração automática cria shortcut #1 com prefixo existente
   - Mantém comportamento idêntico
   - Hotkey legado preservado

3. **Usuário com configurações avançadas**:
   - Migração preserva todas as configurações
   - Adiciona novos campos com valores padrão

### Fallback e Recuperação
- Se migração falhar: restaura backup automático
- Se hotkey não registrar: log de erro mas continua execução
- Se configuração inválida: usa valores padrão

## Limites e Restrições
- **Máximo de 10 shortcuts personalizados** (recomendado, configurável)
- **Hotkeys totalmente customizáveis** pelo usuário
- **Sugestões padrão**: ctrl+shift+1 até ctrl+shift+9
- **Hotkeys reservados** (não podem ser sobrescritos):
  - Ctrl+C, Ctrl+V, Ctrl+X (sistema)
  - Ctrl+Shift+Q (copiar data/hora legado)
  - Ctrl+Shift+R (recarregar menu)
  - Ctrl+Shift+F (buscar histórico)
- Prefixos limitados a 50 caracteres
- Validação impede hotkeys duplicados ou inválidos

## Arquivos que Serão Modificados

### Modificações Significativas (Novos Métodos/Classes)
- `dahora_app/settings.py` ✏️
- `dahora_app/hotkeys.py` ✏️
- `main.py` ✏️

### Modificações Médias (Adaptações)
- `dahora_app/datetime_formatter.py` ✏️
- `dahora_app/ui/menu.py` ✏️

### Novos Arquivos
- `dahora_app/ui/custom_shortcuts_dialog.py` ✨
- `tests/test_multiple_shortcuts.py` ✨
- `docs/MIGRATION_MULTIPLE_PREFIXES.md` ✨ (este arquivo)

### Sem Modificação
- `dahora_app/clipboard_manager.py` ✅
- `dahora_app/counter.py` ✅
- `dahora_app/notifications.py` ✅
- `dahora_app/utils.py` ✅

## Riscos Gerais

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Corrupção de settings | Média | Alto | Backup automático + validação |
| Conflito de hotkeys | Alta | Médio | Try/catch individual + logs |
| UI complexa | Média | Médio | Design iterativo + feedback |
| Bugs em migração | Média | Alto | Testes extensivos + rollback |
| Performance | Baixa | Baixo | Poucos hotkeys, baixo overhead |

## Cronograma Estimado

| Etapa | Duração | Dependências |
|-------|---------|--------------|
| 0. Preparação | 30 min | - |
| 1. Modelo de Dados | 2-3h | Etapa 0 |
| 2. DateTimeFormatter | 1h | Etapa 1 |
| 3. HotkeyManager + Validação | 4-5h | Etapa 1 |
| 4. Interface UI + Editor Hotkeys | 6-7h | Etapas 1-3 |
| 5. Integração main.py | 2-3h | Etapas 1-4 |
| 6. Testes | 4-5h | Etapas 1-5 |
| **TOTAL** | **19-24h** | - |

## UI do Editor de Hotkeys (Preview)

```
┌────────────────────────────────────────────────────────┐
│  Gerenciar Atalhos Personalizados                    │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Atalhos Configurados:                                │
│  ┌────────────────────────────────────────────────┐   │
│  │ ✓ [Ctrl+Shift+1] DAHORA     (Prefixo padrão)  │   │
│  │ ✓ [Alt+F1]       URGENTE    (Tarefas urgentes)│   │
│  │ ✗ [Ctrl+Alt+D]   REUNIAO    (Notas de reunião)│   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
│  [➕ Adicionar]  [✏️ Editar]  [🗑️ Remover]            │
│                                                        │
├────────────────────────────────────────────────────────┤
│  Editar Atalho:                                        │
│                                                        │
│  Prefixo:     [DAHORA________________]                 │
│  Descrição:   [Prefixo padrão________]                 │
│                                                        │
│  Atalho:      [ctrl+shift+1__________] [⌨️ Detectar]  │
│               └── Status: ✅ Disponível                │
│                                                        │
│  Preview:     [DAHORA-05.11.2025-18:47]                │
│                                                        │
│  [ ] Habilitar este atalho                             │
│                                                        │
│  [💾 Salvar]  [❌ Cancelar]                            │
└────────────────────────────────────────────────────────┘

FLUXO DO BOTÃO "⌨️ Detectar":
1. Usuário clica em "Detectar Teclas"
2. Janela captura: "Pressione a combinação desejada..."
3. Usuário pressiona: Ctrl+Alt+D
4. Sistema detecta e preenche: "ctrl+alt+d"
5. Validação automática em tempo real
6. Mostra ✅ se ok ou ❌ se conflito
```

## Validações de Hotkeys

### ✅ Hotkeys Válidos (Exemplos)
- `ctrl+shift+1` até `ctrl+shift+9` (sugestões padrão)
- `alt+f1`, `alt+f2`, etc.
- `ctrl+alt+a`, `ctrl+alt+b`, etc.
- `shift+alt+1`, `shift+alt+2`, etc.
- `ctrl+shift+alt+z` (combinações mais complexas)

### ❌ Hotkeys Inválidos ou Reservados
- `ctrl+c`, `ctrl+v`, `ctrl+x` (sistema)
- `ctrl+shift+q` (usado pelo app - legado)
- `ctrl+shift+r` (usado pelo app - refresh)
- `ctrl+shift+f` (usado pelo app - busca)
- Duplicados dentro da própria lista

### ⚠️ Avisos
- Se hotkey já estiver em uso por outro app, tenta registrar
- Se falhar, avisa: "⚠️ Este atalho pode estar em uso por outro aplicativo"
- Permite salvar mesmo assim (tenta registrar na inicialização)

## Próximos Passos
1. ✅ Revisar este documento
2. ⏳ Aprovar o plano
3. ⏳ Criar branch Git
4. ⏳ Iniciar Etapa 1

## Notas Importantes
- **Não deletar métodos antigos** durante a migração
- **Sempre manter fallbacks** para evitar crashes
- **Testar migração** com settings reais antes do release
- **Documentar breaking changes** (se houver)

---
**Autor**: Dahora Team  
**Data**: 05.11.2025  
**Versão**: 1.0
