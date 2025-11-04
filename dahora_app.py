#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dahora App - Sistema de Bandeja do Windows
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
from logging.handlers import RotatingFileHandler
from threading import Lock

# Import para interface gráfica (janela de prefixo)
try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


def set_prefix_action():
    """Ação para definir prefixo"""
    logging.info("set_prefix_action() chamada - Iniciando janela de prefixo")

    if not TKINTER_AVAILABLE:
        logging.error("Tkinter não disponível")
        show_toast_notification("Dahora App", "Tkinter não disponível. Não é possível definir prefixo.")
        return

    # Executa em thread separada para evitar conflitos com pystray
    import threading

    def show_prefix_dialog():
        try:
            logging.info("Criando janela Tkinter (estilo Windows 11) em thread separada")

            # Importa ttk e fontes
            from tkinter import ttk, font as tkFont

            # Janela principal
            root = tk.Tk()
            root.title("Dahora App - Definir Prefixo")
            root.resizable(False, False)
            root.focus_force()

            # Tema moderno do Windows (vista)
            try:
                style = ttk.Style()
                style.theme_use('vista')
            except Exception:
                style = ttk.Style()

            # Fonte preferida
            def get_available_font():
                try:
                    available_fonts = tkFont.families()
                    preferred_fonts = ["Segoe UI", "Segoe UI Variable", "Arial", "Tahoma", "Microsoft Sans Serif", "Verdana"]
                    for f in preferred_fonts:
                        if f in available_fonts:
                            return f
                    return "TkDefaultFont"
                except Exception:
                    return "TkDefaultFont"

            default_font = get_available_font()
            logging.info(f"Usando fonte: {default_font}")

            # Conteúdo
            main = ttk.Frame(root, padding=(20, 16, 20, 16))
            main.pack(fill=tk.BOTH, expand=True)

            # Cabeçalho simples (sem barra colorida)
            ttk.Label(
                main,
                text="Prefixo de data/hora",
                font=(default_font, 11, "bold")
            ).pack(anchor=tk.W, pady=(0, 2))

            ttk.Label(
                main,
                text="Digite um prefixo para personalizar a cópia de data/hora.",
                font=(default_font, 9)
            ).pack(anchor=tk.W, pady=(2, 12))

            # Campo de entrada
            var = tk.StringVar(value=date_prefix)
            ttk.Label(main, text="Prefixo", font=(default_font, 9)).pack(anchor=tk.W)
            entry = ttk.Entry(main, textvariable=var, width=36)
            entry.pack(fill=tk.X, pady=(6, 10))
            entry.focus()
            entry.select_range(0, tk.END)

            # Exemplo dinâmico
            example_label = ttk.Label(main, font=(default_font, 8))
            example_label.pack(anchor=tk.W)

            def render_example():
                base = datetime.now().strftime('%d.%m.%Y-%H:%M')
                p = var.get().strip()
                prefix_part = f"{p}-" if p else ""
                example_label.configure(text=f"Exemplo: [{prefix_part}{base}]")

            render_example()
            try:
                var.trace_add('write', lambda *args: render_example())
            except Exception:
                pass

            # Ações
            def on_ok():
                new_prefix = var.get().strip()
                global date_prefix
                date_prefix = new_prefix
                save_settings()
                show_toast_notification("Dahora App", f"Prefixo atualizado!\n{date_prefix or '(vazio)'}")
                logging.info(f"Prefixo atualizado para: {date_prefix}")
                root.destroy()

            def on_cancel():
                root.destroy()

            # Botões alinhados à direita
            buttons = ttk.Frame(main)
            buttons.pack(fill=tk.X, pady=(16, 0))
            # Ordem moderna: Cancelar à esquerda, Salvar à direita
            ttk.Button(buttons, text="Salvar", command=on_ok).pack(side=tk.RIGHT)
            ttk.Button(buttons, text="Cancelar", command=on_cancel).pack(side=tk.RIGHT, padx=(8, 0))

            # Bind de teclas
            root.bind('<Return>', lambda e: on_ok())
            root.bind('<Escape>', lambda e: on_cancel())

            # Centraliza janela após medir
            root.update_idletasks()
            width = max(420, root.winfo_width())
            height = max(200, root.winfo_height())
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f'{width}x{height}+{x}+{y}')

            # Loop
            root.mainloop()
            logging.info("Janela de prefixo fechada")

        except Exception as e:
            logging.error(f"Erro ao abrir janela de prefixo: {e}")
            show_toast_notification("Dahora App", f"Erro: {e}")

    # Inicia a thread da janela
    thread = threading.Thread(target=show_prefix_dialog, daemon=True)
    thread.start()
    logging.info("Thread da janela de prefixo iniciada")

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
                    app_id="Dahora App",
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


def show_quick_notification(title, message, duration=1):
    """Exibe uma notificação leve e moderna por ~1–2s usando Tkinter."""
    if not 'TKINTER_AVAILABLE' in globals():
        # Fallback se variável não existir
        return show_toast_notification(title, message, duration=duration)

    if not TKINTER_AVAILABLE:
        return show_toast_notification(title, message, duration=duration)

    def _show_quick():
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()

            top = tk.Toplevel(root)
            top.overrideredirect(True)
            try:
                top.attributes('-topmost', True)
            except Exception:
                pass

            # Dimensões e posição (canto inferior direito)
            
            # Tamanho e posição (canto inferior direito)
            try:
                root.update_idletasks()
                sw = root.winfo_screenwidth()
                sh = root.winfo_screenheight()
            except Exception:
                sw, sh = 1366, 768

            width, height = 340, 110
            x = sw - width - 16
            y = sh - height - 48
            top.geometry(f"{width}x{height}+{x}+{y}")

            # Canvas com “card” arredondado para parecer toast do Windows
            canvas = tk.Canvas(top, width=width, height=height, bg='black', highlightthickness=0)
            canvas.pack(fill='both', expand=True)

            # Função para retângulo arredondado
            def round_rect(x1, y1, x2, y2, r=12, **kwargs):
                points = [
                    x1+r, y1,
                    x2-r, y1,
                    x2, y1,
                    x2, y1+r,
                    x2, y2-r,
                    x2, y2,
                    x2-r, y2,
                    x1+r, y2,
                    x1, y2,
                    x1, y2-r,
                    x1, y1+r,
                    x1, y1
                ]
                return canvas.create_polygon(points, smooth=True, **kwargs)

            # Fundo
            round_rect(2, 2, width-2, height-2, r=14, fill='#2b2b2b', outline='#3c3c3c')

            # Título e mensagem
            try:
                title_font = ('Segoe UI Variable', 10, 'bold')
                msg_font = ('Segoe UI Variable', 9)
            except Exception:
                title_font = ('Segoe UI', 10, 'bold')
                msg_font = ('Segoe UI', 9)

            # Use widgets transparentes sobre o canvas com place
            frame = tk.Frame(top, bg='#2b2b2b')
            frame.place(x=0, y=0, width=width, height=height)
            lbl_title = tk.Label(frame, text=title, fg='#c5e1ff', bg='#2b2b2b', font=title_font)
            lbl_title.place(x=16, y=12)
            lbl_msg = tk.Label(frame, text=message, fg='#ffffff', bg='#2b2b2b', font=msg_font, justify='left')
            lbl_msg.place(x=16, y=36)

            # Fecha após duração
            top.after(int(max(1, duration) * 1000), root.destroy)
            root.mainloop()
        except Exception:
            # Fallback se Tk falhar
            show_toast_notification(title, message, duration=duration)

    threading.Thread(target=_show_quick, daemon=True).start()


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
        show_toast_notification("Dahora App", f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {counter}ª vez")
    else:
        # Para atalho, tenta notificação rápida real via Tkinter (~1.5s)
        dur = 1.5 if source == "Atalho" else 2
        try:
            if source == "Atalho" and TKINTER_AVAILABLE:
                show_quick_notification("Dahora App", f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {counter}ª vez", duration=dur)
            elif source == "Atalho" and global_icon:
                global_icon.notify(f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {counter}ª vez", "Dahora App")
                time.sleep(dur)
            else:
                show_toast_notification("Dahora App", f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {counter}ª vez", duration=dur)
        except Exception:
            show_toast_notification("Dahora App", f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {counter}ª vez", duration=dur)


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
APP_NAME = "DahoraApp"

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
    log_path = os.path.join(DATA_DIR, 'dahora.log')
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    )
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, logging.StreamHandler(sys.stdout)]
    )
    logging.info("Sistema de rotação de logs ativado (5MB, 3 backups)")
except Exception as e:
    logging.basicConfig(level=logging.INFO)
    logging.warning(f"Falha ao configurar rotação de logs: {e}")

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

def validate_settings(settings_dict):
    """Valida e sanitiza configurações carregadas"""
    try:
        import re
        # Valida prefix
        prefix = str(settings_dict.get("prefix", ""))
        if len(prefix) > 100:
            logging.warning("Prefixo muito longo, truncando para 100 chars")
            prefix = prefix[:100]
        
        # Remove caracteres perigosos (controle ASCII)
        prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
        
        return {"prefix": prefix}
    except Exception as e:
        logging.error(f"Erro ao validar settings: {e}")
        return {"prefix": ""}

def load_settings():
    global date_prefix
    try:
        with settings_lock:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Valida configurações antes de aplicar
            validated = validate_settings(data)
            date_prefix = validated["prefix"]
    except FileNotFoundError:
        date_prefix = ""
    except json.JSONDecodeError as e:
        logging.error(f"Settings corrompido, usando padrão: {e}")
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
            "app": "Dahora App"
        }
        clipboard_history.append(new_item)
        if len(clipboard_history) > MAX_HISTORY_ITEMS:
            clipboard_history = clipboard_history[-MAX_HISTORY_ITEMS:]
        _atomic_write_json(history_file, clipboard_history)
        logging.info(f"Histórico atualizado: total={len(clipboard_history)}; último='{text[:50]}...'")
        # Não atualiza menu aqui: evita travar UI (pystray/WNDPROC) com chamadas
        # de threads externas. O menu é recalculado apenas na abertura.

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
    show_toast_notification("Dahora App", f"Histórico limpo!\n{total_items} itens removidos")

    # Atualiza o menu dinamicamente para refletir o histórico limpo
    try:
        if 'atualizar_menu_dinamico' in globals():
            atualizar_menu_dinamico()
            logging.info("Menu atualizado após limpar histórico")
    except Exception as e:
        logging.warning(f"Erro ao atualizar menu após limpar histórico: {e}")

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
    show_toast_notification("Dahora App", f"Copiado do histórico!\n{text}\nTotal: {counter}ª vez")

def copy_history_item(text):
    """Copia um item específico do histórico"""
    try:
        pyperclip.copy(text)
        increment_counter()
        show_toast_notification("Dahora App", f"Copiado do histórico!\n{text[:50]}...\nTotal: {counter}ª vez")
    except Exception as e:
        logging.warning(f"Erro ao copiar item do histórico: {e}")

def clear_history(icon=None, item=None):
    """Limpa o histórico do clipboard"""
    global clipboard_history
    with history_lock:
        clipboard_history.clear()
    show_toast_notification("Dahora App", "Histórico limpo!")
    logging.info("Histórico do clipboard limpo")

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
        "Dahora App v0.0.3\n\n"
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
    show_toast_notification("Sobre - Dahora App", about_text, duration=10)


def show_privacy_notice():
    """Mostra aviso de privacidade na primeira execução"""
    notice_file = os.path.join(DATA_DIR, ".privacy_accepted")
    
    if os.path.exists(notice_file):
        return  # Já mostrou antes
    
    message = (
        "AVISO DE PRIVACIDADE\n\n"
        "O Dahora App mantém um histórico local dos últimos 100 itens "
        "copiados para a área de transferência.\n\n"
        "⚠️ Este histórico pode conter informações sensíveis "
        "(senhas, tokens, etc.)\n\n"
        "Os dados são armazenados LOCALMENTE em:\n"
        f"{DATA_DIR}\n\n"
        "Não há coleta de dados ou telemetria.\n\n"
        "Você pode limpar o histórico a qualquer momento pelo menu."
    )
    
    show_toast_notification("Dahora App - Privacidade", message, duration=15)
    logging.info("Aviso de privacidade exibido (primeira execução)")
    
    # Marca como aceito
    try:
        with open(notice_file, 'w', encoding='utf-8') as f:
            f.write(datetime.now().isoformat())
    except Exception as e:
        logging.warning(f"Falha ao marcar aviso de privacidade: {e}")


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

def on_refresh_hotkey_triggered():
    """Hotkey para recarregar itens do menu (aciona ação segura)"""
    try:
        logging.info("[Hotkey] Recarregar Itens acionado (CTRL+SHIFT+R)")
        # Usa a mesma ação do item de menu para manter execução segura
        if 'refresh_menu_action' in globals():
            refresh_menu_action(global_icon, None)
    except Exception as e:
        logging.warning(f"[Hotkey] Erro ao atualizar menu: {e}")

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
        logging.info("[OK] Listener Ctrl+C configurado")
    except Exception as e:
        logging.warning(f"[AVISO] Nao foi possivel configurar listener Ctrl+C: {e}")

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
        print(f"[OK] Tecla de atalho configurada: {hotkey.upper()}")
    except Exception as e:
        print(f"[AVISO] Nao foi possivel configurar a tecla de atalho: {e}")
        print("[INFO] O aplicativo continuara funcionando, mas a hotkey pode nao estar disponivel")

    # Hotkey para recarregar itens do menu
    refresh_hotkey = 'ctrl+shift+r'
    try:
        keyboard.add_hotkey(refresh_hotkey, on_refresh_hotkey_triggered)
        print(f"[OK] Tecla de atalho configurada: {refresh_hotkey.upper()} (recarregar itens do menu)")
    except Exception as e:
        print(f"[AVISO] Nao foi possivel configurar a hotkey de recarga: {e}")

    # Configura listener para Ctrl+C
    setup_ctrl_c_listener()


def copy_from_history(text):
    """Copia item do histórico para clipboard"""
    try:
        pyperclip.copy(text)
        increment_counter()
        show_toast_notification("Dahora App", f"Copiado do histórico!\n{text}\nTotal: {counter}ª vez")
    except Exception as e:
        logging.warning(f"Erro ao copiar do histórico: {e}")

def _copy_datetime_menu(icon, item):
    """Aciona copiar data/hora. Se vier de clique esquerdo, usa estilo do atalho."""
    # Deixamos que copy_datetime identifique a origem:
    # - item None (clique esquerdo default) => "Atalho" (mensagem rápida)
    # - item presente (menu) => "Menu: <texto>" (toast padrão)
    copy_datetime(icon, item)

def quit_app(icon, item):
    """Função para encerrar o aplicativo corretamente"""
    try:
        logging.info("Encerrando Dahora App...")
        if 'mutex_handle' in globals() and mutex_handle:
            win32api.CloseHandle(mutex_handle)
        keyboard.unhook_all()
        icon.stop()
    except Exception as e:
        logging.error(f"Erro ao encerrar app: {e}")
    finally:
        sys.exit(0)

def refresh_menu_action(icon, item):
    """Atualiza manualmente o menu; usada quando o menu está aberto"""
    try:
        logging.info("Atualização manual do menu solicitada pelo usuário (menu aberto)")
        atualizar_menu_dinamico()
        # Informar ao usuário que precisará reabrir o menu para ver as mudanças
        show_toast_notification("Dahora App", "Menu atualizado! Feche e abra novamente para ver.")
    except Exception as e:
        logging.warning(f"Erro ao atualizar menu manualmente: {e}")

def create_menu_dinamico():
    """Cria um menu dinâmico que atualiza o histórico a cada abertura"""
    logging.info("Gerando menu dinâmico com histórico atualizado")
    
    def get_dynamic_menu():
        """Função que retorna o menu atualizado"""
        menu_items = []
        try:
            logging.info("[Menu] Calculando itens dinâmicos (abertura do menu)")
        except Exception:
            pass

        # Opções principais
        menu_items.append(pystray.MenuItem('Copiar Data/Hora', _copy_datetime_menu, default=True))
        menu_items.append(pystray.MenuItem('Definir Prefixo', set_prefix_action))
        # Ação de recarga rápida posicionada acima do histórico
        menu_items.append(pystray.MenuItem('Recarregar Itens', refresh_menu_action))
        
        # Separador
        menu_items.append(pystray.Menu.SEPARATOR)
        
        # Histórico dinâmico (últimos 5 itens atualizados em tempo real)
        recent = get_recent_clipboard_items(5)
        if recent:
            for idx, entry in enumerate(reversed(recent), start=1):
                text = entry.get("text", "") or ""
                display_text = (text[:40] + "...") if len(text) > 40 else text
                display_text = display_text.replace('\n', ' ').replace('\r', ' ')
                
                # Cria função para copiar item do histórico
                def make_copy_func(txt):
                    return lambda icon, item: copy_from_history(txt)
                
                copy_func = make_copy_func(text)
                menu_items.append(pystray.MenuItem(f"{idx}. {display_text}", copy_func))
        else:
            menu_items.append(pystray.MenuItem('(Histórico vazio)', None, enabled=False))
        
        # Separador
        menu_items.append(pystray.Menu.SEPARATOR)
        
        # Opções finais
        menu_items.append(pystray.MenuItem('Limpar Histórico', clear_clipboard_history))
        menu_items.append(pystray.MenuItem('Sobre', show_about))
        menu_items.append(pystray.MenuItem('Sair', quit_app))

        logging.info(f"Menu gerado com {len(recent) if recent else 0} itens do histórico")
        return menu_items
    
    # Retorna um menu dinâmico recalculado a cada abertura (modo estável)
    # Usamos um gerador para forçar reavaliação no evento de abertura
    def dynamic_items():
        try:
            items = get_dynamic_menu()
            logging.info(f"[Menu] Itens calculados: {len(items)}")
            for it in items:
                yield it
        except Exception as e:
            logging.warning(f"Falha ao gerar itens do menu dinâmico: {e}")
            # Fallback mínimo para não quebrar o menu
            yield pystray.MenuItem('(Erro ao gerar menu)', None, enabled=False)
    return pystray.Menu(dynamic_items)


def atualizar_menu_dinamico():
    """Atualiza o menu do ícone com o histórico mais recente"""
    try:
        if global_icon:
            logging.info("Atualizando menu dinamicamente")
            # Recria o menu completamente
            global_icon.menu = create_menu_dinamico()
            logging.info("Menu atualizado com sucesso")
        else:
            logging.warning("Não foi possível atualizar menu - ícone não disponível")
    except Exception as e:
        logging.warning(f"Erro ao atualizar menu dinamicamente: {e}")


def setup_icon(reload=False):
    """Configura o ícone da bandeja com menu estático e estável"""

    # Resolve caminho correto do ícone (suporta execução via PyInstaller)
    try:
        base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    except Exception:
        base_dir = os.path.abspath(os.path.dirname(__file__))
    icon_path = os.path.join(base_dir, 'icon.ico')

    # Carrega o ícone personalizado
    try:
        if os.path.exists(icon_path):
            icon_image = Image.open(icon_path)
        else:
            icon_image = external_create_image() if external_create_image else create_image()
    except Exception:
        icon_image = external_create_image() if external_create_image else create_image()

    # Cria ícone com menu dinâmico que atualiza a cada abertura
    icon = pystray.Icon(
        "Dahora App",
        icon_image,
        "Dahora App - Sistema de Data/Hora",
        menu=create_menu_dinamico()
    )

    # Armazena referência global
    global global_icon
    global_icon = icon

    return icon


def check_single_instance():
    """Verifica se já existe uma instância rodando"""
    global mutex_handle

    if not WIN32_AVAILABLE:
        return True  # Se não tiver Win32, deixa passar

    mutex_name = "Global\\DahoraAppSingleInstance"
    try:
        # Tenta criar um mutex nomeado global
        mutex_handle = win32event.CreateMutex(None, False, mutex_name)
        result = win32api.GetLastError()

        # Se o mutex já existia, outra instância está rodando
        if result == 183:  # ERROR_ALREADY_EXISTS
            notification_thread = threading.Thread(
                target=show_toast_notification,
                args=("Dahora App Já em Execução",
                      "O Dahora App já está rodando na bandeja do sistema!"),
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
            print("[AVISO] Arquivo icon.ico nao encontrado. O app usara icone padrao.")
    except:
        pass

    # Carrega contador, historico e configuracoes ao iniciar
    load_counter()
    load_clipboard_history()
    load_settings()
    
    # Mostra aviso de privacidade na primeira execução
    show_privacy_notice()
    
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
        print(f">>> App iniciado! Counter: {counter}, Histórico: {total_history}, Prefixo: {date_prefix or '(vazio)'}")
        show_toast_notification("Dahora App", f"App iniciado com sucesso!\nAtalho: Ctrl+Shift+Q\nPrefixo: {date_prefix or '(vazio)'}\nMenu: clique direito no ícone\nJá acionado {counter} vezes • Histórico: {total_history} itens")

        # Executa o ícone (bloqueia até fechar)
        print(">>> Iniciando ícone da bandeja...")
        logging.info("Iniciando icon.run()")
        icon.run()
        print(">>> Ícone da bandeja finalizado")

    except KeyboardInterrupt:
        print("Dahora App encerrado pelo usuário")
    except Exception as e:
        try:
            import traceback
            logging.error("Erro inesperado:\n" + traceback.format_exc())
        except Exception:
            pass
        show_fatal_error("Dahora App - Erro", f"Ocorreu um erro inesperado:\n{e}\n\nConsulte o log em: {os.path.join(DATA_DIR, 'dahora.log')}")
    finally:
        # Limpa recursos ao fechar
        try:
            logging.info("Limpando recursos...")
            if 'mutex_handle' in globals() and mutex_handle:
                win32api.CloseHandle(mutex_handle)
                logging.info("Mutex liberado")
            keyboard.unhook_all()
            logging.info("Hotkeys liberados")
            print("Recursos liberados com sucesso")
        except Exception as e:
            logging.error(f"Erro ao limpar recursos: {e}")
        finally:
            logging.info("Dahora App encerrado completamente")


if __name__ == '__main__':
    main()





