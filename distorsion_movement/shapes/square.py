"""
Rendu de forme carrée.
"""

import pygame
from typing import Tuple
from .base_shape import BaseShape


class Square(BaseShape):
    """Moteur de rendu pour les carrés."""
    
    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un carré avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille du carré
            color: Couleur RGB
        """
        half_size = size // 2
        corners = [
            (-half_size, -half_size),
            (half_size, -half_size),
            (half_size, half_size),
            (-half_size, half_size)
        ]
        
        rotated_corners = Square._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback: dessiner un petit rectangle centré
                Square._draw_fallback(surface, x, y, color)