"""
Tela Sobre Moderna usando CustomTkinter
"""
import customtkinter as ctk
import webbrowser
from PIL import Image
import logging
import time

from dahora_app.ui.modern_styles import ModernTheme, ModernLabel, ModernFrame, ModernButton
from dahora_app.ui.icon_manager import IconManager
from dahora_app.constants import APP_VERSION


class ModernAboutDialog:
    """Janela Sobre moderna com CustomTkinter"""
    
    def __init__(self):
        self.window = None
        self.parent = None
        self.colors = ModernTheme.get_colors()

    def set_parent(self, parent: ctk.CTk) -> None:
        self.parent = parent
    
    def show(self):
        """Mostra a janela"""
        start = time.perf_counter()
        if self.window is not None:
            try:
                self.window.deiconify()
            except Exception:
                pass
            t_show = time.perf_counter()
            self._show_window()
            show_ms = (time.perf_counter() - t_show) * 1000
            total_ms = (time.perf_counter() - start) * 1000
            logging.info(f"[UI] ModernAboutDialog.show reuse show={show_ms:.1f}ms total={total_ms:.1f}ms")
            return
        
        t_create = time.perf_counter()
        self._create_window()
        create_ms = (time.perf_counter() - t_create) * 1000

        t_show = time.perf_counter()
        self._show_window()
        show_ms = (time.perf_counter() - t_show) * 1000

        total_ms = (time.perf_counter() - start) * 1000
        logging.info(f"[UI] ModernAboutDialog.show create={create_ms:.1f}ms show={show_ms:.1f}ms total={total_ms:.1f}ms")
    
    def _create_window(self):
        """Cria a janela"""
        self.theme = ModernTheme.setup()
        self.colors = ModernTheme.get_colors(self.theme)

        if self.parent is None:
            raise RuntimeError("ModernAboutDialog precisa de parent (CTk root) antes de show().")

        self.window = ctk.CTkToplevel(self.parent)
        # Evita renderização progressiva (mostra apenas no final)
        self.window.withdraw()
        self.window.title("Sobre - Dahora App")
        self.window.geometry("420x510")
        self.window.resizable(False, False)
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

        try:
            import ctypes
            from ctypes import windll
            self.window.update_idletasks()
            hwnd = windll.user32.GetParent(self.window.winfo_id()) or self.window.winfo_id()
            style = windll.user32.GetWindowLongW(hwnd, -16)
            windll.user32.SetWindowLongW(hwnd, -16, style & ~0x20000)
            windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0004 | 0x0020)
        except Exception:
            pass
        
        # Container
        main = ctk.CTkFrame(self.window, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=24, pady=20)
        
        # Logo
        try:
            icon_img = IconManager.load_icon()
            icon_img = icon_img.resize((64, 64))
            self.photo = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(64, 64))
            ctk.CTkLabel(main, image=self.photo, text="").pack(pady=(0, 12))
        except Exception:
            pass
        
        # Título
        ctk.CTkLabel(
            main,
            text="Dahora App",
            font=("Segoe UI", 20, "bold"),
            text_color=self.colors['text_bright'],
        ).pack(pady=(0, 4))

        ModernLabel(
            main,
            text="Gerenciador Inteligente de Área de Transferência",
            style="muted",
        ).pack(pady=(0, 16))
        
        # Versão badge
        version_frame = ctk.CTkFrame(main, fg_color=self.colors['accent'], corner_radius=12)
        version_frame.pack(pady=(0, 20))
        ctk.CTkLabel(
            version_frame,
            text=f"v{APP_VERSION}",
            font=("Segoe UI", 11, "bold"),
            text_color=self.colors['text_bright'],
        ).pack(padx=16, pady=4)
        
        # Info card
        info_card = ModernFrame(
            main,
            fg_color=self.colors['surface'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=ModernTheme.CORNER_RADIUS,
        )
        info_card.pack(fill="x", pady=(0, 20))
        
        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(fill="x", padx=16, pady=12)
        
        features = [
            "✅ Colagem Automática",
            "✅ Atalhos Ilimitados",
            "✅ Histórico Inteligente",
            "✅ Zero Telemetria"
        ]
        
        for feat in features:
            ModernLabel(info_inner, text=feat).pack(anchor="w", pady=2)
        
        # Botões
        buttons = ctk.CTkFrame(main, fg_color="transparent")
        buttons.pack(pady=(0, 16))
        
        ModernButton(
            buttons,
            text="GitHub",
            width=100,
            command=lambda: webbrowser.open("https://github.com/rkvasne/dahora-app"),
        ).pack(side="left", padx=4)

        ModernButton(
            buttons,
            text="Website",
            width=100,
            command=lambda: webbrowser.open("https://kvasne.com"),
        ).pack(side="left", padx=4)
        
        # Copyright
        ModernLabel(
            main,
            text="© 2025 Raphael Kvasne. Licença MIT.",
            style="muted",
        ).pack(side="bottom", pady=(0, 10))
        
        # Não exibe aqui; show() chama _show_window() depois.
        
        self.window.bind('<Escape>', lambda e: self._on_close())
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Não chama mainloop aqui: o loop Tk roda uma vez no app.

    def _center_window(self) -> None:
        if not self.window:
            return
        self.window.update_idletasks()
        w = self.window.winfo_width()
        h = self.window.winfo_height()
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
    
    def _on_close(self):
        """Fecha"""
        if self.window:
            try:
                self.window.withdraw()
            except Exception:
                try:
                    self.window.destroy()
                except Exception:
                    pass
