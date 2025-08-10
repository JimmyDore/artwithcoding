"""
Schéma de couleur thème reggae.
"""

from typing import Tuple
from .base_color import BaseColor


class Reggae(BaseColor):
    """Thème reggae - vert, jaune, rouge."""
    
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
        Génère des couleurs reggae selon la zone.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur reggae selon la zone
        """
        green  = (0, 153, 51)     # rich green
        yellow = (255, 204, 0)    # bright yellow
        red    = (204, 0, 0)      # deep red

        # Use distance and position to vary tones
        if distance_to_center < 0.33:
            # Center: green
            return green
        elif distance_to_center < 0.66:
            # Mid ring: yellow
            return yellow
        else:
            # Outer ring: red
            return red