#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dahora App - Arquivo Principal
Sistema de Bandeja do Windows para copiar data/hora formatada
"""
import sys
import os
import logging
from typing import Any, cast

# HACK: Forçar Dark Mode em menus nativos do Windows (Bandeja/Pystray)
# Isso usa APIs não documentadas do Windows para garantir que o menu de contexto
# siga o tema escuro, mesmo se o app não tiver manifesto.
# DEVE SER EXECUTADO ANTES DE QUALQUER OUTRA COISA DE UI
try:
    import ctypes
    uxtheme = cast(Any, ctypes.windll.uxtheme)
    
    # Tenta SetPreferredAppMode (Ordinal 135) - Win 10 1903+ / Win 11
    # 2 = Force Dark Mode
    try:
        uxtheme[135](2)
    except:
        # Fallback: Tenta AllowDarkModeForApp (Ordinal 132) - Win 10 1809
        try:
            uxtheme[132](True)
        except:
            pass
except Exception:
    pass

# Configuração de encoding do console
try:
    import ctypes
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    ctypes.windll.kernel32.SetConsoleCP(65001)
except Exception:
    pass

try:
    if sys.stdout is not None:
        cast(Any, sys.stdout).reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr is not None:
        cast(Any, sys.stderr).reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from dahora_app.constants import (
    APP_TITLE,
    LOG_FILE,
    LOG_MAX_BYTES,
    LOG_BACKUP_COUNT,
)

# Imports para verificação de instância única
# Movido para dahora_app/single_instance.py

file_handler = None
try:
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler(
        LOG_FILE,
        mode="a",
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, logging.StreamHandler(sys.stdout)])
    logging.info(
        f"Sistema de rotação de logs ativado ({LOG_MAX_BYTES/1024/1024}MB, {LOG_BACKUP_COUNT} backups)"
    )
except Exception as e:
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])
    logging.warning(f"Falha ao configurar rotação de logs: {e}")

# Variáveis globais


def main():
    """Função principal"""
    # Verifica se icon.ico existe
    if not os.path.exists('icon.ico'):
        print("[AVISO] Arquivo icon.ico não encontrado. O app usará ícone padrão.")
    
    # Cria e executa aplicação
    from dahora_app.app import DahoraApp

    app = DahoraApp(file_handler=file_handler)
    app.run()


if __name__ == '__main__':
    main()
