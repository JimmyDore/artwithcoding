"""
Schéma de couleur en gradient diagonal.
"""

from typing import Tuple
from .base_color import BaseColor


class Gradient(BaseColor):
    """Gradient diagonal du coin supérieur gauche au coin inférieur droit."""
    
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
        Génère un gradient diagonal.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur RGB du gradient
        """
        t = (x_norm + y_norm) / 2.0
        r = int(50 + t * 205)
        g = int(100 + t * 155)
        b = int(200 - t * 100)
        return BaseColor._clamp_rgb(r, g, b)