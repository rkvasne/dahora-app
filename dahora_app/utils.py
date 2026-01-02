"""
Funções utilitárias do Dahora App
"""
import os
import json
import base64
from typing import Any


def format_hotkey_display(hotkey: str) -> str:
    """Formata hotkey para exibição humana.

    Mantém o valor salvo/registrado intacto (ex.: 'ctrl+shift+exclam'), mas
    exibe símbolos quando aplicável (ex.: 'Ctrl+Shift+!').
    """
    if not hotkey:
        return ""

    parts = [p for p in hotkey.replace(" ", "").split("+") if p]

    modifiers = {
        "ctrl": "Ctrl",
        "control": "Ctrl",
        "shift": "Shift",
        "alt": "Alt",
        "win": "Win",
        "windows": "Win",
        "cmd": "Cmd",
        "command": "Cmd",
    }

    # Nomes usados por libs de hotkey (keyboard/tk) para símbolos
    symbols = {
        "exclam": "!",
        "at": "@",
        "numbersign": "#",
        "number_sign": "#",
        "hash": "#",
        "dollar": "$",
        "percent": "%",
        "asciicircum": "^",
        "caret": "^",
        "ampersand": "&",
        "asterisk": "*",
        "parenleft": "(",
        "parenright": ")",
        "minus": "-",
        "underscore": "_",
        "equal": "=",
        "plus": "+",
        "comma": ",",
        "period": ".",
        "dot": ".",
        "slash": "/",
        "backslash": "\\",
        "question": "?",
        "quotedbl": '"',
        "apostrophe": "'",
        "grave": "`",
        "tilde": "~",
        "bracketleft": "[",
        "bracketright": "]",
        "braceleft": "{",
        "braceright": "}",
        "semicolon": ";",
        "colon": ":",
        "less": "<",
        "greater": ">",
        "bar": "|",
    }

    out = []
    for raw in parts:
        key = raw.lower()

        if key in modifiers:
            out.append(modifiers[key])
            continue

        if key in symbols:
            out.append(symbols[key])
            continue

        # F-keys
        if key.startswith("f") and key[1:].isdigit():
            out.append("F" + key[1:])
            continue

        # Um único caractere: letra vira maiúscula; dígito/símbolo mantém
        if len(raw) == 1:
            out.append(raw.upper() if raw.isalpha() else raw)
            continue

        # Default: Title Case simples e troca _ por espaço
        pretty = raw.replace("_", " ")
        out.append(pretty[:1].upper() + pretty[1:] if pretty else pretty)

    return "+".join(out)


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


def atomic_write_bytes(path: str, data: bytes) -> None:
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(data)
    os.replace(tmp_path, path)


def dpapi_encrypt_bytes(data: bytes, entropy: bytes) -> bytes:
    import win32crypt

    encrypted = win32crypt.CryptProtectData(data, None, entropy, None, None, 0)
    if isinstance(encrypted, tuple):
        return encrypted[1]
    return encrypted


def dpapi_decrypt_bytes(blob: bytes, entropy: bytes) -> bytes:
    import win32crypt

    decrypted = win32crypt.CryptUnprotectData(blob, None, entropy, None, None, 0)
    if isinstance(decrypted, tuple):
        return decrypted[1]
    return decrypted


def b64encode_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64decode_str(data: str) -> bytes:
    return base64.b64decode((data or "").encode("ascii"))


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
