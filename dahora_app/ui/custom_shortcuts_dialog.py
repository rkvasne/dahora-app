"""
Gerenciador de Atalhos Personalizados - Dialog de Configurações com CRUD
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Callable, Optional, List, Dict, Any
from datetime import datetime
from dahora_app.ui.styles import Windows11Style
from dahora_app.ui.shortcut_editor import ShortcutEditorDialog

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
        """Cria a janela principal com design moderno e scrollbar"""
        self.window = tk.Tk()
        # Configura estilo moderno
        Windows11Style.configure_window(self.window, "Dahora App - Configurações", "800x650")
        Windows11Style.configure_styles(self.window)
        
        self.window.resizable(True, True)
        
        # Canvas principal com scrollbar para conteúdo que extrapola
        main_canvas = tk.Canvas(self.window, 
                               bg=Windows11Style.COLORS['bg'],
                               highlightthickness=0,
                               borderwidth=0)
        main_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar moderna para o canvas
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=main_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame scrollável dentro do canvas
        scrollable_frame = ttk.Frame(main_canvas, style="TFrame")
        canvas_frame = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Função para atualizar scroll region
        def configure_scroll_region(event=None):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            # Ajusta largura do frame scrollável
            canvas_width = main_canvas.winfo_width()
            main_canvas.itemconfig(canvas_frame, width=canvas_width)
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        main_canvas.bind("<Configure>", configure_scroll_region)
        
        # Frame principal moderno com padding generoso
        main_frame = Windows11Style.create_modern_card(scrollable_frame, padding=24)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho moderno
        header_frame = ttk.Frame(main_frame, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 24))
        
        title_label = Windows11Style.create_section_header(header_frame, "⚙️ Configurações do Dahora App")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(header_frame, text="Personalize atalhos, formatos e preferências", 
                                 style="Muted.TLabel")
        subtitle_label.pack(anchor="w", pady=(4, 0))
        
        # Notebook moderno (Tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # === ABAS MODERNIZADAS ===
        self._create_modern_prefixes_tab(notebook)
        self._create_modern_general_tab(notebook)
        self._create_modern_notifications_tab(notebook)
        self._create_modern_system_hotkeys_tab(notebook)
        self._create_modern_info_tab(notebook)
        
        # Aviso de reinicialização moderno
        self.restart_warning_label = ttk.Label(
            main_frame, 
            text="⚠️ Reinicialização necessária para aplicar algumas mudanças",
            font=("Segoe UI", 10, "bold"),
            foreground=Windows11Style.COLORS['warning']
        )
        
        # Botões modernos
        buttons_frame = ttk.Frame(main_frame, style="TFrame")
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botões alinhados à direita com espaçamento moderno
        cancel_btn = Windows11Style.create_modern_button(buttons_frame, "Cancelar", 
                                                        command=self._on_close)
        cancel_btn.pack(side=tk.RIGHT, padx=(16, 0))
        
        ok_btn = Windows11Style.create_modern_button(buttons_frame, "Salvar", 
                                                   command=self._on_save_and_close, 
                                                   style="Primary.TButton")
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
        
        # Scroll com mouse wheel
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.window.mainloop()
    
    def _create_modern_prefixes_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba moderna de gerenciamento de atalhos personalizados"""
        # Tab com padding moderno
        tab = Windows11Style.create_modern_card(notebook, padding=24)
        notebook.add(tab, text="🎯 Atalhos Personalizados")
        
        # Cabeçalho da seção
        header_frame = ttk.Frame(tab, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Atalhos Configurados", style="Heading.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(header_frame, text="Gerencie seus atalhos personalizados para inserção rápida de timestamps", 
                                 style="Muted.TLabel")
        subtitle_label.pack(anchor="w", pady=(4, 0))
        
        # Card da lista moderna SEM bordas
        list_card = ttk.Frame(tab, style="TFrame")  # Frame simples sem bordas
        list_card.pack(fill=tk.BOTH, expand=True, pady=(0, 16))
        
        # Container da lista com scrollbar moderna
        list_container = ttk.Frame(list_card, style="TFrame")
        list_container.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        # Scrollbar moderna (invisível até hover)
        scrollbar = ttk.Scrollbar(list_container, style="TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox moderna SEM bordas
        self.shortcuts_listbox = tk.Listbox(
            list_container,
            yscrollcommand=scrollbar.set,
            font=("Segoe UI", 10),  # Fonte moderna
            height=12,  # Mais espaço
            borderwidth=0,
            highlightthickness=0,
            selectmode=tk.SINGLE,
            relief='flat'  # Sem relevo
        )
        Windows11Style.configure_listbox(self.shortcuts_listbox)
        self.shortcuts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.shortcuts_listbox.yview)
        
        # Duplo clique para editar
        self.shortcuts_listbox.bind("<Double-Button-1>", lambda e: self._on_edit_clicked())
        
        # Informações da lista
        info_frame = ttk.Frame(tab, style="TFrame")
        info_frame.pack(fill=tk.X, pady=(0, 16))
        
        self.count_label = ttk.Label(info_frame, text="0 atalhos configurados", style="Muted.TLabel")
        self.count_label.pack(anchor="w", padx=16)
        
        # Popula dados iniciais
        self._refresh_list()
        
        # Botões de ação modernos
        buttons_frame = ttk.Frame(tab, style="TFrame")
        buttons_frame.pack(fill=tk.X, padx=16)
        
        # Botões principais à esquerda
        primary_buttons = ttk.Frame(buttons_frame, style="TFrame")
        primary_buttons.pack(side=tk.LEFT)
        
        add_btn = Windows11Style.create_modern_button(primary_buttons, "➕ Adicionar", 
                                                    command=self._on_add_clicked, 
                                                    style="Primary.TButton")
        add_btn.pack(side=tk.LEFT, padx=(0, 12))
        
        edit_btn = Windows11Style.create_modern_button(primary_buttons, "✏️ Editar", 
                                                     command=self._on_edit_clicked)
        edit_btn.pack(side=tk.LEFT, padx=(0, 12))
        
        remove_btn = Windows11Style.create_modern_button(primary_buttons, "🗑️ Remover", 
                                                       command=self._on_remove_clicked, 
                                                       style="Danger.TButton")
        remove_btn.pack(side=tk.LEFT)
        
        # Botão de atualizar à direita
        refresh_btn = Windows11Style.create_modern_button(buttons_frame, "🔄 Atualizar", 
                                                        command=self._refresh_list)
        refresh_btn.pack(side=tk.RIGHT)
    
    def _create_modern_general_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba moderna de configurações de formato"""
        tab = Windows11Style.create_modern_card(notebook, padding=24)
        notebook.add(tab, text="📅 Formato")
        
        # Cabeçalho
        header_frame = ttk.Frame(tab, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 24))
        
        title_label = ttk.Label(header_frame, text="Formato de Data e Hora", style="Heading.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(header_frame, text="Configure como a data e hora serão formatadas nos timestamps", 
                                 style="Muted.TLabel")
        subtitle_label.pack(anchor="w", pady=(4, 0))
        
        # Seção de formato principal
        format_card = Windows11Style.create_modern_card(tab, padding=20)
        format_card.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(format_card, text="Formato de Data/Hora", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 8))
        
        self.var_datetime_format = tk.StringVar(
            value=self.current_settings.get("datetime_format", "%d.%m.%Y-%H:%M"))
        
        format_entry = Windows11Style.create_modern_entry(format_card, textvariable=self.var_datetime_format, width=40)
        format_entry.pack(fill=tk.X, pady=(0, 12))
        
        # Explicação com exemplos
        help_card = Windows11Style.create_modern_card(format_card, padding=16)
        help_card.pack(fill=tk.X)
        
        ttk.Label(help_card, text="💡 Códigos Disponíveis", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 8))
        
        codes_text = (
            "• %d = dia (01-31)     • %m = mês (01-12)     • %Y = ano (2025)\n"
            "• %H = hora 24h (00-23)     • %M = minuto (00-59)     • %S = segundo (00-59)\n\n"
            "Exemplo: %d.%m.%Y-%H:%M resulta em → 29.12.2025-14:30"
        )
        ttk.Label(help_card, text=codes_text, style="Card.TLabel").pack(anchor="w")
        
        # Seção de delimitadores
        delim_card = Windows11Style.create_modern_card(tab, padding=20)
        delim_card.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(delim_card, text="Caracteres de Delimitação", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 16))
        
        delim_container = ttk.Frame(delim_card, style="TFrame")
        delim_container.pack(fill=tk.X)
        
        # Abertura
        open_frame = ttk.Frame(delim_container, style="TFrame")
        open_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 16))
        
        ttk.Label(open_frame, text="Abertura", style="Card.TLabel").pack(anchor="w", pady=(0, 6))
        self.var_bracket_open = tk.StringVar(value=self.current_settings.get("bracket_open", "["))
        open_entry = Windows11Style.create_modern_entry(open_frame, textvariable=self.var_bracket_open, width=10)
        open_entry.pack(fill=tk.X)
        
        # Fechamento
        close_frame = ttk.Frame(delim_container, style="TFrame")
        close_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(close_frame, text="Fechamento", style="Card.TLabel").pack(anchor="w", pady=(0, 6))
        self.var_bracket_close = tk.StringVar(value=self.current_settings.get("bracket_close", "]"))
        close_entry = Windows11Style.create_modern_entry(close_frame, textvariable=self.var_bracket_close, width=10)
        close_entry.pack(fill=tk.X)
        
        # Preview do resultado
        preview_card = Windows11Style.create_modern_card(delim_card, padding=16)
        preview_card.pack(fill=tk.X, pady=(16, 0))
        
        ttk.Label(preview_card, text="Preview", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 8))
        preview_text = "[dahora-29.12.2025-14:30]"
        ttk.Label(preview_card, text=preview_text, font=("Consolas", 11, "bold"), 
                 style="Card.TLabel").pack(anchor="w")
        
        # Configurações de histórico
        history_card = Windows11Style.create_modern_card(tab, padding=20)
        history_card.pack(fill=tk.X)
        
        ttk.Label(history_card, text="Configurações de Histórico", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 16))
        
        # Grid para configurações
        config_frame = ttk.Frame(history_card, style="TFrame")
        config_frame.pack(fill=tk.X)
        
        # Máximo de itens
        max_frame = ttk.Frame(config_frame, style="TFrame")
        max_frame.pack(fill=tk.X, pady=(0, 12))
        
        ttk.Label(max_frame, text="Máximo de itens no histórico", style="Card.TLabel").pack(anchor="w", pady=(0, 6))
        self.var_max_history = tk.IntVar(value=self.current_settings.get("max_history_items", 100))
        max_spinbox = ttk.Spinbox(max_frame, from_=10, to=1000, textvariable=self.var_max_history, width=15)
        max_spinbox.pack(anchor="w")
        
        # Intervalo de monitoramento
        interval_frame = ttk.Frame(config_frame, style="TFrame")
        interval_frame.pack(fill=tk.X, pady=(0, 12))
        
        ttk.Label(interval_frame, text="Intervalo de monitoramento (segundos)", style="Card.TLabel").pack(anchor="w", pady=(0, 6))
        self.var_monitor_interval = tk.DoubleVar(value=self.current_settings.get("clipboard_monitor_interval", 3.0))
        interval_spinbox = ttk.Spinbox(interval_frame, from_=0.5, to=10.0, increment=0.5, 
                                     textvariable=self.var_monitor_interval, width=15)
        interval_spinbox.pack(anchor="w")
        
        # Tempo ocioso
        idle_frame = ttk.Frame(config_frame, style="TFrame")
        idle_frame.pack(fill=tk.X)
        
        ttk.Label(idle_frame, text="Tempo ocioso para pausar (segundos)", style="Card.TLabel").pack(anchor="w", pady=(0, 6))
        self.var_idle_threshold = tk.DoubleVar(value=self.current_settings.get("clipboard_idle_threshold", 30.0))
        idle_spinbox = ttk.Spinbox(idle_frame, from_=10, to=300, increment=10, 
                                 textvariable=self.var_idle_threshold, width=15)
        idle_spinbox.pack(anchor="w")
    
    def _create_modern_notifications_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba moderna de configurações de notificações"""
        tab = Windows11Style.create_modern_card(notebook, padding=24)
        notebook.add(tab, text="🔔 Notificações")
        
        # Cabeçalho
        header_frame = ttk.Frame(tab, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 24))
        
        title_label = ttk.Label(header_frame, text="Configurações de Notificações", style="Heading.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(header_frame, text="Configure como e quando as notificações serão exibidas", 
                                 style="Muted.TLabel")
        subtitle_label.pack(anchor="w", pady=(4, 0))
        
        # Card principal de notificações
        notif_card = Windows11Style.create_modern_card(tab, padding=20)
        notif_card.pack(fill=tk.X, pady=(0, 20))
        
        # Toggle principal
        toggle_frame = ttk.Frame(notif_card, style="TFrame")
        toggle_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.var_notifications_enabled = tk.BooleanVar(
            value=self.current_settings.get("notification_enabled", True))
        
        enable_check = ttk.Checkbutton(toggle_frame, text="🔔 Habilitar notificações do sistema", 
                                     variable=self.var_notifications_enabled, 
                                     style="TCheckbutton")
        enable_check.pack(anchor="w")
        
        ttk.Label(toggle_frame, text="Exibe notificações quando atalhos são acionados ou ações são realizadas", 
                 style="Muted.TLabel").pack(anchor="w", pady=(4, 0))
        
        # Configurações de duração
        duration_frame = ttk.Frame(notif_card, style="TFrame")
        duration_frame.pack(fill=tk.X)
        
        ttk.Label(duration_frame, text="Duração da Notificação", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 8))
        
        duration_container = ttk.Frame(duration_frame, style="TFrame")
        duration_container.pack(fill=tk.X)
        
        self.var_notification_duration = tk.IntVar(
            value=self.current_settings.get("notification_duration", 2))
        
        duration_spinbox = ttk.Spinbox(duration_container, from_=1, to=15, 
                                     textvariable=self.var_notification_duration, width=10)
        duration_spinbox.pack(side=tk.LEFT, padx=(0, 8))
        
        ttk.Label(duration_container, text="segundos", style="Card.TLabel").pack(side=tk.LEFT)
        
        # Card de preview
        preview_card = Windows11Style.create_modern_card(tab, padding=20)
        preview_card.pack(fill=tk.X)
        
        ttk.Label(preview_card, text="💡 Tipos de Notificações", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 12))
        
        examples_text = (
            "• Atalho acionado: 'Copiado com sucesso via Atalho! [dahora-29.12.2025-14:30]'\n"
            "• Item do histórico: 'Copiado do histórico! [texto copiado]'\n"
            "• Configurações salvas: 'Configurações salvas com sucesso!'\n"
            "• Erros: 'Erro ao processar atalho: [detalhes do erro]'"
        )
        
        ttk.Label(preview_card, text=examples_text, style="Card.TLabel").pack(anchor="w")
    
    def _create_modern_system_hotkeys_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba moderna de atalhos do sistema"""
        tab = Windows11Style.create_modern_card(notebook, padding=24)
        notebook.add(tab, text="⌨️ Teclas de Atalho")
        
        # Cabeçalho
        header_frame = ttk.Frame(tab, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 24))
        
        title_label = ttk.Label(header_frame, text="Atalhos do Sistema", style="Heading.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(header_frame, text="Configure os atalhos globais para funções do sistema", 
                                 style="Muted.TLabel")
        subtitle_label.pack(anchor="w", pady=(4, 0))
        
        # Card de atalhos principais
        hotkeys_card = Windows11Style.create_modern_card(tab, padding=20)
        hotkeys_card.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(hotkeys_card, text="Atalhos Principais", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 16))
        
        # Atalho de busca
        search_frame = ttk.Frame(hotkeys_card, style="TFrame")
        search_frame.pack(fill=tk.X, pady=(0, 16))
        
        ttk.Label(search_frame, text="🔍 Buscar no Histórico", style="Card.TLabel").pack(anchor="w", pady=(0, 6))
        self.var_hotkey_search = tk.StringVar(
            value=self.current_settings.get("hotkey_search_history", "ctrl+shift+f"))
        self.var_hotkey_search.trace_add("write", lambda *args: self._mark_needs_restart())
        
        search_entry = Windows11Style.create_modern_entry(search_frame, textvariable=self.var_hotkey_search, width=30)
        search_entry.pack(fill=tk.X)
        
        # Atalho de refresh
        refresh_frame = ttk.Frame(hotkeys_card, style="TFrame")
        refresh_frame.pack(fill=tk.X)
        
        ttk.Label(refresh_frame, text="🔄 Recarregar Menu", style="Card.TLabel").pack(anchor="w", pady=(0, 6))
        self.var_hotkey_refresh = tk.StringVar(
            value=self.current_settings.get("hotkey_refresh_menu", "ctrl+shift+r"))
        self.var_hotkey_refresh.trace_add("write", lambda *args: self._mark_needs_restart())
        
        refresh_entry = Windows11Style.create_modern_entry(refresh_frame, textvariable=self.var_hotkey_refresh, width=30)
        refresh_entry.pack(fill=tk.X)
        
        # Card de orientações
        guide_card = Windows11Style.create_modern_card(tab, padding=20)
        guide_card.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(guide_card, text="💡 Orientações", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 12))
        
        guide_text = (
            "✅ Combinações recomendadas:\n"
            "   • ctrl+shift+letra (ex: ctrl+shift+f)\n"
            "   • ctrl+alt+letra (ex: ctrl+alt+h)\n"
            "   • alt+shift+letra (ex: alt+shift+s)\n\n"
            "⚠️ Evite conflitos com atalhos já utilizados por outros programas"
        )
        
        ttk.Label(guide_card, text=guide_text, style="Card.TLabel").pack(anchor="w")
        
        # Card de atalhos reservados
        reserved_card = Windows11Style.create_modern_card(tab, padding=20)
        reserved_card.pack(fill=tk.X)
        
        ttk.Label(reserved_card, text="🚫 Atalhos Reservados", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 12))
        
        ttk.Label(reserved_card, text="Os seguintes atalhos são reservados pelo sistema e não podem ser alterados:", 
                 style="Card.TLabel").pack(anchor="w", pady=(0, 8))
        
        reserved_text = "Ctrl+C • Ctrl+V • Ctrl+X • Ctrl+A • Ctrl+Z"
        ttk.Label(reserved_card, text=reserved_text, font=("Consolas", 10, "bold"), 
                 style="Card.TLabel").pack(anchor="w")
        
        # Aviso de reinicialização
        restart_card = Windows11Style.create_modern_card(tab, padding=16)
        restart_card.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Label(restart_card, text="⚠️ Alterações nestes atalhos requerem reinicialização da aplicação", 
                 font=("Segoe UI", 9, "bold"), foreground=Windows11Style.COLORS['warning'], 
                 style="Card.TLabel").pack(anchor="w")
    
    def _create_modern_info_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba moderna de informações sobre o aplicativo"""
        tab = Windows11Style.create_modern_card(notebook, padding=24)
        notebook.add(tab, text="ℹ️ Sobre")
        
        # Cabeçalho principal
        header_frame = ttk.Frame(tab, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 24))
        
        title_label = ttk.Label(header_frame, text="🚀 Dahora App", style="Title.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(header_frame, text="Sistema avançado de timestamps com total liberdade de configuração", 
                                 style="Subtitle.TLabel")
        subtitle_label.pack(anchor="w", pady=(4, 0))
        
        # Card de destaque
        highlight_card = Windows11Style.create_modern_card(tab, padding=20)
        highlight_card.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(highlight_card, text="✨ Total Liberdade de Configuração", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 12))
        
        freedom_text = (
            "Nenhum atalho é fixo neste aplicativo! Você tem controle total sobre:\n"
            "• Todas as combinações de teclas\n"
            "• Todos os prefixos e formatos\n"
            "• Todas as configurações de comportamento"
        )
        
        ttk.Label(highlight_card, text=freedom_text, style="Card.TLabel").pack(anchor="w")
        
        # Card de recursos
        features_card = Windows11Style.create_modern_card(tab, padding=20)
        features_card.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(features_card, text="🎯 Recursos Principais", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 12))
        
        features_text = (
            "✅ Atalhos personalizados ilimitados\n"
            "✅ Prefixos customizados por atalho\n"
            "✅ Formato de data/hora totalmente configurável\n"
            "✅ Caracteres de delimitação ajustáveis\n"
            "✅ Histórico inteligente de clipboard\n"
            "✅ Notificações personalizáveis\n"
            "✅ Interface moderna e responsiva\n"
            "✅ Tema automático (claro/escuro)"
        )
        
        ttk.Label(features_card, text=features_text, style="Card.TLabel").pack(anchor="w")
        
        # Card de dicas
        tips_card = Windows11Style.create_modern_card(tab, padding=20)
        tips_card.pack(fill=tk.X)
        
        ttk.Label(tips_card, text="💡 Dicas de Uso", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 12))
        
        tips_text = (
            "🎯 Configure quantos atalhos quiser na aba 'Atalhos Personalizados'\n"
            "⌨️ Use combinações como ctrl+shift+letra para evitar conflitos\n"
            "🔄 Cada atalho pode ser habilitado/desabilitado individualmente\n"
            "📋 O histórico mantém os últimos 100 itens copiados\n"
            "🔍 Use Ctrl+Shift+F para buscar no histórico rapidamente"
        )
        
        ttk.Label(tips_card, text=tips_text, style="Card.TLabel").pack(anchor="w")
    
    def _refresh_list(self) -> None:
        """Atualiza a Listbox com dados dos atalhos em formato moderno"""
        if not hasattr(self, 'shortcuts_listbox') or not self.shortcuts_listbox:
            return
        
        # Limpa listbox
        self.shortcuts_listbox.delete(0, tk.END)
        
        # Popula listbox com formato moderno
        for shortcut in self.shortcuts_data:
            status_icon = "✅" if shortcut.get("enabled", True) else "⏸️"
            hotkey = shortcut.get("hotkey", "").upper()
            prefix = shortcut.get("prefix", "")
            description = shortcut.get("description", "")
            
            # Formato moderno: ✅ CTRL+SHIFT+1 → dahora - Prefixo principal
            if description:
                display = f"{status_icon} {hotkey} → {prefix} - {description}"
            else:
                display = f"{status_icon} {hotkey} → {prefix}"
            
            self.shortcuts_listbox.insert(tk.END, display)
        
        # Atualiza contagem com texto moderno
        if hasattr(self, 'count_label'):
            count = len(self.shortcuts_data)
            if count == 0:
                self.count_label.config(text="Nenhum atalho configurado")
            elif count == 1:
                self.count_label.config(text="1 atalho configurado")
            else:
                self.count_label.config(text=f"{count} atalhos configurados")
    
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
        try:
            logging.info("=== Botão Adicionar clicado ===")
            logging.info(f"Window exists: {self.window is not None}")
            if self.window:
                try:
                    logging.info(f"Window is valid: {self.window.winfo_exists()}")
                except tk.TclError as e:
                    logging.error(f"Window validation failed: {e}")
            
            self._show_editor_dialog()
            logging.info("=== _show_editor_dialog() retornou ===")
        except Exception as e:
            logging.error(f"Erro no _on_add_clicked: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            if self.notification_callback:
                self.notification_callback("Erro", f"Erro ao adicionar: {str(e)}")
    
    def _on_edit_clicked(self) -> None:
        """Callback para editar shortcut selecionado (usando Listbox)"""
        try:
            logging.info("=== Botão Editar clicado ===")
            
            if not hasattr(self, 'shortcuts_listbox') or not self.shortcuts_listbox:
                logging.error("shortcuts_listbox não existe")
                return
            
            selection = self.shortcuts_listbox.curselection()
            logging.info(f"Seleção atual: {selection}")
            
            if not selection:
                logging.warning("Nenhum atalho selecionado")
                messagebox.showwarning("Aviso", "Selecione um atalho para editar")
                return
            
            idx = selection[0]
            logging.info(f"Índice selecionado: {idx}, total de atalhos: {len(self.shortcuts_data)}")
            
            if idx >= len(self.shortcuts_data):
                logging.error(f"Índice {idx} fora do range")
                return
            
            shortcut_data = self.shortcuts_data[idx]
            logging.info(f"Dados do atalho selecionado: {shortcut_data}")
            
            logging.info(f"Window exists: {self.window is not None}")
            if self.window:
                try:
                    logging.info(f"Window is valid: {self.window.winfo_exists()}")
                except tk.TclError as e:
                    logging.error(f"Window validation failed: {e}")
            
            self._show_editor_dialog(shortcut_data)
            logging.info("=== _show_editor_dialog() retornou ===")
            
        except Exception as e:
            logging.error(f"Erro no _on_edit_clicked: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            if self.notification_callback:
                self.notification_callback("Erro", f"Erro ao editar: {str(e)}")
    
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
        try:
            logging.info(f"=== _show_editor_dialog iniciado ===")
            logging.info(f"Shortcut data: {shortcut}")
            
            if not self.window:
                logging.error("Janela principal não existe")
                if self.notification_callback:
                    self.notification_callback("Erro", "Janela principal não encontrada")
                return
            
            # Verifica se a janela principal ainda está válida
            try:
                exists = self.window.winfo_exists()
                logging.info(f"Janela principal existe: {exists}")
                if not exists:
                    raise tk.TclError("Window does not exist")
            except tk.TclError as e:
                logging.error(f"Janela principal não é mais válida: {e}")
                if self.notification_callback:
                    self.notification_callback("Erro", "Janela principal não é mais válida")
                return
            
            logging.info("Criando ShortcutEditorDialog...")
            editor = ShortcutEditorDialog(
                parent=self.window,
                shortcut=shortcut,
                on_save=self._on_editor_save,
                on_validate_hotkey=self.on_validate_hotkey_callback
            )
            logging.info("ShortcutEditorDialog criado com sucesso")
            
            logging.info("Chamando editor.show()...")
            editor.show()
            logging.info("editor.show() retornou com sucesso")
            
        except Exception as e:
            logging.error(f"=== ERRO em _show_editor_dialog ===")
            logging.error(f"Erro: {e}")
            import traceback
            logging.error(f"Traceback completo:\n{traceback.format_exc()}")
            
            if self.notification_callback:
                self.notification_callback("Erro", f"Erro ao abrir editor:\n{str(e)}")
            else:
                import tkinter.messagebox as mb
                mb.showerror("Erro", f"Erro ao abrir editor de atalho:\n{str(e)}")
        finally:
            logging.info("=== _show_editor_dialog finalizado ===")
    
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
