"""
Schéma de couleur noir et blanc alternant (damier).
"""

from typing import Tuple
from .base_color import BaseColor


class BlackWhiteAlternating(BaseColor):
    """Schéma noir et blanc en damier/checkerboard."""
    
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
        Génère un pattern de damier noir et blanc.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré dans la grille
            dimension: Dimension de la grille
            
        Returns:
            Couleur noir ou blanc selon la position dans le damier
        """
        row = index // dimension
        col = index % dimension
        # Pattern damier classique
        is_white = (row + col) % 2 == 0
        return (255, 255, 255) if is_white else (0, 0, 0)