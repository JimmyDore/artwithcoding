"""
Schéma de couleur thème forêt.
"""

from typing import Tuple
from .base_color import BaseColor


class Forest(BaseColor):
    """Thème forêt - verts variés."""
    
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
        Génère des couleurs de forêt avec différentes nuances de vert.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur de forêt selon l'intensité verte
        """
        green_intensity = 0.3 + distance_to_center * 0.7 + x_norm * 0.2
        if green_intensity > 0.8:
            return (144, 238, 144)  # Vert clair
        elif green_intensity > 0.5:
            return (34, 139, 34)    # Vert forêt
        else:
            return (0, 100, 0)      # Vert foncé