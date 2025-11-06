"""
Gerenciamento de hotkeys globais
"""
import logging
import keyboard
from typing import Callable, Optional, Dict, Any, List, Tuple
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
        self.search_callback: Optional[Callable] = None
        self.ctrl_c_callback: Optional[Callable] = None
        
        # Custom shortcuts (NOVO)
        self.custom_shortcuts_callbacks: Dict[int, Callable] = {}  # shortcut_id -> callback
        self.custom_shortcuts_hotkeys: Dict[int, str] = {}  # shortcut_id -> hotkey
        # Apenas atalhos de clipboard que NÃO devem ser sobrescritos
        self.reserved_hotkeys = [
            "ctrl+c", "ctrl+v", "ctrl+x", "ctrl+a", "ctrl+z"
        ]
    
    def set_copy_datetime_callback(self, callback: Callable) -> None:
        """Define callback para copiar data/hora"""
        self.copy_datetime_callback = callback
    
    def set_refresh_menu_callback(self, callback: Callable) -> None:
        """Define callback para refresh do menu"""
        self.refresh_menu_callback = callback
    
    def set_search_callback(self, callback: Callable) -> None:
        """Define callback para busca no histórico"""
        self.search_callback = callback
    
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
    
    def _on_search_triggered(self) -> None:
        """Callback interno para hotkey de busca"""
        try:
            logging.info("[Hotkey] Buscar no Histórico acionado (CTRL+SHIFT+F)")
            if self.search_callback:
                self.search_callback()
        except Exception as e:
            logging.warning(f"[Hotkey] Erro ao abrir busca: {e}")
    
    def _on_ctrl_c_triggered(self, event=None) -> None:
        """Callback interno para Ctrl+C"""
        try:
            if self.ctrl_c_callback:
                self.ctrl_c_callback()
        except Exception as e:
            logging.warning(f"Falha ao processar Ctrl+C: {e}")
    
    def setup_all(self) -> None:
        """Configura hotkeys do sistema (TODOS agora são opcionais/configuráveis)"""
        # REMOVIDO: Todos os atalhos fixos
        # Agora TUDO é configurado pelo usuário via custom shortcuts
        # Incluindo refresh (Ctrl+Shift+R) e busca (Ctrl+Shift+F)
        
        # Listener para Ctrl+C (único que permanece automático para monitorar clipboard)
        try:
            keyboard.on_press_key('c', self._on_ctrl_c_triggered)
            logging.info("[OK] Listener Ctrl+C configurado")
        except Exception as e:
            logging.warning(f"Não foi possível configurar o Ctrl+C: {e}")
    
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
            self.custom_shortcuts_callbacks.clear()
            self.custom_shortcuts_hotkeys.clear()
            logging.info("Hotkeys liberados")
        except Exception as e:
            logging.error(f"Erro ao limpar hotkeys: {e}")
    
    # ========== MÉTODOS PARA CUSTOM SHORTCUTS (NOVO) ==========
    
    def validate_hotkey(self, hotkey: str, exclude_shortcut_id: Optional[int] = None) -> Tuple[bool, str]:
        """Valida se hotkey pode ser usado
        
        Args:
            hotkey: String do hotkey (ex: 'ctrl+shift+1')
            exclude_shortcut_id: ID de shortcut a excluir da verificação (para updates)
            
        Returns:
            Tuple[bool, str]: (válido, mensagem)
        """
        try:
            hotkey = hotkey.strip().lower()
            
            if not hotkey:
                return False, "Hotkey não pode ser vazio"
            
            # Verifica se é hotkey reservado
            if hotkey in self.reserved_hotkeys:
                return False, f"Hotkey '{hotkey}' é reservado pelo sistema"
            
            # Verifica se já está em uso por outro custom shortcut
            for shortcut_id, used_hotkey in self.custom_shortcuts_hotkeys.items():
                if shortcut_id != exclude_shortcut_id and used_hotkey == hotkey:
                    return False, f"Hotkey '{hotkey}' já está em uso por outro atalho"
            
            # Validação básica de formato (deve ter pelo menos um modificador)
            if '+' not in hotkey:
                return False, "Hotkey deve ter pelo menos um modificador (ctrl, alt, shift)"
            
            return True, "Hotkey válido"
        
        except Exception as e:
            logging.error(f"Erro ao validar hotkey: {e}")
            return False, f"Erro na validação: {str(e)}"
    
    def test_register_hotkey(self, hotkey: str) -> Tuple[bool, str]:
        """Testa se consegue registrar o hotkey
        
        Args:
            hotkey: String do hotkey para testar
            
        Returns:
            Tuple[bool, str]: (conseguiu registrar, mensagem)
        """
        try:
            hotkey = hotkey.strip().lower()
            
            # Tenta registrar temporariamente
            def dummy_callback():
                pass
            
            keyboard.add_hotkey(hotkey, dummy_callback)
            
            # Se conseguiu, remove imediatamente
            keyboard.remove_hotkey(hotkey)
            
            return True, "Hotkey disponível"
        
        except Exception as e:
            error_msg = str(e)
            if "already" in error_msg.lower() or "conflict" in error_msg.lower():
                return False, f"Hotkey '{hotkey}' pode estar em uso por outro aplicativo"
            return False, f"Não foi possível registrar: {error_msg}"
    
    def setup_custom_hotkeys(self, custom_shortcuts: List[Dict[str, Any]]) -> Dict[int, str]:
        """Registra múltiplos custom shortcuts
        
        Args:
            custom_shortcuts: Lista de dicts com 'id', 'hotkey', 'prefix', 'enabled'
            
        Returns:
            Dict[int, str]: Mapeamento de shortcut_id -> status ("ok", "erro: ...")
        """
        results = {}
        
        for shortcut in custom_shortcuts:
            try:
                shortcut_id = shortcut.get("id")
                hotkey = shortcut.get("hotkey", "").strip().lower()
                enabled = shortcut.get("enabled", True)
                
                if not enabled:
                    results[shortcut_id] = "disabled"
                    continue
                
                if not hotkey:
                    results[shortcut_id] = "erro: hotkey vazio"
                    continue
                
                # Valida hotkey
                valid, msg = self.validate_hotkey(hotkey)
                if not valid:
                    results[shortcut_id] = f"erro: {msg}"
                    logging.warning(f"Shortcut ID={shortcut_id} inválido: {msg}")
                    continue
                
                # Registra hotkey com callback específico
                success = self._register_custom_shortcut(shortcut_id, hotkey)
                
                if success:
                    results[shortcut_id] = "ok"
                    logging.info(f"Custom shortcut registrado: ID={shortcut_id}, hotkey={hotkey}")
                else:
                    results[shortcut_id] = "erro: falha ao registrar"
            
            except Exception as e:
                results[shortcut_id] = f"erro: {str(e)}"
                logging.error(f"Erro ao configurar shortcut ID={shortcut_id}: {e}")
        
        return results
    
    def _register_custom_shortcut(self, shortcut_id: int, hotkey: str) -> bool:
        """Registra um custom shortcut específico
        
        Args:
            shortcut_id: ID do shortcut
            hotkey: String do hotkey
            
        Returns:
            bool: True se registrou com sucesso
        """
        try:
            # Cria callback com closure para passar o shortcut_id
            def callback():
                self._on_custom_shortcut_triggered(shortcut_id)
            
            # Registra hotkey
            keyboard.add_hotkey(hotkey, callback)
            
            # Armazena mapeamentos
            self.custom_shortcuts_callbacks[shortcut_id] = callback
            self.custom_shortcuts_hotkeys[shortcut_id] = hotkey
            self.registered_hotkeys.append(hotkey)
            
            return True
        
        except Exception as e:
            logging.error(f"Falha ao registrar custom shortcut ID={shortcut_id}: {e}")
            return False
    
    def _on_custom_shortcut_triggered(self, shortcut_id: int) -> None:
        """Callback quando custom shortcut é acionado
        
        Args:
            shortcut_id: ID do shortcut que foi acionado
        """
        try:
            logging.info(f"[Hotkey] Custom shortcut acionado: ID={shortcut_id}")
            
            # Chama callback registrado (será definido pela aplicação)
            callback = self.custom_shortcuts_callbacks.get(shortcut_id)
            if callback:
                callback()
        
        except Exception as e:
            logging.error(f"Erro ao processar custom shortcut ID={shortcut_id}: {e}")
    
    def set_custom_shortcut_callback(self, shortcut_id: int, callback: Callable) -> None:
        """Define callback para custom shortcut específico
        
        Args:
            shortcut_id: ID do shortcut
            callback: Função a ser chamada quando hotkey for acionado
        """
        self.custom_shortcuts_callbacks[shortcut_id] = callback
    
    def unregister_custom_shortcut(self, shortcut_id: int) -> Tuple[bool, str]:
        """Remove registro de custom shortcut
        
        Args:
            shortcut_id: ID do shortcut a remover
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            if shortcut_id not in self.custom_shortcuts_hotkeys:
                return False, f"Shortcut ID={shortcut_id} não está registrado"
            
            hotkey = self.custom_shortcuts_hotkeys[shortcut_id]
            
            # Remove hotkey
            try:
                keyboard.remove_hotkey(hotkey)
            except Exception as e:
                logging.warning(f"Erro ao remover hotkey '{hotkey}': {e}")
            
            # Remove dos mapeamentos
            del self.custom_shortcuts_hotkeys[shortcut_id]
            if shortcut_id in self.custom_shortcuts_callbacks:
                del self.custom_shortcuts_callbacks[shortcut_id]
            
            if hotkey in self.registered_hotkeys:
                self.registered_hotkeys.remove(hotkey)
            
            logging.info(f"Custom shortcut removido: ID={shortcut_id}, hotkey={hotkey}")
            return True, "Shortcut removido com sucesso"
        
        except Exception as e:
            logging.error(f"Erro ao remover custom shortcut ID={shortcut_id}: {e}")
            return False, f"Erro ao remover: {str(e)}"
    
    def unregister_all_custom_shortcuts(self) -> int:
        """Remove todos os custom shortcuts
        
        Returns:
            int: Número de shortcuts removidos
        """
        count = 0
        shortcut_ids = list(self.custom_shortcuts_hotkeys.keys())
        
        for shortcut_id in shortcut_ids:
            success, _ = self.unregister_custom_shortcut(shortcut_id)
            if success:
                count += 1
        
        return count
    
    def get_registered_custom_shortcuts(self) -> List[Dict[str, Any]]:
        """Retorna lista de custom shortcuts registrados
        
        Returns:
            Lista de dicts com 'id' e 'hotkey'
        """
        return [
            {"id": shortcut_id, "hotkey": hotkey}
            for shortcut_id, hotkey in self.custom_shortcuts_hotkeys.items()
        ]
