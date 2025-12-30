#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dahora App - Arquivo Principal
Sistema de Bandeja do Windows para copiar data/hora formatada
"""
import sys
import os
import logging
import threading
import pyperclip
import pystray
import keyboard
import time
from typing import Optional

# HACK: Forçar Dark Mode em menus nativos do Windows (Bandeja/Pystray)
# Isso usa APIs não documentadas do Windows para garantir que o menu de contexto
# siga o tema escuro, mesmo se o app não tiver manifesto.
# DEVE SER EXECUTADO ANTES DE QUALQUER OUTRA COISA DE UI
try:
    import ctypes
    uxtheme = ctypes.windll.uxtheme
    
    # Tenta SetPreferredAppMode (Ordinal 135) - Win 10 1903+ / Win 11
    # 2 = Force Dark Mode
    try:
        uxtheme[135](2)
    except:
        # Fallback: Tenta AllowDarkModeForApp (Ordinal 132) - Win 10 1809
        try:
            uxtheme[132](True)
        except:
            pass
except Exception:
    pass

# Configuração de encoding do console
try:
    import ctypes
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    ctypes.windll.kernel32.SetConsoleCP(65001)
except Exception:
    pass

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Imports do pacote dahora_app
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
from dahora_app.constants import (
    APP_TITLE,
    APP_VERSION,
    DATA_DIR,
    LOG_FILE,
    LOG_MAX_BYTES,
    LOG_BACKUP_COUNT,
    PRIVACY_MARKER_FILE
)

# Imports para verificação de instância única
try:
    import win32event
    import win32con
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# Configuração de logging
try:
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    )
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, logging.StreamHandler(sys.stdout)]
    )
    logging.info(f"Sistema de rotação de logs ativado ({LOG_MAX_BYTES/1024/1024}MB, {LOG_BACKUP_COUNT} backups)")
except Exception as e:
    logging.basicConfig(level=logging.INFO)
    logging.warning(f"Falha ao configurar rotação de logs: {e}")

# Variáveis globais
global_icon = None
mutex_handle = None


class DahoraApp:
    """Aplicação principal do Dahora App"""
    
    def __init__(self):
        """Inicializa a aplicação"""
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

        # Root UI (Tk) único: evita criar CTk() e mainloop() em callbacks do tray.
        self._ui_root = None
        self._shutdown_requested = False
        self._tray_thread: Optional[threading.Thread] = None
        self.about_dialog = AboutDialog()
        self.menu_builder = MenuBuilder()
        self.icon = None
    
    def initialize(self):
        """Inicializa todos os componentes"""
        logging.info("Inicializando Dahora App...")
        
        # Carrega dados persistentes
        self.counter.load()
        self.clipboard_manager.load_history()
        self.settings_manager.load()
        
        # Sincroniza prefixo e brackets
        self.datetime_formatter.set_prefix(self.settings_manager.get_prefix())
        self.datetime_formatter.set_brackets(
            self.settings_manager.bracket_open,
            self.settings_manager.bracket_close
        )
        
        # Configura callbacks
        self._setup_callbacks()
        
        # Configura custom shortcuts (NOVO)
        print(">>> Iniciando setup de custom shortcuts...")
        self._setup_custom_shortcuts()
        print(">>> Setup de custom shortcuts concluído")
        
        # Mostra aviso de privacidade
        self.show_privacy_notice()
        
        # Inicializa clipboard
        self.clipboard_manager.initialize_last_content()
        
        logging.info("Dahora App inicializado com sucesso")
    
    def _setup_callbacks(self):
        """Configura todos os callbacks entre componentes"""
        # Prefix dialog
        self.prefix_dialog.set_prefix(self.settings_manager.get_prefix())
        self.prefix_dialog.set_on_save_callback(self._on_prefix_saved)
        self.prefix_dialog.notification_callback = self.notification_manager.show_toast
        
        # Settings dialog
        self.settings_dialog.set_current_settings(self.settings_manager.get_all())
        self.settings_dialog.set_on_save_callback(self._on_settings_saved)
        self.settings_dialog.notification_callback = self.notification_manager.show_toast
        
        # Search dialog
        self.search_dialog.set_get_history_callback(lambda: self.clipboard_manager.clipboard_history)
        self.search_dialog.set_copy_callback(self._copy_from_history)
        self.search_dialog.notification_callback = self.notification_manager.show_toast
        
        # Modern search dialog (CustomTkinter)
        self.modern_search_dialog.set_get_history_callback(lambda: self.clipboard_manager.clipboard_history)
        self.modern_search_dialog.set_copy_callback(self._copy_from_history)
        self.modern_search_dialog.notification_callback = self.notification_manager.show_toast
        
        # Custom shortcuts dialog (agora com tabs completas)
        self.custom_shortcuts_dialog.set_current_settings(self.settings_manager.get_all())
        self.custom_shortcuts_dialog.set_on_add_callback(self._on_add_custom_shortcut_wrapper)  # Wrapper com registro imediato
        self.custom_shortcuts_dialog.set_on_update_callback(self._on_update_custom_shortcut_wrapper)  # Wrapper com re-registro
        self.custom_shortcuts_dialog.set_on_remove_callback(self._on_remove_custom_shortcut_wrapper)  # Wrapper com desregistro
        self.custom_shortcuts_dialog.set_on_validate_hotkey_callback(self.hotkey_manager.validate_hotkey)
        self.custom_shortcuts_dialog.set_on_save_callback(self._on_settings_saved)  # Para salvar configs gerais
        self.custom_shortcuts_dialog.on_get_settings_callback = self.settings_manager.get_all  # Para recarregar dados frescos
        self.custom_shortcuts_dialog.notification_callback = self.notification_manager.show_toast
        
        # Modern settings dialog (CustomTkinter - UI Moderna)
        self.modern_settings_dialog.set_current_settings(self.settings_manager.get_all())
        self.modern_settings_dialog.set_on_add_callback(self._on_add_custom_shortcut_wrapper)
        self.modern_settings_dialog.set_on_update_callback(self._on_update_custom_shortcut_wrapper)
        self.modern_settings_dialog.set_on_remove_callback(self._on_remove_custom_shortcut_wrapper)
        self.modern_settings_dialog.set_on_validate_hotkey_callback(self.hotkey_manager.validate_hotkey)
        self.modern_settings_dialog.set_on_save_callback(self._on_settings_saved)
        self.modern_settings_dialog.on_get_settings_callback = self.settings_manager.get_all
        self.modern_settings_dialog.notification_callback = self.notification_manager.show_toast
        
        # Hotkeys
        # Ctrl+Shift+Q: cola (paste) no cursor, preservando o clipboard
        self.hotkey_manager.set_copy_datetime_callback(self._on_copy_datetime_hotkey)
        self.hotkey_manager.set_refresh_menu_callback(self._on_refresh_menu)
        self.hotkey_manager.set_search_callback(self._show_search_dialog)
        self.hotkey_manager.set_ctrl_c_callback(self._on_ctrl_c)

        # Hotkeys configuráveis (usados pelo HotkeyManager.setup_all)
        self.hotkey_manager.set_configured_hotkeys(
            self.settings_manager.hotkey_copy_datetime,
            self.settings_manager.hotkey_search_history,
            self.settings_manager.hotkey_refresh_menu,
        )
        
        # Menu builder callbacks
        self.menu_builder.set_copy_datetime_callback(self._copy_datetime_menu)
        self.menu_builder.set_show_search_callback(self._show_search_dialog)
        self.menu_builder.set_show_custom_shortcuts_callback(self._show_custom_shortcuts_dialog)  # Configurações unificadas
        self.menu_builder.set_refresh_menu_callback(self._refresh_menu_action)
        # Atualiza atalhos no menu
        self.menu_builder.hotkey_copy_datetime = self.settings_manager.hotkey_copy_datetime
        self.menu_builder.hotkey_search_history = self.settings_manager.hotkey_search_history
        self.menu_builder.hotkey_refresh_menu = self.settings_manager.hotkey_refresh_menu
        self.menu_builder.set_get_recent_items_callback(self.clipboard_manager.get_recent_items)
        self.menu_builder.set_copy_from_history_callback(self._copy_from_history)
        self.menu_builder.set_clear_history_callback(self._clear_history)
        self.menu_builder.set_show_about_callback(self._show_about)
        self.menu_builder.set_toggle_pause_callback(self._toggle_pause)
        self.menu_builder.set_is_paused_callback(lambda: self.clipboard_manager.paused)
        self.menu_builder.set_quit_callback(self._quit_app)
    
    def _on_prefix_saved(self, prefix: str):
        """Callback quando prefixo é salvo"""
        self.settings_manager.set_prefix(prefix)
        self.datetime_formatter.set_prefix(prefix)
        self.prefix_dialog.set_prefix(prefix)
    
    def _on_settings_saved(self, settings: dict):
        """Callback quando configurações são salvas"""
        # Snapshot antes da atualização (para fallback de campos que uma UI não envia)
        previous_settings = self.settings_manager.get_all()

        # Atualiza o settings_manager
        self.settings_manager.update_all(settings)
        current_settings = self.settings_manager.get_all()
        
        # Sincroniza componentes que dependem das configurações
        self.datetime_formatter.set_prefix(settings.get("prefix", ""))
        self.datetime_formatter.set_brackets(
            settings.get("bracket_open", "["),
            settings.get("bracket_close", "]")
        )
        
        # Atualiza atalhos no menu builder
        self.menu_builder.hotkey_copy_datetime = current_settings.get("hotkey_copy_datetime", "ctrl+shift+q")
        self.menu_builder.hotkey_search_history = current_settings.get("hotkey_search_history", "ctrl+shift+f")
        self.menu_builder.hotkey_refresh_menu = current_settings.get("hotkey_refresh_menu", "ctrl+shift+r")

        # Aplica hotkeys imediatamente (sem precisar reiniciar)
        copy_hk = current_settings.get("hotkey_copy_datetime") or previous_settings.get("hotkey_copy_datetime")
        search_hk = current_settings.get("hotkey_search_history") or previous_settings.get("hotkey_search_history")
        refresh_hk = current_settings.get("hotkey_refresh_menu") or previous_settings.get("hotkey_refresh_menu")

        self.hotkey_manager.set_configured_hotkeys(copy_hk, search_hk, refresh_hk)
        hotkey_results = self.hotkey_manager.apply_configured_hotkeys()

        # Toast resumido (mostra erro apenas se algum falhou)
        errors = [v for v in hotkey_results.values() if isinstance(v, str) and v.startswith("erro")]
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
            logging.info(f"Ctrl+C detectado: {current_content[:50]}...")
    
    def _on_history_updated(self):
        """Callback quando o histórico do clipboard é atualizado"""
        # NOTA: pystray não permite atualização do menu quando já está aberto
        # O menu será atualizado na próxima vez que o usuário abrir
        # ou usar "Recarregar Itens" (Ctrl+Shift+R)
        pass
    
    def _setup_custom_shortcuts(self):
        """Configura custom shortcuts na inicialização (NOVO)"""
        try:
            logging.info("=== Iniciando configuração de custom shortcuts ===")
            
            # Obtém custom shortcuts habilitados
            custom_shortcuts = self.settings_manager.get_custom_shortcuts(enabled_only=True)
            
            if not custom_shortcuts:
                logging.info("Nenhum custom shortcut configurado - OK, pulando")
                return
            
            logging.info(f"Configurando {len(custom_shortcuts)} custom shortcuts...")
            
            # Registra hotkeys
            results = self.hotkey_manager.setup_custom_hotkeys(custom_shortcuts)
            
            # Define callbacks para cada shortcut
            for shortcut in custom_shortcuts:
                shortcut_id = shortcut["id"]
                prefix = shortcut["prefix"]
                
                # Cria callback com closure
                def make_callback(p):
                    return lambda: self._on_custom_shortcut_triggered(p)
                
                self.hotkey_manager.set_custom_shortcut_callback(shortcut_id, make_callback(prefix))
                
                # Log do resultado
                status = results.get(shortcut_id, "unknown")
                hotkey = shortcut.get("hotkey", "").upper()
                if status == "ok":
                    logging.info(f"✓ Custom shortcut OK: [{hotkey}] → {prefix}")
                else:
                    logging.warning(f"✗ Custom shortcut FALHOU: [{hotkey}] → {status}")
            
            # Notifica sucesso
            success_count = sum(1 for s in results.values() if s == "ok")
            if success_count > 0:
                logging.info(f"{success_count}/{len(custom_shortcuts)} custom shortcuts registrados com sucesso")
        
        except Exception as e:
            logging.error(f"Erro ao configurar custom shortcuts: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            # Continua a execução mesmo com erro
    
    def _on_custom_shortcut_triggered(self, prefix: str):
        """Callback quando custom shortcut é acionado (COLA DIRETAMENTE SEM AFETAR CLIPBOARD)"""
        try:
            # Formata com prefixo específico
            dt_string = self.datetime_formatter.format_with_prefix(prefix)
            
            # SALVA o clipboard atual (preserva o que o usuário tinha copiado)
            clipboard_backup = None
            try:
                clipboard_backup = pyperclip.paste()
            except Exception:
                pass
            
            # Copia temporariamente para poder colar
            pyperclip.copy(dt_string)
            time.sleep(0.05)  # Aguarda clipboard estar pronto
            
            # COLA AUTOMATICAMENTE onde o cursor está
            keyboard.send('ctrl+v')
            time.sleep(0.05)  # Aguarda a colagem completar
            
            # RESTAURA o clipboard original (usuário não perde o que tinha copiado)
            if clipboard_backup is not None:
                try:
                    pyperclip.copy(clipboard_backup)
                except Exception:
                    pass
            
            # NÃO adiciona timestamp ao histórico (desnecessário - sempre pode gerar novo)
            
            # Incrementa contador
            count = self.counter.increment()
            
            # Notificação desativada - o usuário já vê o texto colado na tela
            
            logging.info(f"Custom shortcut acionado: prefix='{prefix}', resultado={dt_string}, total={count}ª vez")
        
        except Exception as e:
            logging.error(f"Erro ao processar custom shortcut: {e}")
            self.notification_manager.show_toast("Erro no Atalho", f"Falha ao processar atalho: {e}")

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
        self.clipboard_manager.copy_text(dt_string)
        
        # NÃO adiciona timestamp ao histórico (desnecessário - sempre pode gerar novo)
        
        # Incrementa contador
        count = self.counter.increment()
        
        # Determina origem
        if item and hasattr(item, 'text'):
            source = "Menu: " + item.text
        else:
            source = source or ("Atalho" if icon else "Fallback")
        
        # Mostra notificação
        if source.startswith("Menu:"):
            self.notification_manager.show_toast("Dahora App", 
                f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {count}ª vez")
        else:
            dur = 1.5 if source == "Atalho" else 2
            try:
                if source == "Atalho":
                    self.notification_manager.show_quick_notification("Dahora App",
                        f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {count}ª vez", duration=dur)
                else:
                    self.notification_manager.show_toast("Dahora App",
                        f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {count}ª vez", duration=dur)
            except Exception:
                self.notification_manager.show_toast("Dahora App",
                    f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {count}ª vez", duration=dur)

    def _on_copy_datetime_hotkey(self) -> None:
        """Ctrl+Shift+Q: cola data/hora onde o cursor está, preservando clipboard."""
        try:
            dt_string = self._format_datetime_for_default_shortcut()

            clipboard_backup = None
            try:
                clipboard_backup = pyperclip.paste()
            except Exception:
                pass

            pyperclip.copy(dt_string)
            time.sleep(0.05)
            keyboard.send('ctrl+v')
            time.sleep(0.05)

            if clipboard_backup is not None:
                try:
                    pyperclip.copy(clipboard_backup)
                except Exception:
                    pass

            count = self.counter.increment()
            logging.info(f"Hotkey copiar/colar data/hora acionado: resultado={dt_string}, total={count}ª vez")
        except Exception as e:
            logging.error(f"Erro no hotkey_copy_datetime: {e}")
    
    def _copy_datetime_menu(self, icon, item):
        """Wrapper para copiar data/hora do menu"""
        self.copy_datetime(icon, item)
    
    def _show_prefix_dialog(self):
        """Mostra diálogo de prefixo"""
        self.prefix_dialog.show()
    
    def _show_settings_dialog(self):
        """Mostra diálogo de configurações avançadas"""
        # Atualiza configurações antes de mostrar
        self.settings_dialog.set_current_settings(self.settings_manager.get_all())
        self.settings_dialog.show()
    
    def _show_search_dialog(self):
        """Mostra diálogo de busca no histórico (UI Moderna)"""
        self._run_on_ui_thread(lambda: self.modern_search_dialog.show())
    
    def _on_add_custom_shortcut_wrapper(self, hotkey: str, prefix: str, description: str = "", enabled: bool = True):
        """Wrapper para adicionar custom shortcut E REGISTRAR IMEDIATAMENTE"""
        try:
            # Adiciona no settings
            success, msg, new_id = self.settings_manager.add_custom_shortcut(hotkey, prefix, description, enabled)
            
            if success and enabled and new_id is not None:
                # Registra o hotkey IMEDIATAMENTE
                shortcut = {
                    "id": new_id,
                    "hotkey": hotkey,
                    "prefix": prefix,
                    "enabled": enabled
                }
                
                # Registra no sistema de hotkeys
                results = self.hotkey_manager.setup_custom_hotkeys([shortcut])
                
                if results.get(new_id) == "ok":
                    # Define callback
                    def make_callback(p):
                        return lambda: self._on_custom_shortcut_triggered(p)
                    
                    self.hotkey_manager.set_custom_shortcut_callback(new_id, make_callback(prefix))
                    logging.info(f"✓ Atalho registrado em tempo real: [{hotkey.upper()}] → {prefix}")
                else:
                    logging.warning(f"✗ Falha ao registrar atalho: {results.get(new_id)}")
            
            return success, msg, new_id
        except Exception as e:
            logging.error(f"Erro ao adicionar shortcut: {e}")
            return False, f"Erro: {e}", None
    
    def _on_update_custom_shortcut_wrapper(self, shortcut_id: int, hotkey: Optional[str] = None,
                                          prefix: Optional[str] = None, description: Optional[str] = None,
                                          enabled: Optional[bool] = None):
        """Wrapper para atualizar custom shortcut E RE-REGISTRAR"""
        try:
            # Atualiza no settings
            success, msg = self.settings_manager.update_custom_shortcut(
                shortcut_id, hotkey=hotkey, prefix=prefix, description=description, enabled=enabled
            )
            
            if success:
                # Remove registro antigo
                self.hotkey_manager.unregister_custom_shortcut(shortcut_id)
                
                # Obtém shortcut atualizado
                updated_shortcuts = [s for s in self.settings_manager.get_custom_shortcuts() if s["id"] == shortcut_id]
                
                if updated_shortcuts and updated_shortcuts[0].get("enabled", True):
                    shortcut = updated_shortcuts[0]
                    
                    # Re-registra
                    results = self.hotkey_manager.setup_custom_hotkeys([shortcut])
                    
                    if results.get(shortcut_id) == "ok":
                        # Define callback
                        def make_callback(p):
                            return lambda: self._on_custom_shortcut_triggered(p)
                        
                        self.hotkey_manager.set_custom_shortcut_callback(shortcut_id, make_callback(shortcut["prefix"]))
                        logging.info(f"✓ Atalho atualizado em tempo real: ID={shortcut_id}")
            
            return success, msg
        except Exception as e:
            logging.error(f"Erro ao atualizar shortcut: {e}")
            return False, f"Erro: {e}"
    
    def _on_remove_custom_shortcut_wrapper(self, shortcut_id: int):
        """Wrapper para remover custom shortcut E DESREGISTRAR"""
        try:
            # Remove registro do hotkey PRIMEIRO
            self.hotkey_manager.unregister_custom_shortcut(shortcut_id)
            
            # Remove do settings
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
            self.notification_manager.show_toast("Dahora App", "Menu atualizado! Feche e abra novamente para ver.")
        except Exception as e:
            logging.warning(f"Erro ao atualizar menu: {e}")
    
    def _copy_from_history(self, text: str):
        """Copia item do histórico"""
        self.clipboard_manager.copy_text(text)
        count = self.counter.increment()
        self.notification_manager.show_toast("Dahora App", 
            f"Copiado do histórico!\n{text}\nTotal: {count}ª vez")
    
    def _clear_history(self, icon=None, item=None):
        """Limpa histórico"""
        total = self.clipboard_manager.clear_history()
        self.notification_manager.show_toast("Dahora App", 
            f"Histórico limpo!\n{total} itens removidos")
        self._update_menu()
    
    def _show_about(self, icon, item):
        """Mostra janela Sobre (UI Moderna)"""
        self._run_on_ui_thread(lambda: self.modern_about_dialog.show())

    def _ensure_ui_root(self):
        """Garante um único CTk root rodando no main thread."""
        if self._ui_root is not None:
            return

        import customtkinter as ctk
        from dahora_app.ui.modern_styles import ModernTheme

        ModernTheme.setup()
        self._ui_root = ctk.CTk()
        self._ui_root.withdraw()
        self._ui_root.title("Dahora App")
        try:
            self._ui_root.iconbitmap('icon.ico')
        except Exception:
            pass

        # Injeta o parent para os diálogos (toplevels)
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
        try:
            # Settings é a mais pesada (tabs + widgets)
            self.modern_settings_dialog.set_current_settings(self.settings_manager.get_all())
            # força criação sem mostrar
            if getattr(self.modern_settings_dialog, "window", None) is None:
                self.modern_settings_dialog._create_window()  # noqa: SLF001
                try:
                    self.modern_settings_dialog.window.withdraw()
                except Exception:
                    pass
        except Exception as e:
            logging.warning(f"Falha ao pré-aquecer Configurações: {e}")
            # Se criou parcialmente, destrói para evitar janela "quebrada" (abas faltando/scroll).
            try:
                w = getattr(self.modern_settings_dialog, "window", None)
                if w is not None:
                    try:
                        w.destroy()
                    except Exception:
                        pass
                self.modern_settings_dialog.window = None
            except Exception:
                pass

        # Search/About são leves, mas também podem ser pré-criadas
        try:
            if getattr(self.modern_search_dialog, "window", None) is None:
                self.modern_search_dialog._create_window()  # noqa: SLF001
                try:
                    self.modern_search_dialog.window.withdraw()
                except Exception:
                    pass
        except Exception as e:
            logging.warning(f"Falha ao pré-aquecer Busca: {e}")
            try:
                w = getattr(self.modern_search_dialog, "window", None)
                if w is not None:
                    try:
                        w.destroy()
                    except Exception:
                        pass
                self.modern_search_dialog.window = None
            except Exception:
                pass

        try:
            if getattr(self.modern_about_dialog, "window", None) is None:
                self.modern_about_dialog._create_window()  # noqa: SLF001
                try:
                    self.modern_about_dialog.window.withdraw()
                except Exception:
                    pass
        except Exception as e:
            logging.warning(f"Falha ao pré-aquecer Sobre: {e}")
            try:
                w = getattr(self.modern_about_dialog, "window", None)
                if w is not None:
                    try:
                        w.destroy()
                    except Exception:
                        pass
                self.modern_about_dialog.window = None
            except Exception:
                pass

    def _run_on_ui_thread(self, fn):
        """Agenda uma ação no loop Tk (thread-safe)."""
        # Se o UI root ainda não existe, cria agora.
        # Importante: isso só é chamado depois do run() iniciar.
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
        
        # Atualiza ícone
        logging.info(f"Alternando ícone. Pausado: {is_paused}")
        try:
            # IconManager é uma classe utilitária (não existe self.icon_manager)
            new_icon = IconManager.get_icon_for_tray(is_paused=is_paused)
            target_icon = icon or self.icon
            if target_icon:
                target_icon.icon = new_icon
                # Força atualização visual (algumas versões do pystray precisam disso)
                try:
                    target_icon.visible = False
                    target_icon.visible = True
                except Exception:
                    pass
        except Exception as e:
            logging.warning(f"Falha ao atualizar ícone do tray: {e}")
        
        status = "PAUSADO" if is_paused else "RETOMADO"
        msg = "Monitoramento de clipboard PAUSADO" if is_paused else "Monitoramento de clipboard RETOMADO"
        
        logging.info(f"Estado alterado para: {status}")
        self.notification_manager.show_toast("Dahora App", msg)  
    def _quit_app(self, icon, item):
        """Encerra o aplicativo"""
        # IMPORTANTE: esse callback roda no thread do pystray.
        # sys.exit() aqui NÃO encerra o processo; só encerra o thread.
        # Precisamos pedir para o main thread (Tk) encerrar o mainloop.
        if self._shutdown_requested:
            return
        self._shutdown_requested = True

        try:
            logging.info("Encerrando Dahora App...")
        except Exception:
            pass

        # Para o tray o quanto antes
        try:
            if icon:
                try:
                    icon.visible = False
                except Exception:
                    pass
                icon.stop()
        except Exception:
            pass

        # Encerra o loop Tk no main thread
        try:
            if self._ui_root is not None:
                self._ui_root.after(0, self._ui_root.quit)
                # destroy após sair do mainloop (pequeno delay é ok)
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
        
        self.notification_manager.show_toast("Dahora App - Privacidade", message, duration=15)
        logging.info("Aviso de privacidade exibido (primeira execução)")
        
        # Marca como aceito
        try:
            from datetime import datetime
            with open(PRIVACY_MARKER_FILE, 'w', encoding='utf-8') as f:
                f.write(datetime.now().isoformat())
        except Exception as e:
            logging.warning(f"Falha ao marcar aviso de privacidade: {e}")
    
    def check_single_instance(self):
        """Verifica se já existe uma instância rodando"""
        global mutex_handle
        
        if not WIN32_AVAILABLE:
            return True
        
        mutex_name = "Global\\DahoraAppSingleInstance"
        try:
            mutex_handle = win32event.CreateMutex(None, False, mutex_name)
            result = win32api.GetLastError()
            
            if result == 183:  # ERROR_ALREADY_EXISTS
                notification_thread = threading.Thread(
                    target=self.notification_manager.show_toast,
                    args=("Dahora App Já em Execução",
                          "O Dahora App já está rodando na bandeja do sistema!"),
                    daemon=False
                )
                notification_thread.start()
                notification_thread.join(timeout=3.0)
                return False
            
            return True
        except Exception as e:
            print(f"Erro na verificação de instância única: {e}")
            return True
    
    def setup_icon(self):
        """Configura o ícone da bandeja"""
        icon_image = IconManager.get_icon_for_tray()
        
        self.icon = pystray.Icon(
            "Dahora App",
            icon_image,
            APP_TITLE,
            menu=self.menu_builder.create_dynamic_menu()
        )
        
        # Atualiza referência global
        global global_icon
        global_icon = self.icon
        self.notification_manager.set_icon(self.icon)
        
        return self.icon
    
    def run(self):
        """Executa a aplicação"""
        # Verifica instância única
        if not self.check_single_instance():
            sys.exit(0)
        
        try:
            # Inicializa componentes
            self.initialize()
            
            # Configura hotkeys em thread separada
            hotkey_thread = threading.Thread(target=self.hotkey_manager.setup_all, daemon=True)
            hotkey_thread.start()
            logging.info("Thread de hotkey iniciada")
            
            # Inicia monitor de clipboard em thread separada
            monitor_thread = threading.Thread(
                target=self.clipboard_manager.monitor_clipboard_smart,
                daemon=True
            )
            monitor_thread.start()
            logging.info("Thread de monitoramento de clipboard iniciada")
            
            # Setup ícone
            self.setup_icon()

            # UI root único (Tk): as janelas modernas serão Toplevels desse root.
            self._ensure_ui_root()

            # Pré-aquece UI em background (depois que o app já subiu)
            try:
                self._ui_root.after(700, self._prewarm_ui)
            except Exception:
                pass
            
            # Mensagem de boas-vindas
            total_history = self.clipboard_manager.get_history_size()
            prefix = self.settings_manager.get_prefix() or '(vazio)'
            count = self.counter.get_count()
            
            print(f">>> App iniciado! Counter: {count}, Histórico: {total_history}, Prefixo: {prefix}")
            
            # Mensagem de inicialização
            custom_count = len(self.settings_manager.get_custom_shortcuts())
            if custom_count > 0:
                shortcuts_msg = f"Atalhos configurados: {custom_count}"
            else:
                shortcuts_msg = "Configure seus atalhos em: Configurações → Prefixos"
            
            self.notification_manager.show_toast("Dahora App",
                f"App iniciado com sucesso!\n\n"
                f"{shortcuts_msg}\n"
                f"Prefixo padrão: {prefix}\n"
                f"Menu: clique direito no ícone\n\n"
                f"Já acionado {count} vezes • Histórico: {total_history} itens")
            
            # Inicia ícone em thread daemon.
            # Isso evita que o processo fique preso caso o thread do tray não finalize corretamente.
            print(">>> Iniciando ícone da bandeja...")
            try:
                self._tray_thread = threading.Thread(target=self.icon.run, daemon=True)
                self._tray_thread.start()
                logging.info("Thread do tray (pystray) iniciada")
            except Exception as e:
                logging.error(f"Falha ao iniciar thread do tray: {e}")

            # Mantém o processo vivo e processa eventos de UI.
            # As janelas (Configurações/Busca/Sobre) são Toplevels e são abertas via after().
            self._ui_root.mainloop()
            print(">>> Loop de UI finalizado")
        
        except KeyboardInterrupt:
            print("Dahora App encerrado pelo usuário")
        except Exception as e:
            import traceback
            logging.error("Erro inesperado:\n" + traceback.format_exc())
            self.notification_manager.show_fatal_error("Dahora App - Erro",
                f"Ocorreu um erro inesperado:\n{e}\n\nConsulte o log em: {LOG_FILE}")
        finally:
            # Limpa recursos
            try:
                logging.info("Limpando recursos...")
                global mutex_handle
                if mutex_handle and WIN32_AVAILABLE:
                    win32api.CloseHandle(mutex_handle)
                    logging.info("Mutex liberado")
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


def main():
    """Função principal"""
    # Verifica se icon.ico existe
    if not os.path.exists('icon.ico'):
        print("[AVISO] Arquivo icon.ico não encontrado. O app usará ícone padrão.")
    
    # Cria e executa aplicação
    app = DahoraApp()
    app.run()


if __name__ == '__main__':
    main()
