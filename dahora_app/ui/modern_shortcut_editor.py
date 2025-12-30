"""
Editor de Atalhos Moderno usando CustomTkinter
Interface Windows 11 com cantos arredondados
"""
import customtkinter as ctk
from typing import Callable, Optional, Dict, Any
from datetime import datetime
import logging
from tkinter import messagebox

from dahora_app.ui.modern_styles import (
    ModernTheme,
    ModernFrame,
    ModernButton,
    ModernEntry,
    ModernLabel,
    ModernScrollableFrame,
)

from dahora_app.utils import format_hotkey_display


class ModernShortcutEditor:
    """Editor de atalhos moderno com CustomTkinter"""
    
    def __init__(self, parent: ctk.CTk, shortcut: Optional[Dict[str, Any]] = None,
                 on_save: Optional[Callable] = None, 
                 on_validate_hotkey: Optional[Callable] = None):
        self.parent = parent
        self.shortcut = shortcut.copy() if shortcut else {}
        self.on_save = on_save
        self.on_validate_hotkey = on_validate_hotkey
        
        self.window: Optional[ctk.CTkToplevel] = None
        self.colors = ModernTheme.get_colors()
        
        # Variáveis
        # Usa master explícito para garantir que os valores apareçam ao editar
        self.var_hotkey = ctk.StringVar(master=self.parent, value=self.shortcut.get("hotkey", ""))
        self.var_prefix = ctk.StringVar(master=self.parent, value=self.shortcut.get("prefix", ""))
        self.var_description = ctk.StringVar(master=self.parent, value=self.shortcut.get("description", ""))
        self.var_enabled = ctk.BooleanVar(master=self.parent, value=self.shortcut.get("enabled", True))
        
        # Labels de feedback
        self.validation_label = None
        self.preview_label = None
        
        # Estado de detecção
        self.is_detecting = False
        self.detected_keys = set()
        self._detect_pressed_mods = set()
        self._detect_main_key: Optional[str] = None
    
    def show(self) -> None:
        """Mostra o editor"""
        if self.window is not None:
            self.window.lift()
            self.window.focus_force()
            return
        
        self._create_window()
    
    def _create_window(self) -> None:
        """Cria a janela do editor"""
        is_new = not self.shortcut or "id" not in self.shortcut
        title = "Adicionar Atalho" if is_new else "Editar Atalho"
        
        # Cria janela
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title(title)
        # Ajusta para telas menores
        screen_w = self.parent.winfo_screenwidth()
        screen_h = self.parent.winfo_screenheight()
        width = max(480, min(550, screen_w - 140))
        height = max(460, min(520, screen_h - 200))
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(False, False)
        self.window.configure(fg_color=self.colors['bg'])
        
        # Modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Dark title bar
        try:
            import ctypes
            from ctypes import windll, c_int, byref, sizeof
            self.window.update()
            hwnd = windll.user32.GetParent(self.window.winfo_id())
            value = c_int(1)
            windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(value), sizeof(value))
        except Exception:
            pass
        
        # Container principal
        main = ctk.CTkFrame(self.window, fg_color="transparent")
        # Sem padding horizontal externo: permite scrollbar do conteúdo ficar no canto
        main.pack(fill="both", expand=True, padx=0, pady=0)

        # Área rolável (para telas menores) + barra fixa de botões
        content = ModernScrollableFrame(main)
        content.pack(fill="both", expand=True, padx=0, pady=(16, 0))

        # Padding interno do conteúdo (sem deslocar a scrollbar)
        inner = ctk.CTkFrame(content, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        # Título
        ModernLabel(inner, text=f"{'➕' if is_new else '✏️'} {title}", 
               style="title").pack(anchor="w", pady=(0, 14))

        # === PREFIXO ===
        ModernLabel(inner, text="Prefixo", style="heading").pack(anchor="w", pady=(0, 4))
        ModernLabel(inner, text="Texto inserido antes da data/hora", 
               style="muted").pack(anchor="w", pady=(0, 8))

        prefix_entry = ModernEntry(inner, textvariable=self.var_prefix, width=400)
        prefix_entry.pack(anchor="w", pady=(0, 12))
        prefix_entry.bind("<KeyRelease>", lambda e: self._update_preview())

        # === DESCRIÇÃO ===
        ModernLabel(inner, text="Descrição", style="heading").pack(anchor="w", pady=(0, 4))
        ModernLabel(inner, text="Identificação opcional do atalho", 
               style="muted").pack(anchor="w", pady=(0, 8))

        ModernEntry(inner, textvariable=self.var_description, width=400).pack(anchor="w", pady=(0, 12))

        # === ATALHO ===
        ModernLabel(inner, text="Combinação de Teclas", style="heading").pack(anchor="w", pady=(0, 4))
        ModernLabel(inner, text="Ex: ctrl+shift+1, alt+f1, ctrl+alt+d", 
               style="muted").pack(anchor="w", pady=(0, 8))

        hotkey_frame = ctk.CTkFrame(inner, fg_color="transparent")
        hotkey_frame.pack(fill="x", pady=(0, 8))

        hotkey_entry = ModernEntry(hotkey_frame, textvariable=self.var_hotkey, width=300)
        hotkey_entry.pack(side="left", padx=(0, 12))
        hotkey_entry.bind("<KeyRelease>", lambda e: self._validate_hotkey())

        ModernButton(hotkey_frame, text="🎹 Detectar", 
                command=self._start_detecting).pack(side="left")

        # Validação
        self.validation_label = ModernLabel(inner, text="", style="muted")
        self.validation_label.pack(anchor="w", pady=(0, 12))

        # === PREVIEW ===
        preview_card = ModernFrame(inner, fg_color=self.colors['surface'])
        preview_card.pack(fill="x", pady=(0, 12))

        preview_inner = ctk.CTkFrame(preview_card, fg_color="transparent")
        preview_inner.pack(fill="x", padx=16, pady=12)

        ModernLabel(preview_inner, text="Preview do Resultado", 
               style="heading").pack(anchor="w", pady=(0, 8))

        self.preview_label = ctk.CTkLabel(preview_inner, text="", 
                         font=("Consolas", 13, "bold"),
                         text_color=self.colors['accent'])
        self.preview_label.pack(anchor="w")

        # === OPÇÕES ===
        ctk.CTkSwitch(inner, text="Habilitar este atalho",
                 variable=self.var_enabled,
                 fg_color=self.colors['bg_tertiary'],
                 progress_color=self.colors['accent'],
                 button_color=self.colors['text_bright'],
                 text_color=self.colors['text'],
             font=('Segoe UI', ModernTheme.FONT_SIZE_BASE)).pack(anchor="w", pady=(0, 12))

        # Espaço extra no fim do scroll
        ctk.CTkFrame(inner, fg_color="transparent", height=16).pack(fill="x")

        # === BOTÕES (fixos no rodapé do editor) ===
        buttons = ctk.CTkFrame(main, fg_color="transparent")
        buttons.pack(fill="x", pady=(10, 16), padx=16)

        ModernButton(buttons, text="Cancelar", 
                command=self._on_cancel).pack(side="right", padx=(8, 0))
        ModernButton(buttons, text="Salvar", style="primary",
                command=self._on_save).pack(side="right")
        
        # Inicializa
        self._update_preview()
        self._validate_hotkey()
        
        # Centraliza
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
        
        # Atalhos
        self.window.bind('<Escape>', lambda e: self._on_cancel())
        self.window.bind('<Return>', lambda e: self._on_save())
        self.window.protocol("WM_DELETE_WINDOW", self._on_cancel)
    
    def _validate_hotkey(self) -> None:
        """Valida o hotkey em tempo real"""
        if not self.validation_label:
            return
        
        hotkey = self.var_hotkey.get().strip()
        
        if not hotkey:
            self.validation_label.configure(text="Digite um atalho", text_color=self.colors['text_muted'])
            return
        
        if self.on_validate_hotkey:
            exclude_id = self.shortcut.get("id") if self.shortcut else None
            valid, msg = self.on_validate_hotkey(hotkey, exclude_id)
            
            if valid:
                self.validation_label.configure(text="✓ Atalho válido", text_color=self.colors['success'])
            else:
                self.validation_label.configure(text=f"✗ {msg}", text_color=self.colors['error'])
        else:
            self.validation_label.configure(text="", text_color=self.colors['text_muted'])
    
    def _update_preview(self) -> None:
        """Atualiza o preview"""
        if not self.preview_label:
            return
        
        prefix = self.var_prefix.get().strip()
        timestamp = datetime.now().strftime("%d.%m.%Y-%H:%M")
        
        if prefix:
            preview = f"[{prefix}-{timestamp}]"
        else:
            preview = f"[{timestamp}]"
        
        self.preview_label.configure(text=preview)
    
    def _start_detecting(self) -> None:
        """Inicia detecção de teclas"""
        self.is_detecting = True
        self.detected_keys.clear()
        self._detect_pressed_mods.clear()
        self._detect_main_key = None
        
        # Janela de detecção
        detect = ctk.CTkToplevel(self.window)
        detect.title("Detectar Teclas")
        detect.geometry("400x180")
        detect.resizable(False, False)
        detect.configure(fg_color=self.colors['bg'])
        detect.transient(self.window)
        detect.grab_set()
        
        # Dark title bar
        try:
            import ctypes
            from ctypes import windll, c_int, byref, sizeof
            detect.update()
            hwnd = windll.user32.GetParent(detect.winfo_id())
            value = c_int(1)
            windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(value), sizeof(value))
        except Exception:
            pass
        
        container = ctk.CTkFrame(detect, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=24, pady=24)
        
        ModernLabel(container, text="Pressione a combinação de teclas...",
                   style="heading").pack(pady=(0, 16))
        
        keys_label = ctk.CTkLabel(container, text="", 
                                 font=("Segoe UI", 16, "bold"),
                                 text_color=self.colors['accent'])
        keys_label.pack(pady=(0, 20))
        
        ModernButton(container, text="Cancelar",
                    command=lambda: self._stop_detecting(detect, None)).pack()

        def normalize_key(keysym: str) -> Optional[str]:
            k = keysym
            if not k:
                return None

            k_low = k.lower()

            # Modificadores
            if k_low in {"control_l", "control_r", "control"}:
                return "ctrl"
            if k_low in {"shift_l", "shift_r", "shift"}:
                return "shift"
            if k_low in {"alt_l", "alt_r", "alt", "option_l", "option_r"}:
                return "alt"

            # Teclas comuns
            mapping = {
                "return": "enter",
                "escape": "esc",
                "backspace": "backspace",
                "space": "space",
                "tab": "tab",
                "delete": "del",
                "prior": "pageup",
                "next": "pagedown",
                "left": "left",
                "right": "right",
                "up": "up",
                "down": "down",
            }
            if k_low in mapping:
                return mapping[k_low]

            # F-keys
            if k_low.startswith("f") and k_low[1:].isdigit():
                return k_low

            # Letras/números (keysym pode vir como '1', 'a', etc.)
            if len(k) == 1:
                return k_low

            return k_low

        def update_display() -> None:
            parts = sorted(self._detect_pressed_mods)
            if self._detect_main_key:
                parts.append(self._detect_main_key)
            self.detected_keys = set(parts)
            keys_label.configure(text=format_hotkey_display("+".join(parts)))

        def finalize_if_ready() -> None:
            mods = [m for m in ["ctrl", "shift", "alt"] if m in self._detect_pressed_mods]
            if mods and self._detect_main_key:
                self._stop_detecting(detect, "+".join(mods + [self._detect_main_key]))

        def on_key_press(e):
            if not self.is_detecting:
                return
            key = normalize_key(getattr(e, "keysym", ""))
            if not key:
                return

            if key in {"ctrl", "shift", "alt"}:
                self._detect_pressed_mods.add(key)
                update_display()
                return

            # Primeira tecla não-modificadora
            self._detect_main_key = key
            update_display()
            finalize_if_ready()

        def on_key_release(e):
            if not self.is_detecting:
                return
            key = normalize_key(getattr(e, "keysym", ""))
            if key in {"ctrl", "shift", "alt"}:
                # mantém o display atualizado, mas não zera main_key
                self._detect_pressed_mods.discard(key)
                update_display()

        # Captura teclas no próprio diálogo
        detect.bind("<KeyPress>", on_key_press)
        detect.bind("<KeyRelease>", on_key_release)
        detect.bind("<Escape>", lambda e: self._stop_detecting(detect, None))
        detect.focus_force()
        
        # Centraliza
        detect.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (detect.winfo_width() // 2)
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (detect.winfo_height() // 2)
        detect.geometry(f"+{x}+{y}")
    
    def _stop_detecting(self, detect_window: ctk.CTkToplevel, hotkey: Optional[str]) -> None:
        """Para a detecção"""
        self.is_detecting = False
        
        detect_window.destroy()
        
        if hotkey:
            self.var_hotkey.set(hotkey)
            self._validate_hotkey()
    
    def _on_save(self) -> None:
        """Salva o atalho"""
        hotkey = self.var_hotkey.get().strip()
        prefix = self.var_prefix.get().strip()
        
        if not hotkey:
            return
        
        # Valida
        if self.on_validate_hotkey:
            exclude_id = self.shortcut.get("id") if self.shortcut else None
            valid, msg = self.on_validate_hotkey(hotkey, exclude_id)
            if not valid:
                return
        
        # Prepara dados
        result = self.shortcut.copy()
        result.update({
            "hotkey": hotkey,
            "prefix": prefix,
            "description": self.var_description.get().strip(),
            "enabled": self.var_enabled.get()
        })
        
        # Callback
        if self.on_save:
            self.on_save(result)
        
        self._close()
    
    def _on_cancel(self) -> None:
        """Cancela"""
        self._close()
    
    def _close(self) -> None:
        """Fecha a janela"""
        if self.window:
            self.window.grab_release()
            self.window.destroy()
            self.window = None
