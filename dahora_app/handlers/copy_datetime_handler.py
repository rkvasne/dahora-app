import logging
import time
import threading
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from dahora_app.callback_manager import CallbackHandler

if TYPE_CHECKING:
    from dahora_app.app import DahoraApp
    from dahora_app.datetime_formatter import DateTimeFormatter
    from dahora_app.clipboard_manager import ClipboardManager

logger = logging.getLogger(__name__)

class CopyDateTimeHandler(CallbackHandler):
    """Handler para copiar timestamp atual para clipboard"""

    def __init__(self, app: Optional["DahoraApp"] = None):
        """
        Inicializa o handler de copy

        Args:
            app: Referência à instância de DahoraApp
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

    def _get_clipboard_text(self) -> str:
        """Obtém texto atual do clipboard de forma segura"""
        if not self.app or not self.app.clipboard_manager:
            return ""
        return self.app.clipboard_manager.get_text()

    def _copy_to_clipboard(self, text: str) -> None:
        """Copia texto para clipboard de forma segura"""
        if self.app and self.app.clipboard_manager:
            self.app.clipboard_manager.set_text(text)

    def _mark_own_content(self, text: str) -> None:
        """Marca conteúdo como próprio para evitar histórico"""
        if self.app and self.app.clipboard_manager:
            self.app.clipboard_manager.mark_own_content(text, ttl_seconds=2.0)

    def _get_separator(self) -> str:
        """Obtém separador configurado"""
        try:
            if self.app and self.app.settings_manager:
                settings_container = getattr(
                    self.app.settings_manager, "settings", None
                )
                sep = getattr(settings_container, "separator", None)
                if isinstance(sep, str) and sep:
                    return sep
        except Exception:
            pass
        return "-"

    def _restore_clipboard(self, text: str) -> None:
        time.sleep(0.1)
        try:
            self._mark_own_content(text)
            self._copy_to_clipboard(text)
            logger.debug("Clipboard restored to original content")
        except Exception as e:
            logger.debug(f"Could not restore clipboard: {e}")

    def _restore_clipboard_async(self, text: str) -> None:
        """Restaura clipboard original em background"""
        def restore_task():
            self._restore_clipboard(text)

        if self.app and hasattr(self.app, "_sync_manager"):
            sync_manager = self.app._sync_manager
            if sync_manager and hasattr(sync_manager, "start_daemon_thread"):
                start_daemon_thread = sync_manager.start_daemon_thread
                if callable(start_daemon_thread):
                    try:
                        start_daemon_thread(restore_task)
                        return
                    except Exception:
                        pass

        thread = threading.Thread(target=restore_task, daemon=True)
        thread.start()

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
            datetime_formatter = self.app.datetime_formatter
            clipboard_manager = self.app.clipboard_manager

            if not datetime_formatter or not clipboard_manager:
                logger.error("CopyDateTimeHandler: missing dependencies")
                return False

            formatted = datetime_formatter.format_datetime(datetime.now())
            timestamp = formatted if isinstance(formatted, str) else str(formatted)
            if not timestamp:
                return False

            if self.prefix:
                timestamp = f"{self.prefix}{self._get_separator()}{timestamp}"

            # Guardar clipboard atual para preservação
            old_clipboard = self._get_clipboard_text()

            # Marcar conteúdo como próprio
            self._mark_own_content(timestamp)

            # Copiar timestamp para clipboard
            self._copy_to_clipboard(timestamp)

            clipboard_ok = False
            for _ in range(3):
                if self._get_clipboard_text() == timestamp:
                    clipboard_ok = True
                    break
                time.sleep(0.02)

            if not clipboard_ok:
                logger.warning("CopyDateTimeHandler: clipboard copy failed")
                return False
            
            # Aguarda clipboard estar pronto e envia Ctrl+V para colar automaticamente
            time.sleep(0.05)
            try:
                import keyboard
                keyboard.send('ctrl+v')
                logger.info(f"Timestamp pasted: {timestamp[:30]}...")
            except Exception as e:
                logger.warning(f"Could not auto-paste (keyboard.send failed): {e}")
                logger.info(f"Timestamp copied: {timestamp[:30]}...")
            
            time.sleep(0.05)  # Aguarda colagem completar

            # Restaurar clipboard original se for diferente
            if old_clipboard and old_clipboard != timestamp:
                self._restore_clipboard_async(old_clipboard)

            return True

        except Exception as e:
            logger.error(f"Error in CopyDateTimeHandler: {e}", exc_info=True)
            return False

    def get_name(self) -> str:
        """Retorna nome descritivo do handler"""
        return "CopyDateTimeHandler"
