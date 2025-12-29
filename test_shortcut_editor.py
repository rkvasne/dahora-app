#!/usr/bin/env python3
"""
Teste simples para verificar se o ShortcutEditorDialog abre corretamente
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox

# Adiciona o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_shortcut_editor():
    """Testa se o ShortcutEditorDialog pode ser aberto"""
    try:
        print("Importando módulos...")
        from dahora_app.ui.styles import Windows11Style
        from dahora_app.ui.shortcut_editor import ShortcutEditorDialog
        print("✓ Imports OK")
        
        print("Criando janela principal...")
        root = tk.Tk()
        Windows11Style.configure_window(root, "Teste Editor", "400x300")
        Windows11Style.configure_styles(root)
        print("✓ Janela principal OK")
        
        # Frame principal
        main_frame = Windows11Style.create_modern_card(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = Windows11Style.create_section_header(main_frame, "🧪 Teste do Editor de Atalhos")
        title.pack(anchor="w", pady=(0, 20))
        
        # Botão para testar
        def test_editor():
            try:
                print("Criando ShortcutEditorDialog...")
                
                def on_save(data):
                    print(f"Dados salvos: {data}")
                    messagebox.showinfo("Sucesso", f"Atalho salvo:\n{data}")
                
                def validate_hotkey(hotkey, exclude_id=None):
                    if not hotkey or len(hotkey) < 3:
                        return False, "Atalho muito curto"
                    return True, "OK"
                
                # Dados de exemplo para edição
                sample_data = {
                    "id": 1,
                    "hotkey": "ctrl+shift+1",
                    "prefix": "dahora",
                    "description": "Teste",
                    "enabled": True
                }
                
                editor = ShortcutEditorDialog(
                    parent=root,
                    shortcut=sample_data,
                    on_save=on_save,
                    on_validate_hotkey=validate_hotkey
                )
                
                print("Chamando editor.show()...")
                editor.show()
                print("✓ Editor aberto com sucesso!")
                
            except Exception as e:
                print(f"✗ Erro ao abrir editor: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("Erro", f"Erro ao abrir editor:\n{str(e)}")
        
        test_btn = Windows11Style.create_modern_button(
            main_frame, 
            "🚀 Testar Editor de Atalhos", 
            command=test_editor,
            style="Primary.TButton"
        )
        test_btn.pack(pady=10)
        
        # Informações
        info_text = (
            "Este teste verifica se o ShortcutEditorDialog\n"
            "pode ser aberto corretamente com a nova\n"
            "interface modernizada."
        )
        info_label = tk.Label(main_frame, text=info_text, 
                             font=("Segoe UI", 9),
                             bg=Windows11Style.COLORS['bg'],
                             fg=Windows11Style.COLORS['text_muted'])
        info_label.pack(pady=(20, 0))
        
        print("Iniciando interface...")
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_shortcut_editor()