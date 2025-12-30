"""
QuitAppHandler - Handler para encerrar o aplicativo
"""
import logging
from typing import TYPE_CHECKING, Optional

from dahora_app.callback_manager import CallbackHandler

if TYPE_CHECKING:
    from dahora_app import DahoraApp  # Import apenas para type hints


logger = logging.getLogger(__name__)


class QuitAppHandler(CallbackHandler):
    """Handler para encerrar a aplicação de forma segura"""
    
    def __init__(self, app: Optional["DahoraApp"] = None):
        """
        Inicializa o handler de quit
        
        Args:
            app: Referência à instância de DahoraApp (pode ser injetada depois)
        """
        self.app = app
        self._already_shutting_down = False
    
    def set_app(self, app: "DahoraApp") -> None:
        """
        Define a referência à aplicação (injeta dependência)
        
        Args:
            app: Instância de DahoraApp
        """
        self.app = app
    
    def handle(self, icon=None, item=None) -> bool:
        """
        Encerra o aplicativo de forma segura e coordenada
        
        Args:
            icon: Ícone do pystray (callback param)
            item: Item do menu (callback param)
        
        Returns:
            bool: True se shutdown foi iniciado, False se já estava em progresso
        """
        if not self.app:
            logger.error("QuitAppHandler: app reference not set")
            return False
        
        try:
            # Requisita shutdown através do ThreadSyncManager
            sync_manager = self.app._sync_manager
            if not sync_manager.request_shutdown():
                logger.debug("Shutdown já foi requisitado por outra thread")
                return False
            
            logger.info("Encerrando Dahora App...")
            
            # Para o tray o quanto antes
            try:
                if icon:
                    try:
                        icon.visible = False
                    except Exception:
                        pass
                    icon.stop()
                    logger.debug("Pystray stopped")
            except Exception as e:
                logger.error(f"Error stopping pystray: {e}")
            
            # Encerra o loop Tk no main thread
            try:
                if self.app._ui_root is not None:
                    self.app._ui_root.after(0, self.app._ui_root.quit)
                    logger.debug("Tk mainloop quit requested")
            except Exception as e:
                logger.error(f"Error quitting Tk: {e}")
            
            # Cleanup de recursos
            try:
                from dahora_app.single_instance import cleanup_single_instance
                cleanup_single_instance()
                logger.debug("Single instance cleaned up")
            except Exception as e:
                logger.warning(f"Error in cleanup_single_instance: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in QuitAppHandler: {e}", exc_info=True)
            return False
    
    def get_name(self) -> str:
        """Retorna nome descritivo do handler"""
        return "QuitAppHandler"
