#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar o executável Windows do Dahora App
"""

import subprocess
import sys
import os
import time


def _create_release_zip(exe_name: str) -> str | None:
    """Cria um ZIP somente com o artefato final em dist/.

    - Se existir dist/<exe_name>.exe (onefile), zipa apenas o .exe.
    - Se existir dist/<exe_name>/ (onedir), zipa a pasta inteira.
    """
    from pathlib import Path
    import zipfile

    dist_dir = Path('dist')
    exe_path = dist_dir / f'{exe_name}.exe'
    onedir_path = dist_dir / exe_name
    zip_path = dist_dir / f'{exe_name}.zip'

    if zip_path.exists():
        zip_path.unlink()

    if exe_path.exists():
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(exe_path, arcname=exe_path.name)
        return str(zip_path)

    if onedir_path.exists() and onedir_path.is_dir():
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for file_path in onedir_path.rglob('*'):
                if file_path.is_dir():
                    continue
                arcname = str(file_path.relative_to(dist_dir))
                zf.write(file_path, arcname=arcname)
        return str(zip_path)

    return None


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

    # Define o nome do executável com versão (fonte da verdade: constants.APP_VERSION)
    try:
        from dahora_app.constants import APP_VERSION
        exe_name = f"DahoraApp_v{APP_VERSION}"
    except Exception:
        exe_name = 'DahoraApp_v0.2.3'

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

    # Verifica se icon.ico existe
    if not os.path.exists('icon.ico'):
        print(">>> ERRO: icon.ico não encontrado!")
        print(">>> Build cancelado. Certifique-se de que icon.ico existe.")
        return

    console_build = ('--console' in sys.argv) or ('--debug' in sys.argv)
    debug_build = ('--debug' in sys.argv)

    cmd = [
        'pyinstaller',
        '--onefile',
        f'--name={exe_name}',
        '--icon=icon.ico',
        '--add-data=icon.ico;.',
        '--add-data=icon_paused.ico;.',
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
        '--hidden-import=dahora_app',
        '--hidden-import=dahora_app.ui',
        '--manifest=manifest.xml',
        'main.py'
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

        if '--no-zip' not in sys.argv:
            zip_created = _create_release_zip(exe_name)
            if zip_created:
                print(f">>> ZIP gerado: {zip_created}")
            else:
                print(">>> Aviso: Não foi possível gerar ZIP (artefato não encontrado em dist/)")
    except subprocess.CalledProcessError as e:
        print(f"\n>>> Erro ao gerar executavel: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n>>> PyInstaller nao encontrado! Execute: pip install pyinstaller")
        sys.exit(1)


if __name__ == '__main__':
    build_executable()

