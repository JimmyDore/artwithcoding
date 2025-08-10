"""
Schéma de couleur basé sur la température.
"""

from typing import Tuple
from .base_color import BaseColor


class Temperature(BaseColor):
    """Couleurs chaudes au centre, froides aux bords."""
    
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
        Génère des couleurs selon la température basée sur la distance au centre.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur chaude (centre) ou froide (bords)
        """
        temp = 1.0 - distance_to_center
        if temp > 0.7:
            # Très chaud - rouge/jaune
            return BaseColor._hsv_to_rgb_clamped(0.1, 0.8, 1.0)
        elif temp > 0.4:
            # Chaud - orange/rouge
            return BaseColor._hsv_to_rgb_clamped(0.05, 0.9, 0.9)
        else:
            # Froid - bleu/violet
            return BaseColor._hsv_to_rgb_clamped(0.6 + temp * 0.2, 0.7, 0.8)