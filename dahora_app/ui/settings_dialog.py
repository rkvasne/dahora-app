"""
Janela de Configurações Avançadas do Dahora App
"""
import logging
import threading
from typing import Optional, Callable

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
        self.current_settings = {}
    
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
            root.title("Dahora App - Configurações")
            root.resizable(False, False)
            root.focus_force()
            
            # Tema moderno
            try:
                style = ttk.Style()
                style.theme_use('vista')
            except Exception:
                style = ttk.Style()
            
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
            tab_general = ttk.Frame(notebook, padding=16)
            notebook.add(tab_general, text="Geral")
            
            # Prefixo
            ttk.Label(tab_general, text="Prefixo de Data/Hora:", font=(default_font, 9)).grid(row=0, column=0, sticky=tk.W, pady=4)
            var_prefix = tk.StringVar(value=self.current_settings.get("prefix", ""))
            entry_prefix = ttk.Entry(tab_general, textvariable=var_prefix, width=30)
            entry_prefix.grid(row=0, column=1, sticky=tk.W, pady=4, padx=(8, 0))
            
            # Formato de data/hora
            ttk.Label(tab_general, text="Formato de Data/Hora:", font=(default_font, 9)).grid(row=1, column=0, sticky=tk.W, pady=4)
            var_datetime_format = tk.StringVar(value=self.current_settings.get("datetime_format", "%d.%m.%Y-%H:%M"))
            entry_datetime_format = ttk.Entry(tab_general, textvariable=var_datetime_format, width=30)
            entry_datetime_format.grid(row=1, column=1, sticky=tk.W, pady=4, padx=(8, 0))
            ttk.Label(tab_general, text="Exemplo: %d.%m.%Y-%H:%M", font=(default_font, 8), foreground="gray").grid(row=2, column=1, sticky=tk.W, padx=(8, 0))
            
            # === ABA 2: HISTÓRICO ===
            tab_history = ttk.Frame(notebook, padding=16)
            notebook.add(tab_history, text="Histórico")
            
            # Máximo de itens
            ttk.Label(tab_history, text="Máximo de itens no histórico:", font=(default_font, 9)).grid(row=0, column=0, sticky=tk.W, pady=4)
            var_max_history = tk.IntVar(value=self.current_settings.get("max_history_items", 100))
            spin_max_history = ttk.Spinbox(tab_history, from_=10, to=1000, textvariable=var_max_history, width=10)
            spin_max_history.grid(row=0, column=1, sticky=tk.W, pady=4, padx=(8, 0))
            
            # Intervalo de monitoramento
            ttk.Label(tab_history, text="Intervalo de verificação (segundos):", font=(default_font, 9)).grid(row=1, column=0, sticky=tk.W, pady=4)
            var_monitor_interval = tk.DoubleVar(value=self.current_settings.get("clipboard_monitor_interval", 3))
            spin_monitor_interval = ttk.Spinbox(tab_history, from_=0.5, to=60, increment=0.5, textvariable=var_monitor_interval, width=10)
            spin_monitor_interval.grid(row=1, column=1, sticky=tk.W, pady=4, padx=(8, 0))
            
            # Threshold de ociosidade
            ttk.Label(tab_history, text="Tempo ocioso para intervalo maior (s):", font=(default_font, 9)).grid(row=2, column=0, sticky=tk.W, pady=4)
            var_idle_threshold = tk.DoubleVar(value=self.current_settings.get("clipboard_idle_threshold", 30))
            spin_idle_threshold = ttk.Spinbox(tab_history, from_=5, to=300, increment=5, textvariable=var_idle_threshold, width=10)
            spin_idle_threshold.grid(row=2, column=1, sticky=tk.W, pady=4, padx=(8, 0))
            
            # === ABA 3: NOTIFICAÇÕES ===
            tab_notifications = ttk.Frame(notebook, padding=16)
            notebook.add(tab_notifications, text="Notificações")
            
            # Habilitar notificações
            var_notifications_enabled = tk.BooleanVar(value=self.current_settings.get("notification_enabled", True))
            check_notifications = ttk.Checkbutton(tab_notifications, text="Habilitar notificações", variable=var_notifications_enabled)
            check_notifications.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=4)
            
            # Duração da notificação
            ttk.Label(tab_notifications, text="Duração da notificação (segundos):", font=(default_font, 9)).grid(row=1, column=0, sticky=tk.W, pady=4)
            var_notification_duration = tk.IntVar(value=self.current_settings.get("notification_duration", 2))
            spin_notification_duration = ttk.Spinbox(tab_notifications, from_=1, to=15, textvariable=var_notification_duration, width=10)
            spin_notification_duration.grid(row=1, column=1, sticky=tk.W, pady=4, padx=(8, 0))
            
            # === ABA 4: ATALHOS ===
            tab_hotkeys = ttk.Frame(notebook, padding=16)
            notebook.add(tab_hotkeys, text="Atalhos")
            
            # Hotkey copiar data/hora
            ttk.Label(tab_hotkeys, text="Copiar Data/Hora:", font=(default_font, 9)).grid(row=0, column=0, sticky=tk.W, pady=4)
            var_hotkey_copy = tk.StringVar(value=self.current_settings.get("hotkey_copy_datetime", "ctrl+shift+q"))
            entry_hotkey_copy = ttk.Entry(tab_hotkeys, textvariable=var_hotkey_copy, width=25)
            entry_hotkey_copy.grid(row=0, column=1, sticky=tk.W, pady=4, padx=(8, 0))
            ttk.Label(tab_hotkeys, text="Exemplo: ctrl+shift+q", font=(default_font, 8), foreground="gray").grid(row=1, column=1, sticky=tk.W, padx=(8, 0))
            
            # Hotkey refresh menu
            ttk.Label(tab_hotkeys, text="Atualizar Menu:", font=(default_font, 9)).grid(row=2, column=0, sticky=tk.W, pady=4)
            var_hotkey_refresh = tk.StringVar(value=self.current_settings.get("hotkey_refresh_menu", "ctrl+shift+r"))
            entry_hotkey_refresh = ttk.Entry(tab_hotkeys, textvariable=var_hotkey_refresh, width=25)
            entry_hotkey_refresh.grid(row=2, column=1, sticky=tk.W, pady=4, padx=(8, 0))
            
            # Aviso sobre atalhos
            ttk.Label(tab_hotkeys, text="⚠️ Alterar atalhos requer reiniciar o aplicativo", font=(default_font, 8), foreground="orange").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(12, 0))
            
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
            width = max(480, root.winfo_width())
            height = max(320, root.winfo_height())
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
