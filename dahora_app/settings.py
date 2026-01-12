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
from dahora_app.schemas import SettingsSchema
from pydantic import ValidationError


def _parse_int(value: Any) -> Optional[int]:
    try:
        if value is None:
            return None
        s = str(value).strip()
        if s == "":
            return None
        return int(s)
    except Exception:
        return None


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

        self.log_max_bytes = 1 * 1024 * 1024
        self.log_backup_count = 1
        self.ui_prewarm_delay_ms = 700
        self.tray_menu_cache_window_ms = 200

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
        Valida e sanitiza configurações carregadas usando Pydantic schemas.

        Usa apenas Pydantic para validação (sem fallback manual).
        Se falhar, retorna configurações padrão.

        Args:
            settings_dict: Dicionário com configurações brutas

        Returns:
            Dicionário com configurações validadas
        """
        try:
            # Validação com Pydantic (única fonte de verdade)
            schema = SettingsSchema(
                prefix=settings_dict.get("prefix", ""),
                hotkey_copy_datetime=settings_dict.get(
                    "hotkey_copy_datetime", "ctrl+shift+q"
                ),
                hotkey_search_history=settings_dict.get(
                    "hotkey_search_history", "ctrl+shift+f"
                ),
                hotkey_refresh_menu=settings_dict.get(
                    "hotkey_refresh_menu", "ctrl+shift+r"
                ),
                max_history_items=settings_dict.get("max_history_items", 100),
                clipboard_monitor_interval=settings_dict.get(
                    "clipboard_monitor_interval", 3.0
                ),
                clipboard_idle_threshold=settings_dict.get(
                    "clipboard_idle_threshold", 30
                ),
                datetime_format=settings_dict.get("datetime_format", "%d.%m.%Y-%H:%M"),
                bracket_open=settings_dict.get("bracket_open", "["),
                bracket_close=settings_dict.get("bracket_close", "]"),
                notification_duration=settings_dict.get("notification_duration", 2),
                notification_enabled=settings_dict.get("notification_enabled", True),
                log_max_bytes=settings_dict.get("log_max_bytes", 1 * 1024 * 1024),
                log_backup_count=settings_dict.get("log_backup_count", 1),
                ui_prewarm_delay_ms=settings_dict.get("ui_prewarm_delay_ms", 700),
                tray_menu_cache_window_ms=settings_dict.get(
                    "tray_menu_cache_window_ms", 200
                ),
                custom_shortcuts=settings_dict.get("custom_shortcuts", []),
                default_shortcut_id=settings_dict.get("default_shortcut_id", None),
            )

            # Converte schema validado para dict
            return {
                "prefix": schema.prefix,
                "hotkey_copy_datetime": schema.hotkey_copy_datetime,
                "hotkey_search_history": schema.hotkey_search_history,
                "hotkey_refresh_menu": schema.hotkey_refresh_menu,
                "max_history_items": schema.max_history_items,
                "clipboard_monitor_interval": schema.clipboard_monitor_interval,
                "clipboard_idle_threshold": schema.clipboard_idle_threshold,
                "datetime_format": schema.datetime_format,
                "notification_duration": schema.notification_duration,
                "notification_enabled": schema.notification_enabled,
                "log_max_bytes": schema.log_max_bytes,
                "log_backup_count": schema.log_backup_count,
                "ui_prewarm_delay_ms": schema.ui_prewarm_delay_ms,
                "tray_menu_cache_window_ms": schema.tray_menu_cache_window_ms,
                "bracket_open": schema.bracket_open,
                "bracket_close": schema.bracket_close,
                "custom_shortcuts": [s.model_dump() for s in schema.custom_shortcuts],
                "default_shortcut_id": schema.default_shortcut_id,
            }

        except ValidationError as e:
            # Validação Pydantic falhou - usa defaults em vez de fallback manual
            logging.warning(f"Validação Pydantic falhou, usando defaults: {e}")
            return self._get_default_settings()

        except Exception as e:
            logging.error(f"Erro ao validar settings: {e}")
            return self._get_default_settings()

    def _get_default_settings(self) -> Dict[str, Any]:
        """Retorna configurações padrão"""
        return {
            "prefix": "",
            "hotkey_copy_datetime": "ctrl+shift+q",
            "hotkey_search_history": "ctrl+shift+f",
            "hotkey_refresh_menu": "ctrl+shift+r",
            "max_history_items": 100,
            "clipboard_monitor_interval": 3.0,
            "clipboard_idle_threshold": 30,
            "datetime_format": "%d.%m.%Y-%H:%M",
            "notification_duration": 2,
            "notification_enabled": True,
            "log_max_bytes": 1 * 1024 * 1024,
            "log_backup_count": 1,
            "ui_prewarm_delay_ms": 700,
            "tray_menu_cache_window_ms": 200,
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
                self.hotkey_search_history = validated.get(
                    "hotkey_search_history", "ctrl+shift+f"
                )
                self.hotkey_refresh_menu = validated["hotkey_refresh_menu"]
                self.max_history_items = validated["max_history_items"]
                self.clipboard_monitor_interval = validated[
                    "clipboard_monitor_interval"
                ]
                self.clipboard_idle_threshold = validated["clipboard_idle_threshold"]
                self.datetime_format = validated["datetime_format"]
                self.notification_duration = validated["notification_duration"]
                self.notification_enabled = validated["notification_enabled"]
                self.log_max_bytes = validated.get("log_max_bytes", 1 * 1024 * 1024)
                self.log_backup_count = validated.get("log_backup_count", 1)
                self.ui_prewarm_delay_ms = validated.get("ui_prewarm_delay_ms", 700)
                self.tray_menu_cache_window_ms = validated.get(
                    "tray_menu_cache_window_ms", 200
                )
                self.bracket_open = validated.get("bracket_open", "[")
                self.bracket_close = validated.get("bracket_close", "]")
                self.custom_shortcuts = validated.get("custom_shortcuts", [])
                self.default_shortcut_id = validated.get("default_shortcut_id", None)

                # Migração automática do prefixo legado para custom shortcuts (necessário para retrocompatibilidade)
                self._migrate_legacy_prefix_if_needed(data)

                # Garante que o default_shortcut_id ainda é válido após migração
                if self.custom_shortcuts:
                    ids = {
                        i
                        for s in self.custom_shortcuts
                        for i in [_parse_int(s.get("id"))]
                        if i is not None
                    }
                    if self.default_shortcut_id not in ids:
                        enabled = [
                            s for s in self.custom_shortcuts if s.get("enabled", True)
                        ]
                        pick = enabled[0] if enabled else self.custom_shortcuts[0]
                        picked_id = _parse_int(pick.get("id"))
                        if picked_id is not None:
                            self.default_shortcut_id = picked_id
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
                atomic_write_json(
                    SETTINGS_FILE,
                    {
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
                        "log_max_bytes": self.log_max_bytes,
                        "log_backup_count": self.log_backup_count,
                        "ui_prewarm_delay_ms": self.ui_prewarm_delay_ms,
                        "tray_menu_cache_window_ms": self.tray_menu_cache_window_ms,
                        "custom_shortcuts": self.custom_shortcuts,
                        "default_shortcut_id": self.default_shortcut_id,
                    },
                )
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
            "log_max_bytes": self.log_max_bytes,
            "log_backup_count": self.log_backup_count,
            "ui_prewarm_delay_ms": self.ui_prewarm_delay_ms,
            "tray_menu_cache_window_ms": self.tray_menu_cache_window_ms,
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
            try:
                max_items = int(settings["max_history_items"])
                if max_items < 10:
                    max_items = 10
                if max_items > 1000:
                    max_items = 1000
                self.max_history_items = max_items
            except Exception:
                pass
        if "clipboard_monitor_interval" in settings:
            try:
                monitor_interval = float(settings["clipboard_monitor_interval"])
                if monitor_interval < 0.5:
                    monitor_interval = 0.5
                if monitor_interval > 60.0:
                    monitor_interval = 60.0
                self.clipboard_monitor_interval = monitor_interval
            except Exception:
                pass
        if "clipboard_idle_threshold" in settings:
            try:
                idle_threshold = float(settings["clipboard_idle_threshold"])
                if idle_threshold < 5.0:
                    idle_threshold = 5.0
                if idle_threshold > 300.0:
                    idle_threshold = 300.0
                self.clipboard_idle_threshold = int(idle_threshold)
            except Exception:
                pass
        if "datetime_format" in settings:
            self.datetime_format = str(settings["datetime_format"])
        bracket_open_candidate = None
        bracket_close_candidate = None
        if "bracket_open" in settings:
            bracket_open_candidate = str(settings["bracket_open"])
        if "bracket_close" in settings:
            bracket_close_candidate = str(settings["bracket_close"])
        if bracket_open_candidate is not None or bracket_close_candidate is not None:
            new_open = self.bracket_open
            new_close = self.bracket_close

            if bracket_open_candidate is not None:
                bracket_open_value = bracket_open_candidate.strip()
                if len(bracket_open_value) == 1 and bracket_open_value not in "\n\r\t":
                    new_open = bracket_open_value
            if bracket_close_candidate is not None:
                bracket_close_value = bracket_close_candidate.strip()
                if (
                    len(bracket_close_value) == 1
                    and bracket_close_value not in "\n\r\t"
                ):
                    new_close = bracket_close_value

            if new_open == new_close:
                if new_open != "]":
                    new_close = "]"
                else:
                    new_close = "["

            self.bracket_open = new_open
            self.bracket_close = new_close
        if "notification_duration" in settings:
            try:
                duration_seconds = int(settings["notification_duration"])
                if duration_seconds < 1:
                    duration_seconds = 1
                if duration_seconds > 10:
                    duration_seconds = 10
                self.notification_duration = duration_seconds
            except Exception:
                pass
        if "notification_enabled" in settings:
            self.notification_enabled = bool(settings["notification_enabled"])
        if "log_max_bytes" in settings:
            try:
                log_max_bytes = int(settings["log_max_bytes"])
                if log_max_bytes < (128 * 1024):
                    log_max_bytes = 128 * 1024
                if log_max_bytes > (20 * 1024 * 1024):
                    log_max_bytes = 20 * 1024 * 1024
                self.log_max_bytes = log_max_bytes
            except Exception:
                pass
        if "log_backup_count" in settings:
            try:
                log_backup_count = int(settings["log_backup_count"])
                if log_backup_count < 0:
                    log_backup_count = 0
                if log_backup_count > 10:
                    log_backup_count = 10
                self.log_backup_count = log_backup_count
            except Exception:
                pass
        if "ui_prewarm_delay_ms" in settings:
            try:
                ui_prewarm_delay_ms = int(settings["ui_prewarm_delay_ms"])
                if ui_prewarm_delay_ms < 0:
                    ui_prewarm_delay_ms = 0
                if ui_prewarm_delay_ms > 10000:
                    ui_prewarm_delay_ms = 10000
                self.ui_prewarm_delay_ms = ui_prewarm_delay_ms
            except Exception:
                pass
        if "tray_menu_cache_window_ms" in settings:
            try:
                tray_menu_cache_window_ms = int(settings["tray_menu_cache_window_ms"])
                if tray_menu_cache_window_ms < 0:
                    tray_menu_cache_window_ms = 0
                if tray_menu_cache_window_ms > 2000:
                    tray_menu_cache_window_ms = 2000
                self.tray_menu_cache_window_ms = tray_menu_cache_window_ms
            except Exception:
                pass
        if "custom_shortcuts" in settings:
            self.custom_shortcuts = self._validate_custom_shortcuts(
                settings["custom_shortcuts"]
            )
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

    def _validate_custom_shortcuts(
        self, shortcuts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
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
                    logging.warning(
                        f"Shortcut duplicado ignorado: ID={shortcut_id}, hotkey={hotkey}"
                    )
                    continue

                # Valida tamanho do prefixo
                if len(prefix) > 50:
                    prefix = prefix[:50]
                    logging.warning(f"Prefixo truncado para 50 chars: {prefix}")

                # Sanitiza prefixo
                prefix = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", prefix)

                # Adiciona à lista validada
                validated.append(
                    {
                        "id": shortcut_id,
                        "hotkey": hotkey,
                        "prefix": prefix,
                        "enabled": bool(shortcut.get("enabled", True)),
                        "description": str(shortcut.get("description", ""))[:100],
                    }
                )

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
                logging.info(
                    f"Custom shortcuts já configurados: {len(data['custom_shortcuts'])} encontrados"
                )
                return

            # Se tem prefixo legado e não tem custom shortcuts, migra
            legacy_prefix = data.get("prefix", "")
            if legacy_prefix and legacy_prefix.strip():
                logging.info(
                    f"Migrando prefixo legado '{legacy_prefix}' para custom shortcuts"
                )

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

    def add_custom_shortcut(
        self, hotkey: str, prefix: str, description: str = "", enabled: bool = True
    ) -> Tuple[bool, str, Optional[int]]:
        """Adiciona novo custom shortcut"""
        try:
            with self.settings_lock:
                # Verifica limite
                if len(self.custom_shortcuts) >= self.max_custom_shortcuts:
                    return (
                        False,
                        f"Limite de {self.max_custom_shortcuts} atalhos atingido",
                        None,
                    )

                # Normaliza
                hotkey = hotkey.strip().lower()
                prefix = prefix.strip()

                if not hotkey or not prefix:
                    return False, "Hotkey e prefixo são obrigatórios", None

                # Verifica hotkeys reservados
                reserved = [
                    "ctrl+c",
                    "ctrl+v",
                    "ctrl+x",
                    "ctrl+a",
                    "ctrl+z",
                    "ctrl+shift+q",
                    "ctrl+shift+r",
                    "ctrl+shift+f",
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
                prefix = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", prefix)
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
                        logging.info(
                            f"Custom shortcut removido: ID={shortcut_id}, hotkey={removed['hotkey']}"
                        )
                        return True, "Atalho removido com sucesso"

                return False, f"Atalho com ID {shortcut_id} não encontrado"

        except Exception as e:
            logging.error(f"Erro ao remover custom shortcut: {e}")
            return False, f"Erro ao remover: {str(e)}"

    def update_custom_shortcut(
        self,
        shortcut_id: int,
        hotkey: Optional[str] = None,
        prefix: Optional[str] = None,
        description: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> Tuple[bool, str]:
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
                        "ctrl+c",
                        "ctrl+v",
                        "ctrl+x",
                        "ctrl+a",
                        "ctrl+z",
                        "ctrl+shift+q",
                        "ctrl+shift+r",
                        "ctrl+shift+f",
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
                    prefix = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", prefix)
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
