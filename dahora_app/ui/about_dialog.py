"""
Tela Sobre - Estilo Windows Nativo
"""
import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import ImageTk
from dahora_app.ui.styles import Windows11Style
from dahora_app.ui.icon_manager import IconManager
from dahora_app.constants import APP_VERSION


class AboutDialog:
    """Janela Sobre com informações do aplicativo (estilo Windows nativo)"""
    
    def __init__(self):
        """Inicializa o dialog"""
        self.window = None
    
    def show(self):
        """Mostra a janela Sobre"""
        if self.window is not None:
            self.window.lift()
            self.window.focus_force()
            return
        
        self._create_window()
    
    def _create_window(self):
        """Cria a janela"""
        self.window = tk.Tk()
        # Configura estilo Windows 11 (Dark Mode)
        Windows11Style.configure_window(self.window, "Sobre - Dahora App", "500x450")
        try:
            self.window.iconbitmap(IconManager.resolve_icon_path())
        except Exception:
            pass
        Windows11Style.configure_styles(self.window)
        
        # Frame principal
        main = ttk.Frame(self.window, padding=(20, 20, 20, 20))
        main.pack(fill=tk.BOTH, expand=True)
        
        # === LOGO ===
        try:
            # Carrega ícone, redimensiona para 64x64
            icon_img = IconManager.load_icon()
            icon_img = icon_img.resize((64, 64))
            self.photo_icon = ImageTk.PhotoImage(icon_img)

            logo_label = ttk.Label(main, image=self.photo_icon)
            logo_label.pack(pady=(0, 10))
        except Exception:
            pass

        # Título
        ttk.Label(
            main,
            text="Dahora App",
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(0, 5))

        ttk.Label(
            main,
            text="Gerenciador Inteligente de Clipboard",
            font=("Segoe UI", 10),
            foreground="#aaaaaa",
        ).pack(pady=(0, 20))

        # Versão
        version_frame = ttk.Frame(main)
        version_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            version_frame,
            text=f"Versão v{APP_VERSION}",
            font=("Segoe UI", 10, "bold"),
            background="#2d2d2d",
            foreground="#ffffff",
            padding=(10, 5),
        ).pack()
        
        # Informações
        info_text = (
            "O Dahora App facilita a inserção de timestamps formatados\n"
            "no seu clipboard com atalhos de teclado personalizáveis.\n\n"
            "• Colagem Automática & Preservação de Clipboard\n"
            "• Atalhos Ilimitados & Prefixos Personalizados\n"
            "• Histórico Inteligente & Busca Rápida (Ctrl+Shift+F)\n"
            "• Zero Telemetria & 100% Offline"
        )
        
        ttk.Label(
            main,
            text=info_text,
            font=("Segoe UI", 9),
            justify=tk.CENTER,
            foreground="#cccccc"
        ).pack(pady=(0, 20))
        
        # Links
        links_frame = ttk.Frame(main)
        links_frame.pack(pady=(0, 20))
        
        def open_github():
            webbrowser.open("https://github.com/rkvasne/dahora-app")
            
        def open_website():
            webbrowser.open("https://kvasne.com")
        
        ttk.Button(links_frame, text="GitHub", command=open_github).pack(side=tk.LEFT, padx=5)
        ttk.Button(links_frame, text="Website", command=open_website).pack(side=tk.LEFT, padx=5)
        
        # Copyright
        ttk.Label(
            main,
            text="© 2025 Raphael Kvasne. Licença MIT.",
            font=("Segoe UI", 8),
            foreground="#666666"
        ).pack(side=tk.BOTTOM, pady=(10, 0))
        
        # Protocolo de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Bind ESC
        self.window.bind('<Escape>', lambda e: self._on_close())
        
        # Centraliza janela
        self.window.update_idletasks()
        try:
            x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
            y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
            self.window.geometry(f"+{int(x)}+{int(y)}")
        except Exception:
            pass
        
        self.window.mainloop()
    
    def _on_close(self):
        """Fecha a janela"""
        if self.window:
            self.window.destroy()
            self.window = None
