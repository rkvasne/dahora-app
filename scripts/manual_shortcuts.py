#!/usr/bin/env python3
"""
Script de teste para verificar se os atalhos estão funcionando
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dahora_app.settings import SettingsManager

def test_shortcuts():
    """Testa o sistema de atalhos"""
    print("=== Teste do Sistema de Atalhos ===")
    
    # Cria settings manager
    settings = SettingsManager()
    settings.load()
    
    print(f"Atalhos atuais: {len(settings.custom_shortcuts)}")
    
    for shortcut in settings.custom_shortcuts:
        print(f"  ID: {shortcut['id']}")
        print(f"  Hotkey: {shortcut['hotkey']}")
        print(f"  Prefix: {shortcut['prefix']}")
        print(f"  Enabled: {shortcut['enabled']}")
        print(f"  Description: {shortcut.get('description', '')}")
        print("  ---")
    
    # Testa adicionar um atalho
    print("\n=== Testando Adicionar Atalho ===")
    success, msg, new_id = settings.add_custom_shortcut(
        hotkey="ctrl+shift+t",
        prefix="teste",
        description="Atalho de teste",
        enabled=True
    )
    
    print(f"Resultado: {success}")
    print(f"Mensagem: {msg}")
    print(f"Novo ID: {new_id}")
    
    if success:
        print("\n=== Atalhos após adicionar ===")
        for shortcut in settings.custom_shortcuts:
            print(f"  {shortcut['hotkey']} → {shortcut['prefix']}")
        
        # Remove o atalho de teste
        print("\n=== Removendo atalho de teste ===")
        success, msg = settings.remove_custom_shortcut(new_id)
        print(f"Remoção: {success} - {msg}")

if __name__ == "__main__":
    test_shortcuts()
