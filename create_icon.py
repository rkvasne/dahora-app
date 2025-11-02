#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar o arquivo icon.ico a partir da função create_image
"""

from PIL import Image, ImageDraw
from datetime import datetime

def create_image():
    """Cria um ícone de relógio digital claro e identificável"""
    # Cria uma imagem 64x64 com fundo transparente (RGBA)
    image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Cor principal: laranja (#FF9800)
    color_main = (255, 152, 0, 255)
    color_bg = (40, 40, 40, 255)  # Fundo escuro
    color_text = (255, 255, 255, 255)
    color_accent = (255, 87, 34, 255)  # Laranja mais escuro

    # Desenha um relógio digital tipo mostrador
    # Fundo arredondado (retângulo com bordas arredondadas simuladas)
    draw.rectangle([6, 8, 58, 56], fill=color_bg)

    # Borda externa
    draw.rectangle([6, 8, 58, 56], outline=color_main, width=3)

    # Mostrador digital - formato HH:MM
    # Dois pontos no meio (como relógio digital)
    draw.ellipse([28, 26, 32, 30], fill=color_main)
    draw.ellipse([28, 34, 32, 38], fill=color_main)

    # Números simulados (símbolos para representar hora)
    # Usa caracteres simples para simular display digital
    try:
        from PIL import ImageFont
        try:
            # Tenta usar fonte monospace maior
            font = ImageFont.truetype("consola.ttf", 20)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 18)
            except:
                font = ImageFont.load_default()

        # Texto "12:34" como exemplo visual
        text = "12:34"
        try:
            # Pillow 9.0+
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # Pillow < 9.0
            try:
                bbox = draw.textsize(text, font=font)
                text_width, text_height = bbox
            except:
                text_width, text_height = 50, 20

        x = 32 - text_width // 2
        y = 30 - text_height // 2
        draw.text((x, y), text, fill=color_main, font=font)
    except:
        # Fallback: desenha símbolo simples
        # Desenha linhas para simular display digital
        # Topo
        draw.line([14, 18, 22, 18], fill=color_main, width=3)
        # Meio
        draw.line([14, 32, 22, 32], fill=color_main, width=3)
        # Baixo
        draw.line([14, 46, 22, 46], fill=color_main, width=3)
        # Direita (segundo dígito)
        draw.line([42, 18, 50, 18], fill=color_main, width=3)
        draw.line([42, 32, 50, 32], fill=color_main, width=3)
        draw.line([42, 46, 50, 46], fill=color_main, width=3)

    return image

if __name__ == '__main__':
    # Cria a imagem
    icon_image = create_image()

    # Salva como arquivo .ico (formato Windows)
    icon_image.save('icon.ico', format='ICO')

    print("✅ Arquivo icon.ico criado com sucesso!")
    print("📍 Salvo em: icon.ico")
    print("🎨 Este ícone será usado no executável .exe")