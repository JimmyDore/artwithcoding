"""
Schéma de couleur thème feu.
"""

from typing import Tuple
from .base_color import BaseColor


class Fire(BaseColor):
    """Thème feu - rouges, oranges, jaunes."""
    
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
        Génère des couleurs de feu selon l'intensité.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré (non utilisé)
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur de feu selon l'intensité
        """
        intensity = 1.0 - distance_to_center + y_norm * 0.3
        if intensity > 0.8:
            return (255, 255, 100)  # Jaune chaud
        elif intensity > 0.5:
            return (255, 140, 0)    # Orange
        else:
            return (220, 20, 60)    # Rouge foncé