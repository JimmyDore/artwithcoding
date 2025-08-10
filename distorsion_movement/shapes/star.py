"""
Rendu de forme en étoile.
"""

import pygame
import math
from typing import Tuple
from .base_shape import BaseShape


class Star(BaseShape):
    """Moteur de rendu pour les étoiles."""
    
    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine une étoile à 5 branches avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille de l'étoile (rayon du cercle circonscrit externe)
            color: Couleur RGB
        """
        outer_radius = size // 2
        inner_radius = outer_radius * 0.4  # Rayon interne plus petit
        
        corners = []
        for i in range(10):  # 5 points externes + 5 points internes
            angle = (2 * math.pi * i / 10) - math.pi/2  # Commencer par le haut
            if i % 2 == 0:  # Points externes
                radius = outer_radius
            else:  # Points internes
                radius = inner_radius
            
            corner_x = radius * math.cos(angle)
            corner_y = radius * math.sin(angle)
            corners.append((corner_x, corner_y))
        
        rotated_corners = Star._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                Star._draw_fallback(surface, x, y, color)