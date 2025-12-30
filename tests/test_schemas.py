"""
Testes para schemas de validação Pydantic
"""
import pytest
from pydantic import ValidationError
from dahora_app.schemas import (
    CustomShortcutSchema,
    SettingsSchema,
    NotificationSchema,
    AppConfigSchema
)


class TestCustomShortcutSchema:
    """Testa schema de atalho personalizado"""
    
    def test_valid_shortcut(self):
        shortcut = CustomShortcutSchema(
            id=1,
            hotkey="ctrl+shift+q",
            prefix="test"
        )
        assert shortcut.id == 1
        assert shortcut.hotkey == "ctrl+shift+q"
        assert shortcut.prefix == "test"
        assert shortcut.enabled is True
    
    def test_hotkey_required(self):
        with pytest.raises(ValidationError) as exc_info:
            CustomShortcutSchema(id=1, prefix="test")
        assert "hotkey" in str(exc_info.value).lower()
    
    def test_hotkey_must_have_plus(self):
        with pytest.raises(ValidationError):
            CustomShortcutSchema(id=1, hotkey="ab", prefix="test")
        # Note: "q" é muito curto (min_length=3), vai falhar por tamanho antes da validação do '+'
    
    def test_hotkey_normalized_to_lowercase(self):
        shortcut = CustomShortcutSchema(
            id=1,
            hotkey="Ctrl+Shift+Q",
            prefix="test"
        )
        assert shortcut.hotkey == "ctrl+shift+q"
    
    def test_prefix_sanitized(self):
        # Prefixo com espaços deve ser trimmed
        shortcut = CustomShortcutSchema(
            id=1,
            hotkey="ctrl+q",
            prefix="  test  "
        )
        assert shortcut.prefix == "test"
    
    def test_prefix_required(self):
        with pytest.raises(ValidationError):
            CustomShortcutSchema(id=1, hotkey="ctrl+q", prefix="")
    
    def test_disabled_shortcut(self):
        shortcut = CustomShortcutSchema(
            id=1,
            hotkey="ctrl+q",
            prefix="test",
            enabled=False
        )
        assert shortcut.enabled is False
    
    def test_extra_fields_rejected(self):
        with pytest.raises(ValidationError):
            CustomShortcutSchema(
                id=1,
                hotkey="ctrl+q",
                prefix="test",
                extra_field="should_fail"
            )


class TestSettingsSchema:
    """Testa schema de configurações"""
    
    def test_valid_settings(self):
        settings = SettingsSchema()
        assert settings.prefix == ""
        assert settings.max_history_items == 100
        assert settings.bracket_open == "["
        assert settings.bracket_close == "]"
    
    def test_max_history_bounds(self):
        # Mínimo 10
        with pytest.raises(ValidationError):
            SettingsSchema(max_history_items=5)
        
        # Máximo 1000
        with pytest.raises(ValidationError):
            SettingsSchema(max_history_items=2000)
    
    def test_bracket_must_be_different(self):
        with pytest.raises(ValidationError) as exc_info:
            SettingsSchema(bracket_open="[", bracket_close="[")
        assert "diferentes" in str(exc_info.value).lower()
    
    def test_bracket_must_be_single_char(self):
        with pytest.raises(ValidationError):
            SettingsSchema(bracket_open="[[")
    
    def test_custom_shortcuts_limit(self):
        shortcuts = [
            CustomShortcutSchema(id=i+1, hotkey=f"ctrl+shift+{chr(97+i)}", prefix=f"p{i}")
            for i in range(15)
        ]
        with pytest.raises(ValidationError):
            SettingsSchema(custom_shortcuts=shortcuts)
    
    def test_hotkey_duplicates_detected(self):
        settings_dict = {
            "hotkey_copy_datetime": "ctrl+shift+q",
            "hotkey_search_history": "ctrl+shift+q",  # Duplicado!
            "hotkey_refresh_menu": "ctrl+shift+r"
        }
        with pytest.raises(ValidationError) as exc_info:
            SettingsSchema(**settings_dict)
        assert "duplicado" in str(exc_info.value).lower()
    
    def test_default_shortcut_id_must_exist(self):
        shortcuts = [
            CustomShortcutSchema(id=1, hotkey="ctrl+a", prefix="p1")
        ]
        with pytest.raises(ValidationError) as exc_info:
            SettingsSchema(
                custom_shortcuts=shortcuts,
                default_shortcut_id=999  # Não existe
            )
        assert "não existe" in str(exc_info.value).lower()
    
    def test_custom_shortcut_ids_must_be_unique(self):
        shortcuts = [
            CustomShortcutSchema(id=1, hotkey="ctrl+a", prefix="p1"),
            CustomShortcutSchema(id=1, hotkey="ctrl+b", prefix="p2"),  # Duplicado!
        ]
        with pytest.raises(ValidationError) as exc_info:
            SettingsSchema(custom_shortcuts=shortcuts)
        assert "único" in str(exc_info.value).lower()
    
    def test_prefix_sanitizes_control_chars(self):
        # Caracteres de controle devem ser removidos
        settings = SettingsSchema(prefix="test\x00\x01bad")
        assert settings.prefix == "testbad"
    
    def test_prefix_truncated(self):
        # Prefixos muito longos devem ser rejeitados pelo Pydantic
        long_prefix = "a" * 200
        with pytest.raises(ValidationError):
            SettingsSchema(prefix=long_prefix)
    
    def test_datetime_format_must_have_components(self):
        with pytest.raises(ValidationError):
            SettingsSchema(datetime_format="invalid_format_xyz")
    
    def test_clipboard_monitor_interval_bounds(self):
        with pytest.raises(ValidationError):
            SettingsSchema(clipboard_monitor_interval=0.1)  # < 0.5
        
        with pytest.raises(ValidationError):
            SettingsSchema(clipboard_monitor_interval=100)  # > 60
    
    def test_extra_fields_rejected(self):
        with pytest.raises(ValidationError):
            SettingsSchema(unknown_field="should_fail")


class TestNotificationSchema:
    """Testa schema de notificações"""
    
    def test_valid_notification(self):
        notif = NotificationSchema()
        assert notif.enabled is True
        assert notif.duration_seconds == 2
        assert notif.show_on_error is True
    
    def test_duration_bounds(self):
        with pytest.raises(ValidationError):
            NotificationSchema(duration_seconds=0)
        
        with pytest.raises(ValidationError):
            NotificationSchema(duration_seconds=20)


class TestAppConfigSchema:
    """Testa schema de configuração completa do app"""
    
    def test_valid_app_config(self):
        config = AppConfigSchema(
            settings=SettingsSchema()
        )
        assert config.settings is not None
        assert config.notifications is not None
    
    def test_app_config_with_custom_settings(self):
        settings = SettingsSchema(
            prefix="myapp",
            max_history_items=500
        )
        config = AppConfigSchema(settings=settings)
        assert config.settings.prefix == "myapp"
        assert config.settings.max_history_items == 500
    
    def test_app_config_inherits_validation(self):
        with pytest.raises(ValidationError):
            AppConfigSchema(
                settings=SettingsSchema(bracket_open="[", bracket_close="[")
            )


class TestSchemaIntegration:
    """Testa integração entre schemas"""
    
    def test_full_workflow(self):
        """Teste de workflow completo de configuração"""
        # Cria settings com shortcuts
        settings = SettingsSchema(
            prefix="default",
            custom_shortcuts=[
                CustomShortcutSchema(
                    id=1,
                    hotkey="ctrl+shift+a",
                    prefix="log"
                ),
                CustomShortcutSchema(
                    id=2,
                    hotkey="ctrl+shift+b",
                    prefix="todo",
                    enabled=False
                ),
            ],
            default_shortcut_id=1
        )
        
        assert len(settings.custom_shortcuts) == 2
        assert settings.default_shortcut_id == 1
        assert settings.custom_shortcuts[0].enabled is True
        assert settings.custom_shortcuts[1].enabled is False
    
    def test_settings_to_dict(self):
        """Testa serialização para dict"""
        settings = SettingsSchema(prefix="test")
        data = settings.model_dump()
        
        assert isinstance(data, dict)
        assert data["prefix"] == "test"
        assert "datetime_format" in data
    
    def test_dict_to_settings(self):
        """Testa desserialização de dict"""
        data = {
            "prefix": "test",
            "max_history_items": 200,
            "bracket_open": "<",
            "bracket_close": ">",
        }
        settings = SettingsSchema(**data)
        assert settings.prefix == "test"
        assert settings.max_history_items == 200
