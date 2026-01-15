"""
Janela de Busca Moderna usando CustomTkinter
"""

import customtkinter as ctk
import threading
import logging
import time
from typing import Optional, Callable, List, Dict, Any, cast
from datetime import datetime
import tkinter as tk

from dahora_app.ui.modern_styles import (
    ModernTheme,
    ModernLabel,
    ModernFrame,
    ModernScrollableFrame,
    ModernEntry,
    ModernButton,
)
from dahora_app.ui.icon_manager import IconManager


class ModernSearchDialog:
    """Janela de busca moderna com CustomTkinter"""

    def __init__(self, notification_callback: Optional[Callable] = None):
        self.notification_callback = notification_callback
        self.get_history_callback: Optional[Callable] = None
        self.copy_callback: Optional[Callable] = None
        self.window: Optional[ctk.CTkToplevel] = None
        self.parent: Optional[ctk.CTk] = None
        self.colors = ModernTheme.get_colors()
        self.filtered_results: List[Dict] = []
        self.selected_index = -1
        self.result_buttons: List[ctk.CTkFrame] = []
        self._results_container: Optional[Any] = None
        self._search_after_id: Optional[str] = None
        self.max_results_render: int = 200

    def set_get_history_callback(self, callback: Callable) -> None:
        self.get_history_callback = callback

    def set_copy_callback(self, callback: Callable) -> None:
        self.copy_callback = callback

    def set_parent(self, parent: ctk.CTk) -> None:
        self.parent = parent

    def show(self) -> None:
        """Mostra o diálogo"""
        start = time.perf_counter()
        if self.window is not None:
            try:
                self.window.deiconify()
            except Exception:
                pass
            t_show = time.perf_counter()
            self._show_window()
            show_ms = (time.perf_counter() - t_show) * 1000
            try:
                self.window.after(0, self._schedule_search)
            except Exception:
                pass
            total_ms = (time.perf_counter() - start) * 1000
            logging.info(
                f"[UI] ModernSearchDialog.show reuse show={show_ms:.1f}ms total={total_ms:.1f}ms"
            )
            return

        try:
            t_create = time.perf_counter()
            self._create_window()
            create_ms = (time.perf_counter() - t_create) * 1000

            t_show = time.perf_counter()
            self._show_window()
            show_ms = (time.perf_counter() - t_show) * 1000
            try:
                if self.window is not None:
                    self.window.after(0, self._schedule_search)
            except Exception:
                pass
            total_ms = (time.perf_counter() - start) * 1000
            logging.info(
                f"[UI] ModernSearchDialog.show create={create_ms:.1f}ms show={show_ms:.1f}ms total={total_ms:.1f}ms"
            )
        except Exception as e:
            logging.error(f"Erro ao abrir busca: {e}")
            if self.notification_callback:
                self.notification_callback("Dahora App", f"Erro: {e}")

    def _create_window(self) -> None:
        """Cria a janela"""
        self.theme = ModernTheme.setup()
        self.colors = ModernTheme.get_colors(self.theme)

        if self.parent is None:
            raise RuntimeError(
                "ModernSearchDialog precisa de parent (CTk root) antes de show()."
            )

        window = ctk.CTkToplevel(self.parent)
        self.window = window
        # Evita renderização progressiva (mostra apenas no final)
        window.withdraw()
        window.title("Dahora App - Buscar no Histórico")
        try:
            window.iconbitmap(IconManager.resolve_icon_path())
        except Exception:
            pass
        window.geometry("650x550")
        window.minsize(500, 400)
        window.configure(fg_color=self.colors["bg"])

        # Dark title bar
        if self.theme == "dark":
            try:
                import ctypes
                from ctypes import windll, c_int, byref, sizeof

                window.update_idletasks()
                hwnd = windll.user32.GetParent(window.winfo_id())
                value = c_int(1)
                windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 20, byref(value), sizeof(value)
                )
            except Exception:
                pass

        # Container sem padding horizontal externo (scrollbar no canto)
        outer = ctk.CTkFrame(window, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=0, pady=0)

        # Top (padded)
        top = ctk.CTkFrame(outer, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(16, 0))

        # Header
        ModernLabel(top, text="🔍 Buscar no Histórico", style="title").pack(
            anchor="w", pady=(0, 12)
        )

        # Campo de busca
        search_frame = ctk.CTkFrame(top, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 12))

        self.search_var = ctk.StringVar()
        self.search_entry = ModernEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Digite para buscar...",
            width=400,
            height=36,
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", lambda e: self._schedule_search())
        self.search_entry.bind("<Return>", lambda e: self._on_copy())
        self.search_entry.focus_set()

        ModernButton(
            search_frame,
            text="Buscar",
            style="primary",
            width=80,
            height=36,
            command=self._perform_search,
        ).pack(side="left")

        # Contador
        self.count_label = ModernLabel(top, text="", style="muted")
        self.count_label.pack(anchor="w", pady=(0, 8))

        # Lista de resultados (sem padding horizontal externo)
        self.results_frame = ModernScrollableFrame(outer)
        self.results_frame.pack(fill="both", expand=True, padx=0, pady=(12, 12))
        # CTkScrollableFrame usa um frame interno para os filhos.
        # Usar esse container evita destruir canvas/scrollbar ao limpar resultados.
        results_container = getattr(self.results_frame, "_scrollable_frame", None)
        if results_container is None:
            results_container = self.results_frame
        self._results_container = results_container

        # Botões (padded)
        buttons = ctk.CTkFrame(outer, fg_color="transparent")
        buttons.pack(fill="x", padx=16, pady=(0, 16))

        ModernButton(
            buttons,
            text="Fechar",
            width=120,
            command=self._on_close,
        ).pack(side="right")
        ModernButton(
            buttons,
            text="Copiar Selecionado",
            style="primary",
            width=160,
            command=self._on_copy,
        ).pack(side="right", padx=(0, 8))

        # Atalhos
        window.bind("<Escape>", lambda e: self._on_close())
        window.protocol("WM_DELETE_WINDOW", self._on_close)

        # Não exibe aqui; show() chama _show_window() depois.

        # Não chama mainloop aqui: o loop Tk roda uma vez no app.

    def _center_window(self) -> None:
        window = self.window
        if window is None:
            return
        window.update_idletasks()
        w = window.winfo_width()
        h = window.winfo_height()
        if w <= 1 or h <= 1:
            try:
                window.after(10, self._center_window)
            except Exception:
                pass
            return
        x = (window.winfo_screenwidth() // 2) - (w // 2)
        y = (window.winfo_screenheight() // 2) - (h // 2)
        window.geometry(f"+{x}+{y}")

    def _show_window(self) -> None:
        window = self.window
        if window is None:
            return

        # Centraliza antes de exibir para evitar "pulo" visual.
        try:
            self._center_window()
        except Exception:
            pass
        try:
            window.deiconify()
        except Exception:
            pass
        try:
            window.after_idle(self._center_window)
        except Exception:
            self._center_window()
        try:
            window.after(60, self._center_window)
        except Exception:
            pass
        window.lift()
        try:
            window.focus_force()
        except Exception:
            pass

        # Garante foco no input de busca após o window manager mapear a janela.
        def _focus_search() -> None:
            try:
                if getattr(self, "search_entry", None) is None:
                    return
                self.search_entry.focus_set()
                try:
                    # Coloca o cursor no fim (útil ao reabrir)
                    self.search_entry.icursor("end")
                except Exception:
                    pass
            except Exception:
                pass

        try:
            window.after_idle(_focus_search)
            window.after(120, _focus_search)
        except Exception:
            _focus_search()

    def _schedule_search(self) -> None:
        window = self.window
        if window is None:
            return
        if self._search_after_id is not None:
            try:
                window.after_cancel(self._search_after_id)
            except Exception:
                pass
            self._search_after_id = None
        try:
            self._search_after_id = window.after(150, self._perform_search)
        except Exception:
            self._perform_search()

    def _perform_search(self) -> None:
        """Executa a busca"""
        query = self.search_var.get().lower().strip()

        # Limpa resultados
        container = self._results_container or getattr(
            self.results_frame, "_scrollable_frame", self.results_frame
        )
        for widget in cast(Any, container).winfo_children():
            widget.destroy()
        self.result_buttons.clear()
        self.filtered_results.clear()
        self.selected_index = -1

        if not self.get_history_callback:
            return

        history = self.get_history_callback()
        total_matches = 0
        rendered = 0

        for item in reversed(history):
            text = item.get("text", "")
            if query and query not in text.lower():
                continue

            total_matches += 1
            if rendered < self.max_results_render:
                self.filtered_results.append(item)
                self._create_result_item(
                    item, len(self.filtered_results) - 1, query=query
                )
                rendered += 1

        # Atualiza contador
        if total_matches == rendered:
            self.count_label.configure(
                text=f"{total_matches} resultado{'s' if total_matches != 1 else ''}"
            )
        else:
            self.count_label.configure(
                text=f"{total_matches} resultados (mostrando {rendered})"
            )

    def _create_result_item(self, item: Dict, index: int, query: str = "") -> None:
        """Cria um item de resultado"""
        is_selected = index == self.selected_index
        bg = self.colors["accent"] if is_selected else self.colors["surface"]

        # Altura maior para permitir prévia em múltiplas linhas
        container = self._results_container or getattr(
            self.results_frame, "_scrollable_frame", self.results_frame
        )
        frame = ctk.CTkFrame(container, fg_color=bg, corner_radius=6, height=92)
        # Recuo interno do conteúdo (mantém scrollbar no canto)
        frame.pack(fill="x", pady=2, padx=12)
        frame.pack_propagate(False)

        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=12, pady=8)

        text = item.get("text", "")
        timestamp = item.get("timestamp", "")

        # Formata timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            ts_str = dt.strftime("%d/%m/%Y %H:%M")
        except:
            ts_str = ""

        text_color = self.colors["text_bright"] if is_selected else self.colors["text"]
        muted_color = self.colors["text"] if is_selected else self.colors["text_muted"]

        # Timestamp
        if ts_str:
            ctk.CTkLabel(
                inner,
                text=ts_str,
                font=("Segoe UI", max(10, ModernTheme.FONT_SIZE_BASE - 2)),
                text_color=muted_color,
                anchor="w",
            ).pack(anchor="w")

        # Texto (prévia em múltiplas linhas). Se houver termo de busca,
        # tenta mostrar um trecho que contenha a primeira ocorrência.
        preview = self._build_preview(text or "", query or "")

        # Para permitir highlight de parte do texto, usa CTkTextbox (tk.Text interno suporta tags).
        preview_box = ctk.CTkTextbox(
            inner,
            height=56,
            wrap="word",
            fg_color="transparent",
            border_width=0,
            font=("Segoe UI", ModernTheme.FONT_SIZE_BASE),
            text_color=text_color,
            scrollbar_button_color=bg,
            scrollbar_button_hover_color=bg,
        )
        preview_box.pack(anchor="w", fill="x")
        try:
            preview_box.insert("1.0", preview)
            preview_box.configure(state="disabled")
            self._highlight_query(preview_box, query)
        except Exception:
            pass

        # Binds
        def on_click(e, idx=index):
            self._select_item(idx)

        def on_double(e, idx=index):
            self._select_item(idx)
            self._on_copy()

        for widget in [frame, inner]:
            widget.bind("<Button-1>", on_click)
            widget.bind("<Double-Button-1>", on_double)
            for child in widget.winfo_children():
                child.bind("<Button-1>", on_click)
                child.bind("<Double-Button-1>", on_double)

        self.result_buttons.append(frame)

    def _build_preview(self, full_text: str, query: str) -> str:
        """Constrói uma prévia curta (até ~3 linhas) preferindo mostrar o termo pesquisado."""
        raw_lines = [ln.rstrip() for ln in (full_text or "").splitlines()]
        while raw_lines and not raw_lines[0].strip():
            raw_lines.pop(0)
        while raw_lines and not raw_lines[-1].strip():
            raw_lines.pop()

        max_lines = 3
        # Base: primeiras linhas
        preview_lines = raw_lines[:max_lines] if raw_lines else [""]
        preview = "\n".join(preview_lines)

        q = (query or "").strip()
        if q:
            # Se o termo não aparece no preview inicial, recorta ao redor da 1ª ocorrência
            if q.lower() not in preview.lower():
                lower_text = (full_text or "").lower()
                pos = lower_text.find(q.lower())
                if pos != -1:
                    # Encontra a linha que contém a ocorrência
                    lines = (full_text or "").splitlines()
                    acc = 0
                    line_index = 0
                    for i, ln in enumerate(lines):
                        # +1 por conta do '\n' entre linhas (aproximação suficiente)
                        next_acc = acc + len(ln) + 1
                        if pos < next_acc:
                            line_index = i
                            break
                        acc = next_acc

                    start = max(0, line_index - 1)
                    end = min(len(lines), line_index + 2)
                    context_lines = [l.rstrip() for l in lines[start:end]]

                    # Se for uma única linha muito longa, corta em torno do match
                    if len(context_lines) == 1:
                        ln = context_lines[0]
                        ln_low = ln.lower()
                        p = ln_low.find(q.lower())
                        if p != -1 and len(ln) > 180:
                            left = max(0, p - 60)
                            right = min(len(ln), p + len(q) + 60)
                            snippet = ln[left:right].rstrip()
                            if left > 0:
                                snippet = "…" + snippet
                            if right < len(ln):
                                snippet = snippet + "…"
                            preview = snippet
                        else:
                            preview = ln
                    else:
                        # Mantém até 3 linhas com a ocorrência dentro
                        trimmed = context_lines[:max_lines]
                        preview = "\n".join(trimmed)

        # Se for uma única linha enorme, limita caracteres
        if "\n" not in preview and len(preview) > 180:
            preview = preview[:180].rstrip() + "…"

        # Se havia mais conteúdo além do que mostramos, adiciona reticências (heurística)
        if (
            raw_lines
            and len(raw_lines) > max_lines
            and preview
            and not preview.endswith("…")
        ):
            preview = preview + "…"

        return preview

    def _highlight_query(self, textbox: ctk.CTkTextbox, query: str) -> None:
        """Destaca o termo pesquisado dentro do textbox (case-insensitive)."""
        q = (query or "").strip()
        if not q:
            return

        # CTkTextbox encapsula um tk.Text interno.
        text_widget = getattr(textbox, "_textbox", None)
        if text_widget is None:
            return

        tag = "dahora_highlight"
        try:
            text_widget.tag_delete(tag)
        except Exception:
            pass
        text_widget.tag_configure(
            tag,
            font=("Segoe UI", ModernTheme.FONT_SIZE_BASE, "bold"),
            foreground=self.colors.get("text_bright", "white"),
        )

        # Procura todas as ocorrências usando o search do tk.Text (nocase).
        start = "1.0"
        while True:
            pos = text_widget.search(q, start, stopindex="end", nocase=1)
            if not pos:
                break
            end = f"{pos}+{len(q)}c"
            text_widget.tag_add(tag, pos, end)
            start = end

    def _select_item(self, index: int) -> None:
        """Seleciona um item"""
        self.selected_index = index
        self._refresh_selection()

    def _refresh_selection(self) -> None:
        """Atualiza visual da seleção"""
        for i, frame in enumerate(self.result_buttons):
            is_selected = i == self.selected_index
            bg = self.colors["accent"] if is_selected else self.colors["surface"]
            frame.configure(fg_color=bg)

    def _on_copy(self) -> None:
        """Copia o item selecionado"""
        if self.selected_index < 0 or self.selected_index >= len(self.filtered_results):
            if self.notification_callback:
                self.notification_callback(
                    "Dahora App", "Selecione um item para copiar!"
                )
            return

        item = self.filtered_results[self.selected_index]
        text = item.get("text", "")

        if self.copy_callback:
            self.copy_callback(text)

        if self.notification_callback:
            self.notification_callback("Dahora App", "Copiado para a área de transferência.")

        self._on_close()

    def _on_close(self) -> None:
        """Fecha"""
        if self.window:
            try:
                self.window.withdraw()
            except Exception:
                try:
                    self.window.destroy()
                except Exception:
                    pass
