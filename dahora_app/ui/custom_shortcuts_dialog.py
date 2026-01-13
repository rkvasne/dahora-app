"""
Gerenciador de Atalhos Personalizados - Dialog de Configurações com CRUD
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from dahora_app.utils import format_hotkey_display
from dahora_app.constants import RESERVED_HOTKEYS_BASE
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
        self.shortcuts_listbox: Optional[tk.Listbox] = (
            None  # Listbox simples (como search_dialog)
        )
        self.shortcuts_data: List[Dict[str, Any]] = []
        self.current_settings: Dict[str, Any] = {}  # Para armazenar todas as configs

        # Callbacks
        self.on_save_callback: Optional[Callable] = None
        self.on_add_callback: Optional[Callable] = None
        self.on_update_callback: Optional[Callable] = None
        self.on_remove_callback: Optional[Callable] = None
        self.on_validate_hotkey_callback: Optional[Callable] = None
        self.on_get_settings_callback: Optional[Callable] = (
            None  # Para recarregar dados frescos
        )
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
        """Cria a janela principal com design moderno - ESTRUTURA CORRETA"""
        self.window = tk.Tk()
        # Configura estilo moderno
        Windows11Style.configure_window(
            self.window, "Dahora App - Configurações", "850x700"
        )
        Windows11Style.configure_styles(self.window)

        self.window.resizable(True, True)
        self.window.minsize(700, 500)

        # ========================================
        # ESTRUTURA CORRETA: Header + Tabs FIXOS, Conteúdo SCROLLÁVEL
        # ========================================

        # Container principal
        main_container = ttk.Frame(self.window, style="TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)

        # === HEADER FIXO (não rola) ===
        header_frame = ttk.Frame(main_container, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = ttk.Label(
            header_frame, text="⚙️ Configurações do Dahora App", style="Title.TLabel"
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header_frame,
            text="Personalize atalhos, formatos e preferências",
            style="Muted.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))

        # === NOTEBOOK FIXO (tabs não rolam) ===
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Cria as abas com scroll interno
        self._create_scrollable_prefixes_tab(notebook)
        self._create_scrollable_general_tab(notebook)
        self._create_scrollable_notifications_tab(notebook)
        self._create_scrollable_hotkeys_tab(notebook)
        self._create_scrollable_info_tab(notebook)

        # Aviso de reinicialização
        self.restart_warning_label = ttk.Label(
            main_container,
            text="⚠️ Reinicialização necessária para aplicar algumas mudanças",
            font=("Segoe UI", 10, "bold"),
            foreground=Windows11Style.COLORS["warning"],
            background=Windows11Style.COLORS["bg"],
        )

        # === BOTÕES FIXOS (não rolam) ===
        buttons_frame = ttk.Frame(main_container, style="TFrame")
        buttons_frame.pack(fill=tk.X, pady=(0, 0))

        cancel_btn = Windows11Style.create_modern_button(
            buttons_frame, "Cancelar", command=self._on_close
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(16, 0))

        ok_btn = Windows11Style.create_modern_button(
            buttons_frame,
            "Salvar",
            command=self._on_save_and_close,
            style="Primary.TButton",
        )
        ok_btn.pack(side=tk.RIGHT)

        # Protocolo de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

        # Centraliza janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")

        # Atalhos de teclado
        self.window.bind("<Escape>", lambda e: self._on_close())

        self.window.mainloop()

    def _create_scrollable_frame(self, parent) -> tuple:
        """Cria um frame scrollável para conteúdo de aba - SEM scrollbar visível"""
        # Canvas para scroll
        canvas: Any = tk.Canvas(
            parent,
            bg=Windows11Style.COLORS["bg"],
            highlightthickness=0,
            borderwidth=0,
        )

        # Frame scrollável
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        # Configura scroll
        def configure_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", configure_scroll)

        canvas_frame = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )

        # Ajusta largura do frame ao canvas
        def configure_frame_width(event):
            canvas.itemconfig(canvas_frame, width=event.width)

        canvas.bind("<Configure>", configure_frame_width)

        # Pack - SEM scrollbar visível
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Mouse wheel scroll - CORRIGIDO para funcionar em todas as abas
        def _on_mousewheel(event):
            # Verifica se o canvas ainda existe
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass

        # Bind no canvas E no frame scrollável
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        # Bind em todos os widgets filhos quando criados
        def bind_mousewheel_to_children(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel_to_children(child)

        # Armazena referência para bind posterior
        canvas._mousewheel_callback = _on_mousewheel
        canvas._bind_children = bind_mousewheel_to_children

        return scrollable_frame, canvas

    def _create_scrollable_prefixes_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de atalhos com scroll interno"""
        tab_container = ttk.Frame(notebook, style="TFrame")
        notebook.add(tab_container, text="  🎯 Atalhos  ")

        scrollable_frame, canvas = self._create_scrollable_frame(tab_container)

        # Conteúdo da aba
        content = ttk.Frame(scrollable_frame, style="TFrame", padding=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(content, text="Atalhos Configurados", style="Heading.TLabel").pack(
            anchor="w", pady=(0, 8)
        )
        ttk.Label(
            content, text="Gerencie seus atalhos personalizados", style="Muted.TLabel"
        ).pack(anchor="w", pady=(0, 16))

        # Lista de atalhos
        list_frame = ttk.Frame(content, style="TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        self.shortcuts_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 10),
            height=10,
            borderwidth=0,
            highlightthickness=0,
            selectmode=tk.SINGLE,
            relief="flat",
        )
        Windows11Style.configure_listbox(self.shortcuts_listbox)
        self.shortcuts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.shortcuts_listbox.bind(
            "<Double-Button-1>", lambda e: self._on_edit_clicked()
        )

        # Contador
        self.count_label = ttk.Label(
            content, text="0 atalhos configurados", style="Muted.TLabel"
        )
        self.count_label.pack(anchor="w", pady=(0, 16))

        self._refresh_list()

        # Botões
        buttons = ttk.Frame(content, style="TFrame")
        buttons.pack(fill=tk.X)

        Windows11Style.create_modern_button(
            buttons,
            "➕ Adicionar",
            command=self._on_add_clicked,
            style="Primary.TButton",
        ).pack(side=tk.LEFT, padx=(0, 8))
        Windows11Style.create_modern_button(
            buttons, "✏️ Editar", command=self._on_edit_clicked
        ).pack(side=tk.LEFT, padx=(0, 8))
        Windows11Style.create_modern_button(
            buttons,
            "🗑️ Remover",
            command=self._on_remove_clicked,
            style="Danger.TButton",
        ).pack(side=tk.LEFT)
        Windows11Style.create_modern_button(
            buttons, "🔄", command=self._refresh_list
        ).pack(side=tk.RIGHT)

        # Bind mousewheel em todos os filhos
        if hasattr(canvas, "_bind_children"):
            content.after(100, lambda: canvas._bind_children(content))

    def _create_scrollable_general_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de formato com scroll interno"""
        tab_container = ttk.Frame(notebook, style="TFrame")
        notebook.add(tab_container, text="  📅 Formato  ")

        scrollable_frame, canvas = self._create_scrollable_frame(tab_container)

        content = ttk.Frame(scrollable_frame, style="TFrame", padding=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(content, text="Formato de Data e Hora", style="Heading.TLabel").pack(
            anchor="w", pady=(0, 8)
        )
        ttk.Label(
            content,
            text="Configure como a data e hora serão formatadas",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(0, 20))

        # Formato
        ttk.Label(content, text="Formato de Data/Hora", style="TLabel").pack(
            anchor="w", pady=(0, 6)
        )
        self.var_datetime_format = tk.StringVar(
            value=self.current_settings.get("datetime_format", "%d.%m.%Y-%H:%M")
        )
        format_entry = ttk.Entry(
            content, textvariable=self.var_datetime_format, width=40
        )
        format_entry.pack(fill=tk.X, pady=(0, 16))

        # Ajuda
        help_text = "Códigos: %d=dia, %m=mês, %Y=ano, %H=hora, %M=minuto, %S=segundo"
        ttk.Label(content, text=help_text, style="Muted.TLabel").pack(
            anchor="w", pady=(0, 24)
        )

        # Delimitadores
        ttk.Label(
            content, text="Caracteres de Delimitação", style="Heading.TLabel"
        ).pack(anchor="w", pady=(0, 16))

        delim_frame = ttk.Frame(content, style="TFrame")
        delim_frame.pack(fill=tk.X, pady=(0, 24))

        # Abertura
        open_frame = ttk.Frame(delim_frame, style="TFrame")
        open_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 16))
        ttk.Label(open_frame, text="Abertura", style="TLabel").pack(
            anchor="w", pady=(0, 6)
        )
        self.var_bracket_open = tk.StringVar(
            value=self.current_settings.get("bracket_open", "[")
        )
        ttk.Entry(open_frame, textvariable=self.var_bracket_open, width=10).pack(
            anchor="w"
        )

        # Fechamento
        close_frame = ttk.Frame(delim_frame, style="TFrame")
        close_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(close_frame, text="Fechamento", style="TLabel").pack(
            anchor="w", pady=(0, 6)
        )
        self.var_bracket_close = tk.StringVar(
            value=self.current_settings.get("bracket_close", "]")
        )
        ttk.Entry(close_frame, textvariable=self.var_bracket_close, width=10).pack(
            anchor="w"
        )

        # Histórico
        ttk.Label(
            content, text="Configurações de Histórico", style="Heading.TLabel"
        ).pack(anchor="w", pady=(0, 16))

        ttk.Label(content, text="Máximo de itens no histórico", style="TLabel").pack(
            anchor="w", pady=(0, 6)
        )
        self.var_max_history = tk.IntVar(
            value=self.current_settings.get("max_history_items", 100)
        )
        ttk.Spinbox(
            content, from_=10, to=1000, textvariable=self.var_max_history, width=15
        ).pack(anchor="w", pady=(0, 16))

        ttk.Label(
            content, text="Intervalo de monitoramento (segundos)", style="TLabel"
        ).pack(anchor="w", pady=(0, 6))
        self.var_monitor_interval = tk.DoubleVar(
            value=self.current_settings.get("clipboard_monitor_interval", 3.0)
        )
        ttk.Spinbox(
            content,
            from_=0.5,
            to=60.0,
            increment=0.5,
            textvariable=self.var_monitor_interval,
            width=15,
        ).pack(anchor="w", pady=(0, 16))

        ttk.Label(
            content,
            text="Tempo sem mudanças na área de transferência (segundos)",
            style="TLabel",
        ).pack(anchor="w", pady=(0, 6))
        self.var_idle_threshold = tk.DoubleVar(
            value=self.current_settings.get("clipboard_idle_threshold", 30.0)
        )
        ttk.Spinbox(
            content,
            from_=5,
            to=300,
            increment=5,
            textvariable=self.var_idle_threshold,
            width=15,
        ).pack(anchor="w")

        # Bind mousewheel
        if hasattr(canvas, "_bind_children"):
            content.after(100, lambda: canvas._bind_children(content))

    def _create_scrollable_notifications_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de notificações com scroll interno"""
        tab_container = ttk.Frame(notebook, style="TFrame")
        notebook.add(tab_container, text="  🔔 Notificações  ")

        scrollable_frame, canvas = self._create_scrollable_frame(tab_container)

        content = ttk.Frame(scrollable_frame, style="TFrame", padding=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(
            content, text="Configurações de Notificações", style="Heading.TLabel"
        ).pack(anchor="w", pady=(0, 8))
        ttk.Label(
            content,
            text="Configure como e quando as notificações serão exibidas",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(0, 20))

        # Toggle
        self.var_notifications_enabled = tk.BooleanVar(
            value=self.current_settings.get("notification_enabled", True)
        )
        ttk.Checkbutton(
            content,
            text="🔔 Habilitar notificações do Windows",
            variable=self.var_notifications_enabled,
        ).pack(anchor="w", pady=(0, 8))
        ttk.Label(
            content,
            text="Exibe notificações quando atalhos são acionados",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(0, 24))

        # Duração
        ttk.Label(content, text="Duração da Notificação", style="Heading.TLabel").pack(
            anchor="w", pady=(0, 16)
        )

        duration_frame = ttk.Frame(content, style="TFrame")
        duration_frame.pack(fill=tk.X, pady=(0, 24))

        self.var_notification_duration = tk.IntVar(
            value=self.current_settings.get("notification_duration", 2)
        )
        ttk.Spinbox(
            duration_frame,
            from_=1,
            to=10,
            textvariable=self.var_notification_duration,
            width=10,
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Label(duration_frame, text="segundos", style="TLabel").pack(side=tk.LEFT)

        # Tipos
        ttk.Label(
            content, text="💡 Tipos de Notificações", style="Heading.TLabel"
        ).pack(anchor="w", pady=(0, 12))
        examples = "• Atalho acionado: 'Copiado com sucesso!'\n• Item do histórico: 'Copiado do histórico!'\n• Configurações: 'Configurações salvas!'"
        ttk.Label(content, text=examples, style="Muted.TLabel").pack(anchor="w")

        # Bind mousewheel
        if hasattr(canvas, "_bind_children"):
            content.after(100, lambda: canvas._bind_children(content))

    def _create_scrollable_hotkeys_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de teclas de atalho com scroll interno"""
        tab_container = ttk.Frame(notebook, style="TFrame")
        notebook.add(tab_container, text="  ⌨️ Teclas  ")

        scrollable_frame, canvas = self._create_scrollable_frame(tab_container)

        content = ttk.Frame(scrollable_frame, style="TFrame", padding=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(content, text="Atalhos do Sistema", style="Heading.TLabel").pack(
            anchor="w", pady=(0, 8)
        )
        ttk.Label(
            content,
            text="Configure os atalhos globais para funções do sistema",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(0, 20))

        # Busca
        ttk.Label(content, text="🔍 Buscar no Histórico", style="TLabel").pack(
            anchor="w", pady=(0, 6)
        )
        self.var_hotkey_search = tk.StringVar(
            value=self.current_settings.get("hotkey_search_history", "ctrl+shift+f")
        )
        self.var_hotkey_search.trace_add(
            "write", lambda *args: self._mark_needs_restart()
        )
        ttk.Entry(content, textvariable=self.var_hotkey_search, width=30).pack(
            fill=tk.X, pady=(0, 16)
        )

        # Refresh
        ttk.Label(content, text="🔄 Recarregar Menu", style="TLabel").pack(
            anchor="w", pady=(0, 6)
        )
        self.var_hotkey_refresh = tk.StringVar(
            value=self.current_settings.get("hotkey_refresh_menu", "ctrl+shift+r")
        )
        self.var_hotkey_refresh.trace_add(
            "write", lambda *args: self._mark_needs_restart()
        )
        ttk.Entry(content, textvariable=self.var_hotkey_refresh, width=30).pack(
            fill=tk.X, pady=(0, 24)
        )

        # Orientações
        ttk.Label(content, text="💡 Orientações", style="Heading.TLabel").pack(
            anchor="w", pady=(0, 12)
        )
        guide = "✅ Combinações recomendadas:\n   • ctrl+shift+letra\n   • ctrl+alt+letra\n   • alt+shift+letra"
        ttk.Label(content, text=guide, style="Muted.TLabel").pack(
            anchor="w", pady=(0, 24)
        )

        # Reservados
        ttk.Label(content, text="🚫 Atalhos Reservados", style="Heading.TLabel").pack(
            anchor="w", pady=(0, 12)
        )
        reserved_display = " • ".join(
            format_hotkey_display(h) for h in RESERVED_HOTKEYS_BASE
        )
        ttk.Label(
            content,
            text=reserved_display,
            font=("Consolas", 10),
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(0, 16))

        # Aviso
        ttk.Label(
            content,
            text="⚠️ Alterações requerem reinicialização",
            font=("Segoe UI", 9, "bold"),
            foreground=Windows11Style.COLORS["warning"],
            background=Windows11Style.COLORS["bg"],
        ).pack(anchor="w")

        # Bind mousewheel
        if hasattr(canvas, "_bind_children"):
            content.after(100, lambda: canvas._bind_children(content))

    def _create_scrollable_info_tab(self, notebook: ttk.Notebook) -> None:
        """Cria aba de informações com scroll interno"""
        tab_container = ttk.Frame(notebook, style="TFrame")
        notebook.add(tab_container, text="  ℹ️ Sobre  ")

        scrollable_frame, canvas = self._create_scrollable_frame(tab_container)

        content = ttk.Frame(scrollable_frame, style="TFrame", padding=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(content, text="🚀 Dahora App", style="Title.TLabel").pack(
            anchor="w", pady=(0, 8)
        )
        ttk.Label(
            content,
            text="Sistema avançado de timestamps com total liberdade de configuração",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(0, 24))

        # Destaque
        ttk.Label(
            content, text="✨ Total Liberdade de Configuração", style="Heading.TLabel"
        ).pack(anchor="w", pady=(0, 12))
        freedom = "Nenhum atalho é fixo! Você tem controle total sobre:\n• Todas as combinações de teclas\n• Todos os prefixos e formatos\n• Todas as configurações"
        ttk.Label(content, text=freedom, style="Muted.TLabel").pack(
            anchor="w", pady=(0, 24)
        )

        # Recursos
        ttk.Label(content, text="🎯 Recursos Principais", style="Heading.TLabel").pack(
            anchor="w", pady=(0, 12)
        )
        features = "✅ Atalhos personalizados ilimitados\n✅ Prefixos customizados por atalho\n✅ Formato de data/hora configurável\n✅ Histórico inteligente da área de transferência\n✅ Notificações personalizáveis\n✅ Tema automático (claro/escuro)"
        ttk.Label(content, text=features, style="Muted.TLabel").pack(
            anchor="w", pady=(0, 24)
        )

        # Dicas
        ttk.Label(content, text="💡 Dicas de Uso", style="Heading.TLabel").pack(
            anchor="w", pady=(0, 12)
        )
        tips = "🎯 Configure atalhos na aba 'Atalhos'\n⌨️ Use ctrl+shift+letra para evitar conflitos\n🔍 Use Ctrl+Shift+F para buscar no histórico"
        ttk.Label(content, text=tips, style="Muted.TLabel").pack(anchor="w")

        # Bind mousewheel
        if hasattr(canvas, "_bind_children"):
            content.after(100, lambda: canvas._bind_children(content))

    def _refresh_list(self) -> None:
        """Atualiza a Listbox com dados dos atalhos em formato moderno"""
        if not hasattr(self, "shortcuts_listbox") or not self.shortcuts_listbox:
            return

        # Limpa listbox
        self.shortcuts_listbox.delete(0, tk.END)

        # Popula listbox com formato moderno
        for shortcut in self.shortcuts_data:
            status_icon = "✅" if shortcut.get("enabled", True) else "⏸️"
            hotkey = format_hotkey_display(shortcut.get("hotkey", ""))
            prefix = shortcut.get("prefix", "")
            description = shortcut.get("description", "")

            # Formato moderno: ✅ CTRL+SHIFT+1 → dahora - Prefixo principal
            if description:
                display = f"{status_icon} {hotkey} → {prefix} - {description}"
            else:
                display = f"{status_icon} {hotkey} → {prefix}"

            self.shortcuts_listbox.insert(tk.END, display)

        # Atualiza contagem com texto moderno
        if hasattr(self, "count_label"):
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
                self.restart_warning_label.pack(
                    fill=tk.X,
                    pady=(8, 0),
                    before=self.restart_warning_label.master.winfo_children()[-1],
                )

    def _on_save_all(self) -> None:
        """Salva todas as configurações (tabs Geral e Notificações)"""
        try:
            if self.on_save_callback:
                max_history_items = (
                    self.var_max_history.get() if self.var_max_history else 100
                )
                try:
                    max_history_items = int(max_history_items)
                except Exception:
                    max_history_items = 100
                if max_history_items < 10:
                    max_history_items = 10
                if max_history_items > 1000:
                    max_history_items = 1000
                if self.var_max_history:
                    self.var_max_history.set(max_history_items)

                clipboard_monitor_interval = (
                    self.var_monitor_interval.get()
                    if self.var_monitor_interval
                    else 3.0
                )
                try:
                    clipboard_monitor_interval = float(clipboard_monitor_interval)
                except Exception:
                    clipboard_monitor_interval = 3.0
                if clipboard_monitor_interval < 0.5:
                    clipboard_monitor_interval = 0.5
                if clipboard_monitor_interval > 60.0:
                    clipboard_monitor_interval = 60.0
                if self.var_monitor_interval:
                    self.var_monitor_interval.set(clipboard_monitor_interval)

                clipboard_idle_threshold = (
                    self.var_idle_threshold.get() if self.var_idle_threshold else 30.0
                )
                try:
                    clipboard_idle_threshold = float(clipboard_idle_threshold)
                except Exception:
                    clipboard_idle_threshold = 30.0
                if clipboard_idle_threshold < 5.0:
                    clipboard_idle_threshold = 5.0
                if clipboard_idle_threshold > 300.0:
                    clipboard_idle_threshold = 300.0
                if self.var_idle_threshold:
                    self.var_idle_threshold.set(clipboard_idle_threshold)

                notification_duration = (
                    self.var_notification_duration.get()
                    if self.var_notification_duration
                    else 2
                )
                try:
                    notification_duration = int(notification_duration)
                except Exception:
                    notification_duration = 2
                if notification_duration < 1:
                    notification_duration = 1
                if notification_duration > 10:
                    notification_duration = 10
                if self.var_notification_duration:
                    self.var_notification_duration.set(notification_duration)

                bracket_open = (
                    self.var_bracket_open.get() if self.var_bracket_open else "["
                )
                bracket_close = (
                    self.var_bracket_close.get() if self.var_bracket_close else "]"
                )
                bracket_open = str(bracket_open).strip()
                bracket_close = str(bracket_close).strip()
                if len(bracket_open) != 1 or bracket_open in "\n\r\t":
                    bracket_open = "["
                if len(bracket_close) != 1 or bracket_close in "\n\r\t":
                    bracket_close = "]"
                if bracket_open == bracket_close:
                    if bracket_open != "]":
                        bracket_close = "]"
                    else:
                        bracket_close = "["
                if self.var_bracket_open:
                    self.var_bracket_open.set(bracket_open)
                if self.var_bracket_close:
                    self.var_bracket_close.set(bracket_close)

                settings = {
                    "datetime_format": (
                        self.var_datetime_format.get().strip()
                        if self.var_datetime_format
                        else "%d.%m.%Y-%H:%M"
                    ),
                    "bracket_open": bracket_open,
                    "bracket_close": bracket_close,
                    "max_history_items": max_history_items,
                    "clipboard_monitor_interval": clipboard_monitor_interval,
                    "clipboard_idle_threshold": clipboard_idle_threshold,
                    "notification_enabled": (
                        self.var_notifications_enabled.get()
                        if self.var_notifications_enabled
                        else True
                    ),
                    "notification_duration": notification_duration,
                    "hotkey_search_history": (
                        self.var_hotkey_search.get().strip()
                        if self.var_hotkey_search
                        else "ctrl+shift+f"
                    ),
                    "hotkey_refresh_menu": (
                        self.var_hotkey_refresh.get().strip()
                        if self.var_hotkey_refresh
                        else "ctrl+shift+r"
                    ),
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
                icon="warning",
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
                        "Configurações salvas!\n\nLembre-se de reiniciar para aplicar as mudanças.",
                    )
        else:
            if self.notification_callback:
                self.notification_callback(
                    "Dahora App", "Configurações salvas com sucesso!"
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

            if not hasattr(self, "shortcuts_listbox") or not self.shortcuts_listbox:
                logging.error("shortcuts_listbox não existe")
                return

            selection = self.shortcuts_listbox.curselection()
            logging.info(f"Seleção atual: {selection}")

            if not selection:
                logging.warning("Nenhum atalho selecionado")
                messagebox.showwarning("Aviso", "Selecione um atalho para editar")
                return

            idx = selection[0]
            logging.info(
                f"Índice selecionado: {idx}, total de atalhos: {len(self.shortcuts_data)}"
            )

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
        if not hasattr(self, "shortcuts_listbox") or not self.shortcuts_listbox:
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
        hotkey = format_hotkey_display(shortcut.get("hotkey", ""))

        confirm = messagebox.askyesno(
            "Confirmar Remoção",
            f"Deseja remover o atalho?\n\n" f"Hotkey: {hotkey}\n" f"Prefixo: {prefix}",
        )

        if confirm and self.on_remove_callback:
            success, msg = self.on_remove_callback(shortcut_id)
            if success:
                self._reload_from_settings()
                if self.notification_callback:
                    self.notification_callback(
                        "Dahora App", "Atalho removido com sucesso!"
                    )
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
                    self.notification_callback(
                        "Erro", "Janela principal não encontrada"
                    )
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
                    self.notification_callback(
                        "Erro", "Janela principal não é mais válida"
                    )
                return

            logging.info("Criando ShortcutEditorDialog...")
            editor = ShortcutEditorDialog(
                parent=self.window,
                shortcut=shortcut,
                on_save=self._on_editor_save,
                on_validate_hotkey=self.on_validate_hotkey_callback,
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
                        shortcut_data.get("enabled", True),
                    )

                    if success:
                        self._reload_from_settings()
                        if self.notification_callback:
                            self.notification_callback(
                                "Dahora App", "Atalho adicionado com sucesso!"
                            )
                    else:
                        messagebox.showerror(
                            "Erro", f"Falha ao adicionar atalho:\n{msg}"
                        )
            else:
                if self.on_update_callback:
                    success, msg = self.on_update_callback(
                        shortcut_data["id"],
                        hotkey=shortcut_data.get("hotkey"),
                        prefix=shortcut_data.get("prefix"),
                        description=shortcut_data.get("description"),
                        enabled=shortcut_data.get("enabled"),
                    )

                    if success:
                        self._reload_from_settings()
                        if self.notification_callback:
                            self.notification_callback(
                                "Dahora App", "Atalho atualizado com sucesso!"
                            )
                    else:
                        messagebox.showerror(
                            "Erro", f"Falha ao atualizar atalho:\n{msg}"
                        )
        except Exception as e:
            logging.error(f"Erro ao salvar: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")
