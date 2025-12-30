# PHASE 6: Callback Logic Consolidation

## Objetivo

Consolidar e refatorar lógica de callbacks do aplicativo, centralizando manipuladores de eventos e melhorando testabilidade, manutenibilidade e thread-safety.

## Status

- 🟡 **Planejado** - Próxima fase após Phase 5
- Dependências: Phase 1, 4, 5 (✅ COMPLETAS)
- Estimativa: 40-60 testes novos

## Problemas Identificados

### 1. Callbacks Espalhados em main.py

**Localização:** `main.py` linhas 400-800+
**Exemplos:**
```python
def _quit_app(self, icon, item):
    # Callback do pystray - 30+ linhas de lógica

def _show_notifications(self, item):
    # Callback do menu - 10+ linhas

def _on_hotkey_pressed(self, hotkey_name):
    # Callback de hotkey - 40+ linhas de lógica
```

**Problema:**
- ❌ Callbacks são lambdas/closures sem encapsulamento
- ❌ Lógica de negócio misturada com setup de callbacks
- ❌ Difícil testar isoladamente
- ❌ Reutilização de código limitada

### 2. MenuBuilder Sem Integração de Callbacks

**Localização:** `dahora_app/ui/menu.py`
**Problema:**
- ❌ Callbacks passados após menu construído
- ❌ Sem validação de callbacks antes de usar
- ❌ Sem documentação clara de contrato de callback

### 3. Falta de CallbackHandler Central

**Problema:**
- ❌ Sem padrão consistente para handlers
- ❌ Sem retry logic para operações que podem falhar
- ❌ Sem logging centralizado de eventos

### 4. UI Operations Sem Thread Safety (Parcial)

**Problema:**
- ⚠️ Alguns callbacks usam `_ui_root.after()` manualmente
- ⚠️ Não usam o novo `ThreadSyncManager.ui_operation()`
- ⚠️ Inconsistência após Phase 5

## Solução Proposta

### 1. Criar Novo Módulo: `dahora_app/callback_manager.py`

```python
class CallbackHandler(ABC):
    """Base class para todos os handlers de callback"""
    
    @abstractmethod
    def handle(self, *args, **kwargs) -> bool:
        """Executa o callback, retorna sucesso/falha"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna nome descritivo do handler"""
        pass


class QuitAppHandler(CallbackHandler):
    """Handler para encerrar aplicativo"""
    
    def __init__(self, app: DahoraApp):
        self.app = app
    
    def handle(self, icon=None, item=None) -> bool:
        """Encerra aplicativo de forma segura"""
        try:
            if not self.app._sync_manager.request_shutdown():
                return False  # Já foi requisitado
            
            # Lógica de shutdown...
            return True
        except Exception as e:
            logging.error(f"Error in {self.get_name()}: {e}")
            return False
    
    def get_name(self) -> str:
        return "QuitAppHandler"


class CopyDateTimeHandler(CallbackHandler):
    """Handler para copiar data/hora"""
    
    def handle(self, hotkey_name: str = None) -> bool:
        """Copia timestamp para clipboard"""
        # Implementação...
        pass
    
    def get_name(self) -> str:
        return "CopyDateTimeHandler"


class CallbackRegistry:
    """Registry central de callbacks"""
    
    def __init__(self):
        self._handlers: Dict[str, CallbackHandler] = {}
    
    def register(self, name: str, handler: CallbackHandler) -> None:
        """Registra um novo handler"""
        self._handlers[name] = handler
    
    def get(self, name: str) -> CallbackHandler:
        """Obtém um handler registrado"""
        return self._handlers.get(name)
    
    def execute(self, name: str, *args, **kwargs) -> bool:
        """Executa um handler registrado"""
        handler = self.get(name)
        if handler:
            return handler.handle(*args, **kwargs)
        return False
    
    def list_handlers(self) -> List[str]:
        """Lista todos os handlers registrados"""
        return list(self._handlers.keys())
```

### 2. Refatorar main.py

**Antes:**
```python
def _quit_app(self, icon, item):
    if self._shutdown_requested:
        return
    # 30+ linhas de lógica...
```

**Depois:**
```python
def _quit_app(self, icon, item):
    self.callback_registry.execute("quit_app", icon, item)
```

### 3. Integrar com MenuBuilder

```python
# menu.py
class MenuBuilder:
    def __init__(self, callback_registry: CallbackRegistry):
        self.callback_registry = callback_registry
    
    def build(self) -> pystray.Menu:
        return pystray.Menu(
            pystray.MenuItem(
                "Quit",
                self._make_menu_callback("quit_app")
            ),
            # ...
        )
    
    def _make_menu_callback(self, handler_name: str):
        """Cria callback que delega para registry"""
        def callback(icon, item):
            self.callback_registry.execute(handler_name, icon, item)
        return callback
```

### 4. Testes de Callbacks

```python
# tests/test_callback_manager.py

class TestCallbackRegistry:
    def test_register_and_execute(self):
        registry = CallbackRegistry()
        handler = MockHandler()
        
        registry.register("test", handler)
        result = registry.execute("test", arg1=1)
        
        assert result is True
        assert handler.was_called


class TestQuitAppHandler:
    def test_quit_app_success(self):
        app = MockDahoraApp()
        handler = QuitAppHandler(app)
        
        result = handler.handle()
        
        assert result is True
        assert app.was_shutdown


class TestCallbackErrorHandling:
    def test_handler_exception_is_logged(self):
        registry = CallbackRegistry()
        bad_handler = BadHandler()  # Throws exception
        
        registry.register("bad", bad_handler)
        result = registry.execute("bad")
        
        assert result is False
        # Exception should be logged
```

## Integração com ThreadSyncManager

```python
class CallbackHandler:
    def handle_safe(self, *args, **kwargs) -> bool:
        """Executa callback com proteção de thread"""
        sync_manager = get_sync_manager()
        
        # Para operações de UI
        with sync_manager.ui_operation():
            return self.handle(*args, **kwargs)
```

## Benefícios

1. ✅ **Testabilidade:** Cada handler pode ser testado isoladamente
2. ✅ **Manutenibilidade:** Lógica consolidada em um lugar
3. ✅ **Reutilização:** Handlers podem ser compartilhados entre UI e testes
4. ✅ **Thread-Safety:** Integração com ThreadSyncManager
5. ✅ **Observabilidade:** Logging centralizado de eventos
6. ✅ **Extensibilidade:** Novos handlers são fáceis de adicionar

## Arquivos a Criar

1. `dahora_app/callback_manager.py` (300+ linhas)
   - CallbackHandler base class
   - Implementações específicas (Quit, Copy, Show Settings, etc)
   - CallbackRegistry singleton

2. `tests/test_callback_manager.py` (300+ linhas, 25-30 testes)
   - Testes de registro
   - Testes de execução
   - Testes de error handling
   - Testes de thread-safety

## Arquivos a Modificar

1. `main.py`
   - Inicializar CallbackRegistry
   - Migrar callbacks para handlers
   - Reduzir de 978 para ~850 linhas (128 linhas economizadas)

2. `dahora_app/ui/menu.py`
   - Aceitar CallbackRegistry no construtor
   - Criar callbacks que delegam para registry

3. `dahora_app/__init__.py`
   - Exportar CallbackHandler, CallbackRegistry, implementações específicas

## Commits Esperados

1. `feat(callbacks): Add CallbackManager with handler base class`
   - Novo módulo callback_manager.py
   - Testes iniciais

2. `feat(callbacks): Implement specific handlers (Quit, Copy, Settings, etc)`
   - Implementações de handlers
   - Testes específicos

3. `refactor(main): Integrate CallbackRegistry into DahoraApp`
   - Refator de main.py
   - Integração com MenuBuilder

4. `docs: Add Phase 6 summary - Callback Logic Consolidation`
   - Documentação completa
   - Exemplos de uso

## Métricas Esperadas

| Métrica | Valor |
|---------|-------|
| Testes Novos | 25-30 |
| Linhas Adicionadas | 600+ |
| Linhas Economizadas (main.py) | 128 |
| Breaking Changes | 0 |
| Taxa de Passagem | 100% (205-210 testes) |

## Critérios de Sucesso

- ✅ 25-30 novos testes passando
- ✅ 0 breaking changes
- ✅ main.py reduzido em linhas sem perder funcionalidade
- ✅ Todos os callbacks migrados para handlers
- ✅ Documentação completa com exemplos
- ✅ 2-3 commits descritivos

## Próximas Dependências

Phase 6 será dependência para:
- Phase 7: Completion de Type Hints (handlers bem tipados)
- Phase 8: UTC Timestamps (handlers usam DateTimeFormatter)
- Phase 9: Performance & Caching (callbacks podem ser cacheados)

---

**Status:** Pronto para início imediatamente após Phase 5 ✅
