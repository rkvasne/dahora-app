"""
CopyDateTimeHandler - Handler para copiar data/hora formatada e colar automaticamente
"""

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

            def get_clipboard_text() -> str:
                clipboard_get = getattr(clipboard_manager, "get_clipboard", None)
                if callable(clipboard_get):
                    try:
                        value = clipboard_get()
                        return value if isinstance(value, str) else ""
                    except Exception:
                        return ""

                clipboard_paste = getattr(clipboard_manager, "paste_text", None)
                if callable(clipboard_paste):
                    try:
                        value = clipboard_paste()
                        return value if isinstance(value, str) else ""
                    except Exception:
                        return ""

                return ""

            def copy_to_clipboard(text: str) -> None:
                clipboard_copy = getattr(clipboard_manager, "copy_to_clipboard", None)
                if callable(clipboard_copy):
                    clipboard_copy(text)
                    return

                clipboard_copy_text = getattr(clipboard_manager, "copy_text", None)
                if callable(clipboard_copy_text):
                    clipboard_copy_text(text)
                    return

                raise RuntimeError(
                    "ClipboardManager não possui método de cópia suportado"
                )

            def get_separator() -> str:
                try:
                    settings = getattr(self.app, "settings_manager", None)
                    settings_obj = getattr(settings, "settings", None)
                    sep = getattr(settings_obj, "separator", None)
                    if isinstance(sep, str) and sep:
                        return sep
                except Exception:
                    pass
                return "-"

            # Obter componentes
            datetime_formatter: "DateTimeFormatter" = self.app.datetime_formatter
            clipboard_manager: "ClipboardManager" = self.app.clipboard_manager

            if not datetime_formatter or not clipboard_manager:
                logger.error("CopyDateTimeHandler: missing dependencies")
                return False

            formatted = datetime_formatter.format_datetime(datetime.now())
            timestamp = formatted if isinstance(formatted, str) else str(formatted)
            if not timestamp:
                return False

            if self.prefix:
                timestamp = f"{self.prefix}{get_separator()}{timestamp}"

            # Guardar clipboard atual para preservação
            old_clipboard = get_clipboard_text()

            # Marcar conteúdo como próprio (evita ir para histórico)
            mark_own_content = getattr(clipboard_manager, "mark_own_content", None)
            if callable(mark_own_content):
                mark_own_content(timestamp, ttl_seconds=2.0)

            # Copiar timestamp para clipboard
            copy_to_clipboard(timestamp)
            
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

            # Restaurar clipboard original após pequeno delay (preservação inteligente)
            if old_clipboard and old_clipboard != timestamp:
                def restore_clipboard():
                    time.sleep(0.1)  # Pequeno delay para garantir colagem
                    try:
                        if callable(mark_own_content):
                            mark_own_content(old_clipboard, ttl_seconds=2.0)
                        copy_to_clipboard(old_clipboard)
                        logger.debug("Clipboard restored to original content")
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
