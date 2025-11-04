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
    
    def validate_settings(self, settings_dict: Dict[str, Any]) -> Dict[str, str]:
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
            
            # Remove caracteres perigosos (controle ASCII)
            prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
            
            return {"prefix": prefix}
        except Exception as e:
            logging.error(f"Erro ao validar settings: {e}")
            return {"prefix": ""}
    
    def load(self) -> None:
        """Carrega configurações do arquivo"""
        try:
            with self.settings_lock:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Valida configurações antes de aplicar
                validated = self.validate_settings(data)
                self.date_prefix = validated["prefix"]
        except FileNotFoundError:
            self.date_prefix = ""
        except json.JSONDecodeError as e:
            logging.error(f"Settings corrompido, usando padrão: {e}")
            self.date_prefix = ""
        except Exception as e:
            logging.warning(f"Falha ao carregar settings: {e}")
            self.date_prefix = ""
    
    def save(self) -> None:
        """Salva configurações no arquivo"""
        try:
            with self.settings_lock:
                atomic_write_json(SETTINGS_FILE, {"prefix": self.date_prefix})
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
            "prefix": self.date_prefix
        }
