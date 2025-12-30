"""
Validação rigorosa de hotkeys
Módulo seguro para validar combinações de teclas globais
"""
import re
import logging
from typing import Tuple, List, Optional


class HotkeyValidator:
    """Validador de hotkeys globais com regras de segurança"""
    
    # Modificadores válidos (ordem importa: Ctrl, Shift, Alt, Win)
    VALID_MODIFIERS = {"ctrl", "shift", "alt", "win"}
    
    # Teclas especiais válidas
    VALID_SPECIAL_KEYS = {
        # Função
        "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
        # Navegação
        "home", "end", "pageup", "pagedown", "insert", "delete",
        # Setas
        "up", "down", "left", "right",
        # Sistema
        "enter", "tab", "space", "backspace", "escape",
        # Mais
        "printscreen", "pause", "numlock", "capslock", "scrolllock",
    }
    
    # Hotkeys reservados do app (não podem ser customizados)
    # Nota: Ctrl+C/V/X são para clipboard, Ctrl+A/Z são para edição geral
    # Por segurança, bloqueamos apenas os mais críticos: Ctrl+C (interrupção de processos)
    RESERVED_HOTKEYS = {
        "ctrl+c",  # Ctrl+C é crítico - interrompe processos, não pode ser customizado
    }
    
    # Teclas bloqueadas (nunca podem ser usadas sozinhas ou com apenas 1 modifier)
    BLOCKED_KEYS = {
        "escape",  # Sair de tudo
        "pause",   # Pause do sistema
    }
    
    @staticmethod
    def normalize(hotkey: str) -> str:
        """
        Normaliza um hotkey para format padrão lowercase.
        
        Args:
            hotkey: Hotkey a normalizar (ex: "Ctrl+Shift+A" ou "ctrl+shift+a")
            
        Returns:
            Hotkey normalizado em lowercase (ex: "ctrl+shift+a")
        """
        if not hotkey:
            return ""
        
        # Remove espaços
        hotkey = hotkey.replace(" ", "")
        
        # Converte para lowercase
        return hotkey.lower()
    
    @staticmethod
    def parse(hotkey: str) -> Tuple[List[str], Optional[str]]:
        """
        Faz parse de um hotkey em (modifiers, key).
        
        Args:
            hotkey: Hotkey a fazer parse (ex: "ctrl+shift+q")
            
        Returns:
            Tupla (modifiers_list, final_key) ou ([], None) se inválido
            
        Exemplo:
            >>> parse("ctrl+shift+q")
            (["ctrl", "shift"], "q")
            
            >>> parse("invalid")
            ([], None)
        """
        if not hotkey or not isinstance(hotkey, str):
            return [], None
        
        # Normaliza
        normalized = HotkeyValidator.normalize(hotkey)
        
        # Faz split
        parts = [p.strip() for p in normalized.split("+") if p.strip()]
        
        if not parts:
            return [], None
        
        # Último part é a tecla
        key = parts[-1]
        modifiers = parts[:-1]
        
        return modifiers, key
    
    @classmethod
    def is_valid(cls, hotkey: str, allow_reserved: bool = False) -> bool:
        """
        Valida se um hotkey é válido e seguro.
        
        Args:
            hotkey: Hotkey a validar
            allow_reserved: Se True, permite hotkeys reservados do app (apenas para dev)
            
        Returns:
            True se válido, False caso contrário
        """
        if not hotkey or not isinstance(hotkey, str):
            return False
        
        normalized = cls.normalize(hotkey)
        
        # Verifica hotkeys reservados
        if not allow_reserved and normalized in cls.RESERVED_HOTKEYS:
            return False
        
        modifiers, key = cls.parse(normalized)
        
        # Precisa de pelo menos 1 modifier
        if not modifiers or not key:
            return False
        
        # Valida modifiers
        for mod in modifiers:
            if mod not in cls.VALID_MODIFIERS:
                return False
        
        # Valida key
        if not cls._is_valid_key(key):
            return False
        
        # Verifica teclas bloqueadas
        if key in cls.BLOCKED_KEYS:
            return False
        
        return True
    
    @classmethod
    def _is_valid_key(cls, key: str) -> bool:
        """Verifica se uma tecla é válida"""
        if not key or not isinstance(key, str):
            return False
        
        key_lower = key.lower()
        
        # Tecla especial
        if key_lower in cls.VALID_SPECIAL_KEYS:
            return True
        
        # Letra única
        if len(key_lower) == 1 and key_lower.isalpha():
            return True
        
        # Número único
        if len(key) == 1 and key.isdigit():
            return True
        
        # Símbolos comuns em hotkeys
        if key in {"!", "@", "#", "$", "%", "^", "&", "*", "(", ")"}:
            return True
        
        # Nomes de símbolos
        symbol_names = {
            "exclam", "at", "numbersign", "number_sign", "hash", "dollar",
            "percent", "asciicircum", "caret", "ampersand", "asterisk",
            "parenleft", "parenright", "minus", "underscore", "equal", "plus",
            "comma", "period", "dot", "slash", "backslash", "question",
            "quotedbl", "apostrophe", "grave", "tilde", "bracketleft",
            "bracketright", "braceleft", "braceright", "semicolon", "colon",
            "less", "greater", "bar",
        }
        if key in symbol_names:
            return True
        
        return False
    
    @classmethod
    def validate_with_reason(cls, hotkey: str, allow_reserved: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Valida um hotkey e retorna razão da falha (se houver).
        
        Args:
            hotkey: Hotkey a validar
            allow_reserved: Se True, permite hotkeys reservados
            
        Returns:
            Tupla (is_valid, reason_if_invalid)
            
        Exemplo:
            >>> validate_with_reason("ctrl+q")
            (True, None)
            
            >>> validate_with_reason("q")
            (False, "Requer pelo menos 1 modificador (Ctrl/Shift/Alt/Win)")
            
            >>> validate_with_reason("ctrl+c")
            (False, "Ctrl+C é reservado para funções do sistema")
        """
        if not hotkey or not isinstance(hotkey, str):
            return False, "Hotkey vazio ou inválido"
        
        normalized = cls.normalize(hotkey)
        
        # Verifica hotkeys reservados
        if not allow_reserved and normalized in cls.RESERVED_HOTKEYS:
            return False, f"{normalized.upper()} é reservado para funções do sistema"
        
        modifiers, key = cls.parse(normalized)
        
        # Verifica modifiers
        if not modifiers:
            return False, "Requer pelo menos 1 modificador (Ctrl/Shift/Alt/Win)"
        
        if not key:
            return False, "Tecla final não especificada"
        
        # Valida modifiers
        for mod in modifiers:
            if mod not in cls.VALID_MODIFIERS:
                return False, f"Modificador inválido: '{mod}' (use Ctrl, Shift, Alt ou Win)"
        
        # Valida key
        if not cls._is_valid_key(key):
            return False, f"Tecla inválida: '{key}' (use letra, número ou função)"
        
        # Verifica teclas bloqueadas
        if key in cls.BLOCKED_KEYS:
            return False, f"Tecla '{key}' não pode ser usada em hotkeys globais"
        
        return True, None
    
    @classmethod
    def suggest_free_hotkey(cls, base_prefix: str = "ctrl+shift") -> str:
        """
        Sugere um hotkey livre baseado em um prefixo.
        
        Args:
            base_prefix: Prefixo para sugestão (ex: "ctrl+shift")
            
        Returns:
            Hotkey sugerido (ex: "ctrl+shift+j")
        """
        # Letras em ordem de "frequência de uso baixa"
        candidates = "jkxzq"  # letras menos usadas
        
        for letter in candidates:
            suggested = f"{base_prefix}+{letter}"
            if cls.is_valid(suggested):
                return suggested
        
        # Fallback: numeros
        for num in "123456789":
            suggested = f"{base_prefix}+{num}"
            if cls.is_valid(suggested):
                return suggested
        
        return ""  # Nenhum encontrado (improvável)


# Função de conveniência para uso rápido
def validate_hotkey(hotkey: str, allow_reserved: bool = False) -> bool:
    """Função rápida para validar um hotkey"""
    return HotkeyValidator.is_valid(hotkey, allow_reserved)
