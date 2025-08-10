"""
Rendu de forme triangulaire.
"""

import pygame
import math
from typing import Tuple
from .base_shape import BaseShape


class Triangle(BaseShape):
    """Moteur de rendu pour les triangles."""
    
    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un triangle équilatéral avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille du triangle (rayon du cercle circonscrit)
            color: Couleur RGB
        """
        radius = size // 2
        # Triangle équilatéral avec un sommet vers le haut
        corners = []
        for i in range(3):
            angle = (2 * math.pi * i / 3) - math.pi/2  # Commencer par le haut
            corner_x = radius * math.cos(angle)
            corner_y = radius * math.sin(angle)
            corners.append((corner_x, corner_y))
        
        rotated_corners = Triangle._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                Triangle._draw_fallback(surface, x, y, color)