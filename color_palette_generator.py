from PIL import Image
from colorthief import ColorThief
from typing import List, Tuple

def get_color_palette(image_path: str, num_colors: int = 10) -> List[str]:
    """
    Gera uma paleta de cores a partir de uma imagem.

    Args:
        image_path: Caminho para a imagem.
        num_colors: O número de cores na paleta.

    Returns:
        Uma lista de strings de cores em formato hexadecimal.
    """
    try:
        color_thief = ColorThief(image_path)
        palette = color_thief.get_palette(color_count=num_colors)
        
        # Converte a tupla RGB para formato hexadecimal
        return [rgb_to_hex(color) for color in palette]
    except Exception as e:
        raise Exception(f"Erro ao gerar a paleta de cores: {e}")

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    Converte uma tupla RGB em um código de cor hexadecimal.
    """
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'