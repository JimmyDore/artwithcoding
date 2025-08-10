"""
Schéma de couleur coucher de soleil.
"""

from typing import Tuple
from .base_color import BaseColor


class Sunset(BaseColor):
    """Gradient de coucher de soleil: jaune chaud → orange → rose → violet."""
    
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
        Génère un gradient de coucher de soleil vertical.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur de coucher de soleil RGB
        """
        yellow = (255, 223, 0)
        orange = (255, 140, 0)
        pink   = (255, 105, 180)
        purple = (128, 0, 128)

        # Map vertical position to gradient
        t = y_norm  # 0 = top, 1 = bottom

        if t < 0.33:
            # Yellow to orange
            blend = t / 0.33
            return BaseColor._blend_colors(yellow, orange, blend)
        elif t < 0.66:
            # Orange to pink
            blend = (t - 0.33) / 0.33
            return BaseColor._blend_colors(orange, pink, blend)
        else:
            # Pink to purple
            blend = (t - 0.66) / 0.34
            return BaseColor._blend_colors(pink, purple, blend)