"""
Schéma de couleur pop art.
"""

from typing import Tuple
from .base_color import BaseColor


class PopArt(BaseColor):
    """Pop Art - primaires vives avec contours noir/blanc."""
    
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
        Génère des couleurs pop art avec primaires et contours.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré dans la grille
            dimension: Dimension de la grille
            
        Returns:
            Couleur pop art RGB
        """
        primaries = [
            (255, 0, 0),    # Red
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 0)     # Green
        ]

        row = index // dimension
        col = index % dimension

        # Every Nth cell becomes black/white for a bold outline effect
        if row % 5 == 0 or col % 5 == 0:
            return (0, 0, 0) if (row + col) % 2 == 0 else (255, 255, 255)

        # Otherwise, cycle through bright primaries
        return primaries[(row + col) % len(primaries)]