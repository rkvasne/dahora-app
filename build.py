#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar o executável Windows do Dahora App
"""

import subprocess
import sys
import os
import time

def build_executable():
    """Gera o executável usando PyInstaller"""
    print("🚀 Iniciando build do Dahora App...")
    print("📦 Verificando dependências...")
    
    # Verifica se as dependências estão instaladas
    try:
        import pystray
        import pyperclip
        import keyboard
        import winotify
        from PIL import Image
        print("✅ Todas as dependências estão instaladas")
    except ImportError as e:
        print(f"\n❌ Dependência faltando: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("\n⚠️  PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("✅ PyInstaller instalado com sucesso!")
    
    print("\n🔨 Gerando executável...")
    
    # Tenta remover o executável antigo se existir
    exe_path = os.path.join("dist", "dahora_app.exe")
    if os.path.exists(exe_path):
        print("⚠️  Executável antigo encontrado. Tentando remover...")
        try:
            # Tenta fechar o processo se estiver rodando
            try:
                import subprocess
                subprocess.run(["taskkill", "/F", "/IM", "dahora_app.exe"], 
                             capture_output=True, timeout=2)
                time.sleep(1)  # Aguarda um pouco
            except:
                pass
            
            # Tenta remover o arquivo
            os.remove(exe_path)
            print("✅ Executável antigo removido com sucesso")
        except PermissionError:
            print("❌ Erro: Não foi possível remover o executável antigo.")
            print("💡 Certifique-se de que o aplicativo não está rodando e tente novamente.")
            print("💡 Ou feche manualmente o processo 'dahora_app.exe' no Gerenciador de Tarefas.")
            sys.exit(1)
        except Exception as e:
            print(f"⚠️  Aviso ao remover executável antigo: {e}")
    
    # Comando PyInstaller com todas as dependências incluídas
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=dahora_app',
        '--hidden-import=pystray',
        '--hidden-import=pyperclip',
        '--hidden-import=keyboard',
        '--hidden-import=winotify',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageDraw',
        '--hidden-import=PIL.ImageFont',
        '--collect-all=pystray',
        '--collect-all=PIL',
        '--collect-all=keyboard',
        'dahora_app.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Build concluído com sucesso!")
        print("📦 Executável criado em: dist/dahora_app.exe")
        print("\n💡 Você pode mover o arquivo .exe para qualquer lugar e executá-lo!")
        print("💡 Não precisa mais do Python instalado para usar o .exe!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao gerar executável: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ PyInstaller não encontrado!")
        print("💡 Execute: pip install pyinstaller")
        sys.exit(1)

if __name__ == '__main__':
    build_executable()

