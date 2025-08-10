"""
Rendu de forme hexagonale.
"""

import pygame
import math
from typing import Tuple
from .base_shape import BaseShape


class Hexagon(BaseShape):
    """Moteur de rendu pour les hexagones."""
    
    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un hexagone régulier avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille de l'hexagone (rayon du cercle circonscrit)
            color: Couleur RGB
        """
        radius = size // 2
        corners = []
        for i in range(6):
            angle = 2 * math.pi * i / 6
            corner_x = radius * math.cos(angle)
            corner_y = radius * math.sin(angle)
            corners.append((corner_x, corner_y))
        
        rotated_corners = Hexagon._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                Hexagon._draw_fallback(surface, x, y, color)