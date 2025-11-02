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


def generate_datetime_string():
    """Gera a data e hora no formato [DD.MM.AAAA-HH:MM]"""
    now = datetime.now()
    return f"[{now.strftime('%d.%m.%Y-%H:%M')}]"


def show_toast_notification(title, message, duration=2):
    """Mostra notificação toast do Windows - APENAS toast, sem MessageBox"""
    def _show_notification():
        # Método 1: winotify (toast nativo) - dura especificada
        if TOAST_AVAILABLE:
            try:
                toast = Notification(
                    app_id="Dahora App",
                    title=title,
                    msg=message,
                    duration=str(duration)
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


def copy_datetime(icon=None, item=None):
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
        source = "Atalho" if icon else "Fallback"

    # Mostra mensagem com contador (sem repetir atalho para menu)
    if source.startswith("Menu:"):
        show_toast_notification("Dahora App", f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {counter}ª vez")
    else:
        show_toast_notification("Dahora App", f"Copiado com sucesso via {source}!\n{dt_string}\nTotal: {counter}ª vez")


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

# Variável para controlar último clique esquerdo
last_click_time = 0
click_threshold = 0.5  # 500ms para considerar como clique duplo

# Variável global para contador de acionamentos
counter_file = "dahora_counter.txt"
counter = 0

# Variável global para histórico de clipboard
history_file = "clipboard_history.json"
clipboard_history = []
MAX_HISTORY_ITEMS = 100

# Variável para monitoramento de clipboard
last_clipboard_content = ""

def load_counter():
    """Carrega o contador do arquivo ou inicia com 0"""
    global counter
    try:
        with open(counter_file, "r", encoding="utf-8") as f:
            counter = int(f.read().strip())
    except:
        counter = 0

def save_counter():
    """Salva o contador no arquivo"""
    try:
        with open(counter_file, "w", encoding="utf-8") as f:
            f.write(str(counter))
    except:
        pass

def increment_counter():
    """Incrementa o contador e salva"""
    global counter
    counter += 1
    save_counter()


# Funções de histórico de clipboard
def load_clipboard_history():
    """Carrega o histórico do arquivo ou inicia com lista vazia"""
    global clipboard_history
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            clipboard_history = json.load(f)
            # Limita ao máximo de itens
            if len(clipboard_history) > MAX_HISTORY_ITEMS:
                clipboard_history = clipboard_history[-MAX_HISTORY_ITEMS:]
    except:
        clipboard_history = []

def save_clipboard_history():
    """Salva o histórico no arquivo"""
    try:
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(clipboard_history, f, ensure_ascii=False, indent=2)
    except:
        pass

def add_to_clipboard_history(text):
    """Adiciona um item ao histórico"""
    global clipboard_history
    if not text.strip():  # Ignora texto vazio ou apenas espaços
        return

    # Verifica se o item já existe para evitar duplicatas
    for item in clipboard_history:
        if item.get("text") == text:
            return

    # Adiciona novo item com timestamp
    new_item = {
        "text": text,
        "timestamp": datetime.now().isoformat(),
        "app": "Dahora App"
    }

    clipboard_history.append(new_item)

    # Limita ao máximo de itens
    if len(clipboard_history) > MAX_HISTORY_ITEMS:
        clipboard_history = clipboard_history[-MAX_HISTORY_ITEMS:]

    save_clipboard_history()

def clear_clipboard_history():
    """Limpa todo o histórico"""
    global clipboard_history
    total_items = len(clipboard_history)
    clipboard_history = []
    save_clipboard_history()

    # Mostra notificação de confirmação
    show_toast_notification("Dahora App", f"Histórico limpo!\n{total_items} itens removidos")

def get_recent_clipboard_items(limit=10):
    """Retorna os itens mais recentes do histórico"""
    return clipboard_history[-limit:] if clipboard_history else []

def monitor_clipboard():
    """Monitora as mudanças na clipboard"""
    global last_clipboard_content

    while True:
        try:
            current_content = pyperclip.paste()

            if current_content != last_clipboard_content and current_content.strip():
                # Adiciona ao histórico
                add_to_clipboard_history(current_content)
                last_clipboard_content = current_content

        except Exception:
            pass

        # Espera 2 segundos antes de verificar novamente
        time.sleep(2)

def copy_from_history(text):
    """Copia um item do histórico para a clipboard"""
    pyperclip.copy(text)
    # Incrementa o contador principal
    increment_counter()
    # Mostra notificação
    show_toast_notification("Dahora App", f"Copiado do histórico!\n{text}\nTotal: {counter}ª vez")

def show_about(icon, item):
    """Mostra informações sobre o aplicativo"""
    about_text = (
        "Dahora App v1.0\n\n"
        "Aplicativo para copiar data e hora\n"
        "Formato: [DD.MM.AAAA-HH:MM]\n\n"
        f"Total de acionamentos: {counter} vezes\n"
        f"Histórico de clipboard: {len(clipboard_history)} itens\n\n"
        "Atalho: Ctrl+Shift+Q\n\n"
        "Menu de opções via clique direito\n\n"
        "Histórico mantém últimos 100 itens\n"
        "Monitora automaticamente clipboard\n"
        "Clique em itens do histórico para copiar"
    )
    # Mostra toast modal (dura 10 segundos para permitir leitura)
    show_toast_notification("Sobre - Dahora App", about_text, duration=10)


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
    copy_datetime()


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


def setup_icon():
    """Configura o ícone da bandeja do sistema"""
    global global_icon, last_click_time

    # Cria submenu para histórico de clipboard
    history_items = get_recent_clipboard_items(5)  # Mostra últimos 5 itens
    history_menu = pystray.Menu()

    for i, item in enumerate(history_items):
        # Limita o texto do menu para não ficar muito longo
        display_text = item.get("text", "")[:40] + "..." if len(item.get("text", "")) > 40 else item.get("text", "")
        history_menu.add(pystray.MenuItem(f"[{len(history_items)-i}] {display_text}",
                                         lambda item=item: copy_from_history(item.get("text", ""))))

    # Se não houver histórico, mostra mensagem desativada
    if not history_items:
        history_menu.add(pystray.MenuItem("Nenhum item no histórico", lambda: None))

    menu = pystray.Menu(
        pystray.MenuItem('Copiar Data/Hora (Ctrl+Shift+Q)', copy_datetime),
        pystray.MenuItem('Histórico de Clipboard', history_menu),
        pystray.MenuItem('Limpar Histórico', clear_clipboard_history),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Sobre', show_about),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Sair', on_exit)
    )

    image = create_image()

    # Handler para clique esquerdo - detecta clique duplo
    def on_left_click(icon, item):
        global last_click_time
        current_time = time.time()

        # Verifica se é um clique duplo
        if current_time - last_click_time < click_threshold:
            # Clique duplo: copia data/hora
            copy_datetime(icon, item)
            # Reseta o tempo do último clique
            last_click_time = 0
        else:
            # Clique simples: mostra instruções
            show_toast_notification("Dahora App", "Menu de opções disponível\nClique com o botão direito no ícone")
            # Registra o tempo do clique
            last_click_time = current_time

    icon = pystray.Icon(
        "Dahora App",
        image,
        "Dahora App - Clique esquerdo: instruções\nClique duplo: copiar data/hora\nClique direito: menu completo\nAtalho: Ctrl+Shift+Q",
        menu,
        default_action=copy_datetime  # Fallback: copiar se não conseguir abrir menu
    )

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
            # Mostra notificação imediatamente usando thread
            notification_thread = threading.Thread(
                target=show_toast_notification,
                args=("Dahora App Já em Execução",
                      "O Dahora App já está rodando na bandeja do sistema!"),
                daemon=False
            )
            notification_thread.start()

            # Espera a notificação ser exibida
            notification_thread.join(timeout=3.0)  # Espera até 3 segundos

            return False

        # Se criamos o mutex com sucesso, mantém aberto enquanto o app roda
        return True

    except Exception as e:
        print(f"Erro na verificação de instância única: {e}")
        # Se falhar, permite continuar (melhor ter múltiplas instâncias do que bloquear)
        return True



def main():
    """Função principal"""
    global mutex_handle

    # Cria o arquivo de ícone para o executável (se não existir)
    try:
        import os
        if not os.path.exists('icon.ico'):
            # Se Python estiver disponível, tenta criar o ícone
            try:
                from PIL import Image, ImageDraw
                icon_image = create_image()
                icon_image.save('icon.ico', format='ICO')
                print("✅ Arquivo icon.ico criado com sucesso!")
            except Exception:
                print("⚠️  Não foi possível criar o arquivo icon.ico")
    except:
        pass

    # Carrega o contador e o histórico ao iniciar
    load_counter()
    load_clipboard_history()

    # Verifica se já existe uma instância rodando
    if not check_single_instance():
        sys.exit(0)

    try:
        # Configura a hotkey em uma thread separada
        hotkey_thread = threading.Thread(target=setup_hotkey_listener, daemon=True)
        hotkey_thread.start()

        # Inicia o monitoramento de clipboard em uma thread separada
        monitor_thread = threading.Thread(target=monitor_clipboard, daemon=True)
        monitor_thread.start()

        # Inicia o ícone da bandeja
        icon = setup_icon()

        # Mostra mensagem de boas-vindas com contador atual
        total_history = len(clipboard_history)
        show_toast_notification("Dahora App", f"App iniciado com sucesso!\nClique duplo: Ctrl+Shift+Q\nJá acionado {counter} vezes\nHistórico: {total_history} itens")

        # Executa o ícone (bloqueia até fechar)
        icon.run()

    except KeyboardInterrupt:
        print("Dahora App encerrado pelo usuário")
    except Exception as e:
        print(f"Erro inesperado: {e}")
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

