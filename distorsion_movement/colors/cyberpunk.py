"""
Schéma de couleur cyberpunk.
"""

from typing import Tuple
from .base_color import BaseColor


class Cyberpunk(BaseColor):
    """Neon magenta & cyan avec accents violets profonds."""
    
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
        Génère des couleurs cyberpunk avec magenta et cyan néon.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré dans la grille
            dimension: Dimension de la grille
            
        Returns:
            Couleur cyberpunk RGB
        """
        hue_base = 0.83 if (index + (index // dimension)) % 2 == 0 else 0.5  # magenta or cyan
        # Slight hue variation for organic feel
        hue = (hue_base + (x_norm - 0.5) * 0.1 + (y_norm - 0.5) * 0.1) % 1.0
        sat = 1.0
        # Bright at center, darker towards edges
        val = 0.6 + 0.4 * (1.0 - distance_to_center)
        return BaseColor._hsv_to_rgb_clamped(hue, sat, val)