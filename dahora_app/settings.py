"""
Gerenciamento de configurações persistentes
"""
import json
import logging
import re
from threading import Lock
from typing import Dict, Any
from dahora_app.constants import SETTINGS_FILE
from dahora_app.utils import atomic_write_json


class SettingsManager:
    """Gerenciador de configurações do aplicativo"""
    
    def __init__(self):
        """Inicializa o gerenciador de settings"""
        self.settings_lock = Lock()
        self.date_prefix = ""
        
        # Configurações avançadas
        self.hotkey_copy_datetime = "ctrl+shift+q"
        self.hotkey_refresh_menu = "ctrl+shift+r"
        self.max_history_items = 100
        self.clipboard_monitor_interval = 3
        self.clipboard_idle_threshold = 30
        self.datetime_format = "%d.%m.%Y-%H:%M"
        self.notification_duration = 2
        self.notification_enabled = True
    
    def validate_settings(self, settings_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida e sanitiza configurações carregadas
        
        Args:
            settings_dict: Dicionário com configurações brutas
            
        Returns:
            Dicionário com configurações validadas
        """
        try:
            # Valida prefix
            prefix = str(settings_dict.get("prefix", ""))
            if len(prefix) > 100:
                logging.warning("Prefixo muito longo, truncando para 100 chars")
                prefix = prefix[:100]
            prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
            
            # Valida hotkeys
            hotkey_copy = str(settings_dict.get("hotkey_copy_datetime", "ctrl+shift+q"))
            hotkey_refresh = str(settings_dict.get("hotkey_refresh_menu", "ctrl+shift+r"))
            
            # Valida max_history_items
            max_history = int(settings_dict.get("max_history_items", 100))
            if max_history < 10: max_history = 10
            if max_history > 1000: max_history = 1000
            
            # Valida intervalos
            monitor_interval = float(settings_dict.get("clipboard_monitor_interval", 3))
            if monitor_interval < 0.5: monitor_interval = 0.5
            if monitor_interval > 60: monitor_interval = 60
            
            idle_threshold = float(settings_dict.get("clipboard_idle_threshold", 30))
            if idle_threshold < 5: idle_threshold = 5
            if idle_threshold > 300: idle_threshold = 300
            
            # Valida formato de data/hora
            datetime_format = str(settings_dict.get("datetime_format", "%d.%m.%Y-%H:%M"))
            
            # Valida notificações
            notification_duration = int(settings_dict.get("notification_duration", 2))
            if notification_duration < 1: notification_duration = 1
            if notification_duration > 15: notification_duration = 15
            
            notification_enabled = bool(settings_dict.get("notification_enabled", True))
            
            return {
                "prefix": prefix,
                "hotkey_copy_datetime": hotkey_copy,
                "hotkey_refresh_menu": hotkey_refresh,
                "max_history_items": max_history,
                "clipboard_monitor_interval": monitor_interval,
                "clipboard_idle_threshold": idle_threshold,
                "datetime_format": datetime_format,
                "notification_duration": notification_duration,
                "notification_enabled": notification_enabled,
            }
        except Exception as e:
            logging.error(f"Erro ao validar settings: {e}")
            return {
                "prefix": "",
                "hotkey_copy_datetime": "ctrl+shift+q",
                "hotkey_refresh_menu": "ctrl+shift+r",
                "max_history_items": 100,
                "clipboard_monitor_interval": 3,
                "clipboard_idle_threshold": 30,
                "datetime_format": "%d.%m.%Y-%H:%M",
                "notification_duration": 2,
                "notification_enabled": True,
            }
    
    def load(self) -> None:
        """Carrega configurações do arquivo"""
        try:
            with self.settings_lock:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Valida configurações antes de aplicar
                validated = self.validate_settings(data)
                self.date_prefix = validated["prefix"]
                self.hotkey_copy_datetime = validated["hotkey_copy_datetime"]
                self.hotkey_refresh_menu = validated["hotkey_refresh_menu"]
                self.max_history_items = validated["max_history_items"]
                self.clipboard_monitor_interval = validated["clipboard_monitor_interval"]
                self.clipboard_idle_threshold = validated["clipboard_idle_threshold"]
                self.datetime_format = validated["datetime_format"]
                self.notification_duration = validated["notification_duration"]
                self.notification_enabled = validated["notification_enabled"]
        except FileNotFoundError:
            pass  # Usa padrões do __init__
        except json.JSONDecodeError as e:
            logging.error(f"Settings corrompido, usando padrão: {e}")
        except Exception as e:
            logging.warning(f"Falha ao carregar settings: {e}")
    
    def save(self) -> None:
        """Salva configurações no arquivo"""
        try:
            with self.settings_lock:
                atomic_write_json(SETTINGS_FILE, {
                    "prefix": self.date_prefix,
                    "hotkey_copy_datetime": self.hotkey_copy_datetime,
                    "hotkey_refresh_menu": self.hotkey_refresh_menu,
                    "max_history_items": self.max_history_items,
                    "clipboard_monitor_interval": self.clipboard_monitor_interval,
                    "clipboard_idle_threshold": self.clipboard_idle_threshold,
                    "datetime_format": self.datetime_format,
                    "notification_duration": self.notification_duration,
                    "notification_enabled": self.notification_enabled,
                })
        except Exception as e:
            logging.warning(f"Falha ao salvar settings: {e}")
    
    def get_prefix(self) -> str:
        """Retorna o prefixo atual"""
        return self.date_prefix
    
    def set_prefix(self, prefix: str) -> None:
        """Define novo prefixo e salva"""
        self.date_prefix = prefix.strip()
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Retorna todas as configurações"""
        return {
            "prefix": self.date_prefix,
            "hotkey_copy_datetime": self.hotkey_copy_datetime,
            "hotkey_refresh_menu": self.hotkey_refresh_menu,
            "max_history_items": self.max_history_items,
            "clipboard_monitor_interval": self.clipboard_monitor_interval,
            "clipboard_idle_threshold": self.clipboard_idle_threshold,
            "datetime_format": self.datetime_format,
            "notification_duration": self.notification_duration,
            "notification_enabled": self.notification_enabled,
        }
    
    def update_all(self, settings: Dict[str, Any]) -> None:
        """Atualiza todas as configurações de uma vez"""
        if "prefix" in settings:
            self.date_prefix = str(settings["prefix"]).strip()
        if "hotkey_copy_datetime" in settings:
            self.hotkey_copy_datetime = str(settings["hotkey_copy_datetime"])
        if "hotkey_refresh_menu" in settings:
            self.hotkey_refresh_menu = str(settings["hotkey_refresh_menu"])
        if "max_history_items" in settings:
            self.max_history_items = int(settings["max_history_items"])
        if "clipboard_monitor_interval" in settings:
            self.clipboard_monitor_interval = float(settings["clipboard_monitor_interval"])
        if "clipboard_idle_threshold" in settings:
            self.clipboard_idle_threshold = float(settings["clipboard_idle_threshold"])
        if "datetime_format" in settings:
            self.datetime_format = str(settings["datetime_format"])
        if "notification_duration" in settings:
            self.notification_duration = int(settings["notification_duration"])
        if "notification_enabled" in settings:
            self.notification_enabled = bool(settings["notification_enabled"])
        self.save()
