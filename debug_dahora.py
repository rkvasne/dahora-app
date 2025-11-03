#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import sys

print("=== DEBUG DAHORA APP ===")

try:
    # Importar e executar o dahora_app com encoding UTF-8
    with open('dahora_app.py', 'r', encoding='utf-8') as f:
        exec(f.read())
except Exception as e:
    print(f"\n❌ ERRO CAPTURADO: {e}")
    print(f"Tipo: {type(e).__name__}")
    print("\n📋 TRACEBACK COMPLETO:")
    traceback.print_exc()
    print("\n" + "="*50)
    sys.exit(1)