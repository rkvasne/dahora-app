# HACKs e Decisões de Design — Dahora App

> Navegação: [Documentação](README.md) • [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

Este documento registra **workarounds e decisões de design** que impactam manutenção, compatibilidade ou UX.

## 1. Dark Mode Forçado em Menus do Windows

### Localização
**main.py, linhas 12-31**

### Problema
Pystray em Windows não respeita automaticamente o tema escuro do sistema, resultando em menus de contexto com tema claro mesmo quando o SO está configurado para dark mode.

### Solução Atual (Hack)
```python
# HACK: Forçar Dark Mode em menus nativos do Windows (Bandeja/Pystray)
import ctypes
from typing import Any, cast

uxtheme = cast(Any, ctypes.windll.uxtheme)

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
**WON'T FIX (Design Decision):**
- APIs não documentadas são a única forma de forçar dark mode em pystray
- Pystray não tem manutenção ativa, não há alternativa nativa
- O hack funciona na maioria das versões do Windows (10 1903+ / 11)
- Impacto é puramente cosmético (menu fica claro em dark mode para alguns usuários)
- Esforço para "resolver corretamente" (migrar para Qt/WxPython) não compensa

---

## 2. Configuração de console UTF-8

### Localização
**main.py, linhas 33-47**

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
    import sys
    from typing import Any, cast

    if sys.stdout is not None:
        cast(Any, sys.stdout).reconfigure(encoding="utf-8", errors="replace")
    if sys.stderr is not None:
        cast(Any, sys.stderr).reconfigure(encoding="utf-8", errors="replace")
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

## 3) Itens tratados (resumo)

Os itens que anteriormente exigiam workarounds internos foram tratados na implementação atual, e o detalhamento antigo foi removido deste arquivo para evitar contradições com o código.

- Instância única: `dahora_app/single_instance.py`
- Sincronização de threads: `dahora_app/thread_sync.py`
- UI root thread-safe e prewarm da UI moderna: `dahora_app/app.py`
- CallbackRegistry + handlers: `dahora_app/callback_manager.py` e `dahora_app/handlers/`
- Menu dinâmico com cache curto: `dahora_app/ui/menu.py`
- Rotação de logs: `main.py` (RotatingFileHandler)
- Compatibilidade de settings (`description` em atalhos): `dahora_app/schemas.py`

---

## Resumo de Prioridades

| # | Hack | Severidade | Esforço | Prioridade | Status |
|---|------|-----------|--------|-----------|--------|
| 3 | Single Instance Mutex | 🔴 Alta | Médio | 🔴 CRÍTICO | ✅ Implementado (`single_instance.py`) - 21 testes |
| 4 | Thread Sync | 🟡 Média | Médio | 🟡 Média | ✅ Implementado (`thread_sync.py`) |
| 5 | UI Root Singleton | 🟡 Média | Médio | 🟡 Média | ✅ Implementado (Lock em `_ensure_ui_root`) |
| 6 | Callbacks Wrappers | 🟠 Baixa | Alto | 🟡 Média | ✅ Implementado (CallbackRegistry + 4 handlers) |
| 7 | Validação Dupla | 🟠 Baixa | Médio | 🟢 Baixa | ✅ Removida (SettingsSchema em `settings.py`, sem `_validate_settings_manual`) |
| 10 | Type Hints | 🟢 Baixa | Médio | 🟢 Baixa | ✅ Implementado (8 Protocols em `callback_manager.py`) |
| 1 | Dark Mode API | 🟡 Média | Alto | 🟢 Baixa | ✅ Won't Fix (design - APIs não documentadas são a única opção) |
| 2 | Console UTF-8 | 🟢 Baixa | Baixo | 🟢 Baixa | ✅ Resolvido/mitigado |
| 8 | Global Variables | 🟠 Baixa | Médio | 🟢 Baixa | ✅ Mitigado (config flake8 em `.flake8`) |
| 9 | Timestamps UTC | 🟢 Baixa | Baixo | 🟢 Baixa | ✅ Won't Fix (design - app offline, timestamps locais são corretos) |
| 11 | Prewarm UI | 🟡 Média | Médio | 🟡 Média | ✅ Implementado |
| 12 | Menu Cache | 🟠 Baixa | Baixo | 🟢 Baixa | ✅ Implementado |
| 13 | Logs Rotação | 🟢 Baixa | Baixo | 🟢 Baixa | ✅ Implementado |
| 14 | Description Compat | 🟢 Baixa | Baixo | 🟢 Baixa | ✅ Implementado |

### Estatísticas (12/01/2026)

- **Total de Hacks:** 14
- **Tratados:** 14 (100%) ✅
  - Resolvidos/Implementados: 12
  - Won't Fix (design decisions): 2
- **Testes:** suíte automatizada (pytest) — ver `tests/README.md`

## Próximos Passos

1. ~~**Curto Prazo:** Melhorar type hints e checagem estática (mypy).~~ ✅ **COMPLETO** (8 Protocols)
2. ~~**Curto Prazo:** Revisar dependências/arquivos UI legados.~~ ✅ **CONFIGURADO** (flake8 em `.flake8`)
3. ~~**Médio Prazo:** Remover validação duplicada.~~ ✅ **COMPLETO** (SettingsSchema em `settings.py`)
4. ~~**Opcional:** Timestamps UTC~~ ✅ **WON'T FIX** (design - app offline)
5. ~~**Opcional:** Dark Mode API~~ ✅ **WON'T FIX** (design - APIs não documentadas são necessárias)

**🎉 TODOS OS HACKS TRATADOS! 100%**

---

**Última Atualização:** 12 de janeiro de 2026
**Documento de Referência para Refatoração Futura**
