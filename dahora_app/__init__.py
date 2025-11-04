"""
Dahora App - Sistema de Bandeja do Windows
Gera data e hora no formato [DD.MM.AAAA-HH:MM] e copia para área de transferência
"""

__version__ = "0.0.9"
__author__ = "Dahora App Team"

# Imports principais
from dahora_app.constants import APP_NAME, APP_VERSION, DATA_DIR
from dahora_app.settings import SettingsManager
from dahora_app.counter import UsageCounter
from dahora_app.clipboard_manager import ClipboardManager
from dahora_app.datetime_formatter import DateTimeFormatter
from dahora_app.notifications import NotificationManager
from dahora_app.hotkeys import HotkeyManager
from dahora_app.ui import PrefixDialog, IconManager, MenuBuilder, SettingsDialog

__all__ = [
    'APP_NAME',
    'APP_VERSION',
    'DATA_DIR',
    'SettingsManager',
    'UsageCounter',
    'ClipboardManager',
    'DateTimeFormatter',
    'NotificationManager',
    'HotkeyManager',
    'PrefixDialog',
    'IconManager',
    'MenuBuilder',
    'SettingsDialog',
]
