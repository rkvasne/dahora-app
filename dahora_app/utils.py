"""
Funções utilitárias do Dahora App
"""
import os
import json
from typing import Any


def atomic_write_text(path: str, text: str, encoding: str = "utf-8") -> None:
    """
    Escreve texto em arquivo de forma atômica (evita corrupção)
    
    Args:
        path: Caminho do arquivo
        text: Texto a ser escrito
        encoding: Codificação do arquivo
    """
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding=encoding) as f:
        f.write(text)
    os.replace(tmp_path, path)


def atomic_write_json(path: str, obj: Any) -> None:
    """
    Escreve objeto JSON em arquivo de forma atômica
    
    Args:
        path: Caminho do arquivo
        obj: Objeto a ser serializado como JSON
    """
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Trunca texto para tamanho máximo
    
    Args:
        text: Texto a ser truncado
        max_length: Tamanho máximo
        suffix: Sufixo a adicionar se truncado
        
    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def sanitize_text_for_display(text: str) -> str:
    """
    Sanitiza texto para exibição (remove quebras de linha, tabs, etc)
    
    Args:
        text: Texto a ser sanitizado
        
    Returns:
        Texto sanitizado
    """
    return text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
