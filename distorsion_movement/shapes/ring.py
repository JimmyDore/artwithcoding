"""
Rendu de forme en anneau.
"""

import pygame
from typing import Tuple
from .base_shape import BaseShape


class Ring(BaseShape):
    """Moteur de rendu pour les anneaux."""
    
    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int,
             color: Tuple[int, int, int], thickness_ratio: float = 0.2):
        """
        Dessine un anneau (cercle creux) avec un certain épaisseur.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians (ignorée pour un cercle parfait)
            size: Diamètre extérieur de l'anneau
            color: Couleur RGB de l'anneau
            thickness_ratio: Proportion de l'épaisseur par rapport au rayon
        """
        try:
            outer_radius = max(1, size // 2)
            thickness = max(1, int(outer_radius * thickness_ratio)) * 2
            pygame.draw.circle(surface, color, (int(x), int(y)), outer_radius, thickness)
        except (TypeError, ValueError):
            Ring._draw_fallback(surface, x, y, color)