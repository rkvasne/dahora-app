"""
ShowSearchHandler - Handler para exibir janela de busca
"""
import logging
from typing import TYPE_CHECKING, Optional

from dahora_app.callback_manager import CallbackHandler

if TYPE_CHECKING:
    from main import DahoraApp


logger = logging.getLogger(__name__)


class ShowSearchHandler(CallbackHandler):
    """Handler para abrir a janela de busca no histórico"""
    
    def __init__(self, app: Optional["DahoraApp"] = None):
        """
        Inicializa o handler de search
        
        Args:
            app: Referência à instância de DahoraApp (pode ser injetada depois)
        """
        self.app = app
        self.use_modern_ui: bool = True
    
    def set_app(self, app: "DahoraApp") -> None:
        """
        Define a referência à aplicação
        
        Args:
            app: Instância de DahoraApp
        """
        self.app = app
    
    def set_use_modern_ui(self, use_modern: bool) -> None:
        """
        Define qual UI usar (moderna ou clássica)
        
        Args:
            use_modern: True para UI moderna, False para clássica
        """
        self.use_modern_ui = use_modern
    
    def handle(self, icon=None, item=None) -> bool:
        """
        Exibe a janela de busca
        
        Args:
            icon: Ícone do pystray (callback param)
            item: Item do menu (callback param)
        
        Returns:
            bool: True se janela foi exibida, False caso contrário
        """
        if not self.app:
            logger.error("ShowSearchHandler: app reference not set")
            return False
        
        try:
            # Verifica qual UI usar baseado em settings
            try:
                use_modern = self.app.settings_manager.settings.use_modern_ui
            except (AttributeError, KeyError):
                use_modern = self.use_modern_ui
            
            # Seleciona o dialog apropriado
            if use_modern:
                search_dialog = self.app.modern_search_dialog
                logger.debug("Opening modern search dialog")
            else:
                search_dialog = self.app.search_dialog
                logger.debug("Opening classic search dialog")
            
            if not search_dialog:
                logger.error("ShowSearchHandler: search dialog not initialized")
                return False
            
            # Exibe a janela
            search_dialog.show()
            logger.info("Search dialog opened")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in ShowSearchHandler: {e}", exc_info=True)
            return False
    
    def get_name(self) -> str:
        """Retorna nome descritivo do handler"""
        return "ShowSearchHandler"
