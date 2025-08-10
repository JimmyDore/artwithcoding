"""
Rendu de forme en losange.
"""

import pygame
import math
from typing import Tuple
from .base_shape import BaseShape


class Diamond(BaseShape):
    """Moteur de rendu pour les losanges."""
    
    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un losange (carré à 45°) avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille du losange
            color: Couleur RGB
        """
        half_size = size // 2
        # Losange = carré tourné de 45°
        base_rotation = math.pi / 4  # 45 degrés
        total_rotation = rotation + base_rotation
        
        corners = [
            (-half_size, -half_size),
            (half_size, -half_size),
            (half_size, half_size),
            (-half_size, half_size)
        ]
        
        rotated_corners = Diamond._rotate_points(corners, total_rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                Diamond._draw_fallback(surface, x, y, color)