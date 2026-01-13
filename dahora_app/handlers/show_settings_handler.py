"""
ShowSettingsHandler - Handler para exibir janela de configurações
"""

import logging
from typing import TYPE_CHECKING, Optional

from dahora_app.callback_manager import CallbackHandler

if TYPE_CHECKING:
    from dahora_app.app import DahoraApp


logger = logging.getLogger(__name__)


class ShowSettingsHandler(CallbackHandler):
    """Handler para abrir o painel de configurações"""

    def __init__(self, app: Optional["DahoraApp"] = None):
        """
        Inicializa o handler de settings

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
        Exibe a janela de configurações

        Args:
            icon: Ícone do pystray (callback param)
            item: Item do menu (callback param)

        Returns:
            bool: True se janela foi exibida, False caso contrário
        """
        if not self.app:
            logger.error("ShowSettingsHandler: app reference not set")
            return False

        try:
            # Verifica qual UI usar baseado em settings
            try:
                use_modern = self.app.settings_manager.settings.use_modern_ui
            except (AttributeError, KeyError):
                use_modern = self.use_modern_ui

            # Seleciona o dialog apropriado
            if use_modern:
                settings_dialog = self.app.modern_settings_dialog
                logger.debug("Opening modern settings dialog")
            else:
                settings_dialog = self.app.settings_dialog
                logger.debug("Opening classic settings dialog")

            if not settings_dialog:
                logger.error("ShowSettingsHandler: settings dialog not initialized")
                return False

            # Exibe a janela
            settings_dialog.show()
            logger.info("Settings dialog opened")

            return True

        except Exception as e:
            logger.error(f"Error in ShowSettingsHandler: {e}", exc_info=True)
            return False

    def get_name(self) -> str:
        """Retorna nome descritivo do handler"""
        return "ShowSettingsHandler"
