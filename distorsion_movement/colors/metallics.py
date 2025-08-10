"""
Schéma de couleur métalliques.
"""

from typing import Tuple
from .base_color import BaseColor


class Metallics(BaseColor):
    """Gradients métalliques - or, argent, bronze."""
    
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
        Génère des couleurs métalliques avec gradients.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur métallique RGB
        """
        gold   = (212, 175, 55)
        silver = (192, 192, 192)
        bronze = (205, 127, 50)

        # Use position to blend smoothly between metals
        t = (x_norm + y_norm) / 2.0  # 0..1 diagonal gradient

        if t < 0.33:
            # Blend from gold to silver
            blend = t / 0.33
            return BaseColor._blend_colors(gold, silver, blend)
        elif t < 0.66:
            # Blend from silver to bronze
            blend = (t - 0.33) / 0.33
            return BaseColor._blend_colors(silver, bronze, blend)
        else:
            # Blend from bronze back to gold
            blend = (t - 0.66) / 0.34
            return BaseColor._blend_colors(bronze, gold, blend)