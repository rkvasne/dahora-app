"""
Testes para formatação de data e hora
"""
import sys
import os
import re
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importa o formatador
from dahora_app.datetime_formatter import DateTimeFormatter

# Import da função principal (será necessário ajustar dahora_app.py para permitir import)
# Por enquanto, vamos testar o formato esperado


def test_datetime_format_structure():
    """Testa se o formato da string de data/hora está correto"""
    # Padrão esperado: [DD.MM.YYYY-HH:MM]
    pattern = r'^\[\d{2}\.\d{2}\.\d{4}-\d{2}:\d{2}\]$'
    
    # Simula geração (em produção virá de generate_datetime_string())
    now = datetime.now()
    result = f"[{now.strftime('%d.%m.%Y-%H:%M')}]"
    
    assert re.match(pattern, result), f"Formato inválido: {result}"
    assert result.startswith('['), "Deve começar com ["
    assert result.endswith(']'), "Deve terminar com ]"
    assert '-' in result, "Deve conter separador -"
    assert '.' in result, "Deve conter separador ."


def test_datetime_format_with_prefix():
    """Testa formato com prefixo customizado"""
    prefix = "TESTE"
    now = datetime.now()
    result = f"[{prefix}-{now.strftime('%d.%m.%Y-%H:%M')}]"
    
    pattern = r'^\[TESTE-\d{2}\.\d{2}\.\d{4}-\d{2}:\d{2}\]$'
    
    assert re.match(pattern, result), f"Formato com prefixo inválido: {result}"
    assert prefix in result, f"Prefixo '{prefix}' não encontrado"


def test_datetime_components():
    """Testa componentes individuais da data/hora"""
    now = datetime.now()
    result = f"[{now.strftime('%d.%m.%Y-%H:%M')}]"
    
    # Remove os colchetes
    content = result[1:-1]
    
    # Deve ter formato: DD.MM.YYYY-HH:MM
    parts = content.split('-')
    assert len(parts) == 2, "Deve ter exatamente 2 partes separadas por -"
    
    date_part = parts[0]
    time_part = parts[1]
    
    # Valida data: DD.MM.YYYY
    date_components = date_part.split('.')
    assert len(date_components) == 3, "Data deve ter 3 componentes"
    assert len(date_components[0]) == 2, "Dia deve ter 2 dígitos"
    assert len(date_components[1]) == 2, "Mês deve ter 2 dígitos"
    assert len(date_components[2]) == 4, "Ano deve ter 4 dígitos"
    
    # Valida hora: HH:MM
    time_components = time_part.split(':')
    assert len(time_components) == 2, "Hora deve ter 2 componentes"
    assert len(time_components[0]) == 2, "Hora deve ter 2 dígitos"
    assert len(time_components[1]) == 2, "Minuto deve ter 2 dígitos"


def test_datetime_values_are_valid():
    """Testa se os valores de data/hora são válidos"""
    now = datetime.now()
    result = f"[{now.strftime('%d.%m.%Y-%H:%M')}]"
    
    # Extrai valores
    content = result[1:-1]
    date_part, time_part = content.split('-')
    day, month, year = map(int, date_part.split('.'))
    hour, minute = map(int, time_part.split(':'))
    
    # Valida ranges
    assert 1 <= day <= 31, f"Dia inválido: {day}"
    assert 1 <= month <= 12, f"Mês inválido: {month}"
    assert 2000 <= year <= 2100, f"Ano inválido: {year}"
    assert 0 <= hour <= 23, f"Hora inválida: {hour}"
    assert 0 <= minute <= 59, f"Minuto inválido: {minute}"


def test_datetime_consistency():
    """Testa consistência temporal (2 chamadas seguidas devem ser próximas)"""
    now1 = datetime.now()
    result1 = f"[{now1.strftime('%d.%m.%Y-%H:%M')}]"
    
    now2 = datetime.now()
    result2 = f"[{now2.strftime('%d.%m.%Y-%H:%M')}]"
    
    # Em chamadas sucessivas, devem ser iguais ou diferir apenas no minuto
    # (assumindo que não atravessamos um minuto)
    assert len(result1) == len(result2), "Comprimento deve ser consistente"
    
    # Formato deve ser idêntico
    assert result1.count('[') == result2.count('[') == 1
    assert result1.count(']') == result2.count(']') == 1
    assert result1.count('-') == result2.count('-') == 1


# ========== NOVOS TESTES PARA MÚLTIPLOS PREFIXOS ==========

def test_format_with_prefix_novo():
    """Testa novo método format_with_prefix() sem alterar instância"""
    formatter = DateTimeFormatter(prefix="ORIGINAL")
    
    # Formata com prefixo diferente
    result1 = formatter.format_with_prefix("DAHORA")
    result2 = formatter.format_with_prefix("URGENTE")
    result3 = formatter.format_with_prefix("REUNIAO")
    
    # Verifica que cada um tem seu prefixo
    assert result1.startswith("[DAHORA-")
    assert result2.startswith("[URGENTE-")
    assert result3.startswith("[REUNIAO-")
    
    # Verifica que prefixo original não mudou
    result_original = formatter.format_now()
    assert result_original.startswith("[ORIGINAL-")


def test_format_with_prefix_empty():
    """Testa format_with_prefix() com prefixo vazio"""
    formatter = DateTimeFormatter()
    result = formatter.format_with_prefix("")
    
    # Deve formatar sem prefixo
    assert result.startswith("[")
    assert not result.startswith("[-")  # Não deve ter hífen extra


def test_format_with_prefix_whitespace():
    """Testa format_with_prefix() com prefixo com espaços"""
    formatter = DateTimeFormatter()
    result = formatter.format_with_prefix("  DAHORA  ")
    
    # Deve remover espaços
    assert result.startswith("[DAHORA-")
    assert "  " not in result


def test_format_datetime_with_prefix():
    """Testa format_datetime_with_prefix() com data específica"""
    formatter = DateTimeFormatter()
    dt = datetime(2025, 11, 5, 18, 54, 30)
    
    result1 = formatter.format_datetime_with_prefix(dt, "DAHORA")
    result2 = formatter.format_datetime_with_prefix(dt, "URGENTE")
    
    assert "[DAHORA-05.11.2025-18:54]" == result1
    assert "[URGENTE-05.11.2025-18:54]" == result2


def test_format_multiple_prefixes_sequential():
    """Testa múltiplas formatações sequenciais sem interferência"""
    formatter = DateTimeFormatter()
    
    # Simula múltiplos atalhos sendo usados
    results = []
    prefixes = ["DAHORA", "URGENTE", "REUNIAO", "TRABALHO", "PESSOAL"]
    
    for prefix in prefixes:
        result = formatter.format_with_prefix(prefix)
        results.append(result)
    
    # Verifica que cada resultado tem seu prefixo correto
    for i, prefix in enumerate(prefixes):
        assert results[i].startswith(f"[{prefix}-")
        assert results[i].endswith("]")


def test_backward_compatibility_format_now():
    """Testa que métodos legados continuam funcionando"""
    formatter = DateTimeFormatter(prefix="LEGADO")
    
    # Método antigo deve funcionar normalmente
    result = formatter.format_now()
    assert result.startswith("[LEGADO-")
    
    # set_prefix() deve continuar funcionando
    formatter.set_prefix("NOVO")
    result2 = formatter.format_now()
    assert result2.startswith("[NOVO-")


def test_format_with_prefix_same_time():
    """Testa que prefixos diferentes geram mesma timestamp"""
    formatter = DateTimeFormatter()
    
    # Captura timestamp base
    now = datetime.now()
    base_time = now.strftime('%d.%m.%Y-%H:%M')
    
    # Formata com diferentes prefixos
    result1 = formatter.format_with_prefix("PREFIX1")
    result2 = formatter.format_with_prefix("PREFIX2")
    
    # Ambos devem ter o mesmo timestamp (se chamados no mesmo minuto)
    assert base_time in result1
    assert base_time in result2
