"""
Gerenciamento de configurações persistentes
"""
import json
import logging
import re
import os
import shutil
from datetime import datetime
from threading import RLock
from typing import Dict, Any, List, Optional, Tuple
from dahora_app.constants import SETTINGS_FILE
from dahora_app.utils import atomic_write_json


class SettingsManager:
    """Gerenciador de configurações do aplicativo"""
    
    def __init__(self):
        """Inicializa o gerenciador de configurações"""
        self.settings_lock = RLock()  # RLock permite reentrada na mesma thread
        self.date_prefix = ""
        
        # Configurações avançadas
        self.hotkey_copy_datetime = "ctrl+shift+q"
        self.hotkey_search_history = "ctrl+shift+f"
        self.hotkey_refresh_menu = "ctrl+shift+r"
        self.max_history_items = 100
        self.clipboard_monitor_interval = 3
        self.clipboard_idle_threshold = 30
        self.datetime_format = "%d.%m.%Y-%H:%M"
        self.notification_duration = 2
        self.notification_enabled = True
        
        # Caracteres de delimitação configuráveis
        self.bracket_open = "["
        self.bracket_close = "]"
        
        # Múltiplos atalhos personalizados (NOVO)
        self.custom_shortcuts: List[Dict[str, Any]] = []
        self.max_custom_shortcuts = 10
        self.next_shortcut_id = 1

        # Atalho padrão (entre os custom_shortcuts) usado como "principal" do app
        # Ex: ação de copiar/colar timestamp (Ctrl+Shift+Q por padrão)
        self.default_shortcut_id: Optional[int] = None
    
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
            hotkey_search = str(settings_dict.get("hotkey_search_history", "ctrl+shift+f"))
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
            
            # Valida brackets configuráveis
            bracket_open = str(settings_dict.get("bracket_open", "["))[:5]  # Max 5 chars
            bracket_close = str(settings_dict.get("bracket_close", "]"))[:5]  # Max 5 chars
            
            # Valida custom_shortcuts (NOVO)
            custom_shortcuts = self._validate_custom_shortcuts(
                settings_dict.get("custom_shortcuts", [])
            )

            # Atalho padrão (pode não existir em versões antigas)
            default_shortcut_id_raw = settings_dict.get("default_shortcut_id", None)
            default_shortcut_id: Optional[int] = None
            try:
                if default_shortcut_id_raw is not None and str(default_shortcut_id_raw).strip() != "":
                    default_shortcut_id = int(default_shortcut_id_raw)
            except Exception:
                default_shortcut_id = None

            # Se não definido, tenta escolher um padrão coerente
            if default_shortcut_id is None and custom_shortcuts:
                enabled = [s for s in custom_shortcuts if s.get("enabled", True)]
                pick = (enabled[0] if enabled else custom_shortcuts[0])
                default_shortcut_id = int(pick.get("id"))

            # Se definido mas não existe, re-seleciona
            if default_shortcut_id is not None:
                ids = {int(s.get("id")) for s in custom_shortcuts}
                if default_shortcut_id not in ids:
                    enabled = [s for s in custom_shortcuts if s.get("enabled", True)]
                    pick = (enabled[0] if enabled else (custom_shortcuts[0] if custom_shortcuts else None))
                    default_shortcut_id = int(pick.get("id")) if pick else None
            
            return {
                "prefix": prefix,
                "hotkey_copy_datetime": hotkey_copy,
                "hotkey_search_history": hotkey_search,
                "hotkey_refresh_menu": hotkey_refresh,
                "max_history_items": max_history,
                "clipboard_monitor_interval": monitor_interval,
                "clipboard_idle_threshold": idle_threshold,
                "datetime_format": datetime_format,
                "notification_duration": notification_duration,
                "notification_enabled": notification_enabled,
                "bracket_open": bracket_open,
                "bracket_close": bracket_close,
                "custom_shortcuts": custom_shortcuts,
                "default_shortcut_id": default_shortcut_id,
            }
        except Exception as e:
            logging.error(f"Erro ao validar settings: {e}")
            return {
                "prefix": "",
                "hotkey_copy_datetime": "ctrl+shift+q",
                "hotkey_search_history": "ctrl+shift+f",
                "hotkey_refresh_menu": "ctrl+shift+r",
                "max_history_items": 100,
                "clipboard_monitor_interval": 3,
                "clipboard_idle_threshold": 30,
                "datetime_format": "%d.%m.%Y-%H:%M",
                "notification_duration": 2,
                "notification_enabled": True,
                "bracket_open": "[",
                "bracket_close": "]",
                "custom_shortcuts": [],
                "default_shortcut_id": None,
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
                self.hotkey_search_history = validated.get("hotkey_search_history", "ctrl+shift+f")
                self.hotkey_refresh_menu = validated["hotkey_refresh_menu"]
                self.max_history_items = validated["max_history_items"]
                self.clipboard_monitor_interval = validated["clipboard_monitor_interval"]
                self.clipboard_idle_threshold = validated["clipboard_idle_threshold"]
                self.datetime_format = validated["datetime_format"]
                self.notification_duration = validated["notification_duration"]
                self.notification_enabled = validated["notification_enabled"]
                self.bracket_open = validated.get("bracket_open", "[")
                self.bracket_close = validated.get("bracket_close", "]")
                self.custom_shortcuts = validated.get("custom_shortcuts", [])
                self.default_shortcut_id = validated.get("default_shortcut_id", None)

                # Migração automática do prefixo legado para custom shortcuts (necessário para retrocompatibilidade)
                self._migrate_legacy_prefix_if_needed(data)

                # Garante que o default_shortcut_id ainda é válido após migração
                if self.custom_shortcuts:
                    ids = {int(s.get("id")) for s in self.custom_shortcuts}
                    if self.default_shortcut_id not in ids:
                        enabled = [s for s in self.custom_shortcuts if s.get("enabled", True)]
                        pick = (enabled[0] if enabled else self.custom_shortcuts[0])
                        self.default_shortcut_id = int(pick.get("id"))
                        self.save()
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
                    "hotkey_search_history": self.hotkey_search_history,
                    "hotkey_refresh_menu": self.hotkey_refresh_menu,
                    "max_history_items": self.max_history_items,
                    "clipboard_monitor_interval": self.clipboard_monitor_interval,
                    "clipboard_idle_threshold": self.clipboard_idle_threshold,
                    "datetime_format": self.datetime_format,
                    "bracket_open": self.bracket_open,
                    "bracket_close": self.bracket_close,
                    "notification_duration": self.notification_duration,
                    "notification_enabled": self.notification_enabled,
                    "custom_shortcuts": self.custom_shortcuts,
                    "default_shortcut_id": self.default_shortcut_id,
                })
        except Exception as e:
            logging.error(f"Erro ao salvar configurações: {e}")
    
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
            "hotkey_search_history": self.hotkey_search_history,
            "hotkey_refresh_menu": self.hotkey_refresh_menu,
            "max_history_items": self.max_history_items,
            "clipboard_monitor_interval": self.clipboard_monitor_interval,
            "clipboard_idle_threshold": self.clipboard_idle_threshold,
            "datetime_format": self.datetime_format,
            "bracket_open": self.bracket_open,
            "bracket_close": self.bracket_close,
            "notification_duration": self.notification_duration,
            "notification_enabled": self.notification_enabled,
            "custom_shortcuts": self.custom_shortcuts,
            "default_shortcut_id": self.default_shortcut_id,
        }
    
    def update_all(self, settings: Dict[str, Any]) -> None:
        """Atualiza todas as configurações de uma vez"""
        if "prefix" in settings:
            self.date_prefix = str(settings["prefix"]).strip()
        if "hotkey_copy_datetime" in settings:
            self.hotkey_copy_datetime = str(settings["hotkey_copy_datetime"])
        if "hotkey_search_history" in settings:
            self.hotkey_search_history = str(settings["hotkey_search_history"])
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
        if "bracket_open" in settings:
            self.bracket_open = str(settings["bracket_open"])[:5]
        if "bracket_close" in settings:
            self.bracket_close = str(settings["bracket_close"])[:5]
        if "notification_duration" in settings:
            self.notification_duration = int(settings["notification_duration"])
        if "notification_enabled" in settings:
            self.notification_enabled = bool(settings["notification_enabled"])
        if "custom_shortcuts" in settings:
            self.custom_shortcuts = self._validate_custom_shortcuts(settings["custom_shortcuts"])
        if "default_shortcut_id" in settings:
            try:
                raw = settings.get("default_shortcut_id", None)
                if raw is None or str(raw).strip() == "":
                    self.default_shortcut_id = None
                else:
                    self.default_shortcut_id = int(raw)
            except Exception:
                self.default_shortcut_id = None
        self.save()
    
    # ========== MÉTODOS PARA CUSTOM SHORTCUTS (NOVO) ==========
    
    def _validate_custom_shortcuts(self, shortcuts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Valida lista de custom shortcuts"""
        validated = []
        seen_ids = set()
        seen_hotkeys = set()
        
        for shortcut in shortcuts:
            try:
                # Valida estrutura
                if not isinstance(shortcut, dict):
                    continue
                
                # Valida campos obrigatórios
                shortcut_id = int(shortcut.get("id", 0))
                hotkey = str(shortcut.get("hotkey", "")).strip().lower()
                prefix = str(shortcut.get("prefix", "")).strip()
                
                if not hotkey or not prefix:
                    continue
                
                # Valida duplicatas
                if shortcut_id in seen_ids or hotkey in seen_hotkeys:
                    logging.warning(f"Shortcut duplicado ignorado: ID={shortcut_id}, hotkey={hotkey}")
                    continue
                
                # Valida tamanho do prefixo
                if len(prefix) > 50:
                    prefix = prefix[:50]
                    logging.warning(f"Prefixo truncado para 50 chars: {prefix}")
                
                # Sanitiza prefixo
                prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
                
                # Adiciona à lista validada
                validated.append({
                    "id": shortcut_id,
                    "hotkey": hotkey,
                    "prefix": prefix,
                    "enabled": bool(shortcut.get("enabled", True)),
                    "description": str(shortcut.get("description", ""))[:100],
                })
                
                seen_ids.add(shortcut_id)
                seen_hotkeys.add(hotkey)
                
                # Atualiza next_shortcut_id
                if shortcut_id >= self.next_shortcut_id:
                    self.next_shortcut_id = shortcut_id + 1
            
            except Exception as e:
                logging.warning(f"Erro ao validar shortcut: {e}")
                continue
        
        return validated
    
    def _migrate_legacy_prefix_if_needed(self, data: Dict[str, Any]) -> None:
        """Migra prefixo legado para custom shortcuts se necessário"""
        try:
            # Se já tem custom_shortcuts, não precisa migrar
            if data.get("custom_shortcuts"):
                logging.info(f"Custom shortcuts já configurados: {len(data['custom_shortcuts'])} encontrados")
                return
            
            # Se tem prefixo legado e não tem custom shortcuts, migra
            legacy_prefix = data.get("prefix", "")
            if legacy_prefix and legacy_prefix.strip():
                logging.info(f"Migrando prefixo legado '{legacy_prefix}' para custom shortcuts")
                
                # Cria primeiro custom shortcut com prefixo legado
                migrated_shortcut = {
                    "id": 1,
                    "hotkey": "ctrl+shift+1",
                    "prefix": legacy_prefix.strip(),
                    "enabled": True,
                    "description": "Prefixo migrado automaticamente",
                }
                
                self.custom_shortcuts = [migrated_shortcut]
                self.next_shortcut_id = 2

                # Usa o primeiro atalho como padrão do app
                self.default_shortcut_id = 1
                
                # Salva migração
                self.save()
                logging.info("Migração de prefixo legado concluída com sucesso")
        
        except Exception as e:
            logging.error(f"Erro na migração de prefixo legado: {e}")
    
    def add_custom_shortcut(self, hotkey: str, prefix: str, 
                          description: str = "", enabled: bool = True) -> Tuple[bool, str, Optional[int]]:
        """Adiciona novo custom shortcut"""
        try:
            with self.settings_lock:
                # Verifica limite
                if len(self.custom_shortcuts) >= self.max_custom_shortcuts:
                    return False, f"Limite de {self.max_custom_shortcuts} atalhos atingido", None
                
                # Normaliza
                hotkey = hotkey.strip().lower()
                prefix = prefix.strip()
                
                if not hotkey or not prefix:
                    return False, "Hotkey e prefixo são obrigatórios", None
                
                # Verifica hotkeys reservados
                reserved = [
                    "ctrl+c", "ctrl+v", "ctrl+x", "ctrl+a", "ctrl+z",
                    "ctrl+shift+q", "ctrl+shift+r", "ctrl+shift+f",
                ]
                if hotkey in reserved:
                    return False, f"Hotkey '{hotkey}' é reservado pelo sistema", None
                
                # Verifica duplicatas
                for shortcut in self.custom_shortcuts:
                    if shortcut["hotkey"] == hotkey:
                        return False, f"Hotkey '{hotkey}' já está em uso", None
                
                # Valida e sanitiza
                if len(prefix) > 50:
                    prefix = prefix[:50]
                prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
                description = str(description)[:100]
                
                # Cria e adiciona
                new_shortcut = {
                    "id": self.next_shortcut_id,
                    "hotkey": hotkey,
                    "prefix": prefix,
                    "enabled": enabled,
                    "description": description,
                }
                
                self.custom_shortcuts.append(new_shortcut)
                self.next_shortcut_id += 1
                self.save()
                
                logging.info(f"Atalho adicionado: {hotkey} → {prefix}")
                return True, "Atalho adicionado com sucesso", new_shortcut["id"]
        
        except Exception as e:
            logging.error(f"Erro ao adicionar custom shortcut: {e}")
            return False, f"Erro ao adicionar: {str(e)}", None
    
    def remove_custom_shortcut(self, shortcut_id: int) -> Tuple[bool, str]:
        """Remove custom shortcut por ID
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            with self.settings_lock:
                for i, shortcut in enumerate(self.custom_shortcuts):
                    if shortcut["id"] == shortcut_id:
                        removed = self.custom_shortcuts.pop(i)
                        self.save()
                        logging.info(f"Custom shortcut removido: ID={shortcut_id}, hotkey={removed['hotkey']}")
                        return True, "Atalho removido com sucesso"
                
                return False, f"Atalho com ID {shortcut_id} não encontrado"
        
        except Exception as e:
            logging.error(f"Erro ao remover custom shortcut: {e}")
            return False, f"Erro ao remover: {str(e)}"
    
    def update_custom_shortcut(self, shortcut_id: int, 
                             hotkey: Optional[str] = None,
                             prefix: Optional[str] = None,
                             description: Optional[str] = None,
                             enabled: Optional[bool] = None) -> Tuple[bool, str]:
        """Atualiza custom shortcut existente
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            with self.settings_lock:
                # Encontra shortcut
                shortcut = None
                for s in self.custom_shortcuts:
                    if s["id"] == shortcut_id:
                        shortcut = s
                        break
                
                if not shortcut:
                    return False, f"Atalho com ID {shortcut_id} não encontrado"
                
                # Atualiza campos
                if hotkey is not None:
                    hotkey = hotkey.strip().lower()
                    
                    # Verifica hotkeys reservados (apenas clipboard básicos)
                    reserved = [
                        "ctrl+c", "ctrl+v", "ctrl+x", "ctrl+a", "ctrl+z",
                        "ctrl+shift+q", "ctrl+shift+r", "ctrl+shift+f",
                    ]
                    if hotkey in reserved:
                        return False, f"Hotkey '{hotkey}' é reservado pelo sistema"
                    
                    # Verifica duplicatas (exceto o próprio)
                    for s in self.custom_shortcuts:
                        if s["id"] != shortcut_id and s["hotkey"] == hotkey:
                            return False, f"Hotkey '{hotkey}' já está em uso"
                    
                    shortcut["hotkey"] = hotkey
                
                if prefix is not None:
                    prefix = prefix.strip()
                    if len(prefix) > 50:
                        prefix = prefix[:50]
                    prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
                    shortcut["prefix"] = prefix
                
                if description is not None:
                    shortcut["description"] = str(description)[:100]
                
                if enabled is not None:
                    shortcut["enabled"] = bool(enabled)
                
                self.save()
                logging.info(f"Custom shortcut atualizado: ID={shortcut_id}")
                return True, "Atalho atualizado com sucesso"
        
        except Exception as e:
            logging.error(f"Erro ao atualizar custom shortcut: {e}")
            return False, f"Erro ao atualizar: {str(e)}"
    
    def get_custom_shortcuts(self, enabled_only: bool = False) -> List[Dict[str, Any]]:
        """Retorna lista de custom shortcuts
        
        Args:
            enabled_only: Se True, retorna apenas shortcuts habilitados
        
        Returns:
            Lista de custom shortcuts
        """
        if enabled_only:
            return [s for s in self.custom_shortcuts if s.get("enabled", True)]
        return self.custom_shortcuts.copy()
    
    def get_custom_shortcut_by_id(self, shortcut_id: int) -> Optional[Dict[str, Any]]:
        """Retorna custom shortcut por ID"""
        for shortcut in self.custom_shortcuts:
            if shortcut["id"] == shortcut_id:
                return shortcut.copy()
        return None
    
    def get_custom_shortcut_by_hotkey(self, hotkey: str) -> Optional[Dict[str, Any]]:
        """Retorna custom shortcut por hotkey"""
        hotkey = hotkey.strip().lower()
        for shortcut in self.custom_shortcuts:
            if shortcut["hotkey"] == hotkey:
                return shortcut.copy()
        return None
