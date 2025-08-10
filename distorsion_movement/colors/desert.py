"""
Schéma de couleur thème désert.
"""

from typing import Tuple
from .base_color import BaseColor


class Desert(BaseColor):
    """Thème désert - beige sableux, orange chaud, brun mat."""
    
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
        Génère des couleurs de désert selon la zone.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur de désert selon la zone
        """
        sand     = (237, 201, 175)  # sandy beige
        orange   = (210, 125, 45)   # warm orange
        brown    = (102, 51, 0)     # muted brown

        # Use distance and position to vary tones
        if distance_to_center < 0.33:
            # Center: light sand
            return sand
        elif distance_to_center < 0.66:
            # Mid ring: warm orange
            return orange
        else:
            # Outer ring: deep brown
            return brown