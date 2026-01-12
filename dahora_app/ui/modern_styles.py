"""
Estilos Modernos usando CustomTkinter
Interface Windows 11 com cantos arredondados e componentes modernos
"""

import customtkinter as ctk
from typing import Optional, Callable
import logging


class ModernTheme:
    """Gerenciador de tema moderno com CustomTkinter"""

    _initialized: bool = False
    _cached_theme: str = "dark"

    # Cores do tema escuro (inspirado em VS Code/Discord)
    DARK = {
        "bg": "#1a1a1a",
        "bg_secondary": "#252526",
        "bg_tertiary": "#2d2d30",
        "surface": "#323233",
        "text": "#cccccc",
        "text_bright": "#ffffff",
        "text_muted": "#808080",
        "accent": "#0078d4",
        "accent_hover": "#1a8cd8",
        "success": "#4caf50",
        "warning": "#ff9800",
        "error": "#f44336",
        "border": "#3e3e42",
    }

    # Cores do tema claro
    LIGHT = {
        "bg": "#f5f5f5",
        "bg_secondary": "#ffffff",
        "bg_tertiary": "#e8e8e8",
        "surface": "#ffffff",
        "text": "#1a1a1a",
        "text_bright": "#000000",
        "text_muted": "#666666",
        "accent": "#0078d4",
        "accent_hover": "#106ebe",
        "success": "#4caf50",
        "warning": "#ff9800",
        "error": "#f44336",
        "border": "#d4d4d4",
    }

    # Configurações de componentes
    CORNER_RADIUS = 8
    BUTTON_CORNER_RADIUS = 6
    ENTRY_CORNER_RADIUS = 6
    # Tipografia (evita textos pequenos demais em telas high-DPI)
    FONT_SIZE_BASE = 12
    CONTROL_HEIGHT = 32

    @staticmethod
    def setup():
        """Configura o tema global do CustomTkinter"""
        # Evita reconfigurar o CustomTkinter a cada abertura de janela.
        # Isso reduz bastante o tempo de "montar" diálogos (Configurações/Busca/Sobre).
        if ModernTheme._initialized:
            return ModernTheme._cached_theme

        # Detecta tema do sistema
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            theme = "light" if value == 1 else "dark"
        except Exception:
            theme = "dark"

        # Configura CustomTkinter
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")

        ModernTheme._initialized = True
        ModernTheme._cached_theme = theme

        return theme

    @staticmethod
    def get_colors(theme: str = "dark") -> dict:
        """Retorna as cores do tema especificado"""
        return ModernTheme.LIGHT if theme == "light" else ModernTheme.DARK


class ModernWindow(ctk.CTk):
    """Janela moderna com CustomTkinter"""

    def __init__(self, title: str = "Dahora App", size: str = "850x700"):
        super().__init__()

        # Configura tema
        self.theme = ModernTheme.setup()
        self.colors = ModernTheme.get_colors(self.theme)

        # Configura janela
        self.title(title)
        self.geometry(size)
        self.minsize(700, 500)

        # Cor de fundo
        self.configure(fg_color=self.colors["bg"])

        # Aplica dark title bar no Windows
        self._apply_dark_titlebar()

    def _apply_dark_titlebar(self):
        """Aplica barra de título escura no Windows"""
        if self.theme == "dark":
            try:
                import ctypes
                from ctypes import windll, c_int, byref, sizeof

                self.update()
                hwnd = windll.user32.GetParent(self.winfo_id())
                value = c_int(1)
                windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 20, byref(value), sizeof(value)
                )
            except Exception:
                pass


class ModernFrame(ctk.CTkFrame):
    """Frame moderno com cantos arredondados"""

    def __init__(self, parent, **kwargs):
        colors = ModernTheme.get_colors()

        defaults = {
            "fg_color": colors["bg_secondary"],
            "corner_radius": ModernTheme.CORNER_RADIUS,
            "border_width": 0,
        }
        defaults.update(kwargs)

        super().__init__(parent, **defaults)


class ModernButton(ctk.CTkButton):
    """Botão moderno com cantos arredondados"""

    def __init__(
        self,
        parent,
        text: str = "",
        command: Optional[Callable] = None,
        style: str = "default",
        **kwargs
    ):
        colors = ModernTheme.get_colors()

        # Estilos de botão
        styles = {
            "default": {
                "fg_color": colors["bg_tertiary"],
                "hover_color": colors["surface"],
                "text_color": colors["text"],
            },
            "primary": {
                "fg_color": colors["accent"],
                "hover_color": colors["accent_hover"],
                "text_color": colors["text_bright"],
            },
            "success": {
                "fg_color": colors["success"],
                "hover_color": "#45a049",
                "text_color": colors["text_bright"],
            },
            "danger": {
                "fg_color": colors["error"],
                "hover_color": "#d32f2f",
                "text_color": colors["text_bright"],
            },
        }

        style_config = styles.get(style, styles["default"])

        defaults = {
            "text": text,
            "command": command,
            "corner_radius": ModernTheme.BUTTON_CORNER_RADIUS,
            "border_width": 0,
            "font": ("Segoe UI", ModernTheme.FONT_SIZE_BASE),
            "height": ModernTheme.CONTROL_HEIGHT,
        }
        defaults.update(style_config)
        defaults.update(kwargs)

        super().__init__(parent, **defaults)


class ModernEntry(ctk.CTkEntry):
    """Campo de entrada moderno com cantos arredondados"""

    def __init__(self, parent, **kwargs):
        colors = ModernTheme.get_colors()

        defaults = {
            "fg_color": colors["surface"],
            "border_color": colors["border"],
            "text_color": colors["text"],
            "placeholder_text_color": colors["text_muted"],
            "corner_radius": ModernTheme.ENTRY_CORNER_RADIUS,
            "border_width": 1,
            "font": ("Segoe UI", ModernTheme.FONT_SIZE_BASE),
            "height": ModernTheme.CONTROL_HEIGHT,
        }
        defaults.update(kwargs)

        super().__init__(parent, **defaults)


class ModernLabel(ctk.CTkLabel):
    """Label moderno"""

    def __init__(self, parent, text: str = "", style: str = "default", **kwargs):
        colors = ModernTheme.get_colors()

        base = ModernTheme.FONT_SIZE_BASE
        muted = max(base - 1, 11)
        heading = max(base + 3, 15)

        styles = {
            "default": {
                "text_color": colors["text"],
                "font": ("Segoe UI", base),
            },
            "title": {
                "text_color": colors["text_bright"],
                "font": ("Segoe UI", 19, "bold"),
            },
            "heading": {
                "text_color": colors["text_bright"],
                "font": ("Segoe UI", heading, "bold"),
            },
            "muted": {
                "text_color": colors["text_muted"],
                "font": ("Segoe UI", muted),
            },
        }

        style_config = styles.get(style, styles["default"])

        defaults = {
            "text": text,
        }
        defaults.update(style_config)
        defaults.update(kwargs)

        super().__init__(parent, **defaults)


class ModernCheckbox(ctk.CTkCheckBox):
    """Checkbox moderno"""

    def __init__(self, parent, text: str = "", **kwargs):
        colors = ModernTheme.get_colors()

        defaults = {
            "text": text,
            "text_color": colors["text"],
            "fg_color": colors["accent"],
            "hover_color": colors["accent_hover"],
            "border_color": colors["border"],
            "checkmark_color": colors["text_bright"],
            "corner_radius": 4,
            "border_width": 2,
            "font": ("Segoe UI", ModernTheme.FONT_SIZE_BASE),
        }
        defaults.update(kwargs)

        super().__init__(parent, **defaults)


class ModernSpinbox(ctk.CTkFrame):
    """Spinbox moderno (CustomTkinter não tem nativo)"""

    def __init__(
        self,
        parent,
        from_: int = 0,
        to: int = 100,
        variable=None,
        width: int = 100,
        **kwargs
    ):
        colors = ModernTheme.get_colors()

        super().__init__(parent, fg_color="transparent")

        self.variable = variable
        self.from_ = from_
        self.to = to

        # Entry
        self.entry = ModernEntry(self, width=width - 50, textvariable=variable)
        self.entry.pack(side="left", padx=(0, 4))

        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="left")

        self.btn_up = ctk.CTkButton(
            btn_frame,
            text="▲",
            width=20,
            height=14,
            corner_radius=3,
            fg_color=colors["bg_tertiary"],
            hover_color=colors["surface"],
            text_color=colors["text_muted"],
            font=("Segoe UI", 8),
            command=self._increment,
        )
        self.btn_up.pack()

        self.btn_down = ctk.CTkButton(
            btn_frame,
            text="▼",
            width=20,
            height=14,
            corner_radius=3,
            fg_color=colors["bg_tertiary"],
            hover_color=colors["surface"],
            text_color=colors["text_muted"],
            font=("Segoe UI", 8),
            command=self._decrement,
        )
        self.btn_down.pack()

    def _increment(self):
        if self.variable:
            try:
                val = self.variable.get()
                if val < self.to:
                    self.variable.set(val + 1)
            except Exception:
                pass

    def _decrement(self):
        if self.variable:
            try:
                val = self.variable.get()
                if val > self.from_:
                    self.variable.set(val - 1)
            except Exception:
                pass


class ModernTabview(ctk.CTkTabview):
    """Tabview moderno com cantos arredondados"""

    def __init__(self, parent, **kwargs):
        colors = ModernTheme.get_colors()

        defaults = {
            "fg_color": colors["bg"],
            "segmented_button_fg_color": colors["bg_secondary"],
            "segmented_button_selected_color": colors["accent"],
            "segmented_button_selected_hover_color": colors["accent_hover"],
            "segmented_button_unselected_color": colors["bg_secondary"],
            "segmented_button_unselected_hover_color": colors["bg_tertiary"],
            "text_color": colors["text"],
            # corner_radius menor evita “recuo” visual do conteúdo/scrollbar nas bordas
            "corner_radius": 0,
        }
        defaults.update(kwargs)

        super().__init__(parent, **defaults)

        # Algumas versões do CustomTkinter não suportam passar fonte do segmented button via kwargs.
        # Fazemos um ajuste pós-init com fallback para nomes internos diferentes.
        try:
            segmented = getattr(self, "_segmented_button", None)
            if segmented is not None:
                segmented.configure(font=("Segoe UI", ModernTheme.FONT_SIZE_BASE))
        except Exception:
            pass


class ModernScrollableFrame(ctk.CTkScrollableFrame):
    """Frame scrollável moderno com scrollbar overlay"""

    def __init__(self, parent, **kwargs):
        colors = ModernTheme.get_colors()

        defaults = {
            "fg_color": colors["bg"],
            "corner_radius": 0,
            "scrollbar_button_color": colors["bg_tertiary"],
            "scrollbar_button_hover_color": colors["surface"],
        }
        defaults.update(kwargs)

        super().__init__(parent, **defaults)

        # Guarda cores para alternar visibilidade sem mudar o layout.
        self._sb_visible_color = defaults.get(
            "scrollbar_button_color", colors["bg_tertiary"]
        )
        self._sb_visible_hover_color = defaults.get(
            "scrollbar_button_hover_color", colors["surface"]
        )
        self._sb_hidden_color = colors["bg"]
        self._sb_hidden_hover_color = colors["bg"]

        # Auto-hide da scrollbar quando não há conteúdo suficiente para rolar.
        # Isso evita a barra "sobrando" (visualmente estranha) em abas onde tudo cabe.
        try:
            canvas = getattr(self, "_parent_canvas", None)
            if canvas is not None:
                canvas.bind("<Configure>", self._update_scrollbar_visibility, add="+")
            self.bind("<Configure>", self._update_scrollbar_visibility, add="+")
            self.after(50, self._update_scrollbar_visibility)
        except Exception:
            pass

    def _update_scrollbar_visibility(self, event=None) -> None:
        try:
            scrollbar = getattr(self, "_scrollbar", None)
            canvas = getattr(self, "_parent_canvas", None)
            if scrollbar is None or canvas is None:
                return

            # bbox pode ser None quando ainda não layoutou
            bbox = canvas.bbox("all")
            if not bbox:
                needs_scroll = False
            else:
                content_height = bbox[3] - bbox[1]
                viewport_height = canvas.winfo_height()
                needs_scroll = content_height > (viewport_height + 2)

            # Mantém a coluna da scrollbar sempre presente para que o gutter/padding
            # pareça consistente entre abas. Quando não precisa rolar, "esconde" o thumb
            # pintando-o com a mesma cor do fundo.
            try:
                if (
                    scrollbar.winfo_manager() == "grid"
                    and not scrollbar.winfo_ismapped()
                ):
                    scrollbar.grid()
            except Exception:
                pass

            if needs_scroll:
                scrollbar.configure(
                    scrollbar_button_color=self._sb_visible_color,
                    scrollbar_button_hover_color=self._sb_visible_hover_color,
                )
            else:
                scrollbar.configure(
                    scrollbar_button_color=self._sb_hidden_color,
                    scrollbar_button_hover_color=self._sb_hidden_hover_color,
                )
        except Exception:
            pass


class ModernTextbox(ctk.CTkTextbox):
    """Textbox moderno"""

    def __init__(self, parent, **kwargs):
        colors = ModernTheme.get_colors()

        defaults = {
            "fg_color": colors["surface"],
            "text_color": colors["text"],
            "border_color": colors["border"],
            "corner_radius": ModernTheme.CORNER_RADIUS,
            "border_width": 1,
            "font": ("Segoe UI", ModernTheme.FONT_SIZE_BASE),
            "scrollbar_button_color": colors["bg_tertiary"],
            "scrollbar_button_hover_color": colors["surface"],
        }
        defaults.update(kwargs)

        super().__init__(parent, **defaults)
