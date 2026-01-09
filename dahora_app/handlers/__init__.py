"""
Handlers - Implementações específicas de callbacks para eventos da aplicação
"""

from dahora_app.handlers.quit_app_handler import QuitAppHandler
from dahora_app.handlers.copy_datetime_handler import CopyDateTimeHandler
from dahora_app.handlers.show_settings_handler import ShowSettingsHandler
from dahora_app.handlers.show_search_handler import ShowSearchHandler

__all__ = [
    "QuitAppHandler",
    "CopyDateTimeHandler",
    "ShowSettingsHandler",
    "ShowSearchHandler",
]
