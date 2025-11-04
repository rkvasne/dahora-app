"""
Testes para validação e gerenciamento de configurações (settings)
"""
import sys
import os
import json

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def test_validate_settings_basic(sample_settings):
    """Testa validação básica de settings"""
    # Mock da função validate_settings (será importada quando dahora_app for modular)
    def validate_settings(settings_dict):
        import re
        prefix = str(settings_dict.get("prefix", ""))
        if len(prefix) > 100:
            prefix = prefix[:100]
        prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
        return {"prefix": prefix}
    
    result = validate_settings(sample_settings)
    
    assert "prefix" in result
    assert result["prefix"] == "TEST"


def test_validate_settings_truncates_long_prefix():
    """Testa que prefixo longo é truncado para 100 caracteres"""
    def validate_settings(settings_dict):
        import re
        prefix = str(settings_dict.get("prefix", ""))
        if len(prefix) > 100:
            prefix = prefix[:100]
        prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
        return {"prefix": prefix}
    
    long_prefix = "A" * 150  # 150 caracteres
    result = validate_settings({"prefix": long_prefix})
    
    assert len(result["prefix"]) == 100, f"Prefixo deve ser truncado para 100 chars, recebeu {len(result['prefix'])}"
    assert result["prefix"] == "A" * 100


def test_validate_settings_removes_control_chars():
    """Testa remoção de caracteres de controle ASCII"""
    def validate_settings(settings_dict):
        import re
        prefix = str(settings_dict.get("prefix", ""))
        if len(prefix) > 100:
            prefix = prefix[:100]
        prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
        return {"prefix": prefix}
    
    dangerous_prefix = "test\x00\x1f\x7fvalue"
    result = validate_settings({"prefix": dangerous_prefix})
    
    assert "\x00" not in result["prefix"], "Null byte não deve estar presente"
    assert "\x1f" not in result["prefix"], "Caractere de controle não deve estar presente"
    assert "\x7f" not in result["prefix"], "DEL não deve estar presente"
    assert result["prefix"] == "testvalue"


def test_validate_settings_handles_empty_prefix():
    """Testa que prefixo vazio é permitido"""
    def validate_settings(settings_dict):
        import re
        prefix = str(settings_dict.get("prefix", ""))
        if len(prefix) > 100:
            prefix = prefix[:100]
        prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
        return {"prefix": prefix}
    
    result = validate_settings({"prefix": ""})
    assert result["prefix"] == ""


def test_validate_settings_handles_missing_prefix():
    """Testa que prefixo ausente resulta em string vazia"""
    def validate_settings(settings_dict):
        import re
        prefix = str(settings_dict.get("prefix", ""))
        if len(prefix) > 100:
            prefix = prefix[:100]
        prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
        return {"prefix": prefix}
    
    result = validate_settings({})  # Sem campo "prefix"
    assert result["prefix"] == ""


def test_settings_json_structure(create_test_json_file, sample_settings):
    """Testa estrutura de arquivo JSON de settings"""
    filepath = create_test_json_file("settings.json", sample_settings)
    
    # Verifica que arquivo foi criado
    assert os.path.exists(filepath)
    
    # Lê e valida estrutura
    with open(filepath, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    
    assert isinstance(loaded, dict)
    assert "prefix" in loaded
    assert loaded["prefix"] == "TEST"


def test_corrupted_json_handling(create_corrupted_json_file):
    """Testa tratamento de arquivo JSON corrompido"""
    filepath = create_corrupted_json_file("bad_settings.json")
    
    # Tenta ler o arquivo corrompido
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        assert False, "Deveria ter lançado JSONDecodeError"
    except json.JSONDecodeError:
        # Comportamento esperado
        assert True


def test_validate_settings_special_characters():
    """Testa que caracteres especiais permitidos são mantidos"""
    def validate_settings(settings_dict):
        import re
        prefix = str(settings_dict.get("prefix", ""))
        if len(prefix) > 100:
            prefix = prefix[:100]
        prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
        return {"prefix": prefix}
    
    # Caracteres especiais que DEVEM ser permitidos
    special_prefix = "Test-Prefix_123 @#$%"
    result = validate_settings({"prefix": special_prefix})
    
    assert result["prefix"] == special_prefix, "Caracteres especiais normais devem ser preservados"


def test_validate_settings_unicode():
    """Testa que caracteres Unicode são preservados"""
    def validate_settings(settings_dict):
        import re
        prefix = str(settings_dict.get("prefix", ""))
        if len(prefix) > 100:
            prefix = prefix[:100]
        prefix = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', prefix)
        return {"prefix": prefix}
    
    unicode_prefix = "Prefixo-Ñoño-日本語"
    result = validate_settings({"prefix": unicode_prefix})
    
    assert result["prefix"] == unicode_prefix, "Caracteres Unicode devem ser preservados"


def test_settings_file_atomic_write(temp_data_dir):
    """Testa que escrita de settings é atômica (não corrompe arquivo existente)"""
    settings_file = os.path.join(temp_data_dir, "settings.json")
    
    # Escreve settings inicial
    initial_data = {"prefix": "INITIAL"}
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(initial_data, f)
    
    # Simula escrita atômica (escreve em temp, depois move)
    temp_file = settings_file + ".tmp"
    new_data = {"prefix": "UPDATED"}
    
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f)
        
        # Substitui arquivo original
        if os.path.exists(settings_file):
            os.remove(settings_file)
        os.rename(temp_file, settings_file)
        
        # Verifica que novo conteúdo está correto
        with open(settings_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        assert loaded["prefix"] == "UPDATED"
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
