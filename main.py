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
        
        # Custom shortcuts dialog (agora com tabs completas)
        self.custom_shortcuts_dialog.set_current_settings(self.settings_manager.get_all())
        self.custom_shortcuts_dialog.set_on_add_callback(self._on_add_custom_shortcut_wrapper)  # Wrapper com log
        self.custom_shortcuts_dialog.set_on_update_callback(self.settings_manager.update_custom_shortcut)
        self.custom_shortcuts_dialog.set_on_remove_callback(self.settings_manager.remove_custom_shortcut)
        self.custom_shortcuts_dialog.set_on_validate_hotkey_callback(self.hotkey_manager.validate_hotkey)
        self.custom_shortcuts_dialog.set_on_save_callback(self._on_settings_saved)  # Para salvar configs gerais
        self.custom_shortcuts_dialog.on_get_settings_callback = self.settings_manager.get_all  # Para recarregar dados frescos
        self.custom_shortcuts_dialog.notification_callback = self.notification_manager.show_toast
        
        # Hotkeys
        self.hotkey_manager.set_copy_datetime_callback(lambda: self.copy_datetime(source="Atalho"))
        self.hotkey_manager.set_refresh_menu_callback(self._on_refresh_menu)
        self.hotkey_manager.set_search_callback(self._show_search_dialog)
        self.hotkey_manager.set_ctrl_c_callback(self._on_ctrl_c)
        
        # Menu builder callbacks
        self.menu_builder.set_copy_datetime_callback(self._copy_datetime_menu)
        self.menu_builder.set_show_search_callback(self._show_search_dialog)
        self.menu_builder.set_show_custom_shortcuts_callback(self._show_custom_shortcuts_dialog)  # Configurações unificadas
        self.menu_builder.set_refresh_menu_callback(self._refresh_menu_action)
        # Atualiza atalhos no menu
        self.menu_builder.hotkey_search_history = self.settings_manager.hotkey_search_history
        self.menu_builder.hotkey_refresh_menu = self.settings_manager.hotkey_refresh_menu
        self.menu_builder.set_get_recent_items_callback(self.clipboard_manager.get_recent_items)
        self.menu_builder.set_copy_from_history_callback(self._copy_from_history)
        self.menu_builder.set_clear_history_callback(self._clear_history)
        self.menu_builder.set_show_about_callback(self._show_about)
        self.menu_builder.set_quit_callback(self._quit_app)
    
    def _on_prefix_saved(self, prefix: str):
        """Callback quando prefixo é salvo"""
        self.settings_manager.set_prefix(prefix)
        self.datetime_formatter.set_prefix(prefix)
        self.prefix_dialog.set_prefix(prefix)
    
    def _on_settings_saved(self, settings: dict):
        """Callback quando configurações são salvas"""
        # Atualiza o settings_manager
        self.settings_manager.update_all(settings)
        
        # Sincroniza componentes que dependem das configurações
        self.datetime_formatter.set_prefix(settings.get("prefix", ""))
        self.datetime_formatter.set_brackets(
            settings.get("bracket_open", "["),
            settings.get("bracket_close", "]")
        )
        
        # Atualiza atalhos no menu builder
        self.menu_builder.hotkey_search_history = settings.get("hotkey_search_history", "ctrl+shift+f")
        self.menu_builder.hotkey_refresh_menu = settings.get("hotkey_refresh_menu", "ctrl+shift+r")
        
        # Avisa que algumas mudanças requerem restart
        needs_restart = False
        current_settings = self.settings_manager.get_all()
        
        # Verifica se hotkeys mudaram
        if (settings.get("hotkey_copy_datetime") != current_settings.get("hotkey_copy_datetime") or
            settings.get("hotkey_refresh_menu") != current_settings.get("hotkey_refresh_menu")):
            needs_restart = True
        
        if needs_restart:
            self.notification_manager.show_toast(
                "Dahora App", 
                "Configurações salvas!\n\n⚠️ Reinicie o aplicativo para aplicar mudanças em atalhos.",
                duration=5
            )
        else:
            self.notification_manager.show_toast("Dahora App", "Configurações salvas com sucesso!")
        
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
    
    def copy_datetime(self, icon=None, item=None, source=None):
        """Copia a data e hora para a área de transferência"""
        dt_string = self.datetime_formatter.format_now()
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
        """Mostra diálogo de busca no histórico"""
        self.search_dialog.show()
    
    def _on_add_custom_shortcut_wrapper(self, hotkey: str, prefix: str, description: str = "", enabled: bool = True):
        """Wrapper para adicionar custom shortcut"""
        try:
            return self.settings_manager.add_custom_shortcut(hotkey, prefix, description, enabled)
        except Exception as e:
            logging.error(f"Erro ao adicionar shortcut: {e}")
            return False, f"Erro: {e}", None
    
    def _show_custom_shortcuts_dialog(self):
        """Mostra diálogo de gerenciamento de custom shortcuts (NOVO)"""
        # Passa TODAS as configurações (agora tem tabs)
        self.custom_shortcuts_dialog.set_current_settings(self.settings_manager.get_all())
        self.custom_shortcuts_dialog.show()
    
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
        """Mostra janela Sobre (estilo Windows nativo)"""
        self.about_dialog.show()
    
    def _quit_app(self, icon, item):
        """Encerra o aplicativo"""
        try:
            logging.info("Encerrando Dahora App...")
            global mutex_handle
            if mutex_handle and WIN32_AVAILABLE:
                win32api.CloseHandle(mutex_handle)
            self.hotkey_manager.cleanup()
            if icon:
                icon.stop()
        except Exception as e:
            logging.error(f"Erro ao encerrar app: {e}")
        finally:
            sys.exit(0)
    
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
            
            # Inicia ícone (bloqueia até fechar)
            print(">>> Iniciando ícone da bandeja...")
            logging.info("Iniciando icon.run()")
            self.icon.run()
            print(">>> Ícone da bandeja finalizado")
        
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
