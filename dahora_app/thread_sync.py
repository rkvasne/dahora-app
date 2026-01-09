"""
Gerenciador de sincronização de threads para a aplicação
Coordena acesso seguro entre múltiplas threads
"""

import logging
import threading
from typing import Callable, Any, Optional
from contextlib import contextmanager


class ThreadSyncManager:
    """Gerenciador de sincronização thread-safe"""

    def __init__(self):
        """Inicializa o gerenciador com locks necessários"""
        # Lock para UI operations (main thread safe)
        self._ui_lock = threading.RLock()

        # Lock para estado de shutdown
        self._shutdown_lock = threading.RLock()
        self._shutdown_requested = False

        # Lock para acesso a recursos compartilhados
        self._resource_lock = threading.RLock()

        # Event para sincronizar shutdown
        self._shutdown_event = threading.Event()

        logging.debug("[ThreadSync] ThreadSyncManager inicializado")

    # ========== SHUTDOWN MANAGEMENT ==========

    def request_shutdown(self) -> bool:
        """
        Requisita shutdown da aplicação

        Returns:
            bool: True se é a primeira requisição, False se já foi requisitado
        """
        with self._shutdown_lock:
            if self._shutdown_requested:
                return False

            self._shutdown_requested = True
            self._shutdown_event.set()
            logging.info("[ThreadSync] Shutdown requisitado")
            return True

    def is_shutdown_requested(self) -> bool:
        """Verifica se shutdown foi requisitado"""
        with self._shutdown_lock:
            return self._shutdown_requested

    def wait_for_shutdown(self, timeout: Optional[float] = None) -> bool:
        """
        Aguarda requisição de shutdown

        Args:
            timeout: Tempo máximo de espera em segundos (None = infinito)

        Returns:
            bool: True se shutdown foi requisitado, False se timeout
        """
        return self._shutdown_event.wait(timeout)

    def reset_shutdown(self) -> None:
        """Reseta flag de shutdown (para testes)"""
        with self._shutdown_lock:
            self._shutdown_requested = False
            self._shutdown_event.clear()

    # ========== UI THREAD OPERATIONS ==========

    @contextmanager
    def ui_operation(self):
        """
        Context manager para operações seguras na UI thread

        Usage:
            with sync_manager.ui_operation():
                self._ui_root.quit()
        """
        with self._ui_lock:
            yield
            logging.debug("[ThreadSync] UI operation completed")

    def acquire_ui_lock(self) -> bool:
        """
        Adquire lock para operação na UI thread
        Retorna True se conseguiu (blocking)
        """
        self._ui_lock.acquire()
        return True

    def release_ui_lock(self) -> None:
        """Libera lock da UI thread"""
        try:
            self._ui_lock.release()
        except RuntimeError:
            # Lock já foi liberado
            pass

    # ========== RESOURCE LOCKING ==========

    @contextmanager
    def resource_lock(self):
        """
        Context manager para acesso a recursos compartilhados

        Usage:
            with sync_manager.resource_lock():
                # Acesso seguro a recurso
                shared_resource.do_something()
        """
        with self._resource_lock:
            yield
            logging.debug("[ThreadSync] Resource operation completed")

    def acquire_resource_lock(self) -> bool:
        """Adquire lock para recurso compartilhado (blocking)"""
        self._resource_lock.acquire()
        return True

    def release_resource_lock(self) -> None:
        """Libera lock de recurso compartilhado"""
        try:
            self._resource_lock.release()
        except RuntimeError:
            pass

    # ========== SAFE THREAD CREATION ==========

    def create_daemon_thread(
        self,
        target: Callable[..., Any],
        name: str = "",
        args: tuple[Any, ...] = (),
        kwargs: Optional[dict[str, Any]] = None,
    ) -> threading.Thread:
        """
        Cria thread daemon segura

        Args:
            target: Função a executar
            name: Nome da thread
            args: Argumentos posicionais
            kwargs: Argumentos nomeados

        Returns:
            threading.Thread: Thread criada (não iniciada)
        """
        kwargs = kwargs or {}

        def safe_target(*target_args: Any, **target_kwargs: Any) -> Any:
            try:
                return target(*target_args, **target_kwargs)
            except Exception:
                logging.exception("[ThreadSync] Exceção não tratada na thread daemon")
                return None

        thread = threading.Thread(
            target=safe_target,
            name=name or f"DahoraThread-{id(target)}",
            args=args,
            kwargs=kwargs,
            daemon=True,
        )

        logging.debug(f"[ThreadSync] Daemon thread criada: {thread.name}")
        return thread

    def start_daemon_thread(
        self,
        target: Callable[..., Any],
        name: str = "",
        args: tuple[Any, ...] = (),
        kwargs: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Optional[threading.Thread]:
        """
        Cria e inicia thread daemon

        Args:
            target: Função a executar
            name: Nome da thread
            args: Argumentos posicionais
            kwargs: Argumentos nomeados
            timeout: Timeout para join após startup (opcional)

        Returns:
            threading.Thread: Thread iniciada ou None se falhou
        """
        try:
            thread = self.create_daemon_thread(target, name, args, kwargs)
            thread.start()

            if timeout:
                thread.join(timeout=timeout)

            logging.debug(f"[ThreadSync] Daemon thread iniciada: {thread.name}")
            return thread

        except Exception as e:
            logging.error(f"[ThreadSync] Erro ao iniciar thread: {e}")
            return None

    # ========== STATE CHECKING ==========

    def is_main_thread(self) -> bool:
        """Verifica se é thread principal"""
        return threading.current_thread() is threading.main_thread()

    def get_current_thread_name(self) -> str:
        """Obtém nome da thread atual"""
        return threading.current_thread().name

    def get_active_thread_count(self) -> int:
        """Conta threads ativas"""
        return threading.active_count()

    # ========== DEBUGGING ==========

    def log_thread_info(self) -> None:
        """Log informações sobre threads ativas"""
        count = threading.active_count()
        current = threading.current_thread().name
        logging.debug(f"[ThreadSync] Threads ativas: {count}, Current: {current}")

    def __del__(self):
        """Cleanup automático"""
        try:
            self._shutdown_event.set()
        except Exception:
            pass


# Instância global
_thread_sync_manager: Optional[ThreadSyncManager] = None


def get_sync_manager() -> ThreadSyncManager:
    """Obtém instância global do manager (lazy initialization)"""
    global _thread_sync_manager

    if _thread_sync_manager is None:
        _thread_sync_manager = ThreadSyncManager()

    return _thread_sync_manager


def initialize_sync() -> ThreadSyncManager:
    """Inicializa o sync manager (preferível chamar uma vez no startup)"""
    return get_sync_manager()
