"""
Gerenciador de instância única da aplicação
Garante que apenas uma instância do Dahora App esteja rodando por vez
"""

import logging
import os
import sys
import socket
import tempfile
from pathlib import Path
from typing import Any, Optional, Tuple

try:
    import win32event
    import win32api
    import win32con

    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class SingleInstanceManager:
    """Gerenciador de instância única multiplataforma"""

    def __init__(self, app_name: str = "DahoraApp"):
        """
        Inicializa o gerenciador

        Args:
            app_name: Nome da aplicação (usado para criar nomes únicos)
        """
        self.app_name = app_name
        self.mutex_handle: Optional[Any] = None
        self.socket_server: Optional[socket.socket] = None
        self.is_instance_owner = False
        self._cleanup_called = False

    def check_and_lock(self) -> Tuple[bool, str]:
        """
        Verifica se é a primeira instância e adquire lock

        Returns:
            Tuple[bool, str]: (é_primeira_instância, mensagem)

        Exemplos:
            (True, "Primeira instância - lock adquirido")
            (False, "Outra instância já está rodando")
        """
        if WIN32_AVAILABLE:
            return self._check_and_lock_windows()
        else:
            return self._check_and_lock_socket()

    def _check_and_lock_windows(self) -> Tuple[bool, str]:
        """Windows: Usa Mutex do sistema"""
        try:
            mutex_name = f"Global\\{self.app_name}SingleInstance"

            # Tenta criar o mutex
            self.mutex_handle = win32event.CreateMutex(None, False, mutex_name)

            if self.mutex_handle is None:
                return False, "Falha ao criar mutex"

            # Verifica se já existe outra instância
            # ERROR_ALREADY_EXISTS = 183
            last_error = win32api.GetLastError()

            if last_error == 183:
                # Mutex já existia - outra instância está rodando
                try:
                    win32api.CloseHandle(self.mutex_handle)
                except Exception:
                    pass
                self.mutex_handle = None
                return False, "Outra instância já está rodando"

            # Primeira instância - lock adquirido
            self.is_instance_owner = True
            logging.info(f"[SingleInstance] Mutex '{mutex_name}' adquirido")
            return True, "Primeira instância - lock adquirido"

        except Exception as e:
            logging.error(f"Erro ao criar mutex: {e}")
            # Fallback para socket-based se mutex falhar
            return self._check_and_lock_socket()

    def _check_and_lock_socket(self) -> Tuple[bool, str]:
        """Fallback: Usa socket para lock (multiplataforma)"""
        try:
            # Cria arquivo lock em temp
            lock_file = Path(tempfile.gettempdir()) / f".{self.app_name}.lock"
            port = self._get_port_for_app()

            # Tenta abrir socket na porta
            try:
                self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket_server.bind(("127.0.0.1", port))
                self.socket_server.listen(1)
                self.is_instance_owner = True
                logging.info(f"[SingleInstance] Socket lock adquirido na porta {port}")
                return True, f"Primeira instância - socket lock na porta {port}"

            except OSError as e:
                if "Address already in use" in str(e) or "EADDRINUSE" in str(e):
                    return False, f"Outra instância já está usando porta {port}"
                raise

        except Exception as e:
            logging.error(f"Erro ao criar socket lock: {e}")
            # Se tudo falhar, assume que é primeira instância (fallback seguro)
            self.is_instance_owner = True
            return True, f"Socket lock falhou, assumindo primeira instância: {e}"

    def _get_port_for_app(self) -> int:
        """Gera porta única baseada no app name"""
        # Usa hash do app name para gerar porta entre 49152-65535
        hash_value = sum(ord(c) for c in self.app_name)
        port = 49152 + (hash_value % 16383)
        return port

    def release(self) -> bool:
        """
        Libera o lock de instância única

        Returns:
            bool: True se liberou com sucesso
        """
        if self._cleanup_called:
            return True

        self._cleanup_called = True

        try:
            if self.mutex_handle is not None and WIN32_AVAILABLE:
                try:
                    win32api.CloseHandle(self.mutex_handle)
                    logging.info("[SingleInstance] Mutex liberado")
                except Exception as e:
                    logging.error(f"Erro ao liberar mutex: {e}")
                    return False
                finally:
                    self.mutex_handle = None

            if self.socket_server is not None:
                try:
                    self.socket_server.close()
                    logging.info("[SingleInstance] Socket lock liberado")
                except Exception as e:
                    logging.error(f"Erro ao fechar socket: {e}")
                    return False
                finally:
                    self.socket_server = None

            self.is_instance_owner = False
            return True

        except Exception as e:
            logging.error(f"Erro ao liberar lock: {e}")
            return False

    def __del__(self):
        """Cleanup automático ao destruir objeto"""
        try:
            self.release()
        except Exception:
            pass


# Instância global
_single_instance_manager: Optional[SingleInstanceManager] = None


def initialize_single_instance(app_name: str = "DahoraApp") -> Tuple[bool, str]:
    """
    Inicializa manager de instância única

    Args:
        app_name: Nome da aplicação

    Returns:
        Tuple[bool, str]: (é_primeira_instância, mensagem)
    """
    global _single_instance_manager

    _single_instance_manager = SingleInstanceManager(app_name)
    return _single_instance_manager.check_and_lock()


def cleanup_single_instance() -> bool:
    """Libera lock de instância única"""
    global _single_instance_manager

    if _single_instance_manager is None:
        return True

    return _single_instance_manager.release()


def is_first_instance() -> bool:
    """Verifica se é a primeira instância"""
    global _single_instance_manager

    if _single_instance_manager is None:
        return False

    return _single_instance_manager.is_instance_owner
