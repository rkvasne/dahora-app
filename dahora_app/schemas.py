"""
Schemas de validação com Pydantic para Dahora App
Define estruturas de dados seguras e validadas
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
import re
from dahora_app.hotkey_validator import HotkeyValidator


class CustomShortcutSchema(BaseModel):
    """Schema para um atalho personalizado"""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(..., ge=1, description="ID único do atalho")
    hotkey: str = Field(
        ..., min_length=3, max_length=50, description="Hotkey (ex: ctrl+shift+q)"
    )
    prefix: str = Field(
        ..., min_length=1, max_length=100, description="Prefixo para timestamp"
    )
    enabled: bool = Field(default=True, description="Se atalho está ativo")
    description: str = Field(
        default="", max_length=100, description="Descrição opcional do atalho"
    )

    @field_validator("hotkey")
    @classmethod
    def validate_hotkey_format(cls, v: str) -> str:
        """Valida formato básico de hotkey"""
        if not v or not isinstance(v, str):
            raise ValueError("Hotkey deve ser string")

        normalized = HotkeyValidator.normalize(v)
        is_valid, reason = HotkeyValidator.validate_with_reason(normalized)
        if not is_valid:
            raise ValueError(reason or "Hotkey inválido")

        return normalized

    @field_validator("prefix")
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        """Valida prefixo (sem caracteres de controle)"""
        if not v:
            raise ValueError("Prefixo não pode ser vazio")

        # Remove espaços desnecessários
        v = v.strip()

        # Remove caracteres de controle
        v = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", v)

        if not v:
            raise ValueError("Prefixo vazio após sanitização")

        return v


class SettingsSchema(BaseModel):
    """Schema para configurações do aplicativo"""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    # Prefixo e formato
    prefix: str = Field(default="", max_length=100, description="Prefixo padrão")
    datetime_format: str = Field(
        default="%d.%m.%Y-%H:%M", description="Formato de data/hora"
    )
    bracket_open: str = Field(default="[", min_length=1, max_length=1)
    bracket_close: str = Field(default="]", min_length=1, max_length=1)

    # Hotkeys do app
    hotkey_copy_datetime: str = Field(
        default="ctrl+shift+q", description="Hotkey para copiar timestamp"
    )
    hotkey_search_history: str = Field(
        default="ctrl+shift+f", description="Hotkey para buscar histórico"
    )
    hotkey_refresh_menu: str = Field(
        default="ctrl+shift+r", description="Hotkey para recarregar menu"
    )

    # Limites e intervalos
    max_history_items: int = Field(
        default=100, ge=10, le=1000, description="Máximo de itens no histórico"
    )
    clipboard_monitor_interval: float = Field(
        default=3.0,
        ge=0.5,
        le=60.0,
        description="Intervalo de monitoramento em segundos",
    )
    clipboard_idle_threshold: int = Field(
        default=30, ge=5, le=300, description="Limiar de inatividade em segundos"
    )
    notification_duration: int = Field(
        default=2, ge=1, le=10, description="Duração da notificação em segundos"
    )
    notification_enabled: bool = Field(
        default=True, description="Se notificações estão habilitadas"
    )

    log_max_bytes: int = Field(
        default=1 * 1024 * 1024,
        ge=128 * 1024,
        le=20 * 1024 * 1024,
        description="Tamanho máximo do log em bytes",
    )
    log_backup_count: int = Field(
        default=1, ge=0, le=10, description="Quantidade de backups do log"
    )
    ui_prewarm_delay_ms: int = Field(
        default=700, ge=0, le=10000, description="Delay para prewarm da UI (ms)"
    )
    tray_menu_cache_window_ms: int = Field(
        default=200, ge=0, le=2000, description="Janela de cache do menu do tray (ms)"
    )

    # Custom shortcuts
    custom_shortcuts: List[CustomShortcutSchema] = Field(
        default_factory=list
    )
    default_shortcut_id: Optional[int] = Field(
        default=None, ge=1, description="ID do atalho padrão"
    )

    @field_validator("prefix")
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        """Sanitiza prefixo"""
        if not v:
            return ""

        # Remove caracteres de controle
        v = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", v)
        # Trunca a 100 chars SE necessário, mas Pydantic já vai validar o max_length
        return v

    @field_validator("datetime_format")
    @classmethod
    def validate_datetime_format(cls, v: str) -> str:
        """Valida que formato contém pelo menos %d, %m, %Y ou %H"""
        if not v or not any(fmt in v for fmt in ["%d", "%m", "%Y", "%H", "%M", "%S"]):
            raise ValueError(
                "Formato deve conter pelo menos uma especificação de data/hora"
            )
        return v

    @field_validator("bracket_open", "bracket_close")
    @classmethod
    def validate_brackets(cls, v: str) -> str:
        """Valida caracteres de delimitação"""
        if not v or len(v) != 1:
            raise ValueError("Bracket deve ser um único caractere")
        # Evita caracteres problemáticos
        if v in "\n\r\t":
            raise ValueError("Bracket não pode ser whitespace")
        return v

    @model_validator(mode="after")
    def validate_brackets_different(self) -> "SettingsSchema":
        """Valida que brackets aberto e fechado são diferentes"""
        if self.bracket_open == self.bracket_close:
            raise ValueError("Brackets de abertura e fechamento devem ser diferentes")
        return self

    @model_validator(mode="after")
    def validate_custom_shortcut_ids(self) -> "SettingsSchema":
        """Valida que IDs dos shortcuts são únicos e consistentes"""
        if not self.custom_shortcuts:
            return self

        ids = [sc.id for sc in self.custom_shortcuts]

        # Verifica duplicatas
        if len(ids) != len(set(ids)):
            raise ValueError("IDs dos custom shortcuts devem ser únicos")

        # Verifica se default_shortcut_id existe
        if self.default_shortcut_id is not None and self.default_shortcut_id not in ids:
            raise ValueError(
                f"default_shortcut_id {self.default_shortcut_id} não existe nos custom_shortcuts"
            )

        return self

    @model_validator(mode="after")
    def validate_hotkey_duplicates(self) -> "SettingsSchema":
        """Valida que não há hotkeys duplicados"""
        hotkeys = [
            self.hotkey_copy_datetime,
            self.hotkey_search_history,
            self.hotkey_refresh_menu,
        ]

        hotkeys += [sc.hotkey for sc in self.custom_shortcuts]

        # Normaliza e verifica
        normalized = [h.lower().strip() for h in hotkeys]
        if len(normalized) != len(set(normalized)):
            raise ValueError("Hotkeys duplicados detectados")

        return self


class NotificationSchema(BaseModel):
    """Schema para configurações de notificação"""

    model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(default=True)
    duration_seconds: int = Field(default=2, ge=1, le=10)
    show_on_error: bool = Field(default=True)


class AppConfigSchema(BaseModel):
    """Schema completo da configuração do app (principal)"""

    model_config = ConfigDict(extra="forbid")

    settings: SettingsSchema
    notifications: NotificationSchema = Field(default_factory=NotificationSchema)
