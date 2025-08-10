"""
Schéma de couleur aurore boréale.
"""

import math
from typing import Tuple
from .base_color import BaseColor


class AuroraBorealis(BaseColor):
    """Aurora Borealis - teal, vert, violet fluides ensemble."""
    
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
        Génère des couleurs d'aurore boréale avec effet ondulant.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré dans la grille
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur d'aurore boréale RGB
        """
        # Map distance and position into hue shifts for a wave-like effect
        hue_center = 0.4 + math.sin((x_norm + y_norm + distance_to_center) * 4) * 0.1  # base around green/teal
        hue = (hue_center + (math.sin(index * 0.05) * 0.15)) % 1.0  # shifting into purple/blue range
        sat = 0.7 + 0.3 * math.sin(y_norm * 5 + distance_to_center * 3)  # dynamic saturation
        val = 0.6 + 0.4 * math.cos(x_norm * 4 + distance_to_center * 2)  # gentle brightness movement
        return BaseColor._hsv_to_rgb_clamped(hue, sat, val)