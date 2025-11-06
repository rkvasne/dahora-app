"""
Gerenciador de Atalhos Personalizados - Dialog de Configurações com CRUD
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Callable, Optional, List, Dict, Any
from datetime import datetime
# Removido: from dahora_app.ui.styles import Windows11Style

# keyboard será importado apenas quando necessário (lazy import)


class CustomShortcutsDialog:
    """Dialog de configurações com tabs e CRUD de prefixos"""
    
    def __init__(self):
        """Inicializa o dialog"""
        self.window: Optional[tk.Tk] = None
        self.shortcuts_listbox: Optional[tk.Listbox] = None  # Listbox simples (como search_dialog)
        self.shortcuts_data: List[Dict[str, Any]] = []
        self.current_settings: Dict[str, Any] = {}  # Para armazenar todas as configs
        
        # Callbacks
        self.on_save_callback: Optional[Callable] = None
        self.on_add_callback: Optional[Callable] = None
        self.on_update_callback: Optional[Callable] = None
        self.on_remove_callback: Optional[Callable] = None
        self.on_validate_hotkey_callback: Optional[Callable] = None
        self.on_get_settings_callback: Optional[Callable] = None  # Para recarregar dados frescos
        self._notification_callback: Optional[Callable] = None
        
        # Estado
        self.is_detecting_hotkey = False
        self.detected_keys = set()
        
        # Variáveis para configurações gerais (tabs)
        self.var_datetime_format = None
        self.var_bracket_open = None
        self.var_bracket_close = None
        self.var_max_history = None
        self.var_monitor_interval = None
        self.var_idle_threshold = None
        self.var_notifications_enabled = None
        self.var_notification_duration = None
        self.var_hotkey_search = None
        self.var_hotkey_refresh = None
        
        # Rastreio de mudanças que requerem reinício
        self.needs_restart = False
        self.restart_warning_label = None
    
    def set_shortcuts(self, shortcuts: List[Dict[str, Any]]) -> None:
        """Define lista de shortcuts para exibir"""
        self.shortcuts_data = shortcuts.copy()
    
    def set_current_settings(self, settings: Dict[str, Any]) -> None:
        """Define as configurações atuais (para tabs de config geral)"""
        self.current_settings = settings.copy()
        self.shortcuts_data = settings.get("custom_shortcuts", [])
    
    def set_on_save_callback(self, callback: Callable) -> None:
        """Define callback para salvar configurações gerais"""
        self.on_save_callback = callback
    
    def set_on_add_callback(self, callback: Callable) -> None:
        """Define callback para adicionar shortcut"""
        self.on_add_callback = callback
    
    def set_on_update_callback(self, callback: Callable) -> None:
        """Define callback para atualizar shortcut"""
        self.on_update_callback = callback
    
    def set_on_remove_callback(self, callback: Callable) -> None:
        """Define callback para remover shortcut"""
        self.on_remove_callback = callback
    
    def set_on_validate_hotkey_callback(self, callback: Callable) -> None:
        """Define callback para validar hotkey"""
        self.on_validate_hotkey_callback = callback
    
    @property
    def notification_callback(self) -> Optional[Callable]:
        """Getter para notification_callback"""
        return self._notification_callback
    
    @notification_callback.setter
    def notification_callback(self, callback: Optional[Callable]) -> None:
        """Setter para notification_callback"""
        self._notification_callback = callback
    
    def show(self) -> None:
        """Mostra o dialog"""
        if self.window is not None:
            self.window.lift()
            self.window.focus_force()
            return
        
        self._create_window()
    
    def _create_window(self) -> None:
        """Cria a janela principal com tabs"""
        self.window = tk.Tk()
        self.window.title("Dahora App - Configurações")
        self.window.geometry("600x500")  # Ainda mais compacto
        self.window.resizable(False, False)
        
        # Tema nativo Windows (como search_dialog)
        try:
            style = ttk.Style()
            style.theme_use('vista')
        except Exception:
            style = ttk.Style()
        
        self.window.resizable(True, True)
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=(16, 12, 16, 12))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook (Tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # === ABA 1: PREFIXOS (CRUD) ===
        self._create_prefixes_tab(notebook)
        
        # === ABA 2: GERAL ===
        self._create_general_tab(notebook)
        
        # === ABA 3: NOTIFICAÇÕES ===
        self._create_notifications_tab(notebook)
        
        # === ABA 4: ATALHOS DO SISTEMA ===
        self._create_system_hotkeys_tab(notebook)
        
        # === ABA 5: INFORMAÇÕES ===
        self._create_info_tab(notebook)
        
        # Aviso de reinicialização necessária (inicialmente oculto)
        self.restart_warning_label = ttk.Label(
            main_frame, 
            text="⚠️ Reinicialização necessária para aplicar algumas mudanças",
            font=("Segoe UI", 9, "bold"),
            foreground="#D83B01"  # Laranja/vermelho Windows
        )
        # Não empacota ainda - só quando needs_restart = True
        
        # Botões inferiores (padrão Windows: OK azul + Cancelar)
        buttons = ttk.Frame(main_frame)
        buttons.pack(fill=tk.X, pady=(12, 0))
        ttk.Button(buttons, text="Cancelar", command=self._on_close).pack(side=tk.RIGHT, padx=(8, 0))
        ok_btn = ttk.Button(buttons, text="OK", command=self._on_save_and_close, default="active")
        ok_btn.pack(side=tk.RIGHT)
        
        # Protocolo de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Centraliza janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
        
        # Atalhos de teclado
        self.window.bind('<Escape>', lambda e: self._on_close())
        
        self.window.mainloop()
    
    def _create_prefixes_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de gerenciamento de prefixos (CRUD)"""
        tab = ttk.Frame(notebook, padding=(12, 8))
        notebook.add(tab, text="Atalhos Personalizados")
        
        # Frame de resultados com LabelFrame (EXATAMENTE como search_dialog)
        results_frame = ttk.LabelFrame(tab, text="Atalhos Configurados", padding=(8, 8))
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox simples (EXATAMENTE como search_dialog - NÃO usa Treeview)
        self.shortcuts_listbox = tk.Listbox(
            results_frame,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 9),  # Fonte monoespaçada para alinhamento
            height=10  # Reduzido para caber melhor na janela compacta
        )
        self.shortcuts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.shortcuts_listbox.yview)
        
        # Duplo clique para editar
        self.shortcuts_listbox.bind("<Double-Button-1>", lambda e: self._on_edit_clicked())
        
        # Label de contagem (EXATAMENTE como search_dialog)
        self.count_label = ttk.Label(tab, text="0 atalhos configurados", font=("Segoe UI", 8), foreground="gray")
        self.count_label.pack(anchor=tk.W)
        
        # Popula dados iniciais
        self._refresh_list()
        
        # Botões de ação (EXATAMENTE como search_dialog - SEM emojis)
        buttons_frame = ttk.Frame(tab)
        buttons_frame.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(buttons_frame, text="Adicionar", command=self._on_add_clicked).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(buttons_frame, text="Editar", command=self._on_edit_clicked).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(buttons_frame, text="Remover", command=self._on_remove_clicked).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(buttons_frame, text="Atualizar", command=self._refresh_list).pack(side=tk.RIGHT)
    
    def _create_general_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de configurações gerais"""
        tab = ttk.Frame(notebook, padding=(12, 8))
        notebook.add(tab, text="Formato")
        
        # Formato de data/hora padrão
        ttk.Label(tab, text="Formato de data/hora:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.var_datetime_format = tk.StringVar(
            value=self.current_settings.get("datetime_format", "%d.%m.%Y-%H:%M"))
        ttk.Entry(tab, textvariable=self.var_datetime_format, width=30).grid(
            row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Explicação do formato
        help_text = ("Códigos: %d=dia %m=mês %Y=ano %H=hora(24h) %M=minuto %S=segundo\n"
                    "Exemplo: %d.%m.%Y-%H:%M resulta em 05.11.2025-14:30")
        ttk.Label(tab, text=help_text, font=("Segoe UI", 8), foreground="gray").grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Caracteres de delimitação
        delim_frame = ttk.LabelFrame(tab, text="Caracteres de Delimitação", padding=10)
        delim_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E, pady=10)
        
        ttk.Label(delim_frame, text="Abertura:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.var_bracket_open = tk.StringVar(
            value=self.current_settings.get("bracket_open", "["))
        ttk.Entry(delim_frame, textvariable=self.var_bracket_open, width=10).grid(
            row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(delim_frame, text="Fechamento:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.var_bracket_close = tk.StringVar(
            value=self.current_settings.get("bracket_close", "]"))
        ttk.Entry(delim_frame, textvariable=self.var_bracket_close, width=10).grid(
            row=0, column=3, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(delim_frame, text="Ex: [dahora-05.11.2025-14:30]", 
                 font=("Segoe UI", 8), foreground="gray").grid(
            row=1, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
        # Histórico
        ttk.Label(tab, text="Itens no histórico:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.var_max_history = tk.IntVar(
            value=self.current_settings.get("max_history_items", 100))
        ttk.Spinbox(tab, from_=10, to=1000, textvariable=self.var_max_history, 
                   width=15).grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Monitor de clipboard
        ttk.Label(tab, text="Intervalo de monitoramento (seg):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.var_monitor_interval = tk.DoubleVar(
            value=self.current_settings.get("clipboard_monitor_interval", 3.0))
        ttk.Spinbox(tab, from_=0.5, to=10.0, increment=0.5, 
                   textvariable=self.var_monitor_interval, width=15).grid(
                       row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Idle threshold
        ttk.Label(tab, text="Tempo ocioso para pausar (seg):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.var_idle_threshold = tk.DoubleVar(
            value=self.current_settings.get("clipboard_idle_threshold", 30.0))
        ttk.Spinbox(tab, from_=10, to=300, increment=10, 
                   textvariable=self.var_idle_threshold, width=15).grid(
                       row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def _create_notifications_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de configurações de notificações"""
        tab = ttk.Frame(notebook, padding=(12, 8))
        notebook.add(tab, text="Notificações")
        
        # Habilitar notificações
        self.var_notifications_enabled = tk.BooleanVar(
            value=self.current_settings.get("notification_enabled", True))
        ttk.Checkbutton(tab, text="Habilitar notificações", 
                       variable=self.var_notifications_enabled).grid(
                           row=0, column=0, sticky=tk.W, pady=5)
        
        # Duração
        ttk.Label(tab, text="Duração (segundos):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.var_notification_duration = tk.IntVar(
            value=self.current_settings.get("notification_duration", 2))
        ttk.Spinbox(tab, from_=1, to=15, textvariable=self.var_notification_duration, 
                   width=15).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def _create_system_hotkeys_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de atalhos do sistema"""
        tab = ttk.Frame(notebook, padding=(12, 8))
        notebook.add(tab, text="Teclas de Atalho")
        
        # Atalho de busca
        ttk.Label(tab, text="Buscar no histórico:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.var_hotkey_search = tk.StringVar(
            value=self.current_settings.get("hotkey_search_history", "ctrl+shift+f"))
        self.var_hotkey_search.trace_add("write", lambda *args: self._mark_needs_restart())
        ttk.Entry(tab, textvariable=self.var_hotkey_search, width=30).grid(
            row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Atalho de refresh
        ttk.Label(tab, text="Recarregar menu:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.var_hotkey_refresh = tk.StringVar(
            value=self.current_settings.get("hotkey_refresh_menu", "ctrl+shift+r"))
        self.var_hotkey_refresh.trace_add("write", lambda *args: self._mark_needs_restart())
        ttk.Entry(tab, textvariable=self.var_hotkey_refresh, width=30).grid(
            row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Aviso
        warning_text = (
            "Use combinações como:\n"
            "  • ctrl+shift+letra\n"
            "  • ctrl+alt+letra\n"
            "  • alt+shift+letra\n\n"
            "Evite conflitos com atalhos do sistema."
        )
        ttk.Label(tab, text=warning_text, font=("Segoe UI", 8), foreground="gray").grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Atalhos Reservados
        reserved_frame = ttk.LabelFrame(tab, text="Atalhos Reservados (não disponíveis)", padding=10)
        reserved_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(15, 0))
        
        ttk.Label(reserved_frame, text="Apenas atalhos básicos de clipboard:", 
                 font=("Segoe UI", 9)).pack(anchor=tk.W)
        ttk.Label(reserved_frame, text="Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+A, Ctrl+Z", 
                 font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(5, 0))
    
    def _create_info_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de informações sobre configurabilidade"""
        tab = ttk.Frame(notebook, padding=(12, 8))
        notebook.add(tab, text="Info")
        
        # Título
        ttk.Label(tab, text="Total Liberdade de Configuração!", 
                 font=("Segoe UI", 11, "bold")).pack(pady=(10, 15))
        
        ttk.Label(tab, text="Nenhum atalho é fixo neste aplicativo!\n"
                           "Você tem controle total sobre todas as teclas.", 
                 font=("Segoe UI", 9), justify=tk.CENTER).pack(pady=(0, 15))
        
        # Recursos
        recursos_frame = ttk.LabelFrame(tab, text="Recursos Configuráveis", padding=10)
        recursos_frame.pack(fill=tk.X, pady=(0, 10))
        
        recursos_text = (
            "  • Atalhos personalizados ilimitados\n"
            "  • Prefixos customizados por atalho\n"
            "  • Formato de data/hora configurável\n"
            "  • Caracteres de delimitação ajustáveis\n"
            "  • Teclas de busca e refresh definíveis\n"
            "  • Histórico de clipboard configurável\n"
            "  • Notificações personalizáveis"
        )
        ttk.Label(recursos_frame, text=recursos_text, font=("Segoe UI", 9), 
                 justify=tk.LEFT).pack(anchor=tk.W)
        
        # Dica
        dica_frame = ttk.LabelFrame(tab, text="Dica", padding=10)
        dica_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(dica_frame, 
                 text="Configure quantos atalhos quiser na aba 'Atalhos Personalizados'.\n"
                      "Cada atalho pode ter seu próprio prefixo e pode ser habilitado/desabilitado.", 
                 font=("Segoe UI", 9), justify=tk.LEFT).pack(anchor=tk.W)
    
    def _refresh_list(self) -> None:
        """Atualiza a Listbox com dados dos prefixos (EXATAMENTE como search_dialog)"""
        if not hasattr(self, 'shortcuts_listbox') or not self.shortcuts_listbox:
            return
        
        # Limpa listbox
        self.shortcuts_listbox.delete(0, tk.END)
        
        # Popula listbox (formato simples como search_dialog)
        for shortcut in self.shortcuts_data:
            status = "✓" if shortcut.get("enabled", True) else "⏸"
            hotkey = shortcut.get("hotkey", "").upper()
            prefix = shortcut.get("prefix", "")
            description = shortcut.get("description", "")
            
            # Formato: [✓] CTRL+SHIFT+1 → prefix - descrição
            display = f"[{status}] {hotkey:20} → {prefix:15} - {description}"
            self.shortcuts_listbox.insert(tk.END, display)
        
        # Atualiza contagem (EXATAMENTE como search_dialog)
        if hasattr(self, 'count_label'):
            self.count_label.config(text=f"{len(self.shortcuts_data)} atalhos configurados")
    
    def _reload_from_settings(self) -> None:
        """Recarrega a lista diretamente do settings_manager"""
        if self.on_get_settings_callback:
            fresh_settings = self.on_get_settings_callback()
            self.current_settings = fresh_settings
            self.shortcuts_data = fresh_settings.get("custom_shortcuts", [])
        else:
            self.shortcuts_data = self.current_settings.get("custom_shortcuts", [])
        
        self._refresh_list()
    
    def _mark_needs_restart(self) -> None:
        """Marca que é necessário reiniciar e mostra aviso"""
        if not self.needs_restart:
            self.needs_restart = True
            # Mostra o aviso acima dos botões
            if self.restart_warning_label:
                self.restart_warning_label.pack(fill=tk.X, pady=(8, 0), before=self.restart_warning_label.master.winfo_children()[-1])
    
    def _on_save_all(self) -> None:
        """Salva todas as configurações (tabs Geral e Notificações)"""
        try:
            if self.on_save_callback:
                settings = {
                    "datetime_format": self.var_datetime_format.get().strip() if self.var_datetime_format else "%d.%m.%Y-%H:%M",
                    "bracket_open": self.var_bracket_open.get() if self.var_bracket_open else "[",
                    "bracket_close": self.var_bracket_close.get() if self.var_bracket_close else "]",
                    "max_history_items": self.var_max_history.get() if self.var_max_history else 100,
                    "clipboard_monitor_interval": self.var_monitor_interval.get() if self.var_monitor_interval else 3.0,
                    "clipboard_idle_threshold": self.var_idle_threshold.get() if self.var_idle_threshold else 30.0,
                    "notification_enabled": self.var_notifications_enabled.get() if self.var_notifications_enabled else True,
                    "notification_duration": self.var_notification_duration.get() if self.var_notification_duration else 2,
                    "hotkey_search_history": self.var_hotkey_search.get().strip() if self.var_hotkey_search else "ctrl+shift+f",
                    "hotkey_refresh_menu": self.var_hotkey_refresh.get().strip() if self.var_hotkey_refresh else "ctrl+shift+r",
                }
                self.on_save_callback(settings)
            
            # Não mostra notificação aqui - será mostrada no _on_save_and_close
        except Exception as e:
            logging.error(f"Erro ao salvar configurações: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def _on_save_and_close(self) -> None:
        """Salva e fecha, perguntando sobre reiniciar se necessário"""
        # Salva as configurações
        self._on_save_all()
        
        # Se precisa reiniciar, pergunta ao usuário
        if self.needs_restart:
            response = messagebox.askyesno(
                "Reiniciar Aplicativo",
                "Algumas alterações exigem reiniciar o aplicativo.\n\nDeseja reiniciar agora?",
                icon="warning"
            )
            if response:
                # Reinicia o app
                import sys
                import os
                python = sys.executable
                os.execl(python, python, *sys.argv)
            else:
                # Apenas fecha
                if self.notification_callback:
                    self.notification_callback(
                        "Dahora App",
                        "Configurações salvas!\n\nLembre-se de reiniciar para aplicar as mudanças."
                    )
        else:
            if self.notification_callback:
                self.notification_callback(
                    "Dahora App",
                    "Configurações salvas com sucesso!"
                )
        
        self._on_close()
    
    def _on_add_clicked(self) -> None:
        """Callback para adicionar novo shortcut"""
        self._show_editor_dialog()
    
    def _on_edit_clicked(self) -> None:
        """Callback para editar shortcut selecionado (usando Listbox)"""
        if not hasattr(self, 'shortcuts_listbox') or not self.shortcuts_listbox:
            return
        
        selection = self.shortcuts_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um atalho para editar")
            return
        
        idx = selection[0]
        if idx >= len(self.shortcuts_data):
            return
        
        shortcut_data = self.shortcuts_data[idx]
        self._show_editor_dialog(shortcut_data)
    
    def _on_remove_clicked(self) -> None:
        """Callback para remover shortcut selecionado (usando Listbox)"""
        if not hasattr(self, 'shortcuts_listbox') or not self.shortcuts_listbox:
            return
        
        selection = self.shortcuts_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um atalho para remover")
            return
        
        idx = selection[0]
        if idx >= len(self.shortcuts_data):
            return
        
        shortcut = self.shortcuts_data[idx]
        shortcut_id = shortcut.get("id")
        prefix = shortcut.get("prefix", "")
        hotkey = shortcut.get("hotkey", "").upper()
        
        confirm = messagebox.askyesno("Confirmar Remoção",
                                     f"Deseja remover o atalho?\n\n"
                                     f"Hotkey: {hotkey}\n"
                                     f"Prefixo: {prefix}")
        
        if confirm and self.on_remove_callback:
            success, msg = self.on_remove_callback(shortcut_id)
            if success:
                self._reload_from_settings()
                if self.notification_callback:
                    self.notification_callback("Dahora App", "Atalho removido com sucesso!")
            else:
                messagebox.showerror("Erro", f"Falha ao remover atalho:\n{msg}")
    
    def _on_close(self) -> None:
        """Callback para fechar a janela"""
        if self.window:
            self.window.destroy()
            self.window = None
    
    def _show_editor_dialog(self, shortcut: Optional[Dict[str, Any]] = None) -> None:
        """Mostra dialog de edição/criação"""
        editor = ShortcutEditorDialog(
            parent=self.window,
            shortcut=shortcut,
            on_save=self._on_editor_save,
            on_validate_hotkey=self.on_validate_hotkey_callback
        )
        editor.show()
    
    def _on_editor_save(self, shortcut_data: Dict[str, Any]) -> None:
        """Callback quando editor salva"""
        # Executa com after(0) para não bloquear o mainloop do Tkinter
        if self.window:
            self.window.after(0, lambda: self._process_save(shortcut_data))
        else:
            self._process_save(shortcut_data)
    
    def _process_save(self, shortcut_data: Dict[str, Any]) -> None:
        """Processa o salvamento do shortcut (chamado via after)"""
        try:
            is_new = "id" not in shortcut_data or shortcut_data["id"] is None
            
            if is_new:
                if self.on_add_callback:
                    success, msg, new_id = self.on_add_callback(
                        shortcut_data.get("hotkey", ""),
                        shortcut_data.get("prefix", ""),
                        shortcut_data.get("description", ""),
                        shortcut_data.get("enabled", True)
                    )
                    
                    if success:
                        self._reload_from_settings()
                        if self.notification_callback:
                            self.notification_callback("Dahora App", "Atalho adicionado com sucesso!")
                    else:
                        messagebox.showerror("Erro", f"Falha ao adicionar atalho:\n{msg}")
            else:
                if self.on_update_callback:
                    success, msg = self.on_update_callback(
                        shortcut_data["id"],
                        hotkey=shortcut_data.get("hotkey"),
                        prefix=shortcut_data.get("prefix"),
                        description=shortcut_data.get("description"),
                        enabled=shortcut_data.get("enabled")
                    )
                    
                    if success:
                        self._reload_from_settings()
                        if self.notification_callback:
                            self.notification_callback("Dahora App", "Atalho atualizado com sucesso!")
                    else:
                        messagebox.showerror("Erro", f"Falha ao atualizar atalho:\n{msg}")
        except Exception as e:
            logging.error(f"Erro ao salvar: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")


class ShortcutEditorDialog:
    """Dialog para editar/criar um shortcut"""
    
    def __init__(self, parent: tk.Tk, shortcut: Optional[Dict[str, Any]], 
                 on_save: Callable, on_validate_hotkey: Optional[Callable]):
        """Inicializa o editor"""
        self.parent = parent
        self.shortcut = shortcut.copy() if shortcut else {}
        self.on_save = on_save
        self.on_validate_hotkey = on_validate_hotkey
        
        self.window: Optional[tk.Toplevel] = None
        self.hotkey_var = tk.StringVar(value=self.shortcut.get("hotkey", ""))
        self.prefix_var = tk.StringVar(value=self.shortcut.get("prefix", ""))
        self.description_var = tk.StringVar(value=self.shortcut.get("description", ""))
        self.enabled_var = tk.BooleanVar(value=self.shortcut.get("enabled", True))
        
        self.validation_label: Optional[ttk.Label] = None
        self.preview_label: Optional[ttk.Label] = None
        
        self.is_detecting = False
        self.detected_keys = set()
    
    def show(self) -> None:
        """Mostra o dialog de edição"""
        is_new = not self.shortcut or "id" not in self.shortcut
        title = "Adicionar Atalho" if is_new else "Editar Atalho"
        
        self.window = tk.Toplevel(self.parent)
        
        # Aplica estilo Windows 11
        self.window.title(title)
        self.window.geometry("500x380")
        try:
            style = ttk.Style()
            style.theme_use('vista')
        except:
            pass
        
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=(16, 12))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Prefixo
        ttk.Label(main_frame, text="Prefixo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        prefix_entry = ttk.Entry(main_frame, textvariable=self.prefix_var, width=40)
        prefix_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        prefix_entry.bind("<KeyRelease>", lambda e: self._update_preview())
        
        # Descrição
        ttk.Label(main_frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W, pady=5)
        description_entry = ttk.Entry(main_frame, textvariable=self.description_var, width=40)
        description_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Hotkey
        ttk.Label(main_frame, text="Atalho:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        hotkey_frame = ttk.Frame(main_frame)
        hotkey_frame.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        
        hotkey_entry = ttk.Entry(hotkey_frame, textvariable=self.hotkey_var)
        hotkey_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        hotkey_entry.bind("<KeyRelease>", lambda e: self._validate_hotkey())
        
        detect_button = ttk.Button(hotkey_frame, text="Detectar", command=self._start_detecting)
        detect_button.pack(side=tk.LEFT)
        
        # Validação
        self.validation_label = ttk.Label(main_frame, text="", foreground="gray")
        self.validation_label.grid(row=3, column=1, sticky=tk.W, pady=(0, 5))
        
        # Preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview")
        preview_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E, pady=10)
        
        self.preview_label = ttk.Label(preview_frame, text="", font=("Segoe UI", 9, "bold"))
        self.preview_label.pack(padx=10, pady=5)
        
        # Enabled checkbox
        ttk.Checkbutton(main_frame, text="Habilitar este atalho", 
                       variable=self.enabled_var).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Botões (padrão Windows - sem emojis)
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))
        
        ttk.Button(buttons_frame, text="Cancelar", 
                  command=self._on_cancel_clicked, width=12).pack(side=tk.RIGHT, padx=(8, 0))
        ttk.Button(buttons_frame, text="OK", 
                  command=self._on_save_clicked, width=12, default="active").pack(side=tk.RIGHT)
        
        # Configure grid
        main_frame.columnconfigure(1, weight=1)
        
        # Atualiza preview inicial
        self._update_preview()
        self._validate_hotkey()
        
        # Centraliza
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def _validate_hotkey(self) -> None:
        """Valida o hotkey em tempo real"""
        if not self.validation_label:
            return
        
        hotkey = self.hotkey_var.get().strip()
        
        if not hotkey:
            self.validation_label.config(text="Digite um atalho", foreground="gray")
            return
        
        if self.on_validate_hotkey:
            exclude_id = self.shortcut.get("id") if self.shortcut else None
            valid, msg = self.on_validate_hotkey(hotkey, exclude_id)
            
            if valid:
                self.validation_label.config(text=f"Hotkey válido", foreground="green")
            else:
                self.validation_label.config(text=f"{msg}", foreground="red")
        else:
            self.validation_label.config(text="", foreground="gray")
    
    def _update_preview(self) -> None:
        """Atualiza o preview do resultado"""
        if not self.preview_label:
            return
        
        prefix = self.prefix_var.get().strip()
        now = datetime.now()
        timestamp = now.strftime("%d.%m.%Y-%H:%M")
        
        if prefix:
            preview = f"[{prefix}-{timestamp}]"
        else:
            preview = f"[{timestamp}]"
        
        self.preview_label.config(text=preview)
    
    def _start_detecting(self) -> None:
        """Inicia detecção de teclas"""
        try:
            import keyboard  # Lazy import apenas quando necessário
        except ImportError:
            messagebox.showerror("Erro", "Biblioteca 'keyboard' não disponível.\nInstale com: pip install keyboard")
            return
        
        self.is_detecting = True
        self.detected_keys.clear()
        
        # Cria janela de detecção
        detect_window = tk.Toplevel(self.window)
        detect_window.title("Detectar Teclas")
        detect_window.geometry("400x200")
        detect_window.transient(self.window)
        detect_window.grab_set()
        
        ttk.Label(detect_window, text="Pressione a combinação de teclas desejada...", 
                 font=("Segoe UI", 9)).pack(pady=20)
        
        keys_label = ttk.Label(detect_window, text="", font=("Segoe UI", 11, "bold"))
        keys_label.pack(pady=10)
        
        ttk.Button(detect_window, text="Cancelar", 
                  command=lambda: self._stop_detecting(detect_window, None)).pack(pady=20)
        
        # Hook de teclado
        def on_key(event):
            if not self.is_detecting:
                return
            
            key_name = event.name.lower()
            
            # Adiciona modificadores
            if key_name in ["ctrl", "shift", "alt"]:
                self.detected_keys.add(key_name)
            else:
                # Tecla final pressionada
                self.detected_keys.add(key_name)
                
                # Monta hotkey
                modifiers = sorted([k for k in self.detected_keys if k in ["ctrl", "shift", "alt"]])
                keys = [k for k in self.detected_keys if k not in ["ctrl", "shift", "alt"]]
                
                if modifiers and keys:
                    hotkey = "+".join(modifiers + keys)
                    self._stop_detecting(detect_window, hotkey)
                    return
            
            # Atualiza label
            display = " + ".join(sorted(self.detected_keys)).upper()
            keys_label.config(text=display)
        
        keyboard.hook(on_key)
        
        # Centraliza
        detect_window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (detect_window.winfo_width() // 2)
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (detect_window.winfo_height() // 2)
        detect_window.geometry(f"+{x}+{y}")
    
    def _stop_detecting(self, detect_window: tk.Toplevel, hotkey: Optional[str]) -> None:
        """Para a detecção de teclas"""
        self.is_detecting = False
        
        try:
            import keyboard
            keyboard.unhook_all()
            keyboard.unhook_all()  # Chama duas vezes para garantir
        except Exception as e:
            logging.warning(f"Erro ao remover hooks de teclado: {e}")
        
        detect_window.destroy()
        
        if hotkey:
            self.hotkey_var.set(hotkey)
            self._validate_hotkey()
    
    def _on_save_clicked(self) -> None:
        """Salva o shortcut"""
        try:
            prefix = self.prefix_var.get().strip()
            hotkey = self.hotkey_var.get().strip().lower()
            description = self.description_var.get().strip()
            enabled = self.enabled_var.get()
            
            if not prefix:
                messagebox.showwarning("Campo Obrigatório", "Por favor, preencha o prefixo.")
                return
            
            if not hotkey:
                messagebox.showwarning("Campo Obrigatório", "Por favor, defina um atalho.")
                return
            
            # Valida hotkey
            if self.on_validate_hotkey:
                exclude_id = self.shortcut.get("id") if self.shortcut else None
                valid, msg = self.on_validate_hotkey(hotkey, exclude_id)
                
                if not valid:
                    messagebox.showerror("Atalho Inválido", msg)
                    return
            
            # Monta dados
            shortcut_data = {
                "hotkey": hotkey,
                "prefix": prefix,
                "description": description,
                "enabled": enabled,
                "datetime_format": "%d.%m.%Y-%H:%M"
            }
            
            if self.shortcut and "id" in self.shortcut:
                shortcut_data["id"] = self.shortcut["id"]
            
            # Fecha janela PRIMEIRO
            if self.window:
                self.window.destroy()
                self.window = None
            
            # Chama callback
            if self.on_save:
                self.on_save(shortcut_data)
            
        except Exception as e:
            logging.error(f"Erro ao salvar: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def _on_cancel_clicked(self) -> None:
        """Cancela a edição"""
        self.window.destroy()
