"""
Dahora App - Sistema de Bandeja do Windows
Cola timestamps formatados diretamente com atalhos personalizáveis
"""

__version__ = "0.2.11"
__author__ = "Dahora App Team"

# Imports principais
from dahora_app.constants import APP_NAME, APP_VERSION, DATA_DIR
from dahora_app.settings import SettingsManager
from dahora_app.counter import UsageCounter
from dahora_app.clipboard_manager import ClipboardManager
from dahora_app.datetime_formatter import DateTimeFormatter
from dahora_app.notifications import NotificationManager
from dahora_app.hotkeys import HotkeyManager
from dahora_app.hotkey_validator import HotkeyValidator
from dahora_app.single_instance import (
    SingleInstanceManager,
    initialize_single_instance,
    cleanup_single_instance,
)
from dahora_app.thread_sync import ThreadSyncManager, initialize_sync, get_sync_manager
from dahora_app.callback_manager import (
    CallbackHandler,
    CallbackRegistry,
    get_callback_registry,
    initialize_callbacks,
    # Protocols para type hints
    CopyDatetimeCallback,
    RefreshMenuCallback,
    MenuItemCallback,
    SearchCallback,
    SettingsSavedCallback,
    CopyFromHistoryCallback,
    NotificationCallback,
    GetHistoryCallback,
)
from dahora_app.handlers import (
    QuitAppHandler,
    CopyDateTimeHandler,
    ShowSettingsHandler,
    ShowSearchHandler,
)
from dahora_app.ui import (
    PrefixDialog,
    IconManager,
    MenuBuilder,
    SettingsDialog,
    SearchDialog,
    CustomShortcutsDialog,
    AboutDialog,
    ModernSettingsDialog,
    ModernAboutDialog,
    ModernSearchDialog,
)

__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "DATA_DIR",
    "SettingsManager",
    "UsageCounter",
    "ClipboardManager",
    "DateTimeFormatter",
    "NotificationManager",
    "HotkeyManager",
    "HotkeyValidator",
    "SingleInstanceManager",
    "initialize_single_instance",
    "cleanup_single_instance",
    "ThreadSyncManager",
    "initialize_sync",
    "get_sync_manager",
    "CallbackHandler",
    "CallbackRegistry",
    "get_callback_registry",
    "initialize_callbacks",
    # Protocols para type hints
    "CopyDatetimeCallback",
    "RefreshMenuCallback",
    "MenuItemCallback",
    "SearchCallback",
    "SettingsSavedCallback",
    "CopyFromHistoryCallback",
    "NotificationCallback",
    "GetHistoryCallback",
    # Handlers
    "QuitAppHandler",
    "CopyDateTimeHandler",
    "ShowSettingsHandler",
    "ShowSearchHandler",
    # UI Components
    "PrefixDialog",
    "IconManager",
    "MenuBuilder",
    "SettingsDialog",
    "SearchDialog",
    "CustomShortcutsDialog",
    "AboutDialog",
    "ModernSettingsDialog",
    "ModernAboutDialog",
    "ModernSearchDialog",
]
