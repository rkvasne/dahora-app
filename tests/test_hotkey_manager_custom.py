"""
Testes para HotkeyManager com Custom Shortcuts
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from dahora_app.hotkeys import HotkeyManager


class TestHotkeyValidation:
    """Testes de validação de hotkeys"""
    
    @pytest.fixture
    def manager(self):
        """Cria HotkeyManager para testes"""
        return HotkeyManager()
    
    def test_validate_hotkey_valid(self, manager):
        """Testa validação de hotkeys válidos"""
        valid_hotkeys = [
            "ctrl+shift+1",
            "alt+f1",
            "ctrl+alt+d",
            "shift+alt+a",
            "ctrl+shift+alt+z"
        ]
        
        for hotkey in valid_hotkeys:
            valid, msg = manager.validate_hotkey(hotkey)
            assert valid is True, f"Hotkey '{hotkey}' deveria ser válido"
            assert "válido" in msg.lower()
    
    def test_validate_hotkey_reserved(self, manager):
        """Testa que hotkeys reservados são bloqueados"""
        reserved = [
            "ctrl+c",
            "ctrl+v",
            "ctrl+x",
            "ctrl+shift+q",
            "ctrl+shift+r",
            "ctrl+shift+f"
        ]
        
        for hotkey in reserved:
            valid, msg = manager.validate_hotkey(hotkey)
            assert valid is False
            assert "reservado" in msg.lower()
    
    def test_validate_hotkey_empty(self, manager):
        """Testa validação de hotkey vazio"""
        valid, msg = manager.validate_hotkey("")
        assert valid is False
        assert "vazio" in msg.lower()
    
    def test_validate_hotkey_no_modifier(self, manager):
        """Testa que hotkey sem modificador é inválido"""
        valid, msg = manager.validate_hotkey("a")
        assert valid is False
        assert "modificador" in msg.lower()
    
    def test_validate_hotkey_normalization(self, manager):
        """Testa que hotkey é normalizado para minúscula"""
        valid, msg = manager.validate_hotkey("CTRL+SHIFT+1")
        assert valid is True
    
    def test_validate_hotkey_duplicate(self, manager):
        """Testa detecção de hotkey duplicado"""
        # Simula um shortcut já registrado
        manager.custom_shortcuts_hotkeys[1] = "ctrl+shift+1"
        
        # Tenta validar o mesmo hotkey para outro shortcut
        valid, msg = manager.validate_hotkey("ctrl+shift+1")
        assert valid is False
        assert "em uso" in msg.lower()
    
    def test_validate_hotkey_exclude_self(self, manager):
        """Testa que pode validar hotkey excluindo o próprio ID"""
        # Simula um shortcut já registrado
        manager.custom_shortcuts_hotkeys[1] = "ctrl+shift+1"
        
        # Valida o mesmo hotkey excluindo o próprio ID (para update)
        valid, msg = manager.validate_hotkey("ctrl+shift+1", exclude_shortcut_id=1)
        assert valid is True


class TestCustomShortcutsRegistration:
    """Testes de registro de custom shortcuts"""
    
    @pytest.fixture
    def manager(self):
        """Cria HotkeyManager para testes"""
        return HotkeyManager()
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_register_custom_shortcut_success(self, mock_keyboard, manager):
        """Testa registro bem-sucedido de custom shortcut"""
        success = manager._register_custom_shortcut(1, "ctrl+shift+1")
        
        assert success is True
        assert 1 in manager.custom_shortcuts_hotkeys
        assert manager.custom_shortcuts_hotkeys[1] == "ctrl+shift+1"
        assert 1 in manager.custom_shortcuts_callbacks
        mock_keyboard.add_hotkey.assert_called_once()
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_register_custom_shortcut_failure(self, mock_keyboard, manager):
        """Testa falha ao registrar custom shortcut"""
        # Simula erro no registro
        mock_keyboard.add_hotkey.side_effect = Exception("Erro de teste")
        
        success = manager._register_custom_shortcut(1, "ctrl+shift+1")
        
        assert success is False
        assert 1 not in manager.custom_shortcuts_hotkeys
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_setup_custom_hotkeys_multiple(self, mock_keyboard, manager):
        """Testa registro de múltiplos custom shortcuts"""
        shortcuts = [
            {"id": 1, "hotkey": "ctrl+shift+1", "prefix": "DAHORA", "enabled": True},
            {"id": 2, "hotkey": "alt+f1", "prefix": "URGENTE", "enabled": True},
            {"id": 3, "hotkey": "ctrl+alt+d", "prefix": "REUNIAO", "enabled": True},
        ]
        
        results = manager.setup_custom_hotkeys(shortcuts)
        
        assert len(results) == 3
        assert results[1] == "ok"
        assert results[2] == "ok"
        assert results[3] == "ok"
        assert len(manager.custom_shortcuts_hotkeys) == 3
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_setup_custom_hotkeys_disabled(self, mock_keyboard, manager):
        """Testa que shortcuts desabilitados não são registrados"""
        shortcuts = [
            {"id": 1, "hotkey": "ctrl+shift+1", "prefix": "DAHORA", "enabled": False},
        ]
        
        results = manager.setup_custom_hotkeys(shortcuts)
        
        assert results[1] == "disabled"
        assert 1 not in manager.custom_shortcuts_hotkeys
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_setup_custom_hotkeys_invalid(self, mock_keyboard, manager):
        """Testa que hotkeys inválidos são detectados"""
        shortcuts = [
            {"id": 1, "hotkey": "ctrl+c", "prefix": "TESTE", "enabled": True},  # Reservado
            {"id": 2, "hotkey": "", "prefix": "TESTE2", "enabled": True},  # Vazio
        ]
        
        results = manager.setup_custom_hotkeys(shortcuts)
        
        assert "erro" in results[1]
        assert "erro" in results[2]
        assert len(manager.custom_shortcuts_hotkeys) == 0
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_unregister_custom_shortcut(self, mock_keyboard, manager):
        """Testa remoção de custom shortcut"""
        # Registra primeiro
        manager._register_custom_shortcut(1, "ctrl+shift+1")
        
        # Remove
        success, msg = manager.unregister_custom_shortcut(1)
        
        assert success is True
        assert "sucesso" in msg.lower()
        assert 1 not in manager.custom_shortcuts_hotkeys
        assert 1 not in manager.custom_shortcuts_callbacks
        mock_keyboard.remove_hotkey.assert_called_once_with("ctrl+shift+1")
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_unregister_nonexistent_shortcut(self, mock_keyboard, manager):
        """Testa remoção de shortcut inexistente"""
        success, msg = manager.unregister_custom_shortcut(999)
        
        assert success is False
        assert "não está registrado" in msg.lower()
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_unregister_all_custom_shortcuts(self, mock_keyboard, manager):
        """Testa remoção de todos os custom shortcuts"""
        # Registra múltiplos
        manager._register_custom_shortcut(1, "ctrl+shift+1")
        manager._register_custom_shortcut(2, "alt+f1")
        manager._register_custom_shortcut(3, "ctrl+alt+d")
        
        # Remove todos
        count = manager.unregister_all_custom_shortcuts()
        
        assert count == 3
        assert len(manager.custom_shortcuts_hotkeys) == 0
        assert len(manager.custom_shortcuts_callbacks) == 0


class TestCustomShortcutCallbacks:
    """Testes de callbacks de custom shortcuts"""
    
    @pytest.fixture
    def manager(self):
        """Cria HotkeyManager para testes"""
        return HotkeyManager()
    
    def test_set_custom_shortcut_callback(self, manager):
        """Testa definição de callback para custom shortcut"""
        callback = Mock()
        
        manager.set_custom_shortcut_callback(1, callback)
        
        assert 1 in manager.custom_shortcuts_callbacks
        assert manager.custom_shortcuts_callbacks[1] == callback
    
    def test_on_custom_shortcut_triggered(self, manager):
        """Testa que callback é chamado quando shortcut é acionado"""
        callback = Mock()
        manager.set_custom_shortcut_callback(1, callback)
        
        # Aciona o shortcut
        manager._on_custom_shortcut_triggered(1)
        
        callback.assert_called_once()
    
    def test_on_custom_shortcut_triggered_no_callback(self, manager):
        """Testa que não dá erro se não há callback definido"""
        # Não deveria dar erro
        manager._on_custom_shortcut_triggered(999)


class TestHotkeyRegistrationTest:
    """Testes de teste de registro de hotkey"""
    
    @pytest.fixture
    def manager(self):
        """Cria HotkeyManager para testes"""
        return HotkeyManager()
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_test_register_hotkey_success(self, mock_keyboard, manager):
        """Testa que consegue testar registro de hotkey"""
        can_register, msg = manager.test_register_hotkey("ctrl+shift+1")
        
        assert can_register is True
        assert "disponível" in msg.lower()
        mock_keyboard.add_hotkey.assert_called_once()
        mock_keyboard.remove_hotkey.assert_called_once()
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_test_register_hotkey_conflict(self, mock_keyboard, manager):
        """Testa detecção de conflito ao tentar registrar"""
        # Simula conflito
        mock_keyboard.add_hotkey.side_effect = Exception("already in use")
        
        can_register, msg = manager.test_register_hotkey("ctrl+shift+1")
        
        assert can_register is False
        assert ("em uso" in msg.lower() or "conflito" in msg.lower())


class TestGetRegisteredShortcuts:
    """Testes de listagem de shortcuts registrados"""
    
    @pytest.fixture
    def manager(self):
        """Cria HotkeyManager para testes"""
        return HotkeyManager()
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_get_registered_custom_shortcuts_empty(self, mock_keyboard, manager):
        """Testa listagem quando não há shortcuts"""
        shortcuts = manager.get_registered_custom_shortcuts()
        
        assert shortcuts == []
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_get_registered_custom_shortcuts(self, mock_keyboard, manager):
        """Testa listagem de shortcuts registrados"""
        # Registra alguns
        manager._register_custom_shortcut(1, "ctrl+shift+1")
        manager._register_custom_shortcut(2, "alt+f1")
        
        shortcuts = manager.get_registered_custom_shortcuts()
        
        assert len(shortcuts) == 2
        assert {"id": 1, "hotkey": "ctrl+shift+1"} in shortcuts
        assert {"id": 2, "hotkey": "alt+f1"} in shortcuts


class TestCleanup:
    """Testes de limpeza de recursos"""
    
    @pytest.fixture
    def manager(self):
        """Cria HotkeyManager para testes"""
        return HotkeyManager()
    
    @patch('dahora_app.hotkeys.keyboard')
    def test_cleanup_clears_custom_shortcuts(self, mock_keyboard, manager):
        """Testa que cleanup limpa custom shortcuts"""
        # Registra alguns
        manager._register_custom_shortcut(1, "ctrl+shift+1")
        manager._register_custom_shortcut(2, "alt+f1")
        
        # Cleanup
        manager.cleanup()
        
        assert len(manager.custom_shortcuts_hotkeys) == 0
        assert len(manager.custom_shortcuts_callbacks) == 0
        mock_keyboard.unhook_all.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
