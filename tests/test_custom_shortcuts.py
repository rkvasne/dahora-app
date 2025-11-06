"""
Testes para Custom Shortcuts (Múltiplas Palavras Personalizadas)
"""
import pytest
import json
import os
import tempfile
from dahora_app.settings import SettingsManager


class TestCustomShortcuts:
    """Testes para funcionalidade de custom shortcuts"""
    
    @pytest.fixture
    def temp_settings_file(self, tmp_path):
        """Cria arquivo temporário de settings"""
        settings_file = tmp_path / "settings.json"
        return str(settings_file)
    
    @pytest.fixture
    def settings_manager(self, temp_settings_file, monkeypatch):
        """Cria SettingsManager com arquivo temporário"""
        monkeypatch.setattr("dahora_app.settings.SETTINGS_FILE", temp_settings_file)
        manager = SettingsManager()
        return manager
    
    def test_add_custom_shortcut_success(self, settings_manager):
        """Testa adicionar custom shortcut com sucesso"""
        success, msg, shortcut_id = settings_manager.add_custom_shortcut(
            hotkey="ctrl+shift+1",
            prefix="DAHORA",
            description="Prefixo padrão",
            enabled=True
        )
        
        assert success is True
        assert "sucesso" in msg.lower()
        assert shortcut_id == 1
        
        # Verifica se foi adicionado
        shortcuts = settings_manager.get_custom_shortcuts()
        assert len(shortcuts) == 1
        assert shortcuts[0]["hotkey"] == "ctrl+shift+1"
        assert shortcuts[0]["prefix"] == "DAHORA"
        assert shortcuts[0]["enabled"] is True
    
    def test_add_multiple_shortcuts(self, settings_manager):
        """Testa adicionar múltiplos shortcuts"""
        # Adiciona 3 shortcuts
        success1, _, id1 = settings_manager.add_custom_shortcut("ctrl+shift+1", "DAHORA")
        success2, _, id2 = settings_manager.add_custom_shortcut("alt+f1", "URGENTE")
        success3, _, id3 = settings_manager.add_custom_shortcut("ctrl+alt+d", "REUNIAO")
        
        assert all([success1, success2, success3])
        assert id1 == 1
        assert id2 == 2
        assert id3 == 3
        
        shortcuts = settings_manager.get_custom_shortcuts()
        assert len(shortcuts) == 3
    
    def test_add_duplicate_hotkey(self, settings_manager):
        """Testa adicionar hotkey duplicado (deve falhar)"""
        # Adiciona primeiro
        success1, _, _ = settings_manager.add_custom_shortcut("ctrl+shift+1", "DAHORA")
        assert success1 is True
        
        # Tenta adicionar duplicado
        success2, msg2, id2 = settings_manager.add_custom_shortcut("ctrl+shift+1", "OUTRO")
        assert success2 is False
        assert "já está em uso" in msg2.lower()
        assert id2 is None
        
        # Verifica que só tem 1
        shortcuts = settings_manager.get_custom_shortcuts()
        assert len(shortcuts) == 1
    
    def test_add_reserved_hotkey(self, settings_manager):
        """Testa adicionar hotkey reservado (deve falhar)"""
        reserved_hotkeys = ["ctrl+shift+q", "ctrl+shift+r", "ctrl+shift+f", "ctrl+c", "ctrl+v"]
        
        for hotkey in reserved_hotkeys:
            success, msg, _ = settings_manager.add_custom_shortcut(hotkey, "TESTE")
            assert success is False
            assert "reservado" in msg.lower()
    
    def test_add_max_shortcuts_limit(self, settings_manager):
        """Testa limite máximo de shortcuts"""
        # Adiciona até o limite (10)
        for i in range(10):
            success, _, _ = settings_manager.add_custom_shortcut(f"ctrl+shift+{i}", f"PREFIX{i}")
            assert success is True
        
        # Tenta adicionar mais um (deve falhar)
        success, msg, _ = settings_manager.add_custom_shortcut("ctrl+shift+x", "EXTRA")
        assert success is False
        assert "limite" in msg.lower()
    
    def test_remove_custom_shortcut(self, settings_manager):
        """Testa remover custom shortcut"""
        # Adiciona
        success, _, shortcut_id = settings_manager.add_custom_shortcut("ctrl+shift+1", "DAHORA")
        assert success is True
        
        # Remove
        success_remove, msg_remove = settings_manager.remove_custom_shortcut(shortcut_id)
        assert success_remove is True
        assert "removido" in msg_remove.lower()
        
        # Verifica que foi removido
        shortcuts = settings_manager.get_custom_shortcuts()
        assert len(shortcuts) == 0
    
    def test_remove_nonexistent_shortcut(self, settings_manager):
        """Testa remover shortcut inexistente"""
        success, msg = settings_manager.remove_custom_shortcut(999)
        assert success is False
        assert "não encontrado" in msg.lower()
    
    def test_update_custom_shortcut(self, settings_manager):
        """Testa atualizar custom shortcut"""
        # Adiciona
        success, _, shortcut_id = settings_manager.add_custom_shortcut("ctrl+shift+1", "DAHORA", "Desc")
        assert success is True
        
        # Atualiza
        success_update, msg_update = settings_manager.update_custom_shortcut(
            shortcut_id,
            hotkey="alt+f1",
            prefix="NOVO",
            description="Nova descrição",
            enabled=False
        )
        assert success_update is True
        assert "atualizado" in msg_update.lower()
        
        # Verifica atualização
        shortcut = settings_manager.get_custom_shortcut_by_id(shortcut_id)
        assert shortcut["hotkey"] == "alt+f1"
        assert shortcut["prefix"] == "NOVO"
        assert shortcut["description"] == "Nova descrição"
        assert shortcut["enabled"] is False
    
    def test_update_hotkey_to_duplicate(self, settings_manager):
        """Testa atualizar hotkey para um já existente (deve falhar)"""
        # Adiciona dois shortcuts
        _, _, id1 = settings_manager.add_custom_shortcut("ctrl+shift+1", "DAHORA")
        _, _, id2 = settings_manager.add_custom_shortcut("ctrl+shift+2", "URGENTE")
        
        # Tenta atualizar segundo para hotkey do primeiro
        success, msg = settings_manager.update_custom_shortcut(id2, hotkey="ctrl+shift+1")
        assert success is False
        assert "já está em uso" in msg.lower()
    
    def test_get_custom_shortcuts_enabled_only(self, settings_manager):
        """Testa filtrar shortcuts habilitados"""
        # Adiciona 3 shortcuts, 2 habilitados e 1 desabilitado
        settings_manager.add_custom_shortcut("ctrl+shift+1", "DAHORA", enabled=True)
        settings_manager.add_custom_shortcut("ctrl+shift+2", "URGENTE", enabled=False)
        settings_manager.add_custom_shortcut("ctrl+shift+3", "REUNIAO", enabled=True)
        
        # Todos
        all_shortcuts = settings_manager.get_custom_shortcuts(enabled_only=False)
        assert len(all_shortcuts) == 3
        
        # Apenas habilitados
        enabled_shortcuts = settings_manager.get_custom_shortcuts(enabled_only=True)
        assert len(enabled_shortcuts) == 2
        assert all(s["enabled"] for s in enabled_shortcuts)
    
    def test_get_custom_shortcut_by_hotkey(self, settings_manager):
        """Testa buscar shortcut por hotkey"""
        settings_manager.add_custom_shortcut("ctrl+shift+1", "DAHORA")
        settings_manager.add_custom_shortcut("alt+f1", "URGENTE")
        
        # Busca existente
        shortcut = settings_manager.get_custom_shortcut_by_hotkey("alt+f1")
        assert shortcut is not None
        assert shortcut["prefix"] == "URGENTE"
        
        # Busca inexistente
        shortcut_none = settings_manager.get_custom_shortcut_by_hotkey("ctrl+alt+z")
        assert shortcut_none is None
    
    def test_prefix_validation(self, settings_manager):
        """Testa validação de prefixo"""
        # Prefixo muito longo (deve truncar)
        long_prefix = "A" * 100
        success, _, _ = settings_manager.add_custom_shortcut("ctrl+shift+1", long_prefix)
        assert success is True
        
        shortcut = settings_manager.get_custom_shortcuts()[0]
        assert len(shortcut["prefix"]) == 50  # Truncado para 50
    
    def test_hotkey_normalization(self, settings_manager):
        """Testa normalização de hotkey (lowercase)"""
        success, _, _ = settings_manager.add_custom_shortcut("CTRL+SHIFT+1", "DAHORA")
        assert success is True
        
        shortcut = settings_manager.get_custom_shortcuts()[0]
        assert shortcut["hotkey"] == "ctrl+shift+1"  # Normalizado para minúscula
    
    def test_persistence(self, settings_manager, temp_settings_file):
        """Testa persistência dos custom shortcuts"""
        # Adiciona shortcuts
        settings_manager.add_custom_shortcut("ctrl+shift+1", "DAHORA")
        settings_manager.add_custom_shortcut("alt+f1", "URGENTE")
        
        # Cria novo manager (simula restart)
        new_manager = SettingsManager()
        new_manager.load()
        
        # Verifica que foram carregados
        shortcuts = new_manager.get_custom_shortcuts()
        assert len(shortcuts) == 2
    
    def test_validate_custom_shortcuts_removes_invalid(self, settings_manager):
        """Testa que validação remove shortcuts inválidos"""
        invalid_shortcuts = [
            {"id": 1, "hotkey": "", "prefix": "DAHORA"},  # hotkey vazio
            {"id": 2, "hotkey": "ctrl+shift+1", "prefix": ""},  # prefix vazio
            {"id": 3, "hotkey": "ctrl+shift+2", "prefix": "VALID"},  # válido
        ]
        
        validated = settings_manager._validate_custom_shortcuts(invalid_shortcuts)
        assert len(validated) == 1  # Apenas o válido
        assert validated[0]["prefix"] == "VALID"


class TestLegacyPrefixMigration:
    """Testes para migração de prefixo legado"""
    
    @pytest.fixture
    def temp_settings_file(self, tmp_path):
        """Cria arquivo temporário de settings"""
        settings_file = tmp_path / "settings.json"
        return str(settings_file)
    
    @pytest.fixture
    def settings_manager(self, temp_settings_file, monkeypatch):
        """Cria SettingsManager com arquivo temporário"""
        monkeypatch.setattr("dahora_app.settings.SETTINGS_FILE", temp_settings_file)
        manager = SettingsManager()
        return manager
    
    def test_migrate_legacy_prefix(self, settings_manager, temp_settings_file):
        """Testa migração automática de prefixo legado"""
        # Cria arquivo com formato antigo
        legacy_settings = {
            "prefix": "DAHORA",
            "hotkey_copy_datetime": "ctrl+shift+q",
            "max_history_items": 100,
        }
        
        with open(temp_settings_file, "w", encoding="utf-8") as f:
            json.dump(legacy_settings, f)
        
        # Carrega (deve migrar automaticamente)
        settings_manager.load()
        
        # Verifica que foi criado custom shortcut
        shortcuts = settings_manager.get_custom_shortcuts()
        assert len(shortcuts) == 1
        assert shortcuts[0]["prefix"] == "DAHORA"
        assert shortcuts[0]["hotkey"] == "ctrl+shift+1"
        assert "migrado" in shortcuts[0]["description"].lower()
    
    def test_no_migration_if_custom_shortcuts_exist(self, settings_manager, temp_settings_file):
        """Testa que não migra se já existem custom shortcuts"""
        # Cria arquivo com custom shortcuts já configurados
        settings_with_shortcuts = {
            "prefix": "OLD",
            "custom_shortcuts": [
                {"id": 1, "hotkey": "ctrl+shift+1", "prefix": "EXISTING", "enabled": True, "description": ""}
            ]
        }
        
        with open(temp_settings_file, "w", encoding="utf-8") as f:
            json.dump(settings_with_shortcuts, f)
        
        # Carrega
        settings_manager.load()
        
        # Verifica que manteve os existentes (não migrou)
        shortcuts = settings_manager.get_custom_shortcuts()
        assert len(shortcuts) == 1
        assert shortcuts[0]["prefix"] == "EXISTING"  # Não mudou para "OLD"
    
    def test_no_migration_if_no_legacy_prefix(self, settings_manager, temp_settings_file):
        """Testa que não migra se não há prefixo legado"""
        # Cria arquivo sem prefixo
        settings_no_prefix = {
            "hotkey_copy_datetime": "ctrl+shift+q",
            "max_history_items": 100,
        }
        
        with open(temp_settings_file, "w", encoding="utf-8") as f:
            json.dump(settings_no_prefix, f)
        
        # Carrega
        settings_manager.load()
        
        # Verifica que não criou nenhum shortcut
        shortcuts = settings_manager.get_custom_shortcuts()
        assert len(shortcuts) == 0


class TestBackwardCompatibility:
    """Testes de retrocompatibilidade"""
    
    @pytest.fixture
    def temp_settings_file(self, tmp_path):
        """Cria arquivo temporário de settings"""
        settings_file = tmp_path / "settings.json"
        return str(settings_file)
    
    @pytest.fixture
    def settings_manager(self, temp_settings_file, monkeypatch):
        """Cria SettingsManager com arquivo temporário"""
        monkeypatch.setattr("dahora_app.settings.SETTINGS_FILE", temp_settings_file)
        manager = SettingsManager()
        return manager
    
    def test_get_prefix_still_works(self, settings_manager):
        """Testa que get_prefix() legado ainda funciona"""
        settings_manager.date_prefix = "DAHORA"
        assert settings_manager.get_prefix() == "DAHORA"
    
    def test_set_prefix_still_works(self, settings_manager):
        """Testa que set_prefix() legado ainda funciona"""
        settings_manager.set_prefix("NOVO")
        assert settings_manager.get_prefix() == "NOVO"
    
    def test_get_all_includes_custom_shortcuts(self, settings_manager):
        """Testa que get_all() inclui custom_shortcuts"""
        settings_manager.add_custom_shortcut("ctrl+shift+1", "DAHORA")
        
        all_settings = settings_manager.get_all()
        assert "custom_shortcuts" in all_settings
        assert len(all_settings["custom_shortcuts"]) == 1
    
    def test_update_all_with_custom_shortcuts(self, settings_manager):
        """Testa que update_all() aceita custom_shortcuts"""
        new_settings = {
            "prefix": "NOVO",
            "custom_shortcuts": [
                {"id": 1, "hotkey": "ctrl+shift+1", "prefix": "DAHORA", "enabled": True, "description": "Teste"}
            ]
        }
        
        settings_manager.update_all(new_settings)
        
        shortcuts = settings_manager.get_custom_shortcuts()
        assert len(shortcuts) == 1
        assert shortcuts[0]["prefix"] == "DAHORA"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
