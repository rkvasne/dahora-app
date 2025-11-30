"""
Tela Sobre - Estilo Windows Nativo
"""
import tkinter as tk
from tkinter import ttk
import webbrowser
from dahora_app.ui.styles import Windows11Style


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
        Windows11Style.configure_window(self.window, "Sobre - Dahora App", "500x400")
        Windows11Style.configure_styles(self.window)
        
        # Frame principal (exatamente como search_dialog)
        main = ttk.Frame(self.window, padding=(16, 12, 16, 12))
        main.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Título
        ttk.Label(
            main,
            text="Dahora App",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(10, 5))
        
        ttk.Label(
            main,
            text="Gerenciador Inteligente de Clipboard",
            font=("Segoe UI", 9)
        ).pack(pady=(0, 20))
        
        # Versão
        version_frame = ttk.LabelFrame(main, text="Versão", padding=(10, 10))
        version_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(version_frame, text="v0.2.0", font=("Segoe UI", 9, "bold")).pack()
        
        # Informações
        info_frame = ttk.LabelFrame(main, text="Informações", padding=(10, 10))
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        info_text = (
            "O Dahora App facilita a inserção de timestamps\n"
            "formatados no seu clipboard com atalhos de teclado\n"
            "personalizáveis.\n\n"
            "Recursos:\n"
            "  • Atalhos de teclado customizáveis\n"
            "  • Prefixos personalizados por atalho\n"
            "  • Histórico inteligente de clipboard\n"
            "  • Busca rápida no histórico\n"
            "  • Caracteres de delimitação configuráveis\n"
            "  • Interface nativa Windows 11\n\n"
            "Desenvolvido com Python e Tkinter"
        )
        
        ttk.Label(
            info_frame,
            text=info_text,
            font=("Segoe UI", 9),
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
        # Links
        links_frame = ttk.LabelFrame(main, text="Links", padding=(10, 10))
        links_frame.pack(fill=tk.X, pady=(0, 10))
        
        def open_github():
            webbrowser.open("https://github.com/rkvasne/dahora-app")
        
        link_btn = ttk.Button(links_frame, text="GitHub Repository", command=open_github)
        link_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # Botão Fechar (exatamente como search_dialog)
        buttons = ttk.Frame(main)
        buttons.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(buttons, text="Fechar", command=self._on_close).pack(side=tk.RIGHT)
        
        # Protocolo de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Bind ESC
        self.window.bind('<Escape>', lambda e: self._on_close())
        
        # Centraliza janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
        
        self.window.mainloop()
    
    def _on_close(self):
        """Fecha a janela"""
        if self.window:
            self.window.destroy()
            self.window = None
