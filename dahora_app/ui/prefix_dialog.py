"""
Diálogo de configuração de prefixo
"""

import logging
import threading
from datetime import datetime
from typing import Optional, Callable

# Import opcional de tkinter
try:
    import tkinter as tk
    from tkinter import ttk, font as tkFont

    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class PrefixDialog:
    """Diálogo para configuração de prefixo"""

    def __init__(self, notification_callback: Optional[Callable] = None):
        """
        Inicializa o diálogo de prefixo

        Args:
            notification_callback: Callback para mostrar notificações
        """
        self.notification_callback = notification_callback
        self.current_prefix = ""
        self.on_save_callback: Optional[Callable] = None

    def set_prefix(self, prefix: str) -> None:
        """Define o prefixo atual"""
        self.current_prefix = prefix

    def set_on_save_callback(self, callback: Callable) -> None:
        """Define callback para quando salvar"""
        self.on_save_callback = callback

    def show(self) -> None:
        """Mostra o diálogo de prefixo"""
        logging.info("show_prefix_dialog() chamada - Iniciando janela de prefixo")

        if not TKINTER_AVAILABLE:
            logging.error("Tkinter não disponível")
            if self.notification_callback:
                self.notification_callback(
                    "Dahora App",
                    "Tkinter não disponível. Não é possível definir prefixo.",
                )
            return

        # Executa em thread separada
        thread = threading.Thread(target=self._show_dialog_thread, daemon=True)
        thread.start()
        logging.info("Thread da janela de prefixo iniciada")

    def _show_dialog_thread(self) -> None:
        """Thread para mostrar o diálogo"""
        try:
            logging.info(
                "Criando janela Tkinter (estilo Windows 11) em thread separada"
            )

            # Janela principal
            root = tk.Tk()
            root.title("Dahora App - Definir Prefixo")
            root.resizable(False, False)
            root.focus_force()

            # Tema moderno
            try:
                style = ttk.Style()
                style.theme_use("vista")
            except Exception:
                style = ttk.Style()

            # Fonte preferida
            def get_available_font():
                try:
                    available_fonts = tkFont.families()
                    preferred_fonts = [
                        "Segoe UI",
                        "Segoe UI Variable",
                        "Arial",
                        "Tahoma",
                        "Microsoft Sans Serif",
                        "Verdana",
                    ]
                    for f in preferred_fonts:
                        if f in available_fonts:
                            return f
                    return "TkDefaultFont"
                except Exception:
                    return "TkDefaultFont"

            default_font = get_available_font()
            logging.info(f"Usando fonte: {default_font}")

            # Conteúdo
            main = ttk.Frame(root, padding=(20, 16, 20, 16))
            main.pack(fill=tk.BOTH, expand=True)

            # Cabeçalho
            ttk.Label(
                main, text="Prefixo de data/hora", font=(default_font, 11, "bold")
            ).pack(anchor=tk.W, pady=(0, 2))

            ttk.Label(
                main,
                text="Digite um prefixo para personalizar a cópia de data/hora.",
                font=(default_font, 9),
            ).pack(anchor=tk.W, pady=(2, 12))

            # Campo de entrada
            var = tk.StringVar(value=self.current_prefix)
            ttk.Label(main, text="Prefixo", font=(default_font, 9)).pack(anchor=tk.W)
            entry = ttk.Entry(main, textvariable=var, width=36)
            entry.pack(fill=tk.X, pady=(6, 10))
            entry.focus()
            entry.select_range(0, tk.END)

            # Exemplo dinâmico
            example_label = ttk.Label(main, font=(default_font, 8))
            example_label.pack(anchor=tk.W)

            def render_example():
                base = datetime.now().strftime("%d.%m.%Y-%H:%M")
                p = var.get().strip()
                prefix_part = f"{p}-" if p else ""
                example_label.configure(text=f"Exemplo: [{prefix_part}{base}]")

            render_example()
            try:
                var.trace_add("write", lambda *args: render_example())
            except Exception:
                pass

            # Ações
            def on_ok():
                new_prefix = var.get().strip()
                if self.on_save_callback:
                    self.on_save_callback(new_prefix)
                if self.notification_callback:
                    self.notification_callback(
                        "Dahora App", f"Prefixo atualizado!\n{new_prefix or '(vazio)'}"
                    )
                logging.info(f"Prefixo atualizado para: {new_prefix}")
                root.destroy()

            def on_cancel():
                root.destroy()

            # Botões
            buttons = ttk.Frame(main)
            buttons.pack(fill=tk.X, pady=(16, 0))
            ttk.Button(buttons, text="Salvar", command=on_ok).pack(side=tk.RIGHT)
            ttk.Button(buttons, text="Cancelar", command=on_cancel).pack(
                side=tk.RIGHT, padx=(8, 0)
            )

            # Bind de teclas
            root.bind("<Return>", lambda e: on_ok())
            root.bind("<Escape>", lambda e: on_cancel())

            # Centraliza janela
            root.update_idletasks()
            width = max(420, root.winfo_width())
            height = max(200, root.winfo_height())
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f"{width}x{height}+{x}+{y}")

            # Loop
            root.mainloop()
            logging.info("Janela de prefixo fechada")

        except Exception as e:
            logging.error(f"Erro ao abrir janela de prefixo: {e}")
            if self.notification_callback:
                self.notification_callback("Dahora App", f"Erro: {e}")
