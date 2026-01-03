# Arquitetura da Dahora App

> Navegação: [Índice](INDEX.md) • [README do projeto](../README.md) • [Release](RELEASE.md)

Documentação detalhada sobre a estrutura, componentes e padrões de design utilizados no projeto.

## 1. Visão Geral

Dahora App é um aplicativo de gerenciamento de timestamps com clipboard e hotkeys globais. O projeto segue uma arquitetura modular com separação clara de responsabilidades entre componentes.

### Estrutura de Diretórios

```
dahora_app/
├── __init__.py                    # Inicialização e exports principais
├── main.py                        # Entrada da aplicação (no root)
├── hotkeys.py                     # Gerenciador de hotkeys globais
├── hotkey_validator.py            # Validação segura de hotkeys (NOVO)
├── clipboard_manager.py           # Monitor de clipboard
├── settings.py                    # Gerenciador de configurações persistentes
├── schemas.py                     # Modelos Pydantic para validação (NOVO)
├── notifications.py               # Sistema de notificações
├── constants.py                   # Constantes do projeto
├── utils.py                       # Funções utilitárias
├── datetime_formatter.py           # Formatação de datas/horas
├── counter.py                     # Contador de eventos
├── ui/                            # Interface gráfica
│   ├── __init__.py
│   ├── menu.py                    # Menu da bandeja
│   ├── modern_settings_dialog.py  # Diálogo de configurações
│   ├── modern_shortcut_editor.py  # Editor de atalhos
│   ├── modern_search_dialog.py    # Diálogo de busca
│   ├── modern_about_dialog.py     # Diálogo sobre
│   ├── modern_styles.py           # Estilos da UI moderna
│   ├── icon_manager.py            # Gerenciador de ícones
│   └── ... (deprecated)           # Versões antigas mantidas para compatibilidade
└── __pycache__/                   # Cache Python

tests/                             # Suíte de testes
├── test_hotkey_validator.py       # 37 testes de validação de hotkeys (NOVO)
├── test_schemas.py                # 29 testes de schemas Pydantic (NOVO)
├── test_hotkey_manager_custom.py  # Testes de custom shortcuts
├── test_custom_shortcuts.py       # Testes de atalhos
└── ... (mais testes)
```

## 2. Fluxo de Execução

### Inicialização da Aplicação

```
main.py
  ├─> load settings
  ├─> initialize HotkeyManager
  ├─> setup HotkeyValidator (centralized)
  ├─> setup clipboard monitoring
  ├─> apply configured hotkeys
  ├─> register custom shortcuts
  └─> show system tray icon
```

## 3. Componentes Principais

### 3.1 HotkeyManager (`hotkeys.py`)

**Responsabilidade:** Gerenciar hotkeys globais do sistema, incluindo hotkeys do app e custom shortcuts.

**Características:**
- Registra hotkeys via biblioteca `keyboard`
- Mantém lista de hotkeys reservados (sistema)
- Valida hotkeys usando `HotkeyValidator`
- Suporta callbacks por hotkey
- Thread-safe com RLock

**Métodos Principais:**
- `validate_hotkey(hotkey, exclude_shortcut_id)` - Valida usando HotkeyValidator
- `setup_custom_hotkeys(custom_shortcuts)` - Registra múltiplos atalhos
- `_register_custom_shortcut(shortcut_id, hotkey)` - Registra um atalho específico
- `set_custom_shortcut_callback(shortcut_id, callback)` - Define callback

**Fluxo de Validação:**
```
User hotkey input
  ├─> HotkeyManager.validate_hotkey()
  │   ├─> HotkeyValidator.is_valid()  <- Validação de formato
  │   ├─> Check reserved hotkeys
  │   └─> Check conflicts with other shortcuts
  └─> Register or reject
```

### 3.2 HotkeyValidator (`hotkey_validator.py`) - NOVO

**Responsabilidade:** Validação segura e centralizada de hotkeys.

**Características:**
- Validação de formato (deve ter modificador + tecla)
- Bloqueio de teclas perigosas (Escape, Pause)
- Reserva apenas Ctrl+C para o sistema
- Suporte para símbolos (exclam→!, at→@, etc)
- Normalização de hotkeys
- Mensagens de erro detalhadas

**Classes:**
- `HotkeyValidator` - Classe principal
  - `is_valid(hotkey)` - Retorna bool
  - `validate_with_reason(hotkey)` - Retorna (bool, str_razao)
  - `normalize(hotkey)` - Padroniza formato
  - `parse(hotkey)` - Analisa componentes
  - `suggest_free_hotkey()` - Sugere alternativa válida

**Validações Realizadas:**
- ✓ Formato: `modifier+key` (ex: `ctrl+shift+a`)
- ✓ Bloqueio: Escape, Pause
- ✓ Símbolos: Conversão automática (exclam→!, shift+1→!)
- ✓ Tamanho: Min 3 chars (`a+b`), Max 50 chars
- ✓ Caracteres válidos: `[a-z0-9+\-_\s]`

### 3.3 SettingsManager (`settings.py`)

**Responsabilidade:** Carregar, validar e persistir configurações.

**Características:**
- Carregamento de arquivo JSON
- Validação com Pydantic `SettingsSchema`
- Fallback para validação manual se Pydantic falhar
- Atomicidade em escrita (via `atomic_write_json`)
- Thread-safe

**Integração com Schemas:**
```
load()
  ├─> read settings.json
  ├─> validate_settings() (Pydantic)
  │   ├─> SettingsSchema validation
  │   └─> Fallback to _validate_settings_manual()
  └─> apply configuration
```

### 3.4 Pydantic Schemas (`schemas.py`) - NOVO

**Responsabilidade:** Definir estrutura e validações de dados de forma centralizada.

**Classes:**

#### CustomShortcutSchema
```python
id: int                    # >= 1, único
hotkey: str               # min 3, max 50 chars, deve ter '+'
prefix: str               # max 100, sanitizado
enabled: bool             # default True
```

Validações:
- Hotkey format: deve conter '+' e formato válido
- Prefix sanitization: remove caracteres de controle
- Extra fields: rejeitados (extra='forbid')

#### SettingsSchema
```python
prefix: str               # max 100
hotkey_copy_datetime: str # padrão: ctrl+shift+q
hotkey_search_history: str # padrão: ctrl+shift+f
hotkey_refresh_menu: str   # padrão: ctrl+shift+r
max_history_items: int     # 10-1000, padrão: 100
clipboard_monitor_interval: float # 0.5-60s, padrão: 3
clipboard_idle_threshold: int # 5-300s, padrão: 30
datetime_format: str       # deve ter componente de data/hora
bracket_open: str          # 1 char, != bracket_close
bracket_close: str         # 1 char, != bracket_open
custom_shortcuts: List[CustomShortcutSchema] # max 10
default_shortcut_id: Optional[int] # existe em custom_shortcuts
notification_duration: int # 1-10s, padrão: 2
notification_enabled: bool # padrão: True
```

Validações:
- Brackets diferentes (open != close)
- Datetime format válido (tem %d, %m, %Y, %H, %M, ou %S)
- Prefix control chars removidos
- Custom shortcuts: max 10
- Default shortcut ID existe
- Hotkeys duplicados detectados
- IDs únicos

#### NotificationSchema
```python
enabled: bool           # padrão: True
duration_seconds: int   # 1-10s, padrão: 2
show_on_error: bool     # padrão: True
```

#### AppConfigSchema
```python
settings: SettingsSchema
notifications: NotificationSchema
```

### 3.5 ClipboardManager (`clipboard_manager.py`)

**Responsabilidade:** Monitorar clipboard e gerenciar histórico.

**Características:**
- Monitora mudanças em clipboard
- Armazena histórico criptografado no Windows (DPAPI)
- Ignora timestamps gerados pelo próprio app
- Suporta formatação customizável de timestamps
- Detecta inatividade para aplicar prefix

### 3.6 Interface Gráfica (`ui/`)

**Componentes:**
- `menu.py` - Menu de bandeja do Windows
- `modern_settings_dialog.py` - Diálogo de configurações (Pydantic-aware)
- `modern_shortcut_editor.py` - Editor de custom shortcuts (com HotkeyValidator)
- `modern_search_dialog.py` - Busca no histórico
- `icon_manager.py` - Gerenciamento de ícones SVG
- `modern_styles.py` - Temas escuro/claro

## 4. Fluxo de Dados

### Carregamento de Configurações

```
Program Start
  ↓
SettingsManager.load()
  ├─ Read settings.json
  ├─ SettingsSchema.validate() (Pydantic)
  │  ├─ HotkeyValidator checks (via hotkeys.py)
  │  ├─ Bracket validation
  │  ├─ Custom shortcuts validation
  │  └─ Prefix sanitization
  ├─ Fallback to manual validation if needed
  └─ Apply settings to UI components
```

### Validação de Hotkey (Novo)

```
User enters hotkey
  ↓
HotkeyManager.validate_hotkey()
  ├─ HotkeyValidator.is_valid()
  │  ├─ Check format (modifier+key)
  │  ├─ Check reserved keys
  │  ├─ Normalize and parse
  │  └─ Return bool
  ├─ Check system reserved hotkeys
  ├─ Check conflicts with custom shortcuts
  └─ Return (bool, error_message)
    ↓
If valid: Register hotkey with keyboard library
If invalid: Show error to user
```

### Salvamento de Configurações

```
User changes setting
  ↓
SettingsManager.update_all(settings_dict)
  ├─ Validate with SettingsSchema
  ├─ Apply to internal state
  └─ Save to settings.json (atomic)
    ↓
HotkeyManager updates hotkeys if needed
  ├─ Unregister old hotkeys
  └─ Register new hotkeys
```

## 5. Validação em Camadas

### Camada 1: Pydantic Schemas (Mais Rigorosa)

Validação estruturada e centralizada de todos os dados:
- Hotkey format validation
- Bracket pair validation
- Duplicate detection
- ID uniqueness
- Field constraints (min/max length, ranges)

**Quando usar:** Carregamento de arquivo, salvamento, importação de dados

### Camada 2: HotkeyValidator (Especializada)

Validação especializada apenas para hotkeys:
- Format parsing
- Symbol conversion
- Reserved key detection
- Human-friendly error messages

**Quando usar:** Qualquer entrada de hotkey (criar, editar, validar)

### Camada 3: HotkeyManager.validate_hotkey() (Integrada)

Combinação de HotkeyValidator + verificações de conflito:
- HotkeyValidator checks (formato)
- Reserved hotkeys checks (sistema)
- Conflict detection (outros shortcuts)

**Quando usar:** Antes de registrar hotkey no sistema

## 6. Segurança

### Validações de Hotkey

- **Bloqueios Hard:** Escape, Pause (podem danificar sistema)
- **Sistema Preservado:** Ctrl+C (único hotkey reservado do app para evitar lockup)
- **Formato Obrigatório:** Modifier + key (evita conflitos com texto)
- **Símbolos Suportados:** Conversão automática (exclam→!, etc)

### Validações de Configuração

- **Sanitização de Prefixo:** Remove caracteres de controle
- **Brackets Validados:** Não podem ser whitespace, devem ser diferentes
- **Limites Enforçados:** Max 100 histórico, max 10 custom shortcuts
- **Campos Extras:** Rejeitados pela Pydantic (extra='forbid')

### Tratamento de Erros

- Fallback de validação (Pydantic → Manual)
- Logging detalhado de erros
- Recuperação graceful com defaults

## 7. Padrões de Design

### Singleton-like (com instância global)
```python
# No main.py
hotkey_manager = HotkeyManager()
settings_manager = SettingsManager()
```

### Validator Pattern
```python
validator = HotkeyValidator()
is_valid, reason = validator.validate_with_reason(hotkey)
```

### Pydantic Models (Data Validation)
```python
try:
    schema = SettingsSchema(**raw_data)
except ValidationError as e:
    handle_error(e)
```

### Fallback Pattern (Validação)
```python
try:
    validated = SettingsSchema(**data)
except ValidationError:
    # Fallback to manual validation
    validated = _validate_settings_manual(data)
```

## 8. Tratamento de Erros

### Contexto: Validação Pydantic

```python
from pydantic import ValidationError
from dahora_app.schemas import SettingsSchema

try:
    schema = SettingsSchema(**settings_dict)
except ValidationError as e:
    for error in e.errors():
        field = error['loc'][0]
        msg = error['msg']
        logging.error(f"Campo '{field}': {msg}")
    # Fallback
    return _validate_settings_manual(settings_dict)
```

### Contexto: Validação de Hotkey

```python
valid, reason = hotkey_manager.validate_hotkey(hotkey)
if not valid:
    show_error(f"Hotkey inválido: {reason}")
    # reason pode ser:
    # - "Hotkey não pode ser vazio"
    # - "Hotkey deve ter pelo menos um '+' (ex: ctrl+shift+q)"
    # - "Hotkey 'ctrl+c' é reservado pelo sistema"
    # - "Hotkey 'ctrl+shift+q' já está em uso por outro atalho"
```

## 9. Testes

### Suite de Testes Total: 133 testes

#### HotkeyValidator (37 testes) - `test_hotkey_validator.py`
- Normalização (10 testes)
- Parsing (8 testes)
- Validação (7 testes)
- Sugestões (3 testes)
- Símbolos (4 testes)
- Edge cases (5 testes)

#### Schemas (29 testes) - `test_schemas.py`
- CustomShortcutSchema (8 testes)
- SettingsSchema (16 testes)
- NotificationSchema (2 testes)
- AppConfigSchema (3 testes)

#### Outros Testes (67 testes)
- Custom shortcuts (22 testes)
- Datetime formatter (12 testes)
- Hotkey manager (21 testes)
- Settings (10 testes)

### Executar Testes

```bash
# Todos os testes
py -m pytest

# Testes específicos
py -m pytest tests/test_hotkey_validator.py -v
py -m pytest tests/test_schemas.py -v

# Com coverage
py -m pytest --cov=dahora_app tests/
```

## 10. Dependências Adicionadas

### Pydantic v2.0+
```
py -m pip install pydantic>=2.0
```

**Uso:**
- Validação estruturada de dados
- Type hints com validação automática
- Mensagens de erro detalhadas
- Serialização/deserialização automática

## 11. Backward Compatibility

### Mantida 100%

- Validação Pydantic com fallback para manual
- Novos módulos não modificam código existente
- HotkeyValidator integrado sem quebrar validação existente
- Schemas usam os mesmos campos que settings.py

### Migração de Dados

Settings antigos são automaticamente validados e convertidos:
```python
# Arquivo settings.json antigo
{"prefix": "old_prefix", ...}
  ↓
Carregado por SettingsSchema (com sanitização)
  ↓
Validado e aplicado
```

## 12. Fluxo de Desenvolvimento Futuro

### Próximas Etapas Sugeridas

1. **Integração de APIs:** Usar schemas para validar dados de APIs externas
2. **Testes de Integração:** UI + Schemas + HotkeyValidator
3. **Documentação de HACKs:** Identificar e documentar workarounds
4. **Performance:** Caching de validação, otimização de clipboard monitor
5. **Testes de Estresse:** Validar com 100+ custom shortcuts

## 13. Guia de Manutenção

### Adicionar Novo Hotkey Validável

1. Editar `HotkeyValidator` se necessário
2. Editar `SettingsSchema` para novo campo
3. Editar `SettingsManager` para carregar novo campo
4. Editar `HotkeyManager` para usar novo hotkey
5. Adicionar testes em `test_schemas.py` e `test_hotkey_validator.py`

### Alterar Regras de Validação

1. Editar `SettingsSchema` ou `HotkeyValidator`
2. Atualizar testes correspondentes
3. Rodar full test suite: `pytest`
4. Verificar backward compatibility

### Adicionar Nova Configuração

1. Definir em `SettingsSchema`
2. Adicionar validação customizada se necessário
3. Atualizar `SettingsManager`
4. Atualizar UI
5. Adicionar testes

## 14. Referências

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Keyboard Library](https://github.com/boppreh/keyboard)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

---

**Última Atualização:** December 2025
**Versão da Documentação:** 1.0
**Status:** Completa e em produção
