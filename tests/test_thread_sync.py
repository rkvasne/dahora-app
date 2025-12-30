"""
Testes para ThreadSyncManager
"""
import pytest
import threading
import time
from dahora_app.thread_sync import ThreadSyncManager, get_sync_manager, initialize_sync


class TestThreadSyncManager:
    """Testes do gerenciador de sincronização"""
    
    def test_create_manager(self):
        """Deve criar manager sem erros"""
        manager = ThreadSyncManager()
        assert manager is not None
        assert not manager.is_shutdown_requested()
    
    def test_request_shutdown(self):
        """Primeiro request deve retornar True"""
        manager = ThreadSyncManager()
        result = manager.request_shutdown()
        assert result is True
        assert manager.is_shutdown_requested()
    
    def test_shutdown_idempotent(self):
        """Segundo request deve retornar False (já foi requisitado)"""
        manager = ThreadSyncManager()
        manager.request_shutdown()
        result2 = manager.request_shutdown()
        assert result2 is False
    
    def test_is_shutdown_requested(self):
        """Deve rastrear estado de shutdown"""
        manager = ThreadSyncManager()
        assert not manager.is_shutdown_requested()
        manager.request_shutdown()
        assert manager.is_shutdown_requested()
    
    def test_reset_shutdown(self):
        """Reset deve limpar flag de shutdown"""
        manager = ThreadSyncManager()
        manager.request_shutdown()
        assert manager.is_shutdown_requested()
        
        manager.reset_shutdown()
        assert not manager.is_shutdown_requested()
    
    def test_wait_for_shutdown_no_timeout(self):
        """Wait sem timeout deve bloquear até shutdown"""
        manager = ThreadSyncManager()
        
        # Dispara shutdown em outra thread
        def shutdown_later():
            time.sleep(0.1)
            manager.request_shutdown()
        
        thread = threading.Thread(target=shutdown_later, daemon=True)
        thread.start()
        
        # Wait deve retornar True (foi requisitado)
        result = manager.wait_for_shutdown(timeout=1.0)
        assert result is True
        
        thread.join(timeout=0.5)
    
    def test_wait_for_shutdown_with_timeout(self):
        """Wait com timeout deve expirar se não houver shutdown"""
        manager = ThreadSyncManager()
        
        # Não dispara shutdown
        result = manager.wait_for_shutdown(timeout=0.1)
        assert result is False
    
    def test_ui_operation_context_manager(self):
        """Context manager de UI operation deve funcionar"""
        manager = ThreadSyncManager()
        
        executed = False
        with manager.ui_operation():
            executed = True
        
        assert executed
    
    def test_ui_lock_acquire_release(self):
        """Deve adquirir e liberar UI lock"""
        manager = ThreadSyncManager()
        
        assert manager.acquire_ui_lock() is True
        manager.release_ui_lock()
    
    def test_resource_lock_context_manager(self):
        """Context manager de resource lock deve funcionar"""
        manager = ThreadSyncManager()
        
        executed = False
        with manager.resource_lock():
            executed = True
        
        assert executed
    
    def test_resource_lock_acquire_release(self):
        """Deve adquirir e liberar resource lock"""
        manager = ThreadSyncManager()
        
        assert manager.acquire_resource_lock() is True
        manager.release_resource_lock()


class TestDaemonThread:
    """Testes de criação de daemon threads"""
    
    def test_create_daemon_thread(self):
        """Deve criar daemon thread"""
        manager = ThreadSyncManager()
        
        def dummy():
            pass
        
        thread = manager.create_daemon_thread(dummy, name="TestThread")
        
        assert thread is not None
        assert thread.daemon is True
        assert thread.name == "TestThread"
    
    def test_create_daemon_thread_with_args(self):
        """Deve criar daemon thread com argumentos"""
        manager = ThreadSyncManager()
        
        result = []
        
        def target(a, b, c=None):
            result.append((a, b, c))
        
        thread = manager.create_daemon_thread(
            target,
            args=(1, 2),
            kwargs={'c': 3}
        )
        
        thread.start()
        thread.join(timeout=1.0)
        
        assert (1, 2, 3) in result
    
    def test_start_daemon_thread(self):
        """Deve criar e iniciar daemon thread"""
        manager = ThreadSyncManager()
        
        executed = False
        
        def target():
            nonlocal executed
            executed = True
        
        thread = manager.start_daemon_thread(target)
        
        assert thread is not None
        thread.join(timeout=1.0)
        assert executed
    
    def test_start_daemon_thread_with_timeout(self):
        """Start com timeout deve aguardar thread"""
        manager = ThreadSyncManager()
        
        executed = False
        
        def target():
            nonlocal executed
            time.sleep(0.05)
            executed = True
        
        thread = manager.start_daemon_thread(target, timeout=0.5)
        
        assert executed
        assert thread is not None
    
    def test_start_daemon_thread_error_handling(self):
        """Erro na thread não deve quebrar start_daemon_thread"""
        manager = ThreadSyncManager()
        
        def bad_target():
            raise ValueError("Test error")
        
        # Não deve lançar exceção
        thread = manager.start_daemon_thread(bad_target)
        
        # Mas thread pode ser None se houve erro
        # ou pode ser criada dependendo do timing
        time.sleep(0.1)


class TestStateChecking:
    """Testes de verificação de estado"""
    
    def test_is_main_thread(self):
        """Deve detectar thread principal"""
        manager = ThreadSyncManager()
        
        # Em teste, é main thread
        assert manager.is_main_thread() is True
        
        # Em outra thread, não é
        is_main = []
        
        def check():
            is_main.append(manager.is_main_thread())
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
        thread.join(timeout=1.0)
        
        assert is_main[0] is False
    
    def test_get_current_thread_name(self):
        """Deve obter nome da thread atual"""
        manager = ThreadSyncManager()
        
        name = manager.get_current_thread_name()
        assert isinstance(name, str)
        assert len(name) > 0
    
    def test_get_active_thread_count(self):
        """Deve contar threads ativas"""
        manager = ThreadSyncManager()
        
        count = manager.get_active_thread_count()
        assert isinstance(count, int)
        assert count >= 1  # Pelo menos main thread


class TestGlobalFunctions:
    """Testes de funções globais"""
    
    def test_get_sync_manager(self):
        """Deve retornar instância global"""
        manager1 = get_sync_manager()
        manager2 = get_sync_manager()
        
        assert manager1 is manager2
    
    def test_initialize_sync(self):
        """Deve inicializar sync manager"""
        manager = initialize_sync()
        
        assert manager is not None
        assert isinstance(manager, ThreadSyncManager)


class TestThreadSafety:
    """Testes de thread-safety"""
    
    def test_multiple_threads_shutdown_request(self):
        """Múltiplas threads requisitando shutdown deve ser seguro"""
        manager = ThreadSyncManager()
        
        results = []
        
        def request_shutdown():
            result = manager.request_shutdown()
            results.append(result)
        
        threads = [
            threading.Thread(target=request_shutdown, daemon=True)
            for _ in range(5)
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join(timeout=1.0)
        
        # Apenas um deve ter sucesso
        assert sum(results) == 1  # Exatamente um True
        assert results.count(True) == 1
        assert results.count(False) == 4
    
    def test_concurrent_lock_operations(self):
        """Operações concorrentes com locks deve ser seguro"""
        manager = ThreadSyncManager()
        
        counter = [0]
        
        def increment():
            with manager.resource_lock():
                current = counter[0]
                counter[0] = current + 1
        
        threads = [
            threading.Thread(target=increment, daemon=True)
            for _ in range(10)
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join(timeout=2.0)
        
        # Deve ter incrementado 10 vezes
        assert counter[0] == 10
    
    def test_shutdown_event_sync(self):
        """Shutdown event deve sincronizar múltiplas threads"""
        manager = ThreadSyncManager()
        
        results = []
        
        def wait_and_record():
            manager.wait_for_shutdown(timeout=2.0)
            results.append(True)
        
        # Inicia 3 threads esperando
        threads = [
            threading.Thread(target=wait_and_record, daemon=True)
            for _ in range(3)
        ]
        
        for t in threads:
            t.start()
        
        time.sleep(0.1)  # Deixa threads esperarem
        
        # Requisita shutdown
        manager.request_shutdown()
        
        # Aguarda threads terminarem
        for t in threads:
            t.join(timeout=1.0)
        
        # Todas devem ter completado
        assert len(results) == 3
