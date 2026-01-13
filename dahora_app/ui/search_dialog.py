"""
Janela de Busca no Histórico do Dahora App
"""

import hashlib
import logging
import threading
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime
from dahora_app.ui.styles import Windows11Style
from dahora_app.ui.icon_manager import IconManager

# Import opcional de tkinter
try:
    import tkinter as tk
    from tkinter import ttk, font as tkFont

    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class SearchDialog:
    """Janela de busca no histórico do clipboard"""

    def __init__(self, notification_callback: Optional[Callable] = None):
        """
        Inicializa o diálogo de busca

        Args:
            notification_callback: Callback para mostrar notificações
        """
        self.notification_callback = notification_callback
        self.get_history_callback: Optional[Callable] = None
        self.copy_callback: Optional[Callable] = None

    def set_get_history_callback(self, callback: Callable) -> None:
        """Define callback para obter histórico completo"""
        self.get_history_callback = callback

    def set_copy_callback(self, callback: Callable) -> None:
        """Define callback para copiar texto"""
        self.copy_callback = callback

    def show(self) -> None:
        """Mostra o diálogo de busca"""
        logging.info("show_search_dialog() chamada - Iniciando janela de busca")

        if not TKINTER_AVAILABLE:
            logging.error("Tkinter não disponível")
            if self.notification_callback:
                self.notification_callback(
                    "Dahora App", "Tkinter não disponível. Não é possível abrir busca."
                )
            return

        # Executa em thread separada
        thread = threading.Thread(target=self._show_dialog_thread, daemon=True)
        thread.start()
        logging.info("Thread da janela de busca iniciada")

    def _show_dialog_thread(self) -> None:
        """Thread para mostrar o diálogo"""
        try:
            logging.info("Criando janela de busca (Tkinter)")

            # Janela principal
            root = tk.Tk()
            # Configura estilo Windows 11 (Dark Mode)
            Windows11Style.configure_window(
                root, "Dahora App - Buscar no Histórico", "600x500"
            )
            try:
                root.iconbitmap(IconManager.resolve_icon_path())
            except Exception as e:
                logging.warning(f"Não foi possível definir ícone da janela: {e}")
            Windows11Style.configure_styles(root)

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
                    ]
                    for f in preferred_fonts:
                        if f in available_fonts:
                            return f
                    return "TkDefaultFont"
                except Exception:
                    return "TkDefaultFont"

            default_font = get_available_font()

            # Frame principal
            main = ttk.Frame(root, padding=(16, 12, 16, 12), style="Card.TFrame")
            main.pack(fill=tk.BOTH, expand=True)

            # Cabeçalho
            ttk.Label(
                main,
                text="Buscar no Histórico da Área de Transferência",
                font=(default_font, 12, "bold"),
                style="Card.TLabel",
            ).pack(anchor=tk.W, pady=(0, 8))

            # Frame de busca
            search_frame = ttk.Frame(main, style="Card.TFrame")
            search_frame.pack(fill=tk.X, pady=(0, 10))

            ttk.Label(
                search_frame,
                text="Buscar:",
                font=(default_font, 9),
                style="Card.TLabel",
            ).pack(side=tk.LEFT, padx=(0, 8))

            search_var = tk.StringVar()
            search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
            search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
            search_entry.focus_set()

            # Variável para armazenar resultados filtrados
            filtered_results: List[Dict[str, Any]] = []

            def perform_search(*args):
                """Executa a busca"""
                query = search_var.get().lower().strip()

                # Limpa listbox
                results_listbox.delete(0, tk.END)
                filtered_results.clear()

                if not self.get_history_callback:
                    return

                # Obtém histórico completo
                history = self.get_history_callback()

                if not query:
                    # Mostra tudo se query vazia
                    for item in reversed(history):
                        text = item.get("text", "")
                        timestamp = item.get("timestamp", "")

                        # Formata timestamp
                        try:
                            dt = datetime.fromisoformat(timestamp)
                            ts_str = dt.strftime("%d/%m/%Y %H:%M")
                        except:
                            ts_str = "sem data"

                        display = f"[{ts_str}] {text[:80]}..."
                        results_listbox.insert(tk.END, display)
                        filtered_results.append(item)
                else:
                    # Busca por query
                    for item in reversed(history):
                        text = item.get("text", "").lower()
                        if query in text:
                            timestamp = item.get("timestamp", "")

                            # Formata timestamp
                            try:
                                dt = datetime.fromisoformat(timestamp)
                                ts_str = dt.strftime("%d/%m/%Y %H:%M")
                            except:
                                ts_str = "sem data"

                            display = f"[{ts_str}] {item.get('text', '')[:80]}..."
                            results_listbox.insert(tk.END, display)
                            filtered_results.append(item)

                # Atualiza contagem
                count_label.config(
                    text=f"{len(filtered_results)} resultados encontrados"
                )

            # Botão buscar
            search_button = ttk.Button(
                search_frame, text="Buscar", command=perform_search
            )
            search_button.pack(side=tk.LEFT)

            # Bind Enter para buscar
            search_entry.bind("<Return>", perform_search)
            search_entry.bind("<KeyRelease>", perform_search)  # Busca em tempo real

            # Frame de resultados
            results_frame = ttk.LabelFrame(
                main, text="Resultados", padding=(10, 10), style="TLabelframe"
            )
            results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

            # Scrollbar
            scrollbar = ttk.Scrollbar(results_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Listbox de resultados
            results_listbox = tk.Listbox(
                results_frame,
                yscrollcommand=scrollbar.set,
                font=(default_font, 9),
                height=15,
            )
            Windows11Style.configure_listbox(results_listbox)
            results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=results_listbox.yview)

            # Label de contagem
            count_label = ttk.Label(
                main,
                text="0 resultados encontrados",
                font=(default_font, 8),
                foreground="gray",
                style="Card.TLabel",
            )
            count_label.pack(anchor=tk.W, pady=(0, 10))

            # Funções de ação
            def on_copy():
                """Copia o item selecionado"""
                selection = results_listbox.curselection()
                if not selection:
                    if self.notification_callback:
                        self.notification_callback(
                            "Dahora App", "Selecione um item para copiar!"
                        )
                    return

                idx = selection[0]
                if idx < len(filtered_results):
                    item = filtered_results[idx]
                    text = item.get("text", "")

                    if self.copy_callback:
                        self.copy_callback(text)

                    if self.notification_callback:
                        self.notification_callback(
                            "Dahora App", "Copiado para a área de transferência."
                        )

                    text_len = len(text) if text else 0
                    text_hash = (
                        hashlib.sha256(text.encode("utf-8", errors="replace"))
                        .hexdigest()[:12]
                        if text_len
                        else "vazio"
                    )
                    logging.info(
                        f"Item copiado da busca: len={text_len}, sha256={text_hash}"
                    )
                    root.destroy()

            def on_double_click(event):
                """Copia ao dar double-click"""
                on_copy()

            def on_close():
                """Fecha a janela"""
                root.destroy()

            # Bind double-click
            results_listbox.bind("<Double-Button-1>", on_double_click)

            # Botões
            buttons = ttk.Frame(main, style="Card.TFrame")
            buttons.pack(fill=tk.X, pady=(0, 0))
            ttk.Button(buttons, text="Fechar", command=on_close).pack(side=tk.RIGHT)
            ttk.Button(buttons, text="Copiar Selecionado", command=on_copy).pack(
                side=tk.RIGHT, padx=(0, 8)
            )

            # Bind de teclas
            root.bind("<Escape>", lambda e: on_close())
            root.bind("<F5>", perform_search)

            # Centraliza janela
            root.update_idletasks()
            # Centraliza janela
            root.update_idletasks()
            width = root.winfo_width()
            height = root.winfo_height()
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f"{width}x{height}+{x}+{y}")

            # Executa busca inicial (mostra tudo)
            perform_search()

            # Loop
            root.mainloop()
            logging.info("Janela de busca fechada")

        except Exception as e:
            logging.error(f"Erro ao abrir janela de busca: {e}")
            if self.notification_callback:
                self.notification_callback("Dahora App", f"Erro: {e}")
