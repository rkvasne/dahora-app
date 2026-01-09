"""
Módulo UI do Dahora App
"""

from dahora_app.ui.prefix_dialog import PrefixDialog
from dahora_app.ui.icon_manager import IconManager
from dahora_app.ui.menu import MenuBuilder
from dahora_app.ui.settings_dialog import SettingsDialog
from dahora_app.ui.search_dialog import SearchDialog
from dahora_app.ui.custom_shortcuts_dialog import CustomShortcutsDialog
from dahora_app.ui.shortcut_editor import ShortcutEditorDialog
from dahora_app.ui.about_dialog import AboutDialog

# Modern UI (CustomTkinter)
from dahora_app.ui.modern_styles import (
    ModernTheme,
    ModernWindow,
    ModernFrame,
    ModernButton,
    ModernEntry,
    ModernLabel,
    ModernCheckbox,
    ModernSpinbox,
    ModernTabview,
    ModernScrollableFrame,
    ModernTextbox,
)
from dahora_app.ui.modern_settings_dialog import ModernSettingsDialog
from dahora_app.ui.modern_shortcut_editor import ModernShortcutEditor
from dahora_app.ui.modern_about_dialog import ModernAboutDialog
from dahora_app.ui.modern_search_dialog import ModernSearchDialog

__all__ = [
    # Legacy UI
    "PrefixDialog",
    "IconManager",
    "MenuBuilder",
    "SettingsDialog",
    "SearchDialog",
    "CustomShortcutsDialog",
    "ShortcutEditorDialog",
    "AboutDialog",
    # Modern UI
    "ModernTheme",
    "ModernWindow",
    "ModernFrame",
    "ModernButton",
    "ModernEntry",
    "ModernLabel",
    "ModernCheckbox",
    "ModernSpinbox",
    "ModernTabview",
    "ModernScrollableFrame",
    "ModernTextbox",
    "ModernSettingsDialog",
    "ModernShortcutEditor",
    "ModernAboutDialog",
    "ModernSearchDialog",
]
