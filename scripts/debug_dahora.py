#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import sys

print("=== DEBUG DAHORA APP ===")

try:
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    sys.path.append(root_dir)
    
    main_path = os.path.join(root_dir, 'main.py')
    
    # Importar e executar o main.py com encoding UTF-8
    with open(main_path, 'r', encoding='utf-8') as f:
        exec(f.read(), {'__file__': main_path, '__name__': '__main__'})
except Exception as e:
    print(f"\n❌ ERRO CAPTURADO: {e}")
    print(f"Tipo: {type(e).__name__}")
    print("\n📋 TRACEBACK COMPLETO:")
    traceback.print_exc()
    print("\n" + "="*50)
    sys.exit(1)