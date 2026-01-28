"""
Gerenciamento de ícone da bandeja
"""

import os
import sys
import logging
from PIL import Image, ImageDraw
from typing import Optional
from functools import lru_cache


class IconManager:
    """Gerenciador de ícone da bandeja"""

    @staticmethod
    @lru_cache(maxsize=16)
    def _load_icon_from_disk_cached(icon_path: str) -> Optional[Image.Image]:
        """Carrega ícone do disco com cache.

        Retorna uma imagem carregada em memória (copy) para evitar reabrir
        o arquivo toda vez que uma janela é mostrada ou o ícone da bandeja muda.
        """
        try:
            if icon_path and os.path.exists(icon_path):
                with Image.open(icon_path) as img:
                    # ICO pode conter múltiplos frames com desenhos diferentes.
                    # Para ficar igual ao ícone das janelas (que costuma usar um frame maior),
                    # selecionamos o MAIOR frame disponível.
                    try:
                        n_frames = getattr(img, "n_frames", 1)
                        if n_frames and n_frames > 1:
                            best_i = 0
                            best_area = -1
                            for i in range(n_frames):
                                try:
                                    img.seek(i)
                                    w, h = img.size
                                    area = int(w) * int(h)
                                except Exception:
                                    continue
                                if area > best_area:
                                    best_area = area
                                    best_i = i
                            try:
                                img.seek(best_i)
                            except Exception:
                                pass
                    except Exception:
                        pass

                    try:
                        return img.convert("RGBA").copy()
                    except Exception:
                        return img.copy()
        except Exception:
            return None
        return None

    @staticmethod
    def _create_simple_fallback_icon() -> Image.Image:
        """
        Cria um ícone simples como fallback

        Returns:
            Imagem do ícone
        """
        image = Image.new("RGBA", (64, 64), color=(255, 152, 0, 255))
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
        # Se não especificou path, usa o path resolvido (suporta PyInstaller)
        if not icon_path:
            icon_path = IconManager.resolve_icon_path()

        # Tenta carregar do path especificado (com cache)
        if icon_path:
            cached = IconManager._load_icon_from_disk_cached(icon_path)
            if cached is not None:
                return cached.copy()

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
        filename = "icon_paused.ico" if is_paused else "icon.ico"

        if getattr(sys, "frozen", False):
            # Se estiver rodando como executável (PyInstaller)
            # Os ícones são adicionados na raiz do bundle (ver build.py)
            base_dir = getattr(sys, "_MEIPASS", "")
            icon_path = os.path.join(base_dir, filename)
        else:
            # Se estiver rodando do código fonte
            # ui -> dahora_app -> raiz
            base_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            icon_path = os.path.join(base_dir, "assets", filename)

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

        # Systray geralmente exibe ~16-24px. Redimensionar a partir do melhor frame
        # (maior) deixa o desenho consistente com as janelas.
        try:
            resample = getattr(Image, "Resampling", Image).LANCZOS
            icon_image = icon_image.resize((64, 64), resample=resample)
        except Exception:
            pass

        # Log para debug
        if os.path.exists(icon_path):
            logging.info(f"Ícone carregado de: {icon_path} (Paused={is_paused})")
        else:
            logging.info(f"Usando ícone gerado dinamicamente (Paused={is_paused})")

        return icon_image
