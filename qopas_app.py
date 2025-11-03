#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qopas App - Sistema de Bandeja do Windows
Gera data e hora no formato [DD.MM.AAAA-HH:MM] e copia para área de transferência
"""

import pystray
import pyperclip
from PIL import Image, ImageDraw
from datetime import datetime
import sys
import threading
import keyboard
import time
import json
import os
import logging
from threading import Lock

try:
    # Reutiliza a função de criação de ícone para evitar duplicação
    from create_icon import create_image as external_create_image
except Exception:
    external_create_image = None

# Para prevenir múltiplas instâncias
try:
    import win32event
    import win32con
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# Para notificações toast do Windows
try:
    from winotify import Notification
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False

# Força UTF-8 no console do Windows para evitar caracteres "?" em acentos
try:
    import ctypes
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    ctypes.windll.kernel32.SetConsoleCP(65001)
except Exception:
    pass

# Carrega o ícone personalizado
try:
    if os.path.exists('icon.ico'):
        icon_image = Image.open('icon.ico')
    else:
        icon_image = external_create_image() if external_create_image else create_image()
except Exception:
    icon_image = external_create_image() if external_create_image else create_image()

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


def generate_datetime_string():
    """Gera a data e hora no formato [<prefixo-]DD.MM.AAAA-HH:MM]"""
    now = datetime.now()
    base = now.strftime('%d.%m.%Y-%H:%M')
    try:
        prefix = date_prefix.strip()
    except Exception:
        prefix = ""
    if prefix:
        return f"[{prefix}-{base}]"
    return f"[{base}]"


def show_toast_notification(title, message, duration=2):
    """Mostra notificação toast do Windows - APENAS toast, sem MessageBox"""
    def _show_notification():
        # Método 1: winotify (toast nativo) - dura especificada
        if TOAST_AVAILABLE:
            try:
                mapped_duration = "short" if duration <= 5 else "long"
                toast = Notification(
                    app_id="Qopas App",
                    title=title,
                    msg=message,
                    duration=mapped_duration
                )
                toast.show()
                # Espera o tempo especificado + 0.5s para garantir
                time.sleep(duration + 0.5)
                return True
            except Exception:
                pass

        # Método 2: notificação do pystray (se icon já estiver rodando)
        try:
            if global_icon:
                global_icon.notify(message, title)
                # Espera o tempo especificado
                time.sleep(duration)
                return True
        except Exception:
            pass

        # Último recurso: print no console
        print(f"\n{'='*50}")
        print(f"{title}")
        print(f"{message}")
        print(f"{'='*50}\n")
        return False

    # Executa em thread para não bloquear
    thread = threading.Thread(target=_show_notification, daemon=False)
    thread.start()
    # Pequeno delay para garantir que iniciou
    time.sleep(0.05)


def show_fatal_error(title, message):
    """Exibe um MessageBox modal em caso de erro fatal no .exe"""
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, str(message), str(title), 0x10)
    except Exception:
        # Sem UI disponível
        pass


def copy_datetime(icon=None, item=None, source=None):
    """Copia a data e hora para a área de transferência"""
    dt_string = generate_datetime_string()
    pyperclip.copy(dt_string)

    # Adiciona data/hora ao histórico de clipboard
    add_to_clipboard_history(dt_string)

    # Incrementa o contador
    increment_counter()

    # Determina a origem da cópia para mensagem correta
    if item and hasattr(item, 'text'):
        # Veio do menu - obtém o texto do item do menu
        menu_text = item.text
        source = "Menu: " + menu_text
    else:
        # Veio de atalho ou fallback
        source = source or ("Atalho" if icon else "Fallback")

    # Mostra mensagem com contador (sem repetir atalho para menu)
    if source.startswith("Menu:"):
        show_toast_notification("Qopas App", f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {counter}ª vez")
    else:
        show_toast_notification("Qopas App", f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {counter}ª vez")


def create_image():
    """Cria um ícone de relógio digital claro e identificável"""
    # Cria uma imagem 64x64 com fundo transparente (RGBA)
    image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Cor principal: laranja (#FF9800)
    color_main = (255, 152, 0, 255)
    color_bg = (40, 40, 40, 255)  # Fundo escuro
    color_text = (255, 255, 255, 255)
    color_accent = (255, 87, 34, 255)  # Laranja mais escuro
    
    # Desenha um relógio digital tipo mostrador
    # Fundo arredondado (retângulo com bordas arredondadas simuladas)
    draw.rectangle([6, 8, 58, 56], fill=color_bg)
    
    # Borda externa
    draw.rectangle([6, 8, 58, 56], outline=color_main, width=3)
    
    # Mostrador digital - formato HH:MM
    # Dois pontos no meio (como relógio digital)
    draw.ellipse([28, 26, 32, 30], fill=color_main)
    draw.ellipse([28, 34, 32, 38], fill=color_main)
    
    # Números simulados (símbolos para representar hora)
    # Usa caracteres simples para simular display digital
    try:
        from PIL import ImageFont
        try:
            # Tenta usar fonte monospace maior
            font = ImageFont.truetype("consola.ttf", 20)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 18)
            except:
                font = ImageFont.load_default()
        
        # Texto "12:34" como exemplo visual
        text = "12:34"
        try:
            # Pillow 9.0+
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # Pillow < 9.0
            try:
                bbox = draw.textsize(text, font=font)
                text_width, text_height = bbox
            except:
                text_width, text_height = 50, 20
        
        x = 32 - text_width // 2
        y = 30 - text_height // 2
        draw.text((x, y), text, fill=color_main, font=font)
    except:
        # Fallback: desenha símbolo simples
        # Desenha linhas para simular display digital
        # Topo
        draw.line([14, 18, 22, 18], fill=color_main, width=3)
        # Meio
        draw.line([14, 32, 22, 32], fill=color_main, width=3)
        # Baixo
        draw.line([14, 46, 22, 46], fill=color_main, width=3)
        # Direita (segundo dígito)
        draw.line([42, 18, 50, 18], fill=color_main, width=3)
        draw.line([42, 32, 50, 32], fill=color_main, width=3)
        draw.line([42, 46, 50, 46], fill=color_main, width=3)
    
    return image


# Variável global para o ícone (necessária para hotkey)
global_icon = None

# Variável global para manter o mutex aberto
mutex_handle = None

# Diretório de dados do usuário para arquivos persistentes
APP_NAME = "QopasApp"

def _get_data_dir():
    base = os.getenv('APPDATA') or os.path.expanduser("~")
    path = os.path.join(base, APP_NAME)
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass
    return path

DATA_DIR = _get_data_dir()

# Logging básico para diagnóstico (arquivo no diretório de dados)
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(DATA_DIR, 'qopas.log'), encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
except Exception:
    logging.basicConfig(level=logging.INFO)

# Variável para controlar último clique esquerdo
last_click_time = 0
click_threshold = 0.5  # 500ms para considerar como clique duplo

# Variável global para contador de acionamentos
counter_file = os.path.join(DATA_DIR, "dahora_counter.txt")
counter = 0

# Variável global para histórico de clipboard
history_file = os.path.join(DATA_DIR, "clipboard_history.json")
clipboard_history = []
MAX_HISTORY_ITEMS = 100

# Variável para monitoramento de clipboard
last_clipboard_content = ""

# Locks para acesso thread-safe e escrita atômica
counter_lock = Lock()
history_lock = Lock()
settings_lock = Lock()

# Configurações persistentes
settings_file = os.path.join(DATA_DIR, "settings.json")
date_prefix = ""

def load_settings():
    global date_prefix
    try:
        with settings_lock:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            date_prefix = str(data.get("prefix", ""))
    except FileNotFoundError:
        date_prefix = ""
    except Exception as e:
        logging.warning(f"Falha ao carregar settings: {e}")
        date_prefix = ""

def save_settings():
    try:
        with settings_lock:
            _atomic_write_json(settings_file, {"prefix": date_prefix})
    except Exception as e:
        logging.warning(f"Falha ao salvar settings: {e}")

def _atomic_write_text(path, text, encoding="utf-8"):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding=encoding) as f:
        f.write(text)
    os.replace(tmp_path, path)

def _atomic_write_json(path, obj):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)

def load_counter():
    """Carrega o contador do arquivo ou inicia com 0"""
    global counter
    try:
        with counter_lock:
            with open(counter_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                counter = int(content) if content else 0
    except FileNotFoundError:
        counter = 0
    except Exception as e:
        logging.warning(f"Falha ao carregar contador: {e}")
        counter = 0

def save_counter():
    """Salva o contador no arquivo"""
    try:
        with counter_lock:
            _atomic_write_text(counter_file, str(counter))
    except Exception as e:
        logging.warning(f"Falha ao salvar contador: {e}")

def increment_counter():
    """Incrementa o contador e salva"""
    global counter
    try:
        with counter_lock:
            counter += 1
            _atomic_write_text(counter_file, str(counter))
    except Exception as e:
        logging.warning(f"Falha ao incrementar contador: {e}")


# Funções de histórico de clipboard
def load_clipboard_history():
    """Carrega o histórico do arquivo ou inicia com lista vazia"""
    global clipboard_history
    try:
        with history_lock:
            with open(history_file, "r", encoding="utf-8") as f:
                clipboard_history = json.load(f)
            if len(clipboard_history) > MAX_HISTORY_ITEMS:
                clipboard_history = clipboard_history[-MAX_HISTORY_ITEMS:]
    except FileNotFoundError:
        clipboard_history = []
    except Exception as e:
        logging.warning(f"Falha ao carregar histórico: {e}")
        clipboard_history = []

def save_clipboard_history():
    """Salva o histórico no arquivo"""
    try:
        with history_lock:
            _atomic_write_json(history_file, clipboard_history)
    except Exception as e:
        logging.warning(f"Falha ao salvar histórico: {e}")

def add_to_clipboard_history(text):
    """Adiciona um item ao histórico"""
    global clipboard_history
    if not text or not text.strip():
        return
    with history_lock:
        for item in clipboard_history:
            if item.get("text") == text:
                return
        new_item = {
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "app": "Qopas App"
        }
        clipboard_history.append(new_item)
        if len(clipboard_history) > MAX_HISTORY_ITEMS:
            clipboard_history = clipboard_history[-MAX_HISTORY_ITEMS:]
        _atomic_write_json(history_file, clipboard_history)

def clear_clipboard_history(icon=None, item=None):
    """Limpa todo o histórico"""
    global clipboard_history
    logging.info("Iniciando limpeza do histórico de clipboard")
    with history_lock:
        total_items = len(clipboard_history)
        clipboard_history = []
        try:
            # Força a escrita do arquivo vazio
            _atomic_write_json(history_file, [])
            logging.info(f"Histórico limpo com sucesso! {total_items} itens removidos")
        except Exception as e:
            logging.error(f"Falha ao salvar histórico limpo: {e}")
            try:
                # Tenta remover o arquivo completamente como fallback
                if os.path.exists(history_file):
                    os.remove(history_file)
                    logging.info("Arquivo de histórico removido como fallback")
            except Exception as e2:
                logging.error(f"Falha ao remover arquivo de histórico: {e2}")

    # Recarrega o histórico do arquivo para garantir consistência
    load_clipboard_history()

    # Mostra notificação de confirmação
    show_toast_notification("Qopas App", f"Histórico limpo!\n{total_items} itens removidos")

def get_recent_clipboard_items(limit=10):
    """Retorna os itens mais recentes do histórico"""
    with history_lock:
        return clipboard_history[-limit:].copy() if clipboard_history else []

def monitor_clipboard():
    """Monitora as mudanças na clipboard"""
    global last_clipboard_content
    logging.info("Monitor de clipboard iniciado")

    attempt = 0
    while True:
        attempt += 1
        try:
            current_content = pyperclip.paste()

            # Sempre loga o estado atual a cada 6 tentativas (a cada 18 segundos)
            if attempt % 6 == 0:
                logging.info(f"Verificação #{attempt} - Clipboard atual: '{current_content[:30] if current_content else 'vazio'}'")

            # Verifica se há conteúdo novo e não vazio
            if current_content and current_content.strip():
                # Se for diferente do último conteúdo ou se for o primeiro
                if current_content != last_clipboard_content:
                    logging.info(f"Clipboard mudou de '{last_clipboard_content[:30] if last_clipboard_content else 'vazio'}' para '{current_content[:30]}...'")
                    # Adiciona ao histórico
                    add_to_clipboard_history(current_content)
                    last_clipboard_content = current_content
                    logging.info(f"Clipboard atualizado: {current_content[:50]}...")

        except Exception as e:
            logging.warning(f"Erro ao monitorar clipboard: {e}")

        # Espera 3 segundos antes de verificar novamente
        time.sleep(3)

def copy_from_history(text):
    """Copia um item do histórico para a clipboard"""
    pyperclip.copy(text)
    # Incrementa o contador principal
    increment_counter()
    # Mostra notificação
    show_toast_notification("Qopas App", f"Copiado do histórico!\n{text}\nTotal: {counter}ª vez")

def _copy_history_item1(icon, item):
    """Copia o primeiro item do histórico (função separada para pystray)"""
    with history_lock:
        recent = clipboard_history[-1:] if clipboard_history else []
        if recent:
            copy_from_history(recent[0]["text"])

def _copy_history_item2(icon, item):
    """Copia o segundo item do histórico (função separada para pystray)"""
    with history_lock:
        recent = clipboard_history[-2:] if clipboard_history else []
        if len(recent) >= 2:
            copy_from_history(recent[1]["text"])

def _copy_history_item3(icon, item):
    """Copia o terceiro item do histórico (função separada para pystray)"""
    with history_lock:
        recent = clipboard_history[-3:] if clipboard_history else []
        if len(recent) >= 3:
            copy_from_history(recent[2]["text"])

def _copy_history_item4(icon, item):
    """Copia o quarto item do histórico (função separada para pystray)"""
    with history_lock:
        recent = clipboard_history[-4:] if clipboard_history else []
        if len(recent) >= 4:
            copy_from_history(recent[3]["text"])

def _copy_history_item5(icon, item):
    """Copia o quinto item do histórico (função separada para pystray)"""
    with history_lock:
        recent = clipboard_history[-5:] if clipboard_history else []
        if len(recent) >= 5:
            copy_from_history(recent[4]["text"])

def _copy_datetime_menu(icon, item):
    """Função wrapper para copy_datetime no menu (resolvendo pystray bug)"""
    copy_datetime(icon, item)

def show_about(icon, item):
    """Mostra informações sobre o aplicativo"""
    about_text = (
        "Qopas App v0.0.3\n\n"
        "Aplicativo para copiar data e hora\n"
        "Formato: [DD.MM.AAAA-HH:MM]\n\n"
        f"Total de acionamentos: {counter} vezes\n"
        f"Histórico de clipboard: {len(clipboard_history)} itens\n\n"
        "Atalho: Ctrl+Shift+Q\n\n"
        "Menu de opções via clique direito\n\n"
        "Histórico mantém últimos 100 itens\n"
        "Monitora clipboard a cada 3 segundos\n"
        "Clique em itens do histórico para copiar\n"
        "Opção 'Limpar Histórico' disponível"
    )
    # Mostra toast modal (dura 10 segundos para permitir leitura)
    show_toast_notification("Sobre - Qopas App", about_text, duration=10)


def on_exit(icon, item):
    """Fecha o aplicativo"""
    icon.stop()
    # Para o listener da hotkey
    try:
        keyboard.unhook_all()
    except:
        pass


def on_hotkey_triggered():
    """Função chamada quando a hotkey é pressionada"""
    copy_datetime(source="Atalho")

def on_ctrl_c_triggered():
    """Função chamada quando Ctrl+C é pressionado - adiciona ao clipboard history"""
    try:
        current_content = pyperclip.paste()
        if current_content and current_content.strip():
            add_to_clipboard_history(current_content)
            logging.info(f"Ctrl+C detectado: {current_content[:50]}...")
    except Exception as e:
        logging.warning(f"Falha ao processar Ctrl+C: {e}")

def setup_ctrl_c_listener():
    """Configura listener para Ctrl+C globalmente"""
    try:
        # Adiciona listener para Ctrl+C
        keyboard.add_hotkey('ctrl+c', on_ctrl_c_triggered, args=())
        logging.info("✅ Listener Ctrl+C configurado")
    except Exception as e:
        logging.warning(f"⚠️  Não foi possível configurar listener Ctrl+C: {e}")

def monitor_clipboard_smart():
    """Monitora inteligente do clipboard - atividade-first, polling-second"""
    global last_clipboard_content
    logging.info("Monitor inteligente de clipboard iniciado")

    # Primeiro, tente obter o conteúdo atual
    try:
        last_clipboard_content = pyperclip.paste()
        logging.info(f"Clipboard inicializado: '{last_clipboard_content[:30] if last_clipboard_content else 'vazio'}'")
    except Exception as e:
        logging.warning(f"Erro ao inicializar clipboard: {e}")
        last_clipboard_content = ""

    attempt = 0
    last_activity_time = time.time()
    last_menu_update = time.time()
    idle_threshold = 30  # segundos sem atividade antes de aumentar intervalo
    menu_update_interval = 10  # segundos entre atualizações do menu

    while True:
        attempt += 1
        current_time = time.time()

        try:
            # Verifica se há conteúdo no clipboard
            current_content = pyperclip.paste()

            # Log a cada 6 tentativas (para logging, não para verificação)
            if attempt % 6 == 0:
                time_idle = current_time - last_activity_time
                logging.info(f"Verificação #{attempt} - Clipboard: '{current_content[:30] if current_content else 'vazio'}' (ocioso há {time_idle:.1f}s)")

            # Verifica se há conteúdo novo e não vazio
            if current_content and current_content.strip():
                # Se for diferente do último conteúdo
                if current_content != last_clipboard_content:
                    logging.info(f"Clipboard mudou de '{last_clipboard_content[:30] if last_clipboard_content else 'vazio'}' para '{current_content[:30]}...'")
                    # Adiciona ao histórico
                    add_to_clipboard_history(current_content)
                    last_clipboard_content = current_content
                    last_activity_time = current_time  # Atualiza tempo de atividade
                    logging.info(f"Clipboard atualizado: {current_content[:50]}...")

                    # Atualiza menu imediatamente quando há novo item
                    if global_icon and hasattr(global_icon, 'update_menu'):
                        try:
                            global_icon.update_menu()
                            logging.info("Menu atualizado imediatamente após nova cópia")
                        except Exception as e:
                            logging.warning(f"Erro ao atualizar menu: {e}")

                # Se há atividade recente, usa intervalo curto (responsivo)
                time_idle = current_time - last_activity_time
                if time_idle < idle_threshold:
                    sleep_time = 0.5  # Responde rápido quando há atividade
                else:
                    sleep_time = 5.0  # Intervalo maior quando ocioso

            else:
                # Clipboard vazio - aumenta intervalo para economizar recursos
                time_idle = current_time - last_activity_time
                if time_idle > idle_threshold:
                    sleep_time = min(10.0, 2 + time_idle * 0.1)  # Intervalo crescente com ociosidade
                else:
                    sleep_time = 2.0

            # Atualiza o menu periodicamente mesmo sem atividade
            if current_time - last_menu_update >= menu_update_interval:
                if global_icon and hasattr(global_icon, 'update_menu'):
                    try:
                        global_icon.update_menu()
                        last_menu_update = current_time
                        logging.info("Menu atualizado periodicamente")
                    except Exception as e:
                        logging.warning(f"Erro ao atualizar menu: {e}")
                else:
                    logging.warning("Icon ou update_menu não disponíveis para atualização periódica")

        except Exception as e:
            logging.warning(f"Erro ao monitorar clipboard: {e}")
            sleep_time = 3.0  # Intervalo padrão em caso de erro

        # Espera baseado na atividade (intervalo adaptativo)
        time.sleep(sleep_time)


def setup_hotkey_listener():
    """Configura o listener da tecla de atalho global"""
    # Tecla de atalho: Ctrl + Shift + Q (Quick) - combinação menos comum
    hotkey = 'ctrl+shift+q'
    try:
        keyboard.add_hotkey(hotkey, on_hotkey_triggered)
        print(f"✅ Tecla de atalho configurada: {hotkey.upper()}")
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível configurar a tecla de atalho: {e}")
        print("💡 O aplicativo continuará funcionando, mas a hotkey pode não estar disponível")

    # Configura listener para Ctrl+C
    setup_ctrl_c_listener()


def setup_icon(reload=False):
    """Configura o ícone da bandeja com menu dinâmico"""

    def copy_from_history(text):
        """Copia item do histórico para clipboard"""
        try:
            pyperclip.copy(text)
            show_toast_notification("Qopas App", f"Copiado do histórico!\n{text}\nTotal: {counter}ª vez")
        except Exception as e:
            logging.warning(f"Erro ao copiar do histórico: {e}")

    def _copy_datetime_menu(icon, item):
        """Função para o menu de copiar data/hora"""
        copy_datetime(source="menu")

    def set_prefix_action():
        """Ação para definir prefixo"""
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal
        root.title("Definir Prefixo")

        # Cria janela simples
        frame = tk.Frame(root)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Prefixo para data/hora:").pack()

        var = tk.StringVar(value=date_prefix)
        entry = tk.Entry(frame, textvariable=var, width=30)
        entry.pack(pady=10)
        entry.focus()
        entry.select_range(0, tk.END)

        def on_ok():
            root.destroy()
            global date_prefix
            date_prefix = var.get()
            save_settings()
            show_toast_notification("Qopas App", f"Prefixo atualizado: {date_prefix or '(vazio)'}")

        def on_cancel():
            root.destroy()

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancelar", command=on_cancel).pack(side=tk.LEFT, padx=5)

        # Bind Enter para OK e Escape para Cancelar
        root.bind('<Return>', lambda e: on_ok())
        root.bind('<Escape>', lambda e: on_cancel())

        root.mainloop()

    # Cria menu dinâmico que pode ser atualizado
    def create_dynamic_menu():
        """Cria menu dinâmico com base no histórico atual"""
        menu_items = [
            pystray.MenuItem('Copiar Data/Hora (Ctrl+Shift+Q)', _copy_datetime_menu, default=True),
            pystray.MenuItem('', None, enabled=False),  # Separador
            pystray.MenuItem('Definir Prefixo...', set_prefix_action),
        ]

        # Pega itens recentes do histórico
        recent = get_recent_clipboard_items(5)

        # Adiciona itens do histórico ao menu
        if recent:
            menu_items.append(pystray.MenuItem('--- Histórico Recente ---', None, enabled=False))
            for idx, entry in enumerate(reversed(recent), start=1):
                text = entry.get("text", "") or ""
                display_text = (text[:40] + "...") if len(text) > 40 else text

                # Cria função dinamicamente para cada item
                def make_copy_func(text):
                    return lambda icon, item: copy_from_history(text)

                copy_func = make_copy_func(text)
                menu_items.append(pystray.MenuItem(f"[{idx}] {display_text}", copy_func))
        else:
            menu_items.append(pystray.MenuItem('Nenhum item no histórico', None, enabled=False))

        menu_items.append(pystray.MenuItem('', None, enabled=False))  # Separador
        menu_items.append(pystray.MenuItem('Limpar Histórico', clear_clipboard_history))
        menu_items.append(pystray.MenuItem('', None, enabled=False))  # Separador
        menu_items.append(pystray.MenuItem('Sobre', show_about))
        menu_items.append(pystray.MenuItem('Sair', lambda icon, item: sys.exit(0)))

        return pystray.Menu(*menu_items)

    # Função para atualizar o menu
    def update_menu():
        """Atualiza o menu com o histórico mais recente"""
        try:
            # Evita atualizações recursivas limitando a uma atualização por chamada
            if not hasattr(update_menu, '_last_update'):
                update_menu._last_update = 0

            current_time = time.time()
            # Limita a uma atualização por segundo para evitar recursão
            if current_time - update_menu._last_update < 1.0:
                return

            update_menu._last_update = current_time

            icon.menu = create_dynamic_menu()
            logging.info("Menu atualizado com histórico mais recente")
        except Exception as e:
            logging.warning(f"Erro ao atualizar menu: {e}")

    # Cria ícone com menu dinâmico
    icon = pystray.Icon(
        "Qopas App",
        icon_image,
        "Qopas App",
        create_dynamic_menu()
    )

    # Armazena função de atualização para uso futuro
    icon.update_menu = update_menu

    return icon


def check_single_instance():
    """Verifica se já existe uma instância rodando"""
    global mutex_handle

    if not WIN32_AVAILABLE:
        return True  # Se não tiver Win32, deixa passar

    mutex_name = "Global\\QopasAppSingleInstance"
    try:
        # Tenta criar um mutex nomeado global
        mutex_handle = win32event.CreateMutex(None, False, mutex_name)
        result = win32api.GetLastError()

        # Se o mutex já existia, outra instância está rodando
        if result == 183:  # ERROR_ALREADY_EXISTS
            notification_thread = threading.Thread(
                target=show_toast_notification,
                args=("Qopas App Já em Execução",
                      "O Qopas App já está rodando na bandeja do sistema!"),
                daemon=False
            )
            notification_thread.start()
            notification_thread.join(timeout=3.0)
            return False

        return True

    except Exception as e:
        print(f"Erro na verificação de instância única: {e}")
        return True


# Variável global para o ícone
global_icon = None

def main():
    """Função principal"""
    global mutex_handle, global_icon

    # Verifica se o arquivo de ícone existe
    try:
        import os
        if not os.path.exists('icon.ico'):
            print("⚠️  Arquivo icon.ico não encontrado. O app usará ícone padrão.")
    except:
        pass

    # Carrega contador, historico e configuracoes ao iniciar
    load_counter()
    load_clipboard_history()
    load_settings()
    # Inicializa o estado atual da clipboard
    try:
        last_clipboard_content = pyperclip.paste()
        logging.info(f"Clipboard inicializado com: {last_clipboard_content[:50] if last_clipboard_content else 'vazio'}")
    except Exception as e:
        logging.warning(f"Erro ao inicializar clipboard: {e}")
        last_clipboard_content = ""
    # Verifica se já existe uma instância rodando
    if not check_single_instance():
        sys.exit(0)

    try:
        # Configura a hotkey em uma thread separada
        hotkey_thread = threading.Thread(target=setup_hotkey_listener, daemon=True)
        hotkey_thread.start()
        logging.info("Thread de hotkey iniciada")

        # Inicia o monitoramento de clipboard inteligente em uma thread separada
        monitor_thread = threading.Thread(target=monitor_clipboard_smart, daemon=True)
        monitor_thread.start()
        logging.info("Thread de monitoramento inteligente de clipboard iniciada")

        # Inicia o ícone da bandeja
        icon = setup_icon()
        global_icon = icon  # Armazena globalmente para acesso do monitoramento

        # Mostra mensagem de boas-vindas com contador, histórico e prefixo
        total_history = len(clipboard_history)
        show_toast_notification("Qopas App", f"App iniciado com sucesso!\nAtalho: Ctrl+Shift+Q\nPrefixo: {date_prefix or '(vazio)'}\nMenu: clique direito no ícone\nJá acionado {counter} vezes • Histórico: {total_history} itens")

        # Executa o ícone (bloqueia até fechar)
        icon.run()

    except KeyboardInterrupt:
        print("Qopas App encerrado pelo usuário")
    except Exception as e:
        try:
            import traceback
            logging.error("Erro inesperado:\n" + traceback.format_exc())
        except Exception:
            pass
        show_fatal_error("Qopas App - Erro", f"Ocorreu um erro inesperado:\n{e}\n\nConsulte o log em: {os.path.join(DATA_DIR, 'qopas.log')}")
    finally:
        # Limpa recursos ao fechar
        try:
            if mutex_handle:
                win32api.CloseHandle(mutex_handle)
            keyboard.unhook_all()
            print("Recursos liberados com sucesso")
        except:
            pass


if __name__ == '__main__':
    main()





