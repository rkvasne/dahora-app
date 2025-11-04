"""
Gerenciamento de ícone da bandeja
"""
import os
import sys
import logging
from PIL import Image, ImageDraw
from typing import Optional

# Import opcional de create_icon
try:
    from create_icon import create_image as external_create_image
except Exception:
    external_create_image = None


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
        
        # Tenta usar função externa de create_icon.py
        if external_create_image:
            try:
                return external_create_image()
            except Exception:
                pass
        
        # Fallback simples
        return IconManager._create_simple_fallback_icon()
    
    @staticmethod
    def resolve_icon_path() -> str:
        """
        Resolve o caminho correto do ícone (suporta PyInstaller)
        
        Returns:
            Caminho para o arquivo de ícone
        """
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        except Exception:
            base_dir = os.path.abspath(os.path.dirname(__file__))
        
        # Volta dois níveis (ui -> dahora_app -> raiz)
        base_dir = os.path.dirname(os.path.dirname(base_dir))
        icon_path = os.path.join(base_dir, 'icon.ico')
        
        return icon_path
    
    @staticmethod
    def get_icon_for_tray() -> Image.Image:
        """
        Obtém ícone otimizado para bandeja do sistema
        
        Returns:
            Imagem do ícone
        """
        icon_path = IconManager.resolve_icon_path()
        icon_image = IconManager.load_icon(icon_path)
        
        # Log para debug
        if os.path.exists(icon_path):
            logging.info(f"Ícone carregado de: {icon_path}")
        else:
            logging.info("Usando ícone gerado dinamicamente")
        
        return icon_image
