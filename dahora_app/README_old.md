# Dahora App - Arquitetura Modular

Esta pasta contém a arquitetura modular do Dahora App, dividida em componentes especializados para melhor manutenibilidade e testabilidade.

## 📁 Estrutura

```
dahora_app/
├── __init__.py              # Módulo principal, expõe API pública
├── constants.py             # Constantes e configurações globais
├── utils.py                 # Funções utilitárias (atomic_write, etc)
├── settings.py              # Gerenciamento de settings (SettingsManager)
├── counter.py               # Gerenciamento de contador (UsageCounter)
├── clipboard_manager.py     # Gerenciamento de clipboard e histórico
├── datetime_formatter.py    # Formatação de data/hora (DateTimeFormatter)
├── notifications.py         # Sistema de notificações (NotificationManager)
├── hotkeys.py               # Gerenciamento de hotkeys globais (HotkeyManager)
└── ui/
    ├── __init__.py          # Módulo UI
    ├── prefix_dialog.py     # Diálogo de configuração de prefixo
    ├── icon_manager.py      # Gerenciamento de ícone da bandeja
    └── menu.py              # Criação e atualização de menus
```

## 🧩 Componentes

### **constants.py**
Centraliza todas as constantes do aplicativo:
- Informações do app (nome, versão)
- Caminhos de arquivos (settings, log, histórico, etc)
- Configurações (hotkeys, limites, intervalos)

### **utils.py**
Funções utilitárias reutilizáveis:
- `atomic_write_text()` - Escrita atômica de arquivos texto
- `atomic_write_json()` - Escrita atômica de JSON
- `truncate_text()` - Trunca texto para exibição
- `sanitize_text_for_display()` - Sanitiza texto

### **settings.py - SettingsManager**
Gerencia configurações persistentes:
- `load()` - Carrega settings do arquivo
- `save()` - Salva settings no arquivo
- `validate_settings()` - Valida e sanitiza settings
- `get_prefix()` / `set_prefix()` - Gerencia prefixo

### **counter.py - UsageCounter**
Gerencia contador de uso:
- `load()` - Carrega contador
- `save()` - Salva contador
- `increment()` - Incrementa e retorna valor
- `get_count()` - Retorna valor atual
- `reset()` - Reseta contador

### **clipboard_manager.py - ClipboardManager**
Gerencia clipboard e histórico:
- `load_history()` / `save_history()` - Persistência
- `add_to_history()` - Adiciona item
- `clear_history()` - Limpa histórico
- `get_recent_items()` - Obtém itens recentes
- `copy_text()` / `paste_text()` - Operações de clipboard
- `monitor_clipboard_smart()` - Monitor inteligente com polling adaptativo

### **datetime_formatter.py - DateTimeFormatter**
Formatação de data/hora:
- `format_now()` - Formata data/hora atual
- `format_datetime()` - Formata datetime específico
- `set_prefix()` - Define prefixo para formato

### **notifications.py - NotificationManager**
Sistema de notificações multi-canal:
- `show_toast()` - Toast nativo do Windows (winotify)
- `show_quick_notification()` - Notificação leve com Tkinter
- `show_fatal_error()` - MessageBox para erros fatais

### **hotkeys.py - HotkeyManager**
Gerencia hotkeys globais:
- `setup_all()` - Configura todas as hotkeys
- `set_*_callback()` - Define callbacks para ações
- `cleanup()` - Remove todas as hotkeys

### **ui/prefix_dialog.py - PrefixDialog**
Diálogo gráfico para configurar prefixo:
- Interface moderna com Tkinter
- Preview dinâmico do formato
- Validação de entrada

### **ui/icon_manager.py - IconManager**
Gerenciamento de ícone da bandeja:
- `load_icon()` - Carrega ícone de arquivo
- `get_icon_for_tray()` - Obtém ícone para bandeja
- `resolve_icon_path()` - Resolve path (suporta PyInstaller)

### **ui/menu.py - MenuBuilder**
Construtor de menus dinâmicos:
- `create_dynamic_menu()` - Cria menu com histórico atualizado
- Callbacks configuráveis para todas as ações
- Geração dinâmica de itens do histórico

## 🔄 Uso

### Importando componentes:

```python
from dahora_app import (
    SettingsManager,
    UsageCounter,
    ClipboardManager,
    DateTimeFormatter,
    NotificationManager,
    HotkeyManager,
    PrefixDialog,
    IconManager,
    MenuBuilder,
)
```

### Exemplo de uso:

```python
# Inicializa componentes
settings = SettingsManager()
settings.load()

counter = UsageCounter()
counter.load()

clipboard = ClipboardManager()
clipboard.load_history()

formatter = DateTimeFormatter(prefix=settings.get_prefix())

# Usa componentes
dt_string = formatter.format_now()  # "[04.11.2025-08:30]"
clipboard.copy_text(dt_string)
count = counter.increment()  # Incrementa e salva

print(f"Copiado {count} vezes!")
```

## ✅ Benefícios da Modularização

1. **Manutenibilidade**: Cada módulo tem responsabilidade única
2. **Testabilidade**: Componentes podem ser testados isoladamente
3. **Reutilização**: Módulos podem ser usados em outros projetos
4. **Legibilidade**: Código organizado e fácil de entender
5. **Escalabilidade**: Fácil adicionar novos componentes

## 🧪 Testes

Todos os componentes têm testes correspondentes em `tests/`:
- `test_settings.py` - Testa SettingsManager
- `test_datetime_formatter.py` - Testa DateTimeFormatter
- Cobertura: 95%

Execute com: `pytest tests/ -v`

## 📝 Histórico

- **v0.0.9**: Primeira versão modular
  - Migração de dahora_app.py monolítico para arquitetura modular
  - 13 módulos criados
  - ~1200 linhas organizadas em componentes especializados
  - 100% compatível com versão anterior
