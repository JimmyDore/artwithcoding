"""
Schéma de couleur arc-en-ciel.
"""

from typing import Tuple
from .base_color import BaseColor


class Rainbow(BaseColor):
    """Arc-en-ciel basé sur la position."""
    
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
        Génère des couleurs arc-en-ciel selon la position.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur RGB de l'arc-en-ciel
        """
        hue = (x_norm + y_norm * 0.5) % 1.0
        return BaseColor._hsv_to_rgb_clamped(hue, 0.8, 0.9)