"""
Gerenciamento de hotkeys globais
"""
import logging
import keyboard
from typing import Callable, Optional
from dahora_app.constants import (
    HOTKEY_COPY_DATETIME,
    HOTKEY_REFRESH_MENU,
    HOTKEY_CTRL_C
)


class HotkeyManager:
    """Gerenciador de hotkeys globais"""
    
    def __init__(self):
        """Inicializa o gerenciador de hotkeys"""
        self.registered_hotkeys = []
        self.copy_datetime_callback: Optional[Callable] = None
        self.refresh_menu_callback: Optional[Callable] = None
        self.ctrl_c_callback: Optional[Callable] = None
    
    def set_copy_datetime_callback(self, callback: Callable) -> None:
        """Define callback para copiar data/hora"""
        self.copy_datetime_callback = callback
    
    def set_refresh_menu_callback(self, callback: Callable) -> None:
        """Define callback para refresh do menu"""
        self.refresh_menu_callback = callback
    
    def set_ctrl_c_callback(self, callback: Callable) -> None:
        """Define callback para Ctrl+C"""
        self.ctrl_c_callback = callback
    
    def _on_copy_datetime_triggered(self) -> None:
        """Callback interno para hotkey de copiar data/hora"""
        if self.copy_datetime_callback:
            self.copy_datetime_callback()
    
    def _on_refresh_menu_triggered(self) -> None:
        """Callback interno para hotkey de refresh do menu"""
        try:
            logging.info("[Hotkey] Recarregar Itens acionado (CTRL+SHIFT+R)")
            if self.refresh_menu_callback:
                self.refresh_menu_callback()
        except Exception as e:
            logging.warning(f"[Hotkey] Erro ao atualizar menu: {e}")
    
    def _on_ctrl_c_triggered(self) -> None:
        """Callback interno para Ctrl+C"""
        try:
            if self.ctrl_c_callback:
                self.ctrl_c_callback()
        except Exception as e:
            logging.warning(f"Falha ao processar Ctrl+C: {e}")
    
    def setup_all(self) -> None:
        """Configura todas as hotkeys"""
        # Hotkey principal: Ctrl+Shift+Q
        try:
            keyboard.add_hotkey(HOTKEY_COPY_DATETIME, self._on_copy_datetime_triggered)
            self.registered_hotkeys.append(HOTKEY_COPY_DATETIME)
            print(f"[OK] Tecla de atalho configurada: {HOTKEY_COPY_DATETIME.upper()}")
        except Exception as e:
            print(f"[AVISO] Não foi possível configurar a tecla de atalho: {e}")
        
        # Hotkey de refresh: Ctrl+Shift+R
        try:
            keyboard.add_hotkey(HOTKEY_REFRESH_MENU, self._on_refresh_menu_triggered)
            self.registered_hotkeys.append(HOTKEY_REFRESH_MENU)
            print(f"[OK] Tecla de atalho configurada: {HOTKEY_REFRESH_MENU.upper()} (recarregar itens do menu)")
        except Exception as e:
            print(f"[AVISO] Não foi possível configurar a hotkey de recarga: {e}")
        
        # Listener Ctrl+C
        self.setup_ctrl_c_listener()
    
    def setup_ctrl_c_listener(self) -> None:
        """Configura listener para Ctrl+C globalmente"""
        try:
            keyboard.add_hotkey(HOTKEY_CTRL_C, self._on_ctrl_c_triggered, args=())
            self.registered_hotkeys.append(HOTKEY_CTRL_C)
            logging.info("[OK] Listener Ctrl+C configurado")
        except Exception as e:
            logging.warning(f"[AVISO] Não foi possível configurar listener Ctrl+C: {e}")
    
    def cleanup(self) -> None:
        """Remove todas as hotkeys registradas"""
        try:
            keyboard.unhook_all()
            self.registered_hotkeys.clear()
            logging.info("Hotkeys liberados")
        except Exception as e:
            logging.error(f"Erro ao limpar hotkeys: {e}")
