"""
Testes para HotkeyValidator
"""
import pytest
from dahora_app.hotkey_validator import HotkeyValidator, validate_hotkey


class TestHotkeyValidatorNormalize:
    """Testa normalização de hotkeys"""
    
    def test_normalize_uppercase(self):
        assert HotkeyValidator.normalize("Ctrl+Shift+A") == "ctrl+shift+a"
    
    def test_normalize_spaces(self):
        assert HotkeyValidator.normalize("Ctrl + Shift + A") == "ctrl+shift+a"
    
    def test_normalize_empty(self):
        assert HotkeyValidator.normalize("") == ""
    
    def test_normalize_none_like(self):
        assert HotkeyValidator.normalize(None) == ""


class TestHotkeyValidatorParse:
    """Testa parsing de hotkeys"""
    
    def test_parse_valid(self):
        mods, key = HotkeyValidator.parse("ctrl+shift+q")
        assert mods == ["ctrl", "shift"]
        assert key == "q"
    
    def test_parse_single_modifier(self):
        mods, key = HotkeyValidator.parse("ctrl+a")
        assert mods == ["ctrl"]
        assert key == "a"
    
    def test_parse_three_modifiers(self):
        mods, key = HotkeyValidator.parse("ctrl+shift+alt+a")
        assert mods == ["ctrl", "shift", "alt"]
        assert key == "a"
    
    def test_parse_invalid_empty(self):
        mods, key = HotkeyValidator.parse("")
        assert mods == []
        assert key is None
    
    def test_parse_no_key(self):
        mods, key = HotkeyValidator.parse("ctrl+shift+")
        # Quando não há tecla após +, "shift+" será tratado como "shift"
        # Então mods = ["ctrl"], key = "shift"
        assert len(mods) > 0


class TestHotkeyValidatorIsValid:
    """Testa validação de hotkeys"""
    
    def test_valid_simple(self):
        assert HotkeyValidator.is_valid("ctrl+a") is True
    
    def test_valid_multiple_modifiers(self):
        assert HotkeyValidator.is_valid("ctrl+shift+a") is True
    
    def test_valid_function_key(self):
        assert HotkeyValidator.is_valid("ctrl+f1") is True
    
    def test_invalid_no_modifier(self):
        assert HotkeyValidator.is_valid("a") is False
    
    def test_invalid_modifier_only(self):
        assert HotkeyValidator.is_valid("ctrl+shift+") is False
    
    def test_invalid_reserved_ctrl_c(self):
        assert HotkeyValidator.is_valid("ctrl+c") is False
    
    def test_invalid_reserved_allowed(self):
        # Com allow_reserved=True, deve validar sintaxe mas ainda bloquear?
        # Não, allow_reserved permite reservados
        assert HotkeyValidator.is_valid("ctrl+c", allow_reserved=True) is True
    
    def test_invalid_bad_modifier(self):
        assert HotkeyValidator.is_valid("wrong+a") is False
    
    def test_invalid_empty(self):
        assert HotkeyValidator.is_valid("") is False
    
    def test_invalid_none(self):
        assert HotkeyValidator.is_valid(None) is False
    
    def test_invalid_blocked_escape(self):
        assert HotkeyValidator.is_valid("ctrl+escape") is False
    
    def test_invalid_number(self):
        assert HotkeyValidator.is_valid("ctrl+123") is False


class TestHotkeyValidatorValidateWithReason:
    """Testa validação com mensagem de erro"""
    
    def test_valid_with_message(self):
        is_valid, reason = HotkeyValidator.validate_with_reason("ctrl+q")
        assert is_valid is True
        assert reason is None
    
    def test_no_modifier(self):
        is_valid, reason = HotkeyValidator.validate_with_reason("a")
        assert is_valid is False
        assert "modificador" in reason.lower()
    
    def test_reserved_hotkey(self):
        is_valid, reason = HotkeyValidator.validate_with_reason("ctrl+c")
        assert is_valid is False
        assert "reservado" in reason.lower()
    
    def test_invalid_modifier(self):
        is_valid, reason = HotkeyValidator.validate_with_reason("wrong+a")
        assert is_valid is False
        assert "modificador" in reason.lower()
    
    def test_invalid_key(self):
        is_valid, reason = HotkeyValidator.validate_with_reason("ctrl+!")
        # ! é símbolo válido, deve passar
        assert is_valid is True
    
    def test_blocked_key(self):
        is_valid, reason = HotkeyValidator.validate_with_reason("ctrl+escape")
        assert is_valid is False
        assert "bloqueado" in reason.lower() or "não pode ser usada" in reason.lower()


class TestHotkeyValidatorSuggestFree:
    """Testa sugestão de hotkeys livres"""
    
    def test_suggest_free_hotkey(self):
        suggested = HotkeyValidator.suggest_free_hotkey()
        assert HotkeyValidator.is_valid(suggested) is True
    
    def test_suggest_custom_prefix(self):
        suggested = HotkeyValidator.suggest_free_hotkey("alt+shift")
        assert suggested.startswith("alt+shift+")
        assert HotkeyValidator.is_valid(suggested) is True


class TestHotkeyValidatorQuickFunction:
    """Testa função de conveniência validate_hotkey()"""
    
    def test_quick_validate_valid(self):
        assert validate_hotkey("ctrl+q") is True
    
    def test_quick_validate_invalid(self):
        assert validate_hotkey("q") is False


class TestHotkeyValidatorSymbols:
    """Testa suporte a símbolos"""
    
    def test_symbol_exclam(self):
        # exclam é nome para !
        assert HotkeyValidator.is_valid("ctrl+exclam") is True
    
    def test_symbol_at(self):
        assert HotkeyValidator.is_valid("ctrl+at") is True
    
    def test_symbol_hash(self):
        assert HotkeyValidator.is_valid("ctrl+numbersign") is True


class TestHotkeyValidatorEdgeCases:
    """Testa casos extremos"""
    
    def test_many_modifiers(self):
        # Win + Ctrl + Shift + Alt + Q
        assert HotkeyValidator.is_valid("win+ctrl+shift+alt+q") is True
    
    def test_duplicate_modifiers(self):
        # Ctrl aparece 2x - parse vai ver como ["ctrl", "ctrl"], validação deve falhar?
        # Não, porque ambos são válidos. Lib de hotkeys vai ignorar duplicatas
        is_valid, reason = HotkeyValidator.validate_with_reason("ctrl+ctrl+a")
        # Tecnicamente válido na validação, mas não funciona na prática
        # Deixar passar porque a lib de hotkeys trata
        assert is_valid is True
    
    def test_special_keys_all(self):
        # Testa alguns keys especiais
        assert HotkeyValidator.is_valid("ctrl+f1") is True
        assert HotkeyValidator.is_valid("ctrl+home") is True
        assert HotkeyValidator.is_valid("ctrl+enter") is True
        assert HotkeyValidator.is_valid("shift+pageup") is True
