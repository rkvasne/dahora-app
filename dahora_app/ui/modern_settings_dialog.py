"""
Dialog de Configurações Moderno usando CustomTkinter
Interface Windows 11 com cantos arredondados e componentes modernos
"""
import customtkinter as ctk
from typing import Callable, Optional, List, Dict, Any
import logging
import time
import tkinter as tk
from tkinter import messagebox

from dahora_app.ui.modern_styles import (
    ModernTheme, ModernWindow, ModernFrame, ModernButton, 
    ModernEntry, ModernLabel, ModernCheckbox, ModernSpinbox,
    ModernScrollableFrame
)

from dahora_app.utils import format_hotkey_display


class ModernSettingsDialog:
    """Dialog de configurações moderno com CustomTkinter"""
    
    def __init__(self):
        self.parent: Optional[ctk.CTk] = None
        self.window: Optional[ctk.CTk] = None
        self.shortcuts_data: List[Dict[str, Any]] = []
        self.current_settings: Dict[str, Any] = {}
        
        # Callbacks
        self.on_save_callback: Optional[Callable] = None
        self.on_add_callback: Optional[Callable] = None
        self.on_update_callback: Optional[Callable] = None
        self.on_remove_callback: Optional[Callable] = None
        self.on_validate_hotkey_callback: Optional[Callable] = None
        self.on_get_settings_callback: Optional[Callable] = None
        self._notification_callback: Optional[Callable] = None
        
        # Variáveis
        self.var_datetime_format = None
        self.var_bracket_open = None
        self.var_bracket_close = None
        self.var_max_history = None
        self.var_monitor_interval = None
        self.var_idle_threshold = None
        self.var_notifications_enabled = None
        self.var_notification_duration = None
        self.var_log_max_bytes = None
        self.var_log_backup_count = None
        self.var_ui_prewarm_delay_ms = None
        self.var_tray_menu_cache_window_ms = None
        self.var_hotkey_search = None
        self.var_hotkey_refresh = None
        
        # Estado
        self.needs_restart = False
        self.shortcuts_listbox = None
        self.count_label = None
        self.selected_shortcut_index: int = -1
        self.default_shortcut_id: Optional[int] = None

        # Navigation rail
        self._pages: Dict[str, ctk.CTkFrame] = {}
        self._nav_buttons: Dict[str, Dict[str, Any]] = {}
        self._active_page: str = ""
        self._pages_host: Optional[ctk.CTkFrame] = None

        # Tooltips
        self._tooltip_window: Optional[tk.Toplevel] = None
        self._tooltip_after_id: Optional[str] = None
        
        # Cores
        self.colors = ModernTheme.get_colors()
    
    def set_shortcuts(self, shortcuts: List[Dict[str, Any]]) -> None:
        self.shortcuts_data = shortcuts.copy()
    
    def set_current_settings(self, settings: Dict[str, Any]) -> None:
        self.current_settings = settings.copy()
        self.shortcuts_data = settings.get("custom_shortcuts", [])
        try:
            self.default_shortcut_id = settings.get("default_shortcut_id", None)
        except Exception:
            self.default_shortcut_id = None
    
    def set_on_save_callback(self, callback: Callable) -> None:
        self.on_save_callback = callback
    
    def set_on_add_callback(self, callback: Callable) -> None:
        self.on_add_callback = callback
    
    def set_on_update_callback(self, callback: Callable) -> None:
        self.on_update_callback = callback
    
    def set_on_remove_callback(self, callback: Callable) -> None:
        self.on_remove_callback = callback
    
    def set_on_validate_hotkey_callback(self, callback: Callable) -> None:
        self.on_validate_hotkey_callback = callback
    
    @property
    def notification_callback(self) -> Optional[Callable]:
        return self._notification_callback
    
    @notification_callback.setter
    def notification_callback(self, callback: Optional[Callable]) -> None:
        self._notification_callback = callback
    
    def show(self) -> None:
        """Mostra o dialog"""
        start = time.perf_counter()
        if self.window is not None:
            # Reuso da janela: evita recriar tabs/widgets (bem mais rápido)
            try:
                self.window.deiconify()
            except Exception:
                pass
            t_apply = time.perf_counter()
            self._apply_current_settings_to_controls()
            apply_ms = (time.perf_counter() - t_apply) * 1000

            t_show = time.perf_counter()
            self._show_window()
            show_ms = (time.perf_counter() - t_show) * 1000

            total_ms = (time.perf_counter() - start) * 1000
            logging.info(f"[UI] ModernSettingsDialog.show reuse apply={apply_ms:.1f}ms show={show_ms:.1f}ms total={total_ms:.1f}ms")
            return

        if self.parent is None:
            # Para estabilidade, este diálogo deve ser um Toplevel de um root único.
            raise RuntimeError("ModernSettingsDialog precisa de parent (CTk root) antes de show().")
        
        t_create = time.perf_counter()
        self._create_window()
        create_ms = (time.perf_counter() - t_create) * 1000

        t_apply = time.perf_counter()
        self._apply_current_settings_to_controls()
        apply_ms = (time.perf_counter() - t_apply) * 1000

        t_show = time.perf_counter()
        self._show_window()
        show_ms = (time.perf_counter() - t_show) * 1000

        total_ms = (time.perf_counter() - start) * 1000
        logging.info(f"[UI] ModernSettingsDialog.show create={create_ms:.1f}ms apply={apply_ms:.1f}ms show={show_ms:.1f}ms total={total_ms:.1f}ms")

    def set_parent(self, parent: ctk.CTk) -> None:
        self.parent = parent
    
    def _create_window(self) -> None:
        """Cria a janela principal moderna"""
        # Configura tema
        self.theme = ModernTheme.setup()
        self.colors = ModernTheme.get_colors(self.theme)
        
        # Cria janela (Toplevel do root único)
        self.window = ctk.CTkToplevel(self.parent)
        # Evita efeito "montando a tela" (abas -> botões -> centralização)
        # Monta tudo com a janela oculta e só exibe no final.
        self.window.withdraw()
        self.window.title("Dahora App - Configurações")
        # Ajusta tamanho inicial para caber em telas menores (ex: notebook)
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        # Mais compacto por padrão (mantém espaço suficiente para tabs e ações)
        # Com navigation rail, uma largura maior melhora a leitura e evita apertos.
        width = max(620, min(820, screen_w - 260))
        height = max(500, min(620, screen_h - 220))
        self.window.geometry(f"{width}x{height}")
        self.window.minsize(max(600, min(780, screen_w - 320)), max(460, min(560, screen_h - 300)))
        self.window.configure(fg_color=self.colors['bg'])
        
        # Dark title bar
        if self.theme == "dark":
            try:
                import ctypes
                from ctypes import windll, c_int, byref, sizeof
                self.window.update_idletasks()
                hwnd = windll.user32.GetParent(self.window.winfo_id())
                value = c_int(1)
                windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(value), sizeof(value))
            except Exception:
                pass
        
        # Container principal
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        # Sem padding horizontal externo: permite scrollbar ficar mais no canto da janela
        main_container.pack(fill="both", expand=True, padx=0, pady=12)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10), padx=(12, 8))

        self._create_icon_title_row(header, icon="⚙️", title="Configurações do Dahora App", style="title").pack(anchor="w")
        ModernLabel(header, text="Personalize atalhos, formatos e preferências", 
                   style="muted").pack(anchor="w", pady=(4, 0))

        # Corpo: navigation rail + páginas
        body = ctk.CTkFrame(main_container, fg_color="transparent")
        body.pack(fill="both", expand=True, pady=(0, 10), padx=0)

        rail = ctk.CTkFrame(
            body,
            fg_color=self.colors['bg_secondary'],
            corner_radius=ModernTheme.CORNER_RADIUS,
            border_width=1,
            border_color=self.colors['border'],
            width=170,
        )
        rail.pack(side="left", fill="y", padx=(12, 8), pady=0)
        rail.pack_propagate(False)

        pages_host = ctk.CTkFrame(body, fg_color="transparent")
        pages_host.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self._pages_host = pages_host

        # Páginas (equivalentes às abas antigas)
        self._pages.clear()
        self._nav_buttons.clear()

        self._pages["shortcuts"] = self._create_shortcuts_page(pages_host)

        self._create_nav_button(rail, key="shortcuts", icon="🎯", label="Atalhos")
        self._create_nav_button(rail, key="format", icon="📅", label="Formato")
        self._create_nav_button(rail, key="notifications", icon="🔔", label="Notificações")
        self._create_nav_button(rail, key="hotkeys", icon="⌨️", label="Atalhos")
        self._create_nav_button(rail, key="advanced", icon="🛠️", label="Avançado")
        self._create_nav_button(rail, key="about", icon="ℹ️", label="Sobre")

        # Página inicial
        self._show_page("shortcuts")
        
        # Botões (rodapé): manter no fundo sem reduzir altura dos botões
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        # Mantém o mesmo gutter horizontal das abas (padx=(12, 8))
        buttons_frame.pack(side="bottom", fill="x", padx=(12, 8), pady=(10, 0))

        btn_cancel = ModernButton(
            buttons_frame,
            text="Cancelar",
            command=self._on_close,
            width=112,
            height=ModernTheme.CONTROL_HEIGHT,
        )
        btn_cancel.pack(side="right", padx=(8, 0))
        btn_save = ModernButton(
            buttons_frame,
            text="Salvar",
            style="primary",
            command=self._on_save_and_close,
            width=112,
            height=ModernTheme.CONTROL_HEIGHT,
        )
        btn_save.pack(side="right")

        self._attach_tooltip(btn_save, "Salva as configurações. Atalhos são aplicados automaticamente.")
        
        # Protocolo de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Não exibe aqui; show() chama _show_window() depois.
        
        # Atalhos
        self.window.bind('<Escape>', lambda e: self._on_close())

        # Não chama mainloop aqui: o loop Tk roda uma vez no app.

    def _create_nav_button(self, parent: ctk.CTkFrame, key: str, icon: str, label: str) -> None:
        row = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_secondary'],
            corner_radius=ModernTheme.BUTTON_CORNER_RADIUS,
            height=36,
        )
        row.pack(fill="x", padx=8, pady=4)
        try:
            row.pack_propagate(False)
        except Exception:
            pass

        icon_label = ctk.CTkLabel(
            row,
            text=icon,
            text_color=self.colors['text'],
            # Força fonte de emoji para métricas mais consistentes entre ícones
            font=("Segoe UI Emoji", ModernTheme.FONT_SIZE_BASE),
        )
        # Gap consistente sem forçar largura fixa (emoji podem estourar width e criar “vazio”)
        icon_label.pack(side="left", padx=(10, 6))

        text_label = ctk.CTkLabel(
            row,
            text=label,
            text_color=self.colors['text'],
            font=("Segoe UI", ModernTheme.FONT_SIZE_BASE),
        )
        text_label.pack(side="left")

        def on_click(_e=None, k=key):
            self._show_page(k)

        def on_enter(_e=None, k=key):
            if k == self._active_page:
                row.configure(fg_color=self.colors['accent_hover'])
            else:
                row.configure(fg_color=self.colors['bg_tertiary'])

        def on_leave(_e=None, k=key):
            # volta para o estado aplicado pelo seletor
            self._apply_nav_styles()

        for w in (row, icon_label, text_label):
            try:
                w.bind("<Button-1>", on_click, add=True)
                w.bind("<Enter>", on_enter, add=True)
                w.bind("<Leave>", on_leave, add=True)
            except Exception:
                pass

        self._nav_buttons[key] = {"frame": row, "icon": icon_label, "text": text_label}

    def _apply_nav_styles(self) -> None:
        for key, parts in self._nav_buttons.items():
            frame = parts.get("frame")
            icon_label = parts.get("icon")
            text_label = parts.get("text")
            is_active = key == self._active_page
            if frame is None or icon_label is None or text_label is None:
                continue

            try:
                if is_active:
                    frame.configure(fg_color=self.colors['accent'])
                    icon_label.configure(text_color=self.colors['text_bright'])
                    text_label.configure(text_color=self.colors['text_bright'])
                else:
                    frame.configure(fg_color=self.colors['bg_secondary'])
                    icon_label.configure(text_color=self.colors['text'])
                    text_label.configure(text_color=self.colors['text'])
            except Exception:
                pass

    def _create_icon_title_row(self, parent, icon: str, title: str, style: str = "heading") -> ctk.CTkFrame:
        """Cria um título com ícone e texto em colunas (gap consistente)."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        # Padroniza a fonte do ícone para reduzir variação de largura entre emojis
        base = ModernTheme.FONT_SIZE_BASE
        muted = max(base - 1, 11)
        heading = max(base + 3, 15)
        icon_size = {
            "default": base,
            "muted": muted,
            "heading": heading,
            "title": 19,
        }.get(style, base)

        icon_label = ModernLabel(row, text=icon, style=style, font=("Segoe UI Emoji", icon_size))
        icon_label.pack(side="left", padx=(0, 6))
        ModernLabel(row, text=title, style=style).pack(side="left")
        return row

    def _show_page(self, key: str) -> None:
        if key not in self._pages:
            host = self._pages_host
            if host is None:
                return
            if key == "format":
                self._pages[key] = self._create_format_page(host)
            elif key == "notifications":
                self._pages[key] = self._create_notifications_page(host)
            elif key == "hotkeys":
                self._pages[key] = self._create_hotkeys_page(host)
            elif key == "advanced":
                self._pages[key] = self._create_advanced_page(host)
            elif key == "about":
                self._pages[key] = self._create_about_page(host)
            else:
                return

        for k, page in self._pages.items():
            try:
                page.pack_forget()
            except Exception:
                pass

        self._active_page = key
        try:
            self._pages[key].pack(fill="both", expand=True)
        except Exception:
            pass
        self._apply_nav_styles()

    def _center_window(self) -> None:
        if not self.window:
            return
        self.window.update_idletasks()
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        # Em algumas situações o toplevel ainda não tem size válido
        if w <= 1 or h <= 1:
            try:
                self.window.after(10, self._center_window)
            except Exception:
                pass
            return
        x = (self.window.winfo_screenwidth() // 2) - (w // 2)
        y = (self.window.winfo_screenheight() // 2) - (h // 2)
        self.window.geometry(f"+{x}+{y}")

    def _show_window(self) -> None:
        if not self.window:
            return

        # Centraliza antes de exibir para evitar "pulo" visual.
        try:
            self._center_window()
        except Exception:
            pass
        try:
            self.window.deiconify()
        except Exception:
            pass
        # Centraliza depois que o window manager "mapeou" a janela (e novamente após layout final)
        try:
            self.window.after_idle(self._center_window)
        except Exception:
            self._center_window()
        try:
            self.window.after(60, self._center_window)
        except Exception:
            pass
        self.window.lift()
        try:
            self.window.focus_force()
        except Exception:
            pass

    def _apply_current_settings_to_controls(self) -> None:
        """Atualiza variáveis/widgets com base em current_settings (para reuso da janela)."""
        try:
            if self.var_datetime_format is not None:
                self.var_datetime_format.set(self.current_settings.get("datetime_format", "%d.%m.%Y-%H:%M"))
            if self.var_bracket_open is not None:
                self.var_bracket_open.set(self.current_settings.get("bracket_open", "["))
            if self.var_bracket_close is not None:
                self.var_bracket_close.set(self.current_settings.get("bracket_close", "]"))
            if self.var_max_history is not None:
                self.var_max_history.set(self.current_settings.get("max_history_items", 100))
            if self.var_monitor_interval is not None:
                self.var_monitor_interval.set(self.current_settings.get("clipboard_monitor_interval", 3.0))
            if self.var_idle_threshold is not None:
                self.var_idle_threshold.set(self.current_settings.get("clipboard_idle_threshold", 30.0))
            if self.var_notifications_enabled is not None:
                self.var_notifications_enabled.set(self.current_settings.get("notification_enabled", True))
            if self.var_notification_duration is not None:
                self.var_notification_duration.set(self.current_settings.get("notification_duration", 2))
            if self.var_hotkey_search is not None:
                self.var_hotkey_search.set(self.current_settings.get("hotkey_search_history", "ctrl+shift+f"))
            if self.var_hotkey_refresh is not None:
                self.var_hotkey_refresh.set(self.current_settings.get("hotkey_refresh_menu", "ctrl+shift+r"))
            if self.var_log_max_bytes is not None:
                raw = self.current_settings.get("log_max_bytes", 1 * 1024 * 1024)
                try:
                    mb = max(1, int(int(raw) // (1024 * 1024)))
                except Exception:
                    mb = 1
                self.var_log_max_bytes.set(mb)
            if self.var_log_backup_count is not None:
                self.var_log_backup_count.set(self.current_settings.get("log_backup_count", 1))
            if self.var_ui_prewarm_delay_ms is not None:
                self.var_ui_prewarm_delay_ms.set(self.current_settings.get("ui_prewarm_delay_ms", 700))
            if self.var_tray_menu_cache_window_ms is not None:
                self.var_tray_menu_cache_window_ms.set(self.current_settings.get("tray_menu_cache_window_ms", 200))

            self.shortcuts_data = self.current_settings.get("custom_shortcuts", [])
            try:
                self.default_shortcut_id = self.current_settings.get("default_shortcut_id", None)
            except Exception:
                self.default_shortcut_id = None
            self._refresh_list()
        except Exception:
            # Melhor esforço: não queremos quebrar a abertura por causa de um widget opcional.
            pass

    
    
    def _create_shortcuts_page(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Cria página de atalhos"""
        tab = ctk.CTkFrame(parent, fg_color="transparent")

        # Usa o mesmo padrão das outras páginas: scroll_frame + content.
        # Isso evita que o card grande force a janela a "esmagar" o rodapé.
        scroll_frame = ModernScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=(12, 8), pady=(0, 12))

        # Card delimitador (padrão moderno: gutter + container com borda)
        card = ModernFrame(
            content,
            fg_color=self.colors['bg_secondary'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=ModernTheme.CORNER_RADIUS,
        )
        # Card com altura mais contida: evita precisar rolar só para alcançar os botões.
        card.pack(fill="x", expand=False)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", expand=False, padx=16, pady=16)
        
        # Título
        self._create_icon_title_row(inner, icon="🎯", title="Atalhos Configurados", style="heading").pack(anchor="w", pady=(0, 8))
        ModernLabel(inner, text="Gerencie seus atalhos personalizados", 
                   style="muted").pack(anchor="w", pady=(0, 16))
        
        # Lista de atalhos (usando Textbox como lista)
        # Ajuste fino: list_frame +5px e listbox +30px (os elementos abaixo descem junto).
        list_frame = ModernFrame(inner, fg_color=self.colors['surface'], height=185)
        list_frame.pack(fill="x", expand=False, pady=(0, 8))
        try:
            list_frame.pack_propagate(False)
        except Exception:
            pass
        
        self.shortcuts_listbox = ctk.CTkTextbox(
            list_frame,
            fg_color=self.colors['surface'],
            text_color=self.colors['text'],
            font=('Segoe UI', ModernTheme.FONT_SIZE_BASE),
            corner_radius=8,
            border_width=0,
            state="normal",
            height=170,
        )
        # Padding vertical menor para a listbox caber na moldura (que sobe só +5px)
        self.shortcuts_listbox.pack(fill="both", expand=True, padx=8, pady=2)

        # Seleção por clique (mantém read-only via bloqueio de teclas)
        text_widget = self._get_shortcuts_text_widget()
        if text_widget is not None:
            text_widget.tag_configure(
                "dahora_selected",
                background=self.colors.get('accent', self.colors.get('surface')),
                foreground=self.colors.get('text_bright', self.colors.get('text')),
            )
            text_widget.bind("<Button-1>", self._on_shortcut_list_click)
            text_widget.bind("<Double-Button-1>", lambda e: self._on_edit_clicked())
            text_widget.bind("<Key>", lambda e: "break")
            text_widget.bind("<<Paste>>", lambda e: "break")
            text_widget.bind("<<Cut>>", lambda e: "break")
        
        # Contador
        self.count_label = ModernLabel(inner, text="0 atalhos configurados", 
                                       style="muted")
        self.count_label.pack(anchor="w", pady=(0, 10))
        
        self._refresh_list()
        
        # Botões
        buttons = ctk.CTkFrame(inner, fg_color="transparent")
        buttons.pack(fill="x")
        
        btn_add = ModernButton(
            buttons,
            text="➕ Adicionar",
            style="primary",
            width=112,
            command=self._on_add_clicked,
        )
        btn_add.pack(side="left", padx=(0, 6))
        btn_edit = ModernButton(
            buttons,
            text="✏️ Editar",
            width=108,
            command=self._on_edit_clicked,
        )
        btn_edit.pack(side="left", padx=(0, 6))

        btn_default = ModernButton(
            buttons,
            text="⭐ Padrão",
            width=108,
            command=self._on_set_default_clicked,
        )
        btn_default.pack(side="left", padx=(0, 6))

        self._attach_tooltip(
            btn_default,
            "Define qual atalho (prefixo) será usado pelo Ctrl+Shift+Q e pelo menu Copiar.",
            prefer_above=True,
        )
        btn_remove = ModernButton(
            buttons,
            text="🗑️ Remover",
            style="danger",
            width=112,
            command=self._on_remove_clicked,
        )
        btn_remove.pack(side="left")

        btn_reload = ModernButton(
            buttons,
            text="🔄 Atualizar",
            width=108,
            command=self._reload_from_settings,
        )
        btn_reload.pack(side="right")

        # Tooltips úteis
        self._attach_tooltip(
            self.shortcuts_listbox,
            "⭐ indica o atalho padrão usado no Ctrl+Shift+Q.\nDica: selecione um item e clique em ⭐ Padrão.",
            prefer_above=False,
        )

        # Padding final para evitar corte do rodapé em janelas baixas
        ctk.CTkFrame(inner, fg_color="transparent", height=24).pack(fill="x")

        return tab

    def _on_set_default_clicked(self) -> None:
        if not self.shortcuts_data:
            messagebox.showwarning("Aviso", "Nenhum atalho configurado")
            return

        idx = self.selected_shortcut_index
        if idx < 0 or idx >= len(self.shortcuts_data):
            messagebox.showwarning("Aviso", "Selecione um atalho para definir como padrão")
            return

        shortcut_id = self.shortcuts_data[idx].get("id")
        if shortcut_id is None:
            return

        try:
            self.default_shortcut_id = int(shortcut_id)
        except Exception:
            self.default_shortcut_id = None

        self._refresh_list()

        if self.notification_callback:
            self.notification_callback("Dahora App", "Atalho padrão atualizado!")

    def _hide_tooltip(self) -> None:
        if self._tooltip_after_id and self.window is not None:
            try:
                self.window.after_cancel(self._tooltip_after_id)
            except Exception:
                pass
        self._tooltip_after_id = None

        if self._tooltip_window is not None:
            try:
                self._tooltip_window.destroy()
            except Exception:
                pass
        self._tooltip_window = None

    def _show_tooltip(self, widget, text: str, prefer_above: bool = False) -> None:
        self._hide_tooltip()
        if not self.window:
            return

        # Preferir posicionamento perto do cursor (especialmente útil em widgets grandes,
        # como o card/lista de atalhos), evitando ficar "longe" acima/abaixo do card.
        px: Optional[int] = None
        py: Optional[int] = None
        try:
            px = int(widget.winfo_pointerx())
            py = int(widget.winfo_pointery())
        except Exception:
            px = None
            py = None

        widget_x = widget_y = widget_h = None
        try:
            widget_x = int(widget.winfo_rootx())
            widget_y = int(widget.winfo_rooty())
            widget_h = int(widget.winfo_height())
        except Exception:
            widget_x = widget_y = widget_h = None

        try:
            tip = tk.Toplevel(self.window)
            tip.wm_overrideredirect(True)
            tip.attributes("-topmost", True)
            tip.configure(bg=self.colors['border'])

            frame = tk.Frame(tip, bg=self.colors['bg_secondary'], bd=0)
            frame.pack(padx=1, pady=1)
            label = tk.Label(
                frame,
                text=text,
                bg=self.colors['bg_secondary'],
                fg=self.colors['text'],
                justify="left",
                wraplength=360,
                font=("Segoe UI", 9),
            )
            label.pack(padx=10, pady=8)

            # Mede tamanho real do tooltip antes de posicionar
            tip.update_idletasks()
            tip_w = max(tip.winfo_reqwidth(), tip.winfo_width())
            tip_h = max(tip.winfo_reqheight(), tip.winfo_height())

            screen_w = self.window.winfo_screenwidth()
            screen_h = self.window.winfo_screenheight()
            margin = 8

            # Candidatos (quadrantes) relativos ao cursor; se não houver cursor, usa widget.
            def fits(cx: int, cy: int) -> bool:
                return (
                    margin <= cx <= (screen_w - tip_w - margin)
                    and margin <= cy <= (screen_h - tip_h - margin)
                )

            x = y = None
            if px is not None and py is not None:
                candidates = [
                    (px + 16, py + 18),
                    (px + 16, py - tip_h - 18),
                    (px - tip_w - 16, py + 18),
                    (px - tip_w - 16, py - tip_h - 18),
                ]
                if prefer_above:
                    candidates = [
                        (px + 16, py - tip_h - 18),
                        (px + 16, py + 18),
                        (px - tip_w - 16, py - tip_h - 18),
                        (px - tip_w - 16, py + 18),
                    ]

                for cx, cy in candidates:
                    if fits(cx, cy):
                        x, y = cx, cy
                        break

            # Fallback: posiciona relativo ao widget (comportamento anterior)
            if x is None or y is None:
                if widget_x is None or widget_y is None:
                    return
                base_x = widget_x + 10
                base_y = widget_y + (widget_h or 0) + 6
                if prefer_above:
                    base_y = widget_y - tip_h - 6
                x = base_x
                y = base_y

            # Clamp final para caber na tela
            x = min(max(int(x), margin), max(margin, screen_w - tip_w - margin))
            y = min(max(int(y), margin), max(margin, screen_h - tip_h - margin))

            tip.wm_geometry(f"+{x}+{y}")
            self._tooltip_window = tip
        except Exception:
            self._tooltip_window = None

    def _attach_tooltip(self, widget, text: str, delay_ms: int = 350, prefer_above: bool = False) -> None:
        """Anexa tooltip simples a um widget (hover)."""
        if widget is None:
            return

        def on_enter(_e=None):
            if not self.window:
                return

            # agenda para não piscar em hovers rápidos
            try:
                self._tooltip_after_id = self.window.after(
                    delay_ms,
                    lambda: self._show_tooltip(widget, text, prefer_above=prefer_above),
                )
            except Exception:
                self._tooltip_after_id = None

        def on_leave(_e=None):
            self._hide_tooltip()

        try:
            widget.bind("<Enter>", on_enter, add=True)
            widget.bind("<Leave>", on_leave, add=True)
            widget.bind("<ButtonPress>", on_leave, add=True)
        except Exception:
            pass

    def _get_shortcuts_text_widget(self) -> Optional[tk.Text]:
        """Retorna o widget Text interno do CTkTextbox (quando disponível)."""
        if not self.shortcuts_listbox:
            return None

        # CustomTkinter geralmente expõe o Text interno como _textbox.
        inner = getattr(self.shortcuts_listbox, "_textbox", None)
        if isinstance(inner, tk.Text):
            return inner

        # Fallback: algumas versões expõem diretamente a API do Text.
        if isinstance(self.shortcuts_listbox, tk.Text):
            return self.shortcuts_listbox

        return None

    def _set_selected_shortcut_index(self, index: int) -> None:
        if index < 0 or index >= len(self.shortcuts_data):
            self.selected_shortcut_index = -1
        else:
            self.selected_shortcut_index = index
        self._apply_shortcut_selection_highlight()

    def _apply_shortcut_selection_highlight(self) -> None:
        text_widget = self._get_shortcuts_text_widget()
        if text_widget is None:
            return

        # Remove highlight anterior
        text_widget.tag_remove("dahora_selected", "1.0", "end")

        idx = self.selected_shortcut_index
        if idx < 0 or idx >= len(self.shortcuts_data):
            return

        # Cada atalho é uma linha; line numbers no Text são 1-based
        line = idx + 1
        start = f"{line}.0"
        end = f"{line}.end"
        text_widget.tag_add("dahora_selected", start, end)

    def _select_shortcut_by_id(self, shortcut_id: Any) -> None:
        for i, shortcut in enumerate(self.shortcuts_data):
            if shortcut.get("id") == shortcut_id:
                self._set_selected_shortcut_index(i)
                return

    def _on_shortcut_list_click(self, event: tk.Event) -> None:
        """Seleciona o item correspondente à linha clicada."""
        text_widget = self._get_shortcuts_text_widget()
        if text_widget is None:
            return

        try:
            text_index = text_widget.index(f"@{event.x},{event.y}")
            line_str, _col_str = text_index.split(".")
            clicked_line = int(line_str) - 1
        except Exception:
            return

        self._set_selected_shortcut_index(clicked_line)
    
    def _create_format_page(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Cria página de formato"""
        tab = ctk.CTkFrame(parent, fg_color="transparent")
        
        scroll_frame = ModernScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=(12, 8), pady=(0, 12))

        # Card delimitador (padrão moderno: gutter + container com borda)
        card = ModernFrame(
            content,
            fg_color=self.colors['bg_secondary'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=ModernTheme.CORNER_RADIUS,
        )
        card.pack(fill="both", expand=True)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Título
        self._create_icon_title_row(inner, icon="📅", title="Formato de Data e Hora", style="heading").pack(anchor="w", pady=(0, 8))
        ModernLabel(inner, text="Configure como a data e hora serão formatadas", 
               style="muted").pack(anchor="w", pady=(0, 14))
        
        # Formato
        format_label = ModernLabel(inner, text="Formato de Data/Hora")
        format_label.pack(anchor="w", pady=(0, 6))
        self.var_datetime_format = ctk.StringVar(
            value=self.current_settings.get("datetime_format", "%d.%m.%Y-%H:%M"))
        format_entry = ModernEntry(inner, textvariable=self.var_datetime_format, width=400)
        format_entry.pack(anchor="w", pady=(0, 8))
        self._attach_tooltip(
            format_entry,
            "Define como a data/hora será gerada (strftime).\nPadrão: %d.%m.%Y-%H:%M\nExemplo: 29.11.2025-22:45",
        )
        ModernLabel(inner, 
             text="Códigos: %d=dia, %m=mês, %Y=ano, %H=hora, %M=minuto", 
             style="muted", justify="left", wraplength=560).pack(anchor="w", pady=(0, 16))
        
        # Delimitadores
        ModernLabel(inner, text="Caracteres de Delimitação", 
                   style="heading").pack(anchor="w", pady=(0, 16))
        
        delim_frame = ctk.CTkFrame(inner, fg_color="transparent")
        delim_frame.pack(fill="x", pady=(0, 16))
        
        # Abertura
        open_frame = ctk.CTkFrame(delim_frame, fg_color="transparent")
        open_frame.pack(side="left", padx=(0, 32))
        bracket_open_label = ModernLabel(open_frame, text="Abertura")
        bracket_open_label.pack(anchor="w", pady=(0, 6))
        self.var_bracket_open = ctk.StringVar(
            value=self.current_settings.get("bracket_open", "["))
        bracket_open_entry = ModernEntry(open_frame, textvariable=self.var_bracket_open, width=80)
        bracket_open_entry.pack(anchor="w")
        self._attach_tooltip(
            bracket_open_entry,
            "Caractere único usado antes do timestamp.\nExemplos: [  (  {",
        )
        
        # Fechamento
        close_frame = ctk.CTkFrame(delim_frame, fg_color="transparent")
        close_frame.pack(side="left")
        bracket_close_label = ModernLabel(close_frame, text="Fechamento")
        bracket_close_label.pack(anchor="w", pady=(0, 6))
        self.var_bracket_close = ctk.StringVar(
            value=self.current_settings.get("bracket_close", "]"))
        bracket_close_entry = ModernEntry(close_frame, textvariable=self.var_bracket_close, width=80)
        bracket_close_entry.pack(anchor="w")
        self._attach_tooltip(
            bracket_close_entry,
            "Caractere único usado depois do timestamp.\nDeve ser diferente do de abertura.\nExemplos: ]  )  }",
        )
        
        # Histórico
        ModernLabel(inner, text="Configurações de Histórico", 
                   style="heading").pack(anchor="w", pady=(0, 16))
        
        max_history_label = ModernLabel(inner, text="Máximo de itens")
        max_history_label.pack(anchor="w", pady=(0, 6))
        self.var_max_history = ctk.IntVar(
            value=self.current_settings.get("max_history_items", 100))
        max_history_entry = ModernEntry(inner, textvariable=self.var_max_history, width=120)
        max_history_entry.pack(anchor="w", pady=(0, 16))
        self._attach_tooltip(
            max_history_entry,
            "Quantidade máxima de itens guardados no histórico.\nFaixa: 10–1000. Padrão: 100.\nValores maiores usam mais memória e deixam o menu maior.",
        )
        
        monitor_interval_label = ModernLabel(inner, text="Intervalo de monitoramento (seg)")
        monitor_interval_label.pack(anchor="w", pady=(0, 6))
        self.var_monitor_interval = ctk.DoubleVar(
            value=self.current_settings.get("clipboard_monitor_interval", 3.0))
        monitor_interval_entry = ModernEntry(inner, textvariable=self.var_monitor_interval, width=120)
        monitor_interval_entry.pack(anchor="w", pady=(0, 16))
        self._attach_tooltip(
            monitor_interval_entry,
            "Frequência com que o app verifica alterações na área de transferência.\nFaixa: 0,5–60 s. Padrão: 3,0 s.\nValores menores reagem mais rápido, mas podem consumir mais CPU.",
        )
        
        idle_threshold_label = ModernLabel(inner, text="Tempo sem mudanças na área de transferência (seg)")
        idle_threshold_label.pack(anchor="w", pady=(0, 6))
        self.var_idle_threshold = ctk.DoubleVar(
            value=self.current_settings.get("clipboard_idle_threshold", 30.0))
        idle_threshold_entry = ModernEntry(inner, textvariable=self.var_idle_threshold, width=120)
        idle_threshold_entry.pack(anchor="w")
        self._attach_tooltip(
            idle_threshold_entry,
            "Após esse tempo sem mudanças na área de transferência, o monitoramento usa no mínimo 5 s entre verificações (se você estiver usando um intervalo menor).\nFaixa: 5–300 s. Padrão: 30 s.",
        )

        return tab
    
    def _create_notifications_page(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Cria página de notificações"""
        tab = ctk.CTkFrame(parent, fg_color="transparent")

        scroll_frame = ModernScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=(12, 8), pady=(0, 12))

        card = ModernFrame(
            content,
            fg_color=self.colors['bg_secondary'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=ModernTheme.CORNER_RADIUS,
        )
        card.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        # Título
        notifications_title_row = self._create_icon_title_row(inner, icon="🔔", title="Configurações de Notificações", style="heading")
        notifications_title_row.pack(anchor="w", pady=(0, 8))
        self._attach_tooltip(
            notifications_title_row,
            "Define se o Dahora App exibe notificações do Windows e por quanto tempo.\nAs notificações ajudam a confirmar ações sem abrir janelas.",
            prefer_above=True,
        )
        ModernLabel(
            inner,
            text="Configure como as notificações serão exibidas",
            style="muted",
        ).pack(anchor="w", pady=(0, 14))

        # Toggle
        self.var_notifications_enabled = ctk.BooleanVar(
            value=self.current_settings.get("notification_enabled", True)
        )

        switch_frame = ctk.CTkFrame(inner, fg_color="transparent")
        switch_frame.pack(fill="x", pady=(0, 8))

        notifications_switch = ctk.CTkSwitch(
            switch_frame,
            text="Habilitar notificações do Windows",
            variable=self.var_notifications_enabled,
            fg_color=self.colors['bg_tertiary'],
            progress_color=self.colors['accent'],
            button_color=self.colors['text_bright'],
            button_hover_color=self.colors['text'],
            text_color=self.colors['text'],
            font=("Segoe UI", ModernTheme.FONT_SIZE_BASE),
        )
        notifications_switch.pack(anchor="w")
        self._attach_tooltip(
            notifications_switch,
            "Quando desativado, o app não exibirá notificações do Windows ao acionar atalhos, copiar do histórico ou salvar configurações.",
        )

        ModernLabel(
            inner,
            text="Exibe notificações quando atalhos são acionados",
            style="muted",
        ).pack(anchor="w", pady=(0, 16))

        # Duração
        ModernLabel(inner, text="Duração da Notificação", style="heading").pack(
            anchor="w", pady=(0, 16)
        )

        duration_frame = ctk.CTkFrame(inner, fg_color="transparent")
        duration_frame.pack(fill="x", pady=(0, 16))

        self.var_notification_duration = ctk.IntVar(
            value=self.current_settings.get("notification_duration", 2)
        )
        notification_duration_entry = ModernEntry(duration_frame, textvariable=self.var_notification_duration, width=80)
        notification_duration_entry.pack(side="left", padx=(0, 8))
        self._attach_tooltip(
            notification_duration_entry,
            "Duração (em segundos) que a notificação fica visível.\nFaixa: 1–10. Padrão: 2.",
        )
        ModernLabel(duration_frame, text="segundos").pack(side="left")

        # Tipos
        self._create_icon_title_row(inner, icon="💡", title="Tipos de Notificações", style="heading").pack(
            anchor="w", pady=(0, 12)
        )
        ModernLabel(inner, text="Exemplos:", style="muted").pack(anchor="w")
        examples_frame = ctk.CTkFrame(inner, fg_color="transparent")
        examples_frame.pack(fill="x", pady=(4, 0))
        for example in [
            "Atalho acionado: 'Copiado com sucesso!'",
            "Item do histórico: 'Copiado do histórico!'",
            "Configurações: 'Configurações salvas!'",
        ]:
            ModernLabel(
                examples_frame,
                text=f"• {example}",
                style="muted",
                justify="left",
            ).pack(anchor="w", padx=(18, 0), pady=1)

        return tab
    
    def _create_hotkeys_page(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Cria página de teclas de atalho"""
        tab = ctk.CTkFrame(parent, fg_color="transparent")
        
        scroll_frame = ModernScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=(12, 8), pady=(0, 12))

        card = ModernFrame(
            content,
            fg_color=self.colors['bg_secondary'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=ModernTheme.CORNER_RADIUS,
        )
        card.pack(fill="both", expand=True)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Título
        hotkeys_title_row = self._create_icon_title_row(inner, icon="⌨️", title="Atalhos do Sistema", style="heading")
        hotkeys_title_row.pack(anchor="w", pady=(0, 8))
        ModernLabel(inner, text="Configure os atalhos globais", 
               style="muted").pack(anchor="w", pady=(0, 14))

        self._attach_tooltip(
            hotkeys_title_row,
            "Dica: o Ctrl+Shift+Q cola o timestamp usando o ⭐ atalho padrão definido na página Atalhos."
        )
        
        # Busca
        self._create_icon_title_row(inner, icon="🔍", title="Buscar no Histórico", style="default").pack(
            anchor="w", pady=(0, 6)
        )
        self.var_hotkey_search = ctk.StringVar(
            value=self.current_settings.get("hotkey_search_history", "ctrl+shift+f"))
        hotkey_search_entry = ModernEntry(inner, textvariable=self.var_hotkey_search, width=300)
        hotkey_search_entry.pack(anchor="w", pady=(0, 16))
        self._attach_tooltip(
            hotkey_search_entry,
            "Atalho global para abrir a Busca no Histórico.\nExemplo: ctrl+shift+f.\nDica: evite atalhos usados pelo sistema e por outros apps.",
        )
        
        # Refresh
        self._create_icon_title_row(inner, icon="🔄", title="Recarregar Menu", style="default").pack(
            anchor="w", pady=(0, 6)
        )
        self.var_hotkey_refresh = ctk.StringVar(
            value=self.current_settings.get("hotkey_refresh_menu", "ctrl+shift+r"))
        hotkey_refresh_entry = ModernEntry(inner, textvariable=self.var_hotkey_refresh, width=300)
        hotkey_refresh_entry.pack(anchor="w", pady=(0, 16))
        self._attach_tooltip(
            hotkey_refresh_entry,
            "Atalho global para recarregar os itens do menu da bandeja.\nExemplo: ctrl+shift+r.",
        )
        
        # Orientações
        self._create_icon_title_row(inner, icon="💡", title="Orientações", style="heading").pack(
            anchor="w", pady=(0, 12)
        )
        ModernLabel(inner, text="✅ Combinações recomendadas:", style="muted").pack(anchor="w")
        guide_frame = ctk.CTkFrame(inner, fg_color="transparent")
        guide_frame.pack(fill="x", pady=(4, 16))
        for combo in ["ctrl+shift+letra", "ctrl+alt+letra"]:
            ModernLabel(guide_frame, text=f"• {combo}", style="muted", justify="left").pack(
                anchor="w", padx=(18, 0), pady=1
            )
        
        # Reservados
        reserved_title_row = self._create_icon_title_row(inner, icon="🚫", title="Atalhos Reservados", style="heading")
        reserved_title_row.pack(anchor="w", pady=(0, 12))
        self._attach_tooltip(
            reserved_title_row,
            "Essas combinações não podem ser usadas em atalhos personalizados para evitar conflitos com o sistema/app."
        )
        ModernLabel(
            inner,
            text="Ctrl+C • Ctrl+V • Ctrl+X • Ctrl+A • Ctrl+Z • Ctrl+Shift+Q • Ctrl+Shift+R • Ctrl+Shift+F",
            style="muted",
            justify="left",
            wraplength=560,
        ).pack(anchor="w", pady=(0, 16))
        
        return tab

    def _create_advanced_page(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        tab = ctk.CTkFrame(parent, fg_color="transparent")

        scroll_frame = ModernScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=(12, 8), pady=(0, 12))

        card = ModernFrame(
            content,
            fg_color=self.colors['bg_secondary'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=ModernTheme.CORNER_RADIUS,
        )
        card.pack(fill="both", expand=True)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        advanced_title_row = self._create_icon_title_row(inner, icon="🛠️", title="Configurações Avançadas", style="heading")
        advanced_title_row.pack(anchor="w", pady=(0, 8))
        self._attach_tooltip(
            advanced_title_row,
            "Ajustes finos para tamanho de logs, pré-aquecimento da UI e cache do menu.\nRecomendado manter os valores padrão salvo necessidade específica.",
            prefer_above=True,
        )
        ModernLabel(
            inner,
            text="Ajuste limites de log e otimizações internas",
            style="muted",
        ).pack(anchor="w", pady=(0, 16))

        logs_title_row = self._create_icon_title_row(inner, icon="📄", title="Logs", style="heading")
        logs_title_row.pack(anchor="w", pady=(0, 12))
        self._attach_tooltip(
            logs_title_row,
            "Controla o tamanho do arquivo de log do Dahora App e quantos backups antigos serão mantidos.\nÚtil para limitar uso de disco ou manter mais histórico de diagnóstico.",
            prefer_above=True,
        )

        log_frame = ctk.CTkFrame(inner, fg_color="transparent")
        log_frame.pack(fill="x", pady=(0, 12))

        left_log = ctk.CTkFrame(log_frame, fg_color="transparent")
        left_log.pack(side="left", padx=(0, 24))

        log_size_label = ModernLabel(left_log, text="Tamanho máximo do arquivo (MB)")
        log_size_label.pack(anchor="w", pady=(0, 6))
        self._attach_tooltip(
            log_size_label,
            "Tamanho máximo do arquivo de log antes de girar para um backup.\nValores recomendados: 1–5 MB.\nValores menores geram arquivos menores; maiores mantêm mais histórico.",
            prefer_above=False,
        )
        self.var_log_max_bytes = ctk.IntVar(
            value=int(self.current_settings.get("log_max_bytes", 1 * 1024 * 1024) // (1024 * 1024))
        )
        ModernSpinbox(
            left_log,
            variable=self.var_log_max_bytes,
            from_=1,
            to=20,
            step=1,
            width=100,
        ).pack(anchor="w")

        right_log = ctk.CTkFrame(log_frame, fg_color="transparent")
        right_log.pack(side="left")

        log_backup_label = ModernLabel(right_log, text="Quantidade de backups")
        log_backup_label.pack(anchor="w", pady=(0, 6))
        self._attach_tooltip(
            log_backup_label,
            "Número de arquivos de log antigos mantidos além do log atual.\nRecomendado: 1 ou 2.\nAumente apenas se precisar investigar problemas com mais histórico.",
            prefer_above=False,
        )
        self.var_log_backup_count = ctk.IntVar(
            value=int(self.current_settings.get("log_backup_count", 1))
        )
        ModernSpinbox(
            right_log,
            variable=self.var_log_backup_count,
            from_=0,
            to=10,
            step=1,
            width=100,
        ).pack(anchor="w")

        perf_title_row = self._create_icon_title_row(inner, icon="⚡", title="Performance", style="heading")
        perf_title_row.pack(anchor="w", pady=(4, 12))
        self._attach_tooltip(
            perf_title_row,
            "Parâmetros que influenciam a responsividade da UI e o custo para recalcular o menu da bandeja.\nAjuste apenas se notar atrasos ou consumo excessivo.",
            prefer_above=True,
        )

        perf_frame = ctk.CTkFrame(inner, fg_color="transparent")
        perf_frame.pack(fill="x", pady=(0, 12))

        left_perf = ctk.CTkFrame(perf_frame, fg_color="transparent")
        left_perf.pack(side="left", padx=(0, 24))

        prewarm_label = ModernLabel(left_perf, text="Delay para pré-aquecer UI (ms)")
        prewarm_label.pack(anchor="w", pady=(0, 6))
        self._attach_tooltip(
            prewarm_label,
            "Tempo de espera antes de rodar tarefas de pré-aquecimento da interface.\nPadrão: 700 ms.\nValores menores deixam o app pronto mais rápido, mas podem competir com a inicialização do sistema.\nValores maiores adiam otimizações para momentos mais ociosos.",
            prefer_above=False,
        )
        self.var_ui_prewarm_delay_ms = ctk.IntVar(
            value=int(self.current_settings.get("ui_prewarm_delay_ms", 700))
        )
        ModernSpinbox(
            left_perf,
            variable=self.var_ui_prewarm_delay_ms,
            from_=0,
            to=10000,
            step=100,
            width=120,
        ).pack(anchor="w")

        right_perf = ctk.CTkFrame(perf_frame, fg_color="transparent")
        right_perf.pack(side="left")

        tray_cache_label = ModernLabel(right_perf, text="Janela de cache do menu (ms)")
        tray_cache_label.pack(anchor="w", pady=(0, 6))
        self._attach_tooltip(
            tray_cache_label,
            "Tempo mínimo entre recálculos completos dos itens do menu da bandeja.\nPadrão: 200 ms.\nValores maiores reduzem trabalho em aberturas rápidas do menu; valores menores deixam o menu sempre atualizado, com pequeno custo extra.",
            prefer_above=False,
        )
        self.var_tray_menu_cache_window_ms = ctk.IntVar(
            value=int(self.current_settings.get("tray_menu_cache_window_ms", 200))
        )
        ModernSpinbox(
            right_perf,
            variable=self.var_tray_menu_cache_window_ms,
            from_=0,
            to=2000,
            step=50,
            width=120,
        ).pack(anchor="w")

        return tab
    
    def _create_about_page(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Cria página sobre"""
        tab = ctk.CTkFrame(parent, fg_color="transparent")
        
        scroll_frame = ModernScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=(12, 8), pady=(0, 12))

        card = ModernFrame(
            content,
            fg_color=self.colors['bg_secondary'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=ModernTheme.CORNER_RADIUS,
        )
        card.pack(fill="both", expand=True)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Título
        self._create_icon_title_row(inner, icon="ℹ️", title="Dahora App", style="heading").pack(anchor="w", pady=(0, 8))
        ModernLabel(inner, 
                   text="Sistema avançado de timestamps com total liberdade", 
                   style="muted").pack(anchor="w", pady=(0, 24))
        
        # Destaque
        self._create_icon_title_row(inner, icon="✨", title="Total Liberdade de Configuração", style="heading").pack(
            anchor="w", pady=(0, 12)
        )
        ModernLabel(
            inner,
            text=(
                "Nenhum atalho é fixo! Você tem controle total sobre:\n"
                "• Todas as combinações de teclas\n"
                "• Todos os prefixos e formatos"
            ),
            style="muted",
            justify="left",
            wraplength=560,
        ).pack(anchor="w", pady=(0, 24))
        
        # Recursos
        self._create_icon_title_row(inner, icon="🎯", title="Recursos Principais", style="heading").pack(anchor="w", pady=(0, 12))
        features_frame = ctk.CTkFrame(inner, fg_color="transparent")
        features_frame.pack(fill="x", pady=(0, 8))

        for item in [
            "✅ Atalhos personalizados ilimitados",
            "✅ Prefixos customizados",
            "✅ Formato configurável",
            "✅ Histórico inteligente",
            "✅ Tema automático",
        ]:
            ModernLabel(features_frame, text=item, style="muted", justify="left").pack(anchor="w")

        # Padding final para evitar corte no rodapé em janelas baixas
        ctk.CTkFrame(inner, fg_color="transparent", height=24).pack(fill="x")

        return tab
    
    def _refresh_list(self) -> None:
        """Atualiza a lista de atalhos"""
        if not self.shortcuts_listbox:
            return

        # Mantém o textbox em modo normal para permitir highlight via tags;
        # edição é bloqueada pelos binds de teclado.
        self.shortcuts_listbox.configure(state="normal")
        self.shortcuts_listbox.delete("1.0", "end")
        
        for shortcut in self.shortcuts_data:
            status = "✅" if shortcut.get("enabled", True) else "⏸️"
            hotkey = format_hotkey_display(shortcut.get("hotkey", ""))
            prefix = shortcut.get("prefix", "")
            desc = shortcut.get("description", "")

            is_default = False
            try:
                raw_shortcut_id = shortcut.get("id")
                is_default = (
                    self.default_shortcut_id is not None
                    and raw_shortcut_id is not None
                    and int(str(raw_shortcut_id)) == int(str(self.default_shortcut_id))
                )
            except Exception:
                is_default = False

            marker = "⭐ " if is_default else ""
            
            line = f"{status} {marker}{hotkey} → {prefix}"
            if desc:
                line += f" - {desc}"
            line += "\n"
            
            self.shortcuts_listbox.insert("end", line)

        # Reaplica highlight da seleção (se ainda for válida)
        if self.selected_shortcut_index >= len(self.shortcuts_data):
            self.selected_shortcut_index = -1
        self._apply_shortcut_selection_highlight()
        
        if self.count_label:
            count = len(self.shortcuts_data)
            text = f"{count} atalho{'s' if count != 1 else ''} configurado{'s' if count != 1 else ''}"
            self.count_label.configure(text=text)
    
    def _reload_from_settings(self) -> None:
        """Recarrega dados do settings"""
        if self.on_get_settings_callback:
            fresh = self.on_get_settings_callback()
            self.current_settings = fresh
            self.shortcuts_data = fresh.get("custom_shortcuts", [])
            try:
                self.default_shortcut_id = fresh.get("default_shortcut_id", None)
            except Exception:
                self.default_shortcut_id = None
        else:
            self.shortcuts_data = self.current_settings.get("custom_shortcuts", [])
        self._refresh_list()
    
    def _mark_needs_restart(self) -> None:
        """Marca que precisa reiniciar"""
        # Mantido por compatibilidade (não usado: hotkeys aplicam sem reinício)
        self.needs_restart = False
    
    def _on_save_all(self) -> None:
        """Salva todas as configurações"""
        try:
            if self.on_save_callback:
                max_history_items = self.var_max_history.get() if self.var_max_history else 100
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

                clipboard_monitor_interval = self.var_monitor_interval.get() if self.var_monitor_interval else 3.0
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

                clipboard_idle_threshold = self.var_idle_threshold.get() if self.var_idle_threshold else 30.0
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

                notification_duration = self.var_notification_duration.get() if self.var_notification_duration else 2
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

                bracket_open = self.var_bracket_open.get() if self.var_bracket_open else "["
                bracket_close = self.var_bracket_close.get() if self.var_bracket_close else "]"
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
                    "datetime_format": self.var_datetime_format.get().strip() if self.var_datetime_format else "%d.%m.%Y-%H:%M",
                    "bracket_open": bracket_open,
                    "bracket_close": bracket_close,
                    "max_history_items": max_history_items,
                    "clipboard_monitor_interval": clipboard_monitor_interval,
                    "clipboard_idle_threshold": clipboard_idle_threshold,
                    "notification_enabled": self.var_notifications_enabled.get() if self.var_notifications_enabled else True,
                    "notification_duration": notification_duration,
                    "hotkey_search_history": self.var_hotkey_search.get().strip() if self.var_hotkey_search else "ctrl+shift+f",
                    "hotkey_refresh_menu": self.var_hotkey_refresh.get().strip() if self.var_hotkey_refresh else "ctrl+shift+r",
                    "log_max_bytes": (int(self.var_log_max_bytes.get()) * 1024 * 1024) if self.var_log_max_bytes else (1 * 1024 * 1024),
                    "log_backup_count": self.var_log_backup_count.get() if self.var_log_backup_count else 1,
                    "ui_prewarm_delay_ms": self.var_ui_prewarm_delay_ms.get() if self.var_ui_prewarm_delay_ms else 700,
                    "tray_menu_cache_window_ms": self.var_tray_menu_cache_window_ms.get() if self.var_tray_menu_cache_window_ms else 200,
                    "default_shortcut_id": self.default_shortcut_id,
                }
                self.on_save_callback(settings)
        except Exception as e:
            logging.error(f"Erro ao salvar: {e}")
    
    def _on_save_and_close(self) -> None:
        """Salva e fecha"""
        self._on_save_all()

        if self.notification_callback:
            self.notification_callback("Dahora App", "Configurações salvas!")
        
        self._on_close()
    
    def _on_add_clicked(self) -> None:
        """Adicionar atalho"""
        self._show_editor_dialog()
    
    def _on_edit_clicked(self) -> None:
        """Editar atalho selecionado"""
        if not self.shortcuts_data:
            messagebox.showwarning("Aviso", "Nenhum atalho configurado")
            return

        idx = self.selected_shortcut_index
        if idx < 0 or idx >= len(self.shortcuts_data):
            messagebox.showwarning("Aviso", "Selecione um atalho para editar")
            return

        self._show_editor_dialog(self.shortcuts_data[idx])
    
    def _on_remove_clicked(self) -> None:
        """Remover atalho"""
        if not self.shortcuts_data:
            messagebox.showwarning("Aviso", "Nenhum atalho configurado")
            return

        idx = self.selected_shortcut_index
        if idx < 0 or idx >= len(self.shortcuts_data):
            messagebox.showwarning("Aviso", "Selecione um atalho para remover")
            return

        if not self.on_remove_callback:
            return

        shortcut = self.shortcuts_data[idx]
        hotkey = format_hotkey_display(shortcut.get("hotkey", ""))
        prefix = shortcut.get("prefix", "")
        confirm = messagebox.askyesno(
            "Confirmar Remoção",
            f"Deseja remover o atalho?\n\nHotkey: {hotkey}\nPrefixo: {prefix}"
        )
        if not confirm:
            return

        success, msg = self.on_remove_callback(shortcut.get("id"))
        if success:
            self.selected_shortcut_index = -1
            self._reload_from_settings()
            if self.notification_callback:
                self.notification_callback("Dahora App", "Atalho removido!")
        else:
            messagebox.showerror("Erro", msg or "Falha ao remover atalho")
    
    def _show_editor_dialog(self, shortcut: Optional[Dict] = None) -> None:
        """Mostra dialog de edição"""
        from dahora_app.ui.modern_shortcut_editor import ModernShortcutEditor
        
        editor = ModernShortcutEditor(
            parent=self.window,
            shortcut=shortcut,
            on_save=self._on_editor_save,
            on_validate_hotkey=self.on_validate_hotkey_callback
        )
        editor.show()
    
    def _on_editor_save(self, data: Dict) -> None:
        """Callback do editor"""
        is_new = "id" not in data or data["id"] is None
        
        if is_new:
            if self.on_add_callback:
                success, msg, new_id = self.on_add_callback(
                    data.get("hotkey", ""),
                    data.get("prefix", ""),
                    data.get("description", ""),
                    data.get("enabled", True)
                )
                if success:
                    self._reload_from_settings()
                    if new_id is not None:
                        self._select_shortcut_by_id(new_id)
                    elif self.shortcuts_data:
                        self._set_selected_shortcut_index(len(self.shortcuts_data) - 1)
                    if self.notification_callback:
                        self.notification_callback("Dahora App", "Atalho adicionado!")
        else:
            if self.on_update_callback:
                success, msg = self.on_update_callback(
                    data["id"],
                    hotkey=data.get("hotkey"),
                    prefix=data.get("prefix"),
                    description=data.get("description"),
                    enabled=data.get("enabled")
                )
                if success:
                    self._reload_from_settings()
                    self._select_shortcut_by_id(data.get("id"))
                    if self.notification_callback:
                        self.notification_callback("Dahora App", "Atalho atualizado!")
    
    def _on_close(self) -> None:
        """Fecha a janela"""
        if self.window:
            try:
                self._hide_tooltip()
                # Reuso: esconder é muito mais rápido do que destruir.
                self.window.withdraw()
            except Exception:
                try:
                    self.window.destroy()
                except Exception:
                    pass
            # Mantém self.window para reuso; será destruída ao encerrar o app.
