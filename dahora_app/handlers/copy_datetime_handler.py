"""
CopyDateTimeHandler - Handler para copiar data/hora formatada
"""
import logging
from typing import TYPE_CHECKING, Optional

from dahora_app.callback_manager import CallbackHandler

if TYPE_CHECKING:
    from dahora_app import DahoraApp, DateTimeFormatter, ClipboardManager


logger = logging.getLogger(__name__)


class CopyDateTimeHandler(CallbackHandler):
    """Handler para copiar timestamp atual para clipboard"""
    
    def __init__(self, app: Optional["DahoraApp"] = None):
        """
        Inicializa o handler de copy
        
        Args:
            app: Referência à instância de DahoraApp (pode ser injetada depois)
        """
        self.app = app
        self.prefix: str = ""
    
    def set_app(self, app: "DahoraApp") -> None:
        """
        Define a referência à aplicação
        
        Args:
            app: Instância de DahoraApp
        """
        self.app = app
    
    def set_prefix(self, prefix: str) -> None:
        """
        Define o prefixo para o timestamp
        
        Args:
            prefix: Prefixo a usar (ex: "log", "debug", etc)
        """
        self.prefix = prefix
    
    def handle(self, hotkey_name: Optional[str] = None) -> bool:
        """
        Copia o timestamp formatado para clipboard
        
        Args:
            hotkey_name: Nome do hotkey que acionou (opcional)
        
        Returns:
            bool: True se copiado com sucesso, False caso contrário
        """
        if not self.app:
            logger.error("CopyDateTimeHandler: app reference not set")
            return False
        
        try:
            # Obter componentes
            datetime_formatter: "DateTimeFormatter" = self.app.datetime_formatter
            clipboard_manager: "ClipboardManager" = self.app.clipboard_manager
            settings = self.app.settings_manager
            
            if not datetime_formatter or not clipboard_manager:
                logger.error("CopyDateTimeHandler: missing dependencies")
                return False
            
            # Formatar timestamp
            timestamp = datetime_formatter.format_datetime(
                template=settings.settings.template,
                separator=settings.settings.separator
            )
            
            # Adicionar prefixo se necessário
            if self.prefix:
                timestamp = f"{self.prefix}{settings.settings.separator}{timestamp}"
            
            # Guardar clipboard atual
            old_clipboard = clipboard_manager.get_clipboard()
            
            # Copiar timestamp
            clipboard_manager.copy_to_clipboard(timestamp)
            logger.info(f"Timestamp copied: {timestamp[:30]}...")
            
            # Restaurar clipboard após delay (preservação inteligente)
            # Isso é feito em background
            if old_clipboard and old_clipboard != timestamp:
                import threading
                
                def restore_clipboard():
                    import time
                    time.sleep(1)  # Aguarda 1s antes de restaurar
                    try:
                        clipboard_manager.copy_to_clipboard(old_clipboard)
                        logger.debug("Clipboard restored")
                    except Exception as e:
                        logger.debug(f"Could not restore clipboard: {e}")
                
                thread = threading.Thread(target=restore_clipboard, daemon=True)
                thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Error in CopyDateTimeHandler: {e}", exc_info=True)
            return False
    
    def get_name(self) -> str:
        """Retorna nome descritivo do handler"""
        return "CopyDateTimeHandler"
