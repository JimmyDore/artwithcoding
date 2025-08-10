"""
Rendu de forme pentagonale.
"""

import pygame
import math
from typing import Tuple
from .base_shape import BaseShape


class Pentagon(BaseShape):
    """Moteur de rendu pour les pentagones."""
    
    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un pentagone régulier avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille du pentagone (rayon du cercle circonscrit)
            color: Couleur RGB
        """
        radius = size // 2
        corners = []
        for i in range(5):
            angle = (2 * math.pi * i / 5) - math.pi/2  # Commencer par le haut
            corner_x = radius * math.cos(angle)
            corner_y = radius * math.sin(angle)
            corners.append((corner_x, corner_y))
        
        rotated_corners = Pentagon._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                Pentagon._draw_fallback(surface, x, y, color)