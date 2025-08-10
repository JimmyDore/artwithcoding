"""
Schéma de couleur magasin de bonbons.
"""

from typing import Tuple
from .base_color import BaseColor


class CandyShop(BaseColor):
    """Magasin de bonbons - rose bubblegum, vert menthe, jaune citron."""
    
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
        Génère des couleurs de bonbons en damier.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré dans la grille
            dimension: Dimension de la grille
            
        Returns:
            Couleur bonbon RGB
        """
        bubblegum = (255, 105, 180)  # pink
        mint      = (152, 255, 152)  # light mint green
        lemon     = (255, 250, 102)  # lemon yellow

        palette = [bubblegum, mint, lemon]

        row = index // dimension
        col = index % dimension

        # Checkerboard cycling through candy colors
        return palette[(row + col) % len(palette)]