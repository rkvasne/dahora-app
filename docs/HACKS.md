# HACKs em main.py — Documentação de Workarounds

> Navegação: [Índice](INDEX.md) • [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

Este documento detalha os **workarounds, hacks e soluções não-ideais** encontradas em `main.py` que precisam ser revisitadas e possivelmente melhoradas.

## 1. Dark Mode Forçado em Menus do Windows

### Localização
**main.py, linhas 17-36**

### Problema
Pystray em Windows não respeita automaticamente o tema escuro do sistema, resultando em menus de contexto com tema claro mesmo quando o SO está configurado para dark mode.

### Solução Atual (Hack)
```python
# HACK: Forçar Dark Mode em menus nativos do Windows (Bandeja/Pystray)
import ctypes
uxtheme = ctypes.windll.uxtheme

# Tenta SetPreferredAppMode (Ordinal 135) - Win 10 1903+ / Win 11
# 2 = Force Dark Mode
try:
    uxtheme[135](2)
except:
    # Fallback: Tenta AllowDarkModeForApp (Ordinal 132) - Win 10 1809
    try:
        uxtheme[132](True)
    except:
        pass
```

### Por Que É um Hack
1. **APIs Não Documentadas:** Usa ordinais de funções não-públicas da DLL `uxtheme.dll`
2. **Varia por Versão:** Diferentes versões do Windows usam diferentes ordinais
3. **Sem Tratamento de Erro:** Se falhar, simplesmente continua com tema claro
4. **Hard-coded:** Números mágicos (135, 132) sem documentação clara

### Alternativas Consideradas
1. **Manifest XML:** Usar arquivo `.exe.manifest` com `<activeCodePage>`
   - Requer build com PyInstaller com manifest
   - Mais robusto mas menos flexível

2. **Pystray Update:** Aguardar atualização da biblioteca
   - Pystray não tem mais manutenção ativa
   - Unlikely que resolva tão cedo

3. **Qt/CustomTkinter para Menu:** Reimplementar menu em Qt
   - Complexo, quebra integração com Windows
   - Piora performance

### Impacto
- **Baixo:** Menu de contexto fica com tema claro em dark mode
- **Usuário Afetado:** Usuários com tema escuro no Windows 10 1809-1903
- **Severidade:** Cosmética (UX ruim, não funcional)

### Status
**CONHECIMENTO TÉCNICO NECESSÁRIO:** Windows API, ctypes, uxtheme.dll
**PRIORIDADE:** Baixa (cosmética)

---

## 2. Configuração de console UTF-8

### Localização
**main.py, linhas 38-46**

### Problema
Python no Windows por padrão usa encoding CP1252, causando problemas com caracteres especiais (á, é, ç, etc) em console e logs.

### Solução Atual
```python
try:
    import ctypes
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)  # UTF-8
    ctypes.windll.kernel32.SetConsoleCP(65001)       # UTF-8
except Exception:
    pass

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
```

### Por Que É um Hack
1. **Configuração dupla:** Tenta ctypes AND reconfigure (redundante)
2. **Falhas silenciosas:** Catches Exception, silenciosamente continua se falhar
3. **Plataforma Específica:** Só funciona em Windows
4. **Não Garante Sucesso:** Pode falhar em alguns ambientes (terminals específicos, etc)

### Alternativas
1. **PYTHONIOENCODING:** Usar variável de ambiente
   ```bash
   set PYTHONIOENCODING=utf-8
   ```

2. **setup.py/pyproject.toml:** Configurar em tempo de build
   ```python
   # pyproject.toml
   [tool.poetry]
   encoding = "utf-8"
   ```

3. **Logging com Encoding Explícito:** Já faz isso em RotatingFileHandler (correto)
   ```python
   RotatingFileHandler(..., encoding='utf-8')
   ```

### Impacto
- **Baixo:** Sem UTF-8, caracteres especiais aparecem como `?`
- **Casos Afetados:** Logs com timestamps em português, outputs do app
- **Severidade:** Média (funcional mas feio)

### Status
**CONHECIDO:** Funciona na maioria dos casos
**MANUTENÇÃO:** Baixo esforço se precisar ajustar

---

## 3. Single Instance Mutex (Incompleto)

### Localização
**main.py, linhas 130-131**

### Problema
Aplicação deveria ser single-instance (apenas uma execução por vez), mas implementação está incompleta.

### Código Atual
```python
global_icon = None
mutex_handle = None
```

### Status
- **Variáveis Globais Declaradas:** Sim
- **Lógica de Mutex Implementada:** Não
- **Função: check_single_instance():** Não encontrada em main.py
- **Resultado:** App pode ser iniciado múltiplas vezes

### Por Que É um Hack
1. **Incomplete Code:** Variáveis globais sem uso
2. **No Validation:** Nenhuma verificação de instância duplicada
3. **Deadlock Potencial:** Se houvesse código de mutex, poderia ficar preso

### Alternativas
1. **win32event (Windows):**
   ```python
   import win32event
   import win32con
   
   mutex = win32event.CreateEvent(None, 0, 0, "DahoraAppMutex")
   if win32event.WaitForSingleObject(mutex, 0) != 0:
       print("Already running")
       sys.exit(1)
   ```

2. **PID File (Cross-Platform):**
   ```python
   pid_file = Path(DATA_DIR) / "dahora.pid"
   if pid_file.exists():
       old_pid = pid_file.read_text().strip()
       if psutil.pid_exists(int(old_pid)):
           sys.exit(1)
   pid_file.write_text(str(os.getpid()))
   ```

3. **Socket Lock (Portável):**
   ```python
   import socket
   sock = socket.socket()
   try:
       sock.bind(('127.0.0.1', 12345))
   except OSError:
       print("Already running")
       sys.exit(1)
   ```

### Impacto
- **Alta:** Múltiplas instâncias causam:
  - Conflitos de clipboard
  - Múltiplos hotkeys registrados
  - Múltiplos monitors de clipboard
  - Consumo desnecessário de recursos

### Status
**CRÍTICO:** Deve ser implementado
**TODO:** Implementar single-instance check adequadamente

---

## 4. Thread de Tray Sem Sincronização Explícita

### Localização
**main.py, linhas 144, 1002+ (startup)**

### Problema
Pystray roda em thread separada, mas há pouca sincronização com a thread principal.

### Código Relevante
```python
self._tray_thread: Optional[threading.Thread] = None
self._shutdown_requested = False
self._ui_root = None
```

### Por Que É um Hack
1. **Thread Management:** Cria thread, mas controle é mínimo
2. **UI Root Singleton:** `self._ui_root` é singleton sem sincronização
3. **Shutdown Flag:** Flag booleana simples, não é thread-safe
4. **No Join/Timeout:** Não aguarda thread terminar explicitamente

### Padrão Ideal
```python
import threading

class DahoraApp:
    def __init__(self):
        self._shutdown_event = threading.Event()
        self._tray_ready = threading.Event()
        
    def _run_tray(self):
        # ... código tray ...
        self._tray_ready.set()
        
    def shutdown(self):
        self._shutdown_event.set()
        self._tray_thread.join(timeout=5)
        if self._tray_thread.is_alive():
            logging.warning("Tray thread did not terminate")
```

### Alternativas
1. **Usar Queue para Comunicação:**
   ```python
   self._tray_queue = queue.Queue()
   # Send messages: self._tray_queue.put(("action", data))
   # Receive: action, data = self._tray_queue.get(timeout=1)
   ```

2. **Usar contextvars para Isolamento:**
   ```python
   import contextvars
   _tray_context = contextvars.ContextVar('tray_app')
   ```

3. **Usar RLock para Sincronização:**
   ```python
   self._tray_lock = threading.RLock()
   # with self._tray_lock: ...
   ```

### Impacto
- **Médio:** Geralmente funciona mas pode ter race conditions em:
  - Shutdown durante operação tray
  - Múltiplas UI aberturas simultaneamente
  - Mudanças de settings durante tray refresh

### Status
**FUNCIONA MAS FRÁGIL:** Precisa refatoração thread-safety
**PRIORIDADE:** Média (pode causar crashes em casos extremos)

---

## 5. UI Root Singleton Sem Sincronização

### Localização
**main.py, vários métodos de UI**

### Problema
```python
self._ui_root = None  # Singleton sem lock
```

Usado em múltiplos callbacks que podem rodar em threads diferentes.

### Exemplo Problemático
```python
def _show_search_dialog(self):
    if self._ui_root is None:
        self._ui_root = tk.Tk()  # RACE CONDITION: Dois threads podem criar simultaneamente
```

### Por Que É um Hack
1. **TOCTOU (Time Of Check Time Of Use):** Verifica `None`, depois cria - intervalo vulnerável
2. **Sem Lock:** Múltiplas threads podem criar múltiplas roots simultaneamente
3. **Cleanup:** Nenhuma estratégia de quando deletar `_ui_root`

### Solução Ideal
```python
from threading import Lock

def _ensure_ui_root(self):
    """Garante UI root única, thread-safe"""
    with self._ui_lock:
        if self._ui_root is None:
            self._ui_root = tk.Tk()
            self._ui_root.withdraw()  # Esconde janela principal
        return self._ui_root

# Em todos os callbacks:
root = self._ensure_ui_root()
# ... usar root ...
```

### Impacto
- **Médio:** Raro em prática (UI callbacks geralmente em thread Tk), mas possível
- **Sintomas:** Crashes aleatórios ao abrir múltiplas dialogs
- **Reprodução:** Abrir settings + search + custom shortcuts muito rápido

### Status
**FUNCIONA NA MAIORIA DAS VEZES:** Problema teórico
**PRIORIDADE:** Baixa-Média (rare edge case)

---

## 6. Callbacks com Wrappers Complexos

### Localização
**main.py, linhas 200-230**

### Código
```python
self.custom_shortcuts_dialog.set_on_add_callback(
    self._on_add_custom_shortcut_wrapper  # Wrapper com registro imediato
)
self.custom_shortcuts_dialog.set_on_update_callback(
    self._on_update_custom_shortcut_wrapper  # Wrapper com re-registro
)
self.custom_shortcuts_dialog.set_on_remove_callback(
    self._on_remove_custom_shortcut_wrapper  # Wrapper com desregistro
)
```

### Por Que É um Hack
1. **Naming Confusion:** "wrapper" não explica o propósito
2. **Side Effects:** Callbacks fazem mais que atualizar settings
3. **Hard to Track:** Fluxo real é:
   - Dialog → wrapper callback
   - Wrapper → hotkey registration
   - Wrapper → settings save
   - Settings save → aplica hotkeys novamente (DUPLICAÇÃO)

4. **Indirection:** 3 níveis: dialog → wrapper → hotkey_manager

### Fluxo Atual (Confuso)
```
User modifica atalho
  ↓
Dialog chama on_add_callback (wrapper)
  ↓
Wrapper registra hotkey EM TEMPO REAL
  ↓
Wrapper chama on_save_callback
  ↓
on_save_callback aplica hotkeys NOVAMENTE
  ↓
RESULTADO: Hotkey registrado DUAS VEZES
```

### Solução Ideal
```python
class CustomShortcutsDialog:
    def save(self):
        """Salva tudo de uma vez"""
        new_settings = self._get_all_settings()
        self.on_save_callback(new_settings)
        # Deixa on_save_callback fazer ALL a work

class DahoraApp:
    def _on_settings_saved(self, settings):
        """Único entry point para salvar configurações"""
        self.settings_manager.update_all(settings)
        self._sync_all_components()  # Sincroniza hotkeys, UI, etc
```

### Impacto
- **Baixo-Médio:** Funciona, mas é confuso para manutenção
- **Problema:** Se adicionar novo tipo de config, callback precisa ser atualizado também
- **Fragmentação:** Lógica de "ao salvar" espalhada por múltiplos wrappers

### Status
**FUNCIONA:** Mas frágil e difícil de manter
**REFATORAÇÃO RECOMENDADA:** Consolidar em um único `_on_settings_saved()`

---

## 7. Fallback Manual vs Pydantic em Settings

### Localização
**settings.py, linhas 47-150**

### Problema
```python
def validate_settings(self, settings_dict):
    try:
        schema = SettingsSchema(**settings_dict)
        # ... usar schema ...
    except ValidationError:
        # Fallback para validação manual
        return self._validate_settings_manual(settings_dict)
```

### Por Que É um Hack
1. **Duplicação:** Dois sistemas de validação
2. **Inconsistência:** Se alguém atualizar Pydantic, manual fica desatualizado
3. **Cobertura Diferente:** Manual pode validar diferente de Pydantic
4. **Debugging Confuso:** Qual validação falhou?

### Alternativa
```python
def validate_settings(self, settings_dict):
    """Use Pydantic SEMPRE, com coerção agressiva"""
    try:
        # ConfigDict(coerce_numbers_to_str=True, ...) para converter automaticamente
        schema = SettingsSchema.model_validate(
            settings_dict,
            from_attributes=True
        )
        return schema.model_dump()
    except ValidationError as e:
        logging.error(f"Settings inválidas: {e}")
        # Não fallback: retorna defaults
        return SettingsSchema().model_dump()
```

### Impacto
- **Médio:** Se configurações antigas forem incompatíveis, Pydantic strict rejeita
- **Solução:** Adicionar migration script ou coerção em Pydantic

### Status
**FUNCIONA:** Mas é technical debt
**REFATORAÇÃO:** Remover fallback manual, usar Pydantic strict

---

## 8. Global Variables sem Context Manager

### Localização
**main.py, linhas 127-131**

### Código
```python
global_icon = None
mutex_handle = None

def main():
    global global_icon
    global_icon = icon  # Acesso global direto
```

### Por Que É um Hack
1. **Global State:** Difícil de testar
2. **Sem Cleanup:** `global_icon` não é deletado explicitamente
3. **Threading Issues:** Múltiplas threads acessam `global_icon` sem sincronização
4. **Anti-pattern:** "Globals are bad"

### Solução Ideal
```python
class DahoraApp:
    def __enter__(self):
        self.initialize()
        return self
    
    def __exit__(self, *args):
        self.shutdown()

# Uso
with DahoraApp() as app:
    app.run()
```

### Impacto
- **Baixo-Médio:** Funciona mas impede testes unitários
- **Testing:** Difícil mockar `global_icon` em testes

### Status
**FUNCIONA:** Mas impede testabilidade
**REFATORAÇÃO:** Usar context manager ou DI

---

## 9. Timestamps Sem Fuso Horário

### Localização
**datetime_formatter.py**

### Problema
App usa `datetime.now()` em vez de `datetime.now(timezone.utc)`, causando problemas em fusos diferentes.

### Impacto
- **Baixo:** Timestamps locais são o esperado
- **Problema Futuro:** Se app sincronizar com servidor, timestamps estarão errados

### Recomendação
```python
from datetime import datetime, timezone

# Correto
timestamp = datetime.now(timezone.utc).isoformat()

# Ou se quiser local com timezone info
import tzlocal
timestamp = datetime.now(tzlocal.get_localzone()).isoformat()
```

### Status
**FUNCIONA:** Timestamps locais são aceitáveis
**FUTURO:** Considerar UTC interno, exibir em local

---

## 10. Sem Validação de Tipos em Callbacks

### Localização
**main.py, múltiplos callbacks**

### Problema
Callbacks aceitam `*args` ou parâmetros genéricos, sem validação de tipo.

```python
def _on_copy_datetime_hotkey(self):  # Deveria validar que hotkey é str
    """Callback para copiar data/hora via hotkey"""
```

### Solução
```python
from typing import Protocol

class CopyDatetimeCallback(Protocol):
    def __call__(self) -> None: ...

class RefreshMenuCallback(Protocol):
    def __call__(self, icon: pystray.Icon, item: pystray.MenuItem) -> None: ...

# Em typing
self.copy_datetime_callback: Optional[CopyDatetimeCallback] = None
```

### Impacto
- **Baixo:** Não causa crashes em produção
- **Problema:** Type checkers (mypy) não validam

### Status
**FUNCIONA:** Sem type hints completos
**NICE TO HAVE:** Adicionar Protocols para melhor type checking

---

## 11. Prewarm de UI (anti-freeze) + Logs de Performance

### Localização
**main.py, método `_prewarm_ui()`**

### Problema
A primeira abertura de algumas janelas modernas (Configurações/Busca/Sobre) podia causar um “freeze” perceptível por conta do custo de criação/layout (CustomTkinter/Tk).

### Solução Atual
- O prewarm é agendado após o app subir (`after(700, ...)`) para não competir com o startup.
- O prewarm é “fatiado” em passos (`after(0, ...)`) para ceder o loop do Tk entre diálogos.
- Foram adicionados logs com `time.perf_counter()` (início/fim por diálogo e tempo total) para medir custo real.

### Por Que Entra em HACKS
1. **Chama métodos privados:** `_create_window()` dos diálogos modernos (dependência de implementação interna).
2. **Ações de window manager:** `withdraw()`/`deiconify()` variam por ambiente e podem falhar silenciosamente.
3. **Mitigação temporal:** evita travar no começo, mas não “resolve” o custo de criação em si.

### Impacto
- **Alto (UX):** reduz travamento perceptível no primeiro uso e gera métricas para diagnóstico.

### Status
**IMPLEMENTADO:** Com instrumentação de tempo e agendamento em idle.

---

## 12. Menu Dinâmico do Tray Calculado Mais de Uma Vez

### Localização
**dahora_app/ui/menu.py, método `create_dynamic_menu()`**

### Problema
Em alguns cenários, o gerador de itens do `pystray.Menu(...)` pode ser consumido mais de uma vez durante a mesma abertura do menu, o que duplica cálculo/logs e pode dar sensação de “trabalho em dobro”.

### Solução Atual
Cache curto por tempo (200ms) usando `time.monotonic()`:
- Se o menu for pedido novamente dentro dessa janela, reutiliza a lista já calculada.
- Fora do período, recalcula normalmente.

### Por Que Entra em HACKS
1. **Heurística por tempo:** não é uma garantia formal de “uma vez por abertura”.
2. **Dependente do comportamento do pystray/Windows:** pode mudar conforme versões.

### Impacto
- **Médio (performance/ruído de log):** reduz cálculos duplicados e torna abertura do menu mais previsível.

### Status
**IMPLEMENTADO:** Cache temporal mínimo no gerador.

---

## 13. Política de Logs: Rotação 1MB sem “Limpar no Startup”

### Localização
**dahora_app/constants.py** e **main.py (configuração de logging)**

### Problema
Limpar logs na inicialização apaga histórico útil e pode remover arquivos não versionados que existam no diretório de dados do usuário.

### Solução Atual
- Rotação via `RotatingFileHandler` com:
  - `LOG_MAX_BYTES = 1MB`
  - `LOG_BACKUP_COUNT = 1`
  - `mode="a"` (append)
- Sem rotina de exclusão de logs no startup.

### Impacto
- **Alto (diagnóstico):** preserva histórico recente (até ~2MB somando log + 1 backup) sem crescer indefinidamente.

### Status
**IMPLEMENTADO:** Rotação ativa e sem limpeza automática.

---

## 14. Compatibilidade de Settings: `description` em `custom_shortcuts`

### Localização
**dahora_app/schemas.py (CustomShortcutSchema)** e **dahora_app/settings.py (fallback manual já suportava)**

### Problema
`SettingsSchema` usava `extra='forbid'`. Se `settings.json` tivesse `custom_shortcuts[].description`, o Pydantic rejeitava e caía no fallback manual.

### Solução Atual
Adicionar o campo `description` ao `CustomShortcutSchema`, mantendo `extra='forbid'` para continuar rejeitando campos desconhecidos de verdade.

### Impacto
- **Médio (robustez):** reduz warnings de validação e evita fallback desnecessário.

### Status
**IMPLEMENTADO:** Schema aceita `description`.

---

## Resumo de Prioridades

| # | Hack | Severidade | Esforço | Prioridade | Status |
|---|------|-----------|--------|-----------|--------|
| 3 | Single Instance Mutex | 🔴 Alta | Médio | 🔴 CRÍTICO | ✅ Implementado (`single_instance.py`) |
| 4 | Thread Sync | 🟡 Média | Médio | 🟡 Média | ✅ Implementado (`thread_sync.py`) |
| 6 | Callbacks Wrappers | 🟠 Baixa | Alto | 🟡 Média | ✅ Implementado (CallbackManager + handlers) |
| 5 | UI Root Singleton | 🟡 Média | Médio | 🟡 Média | 🟡 A avaliar (legado/UI) |
| 7 | Validação Dupla | 🟠 Baixa | Médio | 🟢 Baixa | 🟡 Mantido (fallback seguro) |
| 10 | Type Hints | 🟢 Baixa | Médio | 🟢 Baixa | 🟡 A melhorar |
| 1 | Dark Mode API | 🟡 Média | Alto | 🟢 Baixa | 🟡 Não aplicável ao desktop |
| 2 | Console UTF-8 | 🟢 Baixa | Baixo | 🟢 Baixa | ✅ Resolvido/mitigado |
| 8 | Global Variables | 🟠 Baixa | Médio | 🟢 Baixa | 🟡 A revisar |
| 9 | Timestamps UTC | 🟢 Baixa | Baixo | 🟢 Baixa | 🟡 Backlog |

## Próximos Passos

1. **Curto Prazo:** Melhorar type hints e checagem estática (mypy).
2. **Curto Prazo:** Revisar dependências/arquivos UI legados e reduzir superfície de manutenção.
3. **Médio Prazo:** Reavaliar a necessidade de validação duplicada (manter fallback apenas onde necessário).
4. **Backlog:** Revisar “timestamps UTC” e variáveis globais onde houver impacto real.

---

**Última Atualização:** 6 de janeiro de 2026
**Documento de Referência para Refatoração Futura**
