"""
Dahora App - Aplicação principal
"""

import sys
import os
import hashlib
import logging
import threading
import pyperclip
import pystray
import keyboard
import time
from typing import Optional
from threading import Lock

from dahora_app import (
    SettingsManager,
    UsageCounter,
    ClipboardManager,
    DateTimeFormatter,
    NotificationManager,
    HotkeyManager,
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
from dahora_app.single_instance import initialize_single_instance, cleanup_single_instance
from dahora_app.thread_sync import initialize_sync
from dahora_app.callback_manager import CallbackRegistry
from dahora_app.handlers import (
    CopyDateTimeHandler,
    ShowSearchHandler,
    ShowSettingsHandler,
    QuitAppHandler,
)
from dahora_app.constants import (
    APP_TITLE,
    DATA_DIR,
    LOG_FILE,
    PRIVACY_MARKER_FILE,
)

global_icon = None


class DahoraApp:
    """Aplicação principal do Dahora App"""

    def __init__(self, file_handler=None):
        """Inicializa a aplicação"""
        self._file_handler = file_handler
        self.settings_manager = SettingsManager()
        self.counter = UsageCounter()
        self.clipboard_manager = ClipboardManager()
        self.datetime_formatter = DateTimeFormatter()
        self.notification_manager = NotificationManager()
        self.hotkey_manager = HotkeyManager()
        self.prefix_dialog = PrefixDialog()
        self.settings_dialog = SettingsDialog()
        self.search_dialog = SearchDialog()
        self.custom_shortcuts_dialog = CustomShortcutsDialog()
        self.modern_settings_dialog = ModernSettingsDialog()  # UI Moderna
        self.modern_about_dialog = ModernAboutDialog()  # UI Moderna
        self.modern_search_dialog = ModernSearchDialog()  # UI Moderna

        self._ui_root = None
        self._ui_lock = Lock()
        self._tray_thread: Optional[threading.Thread] = None
        self._sync_manager = initialize_sync()

        self.callback_registry = CallbackRegistry()
        if self._sync_manager:
            self.callback_registry.set_sync_manager(self._sync_manager)

        self.about_dialog = AboutDialog()
        self.menu_builder = MenuBuilder()
        self.icon = None

    def initialize(self):
        """Inicializa todos os componentes"""
        logging.info("Inicializando Dahora App...")

        self.counter.load()
        self.clipboard_manager.load_history()
        self.settings_manager.load()

        try:
            self.clipboard_manager.set_max_history_items(
                int(self.settings_manager.max_history_items)
            )
            self.clipboard_manager.set_monitoring_config(
                float(self.settings_manager.clipboard_monitor_interval),
                float(self.settings_manager.clipboard_idle_threshold),
            )
        except Exception as e:
            logging.warning(
                f"Falha ao configurar parâmetros do clipboard manager: {e}",
                exc_info=False,
            )

        try:
            if self._file_handler is not None:
                self._file_handler.maxBytes = int(self.settings_manager.log_max_bytes)
                self._file_handler.backupCount = int(self.settings_manager.log_backup_count)
        except Exception:
            pass

        self.datetime_formatter.set_prefix(self.settings_manager.get_prefix())
        self.datetime_formatter.set_brackets(
            self.settings_manager.bracket_open, self.settings_manager.bracket_close
        )

        self._register_handlers()
        self._setup_callbacks()

        print(">>> Iniciando setup de custom shortcuts...")
        self._setup_custom_shortcuts()
        print(">>> Setup de custom shortcuts concluído")

        self.show_privacy_notice()

        self.clipboard_manager.initialize_last_content()

        logging.info("Dahora App inicializado com sucesso")

    def _register_handlers(self):
        """Registra todos os handlers no callback registry"""
        copy_handler = CopyDateTimeHandler(app=self)
        copy_handler.set_prefix(self.settings_manager.get_prefix())
        self.callback_registry.register("copy_datetime", copy_handler)

        search_handler = ShowSearchHandler(app=self)
        search_handler.set_use_modern_ui(True)
        self.callback_registry.register("show_search", search_handler)

        settings_handler = ShowSettingsHandler(app=self)
        settings_handler.set_use_modern_ui(True)
        self.callback_registry.register("show_settings", settings_handler)

        quit_handler = QuitAppHandler(app=self)
        self.callback_registry.register("quit_app", quit_handler)

        logging.info("Handlers registrados no callback registry")

    def _sync_all_components(self):
        """
        Sincroniza todos os componentes após mudanças de configuração.
        Único ponto de entrada para aplicar mudanças em hotkeys, UI, etc.
        """
        try:
            current_settings = self.settings_manager.get_all()

            try:
                self.clipboard_manager.set_max_history_items(
                    int(current_settings.get("max_history_items", 100))
                )
                self.clipboard_manager.set_monitoring_config(
                    float(current_settings.get("clipboard_monitor_interval", 3.0)),
                    float(current_settings.get("clipboard_idle_threshold", 30.0)),
                )
            except Exception as e:
                logging.warning(f"Erro ao atualizar clipboard manager: {e}")

            try:
                if self._file_handler is not None:
                    self._file_handler.maxBytes = int(
                        current_settings.get("log_max_bytes", self.settings_manager.log_max_bytes)
                    )
                    self._file_handler.backupCount = int(
                        current_settings.get(
                            "log_backup_count", self.settings_manager.log_backup_count
                        )
                    )
            except Exception as e:
                logging.warning(f"Erro ao atualizar log handler: {e}")

            self.datetime_formatter.set_prefix(current_settings.get("prefix", ""))
            self.datetime_formatter.set_brackets(
                current_settings.get("bracket_open", "["),
                current_settings.get("bracket_close", "]"),
            )

            copy_handler = self.callback_registry.get("copy_datetime")
            if copy_handler and isinstance(copy_handler, CopyDateTimeHandler):
                copy_handler.set_prefix(current_settings.get("prefix", ""))

            self.menu_builder.hotkey_copy_datetime = current_settings.get(
                "hotkey_copy_datetime", "ctrl+shift+q"
            )
            self.menu_builder.hotkey_search_history = current_settings.get(
                "hotkey_search_history", "ctrl+shift+f"
            )
            self.menu_builder.hotkey_refresh_menu = current_settings.get(
                "hotkey_refresh_menu", "ctrl+shift+r"
            )
            try:
                self.menu_builder.tray_menu_cache_window_ms = int(
                    current_settings.get("tray_menu_cache_window_ms", 200)
                )
            except Exception:
                pass

            copy_hk = current_settings.get("hotkey_copy_datetime", "ctrl+shift+q")
            search_hk = current_settings.get("hotkey_search_history", "ctrl+shift+f")
            refresh_hk = current_settings.get("hotkey_refresh_menu", "ctrl+shift+r")

            self.hotkey_manager.set_configured_hotkeys(copy_hk, search_hk, refresh_hk)
            hotkey_results = self.hotkey_manager.apply_configured_hotkeys()

            return hotkey_results

        except Exception as e:
            logging.error(f"Erro ao sincronizar componentes: {e}")
            return {}

    def _setup_callbacks(self):
        """Configura todos os callbacks entre componentes"""
        self.prefix_dialog.set_prefix(self.settings_manager.get_prefix())
        self.prefix_dialog.set_on_save_callback(self._on_prefix_saved)
        self.prefix_dialog.notification_callback = self.notification_manager.show_toast

        self.settings_dialog.set_current_settings(self.settings_manager.get_all())
        self.settings_dialog.set_on_save_callback(self._on_settings_saved)
        self.settings_dialog.notification_callback = self.notification_manager.show_toast

        self.search_dialog.set_get_history_callback(
            lambda: self.clipboard_manager.clipboard_history
        )
        self.search_dialog.set_copy_callback(self._copy_from_history)
        self.search_dialog.notification_callback = self.notification_manager.show_toast

        self.modern_search_dialog.set_get_history_callback(
            lambda: self.clipboard_manager.clipboard_history
        )
        self.modern_search_dialog.set_copy_callback(self._copy_from_history)
        self.modern_search_dialog.notification_callback = (
            self.notification_manager.show_toast
        )

        self.custom_shortcuts_dialog.set_current_settings(self.settings_manager.get_all())
        self.custom_shortcuts_dialog.set_on_add_callback(
            self._on_add_custom_shortcut_wrapper
        )
        self.custom_shortcuts_dialog.set_on_update_callback(
            self._on_update_custom_shortcut_wrapper
        )
        self.custom_shortcuts_dialog.set_on_remove_callback(
            self._on_remove_custom_shortcut_wrapper
        )
        self.custom_shortcuts_dialog.set_on_validate_hotkey_callback(
            self.hotkey_manager.validate_hotkey
        )
        self.custom_shortcuts_dialog.set_on_save_callback(self._on_settings_saved)
        self.custom_shortcuts_dialog.on_get_settings_callback = (
            self.settings_manager.get_all
        )
        self.custom_shortcuts_dialog.notification_callback = (
            self.notification_manager.show_toast
        )

        self.modern_settings_dialog.set_current_settings(self.settings_manager.get_all())
        self.modern_settings_dialog.set_on_add_callback(self._on_add_custom_shortcut_wrapper)
        self.modern_settings_dialog.set_on_update_callback(
            self._on_update_custom_shortcut_wrapper
        )
        self.modern_settings_dialog.set_on_remove_callback(
            self._on_remove_custom_shortcut_wrapper
        )
        self.modern_settings_dialog.set_on_validate_hotkey_callback(
            self.hotkey_manager.validate_hotkey
        )
        self.modern_settings_dialog.set_on_save_callback(self._on_settings_saved)
        self.modern_settings_dialog.on_get_settings_callback = self.settings_manager.get_all
        self.modern_settings_dialog.notification_callback = (
            self.notification_manager.show_toast
        )

        self.hotkey_manager.set_copy_datetime_callback(self._on_copy_datetime_hotkey_wrapper)
        self.hotkey_manager.set_refresh_menu_callback(self._on_refresh_menu)
        self.hotkey_manager.set_search_callback(self._show_search_dialog_wrapper)
        self.hotkey_manager.set_ctrl_c_callback(self._on_ctrl_c)

        self.hotkey_manager.set_configured_hotkeys(
            self.settings_manager.hotkey_copy_datetime,
            self.settings_manager.hotkey_search_history,
            self.settings_manager.hotkey_refresh_menu,
        )

        self.menu_builder.set_copy_datetime_callback(self._copy_datetime_menu)
        self.menu_builder.set_show_search_callback(self._show_search_dialog_wrapper)
        self.menu_builder.set_show_custom_shortcuts_callback(
            self._show_custom_shortcuts_dialog
        )
        self.menu_builder.set_refresh_menu_callback(self._refresh_menu_action)
        self.menu_builder.hotkey_copy_datetime = self.settings_manager.hotkey_copy_datetime
        self.menu_builder.hotkey_search_history = self.settings_manager.hotkey_search_history
        self.menu_builder.hotkey_refresh_menu = self.settings_manager.hotkey_refresh_menu
        try:
            self.menu_builder.tray_menu_cache_window_ms = int(
                self.settings_manager.tray_menu_cache_window_ms
            )
        except Exception:
            pass
        self.menu_builder.set_get_recent_items_callback(
            self.clipboard_manager.get_recent_items
        )
        self.menu_builder.set_copy_from_history_callback(self._copy_from_history)
        self.menu_builder.set_clear_history_callback(self._clear_history)
        self.menu_builder.set_show_about_callback(self._show_about)
        self.menu_builder.set_toggle_pause_callback(self._toggle_pause)
        self.menu_builder.set_is_paused_callback(lambda: self.clipboard_manager.paused)
        self.menu_builder.set_quit_callback(self._quit_app_wrapper)

    def _on_prefix_saved(self, prefix: str):
        """Callback quando prefixo é salvo"""
        self.settings_manager.set_prefix(prefix)
        self.datetime_formatter.set_prefix(prefix)
        self.prefix_dialog.set_prefix(prefix)

    def _on_settings_saved(self, settings: dict):
        """
        Callback quando configurações são salvas.
        Único ponto de entrada - delega sincronização para _sync_all_components()
        """
        self.settings_manager.update_all(settings)
        hotkey_results = self._sync_all_components()

        errors = [
            v
            for v in hotkey_results.values()
            if isinstance(v, str) and v.startswith("erro")
        ]
        if errors:
            self.notification_manager.show_toast(
                "Dahora App",
                "Configurações salvas!\n\n⚠️ Algumas teclas não puderam ser aplicadas agora.\nVerifique conflitos com atalhos personalizados.",
                duration=5,
            )
        else:
            self.notification_manager.show_toast("Dahora App", "Configurações salvas e aplicadas!")

        logging.info(f"Configurações atualizadas: {settings}")

    def _on_refresh_menu(self):
        """Callback para refresh do menu via hotkey"""
        if self.icon:
            self._refresh_menu_action(self.icon, None)

    def _on_ctrl_c(self):
        """Callback para Ctrl+C"""
        current_content = self.clipboard_manager.paste_text()
        if current_content and current_content.strip():
            self.clipboard_manager.add_to_history(current_content)
            content_len = len(current_content)
            content_hash = hashlib.sha256(
                current_content.encode("utf-8", errors="replace")
            ).hexdigest()[:12]
            logging.info(f"Ctrl+C detectado: len={content_len}, sha256={content_hash}")

    def _on_history_updated(self):
        """Callback quando o histórico do clipboard é atualizado"""
        pass

    def _setup_custom_shortcuts(self):
        """Configura custom shortcuts na inicialização (NOVO)"""
        try:
            logging.info("=== Iniciando configuração de custom shortcuts ===")

            custom_shortcuts = self.settings_manager.get_custom_shortcuts(enabled_only=True)

            if not custom_shortcuts:
                logging.info("Nenhum custom shortcut configurado - OK, pulando")
                return

            logging.info(f"Configurando {len(custom_shortcuts)} custom shortcuts...")

            results = self.hotkey_manager.setup_custom_hotkeys(custom_shortcuts)

            for shortcut in custom_shortcuts:
                shortcut_id = shortcut["id"]
                prefix = shortcut["prefix"]

                def make_callback(p):
                    return lambda: self._on_custom_shortcut_triggered(p)

                self.hotkey_manager.set_custom_shortcut_callback(
                    shortcut_id, make_callback(prefix)
                )

                status = results.get(shortcut_id, "unknown")
                hotkey = shortcut.get("hotkey", "").upper()
                if status == "ok":
                    logging.info(f"✓ Custom shortcut OK: [{hotkey}] → {prefix}")
                else:
                    logging.warning(f"✗ Custom shortcut FALHOU: [{hotkey}] → {status}")

            success_count = sum(1 for s in results.values() if s == "ok")
            if success_count > 0:
                logging.info(
                    f"{success_count}/{len(custom_shortcuts)} custom shortcuts registrados com sucesso"
                )

        except Exception as e:
            logging.error(f"Erro ao configurar custom shortcuts: {e}")
            import traceback

            logging.error(f"Traceback: {traceback.format_exc()}")

    def _on_custom_shortcut_triggered(self, prefix: str):
        """Callback quando custom shortcut é acionado (COLA DIRETAMENTE SEM AFETAR CLIPBOARD)"""
        try:
            dt_string = self.datetime_formatter.format_with_prefix(prefix)
            self.clipboard_manager.mark_own_content(dt_string)

            clipboard_backup = None
            try:
                clipboard_backup = pyperclip.paste()
            except Exception:
                pass

            pyperclip.copy(dt_string)
            time.sleep(0.05)

            keyboard.send("ctrl+v")
            time.sleep(0.05)

            if clipboard_backup is not None:
                try:
                    pyperclip.copy(clipboard_backup)
                except Exception:
                    pass

            count = self.counter.increment()

            logging.info(
                f"Custom shortcut acionado: prefix='{prefix}', resultado={dt_string}, total={count}ª vez"
            )

        except Exception as e:
            logging.error(f"Erro ao processar custom shortcut: {e}")
            self.notification_manager.show_toast(
                "Erro no Atalho", f"Falha ao processar atalho: {e}"
            )

    def _format_datetime_for_default_shortcut(self) -> str:
        """Gera timestamp usando o atalho padrão (se existir); fallback para prefixo global."""
        try:
            default_id = getattr(self.settings_manager, "default_shortcut_id", None)
        except Exception:
            default_id = None

        if default_id is not None:
            try:
                shortcut = self.settings_manager.get_custom_shortcut_by_id(int(default_id))
            except Exception:
                shortcut = None

            if shortcut:
                prefix = str(shortcut.get("prefix", ""))
                return self.datetime_formatter.format_with_prefix(prefix)

        return self.datetime_formatter.format_now()

    def copy_datetime(self, icon=None, item=None, source=None):
        """Copia a data e hora para a área de transferência"""
        dt_string = self._format_datetime_for_default_shortcut()
        self.clipboard_manager.mark_own_content(dt_string)
        self.clipboard_manager.copy_text(dt_string)

        count = self.counter.increment()

        if item and hasattr(item, "text"):
            source = "Menu: " + item.text
        else:
            source = source or ("Atalho" if icon else "Fallback")

        if source.startswith("Menu:"):
            self.notification_manager.show_toast(
                "Dahora App",
                f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {count}ª vez",
            )
        else:
            dur = 1.5 if source == "Atalho" else 2
            try:
                if source == "Atalho":
                    self.notification_manager.show_quick_notification(
                        "Dahora App",
                        f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {count}ª vez",
                        duration=dur,
                    )
                else:
                    self.notification_manager.show_toast(
                        "Dahora App",
                        f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {count}ª vez",
                        duration=dur,
                    )
            except Exception:
                self.notification_manager.show_toast(
                    "Dahora App",
                    f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {count}ª vez",
                    duration=dur,
                )

    def _on_copy_datetime_hotkey_wrapper(self) -> None:
        """
        Wrapper para usar handler de copy_datetime.
        """
        handler = self.callback_registry.get("copy_datetime")
        if not handler:
            logging.error("copy_datetime handler not found in registry")
            return
        handler.handle()

    def _copy_datetime_menu(self, icon, item):
        """Wrapper para copiar data/hora do menu"""
        self.copy_datetime(icon, item)

    def _show_prefix_dialog(self):
        """Mostra diálogo de prefixo"""
        self.prefix_dialog.show()

    def _show_settings_dialog(self):
        """Mostra diálogo de configurações avançadas"""
        self.settings_dialog.set_current_settings(self.settings_manager.get_all())
        self.settings_dialog.show()

    def _show_search_dialog_wrapper(self, icon=None, item=None):
        """
        Wrapper para usar handler de show_search.
        """
        handler = self.callback_registry.get("show_search")
        if not handler:
            logging.error("show_search handler not found in registry")
            return
        handler.handle(icon=icon, item=item)

    def _quit_app_wrapper(self, icon=None, item=None):
        """
        Wrapper para usar handler de quit.
        Mantém compatibilidade com menu_builder enquanto migra para handlers.
        """
        handler = self.callback_registry.get("quit_app")
        if handler:
            handler.handle(icon=icon, item=item)
        else:
            self._quit_app(icon, item)

    def _on_add_custom_shortcut_wrapper(
        self, hotkey: str, prefix: str, description: str = "", enabled: bool = True
    ):
        """Wrapper para adicionar custom shortcut E REGISTRAR IMEDIATAMENTE"""
        try:
            success, msg, new_id = self.settings_manager.add_custom_shortcut(
                hotkey, prefix, description, enabled
            )

            if success and enabled and new_id is not None:
                shortcut = {
                    "id": new_id,
                    "hotkey": hotkey,
                    "prefix": prefix,
                    "enabled": enabled,
                }

                results = self.hotkey_manager.setup_custom_hotkeys([shortcut])

                if results.get(new_id) == "ok":
                    def make_callback(p):
                        return lambda: self._on_custom_shortcut_triggered(p)

                    self.hotkey_manager.set_custom_shortcut_callback(
                        new_id, make_callback(prefix)
                    )
                    logging.info(
                        f"✓ Atalho registrado em tempo real: [{hotkey.upper()}] → {prefix}"
                    )
                else:
                    logging.warning(
                        f"✗ Falha ao registrar atalho: {results.get(new_id)}"
                    )

            return success, msg, new_id
        except Exception as e:
            logging.error(f"Erro ao adicionar shortcut: {e}")
            return False, f"Erro: {e}", None

    def _on_update_custom_shortcut_wrapper(
        self,
        shortcut_id: int,
        hotkey: Optional[str] = None,
        prefix: Optional[str] = None,
        description: Optional[str] = None,
        enabled: Optional[bool] = None,
    ):
        """Wrapper para atualizar custom shortcut E RE-REGISTRAR"""
        try:
            success, msg = self.settings_manager.update_custom_shortcut(
                shortcut_id,
                hotkey=hotkey,
                prefix=prefix,
                description=description,
                enabled=enabled,
            )

            if success:
                self.hotkey_manager.unregister_custom_shortcut(shortcut_id)

                updated_shortcuts = [
                    s
                    for s in self.settings_manager.get_custom_shortcuts()
                    if s["id"] == shortcut_id
                ]

                if updated_shortcuts and updated_shortcuts[0].get("enabled", True):
                    shortcut = updated_shortcuts[0]

                    results = self.hotkey_manager.setup_custom_hotkeys([shortcut])

                    if results.get(shortcut_id) == "ok":
                        def make_callback(p):
                            return lambda: self._on_custom_shortcut_triggered(p)

                        self.hotkey_manager.set_custom_shortcut_callback(
                            shortcut_id, make_callback(shortcut["prefix"])
                        )
                        logging.info(
                            f"✓ Atalho atualizado em tempo real: ID={shortcut_id}"
                        )

            return success, msg
        except Exception as e:
            logging.error(f"Erro ao atualizar shortcut: {e}")
            return False, f"Erro: {e}"

    def _on_remove_custom_shortcut_wrapper(self, shortcut_id: int):
        """Wrapper para remover custom shortcut E DESREGISTRAR"""
        try:
            self.hotkey_manager.unregister_custom_shortcut(shortcut_id)

            success, msg = self.settings_manager.remove_custom_shortcut(shortcut_id)

            if success:
                logging.info(f"✓ Atalho removido e desregistrado: ID={shortcut_id}")

            return success, msg
        except Exception as e:
            logging.error(f"Erro ao remover shortcut: {e}")
            return False, f"Erro: {e}"

    def _show_custom_shortcuts_dialog(self):
        """Mostra diálogo de configurações com UI moderna (CustomTkinter)"""
        def _open():
            self.modern_settings_dialog.set_current_settings(self.settings_manager.get_all())
            self.modern_settings_dialog.show()

        self._run_on_ui_thread(_open)

    def _refresh_menu_action(self, icon, item):
        """Atualiza o menu manualmente"""
        try:
            logging.info("Atualização manual do menu solicitada")
            self._update_menu()
            self.notification_manager.show_toast(
                "Dahora App", "Menu atualizado! Feche e abra novamente para ver."
            )
        except Exception as e:
            logging.warning(f"Erro ao atualizar menu: {e}")

    def _copy_from_history(self, text: str):
        """Copia item do histórico"""
        self.clipboard_manager.copy_text(text)
        count = self.counter.increment()
        self.notification_manager.show_toast(
            "Dahora App", f"Copiado do histórico!\n{text}\nTotal: {count}ª vez"
        )

    def _clear_history(self, icon=None, item=None):
        """Limpa histórico"""
        total = self.clipboard_manager.clear_history()
        self.notification_manager.show_toast(
            "Dahora App", f"Histórico limpo!\n{total} itens removidos"
        )
        self._update_menu()

    def _show_about(self, icon, item):
        """Mostra janela Sobre (UI Moderna)"""
        self._run_on_ui_thread(lambda: self.modern_about_dialog.show())

    def _ensure_ui_root(self):
        """
        Garante um único CTk root rodando no main thread.
        Thread-safe usando Lock para prevenir race conditions.
        """
        with self._ui_lock:
            if self._ui_root is not None:
                return

            import customtkinter as ctk
            from dahora_app.ui.modern_styles import ModernTheme

            ModernTheme.setup()
            self._ui_root = ctk.CTk()
            self._ui_root.withdraw()
            self._ui_root.title("Dahora App")
            try:
                self._ui_root.iconbitmap("icon.ico")
            except Exception:
                pass

            try:
                self.modern_settings_dialog.set_parent(self._ui_root)
            except Exception:
                pass
            try:
                self.modern_search_dialog.set_parent(self._ui_root)
            except Exception:
                pass
            try:
                self.modern_about_dialog.set_parent(self._ui_root)
            except Exception:
                pass

    def _prewarm_ui(self) -> None:
        """Constrói as janelas em idle (ocultas) para abertura instantânea depois."""
        total_start = time.perf_counter()
        logging.info("[UI] Prewarm início")

        def _prewarm_about() -> None:
            about_start = time.perf_counter()
            logging.info("[UI] Prewarm About início")
            try:
                if getattr(self.modern_about_dialog, "window", None) is None:
                    self.modern_about_dialog._create_window()
                    try:
                        self.modern_about_dialog.window.withdraw()
                    except Exception:
                        pass
                about_ms = (time.perf_counter() - about_start) * 1000
                logging.info(f"[UI] Prewarm About fim em {about_ms:.1f}ms")
            except Exception as e:
                about_ms = (time.perf_counter() - about_start) * 1000
                logging.warning(f"Falha ao pré-aquecer Sobre: {e}")
                logging.info(f"[UI] Prewarm About falhou em {about_ms:.1f}ms")
            total_ms = (time.perf_counter() - total_start) * 1000
            logging.info(f"[UI] Prewarm fim total em {total_ms:.1f}ms")

        def _prewarm_search() -> None:
            search_start = time.perf_counter()
            logging.info("[UI] Prewarm Search início")
            try:
                if getattr(self.modern_search_dialog, "window", None) is None:
                    self.modern_search_dialog._create_window()
                    try:
                        self.modern_search_dialog.window.withdraw()
                    except Exception:
                        pass
                search_ms = (time.perf_counter() - search_start) * 1000
                logging.info(f"[UI] Prewarm Search fim em {search_ms:.1f}ms")
            except Exception as e:
                search_ms = (time.perf_counter() - search_start) * 1000
                logging.warning(f"Falha ao pré-aquecer Busca: {e}")
                logging.info(f"[UI] Prewarm Search falhou em {search_ms:.1f}ms")
            try:
                if self._ui_root is not None:
                    self._ui_root.after(0, _prewarm_about)
                else:
                    _prewarm_about()
            except Exception:
                _prewarm_about()

        settings_start = time.perf_counter()
        logging.info("[UI] Prewarm Settings início")
        try:
            self.modern_settings_dialog.set_current_settings(self.settings_manager.get_all())
            if getattr(self.modern_settings_dialog, "window", None) is None:
                self.modern_settings_dialog._create_window()
                try:
                    self.modern_settings_dialog.window.withdraw()
                except Exception:
                    pass
            settings_ms = (time.perf_counter() - settings_start) * 1000
            logging.info(f"[UI] Prewarm Settings fim em {settings_ms:.1f}ms")
        except Exception as e:
            settings_ms = (time.perf_counter() - settings_start) * 1000
            logging.warning(f"Falha ao pré-aquecer Configurações: {e}")
            logging.info(f"[UI] Prewarm Settings falhou em {settings_ms:.1f}ms")

        try:
            if self._ui_root is not None:
                self._ui_root.after(0, _prewarm_search)
            else:
                _prewarm_search()
        except Exception:
            _prewarm_search()

    def _run_on_ui_thread(self, fn):
        """Agenda uma ação no loop Tk (thread-safe)."""
        if self._ui_root is None:
            try:
                self._ensure_ui_root()
            except Exception as e:
                logging.error(f"Falha ao inicializar UI root: {e}")
                return

        try:
            self._ui_root.after(0, fn)
        except Exception as e:
            logging.error(f"Falha ao agendar UI action: {e}")

    def _toggle_pause(self, icon=None, item=None):
        """Alterna estado de pausa"""
        self.clipboard_manager.toggle_pause()
        is_paused = self.clipboard_manager.paused

        logging.info(f"Alternando ícone. Pausado: {is_paused}")
        try:
            new_icon = IconManager.get_icon_for_tray(is_paused=is_paused)
            target_icon = icon or self.icon
            if target_icon:
                target_icon.icon = new_icon
                try:
                    target_icon.visible = False
                    target_icon.visible = True
                except Exception:
                    pass
        except Exception as e:
            logging.warning(f"Falha ao atualizar ícone do tray: {e}")

        msg = (
            "Monitoramento de clipboard PAUSADO"
            if is_paused
            else "Monitoramento de clipboard RETOMADO"
        )
        logging.info(f"Estado alterado para: {'PAUSADO' if is_paused else 'RETOMADO'}")
        self.notification_manager.show_toast("Dahora App", msg)

    def _quit_app(self, icon, item):
        """Encerra o aplicativo"""
        if not self._sync_manager.request_shutdown():
            return

        try:
            logging.info("Encerrando Dahora App...")
        except Exception:
            pass

        try:
            if icon:
                try:
                    icon.visible = False
                except Exception as e:
                    logging.debug(f"Falha ao ocultar ícone: {e}", exc_info=False)
                icon.stop()
        except Exception as e:
            logging.warning(
                f"Falha ao parar ícone do tray no shutdown: {e}", exc_info=False
            )

        try:
            if self._ui_root is not None:
                self._ui_root.after(0, self._ui_root.quit)
                self._ui_root.after(50, self._ui_root.destroy)
        except Exception as e:
            try:
                logging.error(f"Falha ao encerrar UI root: {e}")
            except Exception:
                pass

    def _update_menu(self):
        """Atualiza o menu do ícone"""
        try:
            if self.icon:
                logging.info("Atualizando menu dinamicamente")
                self.icon.menu = self.menu_builder.create_dynamic_menu()
                logging.info("Menu atualizado com sucesso")
        except Exception as e:
            logging.warning(f"Erro ao atualizar menu: {e}")

    def show_privacy_notice(self):
        """Mostra aviso de privacidade na primeira execução"""
        if os.path.exists(PRIVACY_MARKER_FILE):
            return

        message = (
            "AVISO DE PRIVACIDADE\n\n"
            "O Dahora App mantém um histórico local dos últimos 100 itens "
            "copiados para a área de transferência.\n\n"
            "⚠️ Este histórico pode conter informações sensíveis "
            "(senhas, tokens, etc.)\n\n"
            "Os dados são armazenados LOCALMENTE em:\n"
            f"{DATA_DIR}\n\n"
            "Não há coleta de dados ou telemetria.\n\n"
            "Você pode limpar o histórico a qualquer momento pelo menu."
        )

        self.notification_manager.show_toast(
            "Dahora App - Privacidade", message, duration=15
        )
        logging.info("Aviso de privacidade exibido (primeira execução)")

        try:
            from datetime import datetime

            with open(PRIVACY_MARKER_FILE, "w", encoding="utf-8") as f:
                f.write(datetime.now().isoformat())
        except Exception as e:
            logging.warning(f"Falha ao marcar aviso de privacidade: {e}")

    def check_single_instance(self):
        """Verifica se já existe uma instância rodando usando SingleInstanceManager"""
        is_first, msg = initialize_single_instance("DahoraApp")

        if not is_first:
            notification_thread = threading.Thread(
                target=self.notification_manager.show_toast,
                args=(
                    "Dahora App Já em Execução",
                    "O Dahora App já está rodando na bandeja do sistema!",
                ),
                daemon=False,
            )
            notification_thread.start()
            notification_thread.join(timeout=3.0)
            logging.warning(f"[SingleInstance] {msg}")
        else:
            logging.info(f"[SingleInstance] {msg}")

        return is_first

    def setup_icon(self):
        """Configura o ícone da bandeja"""
        icon_image = IconManager.get_icon_for_tray()

        self.icon = pystray.Icon(
            "Dahora App", icon_image, APP_TITLE, menu=self.menu_builder.create_dynamic_menu()
        )

        global global_icon
        global_icon = self.icon
        self.notification_manager.set_icon(self.icon)

        return self.icon

    def run(self):
        """Executa a aplicação"""
        if not self.check_single_instance():
            sys.exit(0)

        try:
            self.initialize()

            hotkey_thread = threading.Thread(
                target=self.hotkey_manager.setup_all, daemon=True
            )
            hotkey_thread.start()
            logging.info("Thread de hotkey iniciada")

            monitor_thread = threading.Thread(
                target=self.clipboard_manager.monitor_clipboard_smart, daemon=True
            )
            monitor_thread.start()
            logging.info("Thread de monitoramento de clipboard iniciada")

            self.setup_icon()

            self._ensure_ui_root()

            try:
                self._ui_root.after(
                    int(self.settings_manager.ui_prewarm_delay_ms), self._prewarm_ui
                )
            except Exception as e:
                logging.warning(
                    f"Falha ao agendar pré-aquecimento da UI: {e}", exc_info=False
                )

            total_history = self.clipboard_manager.get_history_size()
            prefix = self.settings_manager.get_prefix() or "(vazio)"
            count = self.counter.get_count()

            print(
                f">>> App iniciado! Counter: {count}, Histórico: {total_history}, Prefixo: {prefix}"
            )

            custom_count = len(self.settings_manager.get_custom_shortcuts())
            if custom_count > 0:
                shortcuts_msg = f"Atalhos configurados: {custom_count}"
            else:
                shortcuts_msg = "Configure seus atalhos em: Configurações → Prefixos"

            self.notification_manager.show_toast(
                "Dahora App",
                f"App iniciado com sucesso!\n\n"
                f"{shortcuts_msg}\n"
                f"Prefixo padrão: {prefix}\n"
                f"Menu: clique direito no ícone\n\n"
                f"Já acionado {count} vezes • Histórico: {total_history} itens",
            )

            print(">>> Iniciando ícone da bandeja...")
            try:
                self._tray_thread = threading.Thread(
                    target=self.icon.run, daemon=True
                )
                self._tray_thread.start()
                logging.info("Thread do tray (pystray) iniciada")
            except Exception as e:
                logging.error(f"Falha ao iniciar thread do tray: {e}")

            self._ui_root.mainloop()
            print(">>> Loop de UI finalizado")

        except KeyboardInterrupt:
            print("Dahora App encerrado pelo usuário")
        except Exception as e:
            import traceback

            logging.error("Erro inesperado:\n" + traceback.format_exc())
            self.notification_manager.show_fatal_error(
                "Dahora App - Erro",
                f"Ocorreu um erro inesperado:\n{e}\n\nConsulte o log em: {LOG_FILE}",
            )
        finally:
            try:
                logging.info("Limpando recursos...")
                cleanup_single_instance()
                self.hotkey_manager.cleanup()
                try:
                    if self.icon:
                        self.icon.stop()
                except Exception:
                    pass
                print("Recursos liberados com sucesso")
            except Exception as e:
                logging.error(f"Erro ao limpar recursos: {e}")
            finally:
                logging.info("Dahora App encerrado completamente")

    def shutdown(self):
        """
        Encerra a aplicação e limpa recursos.
        Usado pelo context manager pattern.
        """
        try:
            logging.info("Limpando recursos...")
            cleanup_single_instance()
            self.hotkey_manager.cleanup()
            try:
                if self.icon:
                    self.icon.stop()
            except Exception:
                pass
            logging.info("Recursos liberados com sucesso")
        except Exception as e:
            logging.error(f"Erro ao limpar recursos: {e}")
        finally:
            logging.info("Dahora App encerrado completamente")

    def __enter__(self):
        """Context manager entry point"""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        self.shutdown()
        return False
