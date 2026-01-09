"""
Gerenciamento de contador de uso
"""

import logging
from threading import Lock
from dahora_app.constants import COUNTER_FILE
from dahora_app.utils import atomic_write_text


class UsageCounter:
    """Contador de uso do aplicativo"""

    def __init__(self):
        """Inicializa o contador"""
        self.counter_lock = Lock()
        self.counter = 0

    def load(self) -> None:
        """Carrega o contador do arquivo ou inicia com 0"""
        try:
            with self.counter_lock:
                with open(COUNTER_FILE, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    self.counter = int(content) if content else 0
        except FileNotFoundError:
            self.counter = 0
        except Exception as e:
            logging.warning(f"Falha ao carregar contador: {e}")
            self.counter = 0

    def save(self) -> None:
        """Salva o contador no arquivo"""
        try:
            with self.counter_lock:
                atomic_write_text(COUNTER_FILE, str(self.counter))
        except Exception as e:
            logging.warning(f"Falha ao salvar contador: {e}")

    def increment(self) -> int:
        """
        Incrementa o contador e salva

        Returns:
            Valor atual do contador após incrementar
        """
        try:
            with self.counter_lock:
                self.counter += 1
                atomic_write_text(COUNTER_FILE, str(self.counter))
                return self.counter
        except Exception as e:
            logging.warning(f"Falha ao incrementar contador: {e}")
            return self.counter

    def get_count(self) -> int:
        """Retorna o valor atual do contador"""
        return self.counter

    def reset(self) -> None:
        """Reseta o contador para zero"""
        with self.counter_lock:
            self.counter = 0
            self.save()
