"""
Formatação de data e hora
"""

from datetime import datetime
from dahora_app.constants import DATETIME_FORMAT


class DateTimeFormatter:
    """Classe para formatação de data/hora"""

    def __init__(
        self, prefix: str = "", bracket_open: str = "[", bracket_close: str = "]"
    ):
        """
        Inicializa o formatador

        Args:
            prefix: Prefixo opcional para incluir no formato
            bracket_open: Caractere de abertura (padrão: "[")
            bracket_close: Caractere de fechamento (padrão: "]")
        """
        self.prefix = prefix
        self.bracket_open = bracket_open
        self.bracket_close = bracket_close

    def set_prefix(self, prefix: str) -> None:
        """Define novo prefixo"""
        self.prefix = prefix

    def set_brackets(self, bracket_open: str, bracket_close: str) -> None:
        """Define novos caracteres de delimitação"""
        self.bracket_open = bracket_open
        self.bracket_close = bracket_close

    def format_now(self) -> str:
        """
        Gera string de data/hora atual no formato [prefixo-]DD.MM.AAAA-HH:MM

        Returns:
            String formatada
        """
        now = datetime.now()
        base = now.strftime(DATETIME_FORMAT)

        try:
            prefix = self.prefix.strip()
        except Exception:
            prefix = ""

        if prefix:
            return f"{self.bracket_open}{prefix}-{base}{self.bracket_close}"
        return f"{self.bracket_open}{base}{self.bracket_close}"

    def format_datetime(self, dt: datetime) -> str:
        """
        Formata um objeto datetime específico

        Args:
            dt: Objeto datetime para formatar

        Returns:
            String formatada
        """
        base = dt.strftime(DATETIME_FORMAT)

        try:
            prefix = self.prefix.strip()
        except Exception:
            prefix = ""

        if prefix:
            return f"{self.bracket_open}{prefix}-{base}{self.bracket_close}"
        return f"{self.bracket_open}{base}{self.bracket_close}"

    def format_with_prefix(self, prefix: str) -> str:
        """
        Gera string de data/hora atual com prefixo específico (NOVO)

        Este método permite formatar com qualquer prefixo sem alterar
        o prefixo padrão da instância. Ideal para múltiplos atalhos.

        Args:
            prefix: Prefixo a ser usado na formatação

        Returns:
            String formatada no formato [prefixo-DD.MM.AAAA-HH:MM]

        Examples:
            >>> formatter = DateTimeFormatter()
            >>> formatter.format_with_prefix("DAHORA")
            '[DAHORA-05.11.2025-18:54]'
            >>> formatter.format_with_prefix("URGENTE")
            '[URGENTE-05.11.2025-18:54]'
        """
        now = datetime.now()
        base = now.strftime(DATETIME_FORMAT)

        try:
            prefix = prefix.strip()
        except Exception:
            prefix = ""

        if prefix:
            return f"{self.bracket_open}{prefix}-{base}{self.bracket_close}"
        return f"{self.bracket_open}{base}{self.bracket_close}"

    def format_datetime_with_prefix(self, dt: datetime, prefix: str) -> str:
        """
        Formata um objeto datetime específico com prefixo customizado (NOVO)

        Args:
            dt: Objeto datetime para formatar
            prefix: Prefixo a ser usado

        Returns:
            String formatada
        """
        base = dt.strftime(DATETIME_FORMAT)

        try:
            prefix = prefix.strip()
        except Exception:
            prefix = ""

        if prefix:
            return f"{self.bracket_open}{prefix}-{base}{self.bracket_close}"
        return f"{self.bracket_open}{base}{self.bracket_close}"
