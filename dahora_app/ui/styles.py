"""
Estilos Windows 11 para a aplicação
"""
import tkinter as tk
from tkinter import ttk, font


class Windows11Style:
    """Gerenciador de estilos Windows 11"""
    
    # Cores Windows 11 Dark Mode
    # Cores Windows 11 Dark Mode (Melhoradas)
    COLORS_DARK = {
        'bg': '#1C1C1C',           # Menos escuro que antes (era #121212)
        'bg_dark': '#0F0F0F',      # Preto profundo para contraste
        'text': '#FFFFFF',         # Branco puro para melhor legibilidade
        'text_secondary': '#B3B3B3', # Cinza mais claro (era #A0A0A0)
        'accent': '#0078D4',       # Azul oficial do Windows 11
        'accent_hover': '#106EBE', # Azul mais escuro para hover
        'success': '#107C10',      # Verde
        'warning': '#FCE100',      # Amarelo
        'error': '#FF4343',        # Vermelho mais suave
        'border': '#323130',       # Bordas mais visíveis (era #2b2b2b)
        'white': '#252423',        # Superfícies mais claras (era #1E1E1E)
        'input_bg': '#323130',     # Fundo de inputs mais claro
        'button_bg': '#3B3A39',    # Botão padrão mais claro
        'button_hover': '#484644', # Botão hover mais claro
    }

    # Cores Windows 11 Light Mode (Melhoradas)
    COLORS_LIGHT = {
        'bg': '#FAFAFA',           # Background mais suave (era #F3F3F3)
        'bg_dark': '#F0F0F0',      # Background secundário
        'text': '#1F1F1F',         # Texto quase preto para melhor contraste
        'text_secondary': '#605E5C', # Cinza mais escuro para melhor legibilidade
        'accent': '#0078D4',       # Azul oficial do Windows 11
        'accent_hover': '#106EBE', # Azul mais escuro para hover
        'success': '#107C10',      # Verde
        'warning': '#F7630C',      # Laranja aviso
        'error': '#D13438',        # Vermelho erro
        'border': '#E1DFDD',       # Bordas mais suaves
        'white': '#FFFFFF',        # Branco puro
        'input_bg': '#FFFFFF',     # Fundo de inputs
        'button_bg': '#F3F2F1',    # Botão padrão
        'button_hover': '#EDEBE9', # Botão hover
    }

    # Cores atuais (serão definidas dinamicamente)
    COLORS = COLORS_DARK
    
    # Fontes Windows 11
    FONTS = {
        'default': ('Segoe UI', 9),
        'heading': ('Segoe UI', 12, 'bold'),
        'title': ('Segoe UI', 14, 'bold'),
        'small': ('Segoe UI', 8),
        'button': ('Segoe UI', 9),
        'input': ('Segoe UI', 9),
    }
    
    # Espaçamentos
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 20,
        'xxl': 24,
    }
    
    @staticmethod
    def get_system_theme() -> str:
        """
        Detecta o tema do sistema (Dark/Light) via registro
        Returns: 'dark' ou 'light'
        """
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return 'light' if value == 1 else 'dark'
        except Exception:
            return 'dark' # Fallback seguro

    @staticmethod
    def apply_dark_title_bar(window: tk.Tk):
        """
        Força a barra de título escura no Windows 10/11
        """
        try:
            import ctypes
            from ctypes import windll, c_int, byref, sizeof
            
            window.update()
            hwnd = windll.user32.GetParent(window.winfo_id())
            
            # Tenta ativar Dark Mode na barra de título
            # 20 = DWMWA_USE_IMMERSIVE_DARK_MODE (Win 11 / Win 10 20H1+)
            # 19 = DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 (Win 10 1903)
            
            value = c_int(1) # 1 = True
            
            # Tenta primeiro o atributo 20
            if windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(value), sizeof(value)) != 0:
                # Se falhar (retorno != 0), tenta o atributo 19
                windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, byref(value), sizeof(value))
        except Exception:
            pass

    @staticmethod
    def configure_window(window: tk.Tk, title: str = "Dahora App", size: str = "700x450"):
        """Configura janela com estilo Windows 11"""
        window.title(title)
        window.geometry(size)
        
        # Detecta tema do sistema automaticamente
        system_theme = Windows11Style.get_system_theme()
        if system_theme == 'light':
            Windows11Style.COLORS = Windows11Style.COLORS_LIGHT
        else:
            Windows11Style.COLORS = Windows11Style.COLORS_DARK
        
        # Aplica dark title bar apenas se estiver em modo escuro
        if system_theme == 'dark':
            window.after(100, lambda: Windows11Style.apply_dark_title_bar(window))
            
        window.configure(bg=Windows11Style.COLORS['bg'])
        
    @staticmethod
    def configure_listbox(listbox: tk.Listbox):
        """Configura cores de um Listbox (widget nativo não-ttk)"""
        listbox.configure(
            background=Windows11Style.COLORS['input_bg'],
            foreground=Windows11Style.COLORS['text'],
            selectbackground=Windows11Style.COLORS['accent'],
            selectforeground='#000000',
            borderwidth=1,
            relief='flat',
            highlightthickness=1,
            highlightbackground=Windows11Style.COLORS['border'],
            highlightcolor=Windows11Style.COLORS['accent']
        )

    @staticmethod
    def configure_styles(window: tk.Tk):
        """Configura todos os estilos ttk"""
        style = ttk.Style(window)
        
        # Usa tema 'clam' para controle total das cores (evita cinza do sistema)
        style.theme_use('clam')
        
        # Frame
        style.configure("TFrame", 
                       background=Windows11Style.COLORS['bg'])
                       
        # Card (Frame com cor de superfície) - SEM BORDA (Flat)
        style.configure("Card.TFrame",
                       background=Windows11Style.COLORS['white'],
                       relief='flat',
                       borderwidth=0)
        
        # Label
        style.configure("TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'])
        
        style.configure("Heading.TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['heading'])
        
        style.configure("Title.TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['title'])
        
        style.configure("Secondary.TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text_secondary'],
                       font=Windows11Style.FONTS['default'])
                       
        # Labels dentro de Cards
        style.configure("Card.TLabel",
                       background=Windows11Style.COLORS['white'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'])
                       
        style.configure("Card.TCheckbutton",
                       background=Windows11Style.COLORS['white'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'])
        
    # ... (previous code) ...

        # Button - estilo moderno FLAT (Windows 11: ~32px height, 4px radius simulated via padding/relief)
        style.configure("TButton",
                       font=Windows11Style.FONTS['button'],
                       padding=(24, 6), # Mais largo, altura controlada (~32px total)
                       borderwidth=0,
                       relief='flat',
                       background=Windows11Style.COLORS['button_bg'],
                       foreground=Windows11Style.COLORS['text'])
        
        style.map("TButton",
                 background=[('active', Windows11Style.COLORS['button_hover']),
                           ('pressed', Windows11Style.COLORS['bg_dark'])],
                 foreground=[('active', Windows11Style.COLORS['text'])],
                 relief=[('pressed', 'flat')])
        
        # Primary Button (Accent Color)
        style.configure("Primary.TButton",
                       font=Windows11Style.FONTS['button'],
                       background=Windows11Style.COLORS['accent'],
                       foreground='#FFFFFF', # Texto branco no accent
                       padding=(24, 6))
        
        style.map("Primary.TButton",
                 background=[('active', Windows11Style.COLORS.get('accent_hover', '#106EBE')),
                           ('pressed', '#005A9E')], # Azul mais escuro para pressed
                 foreground=[('active', '#FFFFFF')])
        
        # Entry - estilo moderno (Windows 11: MinHeight 32px, Padding 10,6)
        style.configure("TEntry",
                       fieldbackground=Windows11Style.COLORS['input_bg'],
                       foreground=Windows11Style.COLORS['text'],
                       insertcolor=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['input'],
                       borderwidth=1,
                       relief='flat',
                       padding=(10, 6)) # Padding lateral maior, vertical ajustado para 32px
        
        style.map("TEntry",
                 bordercolor=[('focus', Windows11Style.COLORS['accent'])],
                 lightcolor=[('focus', Windows11Style.COLORS['accent'])],
                 darkcolor=[('focus', Windows11Style.COLORS['accent'])])
        
        # Spinbox
        style.configure("TSpinbox",
                       fieldbackground=Windows11Style.COLORS['input_bg'],
                       foreground=Windows11Style.COLORS['text'],
                       insertcolor=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['input'],
                       borderwidth=1,
                       relief='flat',
                       padding=(10, 6))
        
        style.map("TSpinbox",
                 bordercolor=[('focus', Windows11Style.COLORS['accent'])],
                 lightcolor=[('focus', Windows11Style.COLORS['accent'])],
                 darkcolor=[('focus', Windows11Style.COLORS['accent'])])
        
        # Checkbutton
        style.configure("TCheckbutton",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'],
                       padding=(4, 0)) # Espaçamento do texto
        
        # Treeview
        style.configure("Treeview",
                       background=Windows11Style.COLORS['white'],
                       foreground=Windows11Style.COLORS['text'],
                       fieldbackground=Windows11Style.COLORS['white'],
                       font=Windows11Style.FONTS['default'],
                       rowheight=36, # Mais alto para toque/modernidade
                       borderwidth=0,
                       relief='flat')
        
        style.configure("Treeview.Heading",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=('Segoe UI', 9, 'bold'),
                       borderwidth=0,
                       relief='flat',
                       padding=(12, 10))
        
        style.map("Treeview",
                 background=[('selected', Windows11Style.COLORS['accent'])],
                 foreground=[('selected', '#000000')],
                 relief=[('selected', 'flat')])
        
        style.map("Treeview.Heading",
                 background=[('active', Windows11Style.COLORS['bg_dark'])],
                 relief=[('pressed', 'flat')])
        
        # Notebook (Tabs)
        style.configure("TNotebook",
                       background=Windows11Style.COLORS['bg'],
                       borderwidth=0,
                       relief='flat')
        
        style.configure("TNotebook.Tab",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text_secondary'],
                       font=Windows11Style.FONTS['default'],
                       padding=(16, 8),
                       borderwidth=0)
        
        style.map("TNotebook.Tab",
                 background=[('selected', Windows11Style.COLORS['bg'])], # Fundo igual ao selecionado
                 foreground=[('selected', Windows11Style.COLORS['accent'])], # Texto azul quando selecionado
                 padding=[('selected', (16, 8))]) # Mantém tamanho
        
        # LabelFrame
        style.configure("TLabelframe",
                       background=Windows11Style.COLORS['white'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'],
                       borderwidth=1,
                       relief='flat',
                       bordercolor=Windows11Style.COLORS['border'])
        
        style.configure("TLabelframe.Label",
                       background=Windows11Style.COLORS['white'],
                       foreground=Windows11Style.COLORS['text'],
                       font=('Segoe UI', 9, 'bold'))
        
        # Separator
        style.configure("TSeparator",
                       background=Windows11Style.COLORS['border'])
                       
        # Scrollbar
        style.configure("TScrollbar",
                       background='#424242',
                       troughcolor=Windows11Style.COLORS['bg'],
                       bordercolor=Windows11Style.COLORS['bg'],
                       arrowcolor=Windows11Style.COLORS['text'],
                       borderwidth=0,
                       relief='flat')
        
        style.map("TScrollbar",
                 background=[('active', '#505050'), 
                           ('pressed', Windows11Style.COLORS['accent'])])
