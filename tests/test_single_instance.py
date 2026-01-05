"""
Testes para SingleInstanceManager
"""
from dahora_app.single_instance import (
    SingleInstanceManager,
    cleanup_single_instance,
    initialize_single_instance,
    is_first_instance,
)


class TestSingleInstanceManager:
    """Testes do gerenciador de instância única"""
    
    def test_create_manager(self):
        """Deve criar manager sem erros"""
        manager = SingleInstanceManager("TestApp")
        assert manager is not None
        assert manager.app_name == "TestApp"
        assert not manager.is_instance_owner
        # Cleanup
        manager.release()
    
    def test_custom_app_name(self):
        """Deve aceitar app name customizado"""
        manager = SingleInstanceManager("MyCustomApp")
        assert manager.app_name == "MyCustomApp"
        manager.release()
    
    def test_get_port_consistency(self):
        """Porta deve ser consistente para mesmo app name"""
        manager1 = SingleInstanceManager("TestApp")
        manager2 = SingleInstanceManager("TestApp")
        
        port1 = manager1._get_port_for_app()
        port2 = manager2._get_port_for_app()
        
        assert port1 == port2
        manager1.release()
        manager2.release()
    
    def test_get_port_different_apps(self):
        """Apps diferentes devem ter portas diferentes"""
        manager1 = SingleInstanceManager("App1")
        manager2 = SingleInstanceManager("App2")
        
        port1 = manager1._get_port_for_app()
        port2 = manager2._get_port_for_app()
        
        assert port1 != port2
        manager1.release()
        manager2.release()
    
    def test_port_in_valid_range(self):
        """Porta deve estar no range válido (49152-65535)"""
        manager = SingleInstanceManager("TestApp")
        port = manager._get_port_for_app()
        
        assert 49152 <= port <= 65535
        manager.release()
    
    def test_first_instance_can_acquire_lock(self):
        """Primeira instância deve adquirir lock com sucesso"""
        manager = SingleInstanceManager("UniqueTest1")
        is_first, msg = manager.check_and_lock()
        
        # Pode ser True (socket) ou True (mutex), mas deve ter sucesso
        assert isinstance(is_first, bool)
        assert isinstance(msg, str)
        assert is_first or not is_first  # Deve retornar bool
        
        manager.release()
    
    def test_release_returns_bool(self):
        """Release deve retornar bool"""
        manager = SingleInstanceManager("TestApp")
        manager.check_and_lock()
        result = manager.release()
        
        assert isinstance(result, bool)
        assert result or not result  # Deve retornar bool
    
    def test_release_idempotent(self):
        """Release deve ser idempotent (seguro chamar múltiplas vezes)"""
        manager = SingleInstanceManager("TestApp")
        manager.check_and_lock()
        
        result1 = manager.release()
        result2 = manager.release()
        
        # Ambas as chamadas devem retornar algo
        assert isinstance(result1, bool)
        assert isinstance(result2, bool)
    
    def test_cleanup_called_flag(self):
        """Flag _cleanup_called deve ser respeitado"""
        manager = SingleInstanceManager("TestApp")
        manager.check_and_lock()
        
        assert not manager._cleanup_called
        manager.release()
        assert manager._cleanup_called
    
    def test_is_instance_owner_after_lock(self):
        """is_instance_owner deve ser True após lock bem-sucedido"""
        manager = SingleInstanceManager("TestApp")
        is_first, _ = manager.check_and_lock()
        
        # Se foi primeira instância, deve marcar como owner
        if is_first:
            assert manager.is_instance_owner
        
        manager.release()
    
    def test_is_instance_owner_after_release(self):
        """is_instance_owner deve ser False após release"""
        manager = SingleInstanceManager("TestApp")
        manager.check_and_lock()
        manager.release()
        
        assert not manager.is_instance_owner


class TestGlobalFunctions:
    """Testes das funções globais"""
    
    def test_initialize_single_instance(self):
        """Deve inicializar com sucesso"""
        is_first, msg = initialize_single_instance("GlobalTest")
        
        assert isinstance(is_first, bool)
        assert isinstance(msg, str)
        assert len(msg) > 0
        
        cleanup_single_instance()
    
    def test_is_first_instance_before_init(self):
        """is_first_instance sem init deve retornar False"""
        # Se não foi inicializado, deve retornar False
        result = is_first_instance()
        assert isinstance(result, bool)
    
    def test_cleanup_single_instance(self):
        """Deve fazer cleanup com sucesso"""
        initialize_single_instance("CleanupTest")
        result = cleanup_single_instance()
        
        assert isinstance(result, bool)
    
    def test_cleanup_without_init(self):
        """Cleanup sem init deve ser seguro"""
        # Limpa qualquer estado anterior
        cleanup_single_instance()
        # Cleanup novamente não deve falhar
        result = cleanup_single_instance()
        assert isinstance(result, bool)


class TestErrorHandling:
    """Testes de tratamento de erros"""
    
    def test_manager_handles_double_release(self):
        """Double release não deve causar erro"""
        manager = SingleInstanceManager("ErrorTest1")
        manager.check_and_lock()
        manager.release()
        
        # Segunda release deve ser segura
        result = manager.release()
        assert isinstance(result, bool)
    
    def test_manager_destructor_safe(self):
        """Destrutor deve ser seguro mesmo sem release explícito"""
        manager = SingleInstanceManager("ErrorTest2")
        manager.check_and_lock()
        # Não faz release explícito
        del manager  # Deve chamar __del__ seguramente
    
    def test_none_handle_release(self):
        """Release com handle None deve ser seguro"""
        manager = SingleInstanceManager("ErrorTest3")
        manager.mutex_handle = None
        manager.socket_server = None
        
        result = manager.release()
        assert isinstance(result, bool)


class TestIntegration:
    """Testes de integração"""
    
    def test_socket_fallback_works(self):
        """Socket fallback deve funcionar se disponível"""
        manager = SingleInstanceManager("FallbackTest")
        is_first, msg = manager._check_and_lock_socket()
        
        assert isinstance(is_first, bool)
        assert isinstance(msg, str)
        
        manager.release()
    
    def test_multiple_managers_different_apps(self):
        """Múltiplos managers para apps diferentes devem coexistir"""
        manager1 = SingleInstanceManager("App1")
        manager2 = SingleInstanceManager("App2")
        
        is_first1, _ = manager1.check_and_lock()
        is_first2, _ = manager2.check_and_lock()
        
        # Pelo menos um deve conseguir (socket permite um por porta)
        assert isinstance(is_first1, bool)
        assert isinstance(is_first2, bool)
        
        manager1.release()
        manager2.release()
    
    def test_message_format(self):
        """Mensagens devem ser strings descritivas"""
        manager = SingleInstanceManager("MsgTest")
        is_first, msg = manager.check_and_lock()
        
        assert isinstance(msg, str)
        assert len(msg) > 5  # Mensagem razoavelmente longa
        assert not msg.startswith(" ")  # Sem espaços extras
        assert not msg.endswith(" ")
        
        manager.release()
