#!/usr/bin/env python3
"""
Test script para verificar a modernização da UI
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# Adiciona o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dahora_app.ui.styles import Windows11Style
    from dahora_app.ui.custom_shortcuts_dialog import CustomShortcutsDialog
    from dahora_app.ui.shortcut_editor import ShortcutEditorDialog
    print("✓ Imports realizados com sucesso")
except ImportError as e:
    print(f"✗ Erro no import: {e}")
    sys.exit(1)

def test_windows11_style():
    """Testa o Windows11Style"""
    print("\n=== Testando Windows11Style ===")
    
    # Testa detecção de tema
    theme = Windows11Style.get_system_theme()
    print(f"Tema do sistema detectado: {theme}")
    
    # Testa cores
    print(f"Cores carregadas: {len(Windows11Style.COLORS)} cores")
    print(f"Background: {Windows11Style.COLORS['bg']}")
    print(f"Accent: {Windows11Style.COLORS['accent']}")
    
    # Testa fontes
    print(f"Fontes disponíveis: {len(Windows11Style.FONTS)}")
    print(f"Fonte padrão: {Windows11Style.FONTS['default']}")
    
    print("✓ Windows11Style OK")

def test_modern_dialog():
    """Testa o dialog modernizado"""
    print("\n=== Testando Dialog Modernizado ===")
    
    try:
        # Cria janela de teste
        root = tk.Tk()
        Windows11Style.configure_window(root, "Teste de Modernização", "800x600")
        Windows11Style.configure_styles(root)
        
        # Cria frame principal
        main_frame = Windows11Style.create_modern_card(root, padding=24)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title = Windows11Style.create_section_header(main_frame, "🎯 Interface Modernizada")
        title.pack(anchor="w", pady=(0, 20))
        
        # Card de exemplo
        card = Windows11Style.create_modern_card(main_frame, padding=20)
        card.pack(fill=tk.X, pady=(0, 16))
        
        ttk.Label(card, text="Exemplo de Card Moderno", style="CardHeading.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(card, text="Este é um exemplo de como a interface ficou moderna com:", style="Card.TLabel").pack(anchor="w", pady=(0, 8))
        
        features_text = (
            "✅ Bordas arredondadas\n"
            "✅ Cores modernas (tema automático)\n"
            "✅ Espaçamento generoso\n"
            "✅ Tipografia melhorada\n"
            "✅ Componentes elevados (cards)\n"
            "✅ Botões modernos\n"
            "✅ Tabs redesenhadas"
        )
        ttk.Label(card, text=features_text, style="Card.TLabel").pack(anchor="w")
        
        # Botões de exemplo
        buttons_frame = ttk.Frame(main_frame, style="TFrame")
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botão primário
        primary_btn = Windows11Style.create_modern_button(buttons_frame, "Botão Primário", 
                                                         style="Primary.TButton")
        primary_btn.pack(side=tk.LEFT, padx=(0, 12))
        
        # Botão secundário
        secondary_btn = Windows11Style.create_modern_button(buttons_frame, "Botão Secundário")
        secondary_btn.pack(side=tk.LEFT, padx=(0, 12))
        
        # Botão de sucesso
        success_btn = Windows11Style.create_modern_button(buttons_frame, "Sucesso", 
                                                         style="Success.TButton")
        success_btn.pack(side=tk.LEFT, padx=(0, 12))
        
        # Botão de perigo
        danger_btn = Windows11Style.create_modern_button(buttons_frame, "Perigo", 
                                                        style="Danger.TButton")
        danger_btn.pack(side=tk.LEFT)
        
        # Botão para testar dialog de atalhos
        test_dialog_btn = Windows11Style.create_modern_button(buttons_frame, "Testar Dialog de Atalhos", 
                                                             command=lambda: test_shortcuts_dialog(root))
        test_dialog_btn.pack(side=tk.RIGHT)
        
        print("✓ Interface moderna criada com sucesso")
        
        # Centraliza janela
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Mostra janela
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Erro ao criar interface: {e}")
        import traceback
        traceback.print_exc()

def test_shortcuts_dialog(parent):
    """Testa o dialog de atalhos"""
    try:
        print("\n=== Testando Dialog de Atalhos ===")
        
        # Dados de exemplo
        sample_shortcuts = [
            {
                "id": 1,
                "hotkey": "ctrl+shift+1",
                "prefix": "dahora",
                "description": "Prefixo principal",
                "enabled": True
            },
            {
                "id": 2,
                "hotkey": "ctrl+shift+2", 
                "prefix": "meeting",
                "description": "Para reuniões",
                "enabled": True
            },
            {
                "id": 3,
                "hotkey": "ctrl+shift+3",
                "prefix": "task",
                "description": "Para tarefas",
                "enabled": False
            }
        ]
        
        sample_settings = {
            "custom_shortcuts": sample_shortcuts,
            "datetime_format": "%d.%m.%Y-%H:%M",
            "bracket_open": "[",
            "bracket_close": "]",
            "max_history_items": 100,
            "clipboard_monitor_interval": 3.0,
            "clipboard_idle_threshold": 30.0,
            "notification_enabled": True,
            "notification_duration": 2,
            "hotkey_search_history": "ctrl+shift+f",
            "hotkey_refresh_menu": "ctrl+shift+r"
        }
        
        # Cria dialog
        dialog = CustomShortcutsDialog()
        dialog.set_current_settings(sample_settings)
        
        # Define callbacks de exemplo
        def on_save(settings):
            print(f"Configurações salvas: {settings}")
        
        def on_add(hotkey, prefix, description, enabled):
            print(f"Adicionando: {hotkey} -> {prefix}")
            return True, "Sucesso", len(sample_shortcuts) + 1
        
        def on_update(shortcut_id, **kwargs):
            print(f"Atualizando ID {shortcut_id}: {kwargs}")
            return True, "Sucesso"
        
        def on_remove(shortcut_id):
            print(f"Removendo ID {shortcut_id}")
            return True, "Sucesso"
        
        def validate_hotkey(hotkey, exclude_id=None):
            if not hotkey or len(hotkey) < 3:
                return False, "Atalho muito curto"
            return True, "OK"
        
        dialog.set_on_save_callback(on_save)
        dialog.set_on_add_callback(on_add)
        dialog.set_on_update_callback(on_update)
        dialog.set_on_remove_callback(on_remove)
        dialog.set_on_validate_hotkey_callback(validate_hotkey)
        dialog.notification_callback = lambda title, msg: print(f"Notificação: {title} - {msg}")
        
        # Mostra dialog
        dialog.show()
        
        print("✓ Dialog de atalhos testado")
        
    except Exception as e:
        print(f"✗ Erro ao testar dialog: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Função principal de teste"""
    print("🚀 Testando Modernização da UI do Dahora App")
    print("=" * 50)
    
    # Testa componentes
    test_windows11_style()
    
    # Testa interface
    test_modern_dialog()

if __name__ == "__main__":
    main()
