"""
Configurações e fixtures compartilhadas para testes do Dahora App
"""
import pytest
import os
import tempfile
import shutil
import json


@pytest.fixture
def temp_data_dir():
    """
    Cria um diretório temporário para testes que é automaticamente limpo.
    
    Yields:
        str: Caminho absoluto para o diretório temporário
    """
    temp_dir = tempfile.mkdtemp(prefix='dahora_test_')
    yield temp_dir
    # Cleanup após o teste
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass


@pytest.fixture
def sample_settings():
    """
    Retorna um dicionário de configurações de exemplo para testes.
    
    Returns:
        dict: Configurações de exemplo
    """
    return {
        "prefix": "TEST"
    }


@pytest.fixture
def sample_clipboard_history():
    """
    Retorna histórico de clipboard de exemplo para testes.
    
    Returns:
        list: Lista de itens de histórico
    """
    return [
        {"text": "Item 1", "timestamp": "2025-11-04T01:00:00"},
        {"text": "Item 2", "timestamp": "2025-11-04T01:01:00"},
        {"text": "Item 3", "timestamp": "2025-11-04T01:02:00"},
    ]


@pytest.fixture
def create_test_json_file(temp_data_dir):
    """
    Factory fixture para criar arquivos JSON de teste.
    
    Returns:
        callable: Função que cria arquivo JSON e retorna o caminho
    """
    def _create_file(filename, data):
        filepath = os.path.join(temp_data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return filepath
    
    return _create_file


@pytest.fixture
def create_corrupted_json_file(temp_data_dir):
    """
    Factory fixture para criar arquivos JSON corrompidos.
    
    Returns:
        callable: Função que cria arquivo JSON corrompido
    """
    def _create_file(filename, content="{ this is not valid json!"):
        filepath = os.path.join(temp_data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    return _create_file
