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
        # Se o arquivo local já existe e for igual, não copia
        if os.path.exists(icon_path):
            try:
                if os.path.getsize(full_icon_path) == os.path.getsize(icon_path):
                    print(f">>> Ícone já está atualizado: {icon_path}")
                    return
            except:
                pass

        # Copia para o local esperado pelo PyInstaller
        import shutil
        try:
            # Tenta forçar a cópia, mesmo se o arquivo estiver sendo usado
            shutil.copy2(full_icon_path, icon_path)
            print(f">>> Ícone copiado para: {icon_path}")
        except Exception as e:
            print(f">>> Aviso ao copiar ícone: {e}")
            print(">>> Tentando usar arquivo diretamente...")
            # Se não conseguir copiar, usa o arquivo direto do caminho completo
            try:
                import subprocess
                subprocess.run(['cmd', '/c', 'copy', '/y', full_icon_path, icon_path],
                             check=False, capture_output=True)
                print(f">>> Ícone copiado via cmd: {icon_path}")
            except Exception as e2:
                print(f">>> Falha na cópia via cmd: {e2}")
                print(">>> Build usará ícone do diretório original")
                # Se não conseguir copiar, modifica o comando do PyInstaller para usar caminho completo
                global exe_name
                exe_name = f'dahora_app_v0.0.2_custom_icon'
                return
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

    # LIMPEZA COMPLETA DO CACHE - Força uso do ícone correto
    print(">>> Limpando cache do PyInstaller...")
    import shutil

    if os.path.exists('build'):
        try:
            shutil.rmtree('build')
            print(">>> Cache build removido")
        except Exception as e:
            print(f">>> Aviso: Não foi possível remover cache build: {e}")

    if os.path.exists('dist'):
        try:
            shutil.rmtree('dist')
            print(">>> Cache dist removido")
        except Exception as e:
            print(f">>> Aviso: Não foi possível remover cache dist: {e}")
            # Tenta remover arquivos individualmente se o diretório estiver em uso
            try:
                subprocess.run(['cmd', '/c', 'rd /s /q dist'], check=False, capture_output=True)
                print(">>> Cache dist removido com cmd")
            except Exception:
                print(">>> Continuando sem limpar cache dist")

    # Garante que está usando o ícone correto
    if os.path.exists('icone.ico'):
        if os.path.exists('icon.ico'):
            os.remove('icon.ico')
        shutil.copy2('icone.ico', 'icon.ico')
        print(">>> Ícone correto icone.ico copiado para icon.ico")

    # Limpa cache de ícones do Windows
    try:
        import subprocess
        print(">>> Limpando cache de ícones do Windows...")
        subprocess.run(['ie4uinit.exe', '-show'], capture_output=True, timeout=5)
        print(">>> Cache de ícones do Windows limpo")
    except Exception as e:
        print(f">>> Aviso: Não foi possível limpar cache de ícones: {e}")

    # Remove arquivos temporários de ícones
    icon_temp_files = ['IconCache.db', 'thumbcache.db']
    for temp_file in icon_temp_files:
        try:
            import glob
            for cache_file in glob.glob(f"**/{temp_file}", recursive=True):
                try:
                    os.remove(cache_file)
                    print(f">>> Arquivo de cache removido: {cache_file}")
                except Exception:
                    pass
        except Exception:
            pass

    # Define o nome do executável com versão
    exe_name = 'dahora_app_v0.0.7'

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

