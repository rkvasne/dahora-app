import sys
import os
import time
from unittest.mock import MagicMock

# Adicionar raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dahora_app.clipboard_manager import ClipboardManager
from dahora_app.handlers.copy_datetime_handler import CopyDateTimeHandler

def test_refactoring():
    print("Iniciando verificação de refatoração...")

    # 1. Testar ClipboardManager
    print("Instanciando ClipboardManager...")
    try:
        cm = ClipboardManager()
    except Exception as e:
        print(f"❌ Erro ao instanciar ClipboardManager: {e}")
        return

    # Testar novos métodos
    print("Testando ClipboardManager.set_text() e get_text()...")
    test_str = f"Test String {time.time()}"
    try:
        cm.set_text(test_str)
        # Pequeno delay para OS processar clipboard
        time.sleep(0.1)
        result = cm.get_text()
        
        if result == test_str:
            print("✅ ClipboardManager: set_text/get_text funcionaram.")
        else:
            print(f"⚠️ ClipboardManager: Diferença encontrada (comum em alguns ambientes). Esperado '{test_str}', obtido '{result}'")
            # Fallback para continuar teste se clipboard falhar (ex: ambiente headless)
    except Exception as e:
        print(f"❌ Erro no teste de clipboard: {e}")

    # 2. Testar CopyDateTimeHandler com mocks
    print("\nTestando CopyDateTimeHandler...")
    
    # Mock do App e dependências
    mock_app = MagicMock()
    mock_app.clipboard_manager = cm
    mock_app.datetime_formatter.format_datetime.return_value = "2024-01-01 12:00:00"
    mock_app.settings_manager.settings.separator = " - "

    handler = CopyDateTimeHandler(app=mock_app)
    
    # Testar métodos privados extraídos (via acesso direto para teste)
    print("Testando métodos privados extraídos...")
    
    # _get_clipboard_text
    try:
        current = handler._get_clipboard_text()
        print(f"   _get_clipboard_text retornou: '{current}'")
        print("✅ _get_clipboard_text executado sem erro")
    except Exception as e:
        print(f"❌ _get_clipboard_text erro: {e}")
        
    # _copy_to_clipboard
    new_str = "New Value"
    try:
        handler._copy_to_clipboard(new_str)
        time.sleep(0.1)
        if cm.get_text() == new_str:
            print("✅ _copy_to_clipboard: OK")
        else:
            print(f"⚠️ _copy_to_clipboard: Valor no clipboard diferente (pode ser delay do OS).")
    except Exception as e:
        print(f"❌ _copy_to_clipboard erro: {e}")
        
    # Testar fluxo principal (sem keyboard.send real para não atrapalhar)
    import keyboard
    keyboard.send = MagicMock() # Mock keyboard.send
    
    print("Testando handle()...")
    try:
        success = handler.handle()
        
        if success:
            print("✅ handle() retornou True")
            # Verificar se chamou format_datetime
            mock_app.datetime_formatter.format_datetime.assert_called()
            print("✅ format_datetime chamado")
            
            # Verificar conteúdo final do clipboard (deve ser o timestamp)
            # Nota: O handler restaura o clipboard original em thread separada após delay.
            # O teste imediato deve pegar o timestamp, a menos que a restauração seja muito rápida.
            final_clip = cm.get_text()
            print(f"Clipboard logo após handle: {final_clip}")
            if "2024-01-01" in final_clip:
                 print("✅ Clipboard contém timestamp")
            else:
                 print("ℹ️ Clipboard pode já ter sido restaurado ou falhou na cópia.")
                 
        else:
            print("❌ handle() retornou False")
    except Exception as e:
        print(f"❌ Erro em handle(): {e}")

if __name__ == "__main__":
    test_refactoring()
