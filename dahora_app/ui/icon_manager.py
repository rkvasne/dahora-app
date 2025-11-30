"""
Gerenciamento de ícone da bandeja
"""
import os
import sys
import logging
from PIL import Image, ImageDraw
from typing import Optional

class IconManager:
    """Gerenciador de ícone da bandeja"""
    
    @staticmethod
    def _create_simple_fallback_icon() -> Image.Image:
        """
        Cria um ícone simples como fallback
        
        Returns:
            Imagem do ícone
        """
        image = Image.new('RGBA', (64, 64), color=(255, 152, 0, 255))
        draw = ImageDraw.Draw(image)
        # Desenha "D" simples no centro
        draw.rectangle([20, 20, 44, 44], fill=(40, 40, 40, 255))
        return image
    
    @staticmethod
    def load_icon(icon_path: Optional[str] = None) -> Image.Image:
        """
        Carrega o ícone do aplicativo
        
        Args:
            icon_path: Caminho opcional para o ícone
            
        Returns:
            Imagem do ícone
        """
        # Se não especificou path, tenta carregar icon.ico da raiz
        if not icon_path:
            try:
                if os.path.exists('icon.ico'):
                    return Image.open('icon.ico')
            except Exception:
                pass
        
        # Tenta carregar do path especificado
        if icon_path:
            try:
                if os.path.exists(icon_path):
                    return Image.open(icon_path)
            except Exception:
                pass
        
        # Fallback: cria ícone simples
        return IconManager._create_simple_fallback_icon()
    
    @staticmethod
    def resolve_icon_path(is_paused: bool = False) -> str:
        """
        Resolve o caminho correto do ícone (suporta PyInstaller)
        
        Args:
            is_paused: Se True, retorna o ícone de pausa
            
        Returns:
            Caminho para o arquivo de ícone
        """
        if getattr(sys, 'frozen', False):
            # Se estiver rodando como executável (PyInstaller)
            base_dir = sys._MEIPASS
        else:
            # Se estiver rodando do código fonte
            # ui -> dahora_app -> raiz
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
        filename = 'icon_paused.ico' if is_paused else 'icon.ico'
        icon_path = os.path.join(base_dir, filename)
        return icon_path
    
    @staticmethod
    def get_icon_for_tray(is_paused: bool = False) -> Image.Image:
        """
        Obtém ícone otimizado para bandeja do sistema
        
        Args:
            is_paused: Se True, retorna o ícone de pausa
        
        Returns:
            Imagem do ícone
        """
        icon_path = IconManager.resolve_icon_path(is_paused)
        icon_image = IconManager.load_icon(icon_path)
        
        # Log para debug
        if os.path.exists(icon_path):
            logging.info(f"Ícone carregado de: {icon_path} (Paused={is_paused})")
        else:
            logging.info(f"Usando ícone gerado dinamicamente (Paused={is_paused})")
        
        return icon_image
