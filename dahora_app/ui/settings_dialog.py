"""
Janela de Configurações Avançadas do Dahora App
"""
import logging
import threading
from typing import Optional, Callable, Any
from dahora_app.ui.styles import Windows11Style
from dahora_app.ui.icon_manager import IconManager

# Import opcional de tkinter
try:
    import tkinter as tk
    from tkinter import ttk, font as tkFont, messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class SettingsDialog:
    """Janela de configurações avançadas com abas"""
    
    def __init__(self, notification_callback: Optional[Callable] = None):
        """
        Inicializa o diálogo de configurações
        
        Args:
            notification_callback: Callback para mostrar notificações
        """
        self.notification_callback = notification_callback
        self.on_save_callback: Optional[Callable] = None
        
        # Valores atuais (serão preenchidos externamente)
        self.current_settings: dict[str, Any] = {}
    
    def set_current_settings(self, settings: dict) -> None:
        """Define as configurações atuais"""
        self.current_settings = settings
    
    def set_on_save_callback(self, callback: Callable) -> None:
        """Define callback para quando salvar"""
        self.on_save_callback = callback
    
    def show(self) -> None:
        """Mostra o diálogo de configurações"""
        logging.info("show_settings_dialog() chamada - Iniciando janela de configurações")
        
        if not TKINTER_AVAILABLE:
            logging.error("Tkinter não disponível")
            if self.notification_callback:
                self.notification_callback("Dahora App", "Tkinter não disponível. Não é possível abrir configurações.")
            return
        
        # Executa em thread separada
        thread = threading.Thread(target=self._show_dialog_thread, daemon=True)
        thread.start()
        logging.info("Thread da janela de configurações iniciada")
    
    def _show_dialog_thread(self) -> None:
        """Thread para mostrar o diálogo"""
        try:
            logging.info("Criando janela de configurações com abas (Tkinter)")
            
            # Janela principal
            root = tk.Tk()
            # Configura estilo Windows 11 (Dark Mode)
            Windows11Style.configure_window(root, "Dahora App - Configurações", "480x350")
            try:
                root.iconbitmap(IconManager.resolve_icon_path())
            except Exception as e:
                logging.warning(f"Não foi possível definir ícone da janela: {e}")
            Windows11Style.configure_styles(root)
            
            # Fonte preferida
            def get_available_font():
                try:
                    available_fonts = tkFont.families()
                    preferred_fonts = ["Segoe UI", "Segoe UI Variable", "Arial", "Tahoma", "Microsoft Sans Serif"]
                    for f in preferred_fonts:
                        if f in available_fonts:
                            return f
                    return "TkDefaultFont"
                except Exception:
                    return "TkDefaultFont"
            
            default_font = get_available_font()
            
            # Frame principal
            main = ttk.Frame(root, padding=(16, 12, 16, 12))
            main.pack(fill=tk.BOTH, expand=True)
            
            # Cabeçalho
            ttk.Label(
                main,
                text="Configurações Avançadas",
                font=(default_font, 12, "bold")
            ).pack(anchor=tk.W, pady=(0, 8))
            
            # Notebook (abas)
            notebook = ttk.Notebook(main)
            notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
            
            # === ABA 1: GERAL ===
            tab_general = ttk.Frame(notebook, padding=16, style="Card.TFrame")
            notebook.add(tab_general, text="Geral")
            
            # Prefixo
            frame_prefix = ttk.Frame(tab_general)
            frame_prefix.pack(fill=tk.X, pady=5)
            ttk.Label(frame_prefix, text="Prefixo de Data/Hora:", font=(default_font, 9), style="Card.TLabel").pack(anchor=tk.W)
            var_prefix = tk.StringVar(value=self.current_settings.get("prefix", ""))
            ttk.Entry(frame_prefix, textvariable=var_prefix, width=40).pack(anchor=tk.W, pady=(2, 0))
            ttk.Label(frame_prefix, text="Ex: [trabalho] (opcional)", font=(default_font, 8), foreground="gray", style="Card.TLabel").pack(anchor=tk.W)

            # Formato de data/hora
            frame_format = ttk.Frame(tab_general)
            frame_format.pack(fill=tk.X, pady=10)
            ttk.Label(frame_format, text="Formato de Data/Hora:", font=(default_font, 9), style="Card.TLabel").pack(anchor=tk.W)
            var_datetime_format = tk.StringVar(value=self.current_settings.get("datetime_format", "%d.%m.%Y-%H:%M"))
            ttk.Entry(frame_format, textvariable=var_datetime_format, width=40).pack(anchor=tk.W, pady=(2, 0))
            ttk.Label(frame_format, text="Exemplo: %d.%m.%Y-%H:%M", font=(default_font, 8), foreground="gray", style="Card.TLabel").pack(anchor=tk.W)
            
            # === ABA 2: HISTÓRICO ===
            tab_history = ttk.Frame(notebook, padding=16, style="Card.TFrame")
            notebook.add(tab_history, text="Histórico")
            
            # Máximo de itens
            frame_max = ttk.Frame(tab_history)
            frame_max.pack(fill=tk.X, pady=5)
            ttk.Label(frame_max, text="Máximo de itens no histórico:", font=(default_font, 9), style="Card.TLabel").pack(side=tk.LEFT)
            var_max_history = tk.IntVar(value=self.current_settings.get("max_history_items", 100))
            ttk.Spinbox(frame_max, from_=10, to=1000, textvariable=var_max_history, width=10).pack(side=tk.RIGHT)
            
            # Intervalo de monitoramento
            frame_interval = ttk.Frame(tab_history)
            frame_interval.pack(fill=tk.X, pady=5)
            ttk.Label(frame_interval, text="Intervalo de verificação (s):", font=(default_font, 9), style="Card.TLabel").pack(side=tk.LEFT)
            var_monitor_interval = tk.DoubleVar(value=self.current_settings.get("clipboard_monitor_interval", 3))
            ttk.Spinbox(frame_interval, from_=0.5, to=60, increment=0.5, textvariable=var_monitor_interval, width=10).pack(side=tk.RIGHT)
            
            # Threshold de ociosidade
            frame_idle = ttk.Frame(tab_history)
            frame_idle.pack(fill=tk.X, pady=5)
            ttk.Label(frame_idle, text="Tempo ocioso para intervalo maior (s):", font=(default_font, 9), style="Card.TLabel").pack(side=tk.LEFT)
            var_idle_threshold = tk.DoubleVar(value=self.current_settings.get("clipboard_idle_threshold", 30))
            ttk.Spinbox(frame_idle, from_=5, to=300, increment=5, textvariable=var_idle_threshold, width=10).pack(side=tk.RIGHT)
            
            # === ABA 3: NOTIFICAÇÕES ===
            tab_notifications = ttk.Frame(notebook, padding=16, style="Card.TFrame")
            notebook.add(tab_notifications, text="Notificações")
            
            # Habilitar notificações
            var_notifications_enabled = tk.BooleanVar(value=self.current_settings.get("notification_enabled", True))
            ttk.Checkbutton(tab_notifications, text="Habilitar notificações", variable=var_notifications_enabled, style="Card.TCheckbutton").pack(anchor=tk.W, pady=10)
            
            # Duração da notificação
            frame_duration = ttk.Frame(tab_notifications)
            frame_duration.pack(fill=tk.X, pady=5)
            ttk.Label(frame_duration, text="Duração da notificação (segundos):", font=(default_font, 9), style="Card.TLabel").pack(side=tk.LEFT)
            var_notification_duration = tk.IntVar(value=self.current_settings.get("notification_duration", 2))
            ttk.Spinbox(frame_duration, from_=1, to=15, textvariable=var_notification_duration, width=10).pack(side=tk.RIGHT)
            
            # === ABA 4: ATALHOS ===
            tab_hotkeys = ttk.Frame(notebook, padding=16, style="Card.TFrame")
            notebook.add(tab_hotkeys, text="Atalhos")
            
            # Hotkey copiar data/hora
            frame_copy = ttk.Frame(tab_hotkeys)
            frame_copy.pack(fill=tk.X, pady=5)
            ttk.Label(frame_copy, text="Copiar Data/Hora:", font=(default_font, 9), style="Card.TLabel").pack(anchor=tk.W)
            var_hotkey_copy = tk.StringVar(value=self.current_settings.get("hotkey_copy_datetime", "ctrl+shift+q"))
            ttk.Entry(frame_copy, textvariable=var_hotkey_copy, width=30).pack(anchor=tk.W, pady=(2, 0))
            ttk.Label(frame_copy, text="Ex: ctrl+shift+q", font=(default_font, 8), foreground="gray", style="Card.TLabel").pack(anchor=tk.W)
            
            # Hotkey refresh menu
            frame_refresh = ttk.Frame(tab_hotkeys)
            frame_refresh.pack(fill=tk.X, pady=10)
            ttk.Label(frame_refresh, text="Atualizar Menu:", font=(default_font, 9), style="Card.TLabel").pack(anchor=tk.W)
            var_hotkey_refresh = tk.StringVar(value=self.current_settings.get("hotkey_refresh_menu", "ctrl+shift+r"))
            ttk.Entry(frame_refresh, textvariable=var_hotkey_refresh, width=30).pack(anchor=tk.W, pady=(2, 0))
            
            # Hotkeys agora aplicam sem reinicialização (o app re-registra automaticamente)
            ttk.Label(tab_hotkeys, text="✅ Alterações em atalhos são aplicadas automaticamente", font=(default_font, 8), foreground="gray", style="Card.TLabel").pack(anchor=tk.W, pady=(5, 0))
            
            # Separador
            ttk.Separator(tab_hotkeys, orient='horizontal').pack(fill=tk.X, pady=15)
            
            # Custom Shortcuts
            ttk.Label(tab_hotkeys, text="Atalhos Personalizados:", font=(default_font, 10, "bold"), style="Card.TLabel").pack(anchor=tk.W)
            ttk.Label(tab_hotkeys, text="Configure múltiplos atalhos com prefixos diferentes", font=(default_font, 8), foreground="gray", style="Card.TLabel").pack(anchor=tk.W, pady=(0, 10))
            
            def on_manage_shortcuts():
                """Abre o gerenciador de atalhos personalizados"""
                try:
                    # Fecha a janela de configurações primeiro
                    root.destroy()
                    
                    # Importa e chama a função global que abre o gerenciador
                    # (será tratado pelo main.py)
                    if self.notification_callback:
                        self.notification_callback("Dahora App", 
                            "Para abrir o gerenciador de atalhos personalizados:\n\n"
                            "1. Reinicie o aplicativo\n"
                            "2. Use o menu: Configurações → Atalhos\n"
                            "3. Clique em 'Gerenciar Atalhos Personalizados'\n\n"
                            "OU adicione atalhos manualmente editando o arquivo settings.json")
                except Exception as e:
                    logging.error(f"Erro ao abrir gerenciador de shortcuts: {e}")
            
            ttk.Button(tab_hotkeys, text="⚙️ Gerenciar Atalhos Personalizados", command=on_manage_shortcuts).pack(fill=tk.X, pady=5)
            
            # Ações
            def on_save():
                try:
                    new_settings = {
                        "prefix": var_prefix.get().strip(),
                        "datetime_format": var_datetime_format.get().strip(),
                        "max_history_items": var_max_history.get(),
                        "clipboard_monitor_interval": var_monitor_interval.get(),
                        "clipboard_idle_threshold": var_idle_threshold.get(),
                        "notification_enabled": var_notifications_enabled.get(),
                        "notification_duration": var_notification_duration.get(),
                        "hotkey_copy_datetime": var_hotkey_copy.get().strip(),
                        "hotkey_refresh_menu": var_hotkey_refresh.get().strip(),
                    }
                    
                    if self.on_save_callback:
                        self.on_save_callback(new_settings)
                    
                    if self.notification_callback:
                        self.notification_callback("Dahora App", "Configurações salvas com sucesso!")
                    
                    logging.info(f"Configurações salvas: {new_settings}")
                    root.destroy()
                except Exception as e:
                    logging.error(f"Erro ao salvar configurações: {e}")
                    messagebox.showerror("Erro", f"Erro ao salvar configurações:\n{e}")
            
            def on_cancel():
                root.destroy()
            
            def on_reset():
                if messagebox.askyesno("Confirmar", "Restaurar todas as configurações para os valores padrão?"):
                    var_prefix.set("")
                    var_datetime_format.set("%d.%m.%Y-%H:%M")
                    var_max_history.set(100)
                    var_monitor_interval.set(3)
                    var_idle_threshold.set(30)
                    var_notifications_enabled.set(True)
                    var_notification_duration.set(2)
                    var_hotkey_copy.set("ctrl+shift+q")
                    var_hotkey_refresh.set("ctrl+shift+r")
            
            # Botões
            buttons = ttk.Frame(main)
            buttons.pack(fill=tk.X, pady=(0, 0))
            ttk.Button(buttons, text="Restaurar Padrões", command=on_reset).pack(side=tk.LEFT)
            ttk.Button(buttons, text="Salvar", command=on_save).pack(side=tk.RIGHT)
            ttk.Button(buttons, text="Cancelar", command=on_cancel).pack(side=tk.RIGHT, padx=(0, 8))
            
            # Bind de teclas
            root.bind('<Escape>', lambda e: on_cancel())
            
            # Centraliza janela
            root.update_idletasks()
            # Centraliza janela
            root.update_idletasks()
            width = root.winfo_width()
            height = root.winfo_height()
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f'{width}x{height}+{x}+{y}')
            
            # Loop
            root.mainloop()
            logging.info("Janela de configurações fechada")
        
        except Exception as e:
            logging.error(f"Erro ao abrir janela de configurações: {e}")
            if self.notification_callback:
                self.notification_callback("Dahora App", f"Erro: {e}")
