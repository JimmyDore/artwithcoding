"""
Schéma de couleur analogues.
"""

import math
from typing import Tuple
from .base_color import BaseColor


class Analogous(BaseColor):
    """Couleurs analogues avec variations subtiles."""
    
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
        Génère des couleurs analogues avec des variations de teinte.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré dans la grille
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur analogue RGB
        """
        base_hue = 0.3  # green-ish
        hue_shift = (x_norm - 0.5) * 0.3 + (y_norm - 0.5) * 0.3  # ±0.3 spread
        sat = 0.5 + 0.5 * (0.5 - distance_to_center)  # more saturated near center
        val = 0.7 + 0.3 * math.sin(index * 0.1)  # subtle brightness wave
        return BaseColor._hsv_to_rgb_clamped((base_hue + hue_shift) % 1.0, sat, val)