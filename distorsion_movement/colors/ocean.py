"""
Schéma de couleur thème océan.
"""

from typing import Tuple
from .base_color import BaseColor


class Ocean(BaseColor):
    """Thème océan - bleus et verts."""
    
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
        Génère des couleurs océan selon la profondeur.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur océan selon la profondeur
        """
        depth = distance_to_center
        if depth < 0.3:
            # Eau peu profonde - turquoise
            return (64, 224, 208)
        elif depth < 0.7:
            # Eau moyenne - bleu océan
            return (0, 119, 190)
        else:
            # Eau profonde - bleu foncé
            return (25, 25, 112)