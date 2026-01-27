# 🔍 Pesquisa: Otimização de Clipboard Monitor com Windows API Events

**Data da Pesquisa:** 13 de janeiro de 2026  
**Versão (na época da pesquisa):** v0.2.12  
**Versão atual (referência do repo):** v0.2.16  
**Status:** ✅ **PESQUISA CONCLUÍDA** - Implementação futura recomendada
**Status (documento):** Histórico — pesquisa concluída; não é guia operacional

---

## 📋 Resumo Executivo

Esta pesquisa investiga a viabilidade de otimizar o monitoramento de clipboard usando Windows API Events (`AddClipboardFormatListener`) em vez de polling adaptativo, para reduzir uso de CPU em idle.

**Status:** ✅ **PESQUISA CONCLUÍDA**  
**Recomendação:** Implementação futura (após testes extensivos)

---

## 1. Contexto Atual

### Implementação Atual (Polling Adaptativo)

O `ClipboardManager` atualmente usa polling adaptativo:
- Verifica clipboard a cada intervalo configurável (`clipboard_monitor_interval`)
- Adapta intervalo baseado em atividade (reduz quando idle)
- Thread-safe com locks
- Funciona bem, mas usa CPU mesmo quando clipboard não muda

**Código Atual:**
```python
def monitor_clipboard_smart(self, on_change_callback=None) -> None:
    while True:
        current_content = pyperclip.paste()
        if current_content != self.last_clipboard_content:
            # Processar mudança
        time.sleep(sleep_time)  # Polling
```

---

## 2. Abordagem Proposta: Windows API Events

### AddClipboardFormatListener

Windows API fornece `AddClipboardFormatListener` que:
- Registra uma janela para receber `WM_CLIPBOARDUPDATE` quando clipboard muda
- **Zero polling** - evento disparado apenas quando clipboard realmente muda
- Reduz CPU em idle para quase zero

### Requisitos de Implementação

Para implementar isso, seria necessário:

1. **Criar Janela Oculta:**
   - Usar `win32gui.WNDCLASS` e `win32gui.CreateWindow`
   - Janela invisível apenas para receber mensagens
   - Thread separada para loop de mensagens

2. **Registrar Listener:**
   - `ctypes.windll.user32.AddClipboardFormatListener(hwnd)`
   - Processar mensagens `WM_CLIPBOARDUPDATE` (0x031D)

3. **Loop de Mensagens:**
   - `win32gui.PumpMessages()` ou loop customizado
   - Thread separada para não bloquear aplicação principal

4. **Cleanup:**
   - `RemoveClipboardFormatListener(hwnd)` no shutdown
   - `DestroyWindow(hwnd)` e `UnregisterClass`

### Código de Referência (Pesquisa)

```python
import ctypes
import win32clipboard
import win32gui
import win32con
import threading

WM_CLIPBOARDUPDATE = 0x031D

def window_proc(hwnd, msg, wparam, lparam):
    if msg == WM_CLIPBOARDUPDATE:
        # Clipboard mudou - processar
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                # Processar texto
            win32clipboard.CloseClipboard()
        except Exception:
            pass
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

# Criar janela e registrar
wc = win32gui.WNDCLASS()
wc.lpfnWndProc = window_proc
wc.lpszClassName = 'DahoraClipboardListener'
class_atom = win32gui.RegisterClass(wc)

hwnd = win32gui.CreateWindow(class_atom, 'DahoraClipboardListener', 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)
ctypes.windll.user32.AddClipboardFormatListener(hwnd)

# Loop de mensagens em thread separada
def message_loop():
    win32gui.PumpMessages()

thread = threading.Thread(target=message_loop, daemon=True)
thread.start()
```

---

## 3. Complexidade e Riscos

### Complexidade Técnica: **ALTA**

- Requer criação e gerenciamento de janela Windows
- Loop de mensagens em thread separada
- Cleanup adequado necessário
- Integração com código existente (fallback para polling)
- Thread-safety entre mensagens Windows e código Python

### Riscos Identificados

1. **Compatibilidade:**
   - Apenas Windows (requer fallback para outros sistemas se aplicável)
   - Requer `pywin32` (já disponível no projeto)

2. **Complexidade Arquitetural:**
   - Mudança significativa na arquitetura atual
   - Requer integração com sistema de shutdown existente
   - Thread separada para loop de mensagens

3. **Testes:**
   - Requer testes extensivos para garantir que funciona corretamente
   - Testes de cleanup em shutdown
   - Testes de thread-safety
   - Testes de compatibilidade com código existente

4. **Manutenibilidade:**
   - Código Windows API é mais complexo que polling
   - Requer conhecimento de Windows API para debug
   - Possíveis race conditions entre threads

### Benefícios vs. Riscos

**Benefícios:**
- ✅ Zero CPU quando clipboard não muda
- ✅ Resposta instantânea quando clipboard muda
- ✅ Melhor para usuários com clipboard raramente usado

**Riscos:**
- ⚠️ Alta complexidade de implementação
- ⚠️ Risco de introduzir bugs
- ⚠️ Requer testes extensivos
- ⚠️ Polling atual funciona bem

---

## 4. Recomendações

### Opção 1: Implementação Híbrida (Recomendada para Futuro)

Implementar Windows API Events com fallback para polling:
- Tenta usar `AddClipboardFormatListener` se disponível
- Se falhar ou não disponível, usa polling atual
- Mantém compatibilidade total

**Vantagens:**
- Melhor performance quando disponível
- Fallback seguro se não disponível
- Compatibilidade garantida

**Desvantagens:**
- Código mais complexo (duas implementações)
- Requer testes para ambos os caminhos

### Opção 2: Manter Polling Atual (Recomendada por Enquanto)

O polling atual funciona bem:
- CPU usage baixo (intervalo adaptativo)
- Código simples e testado
- Sem riscos de introduzir bugs

**Recomendação Atual:** Manter polling até que haja necessidade real de otimização (performance issues relatados).

---

## 5. Implementação Futura (Quando Necessário)

### Passos para Implementação

1. **Criar módulo `clipboard_events.py`:**
   - Implementar classe `ClipboardEventMonitor`
   - Gerenciar janela Windows e loop de mensagens
   - Thread-safe com locks

2. **Integrar com `ClipboardManager`:**
   - Adicionar método `monitor_clipboard_events()`
   - Manter `monitor_clipboard_smart()` como fallback
   - Escolher método baseado em disponibilidade

3. **Testes:**
   - Testes unitários para evento Windows
   - Testes de integração
   - Testes de cleanup
   - Testes de thread-safety

4. **Documentação:**
   - Atualizar `architecture.md`
   - Documentar comportamento híbrido
   - Guia de troubleshooting

### Código Base para Implementação Futura

```python
# dahora_app/clipboard_events.py (futuro)
try:
    import win32gui
    import win32con
    import win32clipboard
    import ctypes
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

class ClipboardEventMonitor:
    """Monitor de clipboard usando Windows API Events"""
    
    def __init__(self, callback):
        self.callback = callback
        self.hwnd = None
        self.running = False
        
    def start(self):
        if not WIN32_AVAILABLE:
            return False
        # Implementar criação de janela e registro
        # ...
        
    def stop(self):
        # Cleanup: RemoveClipboardFormatListener, DestroyWindow
        # ...
```

---

## 6. Conclusão

### Status da Pesquisa: ✅ **CONCLUÍDA**

- ✅ Pesquisa sobre `AddClipboardFormatListener` realizada
- ✅ Código de referência obtido
- ✅ Complexidade avaliada
- ✅ Riscos identificados
- ✅ Recomendação documentada

### Recomendação Final

**Manter polling atual por enquanto:**
- Polling funciona bem e é simples
- CPU usage já é baixo (polling adaptativo)
- Não há problemas de performance reportados
- Implementação de eventos é complexa e arriscada

**Implementação futura:**
- Quando houver necessidade real de otimização
- Após planejamento adequado
- Com testes extensivos
- Em implementação híbrida (eventos + fallback polling)

---

## 7. Referências

- [AddClipboardFormatListener (Microsoft Docs)](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-addclipboardformatlistener)
- [WM_CLIPBOARDUPDATE Message](https://learn.microsoft.com/en-us/windows/win32/dataxchg/wm-clipboardupdate)
- [Python pywin32 Documentation](https://github.com/mhammond/pywin32)

---

**Fim da Pesquisa**

*Esta pesquisa foi realizada em 13 de janeiro de 2026. Para implementação futura, revisar este documento e seguir os passos recomendados.*
