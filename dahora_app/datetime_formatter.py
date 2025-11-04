"""
Formatação de data e hora
"""
from datetime import datetime
from dahora_app.constants import DATETIME_FORMAT


class DateTimeFormatter:
    """Classe para formatação de data/hora"""
    
    def __init__(self, prefix: str = ""):
        """
        Inicializa o formatador
        
        Args:
            prefix: Prefixo opcional para incluir no formato
        """
        self.prefix = prefix
    
    def set_prefix(self, prefix: str) -> None:
        """Define novo prefixo"""
        self.prefix = prefix
    
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
            return f"[{prefix}-{base}]"
        return f"[{base}]"
    
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
            return f"[{prefix}-{base}]"
        return f"[{base}]"
