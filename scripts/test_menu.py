"""
Script de teste para verificar itens do menu
"""
import sys
import os

# Configura encoding UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Adiciona o diretório pai ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dahora_app.ui.menu import MenuBuilder

# Cria menu builder
menu_builder = MenuBuilder()

# Define callbacks dummy
menu_builder.set_copy_datetime_callback(lambda icon, item: print("Copy datetime"))
menu_builder.set_show_search_callback(lambda: print("Show search"))
menu_builder.set_show_custom_shortcuts_callback(lambda: print("Show settings"))
menu_builder.set_refresh_menu_callback(lambda icon, item: print("Refresh"))
menu_builder.set_get_recent_items_callback(lambda limit: [])
menu_builder.set_copy_from_history_callback(lambda text: print(f"Copy: {text}"))
menu_builder.set_clear_history_callback(lambda icon, item: print("Clear"))
menu_builder.set_show_about_callback(lambda icon, item: print("About"))
menu_builder.set_quit_callback(lambda icon, item: print("Quit"))

# Gera itens do menu
items = menu_builder._get_dynamic_menu_items()

print("=" * 60)
print("ITENS DO MENU GERADOS:")
print("=" * 60)

for i, item in enumerate(items, 1):
    if hasattr(item, 'text'):
        print(f"{i}. {item.text}")
    elif str(item) == "Menu.SEPARATOR":
        print(f"{i}. ─────────────────")
    else:
        print(f"{i}. {item}")

print("=" * 60)
print(f"TOTAL: {len(items)} itens")
print("=" * 60)

# Verifica se "Configurações" está presente
config_presente = any(hasattr(item, 'text') and 'Configurações' in item.text for item in items)
print(f"\n✅ 'Configurações' PRESENTE: {config_presente}")

if not config_presente:
    print("❌ ERRO: Item 'Configurações' NÃO encontrado!")
else:
    print("✅ SUCESSO: Item 'Configurações' encontrado no menu!")
