#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar o executável Windows do Dahora App
"""

import subprocess
import sys
import os
import time


def ensure_icon_exists(icon_path='icon.ico'):
    # Usa o caminho completo especificado pelo usuário
    full_icon_path = 'E:\\Dahora\\dahora-app\\icon.ico'

    if os.path.exists(full_icon_path):
        print(f">>> Usando ícone existente: {full_icon_path}")
        # Copia para o local esperado pelo PyInstaller
        import shutil
        try:
            shutil.copy2(full_icon_path, icon_path)
            print(f">>> Ícone copiado para: {icon_path}")
        except Exception as e:
            print(f">>> Aviso ao copiar ícone: {e}")
        return
    elif os.path.exists(icon_path):
        print(f">>> Usando ícone existente: {icon_path}")
        return
    print("\n>>> Criando icon.ico...")
    try:
        from create_icon import create_image
        img = create_image()
    except Exception:
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            d.rectangle([6, 8, 58, 56], outline=(255, 152, 0, 255), width=3)
            d.ellipse([28, 26, 32, 30], fill=(255, 152, 0, 255))
            d.ellipse([28, 34, 32, 38], fill=(255, 152, 0, 255))
        except Exception as e:
            print(f">>> Aviso: Nao foi possivel criar icon.ico automaticamente: {e}")
            return
    try:
        img.save(icon_path, format='ICO')
        print(">>> icon.ico criado com sucesso")
    except Exception as e:
        print(f">>> Aviso: Falha ao salvar icon.ico: {e}")


def build_executable():
    """Gera o executável usando PyInstaller"""
    print(">>> Iniciando build do Dahora App...")
    print(">>> Verificando dependências...")

    # Define o nome do executável com versão
    exe_name = 'dahora_app_v0.0.2'

    # Verifica dependências
    try:
        import pystray  # noqa: F401
        import pyperclip  # noqa: F401
        import keyboard  # noqa: F401
        import winotify  # noqa: F401
        from PIL import Image  # noqa: F401
        print(">>> Todas as dependências estão instaladas")
    except ImportError as e:
        print(f"\n❌ Dependência faltando: {e}")
        print("➡️  Execute: pip install -r requirements.txt")
        sys.exit(1)

    # PyInstaller
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("\n>>> PyInstaller nao encontrado. Instalando...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print(">>> PyInstaller instalado com sucesso!")

    print("\n>>> Gerando executavel...")

    # Remove exe antigo se existir
    exe_path = os.path.join('dist', f'{exe_name}.exe')
    if os.path.exists(exe_path):
        print(">>> Executavel antigo encontrado. Tentando remover...")
        try:
            try:
                subprocess.run(["taskkill", "/F", "/IM", f"{exe_name}.exe"], capture_output=True, timeout=2)
                time.sleep(1)
            except Exception:
                pass
            os.remove(exe_path)
            print(">>> Executavel antigo removido com sucesso")
        except PermissionError:
            print(">>> Erro: Nao foi possivel remover o executavel antigo.")
            print(">>> Feche o app se estiver rodando e tente novamente.")
            sys.exit(1)
        except Exception as e:
            print(f">>> Aviso ao remover executavel antigo: {e}")

    ensure_icon_exists('icon.ico')

    console_build = ('--console' in sys.argv) or ('--debug' in sys.argv)
    debug_build = ('--debug' in sys.argv)

    cmd = [
        'pyinstaller',
        '--onefile',
        f'--name={exe_name}',
        '--icon=icon.ico',
        '--add-data=icon.ico;.',
        '--hidden-import=pystray',
        '--hidden-import=pyperclip',
        '--hidden-import=keyboard',
        '--hidden-import=winotify',
        '--hidden-import=win32api',
        '--hidden-import=win32con',
        '--hidden-import=win32event',
        '--hidden-import=tkinter',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageDraw',
        '--hidden-import=PIL.ImageFont',
        '--collect-all=pystray',
        '--collect-all=keyboard',
        '--collect-all=winotify',
        'dahora_app.py'
    ]
    if console_build:
        cmd.append('--console')
    else:
        cmd.append('--windowed')
    if debug_build:
        cmd += ['--debug', 'all']

    try:
        subprocess.run(cmd, check=True)
        print("\n>>> Build concluido com sucesso!")
        print(f">>> Executavel: dist/{exe_name}.exe")
    except subprocess.CalledProcessError as e:
        print(f"\n>>> Erro ao gerar executavel: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n>>> PyInstaller nao encontrado! Execute: pip install pyinstaller")
        sys.exit(1)


if __name__ == '__main__':
    build_executable()

