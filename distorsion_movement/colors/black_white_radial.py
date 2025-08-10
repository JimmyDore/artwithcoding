"""
Schéma de couleur noir et blanc radial.
"""

from typing import Tuple
from .base_color import BaseColor


class BlackWhiteRadial(BaseColor):
    """Schéma noir et blanc basé sur la distance au centre."""
    
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
        Génère du noir et blanc selon la distance au centre.
        
        Les formes au centre tendent vers le blanc, celles aux bords vers le noir.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré dans la grille
            dimension: Dimension de la grille (non utilisée)
            
        Returns:
            Couleur noir ou blanc selon la distance
        """
        if distance_to_center < 0.3:
            return (255, 255, 255)  # Blanc au centre
        elif distance_to_center > 0.7:
            return (0, 0, 0)  # Noir aux bords
        else:
            # Zone intermédiaire : alternance selon l'index
            return (255, 255, 255) if (index % 2 == 0) else (0, 0, 0)