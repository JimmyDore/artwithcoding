"""
Schéma de couleur infrarouge thermique.
"""

from typing import Tuple
from .base_color import BaseColor


class InfraredThermal(BaseColor):
    """Infrarouge/Thermal - progression classique d'imagerie thermique."""
    
    @staticmethod
    def get_color_for_position(
        square_color: Tuple[int, int, int],
        x_norm: float, 
        y_norm: float, 
        distance_to_center: float, 
        index: int,
        dimension: int
    ) -> Tuple[int, int, int]:
        """
        Génère des couleurs thermiques infrarouge.
        
        Progression: bleu → cyan → vert → jaune → orange → rouge → blanc
        distance_to_center = 0 (centre) -> froid (bleu)
        distance_to_center = 1 (bord)   -> chaud (blanc)
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur thermique RGB
        """
        t = 1.0 - distance_to_center  # invert so center is cold, edges are hot
        
        if t < 0.16:  # 0.0 - 0.16: blue to cyan
            progress = t / 0.16
            hue = 0.66 - progress * 0.08  # blue (0.66) to cyan (0.58)
            sat = 1.0
            val = 0.3 + progress * 0.4  # dark blue to bright cyan
        elif t < 0.33:  # 0.16 - 0.33: cyan to green
            progress = (t - 0.16) / 0.17
            hue = 0.58 - progress * 0.25  # cyan (0.58) to green (0.33)
            sat = 1.0
            val = 0.7 + progress * 0.3
        elif t < 0.5:  # 0.33 - 0.5: green to yellow
            progress = (t - 0.33) / 0.17
            hue = 0.33 - progress * 0.17  # green (0.33) to yellow (0.16)
            sat = 1.0
            val = 1.0
        elif t < 0.66:  # 0.5 - 0.66: yellow to orange
            progress = (t - 0.5) / 0.16
            hue = 0.16 - progress * 0.08  # yellow (0.16) to orange (0.08)
            sat = 1.0
            val = 1.0
        elif t < 0.83:  # 0.66 - 0.83: orange to red
            progress = (t - 0.66) / 0.17
            hue = 0.08 - progress * 0.08  # orange (0.08) to red (0.0)
            sat = 1.0
            val = 1.0
        elif t < 0.92:  # 0.83 - 0.92: red to red-white
            progress = (t - 0.83) / 0.09
            hue = 0.0  # pure red
            sat = 1.0 - progress * 0.3  # desaturate towards white
            val = 1.0
        else:  # 0.92 - 1.0: red-white to pure white
            progress = (t - 0.92) / 0.08
            hue = 0.0
            sat = 0.7 - progress * 0.7  # fully desaturate
            val = 1.0

        return BaseColor._hsv_to_rgb_clamped(hue, sat, val)