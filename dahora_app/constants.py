"""
Constantes e configurações globais do Dahora App
"""
import os

# Informações do aplicativo
APP_NAME = "DahoraApp"
APP_VERSION = "0.2.7"
APP_TITLE = "Dahora App - Sistema de Timestamp"

# Diretório de dados do usuário
def get_data_dir() -> str:
    """Retorna o diretório de dados do aplicativo"""
    base = os.getenv('APPDATA') or os.path.expanduser("~")
    path = os.path.join(base, APP_NAME)
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass
    return path

DATA_DIR = get_data_dir()

# Arquivos de dados
COUNTER_FILE = os.path.join(DATA_DIR, "dahora_counter.txt")
HISTORY_FILE = os.path.join(DATA_DIR, "clipboard_history.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
LOG_FILE = os.path.join(DATA_DIR, "dahora.log")
PRIVACY_MARKER_FILE = os.path.join(DATA_DIR, ".privacy_accepted")

# Configurações de histórico
MAX_HISTORY_ITEMS = 100
DEFAULT_MAX_HISTORY_ITEMS = 100

# Configurações de hotkeys
HOTKEY_COPY_DATETIME = 'ctrl+shift+q'
HOTKEY_REFRESH_MENU = 'ctrl+shift+r'
HOTKEY_CTRL_C = 'ctrl+c'
DEFAULT_HOTKEY_COPY_DATETIME = 'ctrl+shift+q'
DEFAULT_HOTKEY_REFRESH_MENU = 'ctrl+shift+r'

# Configurações de log
LOG_MAX_BYTES = 1 * 1024 * 1024  # 1MB
LOG_BACKUP_COUNT = 1

# Configurações de monitoramento de clipboard
CLIPBOARD_MONITOR_INTERVAL = 3  # segundos
CLIPBOARD_IDLE_THRESHOLD = 30  # segundos sem atividade
DEFAULT_CLIPBOARD_MONITOR_INTERVAL = 3
DEFAULT_CLIPBOARD_IDLE_THRESHOLD = 30

# Formato de data/hora
DATETIME_FORMAT = '%d.%m.%Y-%H:%M'
DEFAULT_DATETIME_FORMAT = '%d.%m.%Y-%H:%M'

# Configurações de notificação
DEFAULT_NOTIFICATION_DURATION = 2  # segundos
DEFAULT_NOTIFICATION_ENABLED = True
