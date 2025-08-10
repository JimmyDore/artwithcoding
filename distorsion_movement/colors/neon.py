"""
Schéma de couleur néon.
"""

from typing import Tuple
from .base_color import BaseColor


class Neon(BaseColor):
    """Couleurs néon vives."""
    
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
        Génère des couleurs néon vives.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur néon RGB
        """
        hue = (distance_to_center + x_norm * 0.5) % 1.0
        return BaseColor._hsv_to_rgb_clamped(hue, 1.0, 1.0)