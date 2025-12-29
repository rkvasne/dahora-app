#!/usr/bin/env python3
"""
Script de teste para verificar se o diálogo de edição de atalhos funciona
"""
import sys
import os
import tkinter as tk
from tkinter import ttk
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Adicionar o diretório dahora_app ao path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from dahora_app.ui.shortcut_editor import ShortcutEditorDialog
    from dahora_app.ui.styles import Windows11Style
    print("✓ Imports realizados com sucesso")
except ImportError as e:
    print(f"✗ Erro no import: {e}")
    sys.exit(1)

def test_shortcut_editor():
    """Testa o diálogo de edição de atalhos"""
    
    def on_save(shortcut_data):
        print(f"✓ Atalho salvo: {shortcut_data}")
        root.quit()
    
    def on_validate_hotkey(hotkey, exclude_id=None):
        print(f"✓ Validando hotkey: {hotkey}")
        return True, "Válido"
    
    # Criar janela principal
    root = tk.Tk()
    Windows11Style.configure_window(root, "Teste - Dahora App", "400x300")
    Windows11Style.configure_styles(root)
    
    print("✓ Janela principal criada")
    
    # Função para abrir o editor
    def abrir_editor():
        print(">>> Abrindo editor de atalho...")
        try:
            editor = ShortcutEditorDialog(
                parent=root,
                shortcut=None,  # Novo atalho
                on_save=on_save,
                on_validate_hotkey=on_validate_hotkey
            )
            print(">>> Editor criado, chamando show()...")
            editor.show()
            print(">>> Editor.show() executado")
        except Exception as e:
            print(f"✗ Erro ao abrir editor: {e}")
            import traceback
            traceback.print_exc()
    
    # Botão para testar
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(frame, text="Teste do Diálogo de Edição de Atalhos", 
              font=("Segoe UI", 12, "bold")).pack(pady=10)
    
    ttk.Button(frame, text="Abrir Editor de Atalho", 
               command=abrir_editor, width=25).pack(pady=20)
    
    ttk.Label(frame, text="Clique no botão acima para testar\nse o diálogo abre corretamente", 
              font=("Segoe UI", 9)).pack(pady=10)
    
    print("✓ Interface criada")
    print(">>> Iniciando aplicação de teste...")
    
    # Centralizar janela
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()
    print(">>> Teste finalizado")

if __name__ == "__main__":
    print("=== Teste do Diálogo de Edição de Atalhos ===")
    test_shortcut_editor()