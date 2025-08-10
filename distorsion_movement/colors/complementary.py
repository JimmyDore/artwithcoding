"""
Schéma de couleur complémentaire.
"""

from typing import Tuple
from .base_color import BaseColor


class Complementary(BaseColor):
    """Couleurs complémentaires alternées."""
    
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
        Génère des couleurs complémentaires alternées.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré dans la grille
            dimension: Dimension de la grille
            
        Returns:
            Couleur orange ou bleue complémentaire
        """
        if (index + (index // dimension)) % 2 == 0:
            return (255, 100, 50)  # Orange
        else:
            return (50, 150, 255)  # Bleu