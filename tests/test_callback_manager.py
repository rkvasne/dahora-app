"""
Testes para CallbackManager
"""
import pytest
import logging
from unittest.mock import Mock, MagicMock, patch

from dahora_app.callback_manager import (
    CallbackHandler,
    CallbackRegistry,
    get_callback_registry,
    initialize_callbacks,
    with_error_handling,
    with_ui_safety,
)


class MockHandler(CallbackHandler):
    """Handler mock para testes"""
    
    def __init__(self, name="mock", should_fail=False, side_effect=None):
        self.name = name
        self.should_fail = should_fail
        self.side_effect = side_effect
        self.call_count = 0
        self.last_args = None
        self.last_kwargs = None
    
    def handle(self, *args, **kwargs) -> bool:
        self.call_count += 1
        self.last_args = args
        self.last_kwargs = kwargs
        
        if self.side_effect:
            self.side_effect(*args, **kwargs)
        
        if self.should_fail:
            raise ValueError("Mock handler failed")
        
        return not self.should_fail
    
    def get_name(self) -> str:
        return self.name


class TestCallbackHandler:
    """Testes da classe base CallbackHandler"""
    
    def test_cannot_instantiate_abstract_class(self):
        """Não é possível instanciar CallbackHandler diretamente"""
        with pytest.raises(TypeError):
            CallbackHandler()
    
    def test_handler_repr(self):
        """Representação em string do handler"""
        handler = MockHandler("test_handler")
        assert "MockHandler" in repr(handler)
        assert "test_handler" in repr(handler)
    
    def test_concrete_handler_works(self):
        """Handler concreto funciona"""
        handler = MockHandler("test")
        result = handler.handle(1, 2, key="value")
        
        assert result is True
        assert handler.call_count == 1
        assert handler.last_args == (1, 2)
        assert handler.last_kwargs == {"key": "value"}


class TestCallbackRegistry:
    """Testes do CallbackRegistry"""
    
    def test_register_handler(self):
        """Registrar um handler"""
        registry = CallbackRegistry()
        handler = MockHandler("test")
        
        registry.register("my_callback", handler)
        
        assert registry.get("my_callback") is handler
        assert "my_callback" in registry.list_handlers()
    
    def test_register_invalid_handler_raises(self):
        """Registrar handler inválido deve lançar exceção"""
        registry = CallbackRegistry()
        
        with pytest.raises(ValueError):
            registry.register("bad", "not a handler")
    
    def test_register_duplicate_warns(self, caplog):
        """Registrar handler duplicado deve avisar"""
        registry = CallbackRegistry()
        handler1 = MockHandler("handler1")
        handler2 = MockHandler("handler2")
        
        registry.register("callback", handler1)
        
        with caplog.at_level(logging.WARNING):
            registry.register("callback", handler2)
        
        assert "Overwriting" in caplog.text
        assert registry.get("callback") is handler2
    
    def test_unregister_handler(self):
        """Desregistrar um handler"""
        registry = CallbackRegistry()
        handler = MockHandler("test")
        
        registry.register("callback", handler)
        assert registry.get("callback") is not None
        
        result = registry.unregister("callback")
        
        assert result is True
        assert registry.get("callback") is None
    
    def test_unregister_nonexistent_handler(self):
        """Desregistrar handler que não existe"""
        registry = CallbackRegistry()
        
        result = registry.unregister("nonexistent")
        
        assert result is False
    
    def test_get_nonexistent_handler(self):
        """Obter handler que não existe"""
        registry = CallbackRegistry()
        
        handler = registry.get("nonexistent")
        
        assert handler is None
    
    def test_execute_handler(self):
        """Executar um handler registrado"""
        registry = CallbackRegistry()
        handler = MockHandler("test")
        
        registry.register("callback", handler)
        result = registry.execute("callback", 1, 2, key="value")
        
        assert result is True
        assert handler.call_count == 1
        assert handler.last_args == (1, 2)
    
    def test_execute_nonexistent_handler(self):
        """Executar handler que não existe"""
        registry = CallbackRegistry()
        
        result = registry.execute("nonexistent")
        
        assert result is False
    
    def test_execute_handler_that_fails(self, caplog):
        """Executar handler que lança exceção"""
        registry = CallbackRegistry()
        handler = MockHandler("test", should_fail=True)
        
        registry.register("callback", handler)
        
        with caplog.at_level(logging.ERROR):
            result = registry.execute("callback")
        
        assert result is False
        assert "Error executing callback" in caplog.text
    
    def test_list_handlers(self):
        """Listar todos os handlers"""
        registry = CallbackRegistry()
        
        registry.register("cb1", MockHandler("h1"))
        registry.register("cb2", MockHandler("h2"))
        registry.register("cb3", MockHandler("h3"))
        
        handlers = registry.list_handlers()
        
        assert len(handlers) == 3
        assert "cb1" in handlers
        assert "cb2" in handlers
        assert "cb3" in handlers
    
    def test_list_handlers_info(self):
        """Listar handlers com informações"""
        registry = CallbackRegistry()
        
        registry.register("cb1", MockHandler("handler1"))
        registry.register("cb2", MockHandler("handler2"))
        
        info = registry.list_handlers_info()
        
        assert len(info) == 2
        assert ("cb1", "handler1") in info
        assert ("cb2", "handler2") in info
    
    def test_clear_all_handlers(self):
        """Limpar todos os handlers"""
        registry = CallbackRegistry()
        
        registry.register("cb1", MockHandler("h1"))
        registry.register("cb2", MockHandler("h2"))
        
        assert len(registry) == 2
        
        registry.clear()
        
        assert len(registry) == 0
        assert registry.list_handlers() == []
    
    def test_registry_length(self):
        """Teste do operador len"""
        registry = CallbackRegistry()
        
        assert len(registry) == 0
        
        registry.register("cb1", MockHandler())
        assert len(registry) == 1
        
        registry.register("cb2", MockHandler())
        assert len(registry) == 2
        
        registry.unregister("cb1")
        assert len(registry) == 1
    
    def test_registry_repr(self):
        """Representação em string do registry"""
        registry = CallbackRegistry()
        registry.register("cb1", MockHandler())
        registry.register("cb2", MockHandler())
        
        repr_str = repr(registry)
        
        assert "CallbackRegistry" in repr_str
        assert "2" in repr_str


class TestGlobalFunctions:
    """Testes das funções globais"""
    
    def test_get_callback_registry_singleton(self):
        """get_callback_registry retorna singleton"""
        registry1 = get_callback_registry()
        registry2 = get_callback_registry()
        
        assert registry1 is registry2
    
    def test_initialize_callbacks_returns_registry(self):
        """initialize_callbacks retorna registry"""
        registry = initialize_callbacks()
        
        assert isinstance(registry, CallbackRegistry)
    
    def test_initialize_callbacks_is_singleton(self):
        """initialize_callbacks retorna sempre o mesmo registry"""
        registry1 = initialize_callbacks()
        registry2 = initialize_callbacks()
        
        assert registry1 is registry2


class TestWithErrorHandling:
    """Testes do decorator @with_error_handling"""
    
    def test_decorator_on_handler_method(self):
        """Decorator pode ser usado em métodos de handler"""
        
        class TestHandler(CallbackHandler):
            @with_error_handling("test_handler")
            def handle(self, *args, **kwargs) -> bool:
                return True
            
            def get_name(self) -> str:
                return "TestHandler"
        
        handler = TestHandler()
        result = handler.handle()
        
        assert result is True
    
    def test_decorator_catches_exceptions(self, caplog):
        """Decorator captura exceções"""
        
        def failing_function():
            raise ValueError("Test error")
        
        decorated = with_error_handling("test")(failing_function)
        
        with caplog.at_level(logging.ERROR):
            result = decorated()
        
        assert result is False
        assert "Error in handler" in caplog.text
    
    def test_decorator_returns_function_result(self):
        """Decorator preserva resultado da função"""
        
        def success_function():
            return True
        
        decorated = with_error_handling("test")(success_function)
        result = decorated()
        
        assert result is True


class TestWithUISafety:
    """Testes do decorator @with_ui_safety"""
    
    def test_decorator_executes_normally_without_sync_manager(self):
        """Decorator funciona mesmo sem ThreadSyncManager"""
        
        def test_function():
            return True
        
        decorated = with_ui_safety(test_function)
        result = decorated()
        
        assert result is True
    
    def test_decorator_preserves_function_signature(self):
        """Decorator preserva assinatura da função"""
        
        def test_function(a, b, c=None):
            return (a, b, c)
        
        decorated = with_ui_safety(test_function)
        result = decorated(1, 2, c=3)
        
        assert result == (1, 2, 3)
    
    @patch("dahora_app.thread_sync.get_sync_manager")
    def test_decorator_uses_ui_operation(self, mock_get_sync_manager):
        """Decorator usa ui_operation quando disponível"""
        
        mock_sync_manager = MagicMock()
        mock_sync_manager.ui_operation = MagicMock()
        mock_sync_manager.ui_operation.return_value.__enter__ = MagicMock()
        mock_sync_manager.ui_operation.return_value.__exit__ = MagicMock()
        mock_get_sync_manager.return_value = mock_sync_manager
        
        def test_function():
            return True
        
        decorated = with_ui_safety(test_function)
        result = decorated()
        
        assert result is True


class TestIntegrationScenarios:
    """Testes de integração de múltiplos handlers"""
    
    def test_multiple_handlers_in_registry(self):
        """Múltiplos handlers podem coexistir"""
        registry = CallbackRegistry()
        
        h1 = MockHandler("h1")
        h2 = MockHandler("h2")
        h3 = MockHandler("h3")
        
        registry.register("callback1", h1)
        registry.register("callback2", h2)
        registry.register("callback3", h3)
        
        registry.execute("callback1", "arg1")
        registry.execute("callback2", "arg2")
        registry.execute("callback3", "arg3")
        
        assert h1.last_args == ("arg1",)
        assert h2.last_args == ("arg2",)
        assert h3.last_args == ("arg3",)
    
    def test_handler_reuses_after_unregister_and_register(self):
        """Handler pode ser removido e registrado novamente"""
        registry = CallbackRegistry()
        handler = MockHandler("test")
        
        registry.register("callback", handler)
        registry.execute("callback")
        
        registry.unregister("callback")
        registry.register("callback", handler)
        registry.execute("callback")
        
        assert handler.call_count == 2
    
    def test_registry_isolation_between_instances(self):
        """Instâncias diferentes de registry são independentes"""
        registry1 = CallbackRegistry()
        registry2 = CallbackRegistry()
        
        h1 = MockHandler("h1")
        h2 = MockHandler("h2")
        
        registry1.register("callback", h1)
        registry2.register("callback", h2)
        
        registry1.execute("callback")
        registry2.execute("callback")
        
        assert h1.call_count == 1
        assert h2.call_count == 1


class TestErrorHandling:
    """Testes de tratamento de erro"""
    
    def test_handler_exception_is_logged(self, caplog):
        """Exceção em handler é registrada"""
        registry = CallbackRegistry()
        handler = MockHandler("test", should_fail=True)
        
        registry.register("callback", handler)
        
        with caplog.at_level(logging.ERROR):
            result = registry.execute("callback")
        
        assert result is False
        assert "Error executing callback" in caplog.text
        assert "Mock handler failed" in caplog.text
    
    def test_handler_with_side_effect_error(self, caplog):
        """Handler que falha em side_effect"""
        
        def failing_side_effect(*args, **kwargs):
            raise RuntimeError("Side effect failed")
        
        registry = CallbackRegistry()
        handler = MockHandler("test", side_effect=failing_side_effect)
        
        registry.register("callback", handler)
        
        with caplog.at_level(logging.ERROR):
            result = registry.execute("callback")
        
        assert result is False
