"""
Gerenciamento de clipboard e histórico
"""
import json
import logging
import time
from datetime import datetime
from threading import Lock
from typing import List, Dict
import pyperclip
from dahora_app.constants import (
    HISTORY_FILE, MAX_HISTORY_ITEMS,
    CLIPBOARD_MONITOR_INTERVAL, CLIPBOARD_IDLE_THRESHOLD
)
from dahora_app.utils import atomic_write_json


class ClipboardManager:
    """Gerenciador de clipboard e histórico"""
    
    def __init__(self):
        """Inicializa o gerenciador de clipboard"""
        self.history_lock = Lock()
        self.clipboard_history: List[Dict[str, str]] = []
        self.last_clipboard_content = ""
    
    def load_history(self) -> None:
        """Carrega o histórico do arquivo ou inicia com lista vazia"""
        try:
            with self.history_lock:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.clipboard_history = json.load(f)
                if len(self.clipboard_history) > MAX_HISTORY_ITEMS:
                    self.clipboard_history = self.clipboard_history[-MAX_HISTORY_ITEMS:]
        except FileNotFoundError:
            self.clipboard_history = []
        except Exception as e:
            logging.warning(f"Falha ao carregar histórico: {e}")
            self.clipboard_history = []
    
    def save_history(self) -> None:
        """Salva o histórico no arquivo"""
        try:
            with self.history_lock:
                atomic_write_json(HISTORY_FILE, self.clipboard_history)
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
            
            atomic_write_json(HISTORY_FILE, self.clipboard_history)
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
                atomic_write_json(HISTORY_FILE, [])
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
                
                # Log reduzido (apenas a cada 120 tentativas = ~1 minuto)
                if attempt % 120 == 0:
                    time_idle = current_time - last_activity_time
                    logging.debug(f"Monitor clipboard ativo (ocioso há {time_idle:.1f}s)")
                
                # Verifica mudança
                if current_content and current_content.strip():
                    if current_content != self.last_clipboard_content:
                        logging.info(f"Clipboard mudou de '{self.last_clipboard_content[:30] if self.last_clipboard_content else 'vazio'}' para '{current_content[:30]}...'")
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
