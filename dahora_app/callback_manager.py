"""
Callback Manager - Centraliza lógica de eventos e manipuladores
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple
from functools import wraps


logger = logging.getLogger(__name__)


class CallbackHandler(ABC):
    """Base class para todos os handlers de callback"""

    @abstractmethod
    def handle(self, *args, **kwargs) -> bool:
        """
        Executa o callback, retorna True se sucesso, False se falha

        Args:
            *args: Argumentos posicionais do callback
            **kwargs: Argumentos nomeados do callback

        Returns:
            bool: True se executado com sucesso, False caso contrário
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Retorna nome descritivo do handler"""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.get_name()})"


class CallbackRegistry:
    """Registry central para gerenciar handlers de callbacks"""

    def __init__(self):
        self._handlers: Dict[str, CallbackHandler] = {}
        self._sync_manager = None  # Será injetado se disponível

    def register(self, name: str, handler: CallbackHandler) -> None:
        """
        Registra um novo handler de callback

        Args:
            name: Nome único do handler
            handler: Instância de CallbackHandler

        Raises:
            ValueError: Se handler não é uma instância de CallbackHandler
            KeyError: Se nome já foi registrado
        """
        if not isinstance(handler, CallbackHandler):
            raise ValueError(
                f"Handler must be instance of CallbackHandler, got {type(handler)}"
            )

        if name in self._handlers:
            logger.warning(f"Overwriting existing handler: {name}")

        self._handlers[name] = handler
        logger.debug(f"Registered callback handler: {name}")

    def unregister(self, name: str) -> bool:
        """
        Remove um handler registrado

        Args:
            name: Nome do handler a remover

        Returns:
            bool: True se removido, False se não existia
        """
        if name in self._handlers:
            del self._handlers[name]
            logger.debug(f"Unregistered callback handler: {name}")
            return True
        return False

    def get(self, name: str) -> Optional[CallbackHandler]:
        """
        Obtém um handler registrado

        Args:
            name: Nome do handler

        Returns:
            CallbackHandler ou None se não encontrado
        """
        return self._handlers.get(name)

    def execute(self, name: str, *args, **kwargs) -> bool:
        """
        Executa um handler registrado

        Args:
            name: Nome do handler a executar
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados

        Returns:
            bool: True se executado com sucesso, False caso contrário
        """
        handler = self.get(name)

        if not handler:
            logger.error(f"Handler not found: {name}")
            return False

        try:
            result = handler.handle(*args, **kwargs)
            logger.debug(f"Executed callback: {name} -> {result}")
            return result
        except Exception as e:
            logger.error(f"Error executing callback {name}: {e}", exc_info=True)
            return False

    def execute_safe(self, name: str, *args, **kwargs) -> bool:
        """
        Executa um handler com proteção de thread (usa ThreadSyncManager se disponível)

        Args:
            name: Nome do handler a executar
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados

        Returns:
            bool: True se executado com sucesso
        """
        if self._sync_manager is None:
            # Fallback: import local para evitar circular import
            try:
                from dahora_app.thread_sync import get_sync_manager

                self._sync_manager = get_sync_manager()
            except ImportError:
                return self.execute(name, *args, **kwargs)

        try:
            # Executa dentro de context manager de UI se disponível
            if hasattr(self._sync_manager, "ui_operation"):
                with self._sync_manager.ui_operation():
                    return self.execute(name, *args, **kwargs)
            else:
                return self.execute(name, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in execute_safe for {name}: {e}")
            return False

    def list_handlers(self) -> List[str]:
        """
        Lista todos os handlers registrados

        Returns:
            list: Nomes dos handlers registrados
        """
        return list(self._handlers.keys())

    def list_handlers_info(self) -> List[Tuple[str, str]]:
        """
        Lista handlers com informações detalhadas

        Returns:
            list: Lista de tuplas (nome, descrição)
        """
        return [(name, handler.get_name()) for name, handler in self._handlers.items()]

    def clear(self) -> None:
        """Remove todos os handlers (útil para testes)"""
        self._handlers.clear()
        logger.debug("Cleared all callback handlers")

    def __len__(self) -> int:
        """Retorna número de handlers registrados"""
        return len(self._handlers)

    def __repr__(self) -> str:
        return f"CallbackRegistry(handlers={len(self._handlers)})"


# Singleton global
_callback_registry: Optional[CallbackRegistry] = None


def get_callback_registry() -> CallbackRegistry:
    """
    Obtém instância global do registry de callbacks

    Returns:
        CallbackRegistry: Instância singleton
    """
    global _callback_registry

    if _callback_registry is None:
        _callback_registry = CallbackRegistry()

    return _callback_registry


def initialize_callbacks() -> CallbackRegistry:
    """
    Inicializa registry global de callbacks

    Returns:
        CallbackRegistry: Instância singleton inicializada
    """
    return get_callback_registry()


def with_error_handling(handler_name: Optional[str] = None):
    """
    Decorator para adicionar tratamento de erro automático em handlers

    Args:
        handler_name: Nome descritivo do handler (opcional)

    Returns:
        Decorator que envolve o método com try/except
    """

    def decorator(func: Callable) -> Callable:
        name = handler_name or func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs) -> bool:
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Handler {name} executed successfully")
                return result
            except Exception as e:
                logger.error(f"Error in handler {name}: {e}", exc_info=True)
                return False

        return wrapper

    return decorator


def with_ui_safety(func: Callable) -> Callable:
    """
    Decorator para executar handler dentro de contexto de UI seguro

    Args:
        func: Método a envolver

    Returns:
        Decorator que envolve com ui_operation() se ThreadSyncManager disponível
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> bool:
        try:
            from dahora_app.thread_sync import get_sync_manager

            sync_manager = get_sync_manager()

            if hasattr(sync_manager, "ui_operation"):
                with sync_manager.ui_operation():
                    return func(*args, **kwargs)
        except ImportError:
            pass

        return func(*args, **kwargs)

    return wrapper
