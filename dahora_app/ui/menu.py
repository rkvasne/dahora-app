"""
Sistema de menus do Dahora App
"""
import logging
import pystray
from typing import Callable, Optional, List, Dict
from dahora_app.utils import truncate_text, sanitize_text_for_display, format_hotkey_display


class MenuBuilder:
    """Construtor de menus dinâmicos"""
    
    def __init__(self):
        """Inicializa o construtor de menus"""
        self.copy_datetime_callback: Optional[Callable] = None
        self.show_search_callback: Optional[Callable] = None
        self.show_custom_shortcuts_callback: Optional[Callable] = None  # Configurações unificadas
        self.refresh_menu_callback: Optional[Callable] = None
        self.get_recent_items_callback: Optional[Callable] = None
        self.copy_from_history_callback: Optional[Callable] = None
        self.clear_history_callback: Optional[Callable] = None
        self.show_about_callback: Optional[Callable] = None
        self.show_about_callback: Optional[Callable] = None
        self.quit_callback: Optional[Callable] = None
        self.toggle_pause_callback: Optional[Callable] = None
        self.is_paused_callback: Optional[Callable] = None
        self.hotkey_copy_datetime: str = "ctrl+shift+q"  # Padrão (ação principal)
        self.hotkey_search_history: str = "ctrl+shift+f"  # Padrão
        self.hotkey_refresh_menu: str = "ctrl+shift+r"  # Padrão

    @staticmethod
    def _format_hotkey_display(hotkey: str) -> str:
        """Formata hotkey para exibição (inclui símbolos como !/@/#)."""
        return format_hotkey_display(hotkey)
    
    def set_copy_datetime_callback(self, callback: Callable) -> None:
        """Define callback para copiar data/hora"""
        self.copy_datetime_callback = callback
    
    def set_show_search_callback(self, callback: Callable) -> None:
        """Define callback para mostrar busca"""
        self.show_search_callback = callback
    
    def set_show_custom_shortcuts_callback(self, callback: Callable) -> None:
        """Define callback para mostrar configurações unificadas"""
        self.show_custom_shortcuts_callback = callback
    
    def set_refresh_menu_callback(self, callback: Callable) -> None:
        """Define callback para refresh do menu"""
        self.refresh_menu_callback = callback
    
    def set_get_recent_items_callback(self, callback: Callable) -> None:
        """Define callback para obter itens recentes"""
        self.get_recent_items_callback = callback
    
    def set_copy_from_history_callback(self, callback: Callable) -> None:
        """Define callback para copiar do histórico"""
        self.copy_from_history_callback = callback
    
    def set_clear_history_callback(self, callback: Callable) -> None:
        """Define callback para limpar histórico"""
        self.clear_history_callback = callback
    
    def set_show_about_callback(self, callback: Callable) -> None:
        """Define callback para mostrar sobre"""
        self.show_about_callback = callback
    
    def set_quit_callback(self, callback: Callable) -> None:
        """Define callback para sair"""
        self.quit_callback = callback

    def set_toggle_pause_callback(self, callback: Callable) -> None:
        """Define callback para alternar pausa"""
        self.toggle_pause_callback = callback

    def set_is_paused_callback(self, callback: Callable) -> None:
        """Define callback para verificar estado de pausa"""
        self.is_paused_callback = callback
    
    def _copy_datetime_wrapper(self, icon, item):
        """Wrapper para callback de copiar data/hora"""
        if self.copy_datetime_callback:
            self.copy_datetime_callback(icon, item)
    
    def _show_search_wrapper(self, icon, item):
        """Wrapper para callback de mostrar busca"""
        if self.show_search_callback:
            self.show_search_callback()
    
    def _show_custom_shortcuts_wrapper(self, icon, item):
        """Wrapper para callback de mostrar configurações unificadas"""
        if self.show_custom_shortcuts_callback:
            self.show_custom_shortcuts_callback()
    
    def _refresh_menu_wrapper(self, icon, item):
        """Wrapper para callback de refresh"""
        if self.refresh_menu_callback:
            self.refresh_menu_callback(icon, item)
    
    def _clear_history_wrapper(self, icon, item):
        """Wrapper para callback de limpar histórico"""
        if self.clear_history_callback:
            self.clear_history_callback(icon, item)
    
    def _show_about_wrapper(self, icon, item):
        """Wrapper para callback de sobre"""
        if self.show_about_callback:
            self.show_about_callback(icon, item)
    
    def _quit_wrapper(self, icon, item):
        """Wrapper para callback de sair"""
        if self.quit_callback:
            self.quit_callback(icon, item)

    def _toggle_pause_wrapper(self, icon, item):
        """Wrapper para callback de alternar pausa"""
        if self.toggle_pause_callback:
            self.toggle_pause_callback(icon, item)
    
    def _get_dynamic_menu_items(self) -> List:
        """
        Gera lista de itens do menu dinamicamente
        
        Returns:
            Lista de itens do menu
        """
        menu_items = []
        
        try:
            logging.info("[Menu] Calculando itens dinâmicos (abertura do menu)")
        except Exception:
            pass
        
        # Opções principais (padrão de mercado: ações + atalhos em parênteses, configurações com reticências)
        copy_hk = self._format_hotkey_display(self.hotkey_copy_datetime)
        copy_label = f"Copiar data/hora ({copy_hk})" if copy_hk else "Copiar data/hora"
        menu_items.append(pystray.MenuItem(copy_label, self._copy_datetime_wrapper, default=True))

        search_hk = self._format_hotkey_display(self.hotkey_search_history)
        search_label = f"Buscar no histórico ({search_hk})" if search_hk else "Buscar no histórico"
        menu_items.append(pystray.MenuItem(search_label, self._show_search_wrapper))

        menu_items.append(pystray.MenuItem('Configurações…', self._show_custom_shortcuts_wrapper))

        refresh_hk = self._format_hotkey_display(self.hotkey_refresh_menu)
        refresh_label = f"Recarregar itens ({refresh_hk})" if refresh_hk else "Recarregar itens"
        menu_items.append(pystray.MenuItem(refresh_label, self._refresh_menu_wrapper))
        
        # Separador
        menu_items.append(pystray.Menu.SEPARATOR)
        
        # Histórico dinâmico (últimos 5 itens)
        if self.get_recent_items_callback:
            recent = self.get_recent_items_callback(5)
            if recent:
                for idx, entry in enumerate(reversed(recent), start=1):
                    text = entry.get("text", "") or ""
                    display_text = truncate_text(text, max_length=40)
                    display_text = sanitize_text_for_display(display_text)
                    
                    # Cria função para copiar item
                    def make_copy_func(txt):
                        return lambda icon, item: (
                            self.copy_from_history_callback(txt) 
                            if self.copy_from_history_callback else None
                        )
                    
                    copy_func = make_copy_func(text)
                    menu_items.append(pystray.MenuItem(f"{idx}. {display_text}", copy_func))
            else:
                menu_items.append(pystray.MenuItem('(Histórico vazio)', None, enabled=False))
        
        # Separador
        menu_items.append(pystray.Menu.SEPARATOR)
        
        # Opções finais
        is_paused = self.is_paused_callback() if self.is_paused_callback else False
        pause_label = 'Retomar monitoramento' if is_paused else 'Pausar monitoramento'
        menu_items.append(pystray.MenuItem(pause_label, self._toggle_pause_wrapper))
        
        menu_items.append(pystray.MenuItem('Limpar histórico', self._clear_history_wrapper))
        menu_items.append(pystray.MenuItem('Sobre…', self._show_about_wrapper))
        menu_items.append(pystray.MenuItem('Sair', self._quit_wrapper))
        
        try:
            recent_count = len(recent) if recent else 0
            logging.info(f"Menu gerado com {recent_count} itens do histórico")
        except Exception:
            pass
        
        return menu_items
    
    def create_dynamic_menu(self) -> pystray.Menu:
        """
        Cria um menu dinâmico que atualiza a cada abertura
        
        ✨ ATUALIZAÇÃO AUTOMÁTICA: O menu é atualizado automaticamente
        quando o histórico do clipboard muda através de um callback.
        Sempre que um novo item é adicionado ao histórico, o menu é
        regenerado para mostrar os itens mais recentes.
        
        O item "Recarregar Itens" ainda é útil para forçar refresh via hotkey.
        
        Returns:
            Menu dinâmico do pystray
        """
        logging.info("Gerando menu dinâmico com histórico atualizado")
        
        def dynamic_items():
            """Gerador de itens dinâmicos"""
            try:
                items = self._get_dynamic_menu_items()
                logging.info(f"[Menu] Itens calculados: {len(items)}")
                for it in items:
                    yield it
            except Exception as e:
                logging.warning(f"Falha ao gerar itens do menu dinâmico: {e}")
                # Fallback mínimo
                yield pystray.MenuItem('(Erro ao gerar menu)', None, enabled=False)
        
        return pystray.Menu(dynamic_items)
