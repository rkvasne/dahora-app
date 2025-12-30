"""
Testes para handlers de callbacks específicos
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, call
import threading

from dahora_app.handlers import (
    QuitAppHandler,
    CopyDateTimeHandler,
    ShowSettingsHandler,
    ShowSearchHandler,
)


class MockApp:
    """Mock de DahoraApp para testes"""
    
    def __init__(self):
        self._sync_manager = MagicMock()
        self._ui_root = MagicMock()
        self.datetime_formatter = MagicMock()
        self.clipboard_manager = MagicMock()
        self.settings_manager = MagicMock()
        self.settings_dialog = MagicMock()
        self.modern_settings_dialog = MagicMock()
        self.search_dialog = MagicMock()
        self.modern_search_dialog = MagicMock()


class TestQuitAppHandler:
    """Testes para QuitAppHandler"""
    
    def test_create_handler_without_app(self):
        """Pode criar handler sem app inicialmente"""
        handler = QuitAppHandler()
        
        assert handler.app is None
        assert handler.get_name() == "QuitAppHandler"
    
    def test_create_handler_with_app(self):
        """Pode criar handler com app injetada"""
        app = MockApp()
        handler = QuitAppHandler(app)
        
        assert handler.app is app
    
    def test_set_app(self):
        """Pode injetar app depois"""
        handler = QuitAppHandler()
        app = MockApp()
        
        handler.set_app(app)
        
        assert handler.app is app
    
    def test_handle_without_app(self):
        """Retorna False se app não foi injetada"""
        handler = QuitAppHandler()
        
        result = handler.handle()
        
        assert result is False
    
    def test_handle_successful_shutdown(self):
        """Shutdown bem-sucedido"""
        app = MockApp()
        app._sync_manager.request_shutdown.return_value = True
        
        handler = QuitAppHandler(app)
        result = handler.handle()
        
        assert result is True
        app._sync_manager.request_shutdown.assert_called_once()
        app._ui_root.after.assert_called_once()
    
    def test_handle_shutdown_already_requested(self):
        """Retorna False se shutdown já foi requisitado"""
        app = MockApp()
        app._sync_manager.request_shutdown.return_value = False
        
        handler = QuitAppHandler(app)
        result = handler.handle()
        
        assert result is False
    
    def test_handle_with_icon(self):
        """Param icon é processado corretamente"""
        app = MockApp()
        app._sync_manager.request_shutdown.return_value = True
        icon = MagicMock()
        
        handler = QuitAppHandler(app)
        result = handler.handle(icon=icon)
        
        assert result is True
        icon.stop.assert_called_once()
    
    def test_handle_error_handling(self):
        """Exceções são capturadas e logadas"""
        app = MockApp()
        app._sync_manager.request_shutdown.side_effect = RuntimeError("Test error")
        
        handler = QuitAppHandler(app)
        result = handler.handle()
        
        assert result is False
    
    def test_handler_repr(self):
        """Handler tem boa representação em string"""
        handler = QuitAppHandler()
        
        assert "QuitAppHandler" in repr(handler)


class TestCopyDateTimeHandler:
    """Testes para CopyDateTimeHandler"""
    
    def test_create_handler_without_app(self):
        """Pode criar handler sem app inicialmente"""
        handler = CopyDateTimeHandler()
        
        assert handler.app is None
        assert handler.prefix == ""
        assert handler.get_name() == "CopyDateTimeHandler"
    
    def test_set_app(self):
        """Pode injetar app depois"""
        handler = CopyDateTimeHandler()
        app = MockApp()
        
        handler.set_app(app)
        
        assert handler.app is app
    
    def test_set_prefix(self):
        """Pode definir prefixo"""
        handler = CopyDateTimeHandler()
        
        handler.set_prefix("debug")
        
        assert handler.prefix == "debug"
    
    def test_handle_without_app(self):
        """Retorna False se app não foi injetada"""
        handler = CopyDateTimeHandler()
        
        result = handler.handle()
        
        assert result is False
    
    def test_handle_successful_copy(self):
        """Cópia bem-sucedida"""
        app = MockApp()
        app.datetime_formatter.format_datetime.return_value = "2025-12-30 10:30:00"
        app.clipboard_manager.get_clipboard.return_value = "old content"
        app.settings_manager.settings.template = "%Y-%m-%d %H:%M:%S"
        app.settings_manager.settings.separator = "-"
        
        handler = CopyDateTimeHandler(app)
        result = handler.handle()
        
        assert result is True
        app.clipboard_manager.copy_to_clipboard.assert_called()
    
    def test_handle_with_prefix(self):
        """Cópia com prefixo"""
        app = MockApp()
        app.datetime_formatter.format_datetime.return_value = "2025-12-30 10:30:00"
        app.clipboard_manager.get_clipboard.return_value = "old content"
        app.settings_manager.settings.template = "%Y-%m-%d %H:%M:%S"
        app.settings_manager.settings.separator = "-"
        
        handler = CopyDateTimeHandler(app)
        handler.set_prefix("log")
        result = handler.handle()
        
        assert result is True
        # Verifica se prefix foi adicionado
        call_args = app.clipboard_manager.copy_to_clipboard.call_args
        assert "log" in call_args[0][0]
    
    def test_handle_error_handling(self):
        """Exceções são capturadas"""
        app = MockApp()
        app.datetime_formatter.format_datetime.side_effect = RuntimeError("Format error")
        
        handler = CopyDateTimeHandler(app)
        result = handler.handle()
        
        assert result is False
    
    def test_handle_clipboard_preservation(self):
        """Clipboard é preservado após delay"""
        app = MockApp()
        app.datetime_formatter.format_datetime.return_value = "2025-12-30"
        app.clipboard_manager.get_clipboard.return_value = "old content"
        app.settings_manager.settings.template = "%Y-%m-%d"
        app.settings_manager.settings.separator = "-"
        
        handler = CopyDateTimeHandler(app)
        result = handler.handle()
        
        assert result is True
        # Cópia original é feita
        app.clipboard_manager.copy_to_clipboard.assert_called_with("2025-12-30")


class TestShowSettingsHandler:
    """Testes para ShowSettingsHandler"""
    
    def test_create_handler_without_app(self):
        """Pode criar handler sem app inicialmente"""
        handler = ShowSettingsHandler()
        
        assert handler.app is None
        assert handler.use_modern_ui is True
        assert handler.get_name() == "ShowSettingsHandler"
    
    def test_set_app(self):
        """Pode injetar app"""
        handler = ShowSettingsHandler()
        app = MockApp()
        
        handler.set_app(app)
        
        assert handler.app is app
    
    def test_set_use_modern_ui(self):
        """Pode alterar preferência de UI"""
        handler = ShowSettingsHandler()
        
        handler.set_use_modern_ui(False)
        
        assert handler.use_modern_ui is False
    
    def test_handle_without_app(self):
        """Retorna False se app não foi injetada"""
        handler = ShowSettingsHandler()
        
        result = handler.handle()
        
        assert result is False
    
    def test_handle_show_modern_settings(self):
        """Exibe settings moderna"""
        app = MockApp()
        app.settings_manager.settings.use_modern_ui = True
        
        handler = ShowSettingsHandler(app)
        result = handler.handle()
        
        assert result is True
        app.modern_settings_dialog.show.assert_called_once()
    
    def test_handle_show_classic_settings(self):
        """Exibe settings clássica"""
        app = MockApp()
        app.settings_manager.settings.use_modern_ui = False
        
        handler = ShowSettingsHandler(app)
        result = handler.handle()
        
        assert result is True
        app.settings_dialog.show.assert_called_once()
    
    def test_handle_dialog_not_initialized(self):
        """Retorna False se dialog não está inicializado"""
        app = MockApp()
        app.settings_manager.settings.use_modern_ui = True
        app.modern_settings_dialog = None
        
        handler = ShowSettingsHandler(app)
        result = handler.handle()
        
        assert result is False
    
    def test_handle_error_handling(self):
        """Exceções são capturadas"""
        app = MockApp()
        app.settings_manager.settings = MagicMock()
        app.settings_manager.settings.use_modern_ui = True
        app.modern_settings_dialog = MagicMock()
        app.modern_settings_dialog.show.side_effect = RuntimeError("Settings error")
        
        handler = ShowSettingsHandler(app)
        result = handler.handle()
        
        # Mesmo com erro, handler trata exceção
        assert result is False


class TestShowSearchHandler:
    """Testes para ShowSearchHandler"""
    
    def test_create_handler_without_app(self):
        """Pode criar handler sem app inicialmente"""
        handler = ShowSearchHandler()
        
        assert handler.app is None
        assert handler.use_modern_ui is True
        assert handler.get_name() == "ShowSearchHandler"
    
    def test_set_app(self):
        """Pode injetar app"""
        handler = ShowSearchHandler()
        app = MockApp()
        
        handler.set_app(app)
        
        assert handler.app is app
    
    def test_set_use_modern_ui(self):
        """Pode alterar preferência de UI"""
        handler = ShowSearchHandler()
        
        handler.set_use_modern_ui(False)
        
        assert handler.use_modern_ui is False
    
    def test_handle_without_app(self):
        """Retorna False se app não foi injetada"""
        handler = ShowSearchHandler()
        
        result = handler.handle()
        
        assert result is False
    
    def test_handle_show_modern_search(self):
        """Exibe search moderna"""
        app = MockApp()
        app.settings_manager.settings.use_modern_ui = True
        
        handler = ShowSearchHandler(app)
        result = handler.handle()
        
        assert result is True
        app.modern_search_dialog.show.assert_called_once()
    
    def test_handle_show_classic_search(self):
        """Exibe search clássica"""
        app = MockApp()
        app.settings_manager.settings.use_modern_ui = False
        
        handler = ShowSearchHandler(app)
        result = handler.handle()
        
        assert result is True
        app.search_dialog.show.assert_called_once()
    
    def test_handle_dialog_not_initialized(self):
        """Retorna False se dialog não está inicializado"""
        app = MockApp()
        app.settings_manager.settings.use_modern_ui = True
        app.modern_search_dialog = None
        
        handler = ShowSearchHandler(app)
        result = handler.handle()
        
        assert result is False
    
    def test_handle_error_handling(self):
        """Exceções são capturadas"""
        app = MockApp()
        app.settings_manager.settings = MagicMock()
        app.settings_manager.settings.use_modern_ui = True
        app.modern_search_dialog = MagicMock()
        app.modern_search_dialog.show.side_effect = RuntimeError("Search error")
        
        handler = ShowSearchHandler(app)
        result = handler.handle()
        
        # Mesmo com erro, handler trata exceção
        assert result is False


class TestHandlerIntegration:
    """Testes de integração entre handlers"""
    
    def test_all_handlers_can_be_initialized(self):
        """Todos os handlers podem ser criados"""
        app = MockApp()
        
        quit_handler = QuitAppHandler(app)
        copy_handler = CopyDateTimeHandler(app)
        settings_handler = ShowSettingsHandler(app)
        search_handler = ShowSearchHandler(app)
        
        assert quit_handler.get_name() == "QuitAppHandler"
        assert copy_handler.get_name() == "CopyDateTimeHandler"
        assert settings_handler.get_name() == "ShowSettingsHandler"
        assert search_handler.get_name() == "ShowSearchHandler"
    
    def test_handlers_accept_common_params(self):
        """Handlers aceitam parâmetros comuns de callback"""
        app = MockApp()
        icon = MagicMock()
        item = MagicMock()
        
        handlers = [
            QuitAppHandler(app),
            ShowSettingsHandler(app),
            ShowSearchHandler(app),
        ]
        
        # Todos devem aceitar icon e item
        for handler in handlers:
            try:
                handler.handle(icon=icon, item=item)
            except TypeError:
                pytest.fail(f"{handler.get_name()} doesn't accept icon/item params")
