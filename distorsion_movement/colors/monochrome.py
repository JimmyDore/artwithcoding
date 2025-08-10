"""
Schéma de couleur monochrome.
"""

from typing import Tuple
from .base_color import BaseColor


class Monochrome(BaseColor):
    """Schéma de couleur monochrome - utilise la couleur de base fournie."""
    
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
        Retourne la couleur de base sans modification.
        
        Args:
            square_color: Couleur de base
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            La couleur de base inchangée
        """
        return square_color