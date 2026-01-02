"""
Gerenciamento de clipboard e histórico
"""
import json
import logging
import os
import time
from datetime import datetime
from threading import Lock
from typing import List, Dict
import pyperclip
from dahora_app.constants import (
    HISTORY_FILE, MAX_HISTORY_ITEMS,
    CLIPBOARD_MONITOR_INTERVAL, CLIPBOARD_IDLE_THRESHOLD
)
from dahora_app.utils import atomic_write_json, dpapi_encrypt_bytes, dpapi_decrypt_bytes, b64encode_bytes, b64decode_str


class ClipboardManager:
    """Gerenciador de clipboard e histórico"""
    
    def __init__(self):
        """Inicializa o gerenciador de clipboard"""
        self.history_lock = Lock()
        self.clipboard_history: List[Dict[str, str]] = []
        self.last_clipboard_content = ""
        self.paused = False
        self._own_content_expiry: Dict[str, float] = {}

        self._dpapi_entropy = b"DahoraApp-clipboard-history-v1"
        self._history_write_disabled = False
        self._history_write_disabled_reason = ""

    def mark_own_content(self, text: str, ttl_seconds: float = 2.0) -> None:
        if not text:
            return

        now = time.time()
        with self.history_lock:
            self._own_content_expiry[text] = now + float(ttl_seconds)
            expired_keys = [k for k, v in self._own_content_expiry.items() if v <= now]
            for k in expired_keys:
                self._own_content_expiry.pop(k, None)

    def _is_own_content(self, text: str) -> bool:
        if not text:
            return False

        now = time.time()
        with self.history_lock:
            expiry = self._own_content_expiry.get(text)
            if expiry is None:
                return False
            if expiry <= now:
                self._own_content_expiry.pop(text, None)
                return False
            return True

    def _write_history_locked(self, *, force: bool = False) -> None:
        if self._history_write_disabled and not force:
            return
        try:
            plain = json.dumps(self.clipboard_history, ensure_ascii=False).encode("utf-8")
            blob = dpapi_encrypt_bytes(plain, self._dpapi_entropy)
            payload = {"dpapi": 1, "blob": b64encode_bytes(blob), "fallback": self.clipboard_history}
            atomic_write_json(HISTORY_FILE, payload)
        except Exception:
            atomic_write_json(HISTORY_FILE, self.clipboard_history)
    
    def toggle_pause(self) -> bool:
        """Alterna estado de pausa do monitoramento"""
        self.paused = not self.paused
        logging.info(f"Monitoramento de clipboard {'pausado' if self.paused else 'retomado'}")
        return self.paused
    
    def load_history(self) -> None:
        """Carrega o histórico do arquivo ou inicia com lista vazia"""
        needs_migration = False
        try:
            with self.history_lock:
                history_write_disabled = False
                history_write_disabled_reason = ""
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    raw = json.load(f)

                if isinstance(raw, dict) and raw.get("dpapi") == 1:
                    blob_str = raw.get("blob")
                    if isinstance(blob_str, str):
                        try:
                            decrypted = dpapi_decrypt_bytes(b64decode_str(blob_str), self._dpapi_entropy)
                            loaded = json.loads(decrypted.decode("utf-8"))
                        except Exception as e:
                            fallback = raw.get("fallback")
                            if isinstance(fallback, list):
                                loaded = fallback
                            else:
                                loaded = []
                                history_write_disabled = False
                                history_write_disabled_reason = str(e)
                    else:
                        loaded = raw
                        needs_migration = isinstance(raw, list)
                else:
                    loaded = raw
                    needs_migration = isinstance(raw, list)

                self.clipboard_history = loaded if isinstance(loaded, list) else []
                if len(self.clipboard_history) > MAX_HISTORY_ITEMS:
                    self.clipboard_history = self.clipboard_history[-MAX_HISTORY_ITEMS:]
                self._history_write_disabled = history_write_disabled
                self._history_write_disabled_reason = history_write_disabled_reason
        except FileNotFoundError:
            self.clipboard_history = []
            self._history_write_disabled = False
            self._history_write_disabled_reason = ""
        except json.JSONDecodeError as e:
            logging.warning(f"Falha ao carregar histórico (JSON inválido): {e}")
            self.clipboard_history = []
            self._history_write_disabled = False
            self._history_write_disabled_reason = ""
        except Exception as e:
            logging.warning(f"Falha ao carregar histórico: {e}")
            self.clipboard_history = []
            if os.path.exists(HISTORY_FILE):
                self._history_write_disabled = True
                self._history_write_disabled_reason = str(e)

        if needs_migration and not self._history_write_disabled:
            try:
                self.save_history()
            except Exception:
                pass
    
    def save_history(self) -> None:
        """Salva o histórico no arquivo"""
        try:
            with self.history_lock:
                self._write_history_locked()
        except Exception as e:
            logging.warning(f"Falha ao salvar histórico: {e}")
    
    def add_to_history(self, text: str) -> None:
        """
        Adiciona um item ao histórico
        
        Args:
            text: Texto a ser adicionado
        """
        if not text or not text.strip():
            return
        
        with self.history_lock:
            # Verifica se já existe
            for item in self.clipboard_history:
                if item.get("text") == text:
                    return
            
            # Adiciona novo item
            new_item = {
                "text": text,
                "timestamp": datetime.now().isoformat(),
                "app": "Dahora App"
            }
            self.clipboard_history.append(new_item)
            
            # Mantém tamanho máximo
            if len(self.clipboard_history) > MAX_HISTORY_ITEMS:
                self.clipboard_history = self.clipboard_history[-MAX_HISTORY_ITEMS:]
            
            self._write_history_locked()
            logging.info(f"Histórico atualizado: total={len(self.clipboard_history)}; último='{text[:50]}...'")
    
    def clear_history(self) -> int:
        """
        Limpa todo o histórico
        
        Returns:
            Número de itens removidos
        """
        logging.info("Iniciando limpeza do histórico de clipboard")
        with self.history_lock:
            total_items = len(self.clipboard_history)
            self.clipboard_history = []
            try:
                self._write_history_locked(force=True)
                logging.info(f"Histórico limpo com sucesso! {total_items} itens removidos")
            except Exception as e:
                logging.error(f"Falha ao salvar histórico limpo: {e}")
        
        return total_items
    
    def get_recent_items(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        Retorna os itens mais recentes do histórico
        
        Args:
            limit: Número máximo de itens
            
        Returns:
            Lista com itens mais recentes
        """
        with self.history_lock:
            return self.clipboard_history[-limit:].copy() if self.clipboard_history else []
    
    def get_history_size(self) -> int:
        """Retorna o número de itens no histórico"""
        return len(self.clipboard_history)
    
    def copy_text(self, text: str) -> None:
        """
        Copia texto para clipboard
        
        Args:
            text: Texto a ser copiado
        """
        pyperclip.copy(text)
    
    def paste_text(self) -> str:
        """
        Obtém texto atual da clipboard
        
        Returns:
            Texto da clipboard
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            logging.warning(f"Erro ao obter clipboard: {e}")
            return ""
    
    def initialize_last_content(self) -> None:
        """Inicializa o último conteúdo da clipboard"""
        try:
            self.last_clipboard_content = pyperclip.paste()
            logging.info(f"Clipboard inicializado: '{self.last_clipboard_content[:30] if self.last_clipboard_content else 'vazio'}'")
        except Exception as e:
            logging.warning(f"Erro ao inicializar clipboard: {e}")
            self.last_clipboard_content = ""
    
    def monitor_clipboard_smart(self, on_change_callback=None) -> None:
        """
        Monitora inteligentemente o clipboard com polling adaptativo
        
        Args:
            on_change_callback: Função a chamar quando clipboard mudar
        """
        logging.info("Monitor inteligente de clipboard iniciado")
        
        # Inicializa conteúdo atual
        self.initialize_last_content()
        
        attempt = 0
        last_activity_time = time.time()
        
        while True:
            attempt += 1
            current_time = time.time()
            
            try:
                current_content = pyperclip.paste()
                
                if attempt % 120 == 0:
                    time_idle = current_time - last_activity_time
                    logging.debug(f"Monitor clipboard ativo (ocioso há {time_idle:.1f}s)")
                
                # Se pausado, apenas atualiza last_content para evitar flood quando despausar
                if self.paused:
                    self.last_clipboard_content = current_content
                    time.sleep(1.0)
                    continue
                
                # Verifica mudança
                if current_content and current_content.strip():
                    if current_content != self.last_clipboard_content:
                        logging.info(f"Clipboard mudou de '{self.last_clipboard_content[:30] if self.last_clipboard_content else 'vazio'}' para '{current_content[:30]}...'")
                        if not self._is_own_content(current_content):
                            self.add_to_history(current_content)
                        self.last_clipboard_content = current_content
                        last_activity_time = current_time
                        
                        # Callback opcional
                        if on_change_callback:
                            on_change_callback()
                        
                        logging.info(f"Clipboard atualizado: {current_content[:50]}...")
                
                # Polling adaptativo
                time_idle = current_time - last_activity_time
                if time_idle < CLIPBOARD_IDLE_THRESHOLD:
                    sleep_time = 0.5  # Responde rápido quando há atividade
                else:
                    sleep_time = 5.0  # Intervalo maior quando ocioso
                
            except Exception as e:
                logging.warning(f"Erro ao monitorar clipboard: {e}")
                sleep_time = CLIPBOARD_MONITOR_INTERVAL
            
            time.sleep(sleep_time)
