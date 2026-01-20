"""
Testes de Integração dos Handlers no DahoraApp (Phase 6 Part 3)
Valida a integração do CallbackRegistry e handlers no main.py
"""
import pytest
from unittest.mock import MagicMock, patch, call
from typing import Optional

from dahora_app.callback_manager import CallbackRegistry
from dahora_app.handlers import (
    QuitAppHandler,
    CopyDateTimeHandler,
    ShowSettingsHandler,
    ShowSearchHandler,
)
from dahora_app.thread_sync import ThreadSyncManager


class MockDahoraApp:
    """Mock da DahoraApp para testes de integração"""
    
    def __init__(self):
        """Inicializa mock com todos os componentes necessários"""
        self._sync_manager = MagicMock(spec=ThreadSyncManager)
        self.clipboard_manager = MagicMock()
        self.datetime_formatter = MagicMock()
        self.notification_manager = MagicMock()
        self.counter = MagicMock()
        self.settings_manager = MagicMock()
        self.icon = MagicMock()
        self._ui_root = MagicMock()
        self.modern_settings_dialog = MagicMock()
        self.modern_search_dialog = MagicMock()


class TestHandlerIntegrationInApp:
    """Testes para integração de handlers na aplicação"""
    
    def test_registry_initialization_in_app(self):
        """Testa inicialização do CallbackRegistry na app"""
        registry = CallbackRegistry()
        assert registry is not None
        # Verifica que registry está vazio no início
        assert registry.get("quit_app") is None
    
    def test_register_quit_handler_in_app(self):
        """Testa registro do QuitAppHandler na app"""
        app = MockDahoraApp()
        handler = QuitAppHandler()
        handler.set_app(app)
        
        registry = CallbackRegistry()
        registry.register("quit_app", handler)
        
        assert registry.get("quit_app") is not None
        assert registry.get("quit_app").get_name() == "QuitAppHandler"
    
    def test_register_copy_datetime_handler_in_app(self):
        """Testa registro do CopyDateTimeHandler na app"""
        app = MockDahoraApp()
        handler = CopyDateTimeHandler()
        handler.set_app(app)
        handler.set_prefix("")
        
        registry = CallbackRegistry()
        registry.register("copy_datetime", handler)
        
        assert registry.get("copy_datetime") is not None
    
    def test_register_settings_handler_in_app(self):
        """Testa registro do ShowSettingsHandler na app"""
        app = MockDahoraApp()
        handler = ShowSettingsHandler()
        handler.set_app(app)
        handler.set_use_modern_ui(True)
        
        registry = CallbackRegistry()
        registry.register("show_settings", handler)
        
        assert registry.get("show_settings") is not None
    
    def test_register_search_handler_in_app(self):
        """Testa registro do ShowSearchHandler na app"""
        app = MockDahoraApp()
        handler = ShowSearchHandler()
        handler.set_app(app)
        handler.set_use_modern_ui(True)
        
        registry = CallbackRegistry()
        registry.register("show_search", handler)
        
        assert registry.get("show_search") is not None
    
    def test_execute_quit_handler_from_registry(self):
        """Testa execução do quit handler via registry"""
        app = MockDahoraApp()
        app._sync_manager.request_shutdown.return_value = True
        
        handler = QuitAppHandler()
        handler.set_app(app)
        
        registry = CallbackRegistry()
        registry.register("quit_app", handler)
        
        # Executa via registry
        result = registry.execute("quit_app")
        assert result is True
        app._sync_manager.request_shutdown.assert_called_once()
    
    def test_execute_copy_datetime_from_registry(self):
        """Testa execução do copy handler via registry"""
        app = MockDahoraApp()
        clipboard_state = {"value": "old content"}

        def get_text():
            return clipboard_state["value"]

        def set_text(value: str):
            clipboard_state["value"] = value

        app.clipboard_manager.get_text.side_effect = get_text
        app.clipboard_manager.set_text.side_effect = set_text
        app.datetime_formatter.format_datetime = MagicMock(return_value="2025-12-30")
        
        handler = CopyDateTimeHandler()
        handler.set_app(app)
        handler.set_prefix("")
        
        registry = CallbackRegistry()
        registry.register("copy_datetime", handler)
        
        # Executa via registry
        result = registry.execute("copy_datetime")
        assert result is True
    
    def test_execute_show_settings_from_registry(self):
        """Testa execução do settings handler via registry"""
        app = MockDahoraApp()
        handler = ShowSettingsHandler()
        handler.set_app(app)
        handler.set_use_modern_ui(True)
        
        registry = CallbackRegistry()
        registry.register("show_settings", handler)
        
        # Executa via registry
        result = registry.execute("show_settings")
        assert result is True
    
    def test_execute_show_search_from_registry(self):
        """Testa execução do search handler via registry"""
        app = MockDahoraApp()
        handler = ShowSearchHandler()
        handler.set_app(app)
        handler.set_use_modern_ui(True)
        
        registry = CallbackRegistry()
        registry.register("show_search", handler)
        
        # Executa via registry
        result = registry.execute("show_search")
        assert result is True
    
    def test_all_handlers_registered_together(self):
        """Testa registro de todos os handlers juntos"""
        app = MockDahoraApp()
        app._sync_manager.request_shutdown.return_value = True
        
        registry = CallbackRegistry()
        
        # Registra todos
        quit_handler = QuitAppHandler()
        quit_handler.set_app(app)
        registry.register("quit_app", quit_handler)
        
        copy_handler = CopyDateTimeHandler()
        copy_handler.set_app(app)
        copy_handler.set_prefix("")
        registry.register("copy_datetime", copy_handler)
        
        settings_handler = ShowSettingsHandler()
        settings_handler.set_app(app)
        settings_handler.set_use_modern_ui(True)
        registry.register("show_settings", settings_handler)
        
        search_handler = ShowSearchHandler()
        search_handler.set_app(app)
        search_handler.set_use_modern_ui(True)
        registry.register("show_search", search_handler)
        
        # Verifica todos registrados
        assert registry.get("quit_app") is not None
        assert registry.get("copy_datetime") is not None
        assert registry.get("show_settings") is not None
        assert registry.get("show_search") is not None
    
    def test_execute_all_handlers_from_registry(self):
        """Testa execução de todos os handlers via registry"""
        app = MockDahoraApp()
        app._sync_manager.request_shutdown.return_value = True
        clipboard_state = {"value": "old content"}

        def get_text():
            return clipboard_state["value"]

        def set_text(value: str):
            clipboard_state["value"] = value

        app.clipboard_manager.get_text.side_effect = get_text
        app.clipboard_manager.set_text.side_effect = set_text
        app.datetime_formatter.format_datetime = MagicMock(return_value="2025-12-30")
        
        registry = CallbackRegistry()
        
        # Registra e executa todos
        quit_handler = QuitAppHandler()
        quit_handler.set_app(app)
        registry.register("quit_app", quit_handler)
        
        copy_handler = CopyDateTimeHandler()
        copy_handler.set_app(app)
        copy_handler.set_prefix("")
        registry.register("copy_datetime", copy_handler)
        
        settings_handler = ShowSettingsHandler()
        settings_handler.set_app(app)
        settings_handler.set_use_modern_ui(True)
        registry.register("show_settings", settings_handler)
        
        search_handler = ShowSearchHandler()
        search_handler.set_app(app)
        search_handler.set_use_modern_ui(True)
        registry.register("show_search", search_handler)
        
        # Executa todos
        assert registry.execute("quit_app") is True
        assert registry.execute("copy_datetime") is True
        assert registry.execute("show_settings") is True
        assert registry.execute("show_search") is True
    
    def test_handler_with_prefix_configuration(self):
        """Testa handler com configuração de prefixo customizado"""
        app = MockDahoraApp()
        app.clipboard_manager.copy_text = MagicMock()
        
        handler = CopyDateTimeHandler()
        handler.set_app(app)
        handler.set_prefix("[CUSTOM]")
        
        registry = CallbackRegistry()
        registry.register("copy_datetime_custom", handler)
        
        # Verifica que o handler foi configurado
        retrieved_handler = registry.get("copy_datetime_custom")
        assert retrieved_handler is not None
    
    def test_handler_modern_ui_selection(self):
        """Testa seleção de UI moderna nos handlers"""
        app = MockDahoraApp()
        
        settings_handler = ShowSettingsHandler()
        settings_handler.set_app(app)
        settings_handler.set_use_modern_ui(True)
        
        search_handler = ShowSearchHandler()
        search_handler.set_app(app)
        search_handler.set_use_modern_ui(False)  # Classic UI
        
        registry = CallbackRegistry()
        registry.register("show_settings", settings_handler)
        registry.register("show_search", search_handler)
        
        # Ambos devem estar registrados
        assert registry.get("show_settings") is not None
        assert registry.get("show_search") is not None
    
    def test_menu_callbacks_replaced_with_registry(self):
        """Testa que callbacks do menu podem usar registry"""
        app = MockDahoraApp()
        clipboard_state = {"value": "old content"}

        def get_text():
            return clipboard_state["value"]

        def set_text(value: str):
            clipboard_state["value"] = value

        app.clipboard_manager.get_text.side_effect = get_text
        app.clipboard_manager.set_text.side_effect = set_text
        app.datetime_formatter.format_datetime = MagicMock(return_value="2025-12-30")
        
        registry = CallbackRegistry()
        
        # Cria handlers e registra
        copy_handler = CopyDateTimeHandler()
        copy_handler.set_app(app)
        copy_handler.set_prefix("")
        registry.register("copy_datetime", copy_handler)
        
        search_handler = ShowSearchHandler()
        search_handler.set_app(app)
        search_handler.set_use_modern_ui(True)
        registry.register("show_search", search_handler)
        
        # Simula callback do menu executando via registry
        # Ao invés de: self._copy_datetime_menu(icon, item)
        # Usa: registry.execute("copy_datetime")
        def menu_callback_copy(icon, item):
            return registry.execute("copy_datetime")
        
        def menu_callback_search(icon, item):
            return registry.execute("show_search")
        
        # Testa callbacks
        assert menu_callback_copy(None, None) is True
        assert menu_callback_search(None, None) is True
    
    def test_hotkey_callbacks_use_registry(self):
        """Testa que callbacks de hotkey podem usar registry"""
        app = MockDahoraApp()
        app._sync_manager.request_shutdown.return_value = True
        
        registry = CallbackRegistry()
        
        # Cria handlers e registra
        quit_handler = QuitAppHandler()
        quit_handler.set_app(app)
        registry.register("quit_app", quit_handler)
        
        # Simula hotkey callback
        def hotkey_callback():
            return registry.execute("quit_app")
        
        # Testa callback
        assert hotkey_callback() is True
    
    def test_error_handling_when_handler_fails(self):
        """Testa tratamento de erro quando handler falha"""
        app = MockDahoraApp()
        app._sync_manager.request_shutdown.return_value = False  # Falha
        
        handler = QuitAppHandler()
        handler.set_app(app)
        
        registry = CallbackRegistry()
        registry.register("quit_app", handler)
        
        # Executa e recebe False (falha silenciosa)
        result = registry.execute("quit_app")
        assert result is False
    
    def test_unregister_handler_from_registry(self):
        """Testa desregistro de handler"""
        app = MockDahoraApp()
        handler = QuitAppHandler()
        handler.set_app(app)
        
        registry = CallbackRegistry()
        registry.register("quit_app", handler)
        
        # Verifica registro
        assert registry.get("quit_app") is not None
        
        # Desregistra
        registry.unregister("quit_app")
        
        # Verifica desregistro
        assert registry.get("quit_app") is None
    
    def test_execute_nonexistent_handler(self):
        """Testa execução de handler que não existe"""
        registry = CallbackRegistry()
        
        # Tenta executar handler inexistente
        result = registry.execute("nonexistent")
        assert result is False
