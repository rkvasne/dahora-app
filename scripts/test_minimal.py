#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Versão minimalista de teste para isolar problemas
"""

import logging
import sys
import time

# Configura logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    datefmt='%H:%M:%S'
)

def main():
    """Função principal minimalista"""
    print("=== VERSÃO MINIMALISTA DE TESTE ===")
    logging.info("Iniciando versão minimalista")

    try:
        # Teste 1: Importações
        print("1. Testando importações...")
        import pystray
        import pyperclip
        from PIL import Image
        print("   [OK] Importacoes OK")

        # Teste 2: Criação de ícone simples
        print("2. Criando ícone simples...")
        img = Image.new('RGB', (64, 64), color='orange')
        icon = pystray.Icon("Test", img, "Test App")
        print("   ✅ Ícone criado")

        # Teste 3: Menu simples
        print("3. Criando menu simples...")
        menu = pystray.Menu(
            pystray.MenuItem("Teste", lambda: print("Menu clicado!")),
            pystray.MenuItem("Sair", lambda icon, item: icon.stop())
        )
        icon.menu = menu
        print("   ✅ Menu criado")

        print("4. Iniciando ícone (clique Ctrl+C para parar)...")
        logging.info("Iniciando ícone minimalista")
        icon.run()

    except KeyboardInterrupt:
        print("\n[INFO] Interrompido pelo usuario")
        logging.info("Interrompido pelo usuário")
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()
        logging.error(f"Erro: {e}")
        logging.error(traceback.format_exc())
        return 1

    print("[OK] Aplicativo finalizado normalmente")
    return 0

if __name__ == '__main__':
    sys.exit(main())