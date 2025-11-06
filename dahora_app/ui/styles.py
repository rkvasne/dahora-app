"""
Estilos Windows 11 para a aplicação
"""
import tkinter as tk
from tkinter import ttk, font


class Windows11Style:
    """Gerenciador de estilos Windows 11"""
    
    # Cores Windows 11
    COLORS = {
        'bg': '#F3F3F3',           # Background claro
        'bg_dark': '#E6E6E6',      # Background escuro
        'text': '#202020',          # Texto principal
        'text_secondary': '#666666', # Texto secundário
        'accent': '#0066CC',        # Azul accent
        'success': '#107C10',       # Verde sucesso
        'warning': '#F7630C',       # Laranja aviso
        'error': '#D13438',         # Vermelho erro
        'border': '#D1D1D1',        # Bordas
        'white': '#FFFFFF',         # Branco puro
    }
    
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
    def configure_window(window: tk.Tk, title: str = "Dahora App", size: str = "700x450"):
        """Configura janela com estilo Windows 11"""
        window.title(title)
        window.geometry(size)
        window.configure(bg=Windows11Style.COLORS['bg'])
        
    @staticmethod
    def configure_styles(window: tk.Tk):
        """Configura todos os estilos ttk"""
        style = ttk.Style(window)
        
        # Usa tema nativo do Windows
        try:
            style.theme_use('vista')  # Windows Vista/7/8/10/11
        except:
            try:
                style.theme_use('winnative')  # Fallback Windows
            except:
                style.theme_use('clam')  # Fallback universal
        
        # Frame
        style.configure("TFrame", 
                       background=Windows11Style.COLORS['bg'])
        
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
        
        # Button - estilo moderno
        style.configure("TButton",
                       font=Windows11Style.FONTS['button'],
                       padding=(16, 8),
                       borderwidth=0,
                       relief='flat',
                       background=Windows11Style.COLORS['white'],
                       foreground=Windows11Style.COLORS['text'])
        
        style.map("TButton",
                 background=[('active', Windows11Style.COLORS['bg_dark']),
                           ('pressed', Windows11Style.COLORS['bg_dark'])],
                 relief=[('pressed', 'flat')])
        
        # Primary Button
        style.configure("Primary.TButton",
                       font=Windows11Style.FONTS['button'],
                       padding=(12, 6))
        
        # Entry - altura maior e bordas suaves
        style.configure("TEntry",
                       fieldbackground=Windows11Style.COLORS['white'],
                       font=Windows11Style.FONTS['input'],
                       borderwidth=1,
                       relief='flat',
                       padding=8)
        
        style.map("TEntry",
                 bordercolor=[('focus', Windows11Style.COLORS['accent'])])
        
        # Spinbox - mesma altura do Entry
        style.configure("TSpinbox",
                       fieldbackground=Windows11Style.COLORS['white'],
                       font=Windows11Style.FONTS['input'],
                       borderwidth=1,
                       relief='flat',
                       padding=8)
        
        style.map("TSpinbox",
                 bordercolor=[('focus', Windows11Style.COLORS['accent'])])
        
        # Checkbutton
        style.configure("TCheckbutton",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'])
        
        # Treeview - visual moderno
        style.configure("Treeview",
                       background=Windows11Style.COLORS['white'],
                       foreground=Windows11Style.COLORS['text'],
                       fieldbackground=Windows11Style.COLORS['white'],
                       font=Windows11Style.FONTS['default'],
                       rowheight=32,
                       borderwidth=1,
                       relief='flat')
        
        style.configure("Treeview.Heading",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=('Segoe UI', 9, 'bold'),
                       borderwidth=0,
                       relief='flat',
                       padding=(8, 8))
        
        style.map("Treeview",
                 background=[('selected', Windows11Style.COLORS['accent'])],
                 foreground=[('selected', Windows11Style.COLORS['white'])],
                 relief=[('selected', 'flat')])
        
        style.map("Treeview.Heading",
                 background=[('active', Windows11Style.COLORS['bg_dark'])],
                 relief=[('pressed', 'flat')])
        
        # Notebook (Tabs) - estilo Windows 11
        style.configure("TNotebook",
                       background=Windows11Style.COLORS['bg'],
                       borderwidth=1,
                       relief='flat')
        
        style.configure("TNotebook.Tab",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text_secondary'],
                       font=Windows11Style.FONTS['default'],
                       padding=(20, 10),
                       borderwidth=0)
        
        style.map("TNotebook.Tab",
                 background=[('selected', Windows11Style.COLORS['white'])],
                 foreground=[('selected', Windows11Style.COLORS['accent'])],
                 padding=[('selected', (20, 10))])
        
        # LabelFrame - bordas suaves
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
