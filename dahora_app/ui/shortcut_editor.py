"""
Dialog para editar/criar um shortcut
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from dahora_app.utils import format_hotkey_display
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
        self.detected_keys: set[str] = set()
        self._detect_keyboard_hook: Optional[Any] = None
    
    def show(self) -> None:
        """Mostra o dialog de edição"""
        try:
            logging.info("ShortcutEditorDialog.show() iniciado")
            
            is_new = not self.shortcut or "id" not in self.shortcut
            title = "Adicionar Atalho" if is_new else "Editar Atalho"
            
            logging.info(f"Criando janela: {title}, is_new: {is_new}")
            
            if not self.parent:
                logging.error("Parent window é None")
                raise Exception("Janela pai não encontrada")
            
            # Verifica se a janela pai ainda existe
            try:
                self.parent.winfo_exists()
                logging.info("Parent window existe e é válida")
            except tk.TclError as e:
                logging.error(f"Parent window não é válida: {e}")
                raise Exception("Janela pai não é mais válida")
            
            window = tk.Toplevel(self.parent)
            self.window = window
            logging.info("tk.Toplevel criado com sucesso")
            
            # Aplica estilo Windows 11
            Windows11Style.configure_window(window, title, "600x500")
            Windows11Style.configure_styles(window)
            logging.info("Estilos aplicados")
            
            window.resizable(False, False)
            window.transient(self.parent)
            window.grab_set()  # Torna a janela modal
            logging.info("Propriedades da janela configuradas")
            
            self._create_window_content()
            logging.info("Conteúdo da janela criado")
            
            # Força a janela para frente e foca
            window.lift()
            window.focus_force()
            window.attributes('-topmost', True)
            window.after(100, lambda: window.attributes('-topmost', False))
            
            # Verifica se a janela foi realmente criada
            window.update_idletasks()
            if window.winfo_exists():
                logging.info("Janela de edição exibida com sucesso")
            else:
                logging.error("Janela foi criada mas não existe")
                raise Exception("Falha na criação da janela")
            
        except Exception as e:
            logging.error(f"Erro em ShortcutEditorDialog.show(): {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            
            # Fallback: mostra um messagebox simples para coletar dados
            self._show_fallback_dialog()
            
    def _show_fallback_dialog(self):
        """Fallback dialog usando messagebox simples"""
        try:
            from tkinter import simpledialog, messagebox
            
            logging.info("Usando fallback dialog")
            
            is_new = not self.shortcut or "id" not in self.shortcut
            title = "Adicionar Atalho" if is_new else "Editar Atalho"
            
            # Coleta dados básicos
            hotkey = simpledialog.askstring(
                title, 
                "Digite o atalho (ex: ctrl+shift+1):",
                initialvalue=self.shortcut.get("hotkey", "") if self.shortcut else ""
            )
            
            if not hotkey:
                return
                
            prefix = simpledialog.askstring(
                title,
                "Digite o prefixo:",
                initialvalue=self.shortcut.get("prefix", "") if self.shortcut else ""
            )
            
            if not prefix:
                return
                
            description = simpledialog.askstring(
                title,
                "Digite a descrição (opcional):",
                initialvalue=self.shortcut.get("description", "") if self.shortcut else ""
            ) or ""
            
            # Valida hotkey
            if self.on_validate_hotkey:
                exclude_id = self.shortcut.get("id") if self.shortcut else None
                valid, msg = self.on_validate_hotkey(hotkey, exclude_id)
                if not valid:
                    messagebox.showerror("Erro", f"Atalho inválido:\n{msg}")
                    return
            
            # Prepara dados
            result_data = self.shortcut.copy() if self.shortcut else {}
            result_data.update({
                "hotkey": hotkey.strip(),
                "prefix": prefix.strip(),
                "description": description.strip(),
                "enabled": True
            })
            
            # Chama callback
            self.on_save(result_data)
            
            logging.info("Fallback dialog concluído com sucesso")
            
        except Exception as e:
            logging.error(f"Erro no fallback dialog: {e}")
            import tkinter.messagebox as mb
            mb.showerror("Erro", f"Erro ao abrir editor de atalho:\n{str(e)}")
    
    def _create_window_content(self) -> None:
        """Cria o conteúdo da janela com design moderno"""
        try:
            logging.info("Criando conteúdo moderno da janela de edição")
            window = self.window
            if window is None:
                raise Exception("Janela não inicializada")
            
            # Frame principal com padding generoso
            main_frame = Windows11Style.create_modern_card(window, padding=24)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Título da seção
            is_new = not self.shortcut or "id" not in self.shortcut
            title_text = "Adicionar Novo Atalho" if is_new else "Editar Atalho"
            title_label = Windows11Style.create_section_header(main_frame, title_text)
            title_label.pack(anchor="w", pady=(0, 20))
            
            # === SEÇÃO PREFIXO ===
            prefix_section = ttk.Frame(main_frame, style="TFrame")
            prefix_section.pack(fill=tk.X, pady=(0, 16))
            
            ttk.Label(prefix_section, text="Prefixo", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 6))
            ttk.Label(prefix_section, text="Texto que será inserido antes da data/hora", 
                     style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
            
            prefix_entry = Windows11Style.create_modern_entry(prefix_section, textvariable=self.prefix_var, width=40)
            prefix_entry.pack(fill=tk.X)
            prefix_entry.bind("<KeyRelease>", lambda e: self._update_preview())
            
            # === SEÇÃO DESCRIÇÃO ===
            desc_section = ttk.Frame(main_frame, style="TFrame")
            desc_section.pack(fill=tk.X, pady=(0, 16))
            
            ttk.Label(desc_section, text="Descrição", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 6))
            ttk.Label(desc_section, text="Descrição opcional para identificar este atalho", 
                     style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
            
            desc_entry = Windows11Style.create_modern_entry(desc_section, textvariable=self.description_var, width=40)
            desc_entry.pack(fill=tk.X)
            
            # === SEÇÃO ATALHO ===
            hotkey_section = ttk.Frame(main_frame, style="TFrame")
            hotkey_section.pack(fill=tk.X, pady=(0, 16))
            
            ttk.Label(hotkey_section, text="Combinação de Teclas", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 6))
            ttk.Label(hotkey_section, text="Ex: ctrl+shift+1, alt+f1, ctrl+alt+d", 
                     style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
            
            hotkey_frame = ttk.Frame(hotkey_section, style="TFrame")
            hotkey_frame.pack(fill=tk.X)
            
            hotkey_entry = Windows11Style.create_modern_entry(hotkey_frame, textvariable=self.hotkey_var)
            hotkey_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12))
            hotkey_entry.bind("<KeyRelease>", lambda e: self._validate_hotkey())
            
            detect_button = Windows11Style.create_modern_button(hotkey_frame, "Detectar", 
                                                              command=self._start_detecting)
            detect_button.pack(side=tk.RIGHT)
            
            # Validação
            self.validation_label = ttk.Label(hotkey_section, text="", style="Muted.TLabel")
            self.validation_label.pack(anchor="w", pady=(8, 0))
            
            # === PREVIEW MODERNO ===
            preview_card = Windows11Style.create_modern_card(main_frame, padding=16)
            preview_card.pack(fill=tk.X, pady=(0, 16))
            
            ttk.Label(preview_card, text="Preview do Resultado", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 8))
            
            self.preview_label = ttk.Label(preview_card, text="", font=("Consolas", 11, "bold"), 
                                         style="Card.TLabel")
            self.preview_label.pack(anchor="w")
            
            # === OPÇÕES ===
            options_section = ttk.Frame(main_frame, style="TFrame")
            options_section.pack(fill=tk.X, pady=(0, 20))
            
            enabled_check = ttk.Checkbutton(options_section, text="Habilitar este atalho", 
                                          variable=self.enabled_var, style="TCheckbutton")
            enabled_check.pack(anchor="w")
            
            # === BOTÕES MODERNOS ===
            buttons_frame = ttk.Frame(main_frame, style="TFrame")
            buttons_frame.pack(fill=tk.X, pady=(20, 0))
            
            # Botões alinhados à direita com espaçamento moderno
            cancel_btn = Windows11Style.create_modern_button(buttons_frame, "Cancelar", 
                                                           command=self._on_cancel_clicked)
            cancel_btn.pack(side=tk.RIGHT, padx=(12, 0))
            
            save_btn = Windows11Style.create_modern_button(buttons_frame, "Salvar", 
                                                         command=self._on_save_clicked, 
                                                         style="Primary.TButton")
            save_btn.pack(side=tk.RIGHT)
            
            # Atualiza preview inicial
            self._update_preview()
            self._validate_hotkey()
            
            # Centraliza janela
            window.update_idletasks()
            x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (window.winfo_width() // 2)
            y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (window.winfo_height() // 2)
            window.geometry(f"+{x}+{y}")
            
            # Protocolo de fechamento
            window.protocol("WM_DELETE_WINDOW", self._on_cancel_clicked)
            
            # Atalhos de teclado
            window.bind('<Escape>', lambda e: self._on_cancel_clicked())
            window.bind('<Return>', lambda e: self._on_save_clicked())
            
            logging.info("Janela moderna de edição criada com sucesso")
            
        except Exception as e:
            logging.error(f"Erro ao criar conteúdo da janela: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            raise
    
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
        window = self.window
        if window is None:
            return
        try:
            import keyboard  # Lazy import apenas quando necessário
        except ImportError:
            messagebox.showerror("Erro", "Biblioteca 'keyboard' não disponível.\nInstale com: pip install keyboard")
            return
        
        self.is_detecting = True
        self.detected_keys.clear()
        
        # Cria janela de detecção
        detect_window = tk.Toplevel(window)
        detect_window.title("Detectar Teclas")
        detect_window.geometry("400x200")
        detect_window.transient(window)
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
            keys_label.config(text=format_hotkey_display("+".join(sorted(self.detected_keys))))
        
        try:
            self._detect_keyboard_hook = keyboard.hook(on_key)
        except Exception as e:
            logging.warning(f"Falha ao iniciar detecção de teclas: {e}")
            self._detect_keyboard_hook = None
        
        # Centraliza
        detect_window.update_idletasks()
        x = window.winfo_x() + (window.winfo_width() // 2) - (detect_window.winfo_width() // 2)
        y = window.winfo_y() + (window.winfo_height() // 2) - (detect_window.winfo_height() // 2)
        detect_window.geometry(f"+{x}+{y}")
    
    def _stop_detecting(self, detect_window: tk.Toplevel, hotkey: Optional[str]) -> None:
        """Para a detecção de teclas"""
        self.is_detecting = False
        
        try:
            import keyboard
            if self._detect_keyboard_hook is not None:
                try:
                    keyboard.unhook(self._detect_keyboard_hook)
                except Exception:
                    pass
            self._detect_keyboard_hook = None
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
        
        # Fecha janela modal
        if self.window:
            self.window.grab_release()
            self.window.destroy()
            self.window = None
    
    def _on_cancel_clicked(self) -> None:
        """Callback do botão Cancelar"""
        if self.window:
            self.window.grab_release()
            self.window.destroy()
            self.window = None
