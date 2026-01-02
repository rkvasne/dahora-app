"""
Estilos Windows 11 para a aplicação
"""
import tkinter as tk
from tkinter import ttk, font
from typing import Any, cast

Window = tk.Tk | tk.Toplevel


class Windows11Style:
    """Gerenciador de estilos Windows 11"""
    
    # Cores Windows 11 Dark Mode
    # Cores Modernas - Inspiradas em Discord/VS Code/Apps Modernos
    COLORS_DARK = {
        'bg': '#1a1a1a',           # Background principal mais moderno
        'bg_secondary': '#2d2d30',  # Background secundário
        'bg_tertiary': '#3e3e42',   # Background terciário
        'surface': '#252526',       # Superfícies elevadas (cards)
        'surface_hover': '#2d2d30', # Hover em superfícies
        'text': '#cccccc',          # Texto principal suave
        'text_bright': '#ffffff',   # Texto destacado
        'text_muted': '#969696',    # Texto secundário
        'text_disabled': '#6a6a6a', # Texto desabilitado
        'accent': '#007acc',        # Azul moderno (VS Code)
        'accent_hover': '#1177bb',  # Azul hover
        'accent_light': '#4fc3f7',  # Azul claro para destaques
        'success': '#4caf50',       # Verde moderno
        'warning': '#ff9800',       # Laranja moderno
        'error': '#f44336',         # Vermelho moderno
        'border': '#3e3e42',        # Bordas sutis
        'border_focus': '#007acc',  # Bordas em foco
        'shadow': 'rgba(0,0,0,0.3)', # Sombras
        'overlay': 'rgba(0,0,0,0.5)', # Overlays
    }

    # Cores Modernas - Modo Claro
    COLORS_LIGHT = {
        'bg': '#ffffff',            # Background branco puro
        'bg_secondary': '#f8f9fa',  # Background secundário
        'bg_tertiary': '#e9ecef',   # Background terciário
        'surface': '#ffffff',       # Superfícies elevadas
        'surface_hover': '#f8f9fa', # Hover em superfícies
        'text': '#212529',          # Texto principal
        'text_bright': '#000000',   # Texto destacado
        'text_muted': '#6c757d',    # Texto secundário
        'text_disabled': '#adb5bd', # Texto desabilitado
        'accent': '#0066cc',        # Azul moderno
        'accent_hover': '#0052a3',  # Azul hover
        'accent_light': '#66b3ff',  # Azul claro
        'success': '#28a745',       # Verde moderno
        'warning': '#fd7e14',       # Laranja moderno
        'error': '#dc3545',         # Vermelho moderno
        'border': '#dee2e6',        # Bordas sutis
        'border_focus': '#0066cc',  # Bordas em foco
        'shadow': 'rgba(0,0,0,0.1)', # Sombras suaves
        'overlay': 'rgba(0,0,0,0.3)', # Overlays
    }

    # Cores atuais (serão definidas dinamicamente)
    COLORS = COLORS_DARK
    
    # Fontes Modernas
    FONTS = {
        'default': ('Segoe UI', 10),        # Ligeiramente maior
        'heading': ('Segoe UI', 14, 'bold'), # Mais proeminente
        'title': ('Segoe UI', 18, 'bold'),   # Títulos grandes
        'subtitle': ('Segoe UI', 12),        # Subtítulos
        'small': ('Segoe UI', 9),           # Texto pequeno
        'button': ('Segoe UI', 10, 'normal'), # Botões sem bold
        'input': ('Segoe UI', 10),          # Inputs
        'mono': ('Consolas', 9),            # Fonte monoespaçada
        'large': ('Segoe UI', 16),          # Texto grande
    }
    
    # Espaçamentos Modernos (mais generosos)
    SPACING = {
        'xs': 6,   # Era 4
        'sm': 12,  # Era 8
        'md': 18,  # Era 12
        'lg': 24,  # Era 16
        'xl': 32,  # Era 20
        'xxl': 48, # Era 24
    }
    
    # Bordas Arredondadas Modernas
    RADIUS = {
        'small': 6,
        'medium': 8,
        'large': 12,
        'xl': 16,
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
    def apply_dark_title_bar(window: Window):
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
    def configure_window(window: Window, title: str = "Dahora App", size: str = "700x450"):
        """Configura janela com estilo moderno"""
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
            
        # Background moderno
        window.configure(bg=Windows11Style.COLORS['bg'])
        
        # Remove bordas padrão para visual mais limpo
        try:
            window.attributes('-alpha', 0.98)  # Transparência sutil
        except:
            pass
        
    @staticmethod
    def configure_listbox(listbox: tk.Listbox):
        """Configura Listbox com estilo moderno e melhor interatividade"""
        cast(Any, listbox).configure(
            background=Windows11Style.COLORS['surface'],
            foreground=Windows11Style.COLORS['text'],
            selectbackground=Windows11Style.COLORS['accent'],
            selectforeground=Windows11Style.COLORS['text_bright'],
            borderwidth=0,
            relief='flat',
            highlightthickness=0,
            font=Windows11Style.FONTS['default'],
            activestyle='none',  # Remove estilo de ativação padrão
            selectborderwidth=0,  # Remove borda da seleção
        )
        
        # Adiciona efeitos de hover personalizados
        try:
            def on_motion(event):
                """Efeito de hover nos itens"""
                index = listbox.nearest(event.y)
                listbox.selection_clear(0, tk.END)
                if 0 <= index < listbox.size():
                    # Não seleciona automaticamente, apenas destaca visualmente
                    pass
            
            def on_leave(event):
                """Remove hover ao sair"""
                # Restaura seleção original se houver
                pass
            
            # Bind eventos (comentado para não interferir com seleção)
            # listbox.bind("<Motion>", on_motion)
            # listbox.bind("<Leave>", on_leave)
            
        except Exception:
            pass

    @staticmethod
    def configure_styles(window: Window):
        """Configura todos os estilos com design moderno"""
        style = ttk.Style(window)
        
        # Usa tema 'clam' para controle total
        style.theme_use('clam')
        
        # === FRAMES MODERNOS ===
        style.configure("TFrame", 
                       background=Windows11Style.COLORS['bg'],
                       relief='flat',
                       borderwidth=0)
                       
        # Card moderno SEM bordas
        style.configure("Card.TFrame",
                       background=Windows11Style.COLORS['surface'],
                       relief='flat',
                       borderwidth=0)
        
        # Card com borda MUITO sutil (quase invisível)
        style.configure("CardBorder.TFrame",
                       background=Windows11Style.COLORS['surface'],
                       relief='flat',
                       borderwidth=0)
        
        # === LABELS MODERNOS (FUNDO CONSISTENTE) ===
        style.configure("TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'])
        
        style.configure("Heading.TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text_bright'],
                       font=Windows11Style.FONTS['heading'])
        
        style.configure("Title.TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text_bright'],
                       font=Windows11Style.FONTS['title'])
        
        style.configure("Subtitle.TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['subtitle'])
        
        style.configure("Muted.TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text_muted'],
                       font=Windows11Style.FONTS['small'])
                       
        # Labels em cards (FUNDO DO CARD)
        style.configure("Card.TLabel",
                       background=Windows11Style.COLORS['surface'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'])
        
        style.configure("CardHeading.TLabel",
                       background=Windows11Style.COLORS['surface'],
                       foreground=Windows11Style.COLORS['text_bright'],
                       font=Windows11Style.FONTS['heading'])
        
        # Labels em frames (FUNDO TRANSPARENTE)
        style.configure("Frame.TLabel",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'])
                       
        # === BOTÕES MODERNOS ===
        # Botão padrão moderno
        style.configure("TButton",
                       font=Windows11Style.FONTS['button'],
                       padding=(24, 12),  # Mais espaçoso
                       borderwidth=0,
                       relief='flat',
                       background=Windows11Style.COLORS['bg_secondary'],
                       foreground=Windows11Style.COLORS['text'],
                       focuscolor='none')  # Remove foco visual
        
        style.map("TButton",
                 background=[('active', Windows11Style.COLORS['bg_tertiary']),
                           ('pressed', Windows11Style.COLORS['border']),
                           ('!active', Windows11Style.COLORS['bg_secondary'])],
                 foreground=[('active', Windows11Style.COLORS['text_bright']),
                           ('pressed', Windows11Style.COLORS['text_bright']),
                           ('!active', Windows11Style.COLORS['text'])],
                 relief=[('pressed', 'flat'),
                        ('!pressed', 'flat')])
        
        # Botão primário moderno
        style.configure("Primary.TButton",
                       font=Windows11Style.FONTS['button'],
                       background=Windows11Style.COLORS['accent'],
                       foreground=Windows11Style.COLORS['text_bright'],
                       padding=(24, 12),
                       borderwidth=0,
                       relief='flat',
                       focuscolor='none')
        
        style.map("Primary.TButton",
                 background=[('active', Windows11Style.COLORS['accent_hover']),
                           ('pressed', Windows11Style.COLORS['accent']),
                           ('!active', Windows11Style.COLORS['accent'])],
                 foreground=[('active', Windows11Style.COLORS['text_bright']),
                           ('pressed', Windows11Style.COLORS['text_bright']),
                           ('!active', Windows11Style.COLORS['text_bright'])],
                 relief=[('pressed', 'flat'),
                        ('!pressed', 'flat')])
        
        # Botão de sucesso
        style.configure("Success.TButton",
                       font=Windows11Style.FONTS['button'],
                       background=Windows11Style.COLORS['success'],
                       foreground=Windows11Style.COLORS['text_bright'],
                       padding=(24, 12),
                       borderwidth=0,
                       relief='flat',
                       focuscolor='none')
        
        style.map("Success.TButton",
                 background=[('active', '#45a049'),  # Verde mais escuro no hover
                           ('pressed', Windows11Style.COLORS['success']),
                           ('!active', Windows11Style.COLORS['success'])],
                 foreground=[('active', Windows11Style.COLORS['text_bright']),
                           ('pressed', Windows11Style.COLORS['text_bright']),
                           ('!active', Windows11Style.COLORS['text_bright'])])
        
        # Botão de perigo
        style.configure("Danger.TButton",
                       font=Windows11Style.FONTS['button'],
                       background=Windows11Style.COLORS['error'],
                       foreground=Windows11Style.COLORS['text_bright'],
                       padding=(24, 12),
                       borderwidth=0,
                       relief='flat',
                       focuscolor='none')
        
        style.map("Danger.TButton",
                 background=[('active', '#d32f2f'),  # Vermelho mais escuro no hover
                           ('pressed', Windows11Style.COLORS['error']),
                           ('!active', Windows11Style.COLORS['error'])],
                 foreground=[('active', Windows11Style.COLORS['text_bright']),
                           ('pressed', Windows11Style.COLORS['text_bright']),
                           ('!active', Windows11Style.COLORS['text_bright'])])
        
        # === INPUTS MODERNOS (SEM BORDAS VISÍVEIS) ===
        style.configure("TEntry",
                       fieldbackground=Windows11Style.COLORS['surface'],
                       foreground=Windows11Style.COLORS['text'],
                       insertcolor=Windows11Style.COLORS['accent'],  # Cursor colorido
                       font=Windows11Style.FONTS['input'],
                       borderwidth=0,  # SEM bordas
                       relief='flat',
                       padding=(16, 12),  # Mais espaçoso
                       focuscolor='none')  # Remove foco padrão
        
        style.map("TEntry",
                 fieldbackground=[('focus', Windows11Style.COLORS['surface']),
                                ('!focus', Windows11Style.COLORS['surface'])],
                 foreground=[('focus', Windows11Style.COLORS['text']),
                           ('!focus', Windows11Style.COLORS['text'])])
        
        # Spinbox moderno SEM bordas
        style.configure("TSpinbox",
                       fieldbackground=Windows11Style.COLORS['surface'],
                       foreground=Windows11Style.COLORS['text'],
                       insertcolor=Windows11Style.COLORS['accent'],
                       font=Windows11Style.FONTS['input'],
                       borderwidth=0,  # SEM bordas
                       relief='flat',
                       padding=(16, 12),
                       focuscolor='none')
        
        style.map("TSpinbox",
                 fieldbackground=[('focus', Windows11Style.COLORS['surface']),
                                ('!focus', Windows11Style.COLORS['surface'])])
        
        # === CHECKBOXES MODERNOS (FUNDO CONSISTENTE) ===
        style.configure("TCheckbutton",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'],
                       padding=(8, 4),
                       borderwidth=0,
                       relief='flat',
                       focuscolor='none')
        
        style.configure("Card.TCheckbutton",
                       background=Windows11Style.COLORS['surface'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'],
                       borderwidth=0,
                       relief='flat',
                       focuscolor='none')
        
        # === NOTEBOOK (TABS) MODERNO - SEM BORDAS ===
        style.configure("TNotebook",
                       background=Windows11Style.COLORS['bg'],
                       borderwidth=0,
                       relief='flat',
                       tabmargins=[0, 0, 0, 0],
                       tabposition='n')
        
        # Remove a borda do notebook completamente
        style.layout("TNotebook", [])
        style.layout("TNotebook.Tab", [
            ("Notebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("Notebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("Notebook.label", {"side": "top", "sticky": ""})
                        ]
                    })
                ]
            })
        ])
        
        style.configure("TNotebook.Tab",
                       background=Windows11Style.COLORS['bg'],
                       foreground=Windows11Style.COLORS['text_muted'],
                       font=Windows11Style.FONTS['default'],
                       padding=(20, 12),
                       borderwidth=0,
                       relief='flat',
                       focuscolor=Windows11Style.COLORS['bg'])
        
        style.map("TNotebook.Tab",
                 background=[('selected', Windows11Style.COLORS['bg']),
                           ('active', Windows11Style.COLORS['bg']),
                           ('!active', Windows11Style.COLORS['bg'])],
                 foreground=[('selected', Windows11Style.COLORS['accent']),
                           ('active', Windows11Style.COLORS['text']),
                           ('!active', Windows11Style.COLORS['text_muted'])],
                 borderwidth=[('selected', 0), ('!selected', 0)],
                 relief=[('selected', 'flat'), ('!selected', 'flat')])
        
        # === LABELFRAME MODERNO (SEM BORDAS) ===
        style.configure("TLabelframe",
                       background=Windows11Style.COLORS['surface'],
                       foreground=Windows11Style.COLORS['text'],
                       font=Windows11Style.FONTS['default'],
                       borderwidth=0,  # SEM bordas
                       relief='flat')
        
        style.configure("TLabelframe.Label",
                       background=Windows11Style.COLORS['surface'],
                       foreground=Windows11Style.COLORS['text_bright'],
                       font=Windows11Style.FONTS['subtitle'])
        
        # === SEPARATOR MODERNO ===
        style.configure("TSeparator",
                       background=Windows11Style.COLORS['border'])
                       
        # === SCROLLBAR OVERLAY INVISÍVEL ===
        style.configure("TScrollbar",
                       background=Windows11Style.COLORS['bg'],  # Mesmo fundo da janela
                       troughcolor=Windows11Style.COLORS['bg'],  # Trilha invisível
                       bordercolor=Windows11Style.COLORS['bg'],  # Borda invisível
                       arrowcolor=Windows11Style.COLORS['bg'],  # Setas invisíveis
                       borderwidth=0,
                       relief='flat',
                       width=8,  # Scrollbar muito fina
                       arrowsize=8)
        
        style.map("TScrollbar",
                 background=[('active', Windows11Style.COLORS['text_muted']), 
                           ('pressed', Windows11Style.COLORS['accent']),
                           ('!active', Windows11Style.COLORS['bg'])],  # Invisível quando não ativa
                 troughcolor=[('active', Windows11Style.COLORS['bg']),
                            ('!active', Windows11Style.COLORS['bg'])],
                 arrowcolor=[('active', Windows11Style.COLORS['text_muted']),
                           ('pressed', Windows11Style.COLORS['accent']),
                           ('!active', Windows11Style.COLORS['bg'])])
    
    @staticmethod
    def create_modern_card(parent, padding=20, **kwargs):
        """Cria um card moderno SEM bordas visíveis"""
        card = ttk.Frame(parent, style="TFrame", padding=padding, **kwargs)
        # Remove qualquer borda ou relevo
        card.configure(relief='flat', borderwidth=0)
        return card
    
    @staticmethod
    def create_modern_button(parent, text, command=None, style="TButton", **kwargs):
        """Cria um botão moderno com espaçamento adequado e efeitos visuais"""
        button = ttk.Button(parent, text=text, command=command, style=style, **kwargs)
        
        # Adiciona efeitos de hover personalizados se possível
        try:
            def on_enter(event):
                """Efeito ao passar o mouse"""
                if style == "Primary.TButton":
                    button.configure(cursor="hand2")
                elif style == "Danger.TButton":
                    button.configure(cursor="hand2")
                else:
                    button.configure(cursor="hand2")
            
            def on_leave(event):
                """Efeito ao sair com o mouse"""
                button.configure(cursor="")
            
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
            
        except Exception:
            # Fallback se houver erro
            pass
            
        return button
    
    @staticmethod
    def create_section_header(parent, text, **kwargs):
        """Cria um cabeçalho de seção moderno"""
        header = ttk.Label(parent, text=text, style="Heading.TLabel", **kwargs)
        return header
    
    @staticmethod
    def create_modern_entry(parent, **kwargs):
        """Cria um campo de entrada moderno"""
        entry = ttk.Entry(parent, style="TEntry", **kwargs)
        return entry
