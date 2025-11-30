"""
Dialog para editar/criar um shortcut
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Callable, Optional, Dict, Any
from datetime import datetime
from dahora_app.ui.styles import Windows11Style

class ShortcutEditorDialog:
    """Dialog para editar/criar um shortcut"""
    
    def __init__(self, parent: tk.Tk, shortcut: Optional[Dict[str, Any]], 
                 on_save: Callable, on_validate_hotkey: Optional[Callable]):
        """Inicializa o editor"""
        self.parent = parent
        self.shortcut = shortcut.copy() if shortcut else {}
        self.on_save = on_save
        self.on_validate_hotkey = on_validate_hotkey
        
        self.window: Optional[tk.Toplevel] = None
        self.hotkey_var = tk.StringVar(value=self.shortcut.get("hotkey", ""))
        self.prefix_var = tk.StringVar(value=self.shortcut.get("prefix", ""))
        self.description_var = tk.StringVar(value=self.shortcut.get("description", ""))
        self.enabled_var = tk.BooleanVar(value=self.shortcut.get("enabled", True))
        
        self.validation_label: Optional[ttk.Label] = None
        self.preview_label: Optional[ttk.Label] = None
        
        self.is_detecting = False
        self.detected_keys = set()
    
    def show(self) -> None:
        """Mostra o dialog de edição"""
        is_new = not self.shortcut or "id" not in self.shortcut
        title = "Adicionar Atalho" if is_new else "Editar Atalho"
        
        self.window = tk.Toplevel(self.parent)
        
        # Aplica estilo Windows 11
        Windows11Style.configure_window(self.window, title, "500x380")
        Windows11Style.configure_styles(self.window)
        
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=(16, 12), style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Prefixo
        ttk.Label(main_frame, text="Prefixo:", style="Card.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
        prefix_entry = ttk.Entry(main_frame, textvariable=self.prefix_var, width=40)
        prefix_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        prefix_entry.bind("<KeyRelease>", lambda e: self._update_preview())
        
        # Descrição
        ttk.Label(main_frame, text="Descrição:", style="Card.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        description_entry = ttk.Entry(main_frame, textvariable=self.description_var, width=40)
        description_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Hotkey
        ttk.Label(main_frame, text="Atalho:", style="Card.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        hotkey_frame = ttk.Frame(main_frame, style="Card.TFrame")
        hotkey_frame.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        
        hotkey_entry = ttk.Entry(hotkey_frame, textvariable=self.hotkey_var)
        hotkey_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        hotkey_entry.bind("<KeyRelease>", lambda e: self._validate_hotkey())
        
        detect_button = ttk.Button(hotkey_frame, text="Detectar", command=self._start_detecting)
        detect_button.pack(side=tk.LEFT)
        
        # Validação
        self.validation_label = ttk.Label(main_frame, text="", foreground="gray", style="Card.TLabel")
        self.validation_label.grid(row=3, column=1, sticky=tk.W, pady=(0, 5))
        
        # Preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview")
        preview_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E, pady=10)
        
        self.preview_label = ttk.Label(preview_frame, text="", font=("Segoe UI", 9, "bold"), style="Card.TLabel")
        self.preview_label.pack(padx=10, pady=5)
        
        # Enabled checkbox
        ttk.Checkbutton(main_frame, text="Habilitar este atalho", 
                       variable=self.enabled_var, style="Card.TCheckbutton").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Botões (padrão Windows - sem emojis)
        buttons_frame = ttk.Frame(main_frame, style="Card.TFrame")
        buttons_frame.grid(row=6, column=0, columnspan=2, sticky=tk.E, pady=(20, 0))
        
        ttk.Button(buttons_frame, text="Cancelar", 
                  command=self._on_cancel_clicked, width=12).pack(side=tk.RIGHT, padx=(8, 0))
        ttk.Button(buttons_frame, text="OK", 
                  command=self._on_save_clicked, width=12, default="active").pack(side=tk.RIGHT)
        
        # Configure grid
        main_frame.columnconfigure(1, weight=1)
        
        # Atualiza preview inicial
        self._update_preview()
        self._validate_hotkey()
        
        # Centraliza
        self.window.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def _validate_hotkey(self) -> None:
        """Valida o hotkey em tempo real"""
        if not self.validation_label:
            return
        
        hotkey = self.hotkey_var.get().strip()
        
        if not hotkey:
            self.validation_label.config(text="Digite um atalho", foreground="gray")
            return
        
        if self.on_validate_hotkey:
            exclude_id = self.shortcut.get("id") if self.shortcut else None
            valid, msg = self.on_validate_hotkey(hotkey, exclude_id)
            
            if valid:
                self.validation_label.config(text=f"Hotkey válido", foreground="green")
            else:
                self.validation_label.config(text=f"{msg}", foreground="red")
        else:
            self.validation_label.config(text="", foreground="gray")
    
    def _update_preview(self) -> None:
        """Atualiza o preview do resultado"""
        if not self.preview_label:
            return
        
        prefix = self.prefix_var.get().strip()
        now = datetime.now()
        timestamp = now.strftime("%d.%m.%Y-%H:%M")
        
        if prefix:
            preview = f"[{prefix}-{timestamp}]"
        else:
            preview = f"[{timestamp}]"
        
        self.preview_label.config(text=preview)
    
    def _start_detecting(self) -> None:
        """Inicia detecção de teclas"""
        try:
            import keyboard  # Lazy import apenas quando necessário
        except ImportError:
            messagebox.showerror("Erro", "Biblioteca 'keyboard' não disponível.\nInstale com: pip install keyboard")
            return
        
        self.is_detecting = True
        self.detected_keys.clear()
        
        # Cria janela de detecção
        detect_window = tk.Toplevel(self.window)
        detect_window.title("Detectar Teclas")
        detect_window.geometry("400x200")
        detect_window.transient(self.window)
        detect_window.grab_set()
        
        ttk.Label(detect_window, text="Pressione a combinação de teclas desejada...", 
                 font=("Segoe UI", 9)).pack(pady=20)
        
        keys_label = ttk.Label(detect_window, text="", font=("Segoe UI", 11, "bold"))
        keys_label.pack(pady=10)
        
        ttk.Button(detect_window, text="Cancelar", 
                  command=lambda: self._stop_detecting(detect_window, None)).pack(pady=20)
        
        # Hook de teclado
        def on_key(event):
            if not self.is_detecting:
                return
            
            key_name = event.name.lower()
            
            # Adiciona modificadores
            if key_name in ["ctrl", "shift", "alt"]:
                self.detected_keys.add(key_name)
            else:
                # Tecla final pressionada
                self.detected_keys.add(key_name)
                
                # Monta hotkey
                modifiers = sorted([k for k in self.detected_keys if k in ["ctrl", "shift", "alt"]])
                keys = [k for k in self.detected_keys if k not in ["ctrl", "shift", "alt"]]
                
                if modifiers and keys:
                    hotkey = "+".join(modifiers + keys)
                    self._stop_detecting(detect_window, hotkey)
                    return
            
            # Atualiza label
            display = " + ".join(sorted(self.detected_keys)).upper()
            keys_label.config(text=display)
        
        keyboard.hook(on_key)
        
        # Centraliza
        detect_window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (detect_window.winfo_width() // 2)
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (detect_window.winfo_height() // 2)
        detect_window.geometry(f"+{x}+{y}")
    
    def _stop_detecting(self, detect_window: tk.Toplevel, hotkey: Optional[str]) -> None:
        """Para a detecção de teclas"""
        self.is_detecting = False
        
        try:
            import keyboard
            keyboard.unhook_all()
            keyboard.unhook_all()  # Chama duas vezes para garantir
        except Exception as e:
            logging.warning(f"Erro ao remover hooks de teclado: {e}")
        
        detect_window.destroy()
        
        if hotkey:
            self.hotkey_var.set(hotkey)
            self._validate_hotkey()
    
    def _on_save_clicked(self) -> None:
        """Callback do botão OK"""
        hotkey = self.hotkey_var.get().strip()
        prefix = self.prefix_var.get().strip()
        
        if not hotkey:
            messagebox.showwarning("Aviso", "O campo Atalho é obrigatório")
            return
        
        # Valida hotkey
        if self.on_validate_hotkey:
            exclude_id = self.shortcut.get("id") if self.shortcut else None
            valid, msg = self.on_validate_hotkey(hotkey, exclude_id)
            if not valid:
                messagebox.showerror("Erro", f"Atalho inválido:\n{msg}")
                return
        
        # Atualiza dados
        self.shortcut["hotkey"] = hotkey
        self.shortcut["prefix"] = prefix
        self.shortcut["description"] = self.description_var.get().strip()
        self.shortcut["enabled"] = self.enabled_var.get()
        
        # Chama callback de salvamento
        self.on_save(self.shortcut)
        
        self.window.destroy()
    
    def _on_cancel_clicked(self) -> None:
        """Callback do botão Cancelar"""
        self.window.destroy()
