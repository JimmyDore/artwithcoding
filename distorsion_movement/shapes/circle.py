"""
Rendu de forme circulaire.
"""

import pygame
from typing import Tuple
from .base_shape import BaseShape


class Circle(BaseShape):
    """Moteur de rendu pour les cercles."""
    
    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un cercle (la rotation n'affecte pas un cercle parfait).
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians (ignorée pour les cercles)
            size: Diamètre du cercle
            color: Couleur RGB
        """
        try:
            radius = max(1, size // 2)
            pygame.draw.circle(surface, color, (int(x), int(y)), radius)
        except (TypeError, ValueError):
            # Fallback: dessiner un petit rectangle centré
            Circle._draw_fallback(surface, x, y, color)